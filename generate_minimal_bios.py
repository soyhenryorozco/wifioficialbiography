#!/usr/bin/env python3
"""Generate minimal bios for a large curated list of notable figures (no API needed)."""
import os, glob, re, html as html_mod

BIOS_DIR = 'bios'
EXISTING = set()
for fp in glob.glob(os.path.join(BIOS_DIR, '*.html')):
    EXISTING.add(os.path.basename(fp).replace('.html', ''))

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
  <meta property="og:image" content="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png">
  <meta property="og:image:alt" content="{title}">
  <meta property="og:site_name" content="Wifi Oficial Biography">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:site" content="@wifioficial">
  <meta name="twitter:image" content="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png">
  <meta name="twitter:image:alt" content="{title}">
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
  "publisher": {{"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {{"@type": "ImageObject", "url": "https://wifioficialbiography.org/images/favicon.jpg"}}}}
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
  "image": "",
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
      <a href="../index.html" class="site-logo"><img src="https://wifioficialbiography.org/images/favicon.jpg" alt="Wifi Oficial Biography" class="logo-icon" width="32" height="32" style="border-radius:50%;"><div class="logo-text">Wifi Oficial <span>Biography</span></div></a>
      <nav class="main-nav" id="mainNav" role="navigation"><ul>
        <li><a href="../index.html">Inicio</a></li>
        <li><a href="../index.html#biografias">Biografías</a></li>
        <li><a href="../index.html#categorias">Categorías</a></li>
        <li><a href="../index.html#about">Acerca de</a></li>
      </ul></nav>
    </div>
  </header>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">
      <nav class="breadcrumbs"><a href="../index.html">Inicio</a> › <a href="../index.html#biografias">Biografías</a> › <span>{title}</span></nav>
      <div class="bio-page-header">
        <div class="bio-page-photo"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png" alt="{title}" width="220" height="275" loading="eager" fetchpriority="high" itemprop="image"></div>
        <div class="bio-page-info"><h1 itemprop="name">{title}</h1><p itemprop="description">{html_desc}</p></div>
      </div>
      <div class="infobox"><div class="infobox-header">{title}</div>
        <table><tbody>
          <tr><th>Occupation</th><td itemprop="jobTitle">{cat_display}</td></tr>
        </tbody></table>
        <div class="infobox-section">Profiles</div>
        <table><tbody>
          <tr><th>Wikipedia</th><td><a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">wikipedia.org/wiki/{wiki_title}</a></td></tr>
        </tbody></table>
      </div>
      <article class="bio-article">
        <h2>Biography</h2>
        <p><strong>{title}</strong> is a notable {profession}.</p>
    <section class="attribution-notice" style="margin-top:2rem;padding:1rem;background:#f5f5f5;border-left:4px solid #888;font-size:0.85rem;">
      <p><strong>Atribucion &mdash; CC BY-SA 4.0</strong></p>
      <p>El contenido textual esta basado en material de Wikipedia, disponible bajo licencia CC BY-SA 4.0.</p>
      <p><strong>Fuentes originales:</strong><br><a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">https://en.wikipedia.org/wiki/{wiki_title}</a></p>
    </section>
    <h2 id="references">References</h2>
        <div class="reflist"><ol>
          <li><span class="cite-note">"{title}." Wikipedia.</span></li>
        </ol></div>
      </article>
    </main>
  </div>
  <footer class="site-footer">
    <div class="footer-inner">
      <p>&copy; 2026 Wifi Oficial Biography.</p>
    </div>
  </footer>
  <script src="../js/app.js"></script>
</body>
</html>"""

def make_slug(title):
    slug = title.lower().replace(' ', '-')
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

# Large curated list: ~4200 top figures
FIGURES = [
    # === USA - MORE SINGERS (300) ===
    ("Aaliyah", "singer", "Singer"), ("Aaron_Carter", "singer", "Singer"),
    ("Adam_Levine", "singer", "Singer"), ("Akon", "singer", "Singer"),
    ("Alanis_Morissette", "singer", "Singer"), ("Alicia_Keys", "singer", "Singer"),
    ("Ashanti_(singer)", "singer", "Singer"), ("Ashlee_Simpson", "singer", "Singer"),
    ("Avril_Lavigne", "singer", "Singer"), ("B.o.B", "singer", "Rapper"),
    ("Backstreet_Boys", "singer", "Band"), ("Barbra_Streisand", "singer", "Singer"),
    ("Barenaked_Ladies", "singer", "Band"), ("Beastie_Boys", "singer", "Band"),
    ("Beck", "singer", "Singer"), ("Big_Sean", "singer", "Rapper"),
    ("Billy_Idol", "singer", "Singer"), ("Birdman_(rapper)", "singer", "Rapper"),
    ("Björk", "singer", "Singer"), ("Black_Eyed_Peas", "singer", "Band"),
    ("Blink-182", "singer", "Band"), ("Bon_Jovi", "singer", "Band"),
    ("Brandy_Norwood", "singer", "Singer"), ("Brittany_Murphy", "actor", "Actress"),
    ("Britney_Spears", "singer", "Singer"), ("Bruce_Springsteen", "singer", "Singer"),
    ("Bruno_Mars", "singer", "Singer"), ("Busta_Rhymes", "singer", "Rapper"),
    ("Camila_Cabello", "singer", "Singer"), ("Celine_Dion", "singer", "Singer"),
    ("Chaka_Khan", "singer", "Singer"), ("Childish_Gambino", "singer", "Rapper"),
    ("Chris_Brown", "singer", "Singer"), ("Christina_Aguilera", "singer", "Singer"),
    ("Ciara", "singer", "Singer"), ("Coldplay", "singer", "Band"),
    ("Common_(rapper)", "singer", "Rapper"), ("Coolio", "singer", "Rapper"),
    ("Cyndi_Lauper", "singer", "Singer"), ("Daddy_Yankee", "singer", "Singer"),
    ("Dave_Matthews_Band", "singer", "Band"), ("David_Bowie", "singer", "Singer"),
    ("Destiny's_Child", "singer", "Band"), ("Diana_Ross", "singer", "Singer"),
    ("Diddy", "singer", "Rapper"), ("DMX", "singer", "Rapper"),
    ("Donna_Summer", "singer", "Singer"), ("Dr._Dre", "singer", "Rapper"),
    ("Dua_Lipa", "singer", "Singer"), ("Duran_Duran", "singer", "Band"),
    ("Ed_Sheeran", "singer", "Singer"), ("Elton_John", "singer", "Singer"),
    ("Enrique_Iglesias", "singer", "Singer"), ("Enya", "singer", "Singer"),
    ("Eve_(rapper)", "singer", "Rapper"), ("Fergie_(singer)", "singer", "Singer"),
    ("Fleetwood_Mac", "singer", "Band"), ("Foo_Fighters", "singer", "Band"),
    ("G-Eazy", "singer", "Rapper"), ("Gloria_Estefan", "singer", "Singer"),
    ("Green_Day", "singer", "Band"), ("Gwen_Stefani", "singer", "Singer"),
    ("Halsey_(singer)", "singer", "Singer"), ("Iggy_Azalea", "singer", "Rapper"),
    ("Imagine_Dragons", "singer", "Band"), ("J._Cole", "singer", "Rapper"),
    ("Jack_Johnson_(musician)", "singer", "Singer"), ("Janet_Jackson", "singer", "Singer"),
    ("Jason_Derulo", "singer", "Singer"), ("Jay-Z", "singer", "Rapper"),
    ("Jennifer_Lopez", "singer", "Singer"), ("Jessi_J", "singer", "Singer"),
    ("Jewel_(singer)", "singer", "Singer"), ("Jimmy_Buffett", "singer", "Singer"),
    ("John_Legend", "singer", "Singer"), ("John_Mayer", "singer", "Singer"),
    ("Jonas_Brothers", "singer", "Band"), ("Justin_Bieber", "singer", "Singer"),
    ("Justin_Timberlake", "singer", "Singer"), ("Kacey_Musgraves", "singer", "Singer"),
    ("Kanye_West", "singer", "Rapper"), ("Katy_Perry", "singer", "Singer"),
    ("Kelly_Clarkson", "singer", "Singer"), ("Kelly_Rowland", "singer", "Singer"),
    ("Kendrick_Lamar", "singer", "Rapper"), ("Kesha", "singer", "Singer"),
    ("Khia", "singer", "Rapper"), ("Kid_Rock", "singer", "Singer"),
    ("Kylie_Minogue", "singer", "Singer"), ("Lady_Gaga", "singer", "Singer"),
    ("Lana_Del_Rey", "singer", "Singer"), ("Lenny_Kravitz", "singer", "Singer"),
    ("Lil_Nas_X", "singer", "Rapper"), ("Lil_Uzi_Vert", "singer", "Rapper"),
    ("Lil_Wayne", "singer", "Rapper"), ("Linkin_Park", "singer", "Band"),
    ("Lizzo", "singer", "Singer"), ("LL_Cool_J", "singer", "Rapper"),
    ("Lorde", "singer", "Singer"), ("Ludacris", "singer", "Rapper"),
    ("M.I.A._(rapper)", "singer", "Rapper"), ("Machine_Gun_Kelly", "singer", "Rapper"),
    ("Madonna", "singer", "Singer"), ("Mariah_Carey", "singer", "Singer"),
    ("Maroon_5", "singer", "Band"), ("Mary_J._Blige", "singer", "Singer"),
    ("Megan_Thee_Stallion", "singer", "Rapper"), ("Melanie_Martinez", "singer", "Singer"),
    ("Metallica", "singer", "Band"), ("Michael_Jackson", "singer", "Singer"),
    ("Miley_Cyrus", "singer", "Singer"), ("Missy_Elliott", "singer", "Rapper"),
    ("Mitchell_Tenpenny", "singer", "Singer"), ("Modest_Mouse", "singer", "Band"),
    ("Monica_(singer)", "singer", "Singer"), ("Mumford_&_Sons", "singer", "Band"),
    ("N.E.R.D.", "singer", "Band"), ("Nas", "singer", "Rapper"),
    ("Natasha_Bedingfield", "singer", "Singer"), ("Ne-Yo", "singer", "Singer"),
    ("Neil_Diamond", "singer", "Singer"), ("Nicki_Minaj", "singer", "Rapper"),
    ("Norah_Jones", "singer", "Singer"), ("NSYNC", "singer", "Band"),
    ("Olivia_Rodrigo", "singer", "Singer"), ("OneRepublic", "singer", "Band"),
    ("Outkast", "singer", "Band"), ("P!nk", "singer", "Singer"),
    ("Panic!_at_the_Disco", "singer", "Band"), ("Paramore", "singer", "Band"),
    ("Paul_McCartney", "singer", "Singer"), ("Pearl_Jam", "singer", "Band"),
    ("Pharrell_Williams", "singer", "Singer"), ("Phil_Collins", "singer", "Singer"),
    ("Pitbull_(rapper)", "singer", "Rapper"), ("Playboi_Carti", "singer", "Rapper"),
    ("Poppy_(singer)", "singer", "Singer"), ("Post_Malone", "singer", "Rapper"),
    ("Prince_(musician)", "singer", "Singer"), ("Queen_Latifah", "singer", "Rapper"),
    ("R._Kelly", "singer", "Singer"), ("Rachel_Platten", "singer", "Singer"),
    ("Rage_Against_the_Machine", "singer", "Band"), ("Ray_Charles", "singer", "Singer"),
    ("Reba_McEntire", "singer", "Singer"), ("Red_Hot_Chili_Peppers", "singer", "Band"),
    ("Rihanna", "singer", "Singer"), ("Rita_Ora", "singer", "Singer"),
    ("Robyn", "singer", "Singer"), ("Rosalía", "singer", "Singer"),
    ("Sade_(singer)", "singer", "Singer"), ("Santana_(band)", "singer", "Band"),
    ("Selena_Gomez", "singer", "Singer"), ("Sia", "singer", "Singer"),
    ("Simon_&_Garfunkel", "singer", "Band"), ("Snoop_Dogg", "singer", "Rapper"),
    ("Soulja_Boy", "singer", "Rapper"), ("Stevie_Wonder", "singer", "Singer"),
    ("Sting_(musician)", "singer", "Singer"), ("SZA", "singer", "Singer"),
    ("T-Pain", "singer", "Rapper"), ("Taylor_Swift", "singer", "Singer"),
    ("The_Beatles", "singer", "Band"), ("The_Cure", "singer", "Band"),
    ("The_Eagles_(band)", "singer", "Band"), ("The_Killers_(band)", "singer", "Band"),
    ("The_Notorious_B.I.G.", "singer", "Rapper"), ("The_Offspring", "singer", "Band"),
    ("The_Rolling_Stones", "singer", "Band"), ("The_Smiths", "singer", "Band"),
    ("The_Weeknd", "singer", "Singer"), ("Tiesto", "singer", "DJ"),
    ("Tiffany_(American_singer)", "singer", "Singer"), ("Timbaland", "singer", "Producer"),
    ("TLC_(group)", "singer", "Band"), ("Tom_Petty", "singer", "Singer"),
    ("Toni_Braxton", "singer", "Singer"), ("Tony_Bennett", "singer", "Singer"),
    ("Travis_Scott", "singer", "Rapper"), ("Trent_Reznor", "singer", "Singer"),
    ("Tupac_Shakur", "singer", "Rapper"), ("Twenty_One_Pilots", "singer", "Band"),
    ("Tyler,_the_Creator", "singer", "Rapper"), ("Usher_(musician)", "singer", "Singer"),
    ("Vanilla_Ice", "singer", "Rapper"), ("Weezer", "singer", "Band"),
    ("Whitney_Houston", "singer", "Singer"), ("Will_i_Am", "singer", "Rapper"),
    ("Willie_Nelson", "singer", "Singer"), ("Wiz_Khalifa", "singer", "Rapper"),
    ("Wyclef_Jean", "singer", "Singer"), ("Xzibit", "singer", "Rapper"),
    ("Yoko_Ono", "singer", "Artist"), ("Young_Thug", "singer", "Rapper"),
    ("Yung_Lean", "singer", "Rapper"), ("Zac_Brown_Band", "singer", "Band"),

    # === USA ACTORS - MORE (400) ===
    ("Adam_Sandler", "actor", "Actor"), ("Adrien_Brody", "actor", "Actor"),
    ("Alan_Arkin", "actor", "Actor"), ("Albert_Brooks", "actor", "Actor"),
    ("Alec_Baldwin", "actor", "Actor"), ("Amy_Adams", "actor", "Actress"),
    ("Amy_Poehler", "actor", "Actress"), ("Andie_MacDowell", "actor", "Actress"),
    ("Andy_García", "actor", "Actor"), ("Andy_Samberg", "actor", "Actor"),
    ("Anna_Faris", "actor", "Actress"), ("Anna_Kendrick", "actor", "Actress"),
    ("Anne_Hathaway", "actor", "Actress"), ("Annette_Bening", "actor", "Actress"),
    ("Anthony_Hopkins", "actor", "Actor"), ("Anthony_Mackie", "actor", "Actor"),
    ("Arnold_Schwarzenegger", "actor", "Actor"), ("Aubrey_Plaza", "actor", "Actress"),
    ("Awkwafina", "actor", "Actress"), ("Ben_Stiller", "actor", "Actor"),
    ("Benedict_Cumberbatch", "actor", "Actor"), ("Bette_Midler", "actor", "Actress"),
    ("Betty_White", "actor", "Actress"), ("Bill_Murray", "actor", "Actor"),
    ("Bill_Nighy", "actor", "Actor"), ("Billy_Bob_Thornton", "actor", "Actor"),
    ("Billy_Crystal", "actor", "Actor"), ("Blake_Lively", "actor", "Actress"),
    ("Bob_Odenkirk", "actor", "Actor"), ("Brendan_Fraser", "actor", "Actor"),
    ("Brie_Larson", "actor", "Actress"), ("Bruce_Willis", "actor", "Actor"),
    ("Bryan_Cranston", "actor", "Actor"), ("Cameron_Diaz", "actor", "Actress"),
    ("Carrie_Fisher", "actor", "Actress"), ("Casey_Affleck", "actor", "Actor"),
    ("Cate_Blanchett", "actor", "Actress"), ("Catherine_Zeta-Jones", "actor", "Actress"),
    ("Chadwick_Boseman", "actor", "Actor"), ("Channing_Tatum", "actor", "Actor"),
    ("Charles_Dance", "actor", "Actor"), ("Charlie_Sheen", "actor", "Actor"),
    ("Chloë_Grace_Moretz", "actor", "Actress"), ("Chris_Evans_(actor)", "actor", "Actor"),
    ("Chris_Hemsworth", "actor", "Actor"), ("Chris_Pratt", "actor", "Actor"),
    ("Chris_Rock", "actor", "Actor"), ("Christian_Bale", "actor", "Actor"),
    ("Christoph_Waltz", "actor", "Actor"), ("Cillian_Murphy", "actor", "Actor"),
    ("Claire_Danes", "actor", "Actress"), ("Clint_Eastwood", "actor", "Actor"),
    ("Colin_Farrell", "actor", "Actor"), ("Colin_Firth", "actor", "Actor"),
    ("Connie_Britton", "actor", "Actress"), ("Courteney_Cox", "actor", "Actress"),
    ("Craig_Robinson_(actor)", "actor", "Actor"), ("Dakota_Fanning", "actor", "Actress"),
    ("Dakota_Johnson", "actor", "Actress"), ("Dame_Judi_Dench", "actor", "Actress"),
    ("Daniel_Craig", "actor", "Actor"), ("Daniel_Kaluuya", "actor", "Actor"),
    ("Daniel_Radcliffe", "actor", "Actor"), ("Danny_DeVito", "actor", "Actor"),
    ("Danny_McBride", "actor", "Actor"), ("Danny_Trejo", "actor", "Actor"),
    ("Dave_Bautista", "actor", "Actor"), ("David_Harbour", "actor", "Actor"),
    ("David_Schwimmer", "actor", "Actor"), ("David_Tennant", "actor", "Actor"),
    ("Denzel_Washington", "actor", "Actor"), ("Diane_Keaton", "actor", "Actress"),
    ("Dianne_Wiest", "actor", "Actress"), ("Dolly_Parton", "singer", "Singer"),
    ("Don_Cheadle", "actor", "Actor"), ("Don_Johnson", "actor", "Actor"),
    ("Donald_Glover", "actor", "Actor"), ("Drew_Barrymore", "actor", "Actress"),
    ("Dwayne_Johnson", "actor", "Actor"), ("Dylan_McDermott", "actor", "Actor"),
    ("Ed_Helms", "actor", "Actor"), ("Eddie_Murphy", "actor", "Actor"),
    ("Eddie_Redmayne", "actor", "Actor"), ("Eiza_González", "actor", "Actress"),
    ("Elijah_Wood", "actor", "Actor"), ("Elisabeth_Moss", "actor", "Actress"),
    ("Elizabeth_Olsen", "actor", "Actress"), ("Ellen_Burstyn", "actor", "Actress"),
    ("Emily_Blunt", "actor", "Actress"), ("Emma_Roberts", "actor", "Actress"),
    ("Emma_Stone", "actor", "Actress"), ("Emma_Thompson", "actor", "Actress"),
    ("Eric_Bana", "actor", "Actor"), ("Ethan_Hawke", "actor", "Actor"),
    ("Eva_Mendes", "actor", "Actress"), ("Ewan_McGregor", "actor", "Actor"),
    ("Famke_Janssen", "actor", "Actress"), ("Florence_Pugh", "actor", "Actress"),
    ("Forest_Whitaker", "actor", "Actor"), ("Fran_Drescher", "actor", "Actress"),
    ("Frances_McDormand", "actor", "Actress"), ("Freida_Pinto", "actor", "Actress"),
    ("Gabriel_Macht", "actor", "Actor"), ("Gal_Gadot", "actor", "Actress"),
    ("Geena_Davis", "actor", "Actress"), ("Gene_Hackman", "actor", "Actor"),
    ("Geoffrey_Rush", "actor", "Actor"), ("George_Clooney", "actor", "Actor"),
    ("George_Lopez", "actor", "Actor"), ("Gerard_Butler", "actor", "Actor"),
    ("Gillian_Anderson", "actor", "Actress"), ("Gina_Rodriguez", "actor", "Actress"),
    ("Glenn_Close", "actor", "Actress"), ("Goldie_Hawn", "actor", "Actress"),
    ("Gong_Li", "actor", "Actress"), ("Gwyneth_Paltrow", "actor", "Actress"),
    ("Halle_Berry", "actor", "Actress"), ("Hank_Azaria", "actor", "Actor"),
    ("Harrison_Ford", "actor", "Actor"), ("Harvey_Keitel", "actor", "Actor"),
    ("Heath_Ledger", "actor", "Actor"), ("Helen_Hunt", "actor", "Actress"),
    ("Helen_Mirren", "actor", "Actress"), ("Henry_Cavill", "actor", "Actor"),
    ("Hilary_Duff", "actor", "Actress"), ("Hilary_Swank", "actor", "Actress"),
    ("Holly_Hunter", "actor", "Actress"), ("Hugh_Jackman", "actor", "Actor"),
    ("Ian_McKellen", "actor", "Actor"), ("Ice_Cube", "actor", "Actor"),
    ("Idina_Menzel", "actor", "Actress"), ("Idris_Elba", "actor", "Actor"),
    ("Imelda_Staunton", "actor", "Actress"), ("Isla_Fisher", "actor", "Actress"),
    ("J._K._Simmons", "actor", "Actor"), ("Jack_Black", "actor", "Actor"),
    ("Jack_Nicholson", "actor", "Actor"), ("Jackie_Chan", "actor", "Actor"),
    ("Jada_Pinkett_Smith", "actor", "Actress"), ("Jamie_Foxx", "actor", "Actor"),
    ("Jamie_Lee_Curtis", "actor", "Actress"), ("Jane_Fonda", "actor", "Actress"),
    ("Jason_Bateman", "actor", "Actor"), ("Jason_Statham", "actor", "Actor"),
    ("Jason_Sudeikis", "actor", "Actor"), ("Javier_Bardem", "actor", "Actor"),
    ("Jeff_Bridges", "actor", "Actor"), ("Jeff_Goldblum", "actor", "Actor"),
    ("Jennifer_Aniston", "actor", "Actress"), ("Jennifer_Connelly", "actor", "Actress"),
    ("Jennifer_Garner", "actor", "Actress"), ("Jennifer_Lawrence", "actor", "Actress"),
    ("Jennifer_Lopez", "actor", "Actress"), ("Jennifer_Saunders", "actor", "Actress"),
    ("Jessica_Alba", "actor", "Actress"), ("Jessica_Chastain", "actor", "Actress"),
    ("Jessica_Lange", "actor", "Actress"), ("Jim_Carrey", "actor", "Actor"),
    ("Jim_Parsons", "actor", "Actor"), ("Joaquin_Phoenix", "actor", "Actor"),
    ("Jodie_Foster", "actor", "Actress"), ("Jodie_Comer", "actor", "Actress"),
    ("Joe_Pesci", "actor", "Actor"), ("John_Boyega", "actor", "Actor"),
    ("John_C._Reilly", "actor", "Actor"), ("John_Cena", "actor", "Actor"),
    ("John_Goodman", "actor", "Actor"), ("John_Krasinski", "actor", "Actor"),
    ("John_Malkovich", "actor", "Actor"), ("John_Travolta", "actor", "Actor"),
    ("Johnny_Depp", "actor", "Actor"), ("Jonah_Hill", "actor", "Actor"),
    ("Jonathan_Groff", "actor", "Actor"), ("Joseph_Gordon-Levitt", "actor", "Actor"),
    ("Josh_Brolin", "actor", "Actor"), ("Josh_Hutcherson", "actor", "Actor"),
    ("Jude_Law", "actor", "Actor"), ("Julia_Louis-Dreyfus", "actor", "Actress"),
    ("Julia_Roberts", "actor", "Actress"), ("Julianne_Moore", "actor", "Actress"),
    ("Julie_Andrews", "actor", "Actress"), ("Kaitlin_Olson", "actor", "Actress"),
    ("Kaley_Cuoco", "actor", "Actress"), ("Kate_Beckinsale", "actor", "Actress"),
    ("Kate_Hudson", "actor", "Actress"), ("Kate_Mara", "actor", "Actress"),
    ("Kate_Upton", "actor", "Actress"), ("Kate_Winslet", "actor", "Actress"),
    ("Katharine_Hepburn", "actor", "Actress"), ("Katherine_Heigl", "actor", "Actress"),
    ("Kathryn_Bigelow", "actor", "Actress"), ("Kathy_Bates", "actor", "Actress"),
    ("Katie_Holmes", "actor", "Actress"), ("Keanu_Reeves", "actor", "Actor"),
    ("Keira_Knightley", "actor", "Actress"), ("Kelly_Macdonald", "actor", "Actress"),
    ("Ken_Watanabe", "actor", "Actor"), ("Kevin_Bacon", "actor", "Actor"),
    ("Kevin_Costner", "actor", "Actor"), ("Kevin_Hart", "actor", "Actor"),
    ("Kevin_Kline", "actor", "Actor"), ("Kevin_McNally", "actor", "Actor"),
    ("Kirsten_Dunst", "actor", "Actress"), ("Kristen_Bell", "actor", "Actress"),
    ("Kristen_Stewart", "actor", "Actress"), ("Kristen_Wiig", "actor", "Actress"),
    ("Krysten_Ritter", "actor", "Actress"), ("Kurt_Russell", "actor", "Actor"),
    ("Kyle_MacLachlan", "actor", "Actor"), ("Larry_David", "actor", "Actor"),
    ("Laura_Dern", "actor", "Actress"), ("Laura_Linney", "actor", "Actress"),
    ("Lauren_Graham", "actor", "Actress"), ("Laurence_Fishburne", "actor", "Actor"),
    ("Lea_Michele", "actor", "Actress"), ("Lena_Headey", "actor", "Actress"),
    ("Leonardo_DiCaprio", "actor", "Actor"), ("Leslie_Jones_(comedian)", "actor", "Actress"),
    ("Liam_Neeson", "actor", "Actor"), ("Liev_Schreiber", "actor", "Actor"),
    ("Lily_James", "actor", "Actress"), ("Lily_Tomlin", "actor", "Actress"),
    ("Lindsay_Lohan", "actor", "Actress"), ("Lisa_Kudrow", "actor", "Actress"),
    ("Logan_Lerman", "actor", "Actor"), ("Lupita_Nyong'o", "actor", "Actress"),
    ("Macaulay_Culkin", "actor", "Actor"), ("Maggie_Gyllenhaal", "actor", "Actress"),
    ("Maggie_Smith", "actor", "Actress"), ("Mahershala_Ali", "actor", "Actor"),
    ("Maisie_Williams", "actor", "Actress"), ("Mandy_Moore", "actor", "Actress"),
    ("Marcia_Cross", "actor", "Actress"), ("Marion_Cotillard", "actor", "Actress"),
    ("Marisa_Tomei", "actor", "Actress"), ("Mark_Hamill", "actor", "Actor"),
    ("Mark_Ruffalo", "actor", "Actor"), ("Mark_Wahlberg", "actor", "Actor"),
    ("Marlon_Brando", "actor", "Actor"), ("Martin_Freeman", "actor", "Actor"),
    ("Martin_Sheen", "actor", "Actor"), ("Mary-Kate_Olsen", "actor", "Actress"),
    ("Mary_Steenburgen", "actor", "Actress"), ("Matt_Damon", "actor", "Actor"),
    ("Matt_LeBlanc", "actor", "Actor"), ("Matthew_McConaughey", "actor", "Actor"),
    ("Matthew_Perry", "actor", "Actor"), ("Meg_Ryan", "actor", "Actress"),
    ("Megan_Fox", "actor", "Actress"), ("Mel_Brooks", "actor", "Actor"),
    ("Mel_Gibson", "actor", "Actor"), ("Melissa_McCarthy", "actor", "Actress"),
    ("Meryl_Streep", "actor", "Actress"), ("Michael_Cera", "actor", "Actor"),
    ("Michael_Douglas", "actor", "Actor"), ("Michael_Fassbender", "actor", "Actor"),
    ("Michael_Imperioli", "actor", "Actor"), ("Michael_J._Fox", "actor", "Actor"),
    ("Michael_Keaton", "actor", "Actor"), ("Michael_Peña", "actor", "Actor"),
    ("Michelle_Pfeiffer", "actor", "Actress"), ("Michelle_Rodriguez", "actor", "Actress"),
    ("Michelle_Williams_(actress)", "actor", "Actress"), ("Michelle_Yeoh", "actor", "Actress"),
    ("Mila_Kunis", "actor", "Actress"), ("Miley_Cyrus", "actor", "Actress"),
    ("Milla_Jovovich", "actor", "Actress"), ("Mindy_Kaling", "actor", "Actress"),
    ("Mira_Sorvino", "actor", "Actress"), ("Miranda_Cosgrove", "actor", "Actress"),
    ("Mischa_Barton", "actor", "Actress"), ("Mohanlal", "actor", "Actor"),
    ("Molly_Ringwald", "actor", "Actress"), ("Mona_Lisa_(actress)", "actor", "Actress"),
    ("Morgan_Freeman", "actor", "Actor"), ("Moses_Ingram", "actor", "Actress"),
    ("Naomie_Harris", "actor", "Actress"), ("Naomi_Watts", "actor", "Actress"),
    ("Natalie_Portman", "actor", "Actress"), ("Natalie_Dormer", "actor", "Actress"),
    ("Neil_Patrick_Harris", "actor", "Actor"), ("Nia_Long", "actor", "Actress"),
    ("Nicholas_Cage", "actor", "Actor"), ("Nick_Nolte", "actor", "Actor"),
    ("Nicole_Kidman", "actor", "Actress"), ("Nicolas_Cage", "actor", "Actor"),
    ("Noah_Schnapp", "actor", "Actor"), ("Octavia_Spencer", "actor", "Actress"),
    ("Oliver_Platt", "actor", "Actor"), ("Olivia_Munn", "actor", "Actress"),
    ("Olivia_Wilde", "actor", "Actress"), ("Oprah_Winfrey", "actor", "Actress"),
    ("Orlando_Bloom", "actor", "Actor"), ("Oscar_Isaac", "actor", "Actor"),
    ("Owen_Wilson", "actor", "Actor"), ("Pamela_Anderson", "actor", "Actress"),
    ("Patricia_Arquette", "actor", "Actress"), ("Patrick_Dempsey", "actor", "Actor"),
    ("Patrick_Stewart", "actor", "Actor"), ("Patton_Oswalt", "actor", "Actor"),
    ("Paul_Bettany", "actor", "Actor"), ("Paul_Giamatti", "actor", "Actor"),
    ("Paul_Rudd", "actor", "Actor"), ("Penélope_Cruz", "actor", "Actress"),
    ("Peter_Dinklage", "actor", "Actor"), ("Philip_Seymour_Hoffman", "actor", "Actor"),
    ("Piper_Perabo", "actor", "Actress"), ("Queen_Latifah", "actor", "Actress"),
    ("Rachel_Bilson", "actor", "Actress"), ("Rachel_McAdams", "actor", "Actress"),
    ("Rachel_Weisz", "actor", "Actress"), ("Rami_Malek", "actor", "Actor"),
    ("Rashida_Jones", "actor", "Actress"), ("Rebecca_Ferguson", "actor", "Actress"),
    ("Reese_Witherspoon", "actor", "Actress"), ("Reneé_Zellweger", "actor", "Actress"),
    ("Rhys_Ifans", "actor", "Actor"), ("Richard_Gere", "actor", "Actor"),
    ("Ridley_Scott", "director", "Director"), ("Rita_Wilson", "actor", "Actress"),
    ("Rob_Lowe", "actor", "Actor"), ("Robert_De_Niro", "actor", "Actor"),
    ("Robert_Downey_Jr.", "actor", "Actor"), ("Robert_Duvall", "actor", "Actor"),
    ("Robert_Pattinson", "actor", "Actor"), ("Robert_Redford", "actor", "Actor"),
    ("Robin_Williams", "actor", "Actor"), ("Robin_Wright", "actor", "Actress"),
    ("Roma_Downey", "actor", "Actress"), ("Ron_Howard", "actor", "Actor"),
    ("Ron_Perlman", "actor", "Actor"), ("Rooney_Mara", "actor", "Actress"),
    ("Rose_McGowan", "actor", "Actress"), ("Rosie_O'Donnell", "actor", "Actress"),
    ("Rowan_Atkinson", "actor", "Actor"), ("Rupert_Friend", "actor", "Actor"),
    ("Rupert_Grint", "actor", "Actor"), ("Russell_Crowe", "actor", "Actor"),
    ("Ruth_Wilson", "actor", "Actress"), ("Ryan_Reynolds", "actor", "Actor"),
    ("Ryan_Gosling", "actor", "Actor"), ("Sacha_Baron_Cohen", "actor", "Actor"),
    ("Sally_Field", "actor", "Actress"), ("Salma_Hayek", "actor", "Actress"),
    ("Sam_Elliott", "actor", "Actor"), ("Sam_Rockwell", "actor", "Actor"),
    ("Sam_Worthington", "actor", "Actor"), ("Samuel_L._Jackson", "actor", "Actor"),
    ("Sandra_Bullock", "actor", "Actress"), ("Saoirse_Ronan", "actor", "Actress"),
    ("Sarah_Jessica_Parker", "actor", "Actress"), ("Sarah_Michelle_Gellar", "actor", "Actress"),
    ("Sarah_Paulson", "actor", "Actress"), ("Sasha_Alexander", "actor", "Actress"),
    ("Scarlett_Johansson", "actor", "Actress"), ("Sean_Connery", "actor", "Actor"),
    ("Sean_Penn", "actor", "Actor"), ("Sebastian_Stan", "actor", "Actor"),
    ("Selena_Gomez", "actor", "Actress"), ("Seth_MacFarlane", "actor", "Actor"),
    ("Seth_Rogen", "actor", "Actor"), ("Shailene_Woodley", "actor", "Actress"),
    ("Shannen_Doherty", "actor", "Actress"), ("Sharon_Stone", "actor", "Actress"),
    ("Shawn_Mendes", "singer", "Singer"), ("Shia_LaBeouf", "actor", "Actor"),
    ("Shirley_MacLaine", "actor", "Actress"), ("Sienna_Miller", "actor", "Actress"),
    ("Sigourney_Weaver", "actor", "Actress"), ("Simon_Pegg", "actor", "Actor"),
    ("Sofia_Vergara", "actor", "Actress"), ("Sophia_Loren", "actor", "Actress"),
    ("Sophie_Turner_(actress)", "actor", "Actress"), ("Stacy_Keibler", "actor", "Actress"),
    ("Stanley_Tucci", "actor", "Actor"), ("Stephen_Fry", "actor", "Actor"),
    ("Steve_Buscemi", "actor", "Actor"), ("Steve_Carell", "actor", "Actor"),
    ("Steve_Martin", "actor", "Actor"), ("Steven_Seagal", "actor", "Actor"),
    ("Susan_Sarandon", "actor", "Actress"), ("Sylvester_Stallone", "actor", "Actor"),
    ("Taron_Egerton", "actor", "Actor"), ("Tatum_O'Neal", "actor", "Actress"),
    ["Tessa_Thompson", "actor", "Actress"], ("Thandiwe_Newton", "actor", "Actress"),
    ("Thomas_Haden_Church", "actor", "Actor"), ("Tilda_Swinton", "actor", "Actress"),
    ("Tim_Allen", "actor", "Actor"), ("Tim_Robbins", "actor", "Actor"),
    ("Timothée_Chalamet", "actor", "Actor"), ("Tina_Fey", "actor", "Actress"),
    ("Tom_Brady", "sports", "Football Player"), ("Tom_Cruise", "actor", "Actor"),
    ("Tom_Everett_Scott", "actor", "Actor"), ("Tom_Hanks", "actor", "Actor"),
    ("Tom_Hiddleston", "actor", "Actor"), ("Tom_Selleck", "actor", "Actor"),
    ("Tommy_Lee_Jones", "actor", "Actor"), ("Toni_Collette", "actor", "Actress"),
    ("Tracee_Ellis_Ross", "actor", "Actress"), ("Travis_Fimmel", "actor", "Actor"),
    ("Ty_Burrell", "actor", "Actor"), ("Tyler_Perry", "actor", "Actor"),
    ("Uma_Thurman", "actor", "Actress"), ("Val_Kilmer", "actor", "Actor"),
    ("Vanessa_Redgrave", "actor", "Actress"), ("Vera_Farmiga", "actor", "Actress"),
    ("Viggo_Mortensen", "actor", "Actor"), ("Vince_Vaughn", "actor", "Actor"),
    ("Viola_Davis", "actor", "Actress"), ("Whoopi_Goldberg", "actor", "Actress"),
    ("Willem_Dafoe", "actor", "Actor"), ("Will_Ferrell", "actor", "Actor"),
    ("Will_Smith", "actor", "Actor"), ("William_H._Macy", "actor", "Actor"),
    ("Winona_Ryder", "actor", "Actress"), ("Woody_Harrelson", "actor", "Actor"),
    ("Yalitza_Aparicio", "actor", "Actress"), ("Zach_Braff", "actor", "Actor"),
    ("Zach_Galifianakis", "actor", "Actor"), ("Zoe_Saldana", "actor", "Actress"),
    ("Zooey_Deschanel", "actor", "Actress"),

    # === MORE FOOTBALLERS (200) ===
    ("Alfredo_Di_Stéfano", "footballer", "Footballer"),
    ("Andrés_Iniesta", "footballer", "Footballer"),
    ("Antoine_Griezmann", "footballer", "Footballer"),
    ("Arjen_Robben", "footballer", "Footballer"),
    ("Bastian_Schweinsteiger", "footballer", "Footballer"),
    ("Cafu", "footballer", "Footballer"),
    ("Carlo_Ancelotti", "footballer", "Coach"),
    ("Casemiro", "footballer", "Footballer"),
    ("Cesc_Fàbregas", "footballer", "Footballer"),
    ("Claudio_Pizarro", "footballer", "Footballer"),
    ("David_Alaba", "footballer", "Footballer"),
    ("David_Villa", "footballer", "Footballer"),
    ("Deco", "footballer", "Footballer"),
    ("Diego_Costa", "footballer", "Footballer"),
    ("Diego_Maradona", "footballer", "Footballer"),
    ("Didier_Drogba", "footballer", "Footballer"),
    ("Eden_Hazard", "footballer", "Footballer"),
    ("Edinson_Cavani", "footballer", "Footballer"),
    ("Edwin_van_der_Sar", "footballer", "Footballer"),
    ("Emmanuel_Adebayor", "footballer", "Footballer"),
    ("Eric_Cantona", "footballer", "Footballer"),
    ("Eden_Hazard", "footballer", "Footballer"),
    ("Falcao_(footballer)", "footballer", "Footballer"),
    ("Francesco_Totti", "footballer", "Footballer"),
    ("Frank_Lampard", "footballer", "Footballer"),
    ("Franz_Beckenbauer", "footballer", "Footballer"),
    ("Fred_(footballer,_born_1993)", "footballer", "Footballer"),
    ("Gareth_Bale", "footballer", "Footballer"),
    ("Gennaro_Gattuso", "footballer", "Footballer"),
    ("Gianluigi_Buffon", "footballer", "Footballer"),
    ("Giorgio_Chiellini", "footballer", "Footballer"),
    ("Harry_Kane_(footballer)", "footballer", "Footballer"),
    ("Hernán_Crespo", "footballer", "Footballer"),
    ("Iker_Casillas", "footballer", "Footballer"),
    ("Ivan_Rakitić", "footballer", "Footballer"),
    ("Jadon_Sancho", "footballer", "Footballer"),
    ("Jamie_Vardy", "footballer", "Footballer"),
    ("Javier_Hernández_(footballer)", "footballer", "Footballer"),
    ("Johan_Cruyff", "footballer", "Footballer"),
    ("John_Terry", "footballer", "Footballer"),
    ("Joshua_Kimmich", "footballer", "Footballer"),
    ("Juan_Sebastián_Verón", "footballer", "Footballer"),
    ("Jürgen_Klopp", "footballer", "Coach"),
    ("Kaka_(footballer)", "footballer", "Footballer"),
    ("Kylian_Mbappé", "footballer", "Footballer"),
    ("Landon_Donovan", "footballer", "Footballer"),
    ("Laurent_Blanc", "footballer", "Footballer"),
    ("Leonardo_Bonucci", "footballer", "Footballer"),
    ("Luis_Suárez_(footballer,_born_1987)", "footballer", "Footballer"),
    ("Luis_Figo", "footballer", "Footballer"),
    ("Luka_Modrić", "footballer", "Footballer"),
    ("Manuel_Neuer", "footballer", "Footballer"),
    ("Marco_Reus", "footballer", "Footballer"),
    ("Marcelo_(footballer,_born_1988)", "footballer", "Footballer"),
    ("Mesut_Özil", "footballer", "Footballer"),
    ("Michael_Laudrup", "footballer", "Footballer"),
    ("Michael_Owen", "footballer", "Footballer"),
    ("Michel_Platini", "footballer", "Footballer"),
    ("N'Golo_Kanté", "footballer", "Footballer"),
    ("Paolo_Maldini", "footballer", "Footballer"),
    ("Papu_Gómez", "footballer", "Footballer"),
    ("Paul_Pogba", "footballer", "Footballer"),
    ("Paulo_Dybala", "footballer", "Footballer"),
    ("Pelé", "footballer", "Footballer"),
    ("Pep_Guardiola", "footballer", "Coach"),
    ("Peter_Schmeichel", "footballer", "Footballer"),
    ("Philipp_Lahm", "footballer", "Footballer"),
    ("Rivaldo", "footballer", "Footballer"),
    ("Roberto_Baggio", "footballer", "Footballer"),
    ("Roberto_Carlos", "footballer", "Footballer"),
    ("Robin_van_Persie", "footballer", "Footballer"),
    ("Ronaldinho", "footballer", "Footballer"),
    ("Ronaldo_(footballer)", "footballer", "Footballer"),
    ("Roy_Keane", "footballer", "Footballer"),
    ("Sergio_Aguëro", "footballer", "Footballer"),
    ("Steven_Gerrard", "footballer", "Footballer"),
    ("Thibaut_Courtois", "footballer", "Footballer"),
    ("Thierry_Henry", "footballer", "Footballer"),
    ("Thomas_Müller", "footballer", "Footballer"),
    ("Toni_Kroos", "footballer", "Footballer"),
    ("Virgil_van_Dijk", "footballer", "Footballer"),
    ("Wayne_Rooney", "footballer", "Footballer"),
    ("Xabi_Alonso", "footballer", "Footballer"),
    ("Xavi_(footballer,_born_1980)", "footballer", "Footballer"),
    ("Zlatan_Ibrahimović", "footballer", "Footballer"),
    ("Zinedine_Zidane", "footballer", "Footballer"),

    # === MORE POLITICIANS (100) ===
    ("Abraham_Lincoln", "politician", "Politician"),
    ("Adolf_Hitler", "politician", "Politician"),
    ("Al_Gore", "politician", "Politician"),
    ("Andrew_Jackson", "politician", "Politician"),
    ("Benjamin_Netanyahu", "politician", "Politician"),
    ("Boris_Johnson", "politician", "Politician"),
    ("Charles_de_Gaulle", "politician", "Politician"),
    ("Cristina_Fernández_de_Kirchner", "politician", "Politician"),
    ("Dilma_Rousseff", "politician", "Politician"),
    ("Evo_Morales", "politician", "Politician"),
    ("Fidel_Castro", "politician", "Politician"),
    ("Franklin_D._Roosevelt", "politician", "Politician"),
    ("George_W._Bush", "politician", "Politician"),
    ("Hillary_Clinton", "politician", "Politician"),
    ("Imran_Khan", "politician", "Politician"),
    ("Jacinda_Ardern", "politician", "Politician"),
    ("Jair_Bolsonaro", "politician", "Politician"),
    ("Jimmy_Carter", "politician", "Politician"),
    ("John_F._Kennedy", "politician", "Politician"),
    ("Juan_Manuel_Santos", "politician", "Politician"),
    ("Mahatma_Gandhi", "politician", "Politician"),
    ("Margaret_Thatcher", "politician", "Politician"),
    ("Mikhail_Gorbachev", "politician", "Politician"),
    ("Nelson_Mandela", "politician", "Politician"),
    ("Nicolás_Maduro", "politician", "Politician"),
    ("Rafael_Correa", "politician", "Politician"),
    ("Ronald_Reagan", "politician", "Politician"),
    ("Shinzō_Abe", "politician", "Politician"),
    ("Theresa_May", "politician", "Politician"),
    ("Tony_Blair", "politician", "Politician"),
    ("Winston_Churchill", "politician", "Politician"),
    ("Woodrow_Wilson", "politician", "Politician"),

    # === SPORTS (100 more) ===
    ("Michael_Jordan", "basketball", "Basketball Player"),
    ("Kobe_Bryant", "basketball", "Basketball Player"),
    ("Magic_Johnson", "basketball", "Basketball Player"),
    ("Larry_Bird", "basketball", "Basketball Player"),
    ("Shaquille_O'Neal", "basketball", "Basketball Player"),
    ("Kareem_Abdul-Jabbar", "basketball", "Basketball Player"),
    ("Tim_Duncan", "basketball", "Basketball Player"),
    ("Bill_Russell", "basketball", "Basketball Player"),
    ("Wilt_Chamberlain", "basketball", "Basketball Player"),
    ("Hakeem_Olajuwon", "basketball", "Basketball Player"),
    ("Muhammad_Ali", "boxer", "Boxer"),
    ("George_Foreman", "boxer", "Boxer"),
    ("Tyson_Fury", "boxer", "Boxer"),
    ("Deontay_Wilder", "boxer", "Boxer"),
    ("Andy_Ruiz_Jr.", "boxer", "Boxer"),
    ("Serena_Williams", "tennis", "Tennis Player"),
    ("Venus_Williams", "tennis", "Tennis Player"),
    ("Roger_Federer", "tennis", "Tennis Player"),
    ("Rafael_Nadal", "tennis", "Tennis Player"),
    ("Novak_Djokovic", "tennis", "Tennis Player"),
    ("Andre_Agassi", "tennis", "Tennis Player"),
    ("Pete_Sampras", "tennis", "Tennis Player"),
    ("Usain_Bolt", "sports", "Athlete"),
    ("Carl_Lewis", "sports", "Athlete"),
    ("Michael_Phelps", "sports", "Swimmer"),
    ("Mark_Spitz", "sports", "Swimmer"),
    ("Simone_Biles", "sports", "Gymnast"),
    ("Nadia_Comăneci", "sports", "Gymnast"),
    ("Ayrton_Senna", "sports", "Racing Driver"),
    ("Michael_Schumacher", "sports", "Racing Driver"),
    ("Lewis_Hamilton", "sports", "Racing Driver"),
    ("Dale_Earnhardt", "sports", "Racing Driver"),
    ("Tony_Hawk", "sports", "Skateboarder"),
    ("Kelly_Slater", "sports", "Surfer"),

    # === MORE COLOMBIAN / LATIN AMERICA (150) ===
    ("Shakira", "singer", "Singer"),
    ("Juanes", "singer", "Singer"),
    ("Carlos_Vives", "singer", "Singer"),
    ("Maluma", "singer", "Singer"),
    ("Karol_G", "singer", "Singer"),
    ("J_Balvin", "singer", "Singer"),
    ("Sebastián_Yatra", "singer", "Singer"),
    ("Manuel_Turizo", "singer", "Singer"),
    ("Camilo_(singer)", "singer", "Singer"),
    ("Greeicy", "singer", "Singer"),
    ("Fonseca_(singer)", "singer", "Singer"),
    ("Silvestre_Dangond", "singer", "Singer"),
    ("Diomedes_Díaz", "singer", "Singer"),
    ("Joe_Arroyo", "singer", "Singer"),
    ("Andrés_Cepeda", "singer", "Singer"),
    ("Jessi_Uribe", "singer", "Singer"),
    ("Paola_Jara", "singer", "Singer"),
    ("Yeison_Jiménez", "singer", "Singer"),
    ("Pipe_Bueno", "singer", "Singer"),
    ("Grupo_Firme", "singer", "Band"),
    ("Bad_Bunny", "singer", "Singer"),
    ("Ozuna", "singer", "Singer"),
    ("Anuel_AA", "singer", "Rapper"),
    ("Daddy_Yankee", "singer", "Singer"),
    ("Luis_Fonsi", "singer", "Singer"),
    ("Nicky_Jam", "singer", "Singer"),
    ("Enrique_Iglesias", "singer", "Singer"),
    ("Ricky_Martin", "singer", "Singer"),
    ("Marc_Anthony", "singer", "Singer"),
    ("Romeo_Santos", "singer", "Singer"),
    ("Becky_G", "singer", "Singer"),
    ("Natti_Natasha", "singer", "Singer"),
    ("Gloria_Trevi", "singer", "Singer"),
    ("Luis_Miguel", "singer", "Singer"),
    ("Alejandro_Fernández", "singer", "Singer"),
    ("Vicente_Fernández", "singer", "Singer"),
    ("Ana_Sofía_Sánchez", "actor", "Actress"),
    ("Sofía_Vergara", "actor", "Actress"),
    ("Kate_del_Castillo", "actor", "Actress"),
    ("Fernando_Colunga", "actor", "Actor"),
    ("Manolo_Cardona", "actor", "Actor"),
    ("Mario_López", "actor", "Actor"),
    ("Luis_Alberto_Posada", "baseball", "Baseball"),
    ("Edgar_Rentería", "baseball", "Baseball"),
    ("Gustavo_Petro", "politician", "Politician"),
    ("Álvaro_Uribe", "politician", "Politician"),
    ("Iván_Duque", "politician", "Politician"),
    ("Juan_Manuel_Santos", "politician", "Politician"),
    ("Nairo_Quintana", "cyclist", "Cyclist"),
    ("Rigoberto_Urán", "cyclist", "Cyclist"),
    ("Egan_Bernal", "cyclist", "Cyclist"),
    ("Mariana_Pajón", "cyclist", "Cyclist"),
    ("Caterine_Ibargüen", "sports", "Athlete"),
    ("Gabriel_García_Márquez", "writer", "Writer"),
    ("Fernando_Botero", "artist", "Artist"),
    ("Álex_Lora", "singer", "Singer"),
    ("Thalía", "singer", "Singer"),
    ("Paulina_Rubio", "singer", "Singer"),
    ("Alejandra_Guzmán", "singer", "Singer"),
    ("Chayanne", "singer", "Singer"),
    ("Juan_Gabriel", "singer", "Singer"),
    ("Luis_Miguel", "singer", "Singer"),
    ("Celia_Cruz", "singer", "Singer"),
    ("Héctor_Lavoe", "singer", "Singer"),
    ("Willie_Colón", "singer", "Singer"),
    ("Rubén_Blades", "singer", "Singer"),
    ("Carlos_Santana", "singer", "Singer"),

    # === EUROPEAN ACTORS - ADDITIONAL (100) ===
    ("Mads_Mikkelsen", "actor", "Actor"),
    ("Lars_von_Trier", "director", "Director"),
    ("Jean_Dujardin", "actor", "Actor"),
    ("Marion_Cotillard", "actor", "Actress"),
    ("Audrey_Tautou", "actor", "Actress"),
    ("Vincent_Cassel", "actor", "Actor"),
    ("Claudia_Cardinale", "actor", "Actress"),
    ("Sophia_Loren", "actor", "Actress"),
    ("Marcello_Mastroianni", "actor", "Actor"),
    ("Roberto_Benigni", "actor", "Actor"),
    ("Toni_Servillo", "actor", "Actor"),
    ("Daniel_Brühl", "actor", "Actor"),
    ("Diane_Kruger", "actor", "Actress"),
    ("Antonio_Banderas", "actor", "Actor"),
    ("Javier_Bardem", "actor", "Actor"),
    ("Penélope_Cruz", "actor", "Actress"),
    ("Carmen_Maura", "actor", "Actress"),
    ("Antonio_Resines", "actor", "Actor"),
    ("Victoria_Abril", "actor", "Actress"),

    # === INFLUENCERS / YOUTUBE (80) ===
    ("MrBeast", "influencer", "Content Creator"),
    ("PewDiePie", "influencer", "Content Creator"),
    ("Markiplier", "influencer", "Content Creator"),
    ("Jacksepticeye", "influencer", "Content Creator"),
    ("DanTDM", "influencer", "Content Creator"),
    ("SSSniperWolf", "influencer", "Content Creator"),
    ("VanossGaming", "influencer", "Content Creator"),
    ("LDShadowLady", "influencer", "Content Creator"),
    ("PopularMMOs", "influencer", "Content Creator"),
    ("Nigahiga", "influencer", "Content Creator"),
    ("Smosh", "influencer", "Group"),
    ("Rhett_&_Link", "influencer", "Duo"),
    ("Philip_DeFranco", "influencer", "Content Creator"),
    ("Casey_Neistat", "influencer", "Content Creator"),
    ("Peter_McKinnon", "influencer", "Content Creator"),
    ("MKBHD", "influencer", "Tech Reviewer"),
    ("Linus_Tech_Tips", "influencer", "Tech Reviewer"),
    ("David_Dobrik", "influencer", "Content Creator"),
    ("Liza_Koshy", "influencer", "Content Creator"),
    ("Emma_Chamberlain", "influencer", "Content Creator"),
    ("James_Charles", "influencer", "Makeup Artist"),
    ("Jeffree_Star", "influencer", "Makeup Artist"),
    ("NikkieTutorials", "influencer", "Makeup Artist"),
    ("Charli_D'Amelio", "influencer", "Content Creator"),
    ("Addison_Rae", "influencer", "Content Creator"),
    ("Bella_Poarch", "influencer", "Content Creator"),
    ("Dixie_D'Amelio", "influencer", "Content Creator"),
    ("Avani_Gregg", "influencer", "Content Creator"),
    ("Josh_Richards", "influencer", "Content Creator"),
    ("Kylie_Jenner", "influencer", "Businesswoman"),
    ("Kim_Kardashian", "influencer", "Businesswoman"),
    ("Kendall_Jenner", "influencer", "Model"),
    ("Khloé_Kardashian", "influencer", "Businesswoman"),
    ("Kourtney_Kardashian", "influencer", "Businesswoman"),
    ("Kris_Jenner", "influencer", "Manager"),
    ("Chiara_Ferragni", "influencer", "Fashion Blogger"),
    ("Lele_Pons", "influencer", "Content Creator"),
    ("Juanpa_Zurita", "influencer", "Content Creator"),
    ("Luisito_Comunica", "influencer", "Content Creator"),
    ("Germán_Garmendia", "influencer", "Content Creator"),
]

# Remove duplicates and existing
seen_titles = set()
filtered = []
for title, cat, prof in FIGURES:
    if title not in seen_titles:
        seen_titles.add(title)
        filtered.append((title, cat, prof))

FIGURES = filtered

print(f"Total in list: {len(FIGURES)}")

new_count = 0
skip_count = 0

for wiki_title, category, profession in FIGURES:
    title_clean = wiki_title.replace('_', ' ')
    slug = make_slug(title_clean)
    
    if slug in EXISTING:
        skip_count += 1
        continue
    
    meta_desc = f"{title_clean} is a notable {profession.lower()}."
    js_desc = html_mod.escape(meta_desc)
    html_desc = html_mod.escape(meta_desc)
    
    html = TEMPLATE.format(
        title=title_clean, slug=slug,
        cat_display=profession,
        meta_desc=meta_desc, js_desc=js_desc,
        html_desc=html_desc, profession=profession.lower(),
        wiki_title=wiki_title
    )
    
    fp = os.path.join(BIOS_DIR, f'{slug}.html')
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(html)
    new_count += 1
    EXISTING.add(slug)

print(f'New bios generated: {new_count}')
print(f'Skipped (already existing): {skip_count}')
print(f'Total bios now: {len(EXISTING)}')
