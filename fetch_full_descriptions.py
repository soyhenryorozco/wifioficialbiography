#!/usr/bin/env python3
"""
Fetch full Wikipedia extracts for all bios via API.
Updates descriptions to be complete, non-truncated text.
Batches requests to respect Wikipedia rate limits.
"""
import os, re, json, glob, time, urllib.request, urllib.parse

BIOS_DIR = 'bios'
DELAY = 0.5  # seconds between API calls

def get_wikipedia_extract(wiki_url):
    """Fetch Wikipedia extract from a Wikipedia URL."""
    m = re.match(r'https?://([a-z]+)\.wikipedia\.org/wiki/(.+)', wiki_url)
    if not m:
        return None
    lang, title = m.group(1), urllib.parse.unquote(m.group(2))
    api_url = f'https://{lang}.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=1&explaintext=1&titles={urllib.parse.quote(title)}&redirects=1'
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'WifiOficialBio/1.0 (fixing truncated bios)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
        pages = data.get('query', {}).get('pages', {})
        for pid, pdata in pages.items():
            if pid != '-1':
                return pdata.get('extract', '')
    except Exception as e:
        return None

def update_description(fp, new_desc):
    """Update the description in a bio HTML file."""
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Update in <p itemprop="description">
    content = re.sub(
        r'(<p[^>]*itemprop="description"[^>]*>).*?(</p>)',
        lambda m: m.group(1) + new_desc + m.group(2),
        content,
        count=1
    )
    
    # Update in meta description (truncate to 160 chars for SEO)
    meta_desc = new_desc[:160] if len(new_desc) > 160 else new_desc
    content = re.sub(
        r'(<meta name="description" content=").*?(")',
        lambda m: m.group(1) + meta_desc.replace('"', '&quot;') + m.group(2),
        content,
        count=1
    )
    
    # Update og:description
    content = re.sub(
        r'(<meta property="og:description" content=").*?(")',
        lambda m: m.group(1) + meta_desc.replace('"', '&quot;') + m.group(2),
        content,
        count=1
    )
    
    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    bio_files = sorted(glob.glob(os.path.join(BIOS_DIR, '*.html')))
    total = len(bio_files)
    
    # First, find all bios that need updating (has Wikipedia URL in sameAs)
    candidates = []
    for fp in bio_files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if has Wikipedia URL
        m = re.search(r'"sameAs"\s*:\s*\[([^\]]+)\]', content)
        if not m:
            continue
        wiki_urls = re.findall(r'https?://([a-z]+)\.wikipedia\.org/wiki/[^\s"\'<>,\]]+', m.group(1))
        if not wiki_urls:
            continue
        
        # Check if description is short/truncated
        desc_m = re.search(r'<p[^>]*itemprop="description"[^>]*>(.*?)</p>', content)
        if not desc_m:
            continue
        current_desc = desc_m.group(1).strip()
        
        # Skip if already good (>= 300 chars, ends with period)
        if len(current_desc) >= 300 and current_desc.endswith('.'):
            continue
        
        candidates.append(fp)
    
    print(f'Bios needing Wikipedia fetch: {len(candidates)}/{total}')
    
    updated = 0
    errors = 0
    
    for i, fp in enumerate(candidates):
        slug = os.path.basename(fp).replace('.html', '')
        
        # Get Wikipedia URL from sameAs
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        m = re.search(r'"sameAs"\s*:\s*\[([^\]]+)\]', content)
        wiki_urls = re.findall(r'https?://([a-z]+)\.wikipedia\.org/wiki/[^\s"\'<>,\]]+', m.group(1))
        
        # Try each Wikipedia URL, prefer English
        wiki_urls.sort(key=lambda u: (0 if u.startswith('https://en.') else 1))
        
        extract = None
        for url_part in wiki_urls:
            # url_part is like "//en.wikipedia.org/wiki/Shakira"
            url = 'https:' + url_part if url_part.startswith('//') else url_part
            if not url.startswith('http'):
                url = 'https://' + url
            extract = get_wikipedia_extract(url)
            if extract:
                break
            time.sleep(DELAY)
        
        if extract:
            # Clean up extract - remove references like [1], [2], etc.
            extract = re.sub(r'\[\d+\]', '', extract)
            extract = re.sub(r'\s+', ' ', extract).strip()
            
            # Take first paragraph (up to first double newline or 500 chars)
            first_para = extract.split('\n\n')[0].strip()
            if len(first_para) < 100:
                first_para = extract[:500].strip()
            
            # Ensure it ends with a period
            if not first_para.endswith('.'):
                last_period = first_para.rfind('.')
                if last_period > 50:
                    first_para = first_para[:last_period+1]
                else:
                    first_para += '.'
            
            if update_description(fp, first_para):
                updated += 1
                if updated % 50 == 0:
                    print(f'  Updated {updated}/{len(candidates)}...')
            else:
                errors += 1
        else:
            errors += 1
        
        if i % 10 == 0:
            time.sleep(DELAY)
    
    print(f'\nDone! Updated: {updated}, Errors: {errors}')

if __name__ == '__main__':
    main()
