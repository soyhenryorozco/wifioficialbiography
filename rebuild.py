#!/usr/bin/env python3
"""
Rebuild index.html, app.js, sitemap.xml, industry pages from all bio HTML files.
Parses existing bios to extract metadata and regenerates all files.
Deduplicates bios with same name (keeps larger file).
"""

import os, re, glob, html, datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BIOS_DIR = os.path.join(BASE_DIR, 'bios')
INDEX_FILE = os.path.join(BASE_DIR, 'index.html')
APPJS_FILE = os.path.join(BASE_DIR, 'js', 'app.js')
SITEMAP_FILE = os.path.join(BASE_DIR, 'sitemap.xml')
DOMAIN = 'https://wifioficialbiography.org'

CATEGORY_META = {
    'singer': {'icon': '🎵', 'label': 'Cantantes', 'industry_label': 'Cantantes y Músicos', 'industry_desc': 'Cantantes, músicos y artistas musicales de todos los géneros.'},
    'actor': {'icon': '🎬', 'label': 'Actores y Actrices', 'industry_label': 'Actores y Actrices', 'industry_desc': 'Actores y actrices de cine, televisión y teatro.'},
    'footballer': {'icon': '⚽', 'label': 'Futbolistas', 'industry_label': 'Futbolistas', 'industry_desc': 'Futbolistas profesionales de ligas nacionales e internacionales.'},
    'politician': {'icon': '🏛️', 'label': 'Políticos', 'industry_label': 'Políticos y Líderes', 'industry_desc': 'Políticos, gobernantes y líderes de opinión.'},
    'writer': {'icon': '✍️', 'label': 'Escritores', 'industry_label': 'Escritores y Poetas', 'industry_desc': 'Escritores, poetas, novelistas y periodistas.'},
    'model': {'icon': '👗', 'label': 'Modelos', 'industry_label': 'Modelos y Fashion', 'industry_desc': 'Modelos, diseñadores y figuras de la moda.'},
    'cyclist': {'icon': '🚴', 'label': 'Ciclistas', 'industry_label': 'Ciclistas', 'industry_desc': 'Ciclistas profesionales de ruta, pista y montaña.'},
    'business': {'icon': '💼', 'label': 'Empresarios', 'industry_label': 'Empresarios y CEOs', 'industry_desc': 'Empresarios, CEOs y figuras del mundo corporativo.'},
    'tv': {'icon': '📺', 'label': 'Televisión', 'industry_label': 'Televisión y Presentadores', 'industry_desc': 'Presentadores, conductores y figuras de televisión.'},
    'chef': {'icon': '🍳', 'label': 'Chefs', 'industry_label': 'Chefs y Gastronomía', 'industry_desc': 'Chefs, cocineros y figuras de la gastronomía.'},
    'journalist': {'icon': '📰', 'label': 'Periodistas', 'industry_label': 'Periodistas', 'industry_desc': 'Periodistas, reporteros y comunicadores.'},
    'comedian': {'icon': '😂', 'label': 'Comedia', 'industry_label': 'Comediantes', 'industry_desc': 'Comediantes, humoristas y figuras del entretenimiento.'},
    'sports': {'icon': '🏆', 'label': 'Deportes Varios', 'industry_label': 'Deportistas', 'industry_desc': 'Atletas y deportistas de diversas disciplinas.'},
    'basketball': {'icon': '🏀', 'label': 'Baloncesto', 'industry_label': 'Baloncesto NBA', 'industry_desc': 'Jugadores de baloncesto profesionales.'},
    'tennis': {'icon': '🎾', 'label': 'Tenis', 'industry_label': 'Tenis', 'industry_desc': 'Tenistas profesionales del circuito internacional.'},
    'director': {'icon': '🎥', 'label': 'Directores', 'industry_label': 'Directores de Cine', 'industry_desc': 'Directores de cine, televisión y teatro.'},
    'influencer': {'icon': '📱', 'label': 'Influencers', 'industry_label': 'Influencers y Creadores', 'industry_desc': 'Creadores de contenido, influencers y personalidades digitales.'},
    'boxer': {'icon': '🥊', 'label': 'Boxeadores', 'industry_label': 'Boxeadores', 'industry_desc': 'Boxeadores profesionales y figuras del boxeo.'},
    'baseball': {'icon': '⚾', 'label': 'Béisbol', 'industry_label': 'Béisbol', 'industry_desc': 'Jugadores de béisbol profesionales.'},
    'tech': {'icon': '💻', 'label': 'Tecnología', 'industry_label': 'Tecnología e Innovación', 'industry_desc': 'Figuras del mundo tecnológico y la innovación.'},
}

LABELS_SPANISH = {
    'singer': 'Cantantes', 'actor': 'Actores y Actrices', 'footballer': 'Futbolistas',
    'politician': 'Políticos', 'writer': 'Escritores', 'model': 'Modelos',
    'cyclist': 'Ciclistas', 'business': 'Empresarios', 'tv': 'Televisión',
    'chef': 'Chefs', 'journalist': 'Periodistas', 'comedian': 'Comedia',
    'sports': 'Deportes Varios', 'basketball': 'Baloncesto', 'tennis': 'Tenis',
    'director': 'Directores', 'influencer': 'Influencers', 'boxer': 'Boxeadores',
    'baseball': 'Béisbol', 'tech': 'Tecnología',
}

CATEGORY_NAMES = list(CATEGORY_META.keys())

# Old slugs that were removed/deduplicated -> their current canonical slug.
# These generate HTML redirect pages so old URLs don't 404 (preserves SEO equity).
REDIRECT_MAP = {
    '50_cent': '50-cent',
    'chris-brown': 'chris_brown',
    'chris-pratt': 'chris_pratt',
    'diomedes-daz': 'diomedes-diaz',
    'doris-salcedo': 'doris_salcedo',
    'dr-disrespect': 'drdisrespect',
    'ederson': 'ederson-moraes',
    'edgar-renteria': 'edgar_rentería',
    'emma_thompson': 'emma-thompson',
    'eslabon_armado': 'eslabon-armado',
    'faryd-mondragon': 'faryd_mondragón',
    'fernando-vallejo': 'fernando_vallejo',
    'gwen-stefani': 'gwen_stefani',
    'jessi_uribe': 'jessi-uribe',
    'joe_arroyo': 'joe-arroyo',
    'juan-cuadrado': 'juan-guillermo-cuadrado',
    'justin-timberlake': 'justin_timberlake',
    'karol_g': 'karol-g',
    'kelly-clarkson': 'kelly_clarkson',
    'laura-restrepo': 'laura_restrepo',
    'luis-alberto-posada': 'luis_alberto_posada',
    'maggie_smith': 'maggie-smith',
    'mary-j-blige': 'mary_j_blige',
    'mau_y_ricky': 'mau-y-ricky',
    'mon_laferte': 'mon-laferte',
    'nat_king_cole': 'nat-king-cole',
    'orlando-bloom': 'orlando_bloom',
    'rodri': 'rodri-hernandez',
    'tom_cruise': 'tom-cruise',
    'abdel-halim-hafez': 'abdelhalim-hafez',
    'addison_rae': 'addison-rae',
    'al_pacino': 'al-pacino',
    'alejandro-irritu': 'alejandro-gonzlez-irritu',
    'alejandro_fernández': 'alejandro-fernndez',
    'alejandro_gonzález_iñárritu': 'alejandro-gonzlez-irritu',
    'alfonso_cuarón': 'alfonso-cuarn',
    'alicia_keys': 'alicia-keys',
    'amy_schumer': 'amy-schumer',
    'amy_winehouse': 'amy-winehouse',
    'andr_s_cepeda': 'andrs-cepeda',
    'angela_merkel': 'angela-merkel',
    'angelina_jolie': 'angelina-jolie',
    'anitta-singer': 'anitta',
    'anthony_bourdain': 'anthony-bourdain',
    'anthony_hopkins': 'anthony-hopkins',
    'antonio_banderas': 'antonio-banderas',
    'anuel_aa': 'anuel-aa',
    'aretha_franklin': 'aretha-franklin',
    'ariana_grande': 'ariana-grande',
    'bad_bunny': 'bad-bunny',
    'barack_obama': 'barack-obama',
    'becky_g': 'becky-g',
    'bella_poarch': 'bella-poarch',
    'belem-guerrero-mendez': 'belem-guerrero-mndez',
    'ben_affleck': 'ben-affleck',
    'benedict_cumberbatch': 'benedict-cumberbatch',
    'bernard_arnault': 'bernard-arnault',
    'bernie_sanders': 'bernie-sanders',
    'beyoncé': 'beyonc',
    'bill_gates': 'bill-gates',
    'billie_eilish': 'billie-eilish',
    'billy_joel': 'billy-joel',
    'bob_dylan': 'bob-dylan',
    'bob_marley': 'bob-marley',
    'bobby_flay': 'bobby-flay',
    'brad_pitt': 'brad-pitt',
    'britney_spears': 'britney-spears',
    'bruce_springsteen': 'bruce-springsteen',
    'bruno_mars': 'bruno-mars',
    'caeleb_dressel': 'caeleb-dressel',
    'café_tacvba': 'caf-tacvba',
    'calvin_harris': 'calvin-harris',
    'camila_cabello': 'camila-cabello',
    'canelo_lvarez': 'canelo-lvarez',
    'cardi_b': 'cardi-b',
    'carlos_valderrama': 'carlos-valderrama',
    'carlos_vives': 'carlos-vives',
    'carolina-giraldo': 'karol-g',
    'carrie_underwood': 'carrie-underwood',
    'catalina-duque-abru': 'catalina-duque-abreu',
    'cate_blanchett': 'cate-blanchett',
    'caterine_ibargüen': 'caterine-ibargen',
    'charlize_theron': 'charlize-theron',
    'chiara_ferragni': 'chiara-ferragni',
    'chris_evans': 'chris-evans',
    'chris_hemsworth': 'chris-hemsworth',
    'chris_rock': 'chris-rock',
    'christian_bale': 'christian-bale',
    'christina_aguilera': 'christina-aguilera',
    'christopher_nolan': 'christopher-nolan',
    'cl': 'cl-rapper',
    'cl-2ne1': 'cl-rapper',
    'colin_firth': 'colin-firth',
    'cristiano_ronaldo': 'cristiano-ronaldo',
    'csar-mora': 'cesar-mora',
    'daddy_yankee': 'daddy-yankee',
    'daft_punk': 'daft-punk',
    'dave_chappelle': 'dave-chappelle',
    'david_beckham': 'david-beckham',
    'david_bowie': 'david-bowie',
    'david_dobrik': 'david-dobrik',
    'david_fincher': 'david-fincher',
    'david_guetta': 'david-guetta',
    'demi_lovato': 'demi-lovato',
    'denzel_washington': 'denzel-washington',
    'diomedes_daz': 'diomedes-diaz',
    'doja_cat': 'doja-cat',
    'dolly_parton': 'dolly-parton',
    'donald_trump': 'donald-trump',
    'dr_dre': 'dr-dre',
    'dua_lipa': 'dua-lipa',
    'dwayne_johnson': 'dwayne-johnson',
    'ed_sheeran': 'ed-sheeran',
    'dulce-maria-rodriguez': 'dulce-mara',
    'edgar-rentera': 'edgar_rentería',
    'edson_lvarez': 'edson-lvarez',
    'egan_bernal': 'egan-bernal',
    'eiza-gonzlez': 'eiza-gonzalez',
    'elaine-thompson': 'elaine-thompson-herah',
    'ellen_degeneres': 'ellen-degeneres',
    'elon_musk': 'elon-musk',
    'elton_john': 'elton-john',
    'elvis_presley': 'elvis-presley',
    'emma_chamberlain': 'emma-chamberlain',
    'emma_stone': 'emma-stone',
    'emma_watson': 'emma-watson',
    'emmanuel_macron': 'emmanuel-macron',
    'enrique_iglesias': 'enrique-iglesias',
    'eric-andr': 'eric-andre',
    'erling_haaland': 'erling-haaland',
    'ewan_mcgregor': 'ewan-mcgregor',
    'fabio-enrique-parra': 'fabio-parra',
    'felix-stray-kids': 'felix',
    'fernando_botero': 'fernando-botero',
    'fluffy': 'gabriel-iglesias',
    'frank_sinatra': 'frank-sinatra',
    'freddie_mercury': 'freddie-mercury',
    'gabriel_garcía_márquez': 'gabriel-garca-mrquez',
    'gary_oldman': 'gary-oldman',
    'george_clooney': 'george-clooney',
    'giannis_antetokounmpo': 'giannis-antetokounmpo',
    'giselle-itie': 'giselle-iti',
    'gloria_trevi': 'gloria-trevi',
    'gordon_ramsay': 'gordon-ramsay',
    'grard_depardieu': 'grard-depardieu',
    'grupo_firme': 'grupo-firme',
    'guillermo_del_toro': 'guillermo-del-toro',
    'guillermo_francella': 'guillermo-francella',
    'gustavo_petro': 'gustavo-petro',
    'halle_berry': 'halle-berry',
    'harrison_ford': 'harrison-ford',
    'harry_styles': 'harry-styles',
    'helen_mirren': 'helen-mirren',
    'hillary_clinton': 'hillary-clinton',
    'huda_kattan': 'huda-kattan',
    'hugh_grant': 'hugh-grant',
    'idris_elba': 'idris-elba',
    'iván_duque': 'ivn-duque',
    'j_balvin': 'j-balvin',
    'jack_dorsey': 'jack-dorsey',
    'jair_bolsonaro': 'jair-bolsonaro',
    'jake_gyllenhaal': 'jake-gyllenhaal',
    'james_cameron': 'james-cameron',
    'james_charles': 'james-charles',
    'james_rodríguez': 'james-rodriguez',
    'jamie_oliver': 'jamie-oliver',
    'janet_jackson': 'janet-jackson',
    'javier_bardem': 'javier-bardem',
    'jean_reno': 'jean-reno',
    'jeff_bezos': 'jeff-bezos',
    'jeffree_star': 'jeffree-star',
    'jennie': 'jennie-kim',
    'jennifer_aniston': 'jennifer-aniston',
    'jennifer_lawrence': 'jennifer-lawrence',
    'jennifer_lopez': 'jennifer-lopez',
    'jeremy_renner': 'jeremy-renner',
    'jerry_seinfeld': 'jerry-seinfeld',
    'jimin-bts': 'jimin',
    'jimmy_fallon': 'jimmy-fallon',
    'jimmy-hendrix': 'jimi-hendrix',
    'jimmy_kimmel': 'jimmy-kimmel',
    'joaquin_phoenix': 'joaquin-phoenix',
    'joe_biden': 'joe-biden',
    'john_legend': 'john-legend',
    'john_lennon': 'john-lennon',
    'john_oliver': 'john-oliver',
    'johnny_cash': 'johnny-cash',
    'johnny_depp': 'johnny-depp',
    'juan_cuadrado': 'juan-guillermo-cuadrado',
    'juan_manuel_santos': 'juan-manuel-santos',
    'juan_pablo_raba': 'juan-pablo-raba',
    'juan-sebastin-vern': 'juan-sebastian-veron',
    'jude_law': 'jude-law',
    'judi_dench': 'judi-dench',
    'julia_roberts': 'julia-roberts',
    'justin_bieber': 'justin-bieber',
    'justin_trudeau': 'justin-trudeau',
    'kamala_harris': 'kamala-harris',
    'kanye_west': 'kanye-west',
    'karim_benzema': 'karim-benzema',
    'kate_winslet': 'kate-winslet',
    'katy_perry': 'katy-perry',
    'keanu_reeves': 'keanu-reeves',
    'kendall_jenner': 'kendall-jenner',
    'kendrick_lamar': 'kendrick-lamar',
    'kevin_de_bruyne': 'kevin-de-bruyne',
    'kevin_durant': 'kevin-durant',
    'kevin_hart': 'kevin-hart',
    'khalil-gibran': 'kahlil-gibran',
    'kim_kardashian': 'kim-kardashian',
    'kylian_mbappé': 'kylian-mbapp',
    'kylie_jenner': 'kylie-jenner',
    'lady_gaga': 'lady-gaga',
    'lana_del_rey': 'lana-del-rey',
    'larry_page': 'larry-page',
    'lebron_james': 'lebron-james',
    'led_zeppelin': 'led-zeppelin',
    'leonardo_dicaprio': 'leonardo-dicaprio',
    'lewis_hamilton': 'lewis-hamilton',
    'liam_neeson': 'liam-neeson',
    'liam_payne': 'liam-payne',
    'lil_wayne': 'lil-wayne',
    'lionel_messi': 'lionel-messi',
    'los_fabulosos_cadillacs': 'los-fabulosos-cadillacs',
    'louis_tomlinson': 'louis-tomlinson',
    'luis_fonsi': 'luis-fonsi',
    'luis-fernando-muriel': 'luis-muriel',
    'luis_miguel': 'luis-miguel',
    'luiz-incio-lula-da-silva': 'lula-da-silva',
    'luka_modrić': 'luka-modri',
    'luke_combs': 'luke-combs',
    'man': 'maná',
    'manny_pacquiao': 'manny-pacquiao',
    'manolo_cardona': 'manolo-cardona',
    'manuel_turizo': 'manuel-turizo',
    'marc_anthony': 'marc-anthony',
    'margot_robbie': 'margot-robbie',
    'maria-fernanda-yepez': 'maria-fernanda-yepes',
    'mariah_carey': 'mariah-carey',
    'mariana-pajn': 'mariana-pajon',
    'mario-alberto-yepes-diaz': 'mario-yepes',
    'marion_cotillard': 'marion-cotillard',
    'mark_ruffalo': 'mark-ruffalo',
    'mark_zuckerberg': 'mark-zuckerberg',
    'martin_garrix': 'martin-garrix',
    'martin_scorsese': 'martin-scorsese',
    'matt_damon': 'matt-damon',
    'max_verstappen': 'max-verstappen',
    'megan_thee_stallion': 'megan-thee-stallion',
    'meryl_streep': 'meryl-streep',
    'michael_jackson': 'michael-jackson',
    'michael_phelps': 'michael-phelps',
    'mick_jagger': 'mick-jagger',
    'mike_bahía': 'mike-baha',
    'mike_tyson': 'mike-tyson',
    'miley_cyrus': 'miley-cyrus',
    'mohamed-abdel-wahab': 'mohammad-abdel-wahab',
    'mohamed_salah': 'mohamed-salah',
    'morgan_freeman': 'morgan-freeman',
    'morgan_wallen': 'morgan-wallen',
    'nairo_quintana': 'nairo-quintana',
    'narendra_modi': 'narendra-modi',
    'natalia_lafourcade': 'natalia-lafourcade',
    'natti_natasha': 'natti-natasha',
    'niall_horan': 'niall-horan',
    'nicki_minaj': 'nicki-minaj',
    'nicole_kidman': 'nicole-kidman',
    'nigahiga': 'ryan-higa',
    'nihachu': 'niki-nihachu',
    'novak_djokovic': 'novak-djokovic',
    'olaf_scholz': 'olaf-scholz',
    'olivia_rodrigo': 'olivia-rodrigo',
    'oprah_winfrey': 'oprah-winfrey',
    'oscar_isaac': 'oscar-isaac',
    'pabllo_vittar': 'pabllo-vittar',
    'paola_jara': 'paola-jara',
    'paul_mccartney': 'paul-mccartney',
    'pedro_almodóvar': 'pedro-almodvar',
    'pedro_pascal': 'pedro-pascal',
    'penélope_cruz': 'penlope-cruz',
    'peso_pluma': 'peso-pluma',
    'pink_floyd': 'pink-floyd',
    'pipe_bueno': 'pipe-bueno',
    'piso_21': 'piso-21',
    'pope_francis': 'pope-francis',
    'post_malone': 'post-malone',
    'queen_(band)': 'queen',
    'quentin_tarantino': 'quentin-tarantino',
    'rachael_ray': 'rachael-ray',
    'radamel_falcao': 'radamel-falcao',
    'rafael_nadal': 'rafael-nadal',
    'ras-tafari': 'haile-selassie',
    'rené_higuita': 'reney-higuita',
    'ricardo_darín': 'ricardo-darn',
    'richard_branson': 'richard-branson',
    'ricky_gervais': 'ricky-gervais',
    'ricky_martin': 'ricky-martin',
    'ridley_scott': 'ridley-scott',
    'rigoberto_urán': 'rigoberto-urn',
    'rishi_sunak': 'rishi-sunak',
    'robert_de_niro': 'robert-de-niro',
    'robert_downey_jr': 'robert-downey-jr',
    'robert_lewandowski': 'robert-lewandowski',
    'roger_federer': 'roger-federer',
    'romeo_santos': 'romeo-santos',
    'ronaldinho': 'ronaldinho-gaucho',
    'rose': 'ros',
    'rosalía': 'rosala',
    'ryan_gosling': 'ryan-gosling',
    'ryan_reynolds': 'ryan-reynolds',
    'salma_hayek': 'salma-hayek',
    'sam_altman': 'sam-altman',
    'sam_smith': 'sam-smith',
    'samuel_l_jackson': 'samuel-l-jackson',
    'sandra_bullock': 'sandra-bullock',
    'sara_corrales': 'sara-corrales',
    'satya_nadella': 'satya-nadella',
    'scarlett_johansson': 'scarlett-johansson',
    'sebastin-yatra': 'sebastian-yatra',
    'selena_gomez': 'selena-gomez',
    'serena_williams': 'serena-williams',
    'sergey_brin': 'sergey-brin',
    'sergio_ramos': 'sergio-ramos',
    'shawn_mendes': 'shawn-mendes',
    'silvestre_dangond': 'silvestre-dangond',
    'simon-garfunkel': 'simon--garfunkel',
    'snoop_dogg': 'snoop-dogg',
    'soda_stereo': 'soda-stereo',
    'sofia-loren': 'sophia-loren',
    'sofía_vergara': 'sofa-vergara',
    'stephen_colbert': 'stephen-colbert',
    'stephen_curry': 'stephen-curry',
    'steven_spielberg': 'steven-spielberg',
    'stevie_wonder': 'stevie-wonder',
    'taylor_swift': 'taylor-swift',
    'thala': 'thalia',
    'the-rolling-stones': 'rolling-stones',
    'the_rolling_stones': 'rolling-stones',
    'the_beatles': 'the-beatles',
    'the_weeknd': 'the-weeknd',
    'tim_cook': 'tim-cook',
    'timothée_chalamet': 'timothe-chalamet',
    'tina_turner': 'tina-turner',
    'tini': 'tini-stoessel',
    'tom_brady': 'tom-brady',
    'tom_hanks': 'tom-hanks',
    'tom-jones': 'tom-jones-singer',
    'tom_hiddleston': 'tom-hiddleston',
    'totó_la_momposina': 'tot-la-momposina',
    'trevor_noah': 'trevor-noah',
    'tyler_the_creator': 'tyler-the-creator',
    'usain_bolt': 'usain-bolt',
    'vicente_fernández': 'vicente-fernndez',
    'vincius-jnior': 'vinicius-jr',
    'vinícius_júnior': 'vinicius-jr',
    'viola_davis': 'viola-davis',
    'virgil_van_dijk': 'virgil-van-dijk',
    'vladimir_putin': 'vladimir-putin',
    'volodymyr_zelenskyy': 'volodymyr-zelenskyy',
    'warren_buffett': 'warren-buffett',
    'whitney_houston': 'whitney-houston',
    'will_smith': 'will-smith',
    'willie_nelson': 'willie-nelson',
    'wolfgang_puck': 'wolfgang-puck',
    'xi_jinping': 'xi-jinping',
    'xavi': 'xavi-hernandez',
    'yeison-jimnez': 'yeison-jimenez',
    'zach_bryan': 'zach-bryan',
    'zach_king': 'zach-king',
    'zayn_malik': 'zayn-malik',
    'zlatan_ibrahimović': 'zlatan-ibrahimovi',
}


def compute_quality(ce, content_len):
    """Compute quality level: A (complete), B (acceptable), C (stub)."""
    checks = {
        'long_excerpt': len(ce['excerpt']) > 200,
        'has_content': content_len > 2000,
        'has_image': bool(ce['image']) and 'Crystal_Clear' not in ce['image'],
        'has_birth': bool(ce['born']),
        'has_nationality': bool(ce['nationality']),
        'has_birthplace': bool(ce['birthPlace']),
        'has_tags': len(ce['tags']) > 0,
        'has_profession': ce['profession'] not in ('Public Figure', ''),
    }
    score = sum(1 for v in checks.values() if v)
    if score >= 6 and checks['long_excerpt'] and checks['has_content']:
        return 'A'
    elif score >= 4:
        return 'B'
    else:
        return 'C'


def parse_bio(filepath):
    """Parse a bio HTML file and extract metadata."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content_len = len(content)
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

    quality = compute_quality({
        'excerpt': excerpt, 'image': image, 'born': born,
        'nationality': nationality, 'birthPlace': birth_place,
        'tags': tags, 'profession': profession,
    }, content_len)

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
        'quality': quality,
        'content_len': content_len,
        'filepath': filepath,
    }


def generate_card(ce):
    tags_html = ''.join(f'<span class="bio-card-tag">{t}</span>' for t in ce['tags'][:3])
    excerpt_short = ce['excerpt'][:150].replace('"', '&quot;')
    badge = ''
    if ce['quality'] == 'C':
        badge = '<span class="stub-badge-card" style="display:inline-block;font-size:0.7rem;background:#fff3cd;color:#856404;padding:0.1rem 0.4rem;border-radius:3px;margin-left:0.25rem;" title="Biografía en desarrollo">📝 Stub</span>'
    elif ce['quality'] == 'A':
        badge = '<span class="stub-badge-card" style="display:inline-block;font-size:0.7rem;background:#d4edda;color:#155724;padding:0.1rem 0.4rem;border-radius:3px;margin-left:0.25rem;" title="Biografía completa">✅ Completa</span>'
    return f'''          <a href="bios/{ce['slug']}.html" class="bio-card{' stub-card' if ce['quality'] == 'C' else ''}" itemscope itemtype="https://schema.org/Person" data-category="{ce['category']}">
            <img src="{ce['image']}" alt="{ce['name']}" class="bio-card-img" width="400" height="250" loading="lazy" itemprop="image">
            <div class="bio-card-body">
              <h3 class="bio-card-name" itemprop="name">{ce['name']}{badge}</h3>
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
    return f"    {{id:'{_esc(ce['slug'])}',name:'{_esc(ce['name'])}',fullName:'{_esc(ce['fullName'])}',profession:'{_esc(ce['profession'])}',excerpt:'{_esc(ce['excerpt'])}',url:'bios/{_esc(ce['slug'])}.html',tags:[{tags_str}],image:'{img}',dateAdded:{ce['dateAdded']}}},"

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
    def file_date(ce):
        try:
            ts = os.path.getmtime(ce['filepath'])
            return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        except Exception:
            return '2026-07-25'
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
    <lastmod>{file_date(ce)}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
{img_block}  </url>"""


INDUSTRY_DIR = os.path.join(BASE_DIR, 'industries')


def normalize_name(name):
    return re.sub(r'[^a-z0-9]', '', name.lower().replace('-', '').replace('_', ''))


def deduplicate_bios(bio_list):
    """Group by normalized name, keep the larger file for duplicates."""
    groups = {}
    for b in bio_list:
        key = normalize_name(b['name'])
        if key not in groups:
            groups[key] = []
        groups[key].append(b)

    deduped = []
    removed = 0
    for key, items in groups.items():
        if len(items) == 1:
            deduped.append(items[0])
        else:
            items.sort(key=lambda x: -x['content_len'])
            deduped.append(items[0])
            removed += len(items) - 1
            for dup in items[1:]:
                print(f'  Dedup: keeping "{items[0]["slug"]}" ({items[0]["content_len"]}b), removing "{dup["slug"]}" ({dup["content_len"]}b)')
                try:
                    os.remove(dup['filepath'])
                    print(f'    Deleted {dup["filepath"]}')
                except OSError as e:
                    print(f'    Could not delete {dup["filepath"]}: {e}')
    return deduped, removed


def generate_redirect_pages(bios):
    """Generate HTML redirect pages for old deduped slugs -> current slugs."""
    existing_slugs = {b['slug'] for b in bios}
    count = 0
    for old, new in REDIRECT_MAP.items():
        if old == new:
            continue
        if new not in existing_slugs:
            continue
        page = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="0; url={DOMAIN}/bios/{new}.html">
  <link rel="canonical" href="{DOMAIN}/bios/{new}.html">
  <meta name="robots" content="noindex, follow">
  <title>Redirección - Wifi Oficial Biography</title>
</head>
<body>
  <p>Esta página se ha movido. <a href="{DOMAIN}/bios/{new}.html">Haz clic aquí para ir a la biografía.</a></p>
  <script>window.location.replace("{DOMAIN}/bios/{new}.html");</script>
</body>
</html>'''
        path = os.path.join(BIOS_DIR, f'{old}.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(page)
        count += 1
    print(f'  Generated {count} redirect pages')


def generate_industry_page(cat_key, bios_in_cat, count):
    """Generate a single industry landing page."""
    meta = CATEGORY_META.get(cat_key, {'icon': '📌', 'label': cat_key.capitalize(), 'industry_label': cat_key.capitalize(), 'industry_desc': ''})
    slug = cat_key
    title = f"{meta['industry_label']} | Wifi Oficial Biography"
    desc = f"Biografías completas de {meta['industry_label'].lower()}. {meta['industry_desc']} Explora {count} perfiles con información verificada y datos estructurados."

    bios_sorted = sorted(bios_in_cat, key=lambda x: -x['content_len'])[:100]
    list_items = '\n'.join(
        f'    <li><a href="../bios/{b["slug"]}.html">{b["name"]}</a> <small style="color:#999;">— {b["profession"][:60]}</small></li>'
        for b in bios_sorted
    )

    html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="{DOMAIN}/industries/{slug}.html">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{html.escape(desc[:200])}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{DOMAIN}/industries/{slug}.html">
  <meta property="og:site_name" content="Wifi Oficial Biography">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{html.escape(desc[:200])}">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "{meta['industry_label']}",
  "description": "{html.escape(desc)}",
  "url": "{DOMAIN}/industries/{slug}.html",
  "about": {{"@type": "Thing", "name": "{meta['industry_label']}"}},
  "numberOfItems": {count}
}}</script>
</head>
<body>
  <header class="site-header" role="banner">
    <div class="header-inner">
      <a href="../index.html" class="site-logo"><img src="../images/favicon.jpg" alt="Wifi Oficial Biography" class="logo-icon" width="32" height="32" style="border-radius:50%;"><div class="logo-text">Wifi Oficial <span>Biography</span></div></a>
      <nav class="main-nav" id="mainNav" role="navigation"><ul>
        <li><a href="../index.html">Inicio</a></li>
        <li><a href="../index.html#biografias">Biografías</a></li>
        <li><a href="../index.html#categorias">Categorías</a></li>
      </ul></nav>
    </div>
  </header>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content">
      <nav class="breadcrumbs"><a href="../index.html">Inicio</a> › <span>{meta['industry_label']}</span></nav>
      <h1>{meta['icon']} {meta['industry_label']}</h1>
      <p style="font-size:1.1rem;color:#555;margin-bottom:1.5rem;">{html.escape(meta['industry_desc'])}</p>
      <p style="color:#888;margin-bottom:2rem;">Total de biografías: <strong>{count}</strong></p>
      <ul style="columns:3 250px;column-gap:2rem;list-style:none;padding:0;">
{list_items}
      </ul>
      <p style="margin-top:2rem;"><a href="../index.html#categorias">← Ver todas las categorías</a></p>
    </main>
  </div>
  <footer class="site-footer">
    <div class="footer-inner">
      <p>&copy; 2026 Wifi Oficial Biography.</p>
    </div>
  </footer>
</body>
</html>'''
    return html_content


def rebuild():
    bio_files = sorted(glob.glob(os.path.join(BIOS_DIR, '*.html')))
    print(f'Found {len(bio_files)} bio files')

    bios = []
    for bf in bio_files:
        try:
            with open(bf, 'r', encoding='utf-8') as _f:
                _head = _f.read(400)
            if 'http-equiv="refresh"' in _head or 'noindex, follow' in _head:
                continue  # redirect page, skip
            ce = parse_bio(bf)
            bios.append(ce)
        except Exception as e:
            print(f'  Error parsing {bf}: {e}')

    # Dedup
    bios, removed_count = deduplicate_bios(bios)
    print(f'After dedup: {len(bios)} bios ({removed_count} duplicates removed)')

    # Generate redirect pages for old deduped slugs BEFORE writing cards, so
    # parse_bio skips them for the current build but they still exist on disk.
    print('Generating redirect pages for old slugs...')
    generate_redirect_pages(bios)

    bios.sort(key=lambda x: x['name'].lower())
    print(f'Parsed {len(bios)} bios successfully')

    cats = {}
    quality_counts = {'A': 0, 'B': 0, 'C': 0}
    for b in bios:
        c = b['category']
        cats[c] = cats.get(c, 0) + 1
        quality_counts[b['quality']] = quality_counts.get(b['quality'], 0) + 1
    total = len(bios)

    print(f'\nCategory counts:')
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f'  {c}: {n}')
    print(f'  TOTAL: {total}')
    print(f'\nQuality distribution:')
    for q in ('A', 'B', 'C'):
        print(f'  Level {q}: {quality_counts.get(q, 0)}')

    print('\nRebuilding index.html...')
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        idx = f.read()

    cards = '\n'.join(generate_card(b) for b in bios)

    PAGINATION_BLOCK = f'''      <div class="show-more-bios-container">
        <span class="show-more-bios-count" id="showMoreCount">Mostrando 10 de {total} biografías</span>
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
    # Update filter bar "Todos" count + bio-filter-results count + stat counter
    idx = _re.sub(
        r'(<button class="bio-filter-btn active" data-filter="all">Todos <span class="filter-count">)\d+(</span>)',
        f'\\g<1>{total}\\2', idx)
    idx = _re.sub(
        r'(<div class="bio-filter-results"[^>]*>Mostrando \d+ de )\d+( biografías</div>)',
        f'\\g<1>{total}\\2', idx)
    idx = _re.sub(
        r'(<span class="stat-number">)\d+(</span>\s*<span class="stat-label">Biografías</span>)',
        f'\\g<1>{total}\\2', idx)

    # Update filter bar individual category counts
    for cat, count in cats.items():
        pattern = rf'(<button class="bio-filter-btn[^"]*" data-filter="{cat}">[^<]*<span class="filter-count">)\d+(</span>)'
        idx = _re.sub(pattern, f'\\g<1>{count}\\2', idx)

    # Update category CARD counts (hardcoded in #categorias section)
    for cat, count in cats.items():
        cat_card_pattern = rf'(<a href="#".*?class="category-card"[^>]*data-cat-filter="{cat}"[^>]*>.*?<span class="category-count">)\d+\s*biografías(</span>)'
        idx = _re.sub(cat_card_pattern, f'\\g<1>{count} biografías\\2', idx, flags=_re.DOTALL)

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

    # Replace sidebar with dynamic latestBios
    sidebar_start = '  const latestBios = [\n'
    sidebar_end = '  (function(){'
    if sidebar_start in js:
        s_idx2 = js.index(sidebar_start)
        e_idx2 = js.index(sidebar_end, s_idx2) + len(sidebar_end) + 100  # include IIFE opening line
        # Find the actual end of the sidebar IIFE (the })(); pattern after our section)
        iife_end = js.find('})();', e_idx2)
        if iife_end != -1:
            e_idx2 = iife_end + 5  # })();
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

    today = datetime.date.today().isoformat()
    sm_header = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">

  <!-- Homepage -->
  <url>
    <loc>https://wifioficialbiography.org/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <image:image>
      <image:loc>https://wifioficialbiography.org/images/henry-orozco.jpg</image:loc>
      <image:title>Wifi Oficial Biography -- Enciclopedia de Biografias</image:title>
      <image:caption>Plataforma de biografias de figuras publicas a nivel internacional</image:caption>
    </image:image>
  </url>

'''
    # Add industry pages to sitemap
    for cat_key in cats:
        sm_header += f'''  <url>
    <loc>{DOMAIN}/industries/{cat_key}.html</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

'''
    sm_footer = '\n</urlset>\n'

    with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
        f.write(sm_header + sitemap_entries + sm_footer)
    print(f'  Written {total + 1 + len(cats)} URLs to sitemap.xml')

    # Generate industry pages
    print('\nGenerating industry pages...')
    os.makedirs(INDUSTRY_DIR, exist_ok=True)
    industry_count = 0
    for cat_key in sorted(cats.keys()):
        count = cats[cat_key]
        bios_in_cat = [b for b in bios if b['category'] == cat_key]
        html_page = generate_industry_page(cat_key, bios_in_cat, count)
        industry_path = os.path.join(INDUSTRY_DIR, f'{cat_key}.html')
        with open(industry_path, 'w', encoding='utf-8') as f:
            f.write(html_page)
        industry_count += 1
        print(f'  Generated industries/{cat_key}.html ({count} bios)')
    print(f'  Total industry pages: {industry_count}')

    print(f'\n=== REBUILD COMPLETE ===')
    print(f'Total bios: {total}')
    print(f'Categories: {len(cats)}')
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f'  {c}: {n}')


if __name__ == '__main__':
    rebuild()
