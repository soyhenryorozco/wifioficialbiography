import urllib.request, urllib.parse, json, re, os, glob, time

BIOS_DIR = 'bios'
desc_pat = re.compile(r'<p[^>]*itemprop="description"[^>]*>(.*?)</p>', re.DOTALL)

candidates = []
for fp in sorted(glob.glob(os.path.join(BIOS_DIR, '*.html'))):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    m = re.search(r'"sameAs"\s*:\s*\[([^\]]+)\]', c)
    if not m:
        continue
    wiki_urls = re.findall(r'https?://([a-z]+)\.wikipedia\.org/wiki/([^\s"\'<>,\]]+)', m.group(1))
    if not wiki_urls:
        continue
    desc_m = desc_pat.search(c)
    current = desc_m.group(1).strip() if desc_m else ''
    if len(current) >= 300 and current.endswith('.'):
        continue
    slug = os.path.basename(fp).replace('.html', '')
    candidates.append((slug, fp, wiki_urls[0]))

print(f'Candidates: {len(candidates)}')

# Use REST API: https://en.wikipedia.org/api/rest_v1/page/summary/Title
# Different rate limit bucket than action API
from collections import defaultdict
by_lang = defaultdict(list)
for slug, fp, (lang, raw_title) in candidates:
    by_lang[lang].append((slug, fp, urllib.parse.unquote(raw_title)))

updated, errors, skipped = 0, 0, 0

for lang in sorted(by_lang):
    entries = by_lang[lang]
    print(f'\n{lang}.wikipedia.org — {len(entries)} titles')
    
    for idx, (slug, fp, title) in enumerate(entries):
        api_url = f'https://{lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}'
        
        try:
            req = urllib.request.Request(api_url, headers={
                'User-Agent': 'WifiOficialBio/3.0 (https://wifioficialbiography.org)'
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            
            extract = data.get('extract', '')
            if not extract:
                errors += 1
                if idx % 50 == 0:
                    print(f'  {idx}/{len(entries)} — {updated} upd, {errors} err, {skipped} skip')
                time.sleep(0.3)
                continue
            
            extract = re.sub(r'\[\d+\]', '', extract)
            extract = re.sub(r'\s+', ' ', extract).strip()
            first_para = extract.split('\n')[0].strip()
            if len(first_para) < 80:
                first_para = extract[:400].strip()
            if not first_para.endswith('.'):
                lp = first_para.rfind('.')
                first_para = first_para[:lp+1] if lp > 50 else first_para + '.'
            
            # Safety: name should appear
            name_words = [w for w in slug.replace('-', ' ').title().split() if len(w) > 3]
            if name_words and not any(w.lower() in first_para.lower() for w in name_words):
                skipped += 1
                time.sleep(0.3)
                continue
            
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            orig = content
            
            content = re.sub(
                r'(<p[^>]*itemprop="description"[^>]*>).*?(</p>)',
                lambda m: m.group(1) + first_para + m.group(2),
                content, count=1, flags=re.DOTALL
            )
            meta = first_para[:160].replace('"', '&quot;')
            for attr in ['name="description"', 'property="og:description"']:
                content = re.sub(
                    rf'({attr} content=").*?(")',
                    lambda m: m.group(1) + meta + m.group(2),
                    content, count=1
                )
            if content != orig:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
        
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(5)
            errors += 1
        except Exception:
            errors += 1
        
        time.sleep(0.3)
        if idx % 100 == 99:
            print(f'  {idx+1}/{len(entries)} — {updated} upd, {errors} err, {skipped} skip')

print(f'\nDone! Updated: {updated}, Errors: {errors}, Skipped (safety): {skipped}')
