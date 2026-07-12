#!/usr/bin/env python3
"""
Enhance schema.org markup, hreflang, and Twitter card tags across all bio files.
"""
import re, os, json, time

BIOS_DIR = "bios"
DOMAIN = "https://wifioficial-biography.com"

# Track stats
stats = {"breadcrumb_added": 0, "article_added": 0, "hreflang_added": 0, "twitter_fixed": 0}

def extract_data(html, fname):
    """Extract available data from bio HTML for schema generation."""
    name = ""
    description = ""
    image = ""
    job_title = ""

    m = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    if m: name = m.group(1).strip()

    m = re.search(r'<meta name="description"[^>]+content="([^"]+)"', html)
    if m: description = m.group(1)

    m = re.search(r'<img[^>]+src="([^"]+)"', html)
    if m: image = m.group(1)

    m = re.search(r'"jobTitle":\s*"([^"]+)"', html)
    if m: job_title = m.group(1)

    return {"name": name, "description": description, "image": image, "job_title": job_title}

def add_breadcrumb(html, fname):
    """Add BreadcrumbList schema if missing."""
    if '"BreadcrumbList"' in html:
        return html
    data = extract_data(html, fname)
    name = data["name"] or fname.replace(".html", "").replace("-", " ").title()

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{DOMAIN}/"},
            {"@type": "ListItem", "position": 2, "name": "Biografías", "item": f"{DOMAIN}/#biografias"},
            {"@type": "ListItem", "position": 3, "name": name, "item": f"{DOMAIN}/bios/{fname}"}
        ]
    }
    schema_html = f'\n  <script type="application/ld+json">\n  {json.dumps(schema, indent=2, ensure_ascii=False)}\n  </script>'
    html = html.replace('</head>', f'{schema_html}\n</head>')
    stats["breadcrumb_added"] += 1
    return html

def add_article(html, fname):
    """Add Article schema if missing."""
    if '"Article"' in html:
        return html
    data = extract_data(html, fname)
    name = data["name"] or fname.replace(".html", "").replace("-", " ").title()
    desc = data["description"] or f"Complete biography of {name}"
    img = data["image"] or ""

    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{name} — Biography",
        "description": desc,
        "author": {"@type": "Organization", "name": "Wifioficial Biography"},
        "publisher": {"@type": "Organization", "name": "Wifioficial Biography", "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/images/favicon.jpg"}},
        "datePublished": "2026-07-12",
        "dateModified": "2026-07-12",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{DOMAIN}/bios/{fname}"},
    }
    if img:
        article["image"] = img

    schema_html = f'\n  <script type="application/ld+json">\n  {json.dumps(article, indent=2, ensure_ascii=False)}\n  </script>'
    html = html.replace('</head>', f'{schema_html}\n</head>')
    stats["article_added"] += 1
    return html

def add_hreflang(html):
    """Add hreflang tags if missing."""
    if 'hreflang' in html:
        return html
    m = re.search(r'<link rel="canonical"[^>]+href="([^"]+)"', html)
    if not m:
        return html
    url = m.group(1)

    tags = f'\n  <link rel="alternate" hreflang="en" href="{url}">\n  <link rel="alternate" hreflang="es" href="{url}">\n  <link rel="alternate" hreflang="x-default" href="{url}">'
    html = html.replace('</head>', f'{tags}\n</head>')
    stats["hreflang_added"] += 1
    return html

def fix_twitter_card(html, fname):
    """Ensure Twitter card tags exist."""
    if 'twitter:title' in html:
        return html
    data = extract_data(html, fname)
    name = data["name"] or fname.replace(".html", "").replace("-", " ").title()
    desc = data["description"] or f"Biografía de {name}"
    img = data["image"] or f"{DOMAIN}/images/favicon.jpg"

    # Find where to insert - after canonical or after og:image
    insert_point = re.search(r'(<meta property="og:image[^>]*>)', html)
    if not insert_point:
        insert_point = re.search(r'(<link rel="canonical"[^>]*>)', html)
    if not insert_point:
        return html

    tags = f'\n  <meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="{name} — Biography | Wifioficial">\n  <meta name="twitter:description" content="{desc[:200]}">\n  <meta name="twitter:image" content="{img}">'

    pos = insert_point.end()
    html = html[:pos] + tags + html[pos:]
    stats["twitter_fixed"] += 1
    return html

# Process all bios
for fname in sorted(os.listdir(BIOS_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BIOS_DIR, fname)

    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    html = add_breadcrumb(html, fname)
    html = add_article(html, fname)
    html = add_hreflang(html)
    html = fix_twitter_card(html, fname)

    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

print("=== Schema Enhancement Complete ===")
print(f"BreadcrumbList added: {stats['breadcrumb_added']}")
print(f"Article added: {stats['article_added']}")
print(f"hreflang added: {stats['hreflang_added']}")
print(f"Twitter cards fixed: {stats['twitter_fixed']}")
