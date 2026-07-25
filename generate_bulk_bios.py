#!/usr/bin/env python3
"""
Bulk biography generator using Wikipedia categories.
Fetches top figures from key categories and generates bios.
"""
import urllib.request, urllib.parse, json, re, os, glob, time, html as html_mod

BIOS_DIR = 'bios'
EXISTING = set()
for fp in glob.glob(os.path.join(BIOS_DIR, '*.html')):
    EXISTING.add(os.path.basename(fp).replace('.html', ''))

# === Wikipedia categories to fetch (most notable figures) ===
CATEGORIES = [
    # USA
    ("American_male_singers", "singer", "Singer"),
    ("American_female_singers", "singer", "Singer"),
    ("American_male_film_actors", "actor", "Actor"),
    ("American_female_film_actors", "actor", "Actress"),
    ("American_rappers", "singer", "Rapper"),
    
    # UK/Europe
    ("English_male_singers", "singer", "Singer"),
    ("English_female_singers", "singer", "Singer"),
    ("English_male_film_actors", "actor", "Actor"),
    ("English_female_film_actors", "actor", "Actress"),
    ("French_male_actors", "actor", "Actor"),
    ("French_female_actors", "actor", "Actress"),
    ("German_male_actors", "actor", "Actor"),
    ("German_female_actors", "actor", "Actress"),
    ("Spanish_male_singers", "singer", "Singer"),
    ("Spanish_female_singers", "singer", "Singer"),
    ("Italian_male_singers", "singer", "Singer"),
    ("Italian_female_singers", "singer", "Singer"),
    
    # Latin America
    ("Latin_music_singers", "singer", "Singer"),
    ("Colombian_male_singers", "singer", "Singer"),
    ("Colombian_female_singers", "singer", "Singer"),
    ("Colombian_male_actors", "actor", "Actor"),
    ("Colombian_female_actors", "actor", "Actress"),
    ("Argentine_male_singers", "singer", "Singer"),
    ("Argentine_female_singers", "singer", "Singer"),
    ("Mexican_male_singers", "singer", "Singer"),
    ("Mexican_female_singers", "singer", "Singer"),
    ("Mexican_male_actors", "actor", "Actor"),
    ("Mexican_female_actors", "actor", "Actress"),
    ("Brazilian_male_singers", "singer", "Singer"),
    ("Brazilian_female_singers", "singer", "Singer"),
    ("Puerto_Rican_male_singers", "singer", "Singer"),
    
    # Sports
    ("Spanish_footballers", "footballer", "Footballer"),
    ("Italian_footballers", "footballer", "Footballer"),
    ("English_footballers", "footballer", "Footballer"),
    ("American_soccer_players", "footballer", "Footballer"),
    ("Argentine_footballers", "footballer", "Footballer"),
    ("Brazilian_footballers", "footballer", "Footballer"),
    ("Colombian_footballers", "footballer", "Footballer"),
    ("American_basketball_players", "basketball", "Basketball Player"),
    ("American_tennis_players", "tennis", "Tennis Player"),
    ("American_boxers", "boxer", "Boxer"),
    ("Formula_One_drivers", "sports", "Racing Driver"),
    
    # Politics
    ("21st-century_American_politicians", "politician", "Politician"),
    ("British_prime_ministers", "politician", "Politician"),
    ("French_politicians", "politician", "Politician"),
    ("German_politicians", "politician", "Politician"),
    ("Colombian_politicians", "politician", "Politician"),
    ("Mexican_politicians", "politician", "Politician"),
    ("Brazilian_politicians", "politician", "Politician"),
    ("Argentine_politicians", "politician", "Politician"),
    ("Spanish_politicians", "politician", "Politician"),
    ("Italian_politicians", "politician", "Politician"),
    
    # Business
    ("American_businesspeople", "business", "Entrepreneur"),
    ("British_businesspeople", "business", "Entrepreneur"),
    ("American_billionaires", "business", "Billionaire"),
    
    # Writers
    ("American_male_novelists", "writer", "Writer"),
    ("American_female_novelists", "writer", "Writer"),
    ("Colombian_writers", "writer", "Writer"),
    ("British_novelists", "writer", "Writer"),
    ("French_novelists", "writer", "Writer"),
    
    # Comedians
    ("American_male_comedians", "comedian", "Comedian"),
    ("American_female_comedians", "comedian", "Comedian"),
    ("English_comedians", "comedian", "Comedian"),
    
    # TV personalities
    ("American_television_personalities", "tv", "TV Personality"),
    ("American_television_actors", "actor", "Actor"),
    
    # Directors
    ("American_film_directors", "director", "Film Director"),
    ("British_film_directors", "director", "Film Director"),
    ("Spanish_film_directors", "director", "Film Director"),
    ("French_film_directors", "director", "Film Director"),
    ("Italian_film_directors", "director", "Film Director"),
    ("Mexican_film_directors", "director", "Film Director"),
    ("Colombian_film_directors", "director", "Film Director"),
    
    # Models
    ("American_female_models", "model", "Model"),
    ("British_female_models", "model", "Model"),
    ("Brazilian_female_models", "model", "Model"),
    
    # Journalists
    ("American_journalists", "journalist", "Journalist"),
    ("Colombian_journalists", "journalist", "Journalist"),
    ("British_journalists", "journalist", "Journalist"),
    
    # Chefs
    ("American_chefs", "chef", "Chef"),
    ("British_chefs", "chef", "Chef"),
    
    # Influence / YouTube
    ("American_YouTubers", "influencer", "YouTuber"),
    ("American_Internet_celebrities", "influencer", "Influencer"),
]

def fetch_category_members(category, limit=500):
    """Fetch page titles from a Wikipedia category."""
    members = []
    cmcontinue = None
    
    while len(members) < limit:
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'categorymembers',
            'cmtitle': f'Category:{category}',
            'cmlimit': 'max',
            'cmtype': 'page'
        }
        if cmcontinue:
            params['cmcontinue'] = cmcontinue
        
        data_enc = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(
            'https://en.wikipedia.org/w/api.php',
            data=data_enc,
            headers={'User-Agent': 'WifiOficialBio/8.0', 'Content-Type': 'application/x-www-form-urlencoded'}
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        
        for m in data.get('query', {}).get('categorymembers', []):
            title = m.get('title', '')
            if title.startswith('Category:') or title.startswith('Template:') or title.startswith('List of'):
                continue
            if ':' in title and not title.startswith('List of'):
                continue
            members.append(title)
        
        cmcontinue = data.get('continue', {}).get('cmcontinue')
        if not cmcontinue:
            break
    
    return members[:limit]


def fetch_page_data(titles):
    """Fetch extracts and images for a batch of titles."""
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts|pageimages',
        'exintro': 1,
        'explaintext': 1,
        'redirects': 1,
        'pithumbsize': 400,
        'titles': '|'.join(titles[:50])
    }
    data_enc = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        'https://en.wikipedia.org/w/api.php',
        data=data_enc,
        headers={'User-Agent': 'WifiOficialBio/8.0', 'Content-Type': 'application/x-www-form-urlencoded'}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — {cat_display} | Wifi Oficial Biography</title>
  <meta name="description" content="{meta_desc}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://wifioficialbiography.org/bios/{slug}.html">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="https://wifioficialbiography.org/bios/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{img}">
  <meta property="og:image:alt" content="{title}">
  <meta property="og:site_name" content="Wifi Oficial Biography">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:site" content="@wifioficial">
  <meta name="twitter:image" content="{img}">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0645ad">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{title}",
  "description": "{js_desc}",
  "url": "https://wifioficialbiography.org/bios/{slug}.html",
  "image": "{img}",
  "sameAs": ["https://en.wikipedia.org/wiki/{wiki_title}"],
  "knowsLanguage": ["English"]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "headline": "{title} — {cat_display}",
  "description": "{js_desc}",
  "url": "https://wifioficialbiography.org/bios/{slug}.html",
  "mainEntity": {{"@type": "Person", "name": "{title}"}},
  "dateCreated": "2026-07-25",
  "dateModified": "2026-07-25",
  "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "publisher": {{"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {{"@type": "ImageObject", "url": "https://wifioficialbiography.org/images/favicon.jpg"}}}},
  "image": "{img}"
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://wifioficialbiography.org/"}},
    {{"@type": "ListItem", "position": 2, "name": "Biografías", "item": "https://wifioficialbiography.org/#biografias"}},
    {{"@type": "ListItem", "position": 3, "name": "{title}", "item": "https://wifioficialbiography.org/bios/{slug}.html"}}
  ]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title} — {cat_display}",
  "description": "{js_desc}",
  "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "publisher": {{"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {{"@type": "ImageObject", "url": "https://wifioficialbiography.org/images/favicon.jpg"}}}},
  "datePublished": "2026-07-25",
  "dateModified": "2026-07-25",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://wifioficialbiography.org/bios/{slug}.html"}},
  "image": "{img}",
  "isBasedOn": "https://en.wikipedia.org/wiki/{wiki_title}",
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type": "Question", "name": "Who is {title}?", "acceptedAnswer": {{"@type": "Answer", "text": "{js_desc}"}}}},
    {{"@type": "Question", "name": "What is {title} known for?", "acceptedAnswer": {{"@type": "Answer", "text": "{title} is a {profession}."}}}}
  ]
}}</script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Wifi Oficial Biography",
    "url": "https://wifioficialbiography.org",
    "logo": "https://wifioficialbiography.org/images/wifioficial-og.png",
    "description": "An independent editorial platform and digital encyclopedia for biographies.",
    "founders": [
      {{"@type": "Person", "name": "Henry Orozco"}},
      {{"@type": "Person", "name": "Farid Duque"}}
    ],
    "isAccessibleForFree": true
  }}
  </script>
</head>
<body>
  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="../index.html" class="site-logo" aria-label="Wifi Oficial Biography">
        <img src="https://wifioficialbiography.org/images/favicon.jpg" alt="Wifi Oficial Biography" class="logo-icon" width="32" height="32" style="border-radius:50%;">
        <div class="logo-text">Wifi Oficial <span>Biography</span></div>
      </a>
      <nav class="main-nav" id="mainNav" role="navigation">
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
    </div>
  </header>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">
      <nav class="breadcrumbs"><a href="../index.html">Inicio</a> › <a href="../index.html#biografias">Biografías</a> › <span>{title}</span></nav>
      <div class="bio-page-header">
        <div class="bio-page-photo">
          <img src="{img}" alt="{title}" width="440" height="660" loading="eager" fetchpriority="high" itemprop="image">
        </div>
        <div class="bio-page-info">
          <h1 itemprop="name">{title}</h1>
          <p itemprop="description">{html_desc}</p>
        </div>
      </div>
      <div class="infobox">
        <div class="infobox-header">{title}</div>
        <div class="infobox-image"><img src="{img}" alt="{title}" width="440" height="660" loading="lazy"></div>
        <table><tbody>
          <tr><th>Occupation</th><td itemprop="jobTitle">{cat_display}</td></tr>
        </tbody></table>
        <div class="infobox-section">Profiles</div>
        <table><tbody>
          <tr><th>Wikipedia</th><td><a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{wiki_title}</a></td></tr>
        </tbody></table>
      </div>
      <article class="bio-article">
        <div class="category-tags">
          <a href="#" class="category-tag">{cat_display}</a>
          <a href="#" class="category-tag">Public Figure</a>
        </div>
        <h2>Biography</h2>
        <p><strong>{title}</strong> {extract_html}</p>
        <p>{extract_html}</p>
        
    <section class="attribution-notice" style="margin-top:2rem;padding:1rem;background:#f5f5f5;border-left:4px solid #888;font-size:0.85rem;">
      <p><strong>Atribucion &mdash; CC BY-SA 4.0</strong></p>
      <p>El contenido textual de esta biografia esta basado en material de Wikipedia, disponible bajo la licencia 
      <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="license noopener">Creative Commons Atribucion-CompartirIgual 4.0 Internacional</a>.
      </p><p>Las imagenes utilizadas pertenecen a <a href="https://commons.wikimedia.org/" target="_blank" rel="noopener">Wikimedia Commons</a>.</p>
      <p><strong>Fuentes originales:</strong><br><a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">https://en.wikipedia.org/wiki/{wiki_title}</a></p>
    </section>
    
    <h2 id="references">References</h2>
        <div class="reflist"><ol>
          <li><span class="cite-note">"{title}." Wikipedia. <a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{wiki_title}</a></span></li>
        </ol></div>
      </article>
    </main>
  </div>
    <footer class="site-footer" role="contentinfo">
    <div class="footer-inner">
      <div class="footer-links">
        <a href="../index.html">Inicio</a>
        <a href="../index.html#biografias">Biografías</a>
        <a href="../index.html#categorias">Categorías</a>
        <a href="../index.html#about">Acerca de</a>
      </div>
      <div class="footer-social">
        <a href="https://www.instagram.com/wifioficial/" target="_blank" rel="noopener">📷 Instagram</a>
        <a href="https://www.facebook.com/wifioficialco" target="_blank" rel="noopener">📘 Facebook</a>
        <a href="https://www.tiktok.com/@wifioficialbiography" target="_blank" rel="noopener">🎵 TikTok</a>
        <a href="https://www.threads.net/@wifioficial" target="_blank" rel="noopener">🧵 Threads</a>
        <a href="https://telegram.me/wifimarco" target="_blank" rel="noopener">✈️ Telegram</a>
      </div>
      <p>&copy; 2026 Wifi Oficial Biography.</p>
    </div>
  </footer>
  <script src="../js/app.js"></script>
</body>
</html>"""

DEFAULT_IMG = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png'

def make_slug(title):
    slug = title.lower().replace(' ', '-')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

def generate_html(title, wiki_title, category, profession, extract, image_url):
    slug = make_slug(title)
    if slug in EXISTING:
        return None
    
    img = image_url or DEFAULT_IMG
    
    first_s = extract.split('.')[0] + '.' if extract and '.' in extract else (extract or f'{title} is a {profession.lower() or "public figure"}.')
    meta_desc = first_s[:160].replace('"', '&quot;').replace('\n', ' ')
    js_desc = html_mod.escape(first_s[:200]).replace('"', '\\"').replace('\n', ' ')
    html_desc = html_mod.escape(first_s[:300]).replace('\n', ' ')
    extract_html = html_mod.escape(extract[:500] if extract else f'{title} is a {profession.lower() or "public figure"}.').replace('\n', ' ')
    
    cat_display = profession or category.title()
    
    return TEMPLATE.format(
        title=title, slug=slug, cat_display=cat_display, meta_desc=meta_desc,
        img=img, js_desc=js_desc, html_desc=html_desc, extract_html=extract_html,
        wiki_title=wiki_title, profession=profession.lower() or 'public figure'
    )

# === MAIN ===
print("Fetching category members...")
all_titles = {}
for cat, cat_id, profession in CATEGORIES:
    try:
        members = fetch_category_members(cat, limit=300)
        for t in members:
            if t not in all_titles:
                all_titles[t] = (cat_id, profession)
        print(f'  {cat}: {len(members)} members')
    except Exception as e:
        print(f'  {cat}: ERROR - {e}')
    time.sleep(0.5)

print(f'\nTotal unique figure titles collected: {len(all_titles)}')

# Filter to those not already existing
to_process = [(t, cat, prof) for t, (cat, prof) in all_titles.items() if make_slug(t) not in EXISTING]
print(f'Already existing: {len(all_titles) - len(to_process)}')
print(f'To generate: {len(to_process)}')

# Limit to ~4000 for manageability
if len(to_process) > 4000:
    to_process = to_process[:4000]
    print(f'Limited to 4000 for this run')

# Process in batches
BATCH = 50
generated = 0
errors = 0

for i in range(0, len(to_process), BATCH):
    batch = to_process[i:i+BATCH]
    titles = [t for t, _, _ in batch]
    
    try:
        data = fetch_page_data(titles)
        pages = data.get('query', {}).get('pages', {})
        redirects = {r['from'].lower().replace(' ', '_'): r['to'] for r in data.get('query', {}).get('redirects', [])}
        
        extract_map = {}
        image_map = {}
        for pid, pdata in pages.items():
            t = pdata.get('title', '')
            if pdata.get('extract'):
                extract_map[t] = pdata['extract']
            thumb = pdata.get('thumbnail', {}).get('source', '')
            if thumb:
                image_map[t] = thumb
        
        for wiki_title, category, profession in batch:
            canon = redirects.get(wiki_title.lower(), wiki_title)
            extract = extract_map.get(canon) or extract_map.get(wiki_title, '')
            image_url = image_map.get(canon) or image_map.get(wiki_title, '')
            
            title_clean = canon.replace('_', ' ')
            
            html = generate_html(title_clean, canon, category, profession, extract, image_url)
            if html is None:
                continue
            
            fp = os.path.join(BIOS_DIR, f'{make_slug(title_clean)}.html')
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(html)
            generated += 1
            
    except Exception as e:
        errors += len(batch)
        if i % 500 == 0:
            print(f'  Error at {i}: {e}')
    
    time.sleep(0.8)
    if (i // BATCH) % 10 == 0:
        print(f'  {min(i+BATCH, len(to_process))}/{len(to_process)} — Gen: {generated}, Err: {errors}', flush=True)

print(f'\nDone! Generated: {generated}, Errors: {errors}')
