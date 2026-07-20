#!/usr/bin/env python3
"""
Generate 1,200 biography HTML files from Wikipedia/Wikidata data.
Follows the Shakira bio schema exactly.
"""
import os, re, json, time, html as html_mod, hashlib, sys
from datetime import datetime
from urllib.parse import quote
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIOS_DIR = os.path.join(BASE_DIR, 'bios')

EXISTING = set()
for f in os.listdir(BIOS_DIR):
    if f.endswith('.html'):
        EXISTING.add(f.replace('.html', ''))

WIKI_HEADER = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Wifioficial Biography</title>
  <meta name="description" content="{meta_desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://wifioficialbiography.org/bios/{slug}.html">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="https://wifioficialbiography.org/bios/{slug}.html">
  <meta property="og:image" content="{image}">
  <meta property="og:image:alt" content="{name}">
  <meta property="og:site_name" content="Wifioficial Biography">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{og_title}">
  <meta name="twitter:description" content="{og_desc}">
  <meta name="twitter:image" content="{image}">
  <meta name="twitter:site" content="@wifioficial">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0645ad">
  <meta name="article:section" content="Biography">
  <link rel="alternate" hreflang="en" href="https://wifioficialbiography.org/bios/{slug}.html">
  <link rel="alternate" hreflang="es" href="https://wifioficialbiography.org/bios/{slug}.html">
  <link rel="alternate" hreflang="x-default" href="https://wifioficialbiography.org/bios/{slug}.html">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
{json_ld}
</head>
<body>
      <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="../index.html" class="site-logo" aria-label="Wifioficial Biography">
        <img src="../images/favicon.jpg" alt="Wifioficial Biography" class="logo-icon" width="32" height="32" style="border-radius:50%;">
        <div class="logo-text">Wifioficial <span>Biography</span></div>
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
  <div class="search-overlay" id="searchOverlay">
    <div class="search-box">
      <input type="search" id="searchOverlayInput" placeholder="Buscar biografía..." autocomplete="off">
      <div class="search-results" id="searchResults"></div>
    </div>
  </div>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <a href="../index.html">Inicio</a> <span class="separator">›</span>
        <a href="../index.html#biografias">Biografías</a> <span class="separator">›</span>
        <span>{name}</span>
      </nav>
      <div class="bio-page-header">
        <div class="bio-page-photo">
          <img src="{image}" alt="{name}" title="{name} — {profession}" width="440" height="{img_height}" loading="eager" fetchpriority="high" itemprop="image">
        </div>
        <div class="bio-page-info">
          <h1 itemprop="name">{name}</h1>
          <div class="subtitle" itemprop="alternateName">{full_name}</div>
          <p itemprop="description">{description}</p>
        </div>
      </div>
      <div class="infobox" role="complementary" aria-label="Personal information">
        <div class="infobox-header">{name}</div>
        <div class="infobox-image"><img src="{image}" alt="{name}" title="{name}" width="440" height="{img_height}" loading="lazy"></div>
        <table><tbody>
          <tr><th>Full Name</th><td itemprop="birthName">{full_name}</td></tr>
          <tr><th>Born</th><td><time itemprop="birthDate" datetime="{birth_date_iso}">{birth_date_display}</time><br><span itemprop="birthPlace">{birth_place}</span></td></tr>
          <tr><th>Nationality</th><td itemprop="nationality">{nationality}</td></tr>
          <tr><th>Occupation(s)</th><td itemprop="jobTitle">{profession}</td></tr>
          <tr><th>Years Active</th><td>{years_active}</td></tr>
        </tbody></table>
        <div class="infobox-section">Profiles</div>
        <table><tbody>
          <tr><th>Wikipedia</th><td><a href="{wikipedia_url}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{wikipedia_title}</a></td></tr>
          <tr><th>Wikidata</th><td><a href="https://www.wikidata.org/wiki/{wikidata_id}" target="_blank" rel="noopener">{wikidata_id}</a></td></tr>
        </tbody></table>
      </div>
      <nav class="toc" aria-label="Table of contents">
        <div class="toc-title">Contents</div>
        <ol>
          <li><a href="#biography">Biography</a></li>
          <li><a href="#career">Career</a></li>
          <li><a href="#personal-life">Personal Life</a></li>
          <li><a href="#references">References</a></li>
          <li><a href="#external-links">External Links</a></li>
        </ol>
      </nav>
      <article class="bio-article">
        <div class="category-tags">
          {category_tags}
        </div>
        <p><strong>{name}</strong> (born {birth_date_display}) is {nationality_article} {profession_lower}. {description}</p>
        <p>{bio_text_1}</p>
        <p>{bio_text_2}</p>
        <h2 id="career">Career</h2>
        <p>{career_text}</p>
        <h2 id="personal-life">Personal Life</h2>
        <p>{personal_life_text}</p>
        <h2 id="references">References</h2>
        <div class="reflist">
          <ol>
            <li id="cite-note-1"><span class="cite-note">"{name}." Wikipedia. <a href="{wikipedia_url}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{wikipedia_title}</a></span></li>
            <li id="cite-note-2"><span class="cite-note">"Wikidata entity: {wikidata_id} — {name}." <a href="https://www.wikidata.org/wiki/{wikidata_id}" target="_blank" rel="noopener">wikidata.org/wiki/{wikidata_id}</a></span></li>
          </ol>
        </div>
        <h2 id="external-links">External Links</h2>
        <h3>Knowledge Platforms</h3>
        <ul>
          <li><a href="{wikipedia_url}" target="_blank" rel="noopener">Wikipedia — {name}</a></li>
          <li><a href="https://www.wikidata.org/wiki/{wikidata_id}" target="_blank" rel="noopener">Wikidata — {wikidata_id}</a></li>
        </ul>
      </article>
    </main>
  </div>
    <footer class="site-footer" role="contentinfo">
    <div class="footer-inner">
      <div class="footer-links">
        <a href="../index.html">Inicio</a>
        <a href="../index.html#biografias">Biografías</a>
        <a href="../index.html#categorias">Categorías</a>
        <a href="../index.html#submit">Publicar</a>
        <a href="../index.html#about">Acerca de</a>
      </div>
      <div class="footer-social">
        <a href="https://www.instagram.com/wifioficial/" target="_blank" rel="noopener">📷 Instagram</a>
        <a href="https://www.facebook.com/wifioficialco" target="_blank" rel="noopener">📘 Facebook</a>
        <a href="https://www.tiktok.com/@wifioficialbiography" target="_blank" rel="noopener">🎵 TikTok</a>
        <a href="https://www.threads.net/@wifioficial" target="_blank" rel="noopener">🧵 Threads</a>
        <a href="https://telegram.me/wifimarco" target="_blank" rel="noopener">✈️ Telegram</a>
      </div>
      <p>&copy; 2026 Wifioficial Biography. Todos los derechos reservados.</p>
    </div>
  </footer>
  <script src="../js/app.js"></script>
</body>
</html>'''

API_BASE = "https://en.wikipedia.org/w/api.php"

def wiki_api(params, retries=5):
    """Call the Wikipedia API."""
    params['format'] = 'json'
    url = API_BASE + '?' + urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'WifioficialBioGenerator/1.0 (henry@example.com)'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(5)
                continue
            return None

def make_slug(name):
    import unicodedata
    slug = name.lower().strip()
    # Normalize unicode and strip diacritics
    slug = unicodedata.normalize('NFKD', slug)
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

def thumbnail_to_full(url):
    """Convert a Wikimedia thumbnail URL to the full image URL."""
    if '/thumb/' in url:
        m = re.match(r'(https://upload\.wikimedia\.org/wikipedia/commons/thumb/)(.)/(..)/([^/]+)/\d+px-(.+\.\w+)', url)
        if m:
            # groups: prefix (with thumb/), hash1, hash2, filename, actual_filename
            return m.group(1).replace('/thumb/', '/') + m.group(2) + '/' + m.group(3) + '/' + m.group(5)
    return url

def get_wikidata_entity(qid):
    """Get structured data from Wikidata for a given QID."""
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'WifioficialBioGenerator/1.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            entity = data.get('entities', {}).get(qid, {})
            claims = entity.get('claims', {})
            
            result = {}
            
            # Birth date (handle approximate dates)
            if 'P569' in claims:
                try:
                    raw = claims['P569'][0]['mainsnak']['datavalue']['value']['time']
                    raw = raw.lstrip('+')
                    if raw.startswith('0000'):
                        pass  # Invalid date
                    else:
                        result['birthDate'] = raw[:10]
                        # Handle approximate dates like 1982-00-00
                        if result['birthDate'].endswith('-00-00'):
                            result['birthDate'] = result['birthDate'][:4] + '-01-01'
                        elif result['birthDate'].endswith('-00'):
                            result['birthDate'] = result['birthDate'][:7] + '-01'
                except:
                    pass
            
            # Birth place
            if 'P19' in claims:
                try:
                    bp_id = claims['P19'][0]['mainsnak']['datavalue']['value']['id']
                    result['birthPlaceId'] = bp_id
                except:
                    pass
            
            # Nationality
            if 'P27' in claims:
                try:
                    nat_id = claims['P27'][0]['mainsnak']['datavalue']['value']['id']
                    result['nationalityId'] = nat_id
                except:
                    pass
            
            # Occupation
            if 'P106' in claims:
                occs = []
                for claim in claims['P106'][:3]:
                    try:
                        occs.append(claim['mainsnak']['datavalue']['value']['id'])
                    except:
                        pass
                if occs:
                    result['occupationIds'] = occs
            
            # Full name / birth name
            if 'P1477' in claims:
                try:
                    result['fullName'] = claims['P1477'][0]['mainsnak']['datavalue']['value']['text']
                except:
                    pass
            
            return result
    except Exception as e:
        return {}

def fetch_labels(qids):
    """Fetch labels for Wikidata QIDs."""
    if not qids:
        return {}
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={'|'.join(qids)}&props=labels&languages=en&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'WifioficialBioGenerator/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            result = {}
            for qid, ent in data.get('entities', {}).items():
                label = ent.get('labels', {}).get('en', {}).get('value', '')
                if label:
                    result[qid] = label
            return result
    except:
        return {}

def parse_extract(extract, name):
    """Parse Wikipedia extract to extract structured data."""
    result = {
        'birth_date': '',
        'nationality': '',
        'occupation': '',
    }
    
    if not extract:
        return result
    
    # Try to find "born DATE" pattern
    m = re.search(r'born\s+(\d+\s+\w+\s+\d{4})', extract, re.IGNORECASE)
    if m:
        result['birth_date'] = m.group(1)
    else:
        m = re.search(r'born\s+(\w+\s+\d+,\s+\d{4})', extract, re.IGNORECASE)
        if m:
            result['birth_date'] = m.group(1)
    
    # Try to find nationality pattern: "is a/an Nationality Occupation"
    m = re.search(r'is\s+(?:a|an)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(.+)', extract)
    if m:
        result['nationality'] = m.group(1)
        occ_raw = m.group(2)
        # Get the first part before punctuation or "who" or "known"
        occ_m = re.match(r'([\w\s/-]+?)(?:[,\.]|\s+who|\s+known)', occ_raw)
        if occ_m:
            result['occupation'] = occ_m.group(1).strip()
        else:
            result['occupation'] = occ_raw.split(',')[0].strip()[:50]
    
    return result

def build_json_ld(data):
    """Build JSON-LD schema blocks."""
    same_as = [f"https://www.wikidata.org/wiki/{data['wikidata_id']}", data['wikipedia_url']]
    
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": data['name'],
        "alternateName": [data['full_name']],
        "description": data['description'],
        "birthDate": data['birth_date_iso'],
        "birthPlace": {"@type": "Place", "name": data['birth_place']},
        "nationality": {"@type": "Country", "name": data['nationality']},
        "jobTitle": [data['profession']],
        "url": f"https://wifioficialbiography.org/bios/{data['slug']}.html",
        "image": data['image'],
        "sameAs": same_as,
    }
    
    profile_page = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "headline": f"{data['name']} — Biography",
        "description": data['description'],
        "url": f"https://wifioficialbiography.org/bios/{data['slug']}.html",
        "mainEntity": person
    }
    
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://wifioficialbiography.org/"},
            {"@type": "ListItem", "position": 2, "name": "Biografías", "item": "https://wifioficialbiography.org/#biografias"},
            {"@type": "ListItem", "position": 3, "name": data['name'], "item": f"https://wifioficialbiography.org/bios/{data['slug']}.html"}
        ]
    }
    
    article = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": f"{data['name']} — {data['profession']}",
        "description": data['description'],
        "author": {"@type": "Organization", "name": "Wifioficial Biography"},
        "publisher": {"@type": "Organization", "name": "Wifioficial Biography", "logo": {"@type": "ImageObject", "url": "https://wifioficialbiography.org/images/favicon.jpg"}},
        "datePublished": "2026-07-20",
        "dateModified": "2026-07-20",
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://wifioficialbiography.org/bios/{data['slug']}.html"},
        "image": data['image']
    }
    
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": f"Who is {data['name']}?", "acceptedAnswer": {"@type": "Answer", "text": data['description']}},
            {"@type": "Question", "name": f"What is {data['name']} known for?", "acceptedAnswer": {"@type": "Answer", "text": f"{data['name']} is a {data['nationality']} {data['profession'].lower()}, born on {data['birth_date_display']}."}}
        ]
    }
    
    blocks = [person, profile_page, breadcrumb, article, faq]
    return '\n'.join(f'  <script type="application/ld+json">\n{json.dumps(b, indent=2)}\n  </script>' for b in blocks)

WD_CATEGORY_MAP = {
    'Q177220': 'singer',     # singer
    'Q33999': 'actor',       # actor
    'Q2526255': 'actor',     # film actor
    'Q10798782': 'actor',    # television actor
    'Q10871364': 'actor',    # voice actor
    'Q937857': 'footballer', # association football player
    'Q82955': 'politician',  # politician
    'Q36180': 'writer',      # writer
    'Q245068': 'comedian',   # comedian
    'Q4610556': 'model',     # model
    'Q901': 'scientist',     # scientist
    'Q131524': 'business',   # businessperson
    'Q1930187': 'journalist',# journalist
    'Q10855167': 'singer',   # rapper
    'Q2526361': 'singer',    # singer-songwriter
    'Q81096': 'director',    # film director
    'Q3709068': 'tv',        # television presenter
    'Q49757': 'chef',        # chef
    'Q188094': 'sports',     # sportsman
    'Q11513337': 'sports',   # basketball player
    'Q10855167': 'singer',   # rapper
    'Q2066131': 'sports',    # sportsperson
    'Q423509': 'sports',     # tennis player
    'Q2419649': 'sports',    # cyclist
    'Q5706012': 'influencer',# YouTuber
}

def infer_category(occupation_ids):
    """Infer the category label from Wikidata occupation IDs."""
    for oid in occupation_ids:
        if oid in WD_CATEGORY_MAP:
            return WD_CATEGORY_MAP[oid]
    return 'singer'  # default

def generate_bio(data):
    """Generate a bio HTML file."""
    slug = data['slug']
    name = data['name']
    
    template_data = {
        'slug': slug,
        'title': f"{name} — {data['profession']} | Wifioficial Biography",
        'name': name,
        'full_name': data['full_name'],
        'meta_desc': html_mod.escape(data['description'])[:200],
        'og_title': f"{name} — {data['profession']}",
        'og_desc': html_mod.escape(data['description'])[:200],
        'image': data['image'],
        'description': html_mod.escape(data['description'])[:200],
        'birth_date_iso': data['birth_date_iso'],
        'birth_date_display': data['birth_date_display'],
        'birth_place': data['birth_place'],
        'nationality': data['nationality'],
        'profession': data['profession'],
        'profession_lower': data['profession'].lower(),
        'nationality_article': 'an' if data['nationality'][0].lower() in 'aeiou' else 'a',
        'years_active': data.get('years_active', '1990\u2013present'),
        'wikipedia_url': f"https://en.wikipedia.org/wiki/{data['wiki_title']}",
        'wikipedia_title': data['wiki_title'],
        'wikidata_id': data['wikidata_id'],
        'category_tags': '\n          '.join(f'<a href="#" class="category-tag">{t}</a>' for t in data['tags'][:6]),
        'bio_text_1': data.get('bio_text_1', ''),
        'bio_text_2': data.get('bio_text_2', ''),
        'career_text': data.get('career_text', ''),
        'personal_life_text': data.get('personal_life_text', ''),
        'img_height': data.get('img_height', 660),
        'json_ld': data['json_ld'],
    }
    
    return WIKI_HEADER.format(**template_data)

def process_page(title, cat_label, cat_name):
    """Process a Wikipedia page to generate a bio."""
    slug = make_slug(title)
    if slug in EXISTING:
        return None
    
    # Get page data
    params = {
        'action': 'query',
        'titles': title,
        'prop': 'pageimages|pageprops|extracts',
        'pithumbsize': 440,
        'exintro': 1,
        'explaintext': 1,
        'ppprop': 'wikibase_item',
    }
    data = wiki_api(params)
    if not data:
        return None
    
    pages = data.get('query', {}).get('pages', {})
    if not pages:
        return None
    
    page = list(pages.values())[0]
    if 'missing' in page:
        return None
    
    wikidata_id = page.get('pageprops', {}).get('wikibase_item', '')
    if not wikidata_id:
        return None
    
    thumbnail = page.get('thumbnail', {}).get('source', '')
    if not thumbnail:
        return None
    
    image = thumbnail_to_full(thumbnail)
    if not image:
        return None
    
    extract = page.get('extract', '')
    parsed = parse_extract(extract, title)
    
    # Get Wikidata data
    wd = get_wikidata_entity(wikidata_id)
    
    # Resolve labels for Wikidata IDs
    label_ids = []
    if wd.get('birthPlaceId'):
        label_ids.append(wd['birthPlaceId'])
    if wd.get('nationalityId'):
        label_ids.append(wd['nationalityId'])
    if wd.get('occupationIds'):
        label_ids.extend(wd['occupationIds'])
    
    labels = fetch_labels(label_ids) if label_ids else {}
    
    # Build birth date from extract or Wikidata
    birth_date_str = parsed.get('birth_date', '')
    birth_date_iso = ''
    birth_date_display = ''
    
    if birth_date_str:
        for fmt in ['%d %B %Y', '%B %d, %Y', '%d %b %Y', '%B %Y', '%Y']:
            try:
                dt = datetime.strptime(birth_date_str, fmt)
                birth_date_display = dt.strftime("%B %d, %Y").lstrip("0").replace(" 0", " ") if '%d' in fmt else dt.strftime("%B %Y")
                birth_date_iso = dt.strftime("%Y-%m-%d")
                break
            except:
                continue
    
    if not birth_date_iso and 'birthDate' in wd:
        birth_date_iso = wd['birthDate']
        try:
            dt = datetime.strptime(birth_date_iso, "%Y-%m-%d")
            birth_date_display = dt.strftime("%B %d, %Y").lstrip("0").replace(" 0", " ")
        except:
            pass
    
    if not birth_date_iso:
        return None
    
    nationality = parsed.get('nationality', '')
    if not nationality and wd.get('nationalityId'):
        nationality = labels.get(wd['nationalityId'], '')
    if not nationality:
        nationality = 'International'
    
    birth_place = ''
    if wd.get('birthPlaceId'):
        birth_place = labels.get(wd['birthPlaceId'], '')
    if not birth_place and parsed.get('birth_date', ''):
        m = re.search(r'born\s+[^.]+\s+in\s+([A-Za-z\s,]+)', extract)
        if m:
            birth_place = m.group(1).strip()
    if not birth_place:
        birth_place = 'Unknown'
    
    occupation = parsed.get('occupation', '')
    if not occupation and wd.get('occupationIds'):
        occs = [labels.get(oid, '') for oid in wd['occupationIds'] if labels.get(oid)]
        if occs:
            occupation = ', '.join(occs[:3])
    if not occupation:
        occupation = cat_label.capitalize()
    
    full_name = wd.get('fullName', title)
    
    desc = extract[:200] if extract else f"Biography of {title}, {nationality} {occupation.lower()}."
    
    tags = [occ.capitalize() for occ in occupation.split(', ')][:2]
    tags.append(nationality)
    tags.append(cat_label.capitalize())
    
    paras = [p.strip() for p in extract.split('\n') if p.strip()]
    bio_text_1 = paras[1] if len(paras) > 1 else f"{title} has established themselves as a prominent {occupation.lower()}."
    bio_text_2 = paras[2] if len(paras) > 2 else f"Born in {birth_place}, {title} has achieved recognition for their work."
    career_text = paras[2] if len(paras) > 2 else f"Throughout their career, {title} has worked extensively as a {occupation.lower()}."
    personal_life = f"{title} was born in {birth_place} on {birth_date_display}."
    if len(paras) > 3:
        personal_life = paras[3]
    
    years_active = '2000\u2013present'
    try:
        birth_year = int(birth_date_iso[:4])
        if birth_year < 1980: years_active = '1990\u2013present'
        elif birth_year < 1990: years_active = '2000\u2013present'
        elif birth_year < 2000: years_active = '2010\u2013present'
        else: years_active = '2020\u2013present'
    except:
        pass
    
    wiki_title = title.replace(' ', '_')
    bio_data = {
        'slug': slug, 'name': title, 'full_name': full_name,
        'description': desc.strip(), 'image': image,
        'birth_date_iso': birth_date_iso, 'birth_date_display': birth_date_display,
        'birth_place': birth_place, 'nationality': nationality,
        'profession': occupation, 'years_active': years_active,
        'wiki_title': wiki_title, 'wikipedia_url': f"https://en.wikipedia.org/wiki/{wiki_title}",
        'wikidata_id': wikidata_id, 'tags': tags[:6],
        'bio_text_1': bio_text_1[:300], 'bio_text_2': bio_text_2[:300],
        'career_text': career_text[:300], 'personal_life_text': personal_life[:300],
        'img_height': 660,
    }
    
    bio_data['json_ld'] = build_json_ld(bio_data)
    
    return generate_bio(bio_data)

def iterate_category(cat_name, cat_label_default, total, target):
    """Iterate through a Wikipedia category, generating bios for new candidates."""
    params = {
        'action': 'query',
        'generator': 'categorymembers',
        'gcmtitle': f'Category:{cat_name}',
        'gcmlimit': 500,
        'gcmtype': 'page',
        'prop': 'pageimages|pageprops',
        'pithumbsize': 440,
        'ppprop': 'wikibase_item',
    }
    
    while total < target:
        data = wiki_api(params)
        if not data:
            break
        
        pages = data.get('query', {}).get('pages', {})
        if not pages:
            break
        
        for pid, page in sorted(pages.items(), key=lambda x: int(x[0])):
            if total >= target:
                return total
            
            title = page.get('title', '')
            if ':' in title:
                continue
            
            thumbnail = page.get('thumbnail', {}).get('source', '')
            if not thumbnail:
                continue
            
            wd_id = page.get('pageprops', {}).get('wikibase_item', '')
            if not wd_id:
                continue
            
            try:
                wd = get_wikidata_entity(wd_id)
                occ_ids = wd.get('occupationIds', [])
                cat_label = infer_category(occ_ids) if occ_ids else cat_label_default
                
                bio_html = process_page(title, cat_label, cat_name)
                if bio_html:
                    filepath = os.path.join(BIOS_DIR, f"{make_slug(title)}.html")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(bio_html)
                    total += 1
                    if total % 25 == 0:
                        print(f"  Generated {total}/{target}")
                    time.sleep(0.25)
            except Exception as e:
                continue
        
        cont = data.get('continue', {})
        cont_keys = [k for k in cont if k != 'continue']
        if cont_keys:
            for k in cont_keys:
                params[k] = cont[k]
        else:
            break
    
    return total


def main():
    total = 0
    target = 1200
    
    print("Generating 1,200 bios from Wikipedia...")
    print(f"Existing bios: {len(EXISTING)}")
    
    # Ordered list of categories to iterate through
    categories = [
        ("Living_people", "singer"),
        ("English-language_singers", "singer"),
        ("American_film_actors", "actor"),
        ("American_television_actors", "actor"),
        ("American_comedians", "comedian"),
        ("American_businesspeople", "business"),
        ("American_female_models", "model"),
        ("British_rock_singers", "singer"),
        ("American_actresses", "actor"),
        ("American_singer-songwriters", "singer"),
        ("English_actresses", "actor"),
        ("French_actors", "actor"),
        ("German_actors", "actor"),
        ("Italian_actors", "actor"),
        ("American_record_producers", "singer"),
        ("American_television_producers", "business"),
        ("American_scientists", "scientist"),
        ("American_chefs", "chef"),
        ("American_journalists", "journalist"),
        ("British_actresses", "actor"),
        ("Australian_actors", "actor"),
        ("American_rappers", "singer"),
        ("American_television_personalities", "tv"),
        ("American_writers", "writer"),
        ("English_cricketers", "sports"),
        ("American_tennis_players", "tennis"),
        ("American_novelists", "writer"),
        ("American_politicians", "politician"),
        ("American_film_directors", "director"),
        ("Canadian_actors", "actor"),
        ("Indian_actors", "actor"),
        ("American_entrepreneurs", "business"),
        ("Spanish_singers", "singer"),
        ("French_singers", "singer"),
        ("Italian_singers", "singer"),
        ("American_youTubers", "influencer"),
        ("Colombian_singers", "singer"),
        ("Mexican_singers", "singer"),
        ("Puerto_Rican_singers", "singer"),
        ("Argentine_singers", "singer"),
        ("Brazilian_singers", "singer"),
    ]
    
    for cat_name, cat_label in categories:
        if total >= target:
            break
        print(f"\n--- {cat_name} ({cat_label}) ---")
        prev = total
        total = iterate_category(cat_name, cat_label, total, target)
        print(f"  Got {total - prev} from {cat_name} (total: {total})")
    
    print(f"\n=== DONE: Generated {total} new bios ===")

if __name__ == '__main__':
    main()
