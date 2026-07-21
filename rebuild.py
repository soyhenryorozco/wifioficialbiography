#!/usr/bin/env python3
"""
Rebuild index.html, app.js, sitemap.xml from all bio HTML files.
Parses existing bios to extract metadata and regenerates all files.
"""

import os, re, glob, html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIOS_DIR = os.path.join(BASE_DIR, 'bios')
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')
APPJS_FILE = os.path.join(BASE_DIR, 'js', 'app.js')
SITEMAP_FILE = os.path.join(BASE_DIR, 'sitemap.xml')
DOMAIN = 'https://wifioficialbiography.org'


def parse_bio(filepath):
    """Parse a bio HTML file and extract metadata."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    slug = os.path.basename(filepath).replace('.html', '')

    name_m = re.search(r'<h1 itemprop="name">(.*?)</h1>', content)
    name = html.unescape(name_m.group(1).strip()) if name_m else slug.replace('-', ' ').title()

    full_name_m = re.search(r'<div class="subtitle" itemprop="alternateName">(.*?)</div>', content)
    full_name = html.unescape(full_name_m.group(1).strip()) if full_name_m else name

    desc_m = re.search(r'<p itemprop="description">(.*?)</p>', content)
    excerpt = html.unescape(desc_m.group(1).strip()) if desc_m else ''

    job_m = re.search(r'itemprop="jobTitle">(.*?)</td>', content)
    profession = html.unescape(job_m.group(1).strip()) if job_m else 'Public Figure'

    img_m = re.search(r'itemprop="image"\s+content="(.*?)"', content) or \
            re.search(r'content="(https://upload\.wikimedia\.org/[^"]*)"[^>]*>\s*<meta\s+name="twitter:card"', content) or \
            re.search(r'<img[^>]*class="bio-hero-img"[^>]*src="(.*?)"', content)
    image = img_m.group(1).strip() if img_m else ''

    if not image:
        og_m = re.search(r'<meta property="og:image" content="(.*?)"', content)
        image = og_m.group(1).strip() if og_m else ''

    born_m = re.search(r'itemprop="birthDate"[^>]*>(.*?)</(?:time|span)>', content)
    born = html.unescape(born_m.group(1).strip()) if born_m else ''

    place_m = re.search(r'<span itemprop="birthPlace">(.*?)</span>', content)
    birth_place = html.unescape(place_m.group(1).strip()) if place_m else ''

    nat_m = re.search(r'itemprop="nationality">(.*?)</td>', content)
    nationality = html.unescape(nat_m.group(1).strip()) if nat_m else ''

    tags = re.findall(r'<a href="#" class="category-tag">(.*?)</a>', content)

    cat_m = re.search(r'data-category="([^"]*)"', content)
    if not cat_m:
        cat_map = {
            'cantante': 'singer', 'singer': 'singer', 'músico': 'singer', 'music': 'singer',
            'actor': 'actor', 'actress': 'actor', 'actriz': 'actor',
            'futbolista': 'footballer', 'footballer': 'footballer', 'soccer': 'footballer',
            'ciclista': 'cyclist', 'cyclist': 'cyclist',
            'deportista': 'sports', 'athlete': 'sports', 'boxer': 'boxer',
            'tenis': 'tennis', 'tennis': 'tennis',
            'baloncesto': 'basketball', 'basketball': 'basketball',
            'béisbol': 'baseball', 'baseball': 'baseball',
            'político': 'politician', 'politician': 'politician',
            'periodista': 'journalist', 'journalist': 'journalist',
            'influencer': 'influencer', 'escritor': 'writer', 'writer': 'writer',
            'comediante': 'comedian', 'comedian': 'comedian',
            'presentador': 'tv', 'presentadora': 'tv', 'television': 'tv',
            'chef': 'chef', 'cocinero': 'chef',
            'empresario': 'business', 'business': 'business',
            'empresaria': 'business',
            'director': 'director', 'directora': 'director',
            'productor': 'producer', 'productora': 'producer',
            'modelo': 'model', 'model': 'model',
            'tecnología': 'tech', 'tech': 'tech',
        }
        prof_lower = profession.lower()
        category = 'singer'
        for key, val in cat_map.items():
            if key in prof_lower:
                category = val
                break
    else:
        category = cat_m.group(1)

    date_added = 0
    try:
        st = os.stat(filepath)
        date_added = int(st.st_birthtime) if hasattr(st, 'st_birthtime') else int(st.st_ctime)
    except:
        pass

    return {
        'slug': slug,
        'name': name,
        'fullName': full_name,
        'profession': profession,
        'born': born,
        'birthPlace': birth_place,
        'nationality': nationality,
        'excerpt': excerpt,
        'image': image,
        'tags': tags,
        'category': category,
        'dateAdded': date_added,
    }


def generate_card(ce):
    tags_html = ''.join(f'<span class="bio-card-tag">{t}</span>' for t in ce['tags'][:3])
    excerpt_short = ce['excerpt'][:150].replace('"', '&quot;')
    return f'''          <a href="bios/{ce['slug']}.html" class="bio-card" itemscope itemtype="https://schema.org/Person" data-category="{ce['category']}">
            <img src="{ce['image']}" alt="{ce['name']}" class="bio-card-img" width="400" height="250" loading="lazy" itemprop="image">
            <div class="bio-card-body">
              <h3 class="bio-card-name" itemprop="name">{ce['name']}</h3>
              <div class="bio-card-profession" itemprop="jobTitle">{ce['profession']}</div>
              <p class="bio-card-excerpt" itemprop="description">{excerpt_short}</p>
              <div class="bio-card-meta">
                {tags_html}
              </div>
            </div>
          </a>'''


def _esc(s):
    return s.replace("'", "\\'").replace('\n', ' ')

def generate_appjs_entry(ce):
    tags_str = ', '.join(f"\"{t.replace(chr(34), chr(92)+chr(34))}\"" for t in ce['tags'])
    img = _esc(ce['image'])
    return f"    {{id:'{ce['slug']}',name:'{_esc(ce['name'])}',fullName:'{_esc(ce['fullName'])}',profession:'{_esc(ce['profession'])}',excerpt:'{_esc(ce['excerpt'])}',url:'bios/{ce['slug']}.html',tags:[{tags_str}],image:'{img}',dateAdded:{ce['dateAdded']}}},"

def generate_latest_bios_js(bios):
    """Generate the latestBios JS array (8 newest by dateAdded)."""
    sorted_bios = sorted(bios, key=lambda x: -x['dateAdded'])[:8]
    entries = []
    for b in sorted_bios:
        cat_icons = {'singer':'🎵','actor':'🎬','footballer':'⚽','politician':'🏛️','journalist':'📰','boxer':'🥊','cyclist':'🚴','tennis':'🎾','basketball':'🏀','baseball':'⚾','comedian':'😂','model':'👗','business':'💼','director':'🎥','chef':'🍳','sports':'🏆','writer':'✍️'}
        icon = cat_icons.get(b['category'], '📌')
        entries.append(f"    {{url:'bios/{b['slug']}.html',name:'{_esc(b['name'])}',icon:'{icon}'}}")
    return '  const latestBios = [\n' + ',\n'.join(entries) + '\n  ];\n'


def url_esc(s):
    """XML-esc + percent-encode non-ASCII chars in a URL."""
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return re.sub(r'[^\x20-\x7E]', lambda m: ''.join(f'%{b:02X}' for b in m.group(0).encode('utf-8')), s)

def generate_sitemap_entry(ce):
    def xml_esc(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    img_block = ''
    if ce['image']:
        img_block = f"""    <image:image>
      <image:loc>{url_esc(ce['image'])}</image:loc>
      <image:title>{xml_esc(ce['name'])} -- Portrait</image:title>
      <image:caption>{xml_esc(ce['name'])}, {xml_esc(ce['nationality'])} {xml_esc(ce['profession'].split(chr(8226))[0].strip())}</image:caption>
    </image:image>
"""
    return f"""  <!-- {xml_esc(ce['name'])} -->
  <url>
    <loc>{DOMAIN}/bios/{ce['slug']}.html</loc>
    <lastmod>2026-07-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
{img_block}  </url>"""


def rebuild():
    bio_files = sorted(glob.glob(os.path.join(BIOS_DIR, '*.html')))
    print(f'Found {len(bio_files)} bio files')

    bios = []
    for bf in bio_files:
        try:
            ce = parse_bio(bf)
            bios.append(ce)
        except Exception as e:
            print(f'  Error parsing {bf}: {e}')

    bios.sort(key=lambda x: x['name'].lower())
    print(f'Parsed {len(bios)} bios successfully')

    cats = {}
    for b in bios:
        c = b['category']
        cats[c] = cats.get(c, 0) + 1
    total = len(bios)

    print(f'\nCategory counts:')
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f'  {c}: {n}')
    print(f'  TOTAL: {total}')

    print('\nRebuilding index.html...')
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        idx = f.read()

    cards = '\n'.join(generate_card(b) for b in bios)

    PAGINATION_BLOCK = f'''      <div class="show-more-bios-container">
        <span class="show-more-bios-count" id="showMoreCount">Mostrando 20 de {total} biografías</span>
        <button class="show-more-bios" id="showMoreBios">Ver más biografías ▾</button>
      </div>'''

    start_marker = '<div class="bio-grid" id="bioGrid">'
    cat_target = '<section id="categorias"'

    if start_marker in idx and cat_target in idx:
        start_idx = idx.index(start_marker) + len(start_marker)
        cat_idx = idx.index(cat_target)

        new_block = f'\n{cards}\n        </div>\n      </section>\n{PAGINATION_BLOCK}\n      '
        idx = idx[:start_idx] + new_block + idx[cat_idx:]
    else:
        print('  WARNING: Could not find bio-grid or categorias markers in index.html')

    import re as _re
    idx = _re.sub(
        r'(<button class="bio-filter-btn active" data-filter="all">Todos <span class="filter-count">)\d+(</span>)',
        f'\\g<1>{total}\\2', idx)
    idx = _re.sub(
        r'(<div class="bio-filter-results"[^>]*>Mostrando \d+ de )\d+( biografías</div>)',
        f'\\g<1>{total}\\2', idx)

    for cat, count in cats.items():
        pattern = rf'(<button class="bio-filter-btn[^"]*" data-filter="{cat}">[^<]*<span class="filter-count">)\d+(</span>)'
        idx = _re.sub(pattern, f'\\g<1>{count}\\2', idx)

    idx = _re.sub(
        r'(<span class="stat-number">)\d+(</span>\s*<span class="stat-label">Biografías</span>)',
        f'\\g<1>{total}\\2', idx)

    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(idx)
    print(f'  Written {total} cards to index.html')

    print('Rebuilding app.js...')
    with open(APPJS_FILE, 'r', encoding='utf-8') as f:
        js = f.read()

    entries = '\n'.join(generate_appjs_entry(b) for b in bios)

    marker_start = '  const biographies = [\n'
    marker_end = '  ];\n\n  var so='

    if marker_start in js and marker_end in js:
        s_idx = js.index(marker_start) + len(marker_start)
        e_idx = js.index(marker_end)
        js = js[:s_idx] + entries + '\n' + js[e_idx:]
    else:
        print('  WARNING: Could not find app.js markers')

    # Replace sidebar hardcoded list with dynamic latestBios usage
    sidebar_start = '  (function(){var la='
    sidebar_end = '}})();'
    if sidebar_start in js:
        s_idx2 = js.index(sidebar_start)
        e_idx2 = js.index(sidebar_end, s_idx2) + len(sidebar_end)
        latest_js = generate_latest_bios_js(bios)
        sidebar_new = f'''{latest_js}
  (function(){{
    var el=document.getElementById('latestBiosList');
    if(el){{
      el.innerHTML=latestBios.map(function(b){{
        return '<li><a href="'+b.url+'"><span>'+b.icon+'</span> '+b.name+'</a></li>';
      }}).join('');
    }}
  }})();'''
        js = js[:s_idx2] + sidebar_new + js[e_idx2:]
    else:
        print('  WARNING: Could not find sidebar marker')

    with open(APPJS_FILE, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f'  Written {total} entries to app.js')

    print('Rebuilding sitemap.xml...')
    sitemap_entries = '\n'.join(generate_sitemap_entry(b) for b in bios)

    sm_header = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">

  <!-- Homepage -->
  <url>
    <loc>https://wifioficialbiography.org/</loc>
    <lastmod>2026-07-11</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>https://wifioficialbiography.org/images/henry-orozco.jpg</image:loc>
      <image:title>Wifi Oficial Biography -- Enciclopedia de Biografias</image:title>
      <image:caption>Plataforma de biografias de figuras publicas a nivel internacional</image:caption>
    </image:image>
  </url>

'''
    sm_footer = '\n</urlset>\n'

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(sm_header + sitemap_entries + sm_footer)
    print(f'  Written {total + 1} URLs to sitemap.xml')

    print(f'\n=== REBUILD COMPLETE ===')
    print(f'Total bios: {total}')
    print(f'Categories: {len(cats)}')
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f'  {c}: {n}')


if __name__ == '__main__':
    rebuild()
