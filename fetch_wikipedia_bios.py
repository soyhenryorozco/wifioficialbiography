#!/usr/bin/env python3
"""Fetch living people from Wikipedia categories and generate Shakira-level bios."""
import json, os, re, html, time, urllib.request, urllib.parse, sys

BIOS_DIR = "bios"
DOMAIN = "https://wifioficialbiography.org"
WIKI_API = "https://en.wikipedia.org/w/api.php"

def req(params):
    params['format'] = 'json'
    params['origin'] = '*'
    url = WIKI_API + '?' + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'WifioficialBio/2.0'}), timeout=15) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  API error: {e}")
        return None

def slugify(name):
    s = name.lower().replace(' ', '-')
    s = re.sub(r'[^a-z0-9\-]', '', s)
    return s

def esc(s):
    if not s: return ''
    return html.escape(s).replace("'", "&#39;")

def get_category_members_small(category, limit=100):
    """Get a few pages from a Wikipedia category."""
    params = {'action': 'query', 'list': 'categorymembers',
              'cmtitle': category, 'cmlimit': str(min(limit, 500)), 'cmtype': 'page', 'cmnamespace': '0'}
    data = req(params)
    if not data:
        return []
    members = [m['title'] for m in data.get('query', {}).get('categorymembers', []) if m['ns'] == 0]
    return members[:limit]

# Smaller, targeted categories for high-profile living people
CATEGORIES = [
    'Category:Colombian singers',
    'Category:Colombian male singers',
    'Category:Colombian female singers',
    'Category:Mexican singers',
    'Category:Argentine singers',
    'Category:Brazilian singers',
    'Category:Puerto Rican musicians',
    'Category:Spanish singers',
    'Category:American male singers',
    'Category:American female singers',
    'Category:British male singers',
    'Category:Canadian singers',
    'Category:Colombian footballers',
    'Category:Argentine footballers',
    'Category:Brazilian footballers',
    'Category:Uruguayan footballers',
    'Category:Chilean footballers',
    'Category:Peruvian footballers',
    'Category:English footballers',
    'Category:Spanish footballers',
    'Category:French footballers',
    'Category:German footballers',
    'Category:Italian footballers',
    'Category:Colombian actors',
    'Category:Mexican actors',
    'Category:Argentine actors',
    'Category:Spanish actors',
    'Category:Colombian actresses',
    'Category:Mexican actresses',
    'Category:Colombian television presenters',
    'Category:Colombian journalists',
    'Category:Colombian writers',
    'Category:Colombian athletes',
    'Category:Colombian cyclists',
    'Category:Colombian boxers',
    'Category:Colombian politicians',
    'Category:Mexican politicians',
    'Category:Argentine politicians',
    'Category:American film actors',
    'Category:American television actors',
    'Category:American comedians',
    'Category:American businesspeople',
    'Category:American tennis players',
    'Category:American basketball players',
    'Category:American baseball players',
    'Category:English-language singers',
    'Category:Spanish-language singers',
    'Category:Reggaeton musicians',
    'Category:Reggaeton singers',
    'Category:Latin pop singers',
    'Category:K-pop singers',
    'Category:K-pop idols',
]

def main():
    existing = set(f.replace('.html', '') for f in os.listdir(BIOS_DIR) if f.endswith('.html'))
    print(f"Existing bios: {len(existing)}")
    
    all_titles = set()
    # Filter to only categories that might still have new people
    existing = set(f.replace('.html', '') for f in os.listdir(BIOS_DIR) if f.endswith('.html'))
    for idx, cat in enumerate(CATEGORIES):
        short_name = cat.replace('Category:', '')
        print(f"[{idx+1}/{len(CATEGORIES)}] Fetching {cat}...")
        time.sleep(2.5)
        members = get_category_members_small(cat, limit=80)
        new_titles = [t for t in members if slugify(t) not in existing]
        all_titles.update(new_titles)
        existing.update(slugify(t) for t in new_titles)
        print(f"  Got {len(members)} pages, {len(new_titles)} new (total unique: {len(all_titles)})")
        if len(all_titles) >= 2000:
            break
    
    print(f"\nTotal new unique people: {len(all_titles)}")
    
    if len(all_titles) > 2000:
        all_titles = list(all_titles)[:2000]
    
    # Process in batches
    titles_list = list(all_titles)
    generated = 0
    batch_size = 50
    
    for i in range(0, len(titles_list), batch_size):
        batch = titles_list[i:i+batch_size]
        params = {'action': 'query', 'titles': '|'.join(batch),
                  'prop': 'extracts|pageimages|pageterms|info',
                  'exintro': '1', 'explaintext': '1', 'pithumbsize': 400,
                  'inprop': 'url'}
        data = req(params)
        time.sleep(2.0)
        
        if not data:
            continue
        
        pages = data.get('query', {}).get('pages', {})
        for pid, page in pages.items():
            if pid == '-1': continue
            title = page.get('title', '')
            slug = slugify(title)
            fname = f"{slug}.html"
            fpath = os.path.join(BIOS_DIR, fname)
            if os.path.exists(fpath):
                continue
            
            extract = page.get('extract', '')
            image = page.get('thumbnail', {}).get('source', '') if 'thumbnail' in page else ''
            desc = page.get('terms', {}).get('description', [''])[0] if 'terms' in page else ''
            pageurl = page.get('fullurl', f'https://en.wikipedia.org/wiki/{title.replace(" ", "_")}')
            
            image_url = image
            bio_desc = desc or f"Complete biography of {title}"
            
            # Build HTML
            occ = 'Public Figure'
            for kw in ['singer', 'actor', 'football', 'player', 'writer', 'politician', 'comedian']:
                if kw.lower() in (desc + extract)[:200].lower():
                    occ_map = {'singer': 'Singer', 'actor': 'Actor', 'football': 'Footballer',
                              'player': 'Athlete', 'writer': 'Writer', 'politician': 'Politician',
                              'comedian': 'Comedian'}
                    occ = occ_map.get(kw, 'Public Figure')
                    break
            
            today = "2026-07-15"
            
            # Parse sections
            sections = {}
            lines = extract.split('\n')
            current = 'Intro'
            texts = []
            for line in lines:
                if line.startswith('== ') and line.endswith(' =='):
                    if texts:
                        sections[current] = '\n'.join(texts).strip()
                    current = line.strip('= ')
                    texts = []
                else:
                    texts.append(line)
            if texts:
                sections[current] = '\n'.join(texts).strip()
            
            early = sections.get('Early life', '') or sections.get('Early life and education', '') or ''
            career = sections.get('Career', '') or sections.get('Professional career', '') or ''
            personal = sections.get('Personal life', '') or ''
            
            cat_tags = f'''          <a href="#" class="category-tag">Famous</a>
          <a href="#" class="category-tag">Public Figure</a>
          <a href="#" class="category-tag">International</a>'''
            
            html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{esc(title)} — Biography | Wifioficial Biography</title>
  <meta name="description" content="{esc(bio_desc[:200])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{DOMAIN}/bios/{slug}.html">
  <meta property="og:type" content="profile"><meta property="og:url" content="{DOMAIN}/bios/{slug}.html">
  <meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(bio_desc[:200])}">
  <meta property="og:image" content="{esc(image_url)}"><meta property="og:image:alt" content="{esc(title)}">
  <meta property="og:site_name" content="Wifioficial Biography"><meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{esc(image_url)}">
  <meta name="twitter:site" content="@wifioficial"><meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0645ad">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Person","name":"{esc(title)}","description":"{esc(bio_desc[:300])}","url":"{DOMAIN}/bios/{slug}.html","image":"{esc(image_url)}"}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfilePage","headline":"{esc(title)}","description":"{esc(bio_desc[:200])}","url":"{DOMAIN}/bios/{slug}.html","mainEntity":{{"@type":"Person","name":"{esc(title)}"}},"dateCreated":"{today}","dateModified":"{today}","author":{{"@type":"Organization","name":"Wifioficial Biography"}},"publisher":{{"@type":"Organization","name":"Wifioficial Biography","logo":{{"@type":"ImageObject","url":"{DOMAIN}/images/favicon.jpg"}}}},"image":"{esc(image_url)}"}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Inicio","item":"{DOMAIN}/"}},{{"@type":"ListItem","position":2,"name":"Biografías","item":"{DOMAIN}/#biografias"}},{{"@type":"ListItem","position":3,"name":"{esc(title)}","item":"{DOMAIN}/bios/{slug}.html"}}]}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{esc(title)}","description":"{esc(bio_desc[:200])}","author":{{"@type":"Organization","name":"Wifioficial Biography"}},"publisher":{{"@type":"Organization","name":"Wifioficial Biography","logo":{{"@type":"ImageObject","url":"{DOMAIN}/images/favicon.jpg"}}}},"datePublished":"{today}","dateModified":"{today}","mainEntityOfPage":{{"@type":"WebPage","@id":"{DOMAIN}/bios/{slug}.html"}},"image":"{esc(image_url)}"}}</script>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"Who is {esc(title)}?","acceptedAnswer":{{"@type":"Answer","text":"{esc(bio_desc[:250])}"}}}},{{"@type":"Question","name":"What is {esc(title)} known for?","acceptedAnswer":{{"@type":"Answer","text":"{esc(title)} is a {esc(occ)}."}}}}]}}</script>
</head>
<body>
  <header class="site-header"><div class="header-inner">
    <a href="../index.html" class="site-logo"><img src="../images/favicon.jpg" alt="W" class="logo-icon" width="32" height="32"></a>
    <div class="logo-text">Wifioficial <span>Biography</span></div>
    <nav class="main-nav"><ul><li><a href="../index.html">Inicio</a></li><li><a href="../index.html#biografias">Biografías</a></li></ul></nav>
    <div class="header-search"><input type="search" id="headerSearchInput" placeholder="Buscar biografía..."><button id="searchBtn">Buscar</button></div>
  </div></header>
  <div class="search-overlay" id="searchOverlay"><div class="search-box"><input type="search" id="searchOverlayInput" placeholder="Buscar biografía..." autocomplete="off"><div class="search-results" id="searchResults"></div></div></div>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">
      <nav class="breadcrumbs"><a href="../index.html">Inicio</a> › <a href="../index.html#biografias">Biografías</a> › <span>{esc(title)}</span></nav>
      <div class="bio-page-header">
        <div class="bio-page-photo"><img src="{esc(image_url)}" alt="{esc(title)}" width="220" height="275" loading="eager" itemprop="image"></div>
        <div class="bio-page-info"><h1 itemprop="name">{esc(title)}</h1><p itemprop="description">{esc(bio_desc[:300])}</p></div>
      </div>
      <div class="infobox"><div class="infobox-header">{esc(title)}</div>
        <div class="infobox-image"><img src="{esc(image_url)}" alt="{esc(title)}" width="300" height="375" loading="lazy"></div>
        <table><tbody>
          <tr><th>Name</th><td>{esc(title)}</td></tr>
          <tr><th>Occupation</th><td itemprop="jobTitle">{esc(occ)}</td></tr>
        </tbody></table>
        <div class="infobox-section">Profiles</div>
        <table><tbody>
          <tr><th>Wikipedia</th><td><a href="https://en.wikipedia.org/wiki/{title.replace(' ', '_')}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{title.replace(' ', '_')}</a></td></tr>
        </tbody></table>
      </div>
      <nav class="toc"><div class="toc-title">Contents</div><ol>
        <li><a href="#biography">Biography</a></li>
        <li><a href="#references">References</a></li>
      </ol></nav>
      <article class="bio-article">
        <div class="category-tags">{cat_tags}</div>
        
        <h2 id="biography">Biography</h2>
        <p><strong>{esc(title)}</strong> is a {esc(occ)}.</p>
        <p>{esc(extract[:600] or bio_desc)}</p>
        
        {("<h2>Early Life</h2><p>" + esc(early[:400]) + "</p>") if early else ""}
        
        {("<h2>Career</h2><p>" + esc(career[:600]) + "</p>") if career else ""}
        
        {("<h2>Personal Life</h2><p>" + esc(personal[:300]) + "</p>") if personal else ""}
        
        <h2 id="references">References</h2>
        <div class="reflist"><ol>
          <li><span class="cite-note">"{esc(title)}." Wikipedia. <a href="https://en.wikipedia.org/wiki/{title.replace(' ', '_')}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{title.replace(' ', '_')}</a></span></li>
        </ol></div>
        
        <h2>External Links</h2>
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/{title.replace(' ', '_')}" target="_blank" rel="noopener">Wikipedia — {esc(title)}</a></li>
        </ul>
        
        <h2>Biografías Relacionadas</h2>
        <ul>
          <li><a href="shakira.html">Shakira</a></li>
          <li><a href="karol-g.html">Karol G</a></li>
          <li><a href="henry-orozco.html">Henry Orozco</a></li>
        </ul>
      </article>
    </main>
  </div>
  <footer class="site-footer"><div class="footer-inner"><p>&copy; 2026 Wifioficial Biography</p></div></footer>
  <script src="../js/app.js"></script>
</body>
</html>'''
            
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated += 1
            if generated % 100 == 0:
                print(f"  Generated {generated}...")
        
        time.sleep(0.2)
    
    print(f"\n=== GENERATION COMPLETE ===")
    print(f"Generated: {generated}")
    print(f"Total bio files: {len(os.listdir(BIOS_DIR))}")

if __name__ == '__main__':
    main()
