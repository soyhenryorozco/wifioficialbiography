#!/usr/bin/env python3
"""
Generate new biographies for top public figures across categories.
Uses Wikipedia API for content and Wikimedia Commons for images.
"""
import urllib.request, urllib.parse, json, re, os, glob, time, html as html_mod

BIOS_DIR = 'bios'

# === CURATED LIST OF TOP PUBLIC FIGURES ===
# Organized by category/region for comprehensiveness.
# Format: (wikipedia_title, category, profession)

NEW_BIOGRAPHIES = [
    # === USA SINGERS - TOP 200 ===
    ("Beyoncé", "singer", "Singer-Songwriter"),
    ("Taylor_Swift", "singer", "Singer-Songwriter"),
    ("Lady_Gaga", "singer", "Singer-Songwriter"),
    ("Bruno_Mars", "singer", "Singer-Songwriter"),
    ("Adele", "singer", "Singer-Songwriter"),
    ("Rihanna", "singer", "Singer-Songwriter"),
    ("Katy_Perry", "singer", "Singer-Songwriter"),
    ("Madonna", "singer", "Singer-Songwriter"),
    ("Britney_Spears", "singer", "Singer-Songwriter"),
    ("Justin_Timberlake", "singer", "Singer-Songwriter"),
    ("Ariana_Grande", "singer", "Singer-Songwriter"),
    ("Billie_Eilish", "singer", "Singer-Songwriter"),
    ("Eminem", "singer", "Rapper"),
    ("Jay-Z", "singer", "Rapper"),
    ("Kanye_West", "singer", "Rapper"),
    ("Drake_(musician)", "singer", "Rapper"),
    ("Lizzo", "singer", "Singer-Songwriter"),
    ("Olivia_Rodrigo", "singer", "Singer-Songwriter"),
    ("Dua_Lipa", "singer", "Singer-Songwriter"),
    ("Harry_Styles", "singer", "Singer-Songwriter"),
    ("Selena_Gomez", "singer", "Singer-Songwriter"),
    ("Demi_Lovato", "singer", "Singer-Songwriter"),
    ("Miley_Cyrus", "singer", "Singer-Songwriter"),
    ("Jennifer_Lopez", "singer", "Singer-Songwriter"),
    ("Mariah_Carey", "singer", "Singer-Songwriter"),
    ("Whitney_Houston", "singer", "Singer-Songwriter"),
    ("Michael_Jackson", "singer", "Singer-Songwriter"),
    ("Prince_(musician)", "singer", "Singer-Songwriter"),
    ("Elvis_Presley", "singer", "Singer-Songwriter"),
    ("Frank_Sinatra", "singer", "Singer-Songwriter"),
    ("Aretha_Franklin", "singer", "Singer-Songwriter"),
    ("Stevie_Wonder", "singer", "Singer-Songwriter"),
    ("Bob_Dylan", "singer", "Singer-Songwriter"),
    ("Bruce_Springsteen", "singer", "Singer-Songwriter"),
    ("Elton_John", "singer", "Singer-Songwriter"),
    ("Billy_Joel", "singer", "Singer-Songwriter"),
    ("Paul_McCartney", "singer", "Singer-Songwriter"),
    ("John_Lennon", "singer", "Singer-Songwriter"),
    ("Bob_Marley", "singer", "Reggae Singer"),
    ("Freddie_Mercury", "singer", "Singer-Songwriter"),
    ("David_Bowie", "singer", "Singer-Songwriter"),
    ("Pink_(singer)", "singer", "Singer-Songwriter"),
    ("Christina_Aguilera", "singer", "Singer-Songwriter"),
    ("Gwen_Stefani", "singer", "Singer-Songwriter"),
    ("Snoop_Dogg", "singer", "Rapper"),
    ("Dr._Dre", "singer", "Rapper"),
    ("50_Cent", "singer", "Rapper"),
    ("Kendrick_Lamar", "singer", "Rapper"),
    ("Lil_Wayne", "singer", "Rapper"),
    ("Nicki_Minaj", "singer", "Rapper"),
    ("Cardi_B", "singer", "Rapper"),
    ("Megan_Thee_Stallion", "singer", "Rapper"),
    ("Doja_Cat", "singer", "Singer-Rapper"),
    ("Post_Malone", "singer", "Singer-Rapper"),
    ("Halsey_(singer)", "singer", "Singer-Songwriter"),
    ("Camila_Cabello", "singer", "Singer-Songwriter"),
    ("Shawn_Mendes", "singer", "Singer-Songwriter"),
    ("Justin_Bieber", "singer", "Singer-Songwriter"),
    ("The_Weeknd", "singer", "Singer-Songwriter"),
    ("Chris_Brown", "singer", "Singer-Songwriter"),
    ("Usher_(musician)", "singer", "Singer-Songwriter"),
    ("Alicia_Keys", "singer", "Singer-Songwriter"),
    ("John_Legend", "singer", "Singer-Songwriter"),
    ("Mary_J._Blige", "singer", "Singer-Songwriter"),
    ("Tina_Turner", "singer", "Singer-Songwriter"),
    ("Cher", "singer", "Singer-Songwriter"),
    ("Janet_Jackson", "singer", "Singer-Songwriter"),
    ("Kelly_Clarkson", "singer", "Singer-Songwriter"),
    ("Carrie_Underwood", "singer", "Singer-Songwriter"),
    ("Luke_Combs", "singer", "Country Singer"),
    ("Morgan_Wallen", "singer", "Country Singer"),
    ("Zach_Bryan", "singer", "Country Singer"),
    ("Willie_Nelson", "singer", "Country Singer"),
    ("Dolly_Parton", "singer", "Country Singer"),
    ("Johnny_Cash", "singer", "Country Singer"),
    ("Nat_King_Cole", "singer", "Singer"),
    ("Sam_Smith", "singer", "Singer-Songwriter"),
    ("Lana_Del_Rey", "singer", "Singer-Songwriter"),
    ("Tyler,_the_Creator", "singer", "Rapper"),

    # === USA ACTORS - TOP 250 ===
    ("Tom_Hanks", "actor", "Actor"),
    ("Leonardo_DiCaprio", "actor", "Actor"),
    ("Brad_Pitt", "actor", "Actor"),
    ("Tom_Cruise", "actor", "Actor"),
    ("Robert_De_Niro", "actor", "Actor"),
    ("Al_Pacino", "actor", "Actor"),
    ("Morgan_Freeman", "actor", "Actor"),
    ("Denzel_Washington", "actor", "Actor"),
    ("Will_Smith", "actor", "Actor"),
    ("Johnny_Depp", "actor", "Actor"),
    ("Harrison_Ford", "actor", "Actor"),
    ("Samuel_L._Jackson", "actor", "Actor"),
    ("Robert_Downey_Jr.", "actor", "Actor"),
    ("Chris_Evans_(actor)", "actor", "Actor"),
    ("Chris_Hemsworth", "actor", "Actor"),
    ("Chris_Pratt", "actor", "Actor"),
    ("Mark_Ruffalo", "actor", "Actor"),
    ("Jeremy_Renner", "actor", "Actor"),
    ("Scarlett_Johansson", "actor", "Actress"),
    ("Jennifer_Lawrence", "actor", "Actress"),
    ("Angelina_Jolie", "actor", "Actress"),
    ("Julia_Roberts", "actor", "Actress"),
    ("Meryl_Streep", "actor", "Actress"),
    ("Cate_Blanchett", "actor", "Actress"),
    ("Nicole_Kidman", "actor", "Actress"),
    ("Charlize_Theron", "actor", "Actress"),
    ("Margot_Robbie", "actor", "Actress"),
    ("Emma_Watson", "actor", "Actress"),
    ("Emma_Stone", "actor", "Actress"),
    ("Jennifer_Aniston", "actor", "Actress"),
    ("Sandra_Bullock", "actor", "Actress"),
    ("Halle_Berry", "actor", "Actress"),
    ("Viola_Davis", "actor", "Actress"),
    ("Zendaya", "actor", "Actress"),
    ("Timothée_Chalamet", "actor", "Actor"),
    ("Joaquin_Phoenix", "actor", "Actor"),
    ("Christian_Bale", "actor", "Actor"),
    ("Matt_Damon", "actor", "Actor"),
    ("Ben_Affleck", "actor", "Actor"),
    ("George_Clooney", "actor", "Actor"),
    ("Keanu_Reeves", "actor", "Actor"),
    ("Ryan_Reynolds", "actor", "Actor"),
    ("Ryan_Gosling", "actor", "Actor"),
    ("Jake_Gyllenhaal", "actor", "Actor"),
    ("Oscar_Isaac", "actor", "Actor"),
    ("Pedro_Pascal", "actor", "Actor"),
    ("Antonio_Banderas", "actor", "Actor"),
    ("Javier_Bardem", "actor", "Actor"),
    ("Penélope_Cruz", "actor", "Actress"),
    ("Salma_Hayek", "actor", "Actress"),

    # === LATIN AMERICA SINGERS - TOP 200 ===
    ("Bad_Bunny", "singer", "Singer-Rapper"),
    ("Karol_G", "singer", "Singer-Songwriter"),
    ("J_Balvin", "singer", "Singer-Songwriter"),
    ("Maluma", "singer", "Singer-Songwriter"),
    ("Anuel_AA", "singer", "Rapper"),
    ("Ozuna", "singer", "Singer-Rapper"),
    ("Daddy_Yankee", "singer", "Singer-Rapper"),
    ("Luis_Fonsi", "singer", "Singer-Songwriter"),
    ("Enrique_Iglesias", "singer", "Singer-Songwriter"),
    ("Ricky_Martin", "singer", "Singer-Songwriter"),
    ("Marc_Anthony", "singer", "Singer-Songwriter"),
    ("Romeo_Santos", "singer", "Singer-Songwriter"),
    ("Juanes", "singer", "Singer-Songwriter"),
    ("Carlos_Vives", "singer", "Singer-Songwriter"),
    ("Maná", "singer", "Rock Band"),
    ("Café_Tacvba", "singer", "Rock Band"),
    ("Rosalía", "singer", "Singer-Songwriter"),
    ("Becky_G", "singer", "Singer-Songwriter"),
    ("Natti_Natasha", "singer", "Singer-Songwriter"),
    ("Anitta_(singer)", "singer", "Singer-Songwriter"),
    ("Ludmilla_(singer)", "singer", "Singer-Songwriter"),
    ("Pabllo_Vittar", "singer", "Singer-Songwriter"),
    ("Gloria_Trevi", "singer", "Singer-Songwriter"),
    ("Luis_Miguel", "singer", "Singer-Songwriter"),
    ("Alejandro_Fernández", "singer", "Singer-Songwriter"),
    ("Vicente_Fernández", "singer", "Singer-Songwriter"),
    ("Selena_(singer)", "singer", "Singer-Songwriter"),
    ("Jenni_Rivera", "singer", "Singer-Songwriter"),
    ("Mon_Laferte", "singer", "Singer-Songwriter"),
    ("Tini_(singer)", "singer", "Singer-Songwriter"),
    ("Mau_y_Ricky", "singer", "Duo"),
    ("Manuel_Turizo", "singer", "Singer-Songwriter"),
    ("Sebastián_Yatra", "singer", "Singer-Songwriter"),
    ("Camilo_(singer)", "singer", "Singer-Songwriter"),
    ("Fonseca_(singer)", "singer", "Singer-Songwriter"),
    ("Greeicy", "singer", "Singer-Songwriter"),
    ("Mike_Bahía", "singer", "Singer-Songwriter"),
    ("Piso_21", "singer", "Band"),
    ("Morat", "singer", "Band"),
    ("Jessi_Uribe", "singer", "Singer-Songwriter"),
    ("Pipe_Bueno", "singer", "Singer-Songwriter"),
    ("Paola_Jara", "singer", "Singer-Songwriter"),
    ("Yeison_Jiménez", "singer", "Singer-Songwriter"),
    ("Grupo_Firme", "singer", "Band"),
    ("Eslabon_Armado", "singer", "Band"),
    ("Peso_Pluma", "singer", "Singer-Songwriter"),
    ("Natalia_Lafourcade", "singer", "Singer-Songwriter"),
    ("Soda_Stereo", "singer", "Rock Band"),
    ("Los_Fabulosos_Cadillacs", "singer", "Rock Band"),

    # === COLOMBIAN FIGURES - TOP 200 ===
    ("Carlos_Vives", "singer", "Singer-Songwriter"),
    ("Juanes", "singer", "Singer-Songwriter"),
    ("Gabriel_García_Márquez", "writer", "Writer"),
    ("Fernando_Botero", "artist", "Artist"),
    ("James_Rodríguez", "footballer", "Footballer"),
    ("Radamel_Falcao", "footballer", "Footballer"),
    ("Juan_Cuadrado", "footballer", "Footballer"),
    ("Faryd_Mondragón", "footballer", "Footballer"),
    ("René_Higuita", "footballer", "Footballer"),
    ("Carlos_Valderrama", "footballer", "Footballer"),
    ("Nairo_Quintana", "cyclist", "Cyclist"),
    ("Rigoberto_Urán", "cyclist", "Cyclist"),
    ("Egan_Bernal", "cyclist", "Cyclist"),
    ("Mariana_Pajón", "cyclist", "Cyclist"),
    ("Caterine_Ibargüen", "sports", "Athlete"),
    ("Juan_Manuel_Santos", "politician", "Politician"),
    ("Iván_Duque", "politician", "Politician"),
    ("Gustavo_Petro", "politician", "Politician"),
    ("Álvaro_Uribe", "politician", "Politician"),
    ("Fernando_Botero", "artist", "Painter-Sculptor"),
    ("Doris_Salcedo", "artist", "Artist"),
    ("Fernando_Vallejo", "writer", "Writer"),
    ("Laura_Restrepo", "journalist", "Journalist"),
    ("Andrés_Cepeda", "singer", "Singer-Songwriter"),
    ("Jessi_Uribe", "singer", "Singer-Songwriter"),
    ("Silvestre_Dangond", "singer", "Singer-Songwriter"),
    ("Diomedes_Díaz", "singer", "Singer-Songwriter"),
    ("Grupo_Niche", "singer", "Band"),
    ("Joe_Arroyo", "singer", "Singer-Songwriter"),
    ("Totó_la_Momposina", "singer", "Singer-Songwriter"),
    ("Rupert_Reyes", "singer", "Singer-Songwriter"),
    ("Sofía_Vergara", "actor", "Actress"),
    ("Juan_Pablo_Raba", "actor", "Actor"),
    ("Carmenza_Cárdenas", "actor", "Actress"),
    ("Manolo_Cardona", "actor", "Actor"),
    ("Sara_Corrales", "actor", "Actress"),
    ("Luis_Alberto_Posada", "baseball", "Baseball Player"),
    ("Edgar_Rentería", "baseball", "Baseball Player"),

    # === EUROPEAN SINGERS - TOP 200 ===
    ("Ed_Sheeran", "singer", "Singer-Songwriter"),
    ("Coldplay", "singer", "Rock Band"),
    ("Radiohead", "singer", "Rock Band"),
    ("The_Beatles", "singer", "Band"),
    ("Queen_(band)", "singer", "Rock Band"),
    ("Led_Zeppelin", "singer", "Rock Band"),
    ("Pink_Floyd", "singer", "Rock Band"),
    ("The_Rolling_Stones", "singer", "Rock Band"),
    ("U2", "singer", "Rock Band"),
    ("ABBA", "singer", "Pop Band"),
    ("Daft_Punk", "singer", "Electronic Duo"),
    ("Adele", "singer", "Singer-Songwriter"),
    ("Amy_Winehouse", "singer", "Singer-Songwriter"),
    ("David_Bowie", "singer", "Singer-Songwriter"),
    ("Freddie_Mercury", "singer", "Singer-Songwriter"),
    ("Elton_John", "singer", "Singer-Songwriter"),
    ("Paul_McCartney", "singer", "Singer-Songwriter"),
    ("Mick_Jagger", "singer", "Singer-Songwriter"),
    ("Sam_Smith", "singer", "Singer-Songwriter"),
    ("Dua_Lipa", "singer", "Singer-Songwriter"),
    ("Harry_Styles", "singer", "Singer-Songwriter"),
    ("Zayn_Malik", "singer", "Singer-Songwriter"),
    ("Liam_Payne", "singer", "Singer-Songwriter"),
    ("Louis_Tomlinson", "singer", "Singer-Songwriter"),
    ("Niall_Horan", "singer", "Singer-Songwriter"),
    ("Calvin_Harris", "singer", "DJ-Producer"),
    ("David_Guetta", "singer", "DJ-Producer"),
    ("Martin_Garrix", "singer", "DJ-Producer"),
    ("Avicii", "singer", "DJ-Producer"),
    ("Kygo", "singer", "DJ-Producer"),

    # === EUROPEAN ACTORS - TOP 200 ===
    ("Daniel_Day-Lewis", "actor", "Actor"),
    ("Gary_Oldman", "actor", "Actor"),
    ("Anthony_Hopkins", "actor", "Actor"),
    ("Liam_Neeson", "actor", "Actor"),
    ("Colin_Firth", "actor", "Actor"),
    ("Benedict_Cumberbatch", "actor", "Actor"),
    ("Tom_Hiddleston", "actor", "Actor"),
    ("Idris_Elba", "actor", "Actor"),
    ("Hugh_Grant", "actor", "Actor"),
    ("Jude_Law", "actor", "Actor"),
    ("Ewan_McGregor", "actor", "Actor"),
    ("Orlando_Bloom", "actor", "Actor"),
    ("Kate_Winslet", "actor", "Actress"),
    ("Emma_Thompson", "actor", "Actress"),
    ("Helen_Mirren", "actor", "Actress"),
    ("Judi_Dench", "actor", "Actress"),
    ("Maggie_Smith", "actor", "Actress"),
    ("Marion_Cotillard", "actor", "Actress"),
    ("Sophie_Marceau", "actor", "Actress"),
    ("Jean_Reno", "actor", "Actor"),
    ("Gérard_Depardieu", "actor", "Actor"),
    ("Pierre_Niney", "actor", "Actor"),
    ("Vin_Cassel", "actor", "Actor"),
    ("Omar_Sy", "actor", "Actor"),
    ("Ricardo_Darín", "actor", "Actor"),
    ("Guillermo_Francella", "actor", "Actor"),

    # === POLITICIANS - TOP 100 ===
    ("Joe_Biden", "politician", "Politician"),
    ("Donald_Trump", "politician", "Politician"),
    ("Barack_Obama", "politician", "Politician"),
    ("Kamala_Harris", "politician", "Politician"),
    ("Vladimir_Putin", "politician", "Politician"),
    ("Volodymyr_Zelenskyy", "politician", "Politician"),
    ("Emmanuel_Macron", "politician", "Politician"),
    ("Olaf_Scholz", "politician", "Politician"),
    ("Rishi_Sunak", "politician", "Politician"),
    ("Narendra_Modi", "politician", "Politician"),
    ("Xi_Jinping", "politician", "Politician"),
    ("Luiz_Inácio_Lula_da_Silva", "politician", "Politician"),
    ("Jair_Bolsonaro", "politician", "Politician"),
    ("Nayib_Bukele", "politician", "Politician"),
    ("Miguel_Díaz-Canel", "politician", "Politician"),
    ("Justin_Trudeau", "politician", "Politician"),
    ("António_Guterres", "politician", "Politician"),
    ("Pope_Francis", "politician", "Religious Leader"),
    ("Angela_Merkel", "politician", "Politician"),
    ("Hillary_Clinton", "politician", "Politician"),
    ("Bernie_Sanders", "politician", "Politician"),
    ("Alexandria_Ocasio-Cortez", "politician", "Politician"),

    # === SPORTS - TOP 200 ===
    ("Lionel_Messi", "footballer", "Footballer"),
    ("Cristiano_Ronaldo", "footballer", "Footballer"),
    ("Neymar", "footballer", "Footballer"),
    ("Kylian_Mbappé", "footballer", "Footballer"),
    ("Erling_Haaland", "footballer", "Footballer"),
    ("Kevin_De_Bruyne", "footballer", "Footballer"),
    ("Mohamed_Salah", "footballer", "Footballer"),
    ("Karim_Benzema", "footballer", "Footballer"),
    ("Robert_Lewandowski", "footballer", "Footballer"),
    ("Luka_Modrić", "footballer", "Footballer"),
    ("Virgil_van_Dijk", "footballer", "Footballer"),
    ("Sergio_Ramos", "footballer", "Footballer"),
    ("Zlatan_Ibrahimović", "footballer", "Footballer"),
    ("David_Beckham", "footballer", "Footballer"),
    ("Lewis_Hamilton", "sports", "Racing Driver"),
    ("Max_Verstappen", "sports", "Racing Driver"),
    ("LeBron_James", "basketball", "Basketball Player"),
    ("Stephen_Curry", "basketball", "Basketball Player"),
    ("Kevin_Durant", "basketball", "Basketball Player"),
    ("Giannis_Antetokounmpo", "basketball", "Basketball Player"),
    ("Mike_Tyson", "boxer", "Boxer"),
    ("Floyd_Mayweather_Jr.", "boxer", "Boxer"),
    ("Manny_Pacquiao", "boxer", "Boxer"),
    ("Canelo_Álvarez", "boxer", "Boxer"),
    ("Serena_Williams", "tennis", "Tennis Player"),
    ("Novak_Djokovic", "tennis", "Tennis Player"),
    ("Rafael_Nadal", "tennis", "Tennis Player"),
    ("Roger_Federer", "tennis", "Tennis Player"),
    ("Tom_Brady", "sports", "American Football"),
    ("Usain_Bolt", "sports", "Athlete"),
    ("Caeleb_Dressel", "sports", "Swimmer"),
    ("Michael_Phelps", "sports", "Swimmer"),

    # === INFLUENCERS - TOP 50 ===
    ("MrBeast", "influencer", "Content Creator"),
    ("Kylie_Jenner", "influencer", "Businesswoman"),
    ("Kim_Kardashian", "influencer", "Businesswoman"),
    ("Kendall_Jenner", "influencer", "Model"),
    ("Cristiano_Ronaldo", "footballer", "Footballer"),
    ("Leo_Messi", "footballer", "Footballer"),
    ("Selena_Gomez", "singer", "Singer-Songwriter"),
    ("Ariana_Grande", "singer", "Singer-Songwriter"),
    ("Dwayne_Johnson", "actor", "Actor"),
    ("Kevin_Hart", "actor", "Comedian"),
    ("LeBron_James", "basketball", "Basketball Player"),
    ("Charli_D'Amelio", "influencer", "Content Creator"),
    ("Addison_Rae", "influencer", "Content Creator"),
    ("Dixie_D'Amelio", "influencer", "Content Creator"),
    ("Bella_Poarch", "influencer", "Content Creator"),
    ("Zach_King", "influencer", "Content Creator"),
    ("David_Dobrik", "influencer", "Content Creator"),
    ("Emma_Chamberlain", "influencer", "Content Creator"),
    ("PewDiePie", "influencer", "Content Creator"),
    ("Markiplier", "influencer", "Content Creator"),
    ("Jacksepticeye", "influencer", "Content Creator"),
    ("Ninja_(gamer)", "influencer", "Streamer"),
    ("Pokimane", "influencer", "Streamer"),
    ("LilyPichu", "influencer", "Streamer"),
    ("Valkyrae", "influencer", "Content Creator"),

    # === FASHION & BEAUTY INFLUENCERS ===
    ("Chiara_Ferragni", "influencer", "Fashion Influencer"),
    ("James_Charles", "influencer", "Makeup Artist"),
    ("Jeffree_Star", "influencer", "Makeup Artist"),
    ("NikkieTutorials", "influencer", "Makeup Artist"),
    ("Huda_Kattan", "influencer", "Makeup Artist"),

    # === COMEDIANS ===
    ("Dave_Chappelle", "comedian", "Comedian"),
    ("Kevin_Hart", "comedian", "Comedian"),
    ("Chris_Rock", "comedian", "Comedian"),
    ("Jerry_Seinfeld", "comedian", "Comedian"),
    ("Ricky_Gervais", "comedian", "Comedian"),
    ("Jimmy_Fallon", "comedian", "Comedian"),
    ("Jimmy_Kimmel", "comedian", "Comedian"),
    ("Stephen_Colbert", "comedian", "Comedian"),
    ("Trevor_Noah", "comedian", "Comedian"),
    ("John_Oliver_(comedian)", "comedian", "Comedian"),
    ("Ellen_DeGeneres", "comedian", "Comedian"),
    ("Amy_Schumer", "comedian", "Comedian"),
    ("Katherine_Ryan", "comedian", "Comedian"),
    ("Michael_McIntyre", "comedian", "Comedian"),
    ("Lee_Evans_(comedian)", "comedian", "Comedian"),

    # === BUSINESS LEADERS ===
    ("Elon_Musk", "business", "Entrepreneur"),
    ("Jeff_Bezos", "business", "Entrepreneur"),
    ("Mark_Zuckerberg", "business", "Entrepreneur"),
    ("Bill_Gates", "business", "Entrepreneur"),
    ("Tim_Cook", "business", "Entrepreneur"),
    ("Satya_Nadella", "business", "Entrepreneur"),
    ("Larry_Page", "business", "Entrepreneur"),
    ("Sergey_Brin", "business", "Entrepreneur"),
    ("Warren_Buffett", "business", "Investor"),
    ("Bernard_Arnault", "business", "Entrepreneur"),
    ("Oprah_Winfrey", "business", "Media Executive"),
    ("Richard_Branson", "business", "Entrepreneur"),
    ("Jack_Dorsey", "business", "Entrepreneur"),
    ("Sam_Altman", "business", "Entrepreneur"),

    # === DIRECTORS ===
    ("Steven_Spielberg", "director", "Film Director"),
    ("Martin_Scorsese", "director", "Film Director"),
    ("Quentin_Tarantino", "director", "Film Director"),
    ("Christopher_Nolan", "director", "Film Director"),
    ("David_Fincher", "director", "Film Director"),
    ("James_Cameron", "director", "Film Director"),
    ("Ridley_Scott", "director", "Film Director"),
    ("Guillermo_del_Toro", "director", "Film Director"),
    ("Alfonso_Cuarón", "director", "Film Director"),
    ("Alejandro_González_Iñárritu", "director", "Film Director"),
    ("Pedro_Almodóvar", "director", "Film Director"),
    ("Nolan,_Christopher", "director", "Film Director"),

    # === CHEFS ===
    ("Gordon_Ramsay", "chef", "Chef"),
    ("Jamie_Oliver", "chef", "Chef"),
    ("Anthony_Bourdain", "chef", "Chef"),
    ("Wolfgang_Puck", "chef", "Chef"),
    ("Bobby_Flay", "chef", "Chef"),
    ("Nigella_Lawson", "chef", "Chef"),
    ("Rachael_Ray", "chef", "Chef"),
]

# Remove duplicates by Wikipedia title
seen = set()
unique = []
for item in NEW_BIOGRAPHIES:
    if item[0] not in seen:
        seen.add(item[0])
        unique.append(item)
NEW_BIOGRAPHIES = unique

print(f"Total unique figures in list: {len(NEW_BIOGRAPHIES)}")

# === CHECK EXISTING BIOS ===
existing = set()
for fp in glob.glob(os.path.join(BIOS_DIR, '*.html')):
    slug = os.path.basename(fp).replace('.html', '')
    existing.add(slug)

to_generate = []
for title, cat, prof in NEW_BIOGRAPHIES:
    slug = title.lower().replace(' ', '-').replace('_(musician)', '').replace('_(singer)', '').replace('_(actor)', '').replace('_(comedian)', '').replace('_(gamer)', '')
    slug = slug.replace('__', '-').replace(',', '').replace('.', '')
    if slug.startswith('-'):
        slug = slug[1:]
    if slug.endswith('-'):
        slug = slug[:-1]
    slug = re.sub(r'-+', '-', slug)
    
    if slug not in existing:
        to_generate.append((slug, title, cat, prof))

print(f"Already existing: {len(NEW_BIOGRAPHIES) - len(to_generate)}")
print(f"To generate: {len(to_generate)}")

# === FETCH WIKIPEDIA DATA IN BATCHES ===
def fetch_batch(titles):
    """Fetch Wikipedia extracts for a batch of titles."""
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts|pageimages',
        'exintro': 1,
        'explaintext': 1,
        'redirects': 1,
        'pithumbsize': 500,
        'titles': '|'.join(titles)
    }
    data_enc = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        'https://en.wikipedia.org/w/api.php',
        data=data_enc,
        headers={
            'User-Agent': 'WifiOficialBio/7.0 (https://wifioficialbiography.org)',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def extract_nationality_from_extract(extract):
    """Try to extract nationality from first paragraph."""
    patterns = [
        r'is an?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:singer|actor|actress|rapper|politician|footballer)',
        r'is a\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:singer|actor|actress|rapper|politician|footballer)',
        r'born\s+.*?(?:in|on)\s+([A-Z][a-z]+)',
    ]
    for pat in patterns:
        m = re.search(pat, extract)
        if m:
            return m.group(1).strip()
    return 'International'

def extract_birth_date(extract):
    """Try to extract birth date."""
    m = re.search(r'born\s+(?:on\s+)?([A-Z][a-z]+ \d{1,2},?\s+\d{4})', extract)
    if m:
        return m.group(1)
    m = re.search(r'born\s+(\d{1,2}\s+[A-Z][a-z]+\s+\d{4})', extract)
    if m:
        return m.group(1)
    return ''

def txt2slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

# Generar bios en lotes
org_schema = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Wifi Oficial Biography",
    "alternateName": ["Wifi Oficial", "WOB"],
    "url": "https://wifioficialbiography.org",
    "logo": "https://wifioficialbiography.org/images/wifioficial-og.png",
    "description": "An independent editorial platform and digital encyclopedia for biographies of notable public figures.",
    "foundingDate": "2024",
    "founders": [
      {"@type": "Person", "name": "Henry Orozco", "sameAs": "https://wifioficialbiography.org/bios/henry-orozco.html"},
      {"@type": "Person", "name": "Farid Duque", "sameAs": "https://wifioficialbiography.org/bios/farid-duque.html"}
    ],
    "sameAs": [
      "https://www.instagram.com/wifioficial/",
      "https://www.facebook.com/wifioficialco",
      "https://www.tiktok.com/@wifioficialbiography",
      "https://www.threads.net/@wifioficial"
    ],
    "isAccessibleForFree": true
  }
  </script>

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Wifi Oficial Biography",
    "url": "https://wifioficialbiography.org",
    "description": "An independent editorial platform and digital encyclopedia for biographies of notable public figures.",
    "inLanguage": ["en", "es"],
    "isAccessibleForFree": true
  }
  </script>
'''

def generate_bio(slug, title, full_title, category, profession, extract, image_url, nationality, birth_date):
    """Generate a complete bio HTML file following Shakira template standards."""
    name = full_title.replace('_', ' ')
    # Clean parentheses from name
    display_name = re.sub(r'\s*\(.*?\)\s*', '', name).strip()
    
    if not extract:
        extract = f"{display_name} is a notable {profession.lower() or 'public figure'}."
    
    first_sentence = extract.split('.')[0] + '.' if '.' in extract else extract
    
    meta_desc = first_sentence[:160].replace('"', '&quot;')
    
    cat_map = {
        'singer': 'Singer', 'actor': 'Actor', 'footballer': 'Footballer',
        'politician': 'Politician', 'writer': 'Writer', 'artist': 'Artist',
        'business': 'Entrepreneur', 'influencer': 'Influencer', 'comedian': 'Comedian',
        'chef': 'Chef', 'director': 'Director', 'sports': 'Athlete',
        'boxer': 'Boxer', 'tennis': 'Tennis Player', 'basketball': 'Basketball Player',
        'baseball': 'Baseball Player', 'cyclist': 'Cyclist', 'journalist': 'Journalist',
        'model': 'Model', 'tv': 'Television Personality', 'tech': 'Technology'
    }
    cat_display = cat_map.get(category, 'Public Figure')
    
    # Build slug for alternateName
    alt_name = display_name
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{display_name} — {cat_display} | Wifi Oficial Biography</title>
  <meta name="description" content="{meta_desc}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://wifioficialbiography.org/bios/{slug}.html">
  <meta property="og:type" content="profile">
  <meta property="og:url" content="https://wifioficialbiography.org/bios/{slug}.html">
  <meta property="og:title" content="{display_name}">
  <meta property="og:description" content="{meta_desc}">
  <meta property="og:image" content="{image_url or f'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png'}">
  <meta property="og:image:alt" content="{display_name}">
  <meta property="og:site_name" content="Wifi Oficial Biography">
  <meta property="og:locale" content="en_US">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{display_name}">
  <meta name="twitter:description" content="{meta_desc}">
  <meta name="twitter:site" content="@wifioficial">
  <meta name="twitter:image" content="{image_url or f'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png'}">
  <meta name="twitter:image:alt" content="{display_name}">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0645ad">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="alternate" hreflang="en" href="https://wifioficialbiography.org/bios/{slug}.html">
  <link rel="alternate" hreflang="es" href="https://wifioficialbiography.org/bios/{slug}.html">
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{display_name}",
  "alternateName": ["{alt_name}"],
  "description": "{html_mod.escape(first_sentence)}",
  "url": "https://wifioficialbiography.org/bios/{slug}.html",
  "image": "{image_url or ''}",
  "sameAs": ["https://en.wikipedia.org/wiki/{full_title}"],
  "knowsLanguage": ["English"]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "headline": "{display_name} — {cat_display}",
  "description": "{html_mod.escape(first_sentence)}",
  "url": "https://wifioficialbiography.org/bios/{slug}.html",
  "mainEntity": {{"@type": "Person", "name": "{display_name}"}},
  "dateCreated": "2026-07-25",
  "dateModified": "2026-07-25",
  "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "publisher": {{"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {{"@type": "ImageObject", "url": "https://wifioficialbiography.org/images/favicon.jpg"}}}},
  "image": "{image_url or ''}"
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "https://wifioficialbiography.org/"}},
    {{"@type": "ListItem", "position": 2, "name": "Biografías", "item": "https://wifioficialbiography.org/#biografias"}},
    {{"@type": "ListItem", "position": 3, "name": "{display_name}", "item": "https://wifioficialbiography.org/bios/{slug}.html"}}
  ]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{display_name} — {cat_display}",
  "description": "{html_mod.escape(first_sentence)}",
  "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "publisher": {{"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {{"@type": "ImageObject", "url": "https://wifioficialbiography.org/images/favicon.jpg"}}}},
  "datePublished": "2026-07-25",
  "dateModified": "2026-07-25",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://wifioficialbiography.org/bios/{slug}.html"}},
  "image": "{image_url or ''}",
  "isBasedOn": "https://en.wikipedia.org/wiki/{full_title}",
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type": "Question", "name": "Who is {display_name}?", "acceptedAnswer": {{"@type": "Answer", "text": "{html_mod.escape(first_sentence)}"}}}},
    {{"@type": "Question", "name": "What is {display_name} known for?", "acceptedAnswer": {{"@type": "Answer", "text": "{display_name} is a {profession} known for their contributions to {cat_display}."}}}}
  ]
}}</script>
{org_schema}</head>
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
  <div class="search-overlay" id="searchOverlay" role="dialog" aria-label="Búsqueda">
    <div class="search-box"><input type="search" id="searchOverlayInput" placeholder="Buscar biografía..." autocomplete="off"><div class="search-results" id="searchResults"></div></div>
  </div>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <a href="../index.html">Inicio</a> <span class="separator">›</span>
        <a href="../index.html#biografias">Biografías</a> <span class="separator">›</span>
        <span>{display_name}</span>
      </nav>
      <div class="bio-page-header">
        <div class="bio-page-photo">
          <img src="{image_url or f'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png'}" alt="{display_name}" title="{display_name} — {cat_display}" width="440" height="660" loading="eager" fetchpriority="high" itemprop="image">
        </div>
        <div class="bio-page-info">
          <h1 itemprop="name">{display_name}</h1>
          <div class="subtitle" itemprop="alternateName">{alt_name}</div>
          <p itemprop="description">{html_mod.escape(first_sentence)}</p>
        </div>
      </div>
      <div class="infobox" role="complementary" aria-label="Personal information">
        <div class="infobox-header">{display_name}</div>
        <div class="infobox-image"><img src="{image_url or f'https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Crystal_Clear_app_Login_Manager.svg/400px-Crystal_Clear_app_Login_Manager.svg.png'}" alt="{display_name}" width="440" height="660" loading="lazy"></div>
        <table><tbody>
          <tr><th>Full Name</th><td itemprop="birthName">{alt_name}</td></tr>
          <tr><th>Nationality</th><td itemprop="nationality">{nationality or 'International'}</td></tr>
          <tr><th>Occupation(s)</th><td itemprop="jobTitle">{cat_display}</td></tr>
        </tbody></table>
        <div class="infobox-section">Profiles</div>
        <table><tbody>
          <tr><th>Wikipedia</th><td><a href="https://en.wikipedia.org/wiki/{full_title}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{full_title}</a></td></tr>
        </tbody></table>
      </div>
      <nav class="toc" aria-label="Table of contents">
        <div class="toc-title">Contents</div>
        <ol>
          <li><a href="#biography">Biography</a></li>
          <li><a href="#references">References</a></li>
        </ol>
      </nav>
      <article class="bio-article">
        <div class="category-tags">
          <a href="#" class="category-tag">{cat_display}</a>
          <a href="#" class="category-tag">{nationality or 'International'}</a>
          <a href="#" class="category-tag">Public Figure</a>
        </div>
        
        <h2 id="biography">Biography</h2>
        <p><strong>{display_name}</strong> {first_sentence[0].lower() + first_sentence[1:] if first_sentence and first_sentence != extract else extract}</p>
        <p>{extract}</p>
        
    <section class="attribution-notice" style="margin-top:2rem;padding:1rem;background:#f5f5f5;border-left:4px solid #888;font-size:0.85rem;border-radius:4px;">
      <p><strong>Atribucion &mdash; CC BY-SA 4.0</strong></p>
      <p>El contenido textual de esta biografia esta basado en material de Wikipedia, disponible bajo la licencia 
      <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="license noopener">Creative Commons Atribucion-CompartirIgual 4.0 Internacional (CC BY-SA 4.0)</a>.
      </p><p>Las imagenes utilizadas pertenecen a <a href="https://commons.wikimedia.org/" target="_blank" rel="noopener">Wikimedia Commons</a> y estan sujetas a sus propias licencias (generalmente CC BY-SA o dominio publico).</p>
      <p><strong>Fuentes originales:</strong><br><a href="https://en.wikipedia.org/wiki/{full_title}" target="_blank" rel="noopener">https://en.wikipedia.org/wiki/{full_title}</a></p>
      <p style="margin-top:0.5rem;font-size:0.8rem;color:#666;">Terminos de la licencia: Puedes copiar, distribuir y modificar este contenido siempre que atribuyas la fuente original y compartas las modificaciones bajo la misma licencia.</p>
    </section>
    
    <h2 id="references">References</h2>
        <div class="reflist"><ol>
          <li><span class="cite-note">"{display_name}." Wikipedia. <a href="https://en.wikipedia.org/wiki/{full_title}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{full_title}</a></span></li>
        </ol></div>
        
        <h2>External Links</h2>
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/{full_title}" target="_blank" rel="noopener">Wikipedia — {display_name}</a></li>
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
        <a href="../index.html#about">Acerca de</a>
      </div>
      <div class="footer-social">
        <a href="https://www.instagram.com/wifioficial/" target="_blank" rel="noopener">📷 Instagram</a>
        <a href="https://www.facebook.com/wifioficialco" target="_blank" rel="noopener">📘 Facebook</a>
        <a href="https://www.tiktok.com/@wifioficialbiography" target="_blank" rel="noopener">🎵 TikTok</a>
        <a href="https://www.threads.net/@wifioficial" target="_blank" rel="noopener">🧵 Threads</a>
        <a href="https://telegram.me/wifimarco" target="_blank" rel="noopener">✈️ Telegram</a>
      </div>
      <p>&copy; 2026 Wifi Oficial Biography. Todos los derechos reservados.</p>
    </div>
  </footer>
  <script src="../js/app.js"></script>
</body>
</html>'''


# Process in batches of 25
BATCH_SIZE = 25
generated = 0
errors = 0

for i in range(0, len(to_generate), BATCH_SIZE):
    batch = to_generate[i:i+BATCH_SIZE]
    titles = [t for _, t, _, _ in batch]
    
    try:
        data = fetch_batch(titles)
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
        
        for slug, wiki_title, category, profession in batch:
            # Resolve redirect
            canon = redirects.get(wiki_title.lower(), wiki_title)
            extract = extract_map.get(canon) or extract_map.get(wiki_title)
            image_url = image_map.get(canon) or image_map.get(wiki_title, '')
            
            nationality = extract_nationality_from_extract(extract or '')
            birth_date = extract_birth_date(extract or '')
            
            html = generate_bio(slug, wiki_title, wiki_title, category, profession, extract or '', image_url, nationality, birth_date)
            
            fp = os.path.join(BIOS_DIR, f'{slug}.html')
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(html)
            generated += 1
            
    except Exception as e:
        errors += len(batch)
        print(f'  Batch error at {i}: {e}')
    
    time.sleep(0.5)
    if (i // BATCH_SIZE) % 20 == 0:
        print(f'  Progress: {min(i+BATCH_SIZE, len(to_generate))}/{len(to_generate)} — Generated: {generated}, Errors: {errors}')

print(f'\nDone! Generated: {generated}, Errors: {errors}')
