#!/usr/bin/env python3
"""Add ProfilePage schema, improve alt text, add related links across all bios."""
import re, json, os

BIOS_DIR = "bios"
DOMAIN = "https://wifioficialbiography.org"
stats = {"profilepage": 0, "alt_fixed": 0, "related_links": 0}

for fname in sorted(os.listdir(BIOS_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BIOS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    slug = fname.replace('.html', '')
    name_match = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    name = name_match.group(1).strip() if name_match else slug.replace('-', ' ').title()
    desc_match = re.search(r'<meta name="description"[^>]+content="([^"]+)"', html)
    desc = desc_match.group(1) if desc_match else f"Complete biography of {name}"
    img_match = re.search(r'<img[^>]+src="([^"]+)"', html)
    img = img_match.group(1) if img_match else ""

    original = html

    # ── 1. Add ProfilePage schema wrapping Person ──────────
    # Find the Person JSON-LD
    person_match = re.search(r'<script type="application/ld\+json">\s*(\{.*?"@type":\s*"Person".*?\})\s*</script>', html, re.DOTALL)
    if person_match and '"ProfilePage"' not in html:
        person_json_str = person_match.group(1)
        try:
            person_data = json.loads(person_json_str)
            profile_page = {
                "@context": "https://schema.org",
                "@type": "ProfilePage",
                "headline": f"{name} — Biography",
                "description": desc,
                "url": f"{DOMAIN}/bios/{fname}",
                "mainEntity": person_data,
                "dateCreated": "2026-07-12",
                "dateModified": "2026-07-12",
                "author": {"@type": "Organization", "name": "Wifi Oficial Biography"},
                "publisher": {"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/images/favicon.jpg"}},
            }
            if img:
                profile_page["image"] = img
            pp_html = f'\n  <script type="application/ld+json">\n  {json.dumps(profile_page, indent=2, ensure_ascii=False)}\n  </script>'
            # Insert after Person block
            html = html.replace(person_match.group(0), person_match.group(0) + pp_html)
            stats["profilepage"] += 1
        except:
            pass

    # ── 2. Fix alt text on main image ──────────────────────
    main_img = re.search(r'(<img[^>]+src="([^"]+)"[^>]*)alt="Photo of ([^"]+)"', html)
    if main_img:
        old_alt = f'alt="Photo of {main_img.group(3)}"'
        # Try to get description from meta
        desc_short = desc[:120] if desc else f"Biografía de {name}"
        new_alt = f'alt="{name} — {desc_short}"'
        html = html.replace(old_alt, new_alt, 1)
        stats["alt_fixed"] += 1

    # ── 3. Add related profiles links section ──────────────
    if 'id="related"' not in html and 'id="external-links"' not in html:
        # Check if profile has social media links to use as related
        social_links = re.findall(r'(https://(?:www\.)?(instagram\.com|facebook\.com|tiktok\.com|twitter\.com|x\.com|youtube\.com)[^"\']+)', html)
        if social_links:
            related_html = '\n\n        <h2 id="related">Perfiles Relacionados</h2>\n        <ul>\n'
            platforms_used = set()
            for url, domain in social_links[:6]:
                domain_name = {'instagram.com': 'Instagram', 'facebook.com': 'Facebook', 'tiktok.com': 'TikTok', 'twitter.com': 'X (Twitter)', 'x.com': 'X (Twitter)', 'youtube.com': 'YouTube'}
                label = domain_name.get(domain, domain)
                if label not in platforms_used:
                    platforms_used.add(label)
                    related_html += f'          <li><a href="{url}" target="_blank" rel="noopener">{label}</a></li>\n'
            related_html += '        </ul>\n'
            
            # Insert before References or at end of article
            ref_match = re.search(r'<h2 id="references"', html)
            if ref_match:
                pos = ref_match.start()
                html = html[:pos] + related_html + html[pos:]
                stats["related_links"] += 1

    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

print("=== SEO Enhancement Complete ===")
print(f"ProfilePage added: {stats['profilepage']}")
print(f"Alt text fixed: {stats['alt_fixed']}")
print(f"Related links added: {stats['related_links']}")
