#!/usr/bin/env python3
"""Second pass: fix remaining bios with Shakira fallback or empty images.
Uses Wikipedia search to find correct page titles for disambiguated names."""

import os, re, json, urllib.request, urllib.parse, time, sys

BIOS_DIR = "bios"
SHAKIRA = "2023-11-16_Gala_de_los_Latin_Grammy%2C_03_%28cropped%2902.jpg"
UA = "WifioficialBio/2.0 (https://wifioficialbiography.org; fix-bio-images-pass2)"

def wiki_api(params):
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=15).read())
    except:
        return None

def find_image(name):
    # Try exact
    data = wiki_api({'action': 'query', 'titles': name, 'prop': 'pageimages', 'format': 'json', 'pithumbsize': 800})
    if data:
        for pid, page in data.get('query', {}).get('pages', {}).items():
            if pid != '-1' and 'thumbnail' in page:
                img = page['thumbnail']['source']
                img = re.sub(r'/thumb/', '/', img)
                img = re.sub(r'/\d+px-[^/]+$', '', img)
                return img
    time.sleep(0.3)
    
    # Search Wikipedia
    data = wiki_api({'action': 'query', 'list': 'search', 'srsearch': name, 'format': 'json', 'srlimit': 3})
    if data:
        for r in data.get('query', {}).get('search', []):
            title = r['title']
            data2 = wiki_api({'action': 'query', 'titles': title, 'prop': 'pageimages', 'format': 'json', 'pithumbsize': 800})
            time.sleep(0.3)
            if data2:
                for pid, page in data2.get('query', {}).get('pages', {}).items():
                    if pid != '-1' and 'thumbnail' in page:
                        img = page['thumbnail']['source']
                        img = re.sub(r'/thumb/', '/', img)
                        img = re.sub(r'/\d+px-[^/]+$', '', img)
                        return img
    return None

def update_bio(path, img):
    content = open(path).read()
    original = content
    
    # Replace Shakira fallback
    content = re.sub(r'https://upload\.wikimedia\.org/[^"\'<>]*?' + re.escape(SHAKIRA), img, content)
    
    # Replace empty og:image
    content = re.sub(r'(<meta[^>]+property="og:image"[^>]+content=")(")', r'\1' + img + '"', content)
    content = re.sub(r'(<meta[^>]+name="twitter:image"[^>]+content=")(")', r'\1' + img + '"', content)
    content = re.sub(r'(<meta[^>]+itemprop="image"[^>]+content=")(")', r'\1' + img + '"', content)
    
    # Replace favicon img src
    content = re.sub(r'(<img[^>]+src=")\.\./images/favicon\.jpg(")', r'\1' + img + '"', content)
    
    if content != original:
        open(path, 'w').write(content)
        return True
    return False

def main():
    print("=== Bio Image Fixer - Pass 2 ===\n")
    
    targets = []
    for f in sorted(os.listdir(BIOS_DIR)):
        if not f.endswith('.html'): continue
        path = os.path.join(BIOS_DIR, f)
        content = open(path).read()
        
        needs = SHAKIRA in content
        if not needs:
            m = re.search(r'<meta[^>]+property="og:image"[^>]+content="("?)"', content)
            if m and not m.group(1):
                needs = True
                
        if needs:
            m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
            name = m.group(1) if m else f.replace('.html','').replace('-',' ').title()
            name = re.sub(r'&#x27;', "'", name, flags=re.I)
            name = name.replace('&amp;', '&').replace('&quot;', '"')
            targets.append((f, name))
    
    total = len(targets)
    print(f"Found {total} remaining bios needing images\n")
    
    fixed = 0
    for i, (f, name) in enumerate(targets):
        path = os.path.join(BIOS_DIR, f)
        print(f"[{i+1}/{total}] {name}...", end=" ", flush=True)
        
        img = find_image(name)
        if img:
            if update_bio(path, img):
                fixed += 1
                print(f"OK -> {img.split('/')[-1][:50]}")
            else:
                print("SKIP")
        else:
            print("NO IMAGE")
        
        time.sleep(0.5)
    
    print(f"\n=== RESULTS ===")
    print(f"Fixed: {fixed}")
    print(f"Still missing: {total - fixed}")

if __name__ == '__main__':
    main()
