#!/usr/bin/env python3
"""Generate 494 Colombian famous people biographies."""
import json, os, re, hashlib, urllib.parse, urllib.request, time

BIOS_DIR = "bios"
DOMAIN = "https://wifioficialbiography.org"
FNAME = "colombian_bios_ready.json"

def slugify(name):
    s = name.lower().replace(' ', '-')
    s = re.sub(r'[^a-z0-9\-]', '', s)
    s = s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace('ü','u')
    return s

# Load data
with open(FNAME, 'r') as f:
    bios = json.load(f)

total = len(bios)
print(f"Generating {total} bios...")

generated = 0
skipped = 0

for idx, bio in enumerate(bios):
    name = bio['name']
    slug = bio['slug']
    desc = bio['description'][:300]
    img = bio['image']
    birth = bio['birthDate']
    occupation = bio['occupation']
    category = bio['category']
    item_id = bio['item_id']
    wiki_url = bio['wikipedia']
    
    fname = f"{slug}.html"
    fpath = os.path.join(BIOS_DIR, fname)
    
    if os.path.exists(fpath):
        skipped += 1
        continue
    
    # Extract year from birth date
    birth_year = birth[:4] if birth else ""
    
    # Generate profession from occupation
    job_titles = occupation if occupation else "Professional"
    if isinstance(job_titles, str):
        job_titles = job_titles
    
    # Description for meta
    meta_desc = desc[:200] if desc else f"Complete biography of {name}"
    
    # Skip Wikipedia API (too slow) - use Wikidata description only
    full_desc = desc[:400] if desc else f"Colombian {job_titles.lower()}."
    
    # Create categories similar to Henry Orozco style
    cat_labels = {
        'footballer': ['Footballer', 'Soccer', 'Colombia', 'Athlete'],
        'singer': ['Singer', 'Musician', 'Colombia', 'Latin Music'],
        'actor': ['Actor', 'Colombia', 'Latin America', 'Entertainment'],
        'politician': ['Politician', 'Colombia', 'Public Figure', 'Leader'],
        'journalist': ['Journalist', 'Colombia', 'Media', 'Communication'],
        'writer': ['Writer', 'Author', 'Colombia', 'Literature'],
        'model': ['Model', 'Colombia', 'Fashion', 'Latin America'],
        'business': ['Entrepreneur', 'Business', 'Colombia', 'Innovation'],
        'director': ['Director', 'Filmmaker', 'Colombia', 'Cinema'],
        'cyclist': ['Cyclist', 'Colombia', 'Sports', 'Athlete'],
        'tennis': ['Tennis Player', 'Colombia', 'Sports', 'Athlete'],
        'basketball': ['Basketball Player', 'Colombia', 'Sports', 'Athlete'],
        'baseball': ['Baseball Player', 'Colombia', 'Sports', 'Athlete'],
        'boxer': ['Boxer', 'Colombia', 'Sports', 'Athlete'],
        'comedian': ['Comedian', 'Colombia', 'Comedy', 'Entertainment'],
        'tv': ['TV Host', 'Colombia', 'Television', 'Media'],
        'chef': ['Chef', 'Colombia', 'Gastronomy', 'Culinary'],
        'tech': ['Technologist', 'Colombia', 'Innovation', 'Tech'],
        'sports': ['Athlete', 'Colombia', 'Sports', 'Competitor'],
    }
    tags = cat_labels.get(category, ['Colombia', 'Public Figure', category])
    cat_en = category
    
    # Birth place - can't get from Wikidata query easily
    birth_place = "Colombia"
    
    # HTML content using Henry Orozco template structure
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{name} — {job_titles} | Wifi Oficial Biography</title>
  <meta name="description" content="{meta_desc}">
  <meta name="keywords" content="{name}, {', '.join(tags[:4])}, biography, Colombian, famous">
  <meta name="author" content="Wifi Oficial Biography">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="{DOMAIN}/bios/{fname}">

  <meta property="og:type" content="profile">
  <meta property="og:url" content="{DOMAIN}/bios/{fname}">
  <meta property="og:title" content="{name} — {job_titles}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:image:alt" content="{name} — {job_titles}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:site_name" content="Wifi Oficial Biography">
  <meta property="og:locale" content="es_ES">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{name} — {job_titles}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:image" content="{img}">
  <meta name="twitter:image:alt" content="{name} — {job_titles}">
  <meta name="twitter:site" content="@wifioficial">

  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0645ad">
  <meta name="article:author" content="https://wifioficialbiography.org/">
  <meta name="article:published_time" content="2026-07-13T00:00:00+00:00">
  <meta name="article:modified_time" content="2026-07-13T00:00:00+00:00">
  <meta name="article:section" content="Biography">
  <meta name="article:tag" content="{name}">
  <meta name="article:tag" content="{tags[0]}">
  <meta name="article:tag" content="Colombia">
  <link rel="alternate" hreflang="en" href="{DOMAIN}/bios/{fname}">
  <link rel="alternate" hreflang="es" href="{DOMAIN}/bios/{fname}">
  <link rel="alternate" hreflang="x-default" href="{DOMAIN}/bios/{fname}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
  <link rel="shortcut icon" href="../images/favicon.jpg">
  <link rel="apple-touch-icon" href="../images/favicon.jpg">
  <link rel="stylesheet" href="../css/style.css">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "{name}",
    "description": "{full_desc}",
    "birthDate": "{birth}",
    "nationality": {{
      "@type": "Country",
      "name": "Colombia"
    }},
    "jobTitle": "{job_titles}",
    "url": "{DOMAIN}/bios/{fname}",
    "image": "{img}",
    "sameAs": [],
    "knowsAbout": {json.dumps(tags)},
    "knowsLanguage": ["Spanish"]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ProfilePage",
    "headline": "{name} — Biography",
    "description": "{meta_desc}",
    "url": "{DOMAIN}/bios/{fname}",
    "mainEntity": {{
      "@type": "Person",
      "name": "{name}"
    }},
    "dateCreated": "2026-07-13",
    "dateModified": "2026-07-13",
    "author": {{
      "@type": "Organization",
      "name": "Wifi Oficial Biography"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "Wifi Oficial Biography",
      "logo": {{
        "@type": "ImageObject",
        "url": "{DOMAIN}/images/favicon.jpg",
        "name": "Wifi Oficial Biography Logo",
        "caption": "Wifi Oficial Biography Logo",
        "copyrightNotice": "© 2026 Wifi Oficial Biography",
        "acquireLicensePage": "{DOMAIN}/about",
        "creditText": "Wifi Oficial Biography",
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": {{"@type": "Organization", "name": "Wifi Oficial Biography"}}
      }}
    }},
    "image": "{img}"
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "{DOMAIN}/"}},
      {{"@type": "ListItem", "position": 2, "name": "Biografías", "item": "{DOMAIN}/#biografias"}},
      {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "{DOMAIN}/bios/{fname}"}}
    ]
  }}
  </script>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{name} — Biography",
    "description": "{meta_desc}",
    "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
    "publisher": {{
      "@type": "Organization",
      "name": "Wifi Oficial Biography",
      "logo": {{"@type": "ImageObject", "url": "{DOMAIN}/images/favicon.jpg"}}
    }},
    "datePublished": "2026-07-13",
    "dateModified": "2026-07-13",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "{DOMAIN}/bios/{fname}"}},
    "image": "{img}",
    "creator": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
    "copyrightNotice": "© 2026 Wifi Oficial Biography. All rights reserved.",
    "acquireLicensePage": "{DOMAIN}/about"
  }}
  </script>

</head>
<body>

  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="../index.html" class="site-logo" aria-label="Wifi Oficial Biography - Inicio">
        <img src="../images/favicon.jpg" alt="Wifi Oficial Biography" class="logo-icon" width="32" height="32" style="border-radius:50%;">
        <div class="logo-text">Wifioficial <span>Biography</span></div>
      </a>
      <nav class="main-nav" id="mainNav" role="navigation" aria-label="Main navigation">
        <ul>
          <li><a href="../index.html">Inicio</a></li>
          <li><a href="../index.html#biografias">Biografías</a></li>
          <li><a href="../index.html#categorias">Categorías</a></li>
          <li><a href="../index.html#about">Acerca de</a></li>
        </ul>
      </nav>
      <div class="header-search">
        <input type="search" id="headerSearchInput" placeholder="Buscar biografía..." aria-label="Buscar biografía">
        <button id="searchBtn" aria-label="Buscar">Buscar</button>
      </div>
      <button class="menu-toggle" id="menuToggle" aria-label="Abrir menú">☰</button>
    </div>
  </header>

  <div class="search-overlay" id="searchOverlay" role="dialog" aria-label="Búsqueda">
    <div class="search-box">
      <input type="search" id="searchOverlayInput" placeholder="Buscar biografía..." aria-label="Buscar biografía" autocomplete="off">
      <div class="search-results" id="searchResults"></div>
      <div style="padding:.5rem 1.25rem;border-top:1px solid #eee;text-align:right;">
        <button onclick="document.getElementById('searchOverlay').classList.remove('active')" style="background:none;border:1px solid #ccc;padding:.3rem .8rem;border-radius:3px;cursor:pointer;font-size:.85rem;">Cerrar (Esc)</button>
      </div>
    </div>
  </div>

  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">

      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <a href="../index.html">Inicio</a>
        <span class="separator">›</span>
        <a href="../index.html#biografias">Biografías</a>
        <span class="separator">›</span>
        <span>{name}</span>
      </nav>

      <div class="bio-page-header">
        <div class="bio-page-photo">
          <img src="{img}" alt="{name} — {job_titles}" title="{name}" width="220" height="275" loading="eager" fetchpriority="high" itemprop="image">
        </div>
        <div class="bio-page-info">
          <h1 itemprop="name">{name}</h1>
          <div class="subtitle" itemprop="alternateName">{job_titles}</div>
          <p itemprop="description" style="font-size:.95rem;line-height:1.6;">{full_desc[:300]}</p>
        </div>
      </div>

      <div class="infobox" role="complementary" aria-label="Personal information">
        <div class="infobox-header">{name}</div>
        <div class="infobox-image">
          <img src="{img}" alt="{name}" title="{name}" width="300" height="375" loading="lazy">
        </div>
        <table>
          <tbody>
            <tr><th>Full Name</th><td itemprop="birthName">{name}</td></tr>
            <tr><th>Born</th><td><span itemprop="birthDate" content="{birth}">{birth}</span><br><span itemprop="birthPlace">Colombia</span></td></tr>
            <tr><th>Nationality</th><td itemprop="nationality">Colombian</td></tr>
            <tr><th>Occupation(s)</th><td itemprop="jobTitle">{job_titles}</td></tr>
            <tr><th>Known for</th><td>{', '.join(tags[:3])}</td></tr>
          </tbody>
        </table>
      </div>

      <nav class="toc" aria-label="Table of contents">
        <div class="toc-title">Contents</div>
        <ol>
          <li><a href="#biography">Biography</a></li>
          <li><a href="#career">Career</a></li>
          <li><a href="#references">References</a></li>
          <li><a href="#external-links">External Links</a></li>
        </ol>
      </nav>

      <article class="bio-article">

        <div class="category-tags">
          {''.join(f'<a href="#" class="category-tag">{t}</a>' for t in tags[:4])}
        </div>

        <p><strong>{name}</strong> (born {birth}) is a Colombian {job_titles.lower()}.</p>

        <p>{full_desc}</p>

        <h2 id="career">Career</h2>
        <p>{name} is a Colombian professional recognized in the field of {job_titles.lower()}. {full_desc[:200]}</p>

        <h2 id="references">References</h2>
        <ol>
          <li><a href="{wiki_url}" target="_blank" rel="noopener">Wikipedia — {name}</a></li>
          <li><a href="https://www.wikidata.org/wiki/{item_id}" target="_blank" rel="noopener">Wikidata — {item_id}</a></li>
        </ol>

        <h2 id="external-links">External Links</h2>
        <ul>
          <li><a href="{wiki_url}" target="_blank" rel="noopener">Wikipedia</a></li>
          <li><a href="https://www.wikidata.org/wiki/{item_id}" target="_blank" rel="noopener">Wikidata</a></li>
        </ul>

      </article>
    </main>
  </div>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <div class="logo-icon" aria-hidden="true">W</div>
        <div class="logo-text">Wifioficial <span>Biography</span></div>
      </div>
      <div class="footer-links">
        <a href="../index.html">Inicio</a>
        <a href="../index.html#biografias">Biografías</a>
        <a href="../index.html#categorias">Categorías</a>
        <a href="../index.html#about">Acerca de</a>
      </div>
      <div class="footer-copy">&copy; 2026 Wifi Oficial Biography. All rights reserved.</div>
    </div>
  </footer>

  <script src="../js/app.js"></script>
</body>
</html>'''

    # Fix JSON-LD curly braces (Python f-string escaping)
    html = html.replace('{{', '{').replace('}}', '}')
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    generated += 1
    if generated % 25 == 0:
        print(f"  {generated}/{total} generated...")

print(f"\nDone! Generated: {generated}, Skipped: {skipped}, Total: {total}")
print(f"Files in bios/: {len([f for f in os.listdir('bios') if f.endswith('.html')])}")
