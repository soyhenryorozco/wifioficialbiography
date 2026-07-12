#!/usr/bin/env python3
"""Add influencer entries to index.html, app.js, and sitemap.xml."""

import os

script_dir = os.path.dirname(os.path.abspath(__file__))
gen_path = os.path.join(script_dir, "generate_influencer_bios.py")

with open(gen_path, "r", encoding="utf-8") as f:
    source = f.read()

namespace = {}
exec(compile(source, gen_path, "exec"), namespace)
influencers = namespace["influencers"]

print(f"Loaded {len(influencers)} influencers")


def js_escape(s):
    return s.replace("\\", "\\\\").replace("'", "\\'")


# ── 1. Update index.html ──────────────────────────────────────
index_path = os.path.join(script_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

# Build HTML cards
cards = []
for inf in influencers:
    tags = inf["tags"]
    card = f'''          <a href="bios/{inf["id"]}.html" class="bio-card" itemscope itemtype="https://schema.org/Person" data-category="influencer">
            <img src="{inf["image"]}" alt="{inf["name"]}" class="bio-card-img" width="400" height="250" loading="lazy" itemprop="image">
            <div class="bio-card-body">
              <h3 class="bio-card-name" itemprop="name">{inf["name"]}</h3>
              <div class="bio-card-profession" itemprop="jobTitle">{inf["profession"]}</div>
              <p class="bio-card-excerpt" itemprop="description">{inf["description"]}</p>
              <div class="bio-card-meta">
                <span class="bio-card-tag">{tags[0]}</span><span class="bio-card-tag">{tags[1]}</span><span class="bio-card-tag">{tags[2]}</span>
              </div>
            </div>
          </a>
'''
    cards.append(card)

cards_text = "".join(cards)

# Insert cards BEFORE the </div> that closes bio-grid (line 11792)
# Pattern: last bio-card </a> followed by the closing </div> of bio-grid
# We insert before the </div> that comes right after the last </a> with class bio-card
marker = """          </a>
        </div>"""
replacement = """          </a>
""" + cards_text + """        </div>"""

assert marker in index_html, "Could not find bio-grid closing marker in index.html"
index_html = index_html.replace(marker, replacement, 1)

# Update stats
# Line 133: stat-number 1055 -> 1091
index_html = index_html.replace(
    '<span class="stat-number">1055</span>',
    '<span class="stat-number">1091</span>'
)

# Line 161: Todos filter count 1055 -> 1091
index_html = index_html.replace(
    'Todos <span class="filter-count">1055</span>',
    'Todos <span class="filter-count">1091</span>'
)

# Line 171: Influencers count 11 -> 47
index_html = index_html.replace(
    'Influencers <span class="filter-count">11</span>',
    'Influencers <span class="filter-count">47</span>'
)

# Line 11795: Mostrando 15 de 1055 -> 1091
index_html = index_html.replace(
    'Mostrando 15 de 1055',
    'Mostrando 15 de 1091'
)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)

print(f"Updated index.html: inserted {len(influencers)} cards, updated stats")


# ── 2. Update app.js ─────────────────────────────────────────
js_path = os.path.join(script_dir, "js", "app.js")
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

entries = []
for inf in influencers:
    tags_list = "[" + ", ".join(f"'{js_escape(t)}'" for t in inf["tags"]) + "]"
    entry = f"""    {{
      id: '{js_escape(inf["id"])}',
      name: '{js_escape(inf["name"])}',
      fullName: '{js_escape(inf["fullName"])}',
      profession: '{js_escape(inf["profession"])}',
      born: '{inf["birthDate"]}',
      birthPlace: '{js_escape(inf["birthPlace"])}',
      nationality: '{js_escape(inf["nationality"])}',
      excerpt: '{js_escape(inf["description"])}',
      url: 'bios/{inf["id"]}.html',
      tags: {tags_list},
      image: '{inf["image"]}'
    }},
"""
    entries.append(entry)

entries_text = "".join(entries)

# Insert before the ]; that closes the biographies array
# Find the last occurrence of "];" that closes the biographies array
idx = js_content.rfind("  ];")
assert idx != -1, "Could not find '];' closing biographies array in app.js"
js_content = js_content[:idx] + entries_text + js_content[idx:]

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Updated js/app.js: inserted {len(influencers)} biography entries")


# ── 3. Update sitemap.xml ─────────────────────────────────────
sitemap_path = os.path.join(script_dir, "sitemap.xml")
with open(sitemap_path, "r", encoding="utf-8") as f:
    sitemap_content = f.read()

sitemap_entries = []
for inf in influencers:
    entry = f"""  <url>
    <loc>https://wifioficial-biography.com/bios/{inf["id"]}.html</loc>
    <lastmod>2026-07-12</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>{inf["image"]}</image:loc>
      <image:title>{inf["name"]}</image:title>
      <image:caption>Biografía de {inf["name"]}</image:caption>
    </image:image>
  </url>
"""
    sitemap_entries.append(entry)

sitemap_text = "".join(sitemap_entries)
sitemap_content = sitemap_content.replace("</urlset>", sitemap_text + "</urlset>")

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap_content)

print(f"Updated sitemap.xml: inserted {len(influencers)} URL entries")
print("\nDone!")
