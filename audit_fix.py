#!/usr/bin/env python3
"""Comprehensive SEO audit fix for all pages."""
import re, os

DOMAIN = "https://wifioficialbiography.org"
BIOS_DIR = "bios"

# ── 1. Fix index.html ──
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add missing meta tags
additions = {
    '<meta property="og:image:height"': '<meta property="og:image:alt" content="Wifioficial Biography — Enciclopedia de Biografías">\n  <meta property="og:image:type" content="image/png">\n  <meta property="og:image:height"',
    '<meta name="twitter:image"': '<meta name="twitter:image:alt" content="Wifioficial Biography">\n  <meta name="twitter:site" content="@wifioficial">\n  <meta name="twitter:image"',
    '<meta name="theme-color"': '<meta name="color-scheme" content="light">\n  <meta name="theme-color"',
}
for after, insert in additions.items():
    html = html.replace(after, insert)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html: fixed")

# ── 2. Fix verify.html ──
with open('verify.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace minimal head with full head
old_head = '''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verificar Identidad — Wifioficial Biography</title>
  <meta name="robots" content="noindex, nofollow">
  <link rel="icon" type="image/jpeg" href="images/favicon.jpg">
  <link rel="shortcut icon" href="images/favicon.jpg">
  <link rel="stylesheet" href="css/style.css">'''

new_head = '''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verificar Identidad — Wifioficial Biography</title>
  <meta name="description" content="Verifica tu identidad para completar tu solicitud de biografía en Wifioficial Biography.">
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="''' + DOMAIN + '''/verify.html">
  <meta property="og:type" content="website">
  <meta property="og:url" content="''' + DOMAIN + '''/verify.html">
  <meta property="og:title" content="Verificar Identidad — Wifioficial Biography">
  <meta property="og:description" content="Verifica tu identidad para completar tu solicitud de biografía en Wifioficial Biography.">
  <meta property="og:image" content="''' + DOMAIN + '''/images/wifioficial-og.png">
  <meta property="og:image:width" content="1536">
  <meta property="og:image:height" content="1024">
  <meta property="og:image:alt" content="Wifioficial Biography">
  <meta property="og:image:type" content="image/png">
  <meta property="og:site_name" content="Wifioficial Biography">
  <meta property="og:locale" content="es_ES">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Verificar Identidad — Wifioficial Biography">
  <meta name="twitter:description" content="Verifica tu identidad para completar tu solicitud de biografía.">
  <meta name="twitter:image" content="''' + DOMAIN + '''/images/wifioficial-og.png">
  <meta name="twitter:image:alt" content="Wifioficial Biography">
  <meta name="twitter:site" content="@wifioficial">
  <meta name="theme-color" content="#0645ad">
  <meta name="color-scheme" content="light">
  <link rel="icon" type="image/jpeg" href="images/favicon.jpg">
  <link rel="shortcut icon" href="images/favicon.jpg">
  <link rel="apple-touch-icon" href="images/favicon.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="css/style.css">'''

html = html.replace(old_head, new_head)

with open('verify.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("verify.html: fixed")

# ── 3. Fix all bios ──
count_alt = 0
count_locale = 0
count_apple = 0
count_color = 0
count_preconnect = 0
count_twitter_site = 0

for fname in sorted(os.listdir(BIOS_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(BIOS_DIR, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    original = html
    slug = fname.replace('.html', '')
    name_match = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    name = name_match.group(1).strip() if name_match else slug.replace('-', ' ').title()
    
    # Get name for alt text from description
    desc_match = re.search(r'<meta name="description"[^>]+content="([^"]+)"', html)
    desc = desc_match.group(1)[:120] if desc_match else f"Biografía de {name}"
    
    # Add og:image:alt after og:image
    if 'og:image:alt' not in html:
        html = html.replace(
            '<meta property="og:image"',
            f'<meta property="og:image:alt" content="{desc}">\n  <meta property="og:image:type" content="image/jpeg">\n  <meta property="og:image"',
            1
        )
        count_alt += 1
    
    # Add og:locale after og:site_name
    if 'og:locale' not in html and 'og:site_name' in html:
        html = html.replace(
            '<meta property="og:site_name"',
            '<meta property="og:locale" content="es_ES">\n  <meta property="og:site_name"'
        )
        count_locale += 1
    
    # Add apple-touch-icon after shortcut icon
    if 'apple-touch-icon' not in html:
        html = html.replace(
            '<link rel="shortcut icon"',
            '<link rel="shortcut icon"'
        )
        html = html.replace(
            '</head>',
            '  <link rel="apple-touch-icon" href="../images/favicon.jpg">\n</head>'
        )
        count_apple += 1
    
    # Add color-scheme
    if 'color-scheme' not in html:
        html = html.replace(
            '<meta name="theme-color"',
            '<meta name="color-scheme" content="light">\n  <meta name="theme-color"'
        )
        count_color += 1
    
    # Add twitter:image:alt and twitter:site if missing
    if 'twitter:image:alt' not in html:
        html = html.replace(
            '<meta name="twitter:image"',
            '<meta name="twitter:image:alt" content="' + desc + '">\n  <meta name="twitter:site" content="@wifioficial">\n  <meta name="twitter:image"'
        )
        count_twitter_site += 1
    
    # Add preconnect if missing
    if 'preconnect' not in html:
        html = html.replace(
            '<link rel="stylesheet"',
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n  <link rel="stylesheet"'
        )
        count_preconnect += 1
    
    if html != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html)

print(f"\nBios fixed:")
print(f"  og:image:alt + og:image:type: {count_alt}")
print(f"  og:locale: {count_locale}")
print(f"  apple-touch-icon: {count_apple}")
print(f"  color-scheme: {count_color}")
print(f"  twitter:image:alt + twitter:site: {count_twitter_site}")
print(f"  preconnect: {count_preconnect}")
print("\nAll fixes applied.")
