#!/usr/bin/env python3
"""
Wifioficial Biography Generator
Fetches Wikipedia data and generates bio HTML files, index cards, app.js entries, sitemap entries.
Usage: python3 generate_bios.py <batch_file.json> [--merge]
"""

import json, os, sys, re, time, hashlib
import requests
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIOS_DIR = os.path.join(BASE_DIR, 'bios')
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')
APPJS_FILE = os.path.join(BASE_DIR, 'js', 'app.js')
SITEMAP_FILE = os.path.join(BASE_DIR, 'sitemap.xml')

DOMAIN = 'https://wifioficialbiography.org'
USER_AGENT = 'WifioficialBioBot/1.0 (https://wifioficialbiography.org; contact@wifioficialbiography.org)'
WIKI_API = 'https://en.wikipedia.org/api/rest_v1/page/summary/{}'

CATEGORY_LABELS = {
    'singer': 'Cantante',
    'actor': 'Actor/Actriz',
    'footballer': 'Futbolista',
    'cyclist': 'Ciclista',
    'sports': 'Deportista',
    'politician': 'Político',
    'journalist': 'Periodista',
    'influencer': 'Influencer',
    'writer': 'Escritor',
    'boxer': 'Boxeador',
    'tennis': 'Tenis',
    'basketball': 'Baloncesto',
    'baseball': 'Béisbol',
    'mma': 'MMA',
    'racing': 'Automovilismo',
    'swimming': 'Natación',
    'olympic': 'Olímpico',
    'model': 'Modelo',
    'tv': 'Televisión',
    'comedian': 'Comediante',
    'producer': 'Productor',
    'director': 'Director',
    'chef': 'Chef',
    'business': 'Empresario',
    'tech': 'Tecnología',
}

session = requests.Session()
session.headers.update({'User-Agent': USER_AGENT})


def slugify(name):
    s = name.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')


def fetch_wiki(title):
    """Fetch Wikipedia summary for a person. Returns dict or None."""
    try:
        encoded = quote(title.replace(' ', '_'), safe='/')
        url = WIKI_API.format(encoded)
        r = session.get(url, timeout=10)
        if r.status_code != 200:
            return None
        d = r.json()
        img = d.get('originalimage', {}).get('source') or d.get('thumbnail', {}).get('source', '')
        if '/thumb/' in img:
            parts = img.split('/thumb/')
            fname = parts[1].rsplit('/', 1)[0]
            img = parts[0] + '/' + fname
        return {
            'title': d.get('title', title),
            'description': d.get('description', ''),
            'extract': d.get('extract', ''),
            'image': img,
        }
    except Exception as e:
        print(f'  [WARN] Wiki fetch failed for {title}: {e}')
        return None


def parse_date_from_extract(extract):
    """Try to extract birth date from Wikipedia extract text."""
    m = re.search(r'\((?:born\s+)?(\w+\s+\d{1,2},?\s+\d{4})', extract)
    if m:
        return m.group(1).replace(',', '').strip()
    m = re.search(r'\((?:born\s+)?(\d{1,2}\s+\w+\s+\d{4})', extract)
    if m:
        return m.group(1).strip()
    return None


def parse_birthplace_from_extract(extract):
    """Try to extract birthplace from extract."""
    m = re.search(r'(?:born|born in|birth place)\s+(?:in\s+)?([A-Z][\w\s]+(?:,\s*[A-Z][\w\s]+){0,2})', extract)
    if m:
        return m.group(1).strip().rstrip('.')
    return None


def guess_wiki_title(name):
    """Generate possible Wikipedia titles to try."""
    titles = [name]
    parts = name.split()
    if len(parts) >= 2:
        titles.append(name)
        titles.append(f"{parts[-1]}, {parts[0]}")
    return titles


def generate_html(ce):
    """Generate bio HTML page content."""
    name = ce['name']
    slug = ce['slug']
    full_name = ce.get('fullName', name)
    profession = ce.get('profession', ce.get('category', 'Public Figure'))
    born = ce.get('born', '')
    birth_place = ce.get('birthPlace', '')
    nationality = ce.get('nationality', '')
    excerpt = ce.get('excerpt', '')
    image = ce.get('image', '')
    wiki_title = ce.get('wiki_title', name)
    tags = ce.get('tags', [])

    tags_html = ''.join(f'<a href="#" class="category-tag">{t}</a>' for t in tags[:8])

    born_display = born
    born_iso = ''
    if born:
        import re as _re
        m = _re.match(r'(\w+\s+\d{1,2},?\s+\d{4})', born)
        if m:
            months = {'January':'01','February':'02','March':'03','April':'04','May':'05','June':'06',
                       'July':'07','August':'08','September':'09','October':'10','November':'11','December':'12'}
            parts = m.group(1).replace(',','').split()
            if len(parts) == 3 and parts[0] in months:
                born_iso = f"{parts[2]}-{months[parts[0]]}-{int(parts[1]):02d}"

    date_tag = f'<time itemprop="birthDate" datetime="{born_iso}">{born_display}</time>' if born_iso else f'<span itemprop="birthDate">{born_display}</span>'

    bio_text = f"""<p><strong>{full_name}</strong> (born {date_tag}), known as <strong>{name}</strong>, is a {nationality.lower()} {profession.lower().split('•')[0].strip()}. Born in <span itemprop="birthPlace">{birth_place}</span>, {excerpt}</p>"""
    if ce.get('wiki_title'):
        bio_text += f"""
        <p>For more information, visit <a href="https://en.wikipedia.org/wiki/{quote(ce['wiki_title'].replace(' ', '_'))}" target="_blank" rel="noopener">Wikipedia: {name}</a>.</p>"""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name} -- Wikipedia-like Biography | Wifioficial Biography</title>
  <meta name="description" content="Complete biography of {name}, {nationality} {profession.lower()}. {excerpt[:120]}">
  <meta name="keywords" content="{name}, {nationality}, {birth_place}, biography, Wikipedia">
  <meta name="author" content="Wifioficial Biography">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{DOMAIN}/bios/{slug}.html">
  <meta property="og:title" content="{name} -- {profession}">
  <meta property="og:description" content="{excerpt[:200]}">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="{DOMAIN}/bios/{slug}.html">
  <meta property="og:site_name" content="Wifioficial Biography">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{name} -- {profession}">
  <meta name="twitter:description" content="{excerpt[:200]}">
  <meta name="twitter:image" content="{image}">
  <meta name="theme-color" content="#4CAF50">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "{name}",
    "alternateName": "{full_name}",
    "description": "{excerpt[:300].replace('"', "'")}",
    "birthDate": "{born_iso}",
    "birthPlace": {{"@type": "Place", "name": "{birth_place}"}},
    "nationality": {{"@type": "Country", "name": "{nationality}"}},
    "jobTitle": "{profession}",
    "image": "{image}",
    "sameAs": ["https://en.wikipedia.org/wiki/{quote(ce.get('wiki_title', name).replace(' ', '_'))}"]
  }}
  </script>
</head>
<body>
  <header class="site-header" role="banner"><div class="header-inner"><a href="../index.html" class="site-logo"><div class="logo-icon">W</div><div class="logo-text">Wifioficial <span>Biography</span></div></a><nav class="main-nav"><ul><li><a href="../index.html">Inicio</a></li><li><a href="../index.html#biografias">Biografias</a></li><li><a href="../index.html#categorias">Categorias</a></li></ul></nav></div></header>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">
      <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="../index.html">Inicio</a> <span class="separator">></span> <a href="../index.html#biografias">Biografias</a> <span class="separator">></span> <span>{name}</span></nav>
      <div class="bio-page-header">
        <div class="bio-page-img"><img src="{image}" alt="Photo of {name}" class="bio-hero-img" itemprop="image"></div><div class="bio-page-info">
          <h1 itemprop="name">{name}</h1>
          <div class="subtitle" itemprop="alternateName">{full_name}</div>
          <p itemprop="description">{excerpt}</p>
        </div>
      </div>
      <div class="infobox" role="complementary">
        <div class="infobox-header">{name}</div>
        <table><tbody>
          <tr><th>Full Name</th><td itemprop="birthName">{full_name}</td></tr>
          <tr><th>Born</th><td>{date_tag}<br><span itemprop="birthPlace">{birth_place}</span></td></tr>
          <tr><th>Nationality</th><td itemprop="nationality">{nationality}</td></tr>
          <tr><th>Occupation(s)</th><td itemprop="jobTitle">{profession}</td></tr>
        </tbody></table>
      </div>
      <article class="bio-article">
        <div class="category-tags">{tags_html}</div>
        {bio_text}
        <h2 id="references">References</h2>
        <div class="reflist"><ol>
          <li><span class="cite-note">"{name}." Wikipedia. <a href="https://en.wikipedia.org/wiki/{quote(ce.get('wiki_title', name).replace(' ', '_'))}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{ce.get('wiki_title', name).replace(' ', '_')}</a></span></li>
        </ol></div>
      </article>
    </main>
  </div>
  <footer class="site-footer"><div class="footer-inner"><p>&copy; 2026 Wifioficial Biography.</p></div></footer>
  <script src="../js/app.js"></script>
</body>
</html>'''


def generate_card(ce):
    """Generate a bio card for index.html."""
    name = ce['name']
    slug = ce['slug']
    profession = ce.get('profession', '')
    category = ce.get('category', 'singer')
    image = ce.get('image', '')
    excerpt = ce.get('excerpt', '')[:150]
    tags = ce.get('tags', [])
    tags_html = ''.join(f'<span class="bio-card-tag">{t}</span>' for t in tags[:3])
    prof_parts = profession.split('•')
    prof_display = profession
    return f'''          <a href="bios/{slug}.html" class="bio-card" itemscope itemtype="https://schema.org/Person" data-category="{category}">
            <img src="{image}" alt="{name}" class="bio-card-img" width="400" height="250" loading="lazy" itemprop="image">
            <div class="bio-card-body">
              <h3 class="bio-card-name" itemprop="name">{name}</h3>
              <div class="bio-card-profession" itemprop="jobTitle">{prof_display}</div>
              <p class="bio-card-excerpt" itemprop="description">{excerpt}</p>
              <div class="bio-card-meta">
                {tags_html}
              </div>
            </div>
          </a>'''


def generate_appjs_entry(ce):
    """Generate an app.js biography entry."""
    tags_str = ', '.join(f"'{t}'" for t in ce.get('tags', []))
    name = ce['name']
    excerpt = ce.get('excerpt', '').replace("'", "\\'")
    return f"""    {{
      id: '{ce['slug']}',
      name: '{name}',
      fullName: '{ce.get('fullName', name)}',
      profession: '{ce.get('profession', '')}',
      born: '{ce.get('born', '')}',
      birthPlace: '{ce.get('birthPlace', '')}',
      nationality: '{ce.get('nationality', '')}',
      excerpt: '{excerpt}',
      url: 'bios/{ce['slug']}.html',
      tags: [{tags_str}],
      image: '{ce.get('image', '')}'
    }},"""


def generate_sitemap_entry(ce):
    """Generate a sitemap.xml entry."""
    name = ce['name']
    slug = ce['slug']
    image = ce.get('image', '')
    return f"""  <!-- {name} -->
  <url>
    <loc>{DOMAIN}/bios/{slug}.html</loc>
    <lastmod>2026-07-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <image:image>
      <image:loc>{image}</image:loc>
      <image:title>{name} -- Portrait</image:title>
      <image:caption>{name}, {ce.get('nationality', '')} {ce.get('profession', '').split('•')[0].strip()}</image:caption>
    </image:image>
  </url>"""


def process_batch(batch_file, merge=False):
    """Process a batch of celebrities from a JSON file."""
    with open(batch_file, 'r', encoding='utf-8') as f:
        celebrities = json.load(f)

    os.makedirs(BIOS_DIR, exist_ok=True)

    existing = set()
    for fn in os.listdir(BIOS_DIR):
        if fn.endswith('.html'):
            existing.add(fn.replace('.html', ''))

    new_bios = []
    skipped = 0
    total = len(celebrities)

    for i, ce in enumerate(celebrities):
        slug = ce.get('slug', slugify(ce['name']))
        ce['slug'] = slug

        if slug in existing:
            skipped += 1
            continue

        print(f'[{i+1}/{total}] {ce["name"]}...', end=' ', flush=True)

        wiki_data = None
        wiki_titles = guess_wiki_title(ce['name'])
        if ce.get('wiki_title'):
            wiki_titles.insert(0, ce['wiki_title'])

        for wt in wiki_titles:
            wiki_data = fetch_wiki(wt)
            if wiki_data:
                ce['wiki_title'] = wt
                break
            time.sleep(0.1)

        if not wiki_data:
            if not ce.get('image'):
                print('SKIP (no wiki)')
                continue
            wiki_data = {'title': ce['name'], 'description': '', 'extract': '', 'image': ce.get('image', '')}

        if not ce.get('image') and wiki_data.get('image'):
            ce['image'] = wiki_data['image']

        if not ce.get('excerpt') and wiki_data.get('extract'):
            ce['excerpt'] = wiki_data['extract'][:250].replace('\n', ' ')
        elif not ce.get('excerpt') and wiki_data.get('description'):
            ce['excerpt'] = wiki_data['description']

        if not ce.get('born') and wiki_data.get('extract'):
            parsed_date = parse_date_from_extract(wiki_data['extract'])
            if parsed_date:
                ce['born'] = parsed_date

        if not ce.get('birthPlace') and wiki_data.get('extract'):
            parsed_place = parse_birthplace_from_extract(wiki_data['extract'])
            if parsed_place:
                ce['birthPlace'] = parsed_place

        if not ce.get('image'):
            print('SKIP (no image)')
            continue

        ce['image'] = ce['image'].replace('/thumb/', '/').split('/220px-')[0].split('/300px-')[0].split('/400px-')[0].split('/640px-')[0]
        if '/thumb/' in ce['image']:
            parts = ce['image'].split('/thumb/')
            fname = parts[1].rsplit('/', 1)[0] if '/' in parts[1] else parts[1]
            ce['image'] = parts[0] + '/' + fname

        html_content = generate_html(ce)
        html_path = os.path.join(BIOS_DIR, f'{slug}.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        new_bios.append(ce)
        print('OK')
        time.sleep(0.15)

    print(f'\n--- Batch Summary ---')
    print(f'Total in batch: {total}')
    print(f'New bios generated: {len(new_bios)}')
    print(f'Skipped (existing): {skipped}')

    if merge and new_bios:
        merge_files(new_bios)

    return new_bios


def merge_files(new_bios):
    """Merge new bios into index.html, app.js, sitemap.xml."""
    print('\nMerging into index.html...')
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()

    cards = '\n'.join(generate_card(ce) for ce in new_bios)
    insert_marker = '        </div>\n      </section>\n\n      <!-- ALL CATEGORIES -->'
    if insert_marker in index_content:
        index_content = index_content.replace(insert_marker, cards + '\n' + insert_marker)
    else:
        alt_marker = '        </div>\n      </section>'
        idx = index_content.rfind(alt_marker)
        if idx != -1:
            index_content = index_content[:idx] + '\n' + cards + '\n' + index_content[idx:]

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f'  Added {len(new_bios)} cards to index.html')

    print('Merging into app.js...')
    with open(APPJS_FILE, 'r', encoding='utf-8') as f:
        appjs_content = f.read()

    entries = '\n'.join(generate_appjs_entry(ce) for ce in new_bios)
    appjs_marker = '  ];\n\n  // ── Search Functionality'
    if appjs_marker in appjs_content:
        appjs_content = appjs_content.replace(appjs_marker, entries + '\n  ];\n\n  // ── Search Functionality')

    with open(APPJS_FILE, 'w', encoding='utf-8') as f:
        f.write(appjs_content)
    print(f'  Added {len(new_bios)} entries to app.js')

    print('Merging into sitemap.xml...')
    with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
        sitemap_content = f.read()

    sitemap_entries = '\n'.join(generate_sitemap_entry(ce) for ce in new_bios)
    sitemap_marker = '</urlset>'
    if sitemap_marker in sitemap_content:
        sitemap_content = sitemap_content.replace(sitemap_marker, sitemap_entries + '\n</urlset>')

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print(f'  Added {len(new_bios)} entries to sitemap.xml')

    print(f'\nTotal new bios merged: {len(new_bios)}')


def update_counts():
    """Recount all bios and update filter counts in index.html."""
    import glob as _glob

    bio_files = _glob.glob(os.path.join(BIOS_DIR, '*.html'))
    total = len(bio_files)
    print(f'\nTotal bio files: {total}')

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    import re as _re
    cats = _re.findall(r'data-category="([^"]*)"', content)
    from collections import Counter
    counts = Counter(cats)

    content = _re.sub(
        r'(<button class="bio-filter-btn active" data-filter="all">Todos <span class="filter-count">)\d+(</span>)',
        f'\\g<1>{total}\\2', content)

    for cat, count in counts.items():
        pattern = rf'(<button class="bio-filter-btn" data-filter="{cat}">[^<]*<span class="filter-count">)\d+(</span>)'
        content = _re.sub(pattern, f'\\g<1>{count}\\2', content)

    content = _re.sub(
        r'(<span class="stat-number" id="heroCount">)\d+(</span>)',
        f'\\g<1>{total}\\2', content)

    content = _re.sub(
        r'(<span class="stat-number">)\d+( Biografías</span>)',
        f'\\g<1>{total}\\2', content)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated index.html counts: {total} total')
    for cat, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f'  {cat}: {count}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generate_bios.py <batch.json> [--merge] [--counts]")
        sys.exit(1)

    if sys.argv[1] == '--counts':
        update_counts()
        sys.exit(0)

    batch_file = sys.argv[1]
    merge = '--merge' in sys.argv
    process_batch(batch_file, merge=merge)
