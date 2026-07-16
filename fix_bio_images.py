#!/usr/bin/env python3
"""Fix bios using generic Shakira fallback image or missing images.
Queries Wikipedia API for each person's main image and updates bio files."""

import os, re, json, urllib.request, urllib.parse, time, sys

BIOS_DIR = "bios"
SHAKIRA_FALLBACK = "2023-11-16_Gala_de_los_Latin_Grammy%2C_03_%28cropped%2902.jpg"
USER_AGENT = "WifioficialBio/1.0 (https://wifioficialbiography.org; fix-bio-images)"
DELAY = 0.6  # seconds between API calls

def get_wikipedia_image(name):
    """Query Wikipedia API for the main image of a person."""
    params = {
        'action': 'query',
        'titles': name,
        'prop': 'pageimages',
        'format': 'json',
        'pithumbsize': 800
    }
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        pages = data.get('query', {}).get('pages', {})
        for pid, page in pages.items():
            if pid != '-1' and 'thumbnail' in page:
                img = page['thumbnail']['source']
                # Convert thumbnail to full-res URL
                img = re.sub(r'/thumb/', '/', img)
                img = re.sub(r'/\d+px-[^/]+$', '', img)
                return img
            if pid != '-1':
                # Page exists but no image - might need a different title
                return None
    except Exception as e:
        return None
    return None

def search_wikipedia_image(name):
    """Search Wikipedia for the person and try to get an image."""
    params = {
        'action': 'query',
        'list': 'search',
        'srsearch': name,
        'format': 'json',
        'srlimit': 1,
        'srprop': ''
    }
    url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        pages = data.get('query', {}).get('search', [])
        if pages:
            title = pages[0]['title']
            time.sleep(DELAY / 2)
            return get_wikipedia_image(title)
    except:
        pass
    return None

def update_bio_image(filepath, new_image_url):
    """Update all image references in a bio file."""
    with open(filepath) as f:
        content = f.read()
    
    original = content
    
    shakira_pattern = re.escape(SHAKIRA_FALLBACK).replace(r'\%', '%')
    # Replace Shakira fallback in meta tags and img tags
    content = re.sub(
        r'(https://upload\.wikimedia\.org/[^"\']*?)' + shakira_pattern,
        new_image_url,
        content
    )
    
    # Replace empty og:image with new image
    content = re.sub(
        r'(<meta[^>]+property="og:image"[^>]+content=")(")',
        r'\g<1>' + new_image_url + r'"',
        content
    )
    
    # Replace empty twitter:image with new image
    content = re.sub(
        r'(<meta[^>]+name="twitter:image"[^>]+content=")(")',
        r'\g<1>' + new_image_url + r'"',
        content
    )
    
    # Replace itemprop="image" empty content
    content = re.sub(
        r'(<meta[^>]+itemprop="image"[^>]+content=")(")',
        r'\g<1>' + new_image_url + r'"',
        content
    )
    
    # Replace favicon.jpg img src with new image
    content = re.sub(
        r'(<img[^>]+src=")\.\./images/favicon\.jpg(")',
        r'\g<1>' + new_image_url + r'"',
        content
    )
    
    # Replace Shakira fallback in JSON-LD image fields
    content = re.sub(
        r'("image"\s*:\s*")https://upload\.wikimedia\.org/[^"\']*?' + shakira_pattern.replace('.', r'\.') + r'(")',
        r'\g<1>' + new_image_url + r'\g<2>',
        content
    )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    print("=== Bio Image Fixer ===")
    print(f"Scanning {BIOS_DIR}/ for bios with Shakira fallback or empty images...\n")
    
    # Find all bios needing fixes
    target_bios = []
    for f in sorted(os.listdir(BIOS_DIR)):
        if not f.endswith('.html'): continue
        path = os.path.join(BIOS_DIR, f)
        content = open(path).read()
        
        needs_fix = False
        if SHAKIRA_FALLBACK in content:
            needs_fix = True
        else:
            # Check for empty og:image
            m = re.search(r'<meta[^>]+property="og:image"[^>]+content="("?)"', content)
            if m and not m.group(1):
                needs_fix = True
        
        if needs_fix:
            m = re.search(r'<h1[^>]*>(.*?)</h1>', content)
            name = m.group(1) if m else f.replace('.html', '').replace('-', ' ').title()
            # Strip HTML entities
            name = re.sub(r'&#[xX]27;', "'", name)
            name = re.sub(r'&amp;', '&', name)
            name = re.sub(r'&quot;', '"', name)
            target_bios.append((f, name))
    
    total = len(target_bios)
    print(f"Found {total} bios needing images\n")
    
    if total == 0:
        print("Nothing to fix!")
        return
    
    fixed = 0
    skipped_api = 0
    not_found = 0
    
    for i, (f, name) in enumerate(target_bios):
        path = os.path.join(BIOS_DIR, f)
        
        print(f"[{i+1}/{total}] {name}...", end=" ", flush=True)
        
        # Try exact name first, then search
        img = get_wikipedia_image(name)
        if not img:
            time.sleep(DELAY * 0.3)
            img = search_wikipedia_image(name)
        
        if img:
            ok = update_bio_image(path, img)
            if ok:
                fixed += 1
                print(f"OK -> {img.split('/')[-1][:50]}")
            else:
                print(f"SKIP (no change needed)")
                skipped_api += 1
        else:
            not_found += 1
            print(f"NO IMAGE FOUND")
        
        time.sleep(DELAY)
    
    print(f"\n=== RESULTS ===")
    print(f"Fixed: {fixed}")
    print(f"No image found: {not_found}")
    print(f"Skipped: {skipped_api}")
    print(f"Total processed: {total}")

if __name__ == '__main__':
    main()
