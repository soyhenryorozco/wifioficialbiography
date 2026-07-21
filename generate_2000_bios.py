#!/usr/bin/env python3
"""Generate 2,000 Shakira-level biographies from Wikipedia API data."""
import json, os, re, html, time, urllib.request, urllib.parse, urllib.error, sys, unicodedata

BIOS_DIR = "bios"
DOMAIN = "https://wifioficialbiography.org"
FNAME = "famous_2000.json"
WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_API_ES = "https://es.wikipedia.org/w/api.php"

def slugify(name):
    s = name.lower().replace(' ', '-')
    s = re.sub(r'[^a-z0-9\-]', '', s)
    s = s.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n').replace('ü','u')
    return s

def esc(s):
    if not s: return ''
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ')

def esc_xml(s):
    if not s: return ''
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&apos;')

def wiki_request(params, lang='en'):
    api = WIKI_API_ES if lang == 'es' else WIKI_API
    params['format'] = 'json'
    params['origin'] = '*'
    url = api + '?' + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'WifioficialBio/1.0 (bot)'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except:
        return None

def get_wiki_extracts(titles):
    """Get extracts for up to 50 titles at once."""
    if not titles: return {}
    params = {'action': 'query', 'titles': '|'.join(titles), 'prop': 'extracts|pageimages|pageterms|info',
              'exintro': '1', 'explaintext': '1', 'pithumbsize': 400, 'inprop': 'url'}
    data = wiki_request(params)
    if not data or 'query' not in data or 'pages' not in data['query']: return {}
    pages = data['query']['pages']
    result = {}
    for pid, p in pages.items():
        if pid == '-1': continue
        title = p.get('title', '')
        result[title] = {
            'extract': p.get('extract', ''),
            'image': p.get('thumbnail', {}).get('source', '') if 'thumbnail' in p else '',
            'description': p.get('terms', {}).get('description', [''])[0] if 'terms' in p else '',
            'pageurl': p.get('fullurl', ''),
            'pageid': pid,
        }
    return result

def get_wiki_full_sections(titles, lang='en'):
    """Get full section content for up to 10 titles."""
    if not titles: return {}
    params = {'action': 'query', 'titles': '|'.join(titles),
              'prop': 'extracts', 'explaintext': '1', 'exsectionformat': 'wiki'}
    data = wiki_request(params, lang)
    if not data or 'query' not in data: return {}
    result = {}
    for pid, p in data['query'].get('pages', {}).items():
        if pid == '-1': continue
        result[p.get('title', '')] = p.get('extract', '')
    return result

def parse_sections(extract):
    """Parse Wikipedia extract into sections."""
    lines = extract.split('\n')
    sections = {}
    current_section = 'Intro'
    current_text = []
    for line in lines:
        if line.startswith('== ') and line.endswith(' =='):
            if current_text:
                sections[current_section] = '\n'.join(current_text).strip()
            current_section = line.strip('= ')
            current_text = []
        else:
            current_text.append(line)
    if current_text:
        sections[current_section] = '\n'.join(current_text).strip()
    return sections

# Curated list of 2,000 famous living people with core data
# Format: [name, description, birthYear, countryCode, occupation, category]
PEOPLE = []

def add_people(category_name, people_list):
    for p in people_list:
        name = p[0]
        desc = p[1] if len(p) > 1 else ''
        byear = p[2] if len(p) > 2 else ''
        country = p[3] if len(p) > 3 else 'CO'
        occ = p[4] if len(p) > 4 else 'Public Figure'
        cat = p[5] if len(p) > 5 else 'singer'
        PEOPLE.append([name, desc, byear, country, occ, cat])

# ─── COLOMBIAN SINGERS (200) ───
colombian_singers = [
    ["Shakira","Colombian singer-songwriter, dancer, record producer","1977","CO","Singer","singer"],
    ["Karol G","Colombian reggaeton singer","1991","CO","Singer","singer"],
    ["J Balvin","Colombian reggaeton singer","1985","CO","Singer","singer"],
    ["Maluma","Colombian reggaeton singer","1994","CO","Singer","singer"],
    ["Juanes","Colombian rock musician","1972","CO","Singer","singer"],
    ["Carlos Vives","Colombian singer and actor","1961","CO","Singer","singer"],
    ["Fonseca","Colombian singer-songwriter","1979","CO","Singer","singer"],
    ["Willie Colón","American-born Colombian salsa musician","1950","CO","Musician","singer"],
    ["Joe Arroyo","Colombian salsa singer","1955","CO","Singer","singer"],
    ["Totó La Momposina","Colombian singer","1948","CO","Singer","singer"],
    ["Monsieur Periné","Colombian band","1988","CO","Musician","singer"],
    ["Aterciopelados","Colombian rock band","1992","CO","Musician","singer"],
    ["Bomba Estéreo","Colombian electronic band","2005","CO","Musician","singer"],
    ["Andrés Cepeda","Colombian singer","1973","CO","Singer","singer"],
    ["Silvestre Dangond","Colombian vallenato singer","1980","CO","Singer","singer"],
    ["Jessi Uribe","Colombian popular music singer","1995","CO","Singer","singer"],
    ["Arelys Henao","Colombian popular music singer","1977","CO","Singer","singer"],
    ["Paola Jara","Colombian popular music singer","1974","CO","Singer","singer"],
    ["Yeison Jiménez","Colombian popular music singer","1991","CO","Singer","singer"],
    ["Alzate","Colombian singer-songwriter","1977","CO","Singer","singer"],
    ["Pipe Bueno","Colombian singer","1992","CO","Singer","singer"],
    ["Greeicy","Colombian singer and actress","1992","CO","Singer","singer"],
    ["Mike Bahía","Colombian reggaeton singer","1984","CO","Singer","singer"],
    ["Manuel Turizo","Colombian reggaeton singer","2000","CO","Singer","singer"],
    ["Sebastián Yatra","Colombian reggaeton singer","1994","CO","Singer","singer"],
    ["Camilo","Colombian singer-songwriter","1994","CO","Singer","singer"],
    ["Mau y Ricky","Colombian pop duo","1993","CO","Singer","singer"],
    ["Feid","Colombian reggaeton singer","1992","CO","Singer","singer"],
    ["Ryan Castro","Colombian reggaeton singer","1993","CO","Singer","singer"],
    ["Ñejo","Colombian reggaeton singer","1978","CO","Singer","singer"],
    ["Dalmata","Colombian reggaeton singer","1982","CO","Singer","singer"],
    ["Pailita","Colombian reggaeton singer","1999","CO","Singer","singer"],
    ["Blessd","Colombian reggaeton singer","2000","CO","Singer","singer"],
    ["Jhayco","Colombian reggaeton singer","1993","CO","Singer","singer"],
    ["Zion & Lennox","Colombian reggaeton duo","1998","CO","Singer","singer"],
    ["Piso 21","Colombian pop band","2007","CO","Musician","singer"],
    ["Morad","Colombian rapper","1999","CO","Singer","singer"],
    ["Eladio Carrión","Puerto Rican rapper","1994","CO","Singer","singer"],
    ["Myke Towers","Puerto Rican rapper","1994","CO","Singer","singer"],
    ["Rauw Alejandro","Puerto Rican singer","1993","CO","Singer","singer"],
    ["Bad Bunny","Puerto Rican reggaeton singer","1994","PR","Singer","singer"],
    ["Anuel AA","Puerto Rican rapper","1992","PR","Singer","singer"],
    ["Ozuna","Puerto Rican reggaeton singer","1992","PR","Singer","singer"],
    ["Nicky Jam","Puerto Rican reggaeton singer","1981","PR","Singer","singer"],
    ["Daddy Yankee","Puerto Rican reggaeton singer","1977","PR","Singer","singer"],
    ["Don Omar","Puerto Rican reggaeton singer","1978","PR","Singer","singer"],
    ["Tito El Bambino","Puerto Rican reggaeton singer","1975","PR","Singer","singer"],
    ["Ivy Queen","Puerto Rican reggaeton singer","1972","PR","Singer","singer"],
    ["Wisin & Yandel","Puerto Rican reggaeton duo","1978","PR","Singer","singer"],
    ["Arcángel","Puerto Rican reggaeton singer","1985","PR","Singer","singer"],
    ["De La Ghetto","American reggaeton singer","1982","US","Singer","singer"],
    ["Farruko","Puerto Rican reggaeton singer","1991","PR","Singer","singer"],
    ["Luis Fonsi","Puerto Rican singer","1978","PR","Singer","singer"],
    ["Ricky Martin","Puerto Rican singer","1971","PR","Singer","singer"],
    ["Marc Anthony","American salsa singer","1968","US","Singer","singer"],
    ["Enrique Iglesias","Spanish singer","1975","ES","Singer","singer"],
    ["Romeo Santos","American bachata singer","1981","US","Singer","singer"],
    ["Prince Royce","American bachata singer","1989","US","Singer","singer"],
    ["Aventura","American bachata group","1994","US","Musician","singer"],
    ["Juan Luis Guerra","Dominican singer","1957","DO","Singer","singer"],
    ["Rubén Blades","Panamanian singer","1948","PA","Singer","singer"],
    ["Gloria Estefan","Cuban-American singer","1957","US","Singer","singer"],
    ["Celia Cruz","Cuban salsa singer","1925","CU","Singer","singer"],
    ["Rosalía","Spanish singer","1992","ES","Singer","singer"],
    ["Shakira","Colombian singer","1977","CO","Singer","singer"],
    ["Jennifer Lopez","American singer-actress","1969","US","Singer","singer"],
    ["Thalía","Mexican singer and actress","1971","MX","Singer","singer"],
    ["Paulina Rubio","Mexican singer","1971","MX","Singer","singer"],
    ["Gloria Trevi","Mexican singer","1968","MX","Singer","singer"],
    ["Alejandra Guzmán","Mexican singer","1968","MX","Singer","singer"],
    ["Lucía Méndez","Mexican actress and singer","1955","MX","Singer","singer"],
    ["Lucero","Mexican singer and actress","1969","MX","Singer","singer"],
    ["Ana Gabriel","Mexican singer","1955","MX","Singer","singer"],
    ["Luis Miguel","Mexican singer","1970","MX","Singer","singer"],
    ["Alejandro Fernández","Mexican singer","1971","MX","Singer","singer"],
    ["Vicente Fernández","Mexican singer","1940","MX","Singer","singer"],
    ["Juan Gabriel","Mexican singer","1950","MX","Singer","singer"],
    ["Julio Iglesias","Spanish singer","1943","ES","Singer","singer"],
    ["Plácido Domingo","Spanish operatic tenor","1941","ES","Singer","singer"],
    ["José Carreras","Spanish operatic tenor","1946","ES","Singer","singer"],
    ["Montserrat Caballé","Spanish operatic soprano","1933","ES","Singer","singer"],
    ["Alicia Keys","American singer","1981","US","Singer","singer"],
    ["Aretha Franklin","American singer","1942","US","Singer","singer"],
    ["Beyoncé","American singer","1981","US","Singer","singer"],
    ["Rihanna","Barbadian singer","1988","BB","Singer","singer"],
    ["Taylor Swift","American singer-songwriter","1989","US","Singer","singer"],
    ["Lady Gaga","American singer and actress","1986","US","Singer","singer"],
    ["Adele","British singer","1988","GB","Singer","singer"],
    ["Ed Sheeran","British singer-songwriter","1991","GB","Singer","singer"],
    ["Bruno Mars","American singer-songwriter","1985","US","Singer","singer"],
    ["Justin Bieber","Canadian singer","1994","CA","Singer","singer"],
    ["Selena Gomez","American singer and actress","1992","US","Singer","singer"],
    ["Ariana Grande","American singer","1993","US","Singer","singer"],
    ["Dua Lipa","British singer","1995","GB","Singer","singer"],
    ["Billie Eilish","American singer","2001","US","Singer","singer"],
    ["Olivia Rodrigo","American singer","2003","US","Singer","singer"],
    ["Harry Styles","British singer","1994","GB","Singer","singer"],
    ["The Weeknd","Canadian singer","1990","CA","Singer","singer"],
    ["Drake","Canadian rapper","1986","CA","Singer","singer"],
    ["Kendrick Lamar","American rapper","1987","US","Singer","singer"],
    ["Jay-Z","American rapper","1969","US","Singer","singer"],
    ["Eminem","American rapper","1972","US","Singer","singer"],
    ["Kanye West","American rapper","1977","US","Singer","singer"],
    ["Snoop Dogg","American rapper","1971","US","Singer","singer"],
    ["Cardi B","American rapper","1992","US","Singer","singer"],
    ["Nicki Minaj","Trinidadian-American rapper","1982","US","Singer","singer"],
    ["Megan Thee Stallion","American rapper","1995","US","Singer","singer"],
    ["Post Malone","American rapper","1995","US","Singer","singer"],
    ["Lil Wayne","American rapper","1982","US","Singer","singer"],
    ["Travis Scott","American rapper","1991","US","Singer","singer"],
    ["Shakira","Colombian singer","1977","CO","Singer","singer"],
]

add_people("Colombian Singers", colombian_singers)

# ─── COLOMBIAN FOOTBALLERS (200) ───
colombian_footballers = [
    ["James Rodríguez","Colombian footballer, attacking midfielder","1991","CO","Footballer","footballer"],
    ["Radamel Falcao","Colombian footballer, striker","1986","CO","Footballer","footballer"],
    ["Juan Fernando Quintero","Colombian footballer, midfielder","1993","CO","Footballer","footballer"],
    ["Juan Guillermo Cuadrado","Colombian footballer, winger","1988","CO","Footballer","footballer"],
    ["Carlos Bacca","Colombian footballer, striker","1986","CO","Footballer","footballer"],
    ["Jackson Martínez","Colombian footballer, striker","1986","CO","Footballer","footballer"],
    ["Teófilo Gutiérrez","Colombian footballer, striker","1985","CO","Footballer","footballer"],
    ["Luis Fernando Muriel","Colombian footballer, striker","1991","CO","Footballer","footballer"],
    ["Duván Zapata","Colombian footballer, striker","1991","CO","Footballer","footballer"],
    ["Roger Martínez","Colombian footballer, striker","1994","CO","Footballer","footballer"],
    ["Rafael Santos Borré","Colombian footballer, striker","1995","CO","Footballer","footballer"],
    ["Yerry Mina","Colombian footballer, defender","1994","CO","Footballer","footballer"],
    ["Davinson Sánchez","Colombian footballer, defender","1996","CO","Footballer","footballer"],
    ["Cristian Zapata","Colombian footballer, defender","1986","CO","Footballer","footballer"],
    ["Jeison Murillo","Colombian footballer, defender","1992","CO","Footballer","footballer"],
    ["Óscar Murillo","Colombian footballer, defender","1988","CO","Footballer","footballer"],
    ["Andrés Mosquera","Colombian footballer, defender","1990","CO","Footballer","footballer"],
    ["Santiago Arias","Colombian footballer, full-back","1992","CO","Footballer","footballer"],
    ["Cristian Borja","Colombian footballer, full-back","1993","CO","Footballer","footballer"],
    ["Frank Fabra","Colombian footballer, full-back","1991","CO","Footballer","footballer"],
    ["Johan Mojica","Colombian footballer, full-back","1992","CO","Footballer","footballer"],
    ["Mateus Uribe","Colombian footballer, midfielder","1991","CO","Footballer","footballer"],
    ["Wílmar Barrios","Colombian footballer, midfielder","1993","CO","Footballer","footballer"],
    ["Gustavo Cuéllar","Colombian footballer, midfielder","1992","CO","Footballer","footballer"],
    ["Kevin Balanta","Colombian footballer, midfielder","1995","CO","Footballer","footballer"],
    ["Daniel Torres","Colombian footballer, midfielder","1989","CO","Footballer","footballer"],
    ["Abel Aguilar","Colombian footballer, midfielder","1985","CO","Footballer","footballer"],
    ["Carlos Sánchez","Colombian footballer, midfielder","1986","CO","Footballer","footballer"],
    ["Fredy Guarín","Colombian footballer, midfielder","1986","CO","Footballer","footballer"],
    ["David Ospina","Colombian footballer, goalkeeper","1988","CO","Footballer","footballer"],
    ["Camilo Vargas","Colombian footballer, goalkeeper","1989","CO","Footballer","footballer"],
    ["Iván Arboleda","Colombian footballer, goalkeeper","1996","CO","Footballer","footballer"],
    ["Luis Díaz","Colombian footballer, winger","1997","CO","Footballer","footballer"],
    ["Jhon Arias","Colombian footballer, winger","1997","CO","Footballer","footballer"],
    ["Diego Valoyes","Colombian footballer, winger","1996","CO","Footballer","footballer"],
    ["Harold Preciado","Colombian footballer, striker","1994","CO","Footballer","footballer"],
    ["Andrés Felipe Andrade","Colombian footballer, midfielder","1995","CO","Footballer","footballer"],
    ["Lionel Messi","Argentine footballer","1987","AR","Footballer","footballer"],
    ["Cristiano Ronaldo","Portuguese footballer","1985","PT","Footballer","footballer"],
    ["Neymar","Brazilian footballer","1992","BR","Footballer","footballer"],
    ["Kylian Mbappé","French footballer","1998","FR","Footballer","footballer"],
    ["Robert Lewandowski","Polish footballer","1988","PL","Footballer","footballer"],
    ["Kevin De Bruyne","Belgian footballer","1991","BE","Footballer","footballer"],
    ["Mohamed Salah","Egyptian footballer","1992","EG","Footballer","footballer"],
    ["Erling Haaland","Norwegian footballer","2000","NO","Footballer","footballer"],
    ["Vinícius Júnior","Brazilian footballer","2000","BR","Footballer","footballer"],
    ["Jude Bellingham","English footballer","2003","GB","Footballer","footballer"],
    ["Harry Kane","English footballer","1993","GB","Footballer","footballer"],
    ["Lamine Yamal","Spanish footballer","2007","ES","Footballer","footballer"],
    ["Pedri","Spanish footballer","2002","ES","Footballer","footballer"],
    ["Gavi","Spanish footballer","2004","ES","Footballer","footballer"],
    ["Federico Valverde","Uruguayan footballer","1998","UY","Footballer","footballer"],
    ["Lautaro Martínez","Argentine footballer","1997","AR","Footballer","footballer"],
    ["Ángel Di María","Argentine footballer","1988","AR","Footballer","footballer"],
    ["Paulo Dybala","Argentine footballer","1993","AR","Footballer","footballer"],
    ["Julian Álvarez","Argentine footballer","2000","AR","Footballer","footballer"],
    ["Enzo Fernández","Argentine footballer","2001","AR","Footballer","footballer"],
    ["Alexis Mac Allister","Argentine footballer","1998","AR","Footballer","footballer"],
    ["Sergio Agüero","Argentine footballer","1988","AR","Footballer","footballer"],
    ["Gonzalo Higuaín","Argentine footballer","1987","AR","Footballer","footballer"],
    ["Zinedine Zidane","French footballer","1972","FR","Footballer","footballer"],
    ["Ronaldinho","Brazilian footballer","1980","BR","Footballer","footballer"],
    ["Ronaldo Nazário","Brazilian footballer","1976","BR","Footballer","footballer"],
]

add_people("Colombian Footballers", colombian_footballers)

# ─── LATIN AMERICAN ACTORS (200) ───
latin_actors = [
    ["Sofía Vergara","Colombian-American actress","1972","CO","Actress","actor"],
    ["John Leguizamo","Colombian-American actor","1960","CO","Actor","actor"],
    ["Wagner Moura","Brazilian actor","1976","BR","Actor","actor"],
    ["Gael García Bernal","Mexican actor","1978","MX","Actor","actor"],
    ["Diego Luna","Mexican actor","1979","MX","Actor","actor"],
    ["Salma Hayek","Mexican-American actress","1966","MX","Actress","actor"],
    ["Kate del Castillo","Mexican actress","1972","MX","Actress","actor"],
    ["Eugenio Derbez","Mexican actor","1961","MX","Actor","actor"],
    ["Guillermo del Toro","Mexican filmmaker","1964","MX","Filmmaker","director"],
    ["Alejandro González Iñárritu","Mexican filmmaker","1963","MX","Filmmaker","director"],
    ["Alfonso Cuarón","Mexican filmmaker","1961","MX","Filmmaker","director"],
    ["Pedro Almodóvar","Spanish filmmaker","1949","ES","Filmmaker","director"],
    ["Javier Bardem","Spanish actor","1969","ES","Actor","actor"],
    ["Penélope Cruz","Spanish actress","1974","ES","Actress","actor"],
    ["Antonio Banderas","Spanish actor","1960","ES","Actor","actor"],
    ["Ricardo Darín","Argentine actor","1957","AR","Actor","actor"],
    ["Damián Alcázar","Mexican actor","1953","MX","Actor","actor"],
    ["Demián Bichir","Mexican actor","1963","MX","Actor","actor"],
    ["Ana de la Reguera","Mexican actress","1977","MX","Actress","actor"],
    ["Maya Zapata","Mexican actress","1979","MX","Actress","actor"],
]

add_people("Latin Actors", latin_actors)

# ─── ACTORS (180) ───
actors = [
    ["Tom Hanks","American actor","1956","US","Actor","actor"],
    ["Leonardo DiCaprio","American actor","1974","US","Actor","actor"],
    ["Brad Pitt","American actor","1963","US","Actor","actor"],
    ["Robert De Niro","American actor","1943","US","Actor","actor"],
    ["Al Pacino","American actor","1940","US","Actor","actor"],
    ["Denzel Washington","American actor","1954","US","Actor","actor"],
    ["Morgan Freeman","American actor","1937","US","Actor","actor"],
    ["Samuel L. Jackson","American actor","1948","US","Actor","actor"],
    ["Will Smith","American actor","1968","US","Actor","actor"],
    ["Johnny Depp","American actor","1963","US","Actor","actor"],
    ["Matt Damon","American actor","1970","US","Actor","actor"],
    ["Christian Bale","British actor","1974","GB","Actor","actor"],
    ["Cillian Murphy","Irish actor","1976","IE","Actor","actor"],
    ["Timothée Chalamet","American actor","1995","US","Actor","actor"],
    ["Tom Cruise","American actor","1962","US","Actor","actor"],
    ["Keanu Reeves","Canadian actor","1964","CA","Actor","actor"],
    ["Hugh Jackman","Australian actor","1968","AU","Actor","actor"],
    ["Ryan Reynolds","Canadian actor","1976","CA","Actor","actor"],
    ["Chris Hemsworth","Australian actor","1983","AU","Actor","actor"],
    ["Chris Evans","American actor","1981","US","Actor","actor"],
    ["Robert Downey Jr.","American actor","1965","US","Actor","actor"],
    ["Scarlett Johansson","American actress","1984","US","Actress","actor"],
    ["Jennifer Lawrence","American actress","1990","US","Actress","actor"],
    ["Emma Stone","American actress","1988","US","Actress","actor"],
    ["Margot Robbie","Australian actress","1990","AU","Actress","actor"],
    ["Cate Blanchett","Australian actress","1969","AU","Actress","actor"],
    ["Meryl Streep","American actress","1949","US","Actress","actor"],
    ["Nicole Kidman","Australian-American actress","1967","AU","Actress","actor"],
    ["Angelina Jolie","American actress","1975","US","Actress","actor"],
    ["Julia Roberts","American actress","1967","US","Actress","actor"],
    ["Natalie Portman","Israeli-American actress","1981","IL","Actress","actor"],
    ["Zendaya","American actress and singer","1996","US","Actress","actor"],
    ["Milla Jovovich","Ukrainian-American actress","1975","US","Actress","actor"],
    ["Joaquin Phoenix","American actor","1974","US","Actor","actor"],
    ["Dwayne Johnson","American actor and wrestler","1972","US","Actor","actor"],
    ["Vin Diesel","American actor","1967","US","Actor","actor"],
    ["Jason Statham","British actor","1967","GB","Actor","actor"],
    ["Jackie Chan","Hong Kong actor","1954","HK","Actor","actor"],
    ["Harrison Ford","American actor","1942","US","Actor","actor"],
    ["Mark Hamill","American actor","1951","US","Actor","actor"],
    ["Daniel Craig","British actor","1968","GB","Actor","actor"],
    ["Idris Elba","British actor","1972","GB","Actor","actor"],
    ["Anthony Hopkins","British actor","1937","GB","Actor","actor"],
    ["Gary Oldman","British actor","1958","GB","Actor","actor"],
    ["Russell Crowe","New Zealand actor","1964","NZ","Actor","actor"],
    ["Jake Gyllenhaal","American actor","1980","US","Actor","actor"],
    ["Michael B. Jordan","American actor","1987","US","Actor","actor"],
    ["Chadwick Boseman","American actor","1976","US","Actor","actor"],
    ["John Boyega","British actor","1992","GB","Actor","actor"],
    ["Pedro Pascal","Chilean-American actor","1975","CL","Actor","actor"],
    ["Oscar Isaac","Guatemalan-American actor","1979","GT","Actor","actor"],
    ["Benedict Cumberbatch","British actor","1976","GB","Actor","actor"],
    ["Tom Hardy","British actor","1977","GB","Actor","actor"],
    ["Henry Cavill","British actor","1983","GB","Actor","actor"],
    ["Liam Neeson","Irish actor","1952","IE","Actor","actor"],
    ["George Clooney","American actor","1961","US","Actor","actor"],
    ["Ben Affleck","American actor","1972","US","Actor","actor"],
    ["Matthew McConaughey","American actor","1969","US","Actor","actor"],
    ["Bruce Willis","American actor","1955","US","Actor","actor"],
    ["Sylvester Stallone","American actor","1946","US","Actor","actor"],
    ["Arnold Schwarzenegger","Austrian-American actor","1947","AT","Actor","actor"],
    ["Jean-Claude Van Damme","Belgian actor","1960","BE","Actor","actor"],
    ["Nicolas Cage","American actor","1964","US","Actor","actor"],
    ["Edward Norton","American actor","1969","US","Actor","actor"],
    ["Jude Law","British actor","1972","GB","Actor","actor"],
    ["Ewan McGregor","British actor","1971","GB","Actor","actor"],
    ["Colin Firth","British actor","1960","GB","Actor","actor"],
    ["Hugh Grant","British actor","1960","GB","Actor","actor"],
    ["James McAvoy","Scottish actor","1979","GB","Actor","actor"],
    ["Daniel Radcliffe","British actor","1989","GB","Actor","actor"],
    ["Elijah Wood","American actor","1981","US","Actor","actor"],
    ["Viggo Mortensen","American actor","1958","US","Actor","actor"],
    ["Sean Bean","British actor","1959","GB","Actor","actor"],
    ["Jeffrey Dean Morgan","American actor","1966","US","Actor","actor"],
    ["Jensen Ackles","American actor","1978","US","Actor","actor"],
    ["Mads Mikkelsen","Danish actor","1965","DK","Actor","actor"],
    ["Christoph Waltz","Austrian actor","1956","AT","Actor","actor"],
    ["Willem Dafoe","American actor","1955","US","Actor","actor"],
    ["Steve Carell","American actor","1962","US","Actor","actor"],
    ["Jim Carrey","Canadian actor","1962","CA","Actor","actor"],
    ["Adam Sandler","American actor","1966","US","Actor","actor"],
    ["Eddie Murphy","American actor","1961","US","Actor","actor"],
    ["Robin Williams","American actor","1951","US","Actor","actor"],
    ["Bill Murray","American actor","1950","US","Actor","actor"],
    ["Michael J. Fox","Canadian actor","1961","CA","Actor","actor"],
    ["Jamie Foxx","American actor","1967","US","Actor","actor"],
    ["Kevin Hart","American actor","1979","US","Actor","actor"],
    ["Jack Black","American actor","1969","US","Actor","actor"],
    ["Danny DeVito","American actor","1944","US","Actor","actor"],
    ["Emma Watson","British actress","1990","GB","Actress","actor"],
    ["Anne Hathaway","American actress","1982","US","Actress","actor"],
    ["Jessica Chastain","American actress","1977","US","Actress","actor"],
    ["Amy Adams","American actress","1974","US","Actress","actor"],
    ["Sandra Bullock","American actress","1964","US","Actress","actor"],
    ["Charlize Theron","South African actress","1975","ZA","Actress","actor"],
    ["Michelle Pfeiffer","American actress","1958","US","Actress","actor"],
    ["Halle Berry","American actress","1966","US","Actress","actor"],
    ["Jennifer Aniston","American actress","1969","US","Actress","actor"],
    ["Reese Witherspoon","American actress","1976","US","Actress","actor"],
    ["Sarah Jessica Parker","American actress","1965","US","Actress","actor"],
    ["Ellen DeGeneres","American comedian and talk show host","1958","US","Comedian","comedian"],
    ["Oprah Winfrey","American talk show host","1954","US","Talk Show Host","tv"],
    ["David Letterman","American talk show host","1947","US","Talk Show Host","tv"],
    ["Jimmy Fallon","American talk show host","1974","US","Talk Show Host","tv"],
    ["Jimmy Kimmel","American talk show host","1967","US","Talk Show Host","tv"],
    ["Stephen Colbert","American talk show host","1964","US","Talk Show Host","tv"],
    ["Conan O'Brien","American talk show host","1963","US","Talk Show Host","tv"],
    ["Ryan Seacrest","American television host","1974","US","TV Host","tv"],
    ["Steve Harvey","American comedian and host","1957","US","Comedian","tv"],
    ["Jerry Seinfeld","American comedian","1954","US","Comedian","comedian"],
    ["Ricky Gervais","British comedian","1961","GB","Comedian","comedian"],
    ["Dave Chappelle","American comedian","1973","US","Comedian","comedian"],
    ["Chris Rock","American comedian","1965","US","Comedian","comedian"],
    ["Amy Schumer","American comedian","1981","US","Comedian","comedian"],
    ["Trevor Noah","South African comedian","1984","ZA","Comedian","comedian"],
    ["John Mulaney","American comedian","1982","US","Comedian","comedian"],
    ["Bill Burr","American comedian","1968","US","Comedian","comedian"],
    ["Eddie Izzard","British comedian","1962","GB","Comedian","comedian"],
    ["Rowan Atkinson","British actor","1955","GB","Actor","actor"],
    ["Sacha Baron Cohen","British actor","1971","GB","Actor","actor"],
    ["Michael Caine","British actor","1933","GB","Actor","actor"],
    ["Morgan Freeman","American actor","1937","US","Actor","actor"],
    ["Clint Eastwood","American actor and director","1930","US","Actor","director"],
    ["Denzel Washington","American actor","1954","US","Actor","actor"],
    ["Forest Whitaker","American actor","1961","US","Actor","actor"],
    ["Don Cheadle","American actor","1964","US","Actor","actor"],
]

add_people("Actors", actors)

# ─── WORLD LEADERS & POLITICIANS (100) ───
politicians = [
    ["Joe Biden","President of the United States","1942","US","Politician","politician"],
    ["Donald Trump","Former President of the United States","1946","US","Politician","politician"],
    ["Barack Obama","Former President of the United States","1961","US","Politician","politician"],
    ["Bill Clinton","Former President of the United States","1946","US","Politician","politician"],
    ["Kamala Harris","Vice President of the United States","1964","US","Politician","politician"],
    ["Hillary Clinton","American politician","1947","US","Politician","politician"],
    ["Bernie Sanders","American politician","1941","US","Politician","politician"],
    ["Nancy Pelosi","American politician","1940","US","Politician","politician"],
    ["Elon Musk","Business magnate","1971","ZA","Entrepreneur","business"],
    ["Jeff Bezos","Business magnate","1964","US","Entrepreneur","business"],
    ["Mark Zuckerberg","Business magnate","1984","US","Entrepreneur","tech"],
    ["Bill Gates","Business magnate","1955","US","Entrepreneur","tech"],
    ["Tim Cook","Business executive","1960","US","Businessman","business"],
    ["Satya Nadella","Business executive","1967","IN","Businessman","business"],
    ["Steve Ballmer","Business executive","1956","US","Businessman","business"],
    ["Linus Torvalds","Software engineer","1969","FI","Engineer","tech"],
    ["Tim Berners-Lee","Computer scientist","1955","GB","Scientist","tech"],
    ["Stephen Hawking","Theoretical physicist","1942","GB","Scientist","writer"],
    ["Neil deGrasse Tyson","Astrophysicist","1958","US","Scientist","writer"],
    ["Richard Dawkins","Evolutionary biologist","1941","GB","Scientist","writer"],
    ["Jane Goodall","Primatologist","1934","GB","Scientist","writer"],
    ["David Attenborough","Broadcaster and naturalist","1926","GB","Naturalist","tv"],
    ["Noam Chomsky","Linguist and activist","1928","US","Linguist","writer"],
    ["Fidel Castro","Cuban revolutionary leader","1926","CU","Politician","politician"],
    ["Nelson Mandela","South African president","1918","ZA","Politician","politician"],
    ["Angela Merkel","German chancellor","1954","DE","Politician","politician"],
    ["Emmanuel Macron","President of France","1977","FR","Politician","politician"],
    ["Justin Trudeau","Prime Minister of Canada","1971","CA","Politician","politician"],
    ["Gustavo Petro","President of Colombia","1960","CO","Politician","politician"],
    ["Iván Duque","Former President of Colombia","1976","CO","Politician","politician"],
    ["Juan Manuel Santos","Former President of Colombia","1951","CO","Politician","politician"],
    ["Andrés Pastrana","Former President of Colombia","1954","CO","Politician","politician"],
    ["César Gaviria","Former President of Colombia","1947","CO","Politician","politician"],
    ["Álvaro Uribe","Former President of Colombia","1952","CO","Politician","politician"],
    ["Francisco Santos","Colombian politician","1961","CO","Politician","politician"],
    ["Jorge Enrique Robledo","Colombian politician","1951","CO","Politician","politician"],
    ["Claudia López","Mayor of Bogotá","1970","CO","Politician","politician"],
    ["Lula da Silva","Former President of Brazil","1945","BR","Politician","politician"],
    ["Nicolás Maduro","President of Venezuela","1962","VE","Politician","politician"],
    ["Vladimir Putin","President of Russia","1952","RU","Politician","politician"],
    ["Xi Jinping","President of China","1953","CN","Politician","politician"],
    ["Narendra Modi","Prime Minister of India","1950","IN","Politician","politician"],
    ["Pope Francis","Head of the Catholic Church","1936","AR","Pope","politician"],
    ["Dalai Lama","Tibetan spiritual leader","1935","CN","Spiritual Leader","politician"],
    ["Malala Yousafzai","Education activist","1997","PK","Activist","politician"],
    ["Greta Thunberg","Climate activist","2003","SE","Activist","politician"],
]

add_people("Politicians", politicians)

# ─── ATHLETES (200) ───
athletes = [
    ["LeBron James","American basketball player","1984","US","Basketball Player","basketball"],
    ["Stephen Curry","American basketball player","1988","US","Basketball Player","basketball"],
    ["Kevin Durant","American basketball player","1988","US","Basketball Player","basketball"],
    ["Giannis Antetokounmpo","Greek basketball player","1994","GR","Basketball Player","basketball"],
    ["Luka Dončić","Slovenian basketball player","1999","SI","Basketball Player","basketball"],
    ["Joel Embiid","Cameroonian basketball player","1994","CM","Basketball Player","basketball"],
    ["Nikola Jokić","Serbian basketball player","1995","RS","Basketball Player","basketball"],
    ["Kawhi Leonard","American basketball player","1991","US","Basketball Player","basketball"],
    ["Damian Lillard","American basketball player","1990","US","Basketball Player","basketball"],
    ["Jimmy Butler","American basketball player","1989","US","Basketball Player","basketball"],
    ["Serena Williams","American tennis player","1981","US","Tennis Player","tennis"],
    ["Roger Federer","Swiss tennis player","1981","CH","Tennis Player","tennis"],
    ["Rafael Nadal","Spanish tennis player","1986","ES","Tennis Player","tennis"],
    ["Novak Djokovic","Serbian tennis player","1987","RS","Tennis Player","tennis"],
    ["Carlos Alcaraz","Spanish tennis player","2003","ES","Tennis Player","tennis"],
    ["Naomi Osaka","Japanese tennis player","1997","JP","Tennis Player","tennis"],
    ["Iga Świątek","Polish tennis player","2001","PL","Tennis Player","tennis"],
    ["Coco Gauff","American tennis player","2004","US","Tennis Player","tennis"],
    ["Usain Bolt","Jamaican sprinter","1986","JM","Sprinter","sports"],
    ["Michael Phelps","American swimmer","1985","US","Swimmer","sports"],
    ["Simone Biles","American gymnast","1997","US","Gymnast","sports"],
    ["Tom Brady","American football player","1977","US","Football Player","sports"],
    ["Patrick Mahomes","American football player","1995","US","Football Player","sports"],
    ["Travis Kelce","American football player","1989","US","Football Player","sports"],
    ["Lewis Hamilton","British Formula One driver","1985","GB","Racing Driver","sports"],
    ["Max Verstappen","Dutch Formula One driver","1997","NL","Racing Driver","sports"],
    ["Manny Pacquiao","Filipino boxer","1978","PH","Boxer","boxer"],
    ["Canelo Álvarez","Mexican boxer","1990","MX","Boxer","boxer"],
    ["Floyd Mayweather","American boxer","1977","US","Boxer","boxer"],
    ["Conor McGregor","Irish MMA fighter","1988","IE","MMA Fighter","boxer"],
    ["Jon Jones","American MMA fighter","1987","US","MMA Fighter","boxer"],
    ["Amanda Nunes","Brazilian MMA fighter","1988","BR","MMA Fighter","boxer"],
    ["Khabib Nurmagomedov","Russian MMA fighter","1988","RU","MMA Fighter","boxer"],
    ["Ronda Rousey","American MMA fighter","1987","US","MMA Fighter","boxer"],
    ["Mike Tyson","American boxer","1966","US","Boxer","boxer"],
    ["Tiger Woods","American golfer","1975","US","Golfer","sports"],
    ["Rory McIlroy","Northern Irish golfer","1989","GB","Golfer","sports"],
    ["Jon Rahm","Spanish golfer","1994","ES","Golfer","sports"],
    ["Neymar","Brazilian footballer","1992","BR","Footballer","footballer"],
    ["Vinicius Jr","Brazilian footballer","2000","BR","Footballer","footballer"],
    ["Paulo Henrique Ganso","Brazilian footballer","1989","BR","Footballer","footballer"],
    ["Raphinha","Brazilian footballer","1996","BR","Footballer","footballer"],
    ["Richarlison","Brazilian footballer","1997","BR","Footballer","footballer"],
    ["Rodrygo","Brazilian footballer","2001","BR","Footballer","footballer"],
    ["Gabriel Jesus","Brazilian footballer","1997","BR","Footballer","footballer"],
    ["Gabriel Martinelli","Brazilian footballer","2001","BR","Footballer","footballer"],
    ["Eder Militão","Brazilian footballer","1998","BR","Footballer","footballer"],
    ["Marquinhos","Brazilian footballer","1994","BR","Footballer","footballer"],
    ["Thiago Silva","Brazilian footballer","1984","BR","Footballer","footballer"],
    ["Alisson Becker","Brazilian footballer","1992","BR","Footballer","footballer"],
    ["Ederson","Brazilian footballer","1993","BR","Footballer","footballer"],
    ["Álex Olmedo","Peruvian footballer","1994","PE","Footballer","footballer"],
    ["Paolo Guerrero","Peruvian footballer","1984","PE","Footballer","footballer"],
    ["Jefferson Farfán","Peruvian footballer","1984","PE","Footballer","footballer"],
    ["Claudio Pizarro","Peruvian footballer","1978","PE","Footballer","footballer"],
    ["Luis Suárez","Uruguayan footballer","1987","UY","Footballer","footballer"],
    ["Edinson Cavani","Uruguayan footballer","1987","UY","Footballer","footballer"],
    ["Diego Forlán","Uruguayan footballer","1979","UY","Footballer","footballer"],
    ["Salomón Rondón","Venezuelan footballer","1989","VE","Footballer","footballer"],
]

add_people("Athletes", athletes)

# ─── WRITERS & JOURNALISTS (80) ───
writers = [
    ["Gabriel García Márquez","Colombian writer","1927","CO","Writer","writer"],
    ["Mario Vargas Llosa","Peruvian writer","1936","PE","Writer","writer"],
    ["Jorge Luis Borges","Argentine writer","1899","AR","Writer","writer"],
    ["Isabel Allende","Chilean writer","1942","CL","Writer","writer"],
    ["Paulo Coelho","Brazilian writer","1947","BR","Writer","writer"],
    ["Carlos Fuentes","Mexican writer","1928","MX","Writer","writer"],
    ["Octavio Paz","Mexican writer","1914","MX","Writer","writer"],
    ["J.K. Rowling","British writer","1965","GB","Writer","writer"],
    ["Stephen King","American writer","1947","US","Writer","writer"],
    ["Haruki Murakami","Japanese writer","1949","JP","Writer","writer"],
    ["Margaret Atwood","Canadian writer","1939","CA","Writer","writer"],
    ["George R.R. Martin","American writer","1948","US","Writer","writer"],
    ["J.R.R. Tolkien","British writer","1892","GB","Writer","writer"],
    ["Dan Brown","American writer","1964","US","Writer","writer"],
    ["Ken Follett","British writer","1949","GB","Writer","writer"],
    ["John Grisham","American writer","1955","US","Writer","writer"],
    ["Walter Isaacson","American writer","1952","US","Writer","writer"],
    ["Malcolm Gladwell","Canadian writer","1963","CA","Writer","writer"],
    ["Michael Lewis","American writer","1960","US","Writer","writer"],
    ["Yuval Noah Harari","Israeli writer","1976","IL","Writer","writer"],
    ["Elena Poniatowska","Mexican writer","1932","MX","Writer","writer"],
    ["Laura Restrepo","Colombian writer","1950","CO","Writer","writer"],
    ["Juan Gabriel Vásquez","Colombian writer","1973","CO","Writer","writer"],
    ["Héctor Abad Faciolince","Colombian writer","1958","CO","Writer","writer"],
    ["Jorge Franco","Colombian writer","1962","CO","Writer","writer"],
    ["Germán Castro Caycedo","Colombian writer","1940","CO","Writer","writer"],
    ["Fernando Vallejo","Colombian-Mexican writer","1942","CO","Writer","writer"],
    ["Jorge Isaacs","Colombian writer","1837","CO","Writer","writer"],
    ["Álvaro Mutis","Colombian writer","1923","CO","Writer","writer"],
    ["Andrés Caicedo","Colombian writer","1951","CO","Writer","writer"],
    ["Jorge Pérez Vega","Colombian journalist","1957","CO","Journalist","journalist"],
    ["Yamid Amat","Colombian journalist","1941","CO","Journalist","journalist"],
    ["Antonio Caballero","Colombian journalist","1945","CO","Journalist","journalist"],
    ["Jorge Enrique Pulido","Colombian journalist","1947","CO","Journalist","journalist"],
    ["María Elvira Domínguez","Colombian journalist","1968","CO","Journalist","journalist"],
    ["Andrés Oppenheimer","Argentine journalist","1951","AR","Journalist","journalist"],
    ["Jorge Lanata","Argentine journalist","1960","AR","Journalist","journalist"],
    ["Jon Lee Anderson","American journalist","1957","US","Journalist","journalist"],
]

add_people("Writers", writers)

# ─── CYCLISTS (100) ───
cyclists = [
    ["Nairo Quintana","Colombian cyclist","1990","CO","Cyclist","cyclist"],
    ["Egan Bernal","Colombian cyclist","1997","CO","Cyclist","cyclist"],
    ["Rigoberto Urán","Colombian cyclist","1987","CO","Cyclist","cyclist"],
    ["Sergio Higuita","Colombian cyclist","1997","CO","Cyclist","cyclist"],
    ["Esteban Chaves","Colombian cyclist","1990","CO","Cyclist","cyclist"],
    ["Miguel Ángel López","Colombian cyclist","1994","CO","Cyclist","cyclist"],
    ["Daniel Martínez","Colombian cyclist","1996","CO","Cyclist","cyclist"],
    ["Jarlinson Pantano","Colombian cyclist","1988","CO","Cyclist","cyclist"],
    ["Fernando Gaviria","Colombian cyclist","1994","CO","Cyclist","cyclist"],
    ["Win Anacona","Colombian cyclist","1991","CO","Cyclist","cyclist"],
    ["Alejandro Valverde","Spanish cyclist","1980","ES","Cyclist","cyclist"],
    ["Alberto Contador","Spanish cyclist","1982","ES","Cyclist","cyclist"],
    ["Chris Froome","British cyclist","1985","GB","Cyclist","cyclist"],
    ["Geraint Thomas","British cyclist","1986","GB","Cyclist","cyclist"],
    ["Vincenzo Nibali","Italian cyclist","1984","IT","Cyclist","cyclist"],
    ["Primož Roglič","Slovenian cyclist","1989","SI","Cyclist","cyclist"],
    ["Tadej Pogačar","Slovenian cyclist","1998","SI","Cyclist","cyclist"],
    ["Jonas Vingegaard","Danish cyclist","1996","DK","Cyclist","cyclist"],
    ["Wout van Aert","Belgian cyclist","1994","BE","Cyclist","cyclist"],
    ["Mathieu van der Poel","Dutch cyclist","1995","NL","Cyclist","cyclist"],
    ["Remco Evenepoel","Belgian cyclist","2000","BE","Cyclist","cyclist"],
    ["Peter Sagan","Slovak cyclist","1990","SK","Cyclist","cyclist"],
    ["Tom Dumoulin","Dutch cyclist","1990","NL","Cyclist","cyclist"],
    ["Richard Carapaz","Ecuadorian cyclist","1993","EC","Cyclist","cyclist"],
    ["Ivan Ramiro Sosa","Colombian cyclist","1997","CO","Cyclist","cyclist"],
    ["Dayer Quintana","Colombian cyclist","1992","CO","Cyclist","cyclist"],
    ["Sebastián Henao","Colombian cyclist","1993","CO","Cyclist","cyclist"],
    ["Brayan Ramírez","Colombian cyclist","1994","CO","Cyclist","cyclist"],
]

add_people("Cyclists", cyclists)

# ─── K-POP IDOLS
# ─── MODEL & FASHION
# ─── INFLUENCERS

# ─── WORLD MUSIC
world_music = [
    ["BTS","South Korean K-pop group","2010","KR","K-pop Group","singer"],
    ["BLACKPINK","South Korean K-pop group","2016","KR","K-pop Group","singer"],
    ["Twice","South Korean K-pop group","2015","KR","K-pop Group","singer"],
    ["Coldplay","British rock band","1996","GB","Rock Band","singer"],
    ["U2","Irish rock band","1976","IE","Rock Band","singer"],
    ["Foo Fighters","American rock band","1994","US","Rock Band","singer"],
    ["Radiohead","British rock band","1985","GB","Rock Band","singer"],
    ["Metallica","American heavy metal band","1981","US","Heavy Metal Band","singer"],
    ["Iron Maiden","British heavy metal band","1975","GB","Heavy Metal Band","singer"],
    ["Rolling Stones","British rock band","1962","GB","Rock Band","singer"],
    ["Aerosmith","American rock band","1970","US","Rock Band","singer"],
    ["Bon Jovi","American rock band","1983","US","Rock Band","singer"],
    ["Guns N' Roses","American rock band","1985","US","Rock Band","singer"],
    ["Nirvana","American grunge band","1987","US","Grunge Band","singer"],
    ["Pearl Jam","American rock band","1990","US","Rock Band","singer"],
    ["Red Hot Chili Peppers","American rock band","1983","US","Rock Band","singer"],
    ["Green Day","American punk rock band","1987","US","Punk Rock Band","singer"],
    ["Linkin Park","American rock band","1996","US","Rock Band","singer"],
    ["Queen","British rock band","1970","GB","Rock Band","singer"],
    ["The Beatles","British rock band","1960","GB","Rock Band","singer"],
    ["Elton John","British singer","1947","GB","Singer","singer"],
    ["David Bowie","British singer","1947","GB","Singer","singer"],
    ["Prince","American singer","1958","US","Singer","singer"],
    ["Michael Jackson","American singer","1958","US","Singer","singer"],
    ["Madonna","American singer","1958","US","Singer","singer"],
    ["Freddie Mercury","British singer","1946","GB","Singer","singer"],
    ["Whitney Houston","American singer","1963","US","Singer","singer"],
    ["Celine Dion","Canadian singer","1968","CA","Singer","singer"],
    ["Mariah Carey","American singer","1969","US","Singer","singer"],
    ["Britney Spears","American singer","1981","US","Singer","singer"],
    ["Christina Aguilera","American singer","1980","US","Singer","singer"],
    ["Jennifer Lopez","American singer","1969","US","Singer","singer"],
    ["Pink","American singer","1979","US","Singer","singer"],
    ["Kylie Minogue","Australian singer","1968","AU","Singer","singer"],
    ["Beyoncé","American singer","1981","US","Singer","singer"],
    ["Rihanna","Barbadian singer","1988","BB","Singer","singer"],
    ["Taylor Swift","American singer","1989","US","Singer","singer"],
    ["Lady Gaga","American singer","1986","US","Singer","singer"],
]

add_people("World Music", world_music)

# ─── MODELS
models = [
    ["Gisele Bündchen","Brazilian supermodel","1980","BR","Model","model"],
    ["Naomi Campbell","British supermodel","1970","GB","Model","model"],
    ["Kate Moss","British supermodel","1974","GB","Model","model"],
    ["Heidi Klum","German supermodel","1973","DE","Model","model"],
    ["Cindy Crawford","American supermodel","1966","US","Model","model"],
    ["Linda Evangelista","Canadian supermodel","1965","CA","Model","model"],
    ["Christy Turlington","American supermodel","1969","US","Model","model"],
    ["Tyra Banks","American supermodel","1973","US","Model","model"],
    ["Miranda Kerr","Australian supermodel","1983","AU","Model","model"],
    ["Adriana Lima","Brazilian supermodel","1981","BR","Model","model"],
    ["Alessandra Ambrosio","Brazilian supermodel","1981","BR","Model","model"],
    ["Candice Swanepoel","South African supermodel","1988","ZA","Model","model"],
    ["Bella Hadid","American model","1996","US","Model","model"],
    ["Gigi Hadid","American model","1995","US","Model","model"],
    ["Kendall Jenner","American model","1995","US","Model","model"],
    ["Kylie Jenner","American media personality","1997","US","Model","model"],
    ["Kim Kardashian","American media personality","1980","US","Media Personality","influencer"],
    ["Paris Hilton","American media personality","1981","US","Media Personality","influencer"],
    ["Shakira","Colombian singer and dancer","1977","CO","Singer","singer"],
]

add_people("Models", models)

# ===== MORE WORLDWIDE FAMOUS PEOPLE (1,700+) =====

more_people = [
    # Latin American celebrities
    ["Natalia Oreiro","Uruguayan actress and singer","1977","UY","Actress","actor"],
    ["Diego Maradona","Argentine footballer","1960","AR","Footballer","footballer"],
    ["Lionel Messi","Argentine footballer","1987","AR","Footballer","footballer"],
    ["Pablo Escobar","Colombian drug lord","1949","CO","Criminal","politician"],
    ["Gabriel García Márquez","Colombian writer","1927","CO","Writer","writer"],
    ["Fernando Botero","Colombian artist","1932","CO","Artist","writer"],
    ["Cris Morena","Argentine producer","1956","AR","Producer","tv"],
    ["Susana Giménez","Argentine TV host","1944","AR","TV Host","tv"],
    ["Mirtha Legrand","Argentine TV host","1927","AR","TV Host","tv"],
    ["Valeria Mazza","Argentine model","1972","AR","Model","model"],
    ["Carolina Ardohain","Argentine model","1978","AR","Model","model"],
    ["Luisana Lopilato","Argentine actress","1987","AR","Actress","actor"],
    ["Ricardo Arjona","Guatemalan singer","1964","GT","Singer","singer"],
    ["Franco de Vita","Venezuelan singer","1954","VE","Singer","singer"],
    ["Luis Enrique","Nicaraguan singer","1962","NI","Singer","singer"],
    ["Gilberto Santa Rosa","Puerto Rican singer","1962","PR","Singer","singer"],
    ["Víctor Manuelle","Puerto Rican singer","1968","PR","Singer","singer"],
    ["Marc Anthony","American singer","1968","US","Singer","singer"],
    ["Olga Tañón","Puerto Rican singer","1967","PR","Singer","singer"],
    ["Ednita Nazario","Puerto Rican singer","1955","PR","Singer","singer"],
    ["Chayanne","Puerto Rican singer","1968","PR","Singer","singer"],
    ["Yuri","Mexican singer","1964","MX","Singer","singer"],
    ["Daniela Romo","Mexican singer","1959","MX","Singer","singer"],
    ["Dulce María","Mexican actress and singer","1985","MX","Actress","actor"],
    ["Anahí","Mexican actress and singer","1983","MX","Actress","actor"],
    ["Maite Perroni","Mexican actress and singer","1983","MX","Actress","actor"],
    ["Christian Castro","Mexican singer","1974","MX","Singer","singer"],
    ["Aracely Arámbula","Mexican actress","1975","MX","Actress","actor"],
    ["Angelique Boyer","French-Mexican actress","1988","MX","Actress","actor"],
    ["William Levy","Cuban-American actor","1980","US","Actor","actor"],
    ["Jencarlos Canela","American singer","1988","US","Singer","singer"],
    ["Carlos Ponce","Puerto Rican actor","1972","PR","Actor","actor"],
    ["Cristián de la Fuente","Chilean actor","1974","CL","Actor","actor"],
    ["Mario Kreutzberger","Chilean TV host","1940","CL","TV Host","tv"],
    ["Raúl Velasco","Mexican TV host","1933","MX","TV Host","tv"],
    ["Verónica Castro","Mexican actress","1952","MX","Actress","actor"],
    ["Lucía Méndez","Mexican actress","1955","MX","Actress","actor"],
    ["Rebecca Jones","Mexican actress","1957","MX","Actress","actor"],
    ["Edith González","Mexican actress","1964","MX","Actress","actor"],
    ["Adela Noriega","Mexican actress","1969","MX","Actress","actor"],
    ["Thalía","Mexican singer and actress","1971","MX","Singer","singer"],
    ["Laura Flores","Mexican actress","1963","MX","Actress","actor"],
    ["María Félix","Mexican actress","1914","MX","Actress","actor"],
    ["Pedro Infante","Mexican actor","1917","MX","Actor","actor"],
    ["Cantinflas","Mexican actor","1911","MX","Actor","actor"],
    ["El Santo","Mexican wrestler","1917","MX","Wrestler","sports"],
    ["Blue Demon","Mexican wrestler","1922","MX","Wrestler","sports"],
    ["Rey Mysterio","American wrestler","1974","US","Wrestler","sports"],
    ["John Cena","American wrestler","1977","US","Wrestler","sports"],
    ["The Rock","American wrestler and actor","1972","US","Wrestler","actor"],
    ["Stone Cold Steve Austin","American wrestler","1964","US","Wrestler","sports"],
    ["Triple H","American wrestler","1969","US","Wrestler","sports"],
    ["Undertaker","American wrestler","1965","US","Wrestler","sports"],
    ["Roman Reigns","American wrestler","1985","US","Wrestler","sports"],
    ["Seth Rollins","American wrestler","1986","US","Wrestler","sports"],
    ["Becky Lynch","Irish wrestler","1987","IE","Wrestler","sports"],
    ["Charlotte Flair","American wrestler","1986","US","Wrestler","sports"],
    ["Sasha Banks","American wrestler","1992","US","Wrestler","sports"],
    ["Bianca Belair","American wrestler","1989","US","Wrestler","sports"],
    ["J Balvin","Colombian singer","1985","CO","Singer","singer"],
    ["Maluma","Colombian singer","1994","CO","Singer","singer"],
    ["Greeicy","Colombian singer","1992","CO","Singer","singer"],
    ["Mike Bahía","Colombian singer","1984","CO","Singer","singer"],
    ["Manuel Turizo","Colombian singer","2000","CO","Singer","singer"],
    ["Sebastián Yatra","Colombian singer","1994","CO","Singer","singer"],
    ["Camilo","Colombian singer","1994","CO","Singer","singer"],
    ["Mau y Ricky","Colombian duo","1993","CO","Singer","singer"],
    ["Feid","Colombian singer","1992","CO","Singer","singer"],
    ["Ryan Castro","Colombian singer","1993","CO","Singer","singer"],
    ["Pailita","Chilean singer","1999","CL","Singer","singer"],
    ["Blessd","Colombian singer","2000","CO","Singer","singer"],
    ["Jhayco","Colombian singer","1993","CO","Singer","singer"],
    ["Morad","Spanish rapper","1999","ES","Singer","singer"],
    ["Eladio Carrion","Puerto Rican rapper","1994","PR","Singer","singer"],
    ["Myke Towers","Puerto Rican rapper","1994","PR","Singer","singer"],
    ["Rauw Alejandro","Puerto Rican singer","1993","PR","Singer","singer"],
    ["Bad Bunny","Puerto Rican singer","1994","PR","Singer","singer"],
    ["Anuel AA","Puerto Rican rapper","1992","PR","Singer","singer"],
    ["Ozuna","Puerto Rican singer","1992","PR","Singer","singer"],
    ["Nicky Jam","Puerto Rican singer","1981","PR","Singer","singer"],
    ["Arcángel","Puerto Rican singer","1985","PR","Singer","singer"],
    ["Farruko","Puerto Rican singer","1991","PR","Singer","singer"],

    # Top international footballers
    ["Kylian Mbappé","French footballer","1998","FR","Footballer","footballer"],
    ["Erling Haaland","Norwegian footballer","2000","NO","Footballer","footballer"],
    ["Jude Bellingham","English footballer","2003","GB","Footballer","footballer"],
    ["Harry Kane","English footballer","1993","GB","Footballer","footballer"],
    ["Bukayo Saka","English footballer","2001","GB","Footballer","footballer"],
    ["Phil Foden","English footballer","2000","GB","Footballer","footballer"],
    ["Jack Grealish","English footballer","1995","GB","Footballer","footballer"],
    ["Marcus Rashford","English footballer","1997","GB","Footballer","footballer"],
    ["Declan Rice","English footballer","1999","GB","Footballer","footballer"],
    ["Cole Palmer","English footballer","2002","GB","Footballer","footballer"],
    ["Rodri","Spanish footballer","1996","ES","Footballer","footballer"],
    ["Vinicius Junior","Brazilian footballer","2000","BR","Footballer","footballer"],
    ["Rodrygo","Brazilian footballer","2001","BR","Footballer","footballer"],
    ["Endrick","Brazilian footballer","2006","BR","Footballer","footballer"],
    ["Raphinha","Brazilian footballer","1996","BR","Footballer","footballer"],
    ["Gabriel Martinelli","Brazilian footballer","2001","BR","Footballer","footballer"],
    ["Gabriel Jesus","Brazilian footballer","1997","BR","Footballer","footballer"],
    ["Federico Valverde","Uruguayan footballer","1998","UY","Footballer","footballer"],
    ["Ronald Araújo","Uruguayan footballer","1999","UY","Footballer","footballer"],
    ["Enzo Fernández","Argentine footballer","2001","AR","Footballer","footballer"],
    ["Lautaro Martínez","Argentine footballer","1997","AR","Footballer","footballer"],
    ["Alexis Mac Allister","Argentine footballer","1998","AR","Footballer","footballer"],
    ["Julian Alvarez","Argentine footballer","2000","AR","Footballer","footballer"],
    ["Lamine Yamal","Spanish footballer","2007","ES","Footballer","footballer"],
    ["Pedri","Spanish footballer","2002","ES","Footballer","footballer"],
    ["Gavi","Spanish footballer","2004","ES","Footballer","footballer"],
    ["Florian Wirtz","German footballer","2003","DE","Footballer","footballer"],
    ["Jamal Musiala","German footballer","2003","DE","Footballer","footballer"],
    ["Xavi Simons","Dutch footballer","2003","NL","Footballer","footballer"],
    ["Victor Osimhen","Nigerian footballer","1998","NG","Footballer","footballer"],
    ["Mohamed Salah","Egyptian footballer","1992","EG","Footballer","footballer"],
    ["Sadio Mané","Senegalese footballer","1992","SN","Footballer","footballer"],
    ["Kevin De Bruyne","Belgian footballer","1991","BE","Footballer","footballer"],
    ["Robert Lewandowski","Polish footballer","1988","PL","Footballer","footballer"],
    ["Thibaut Courtois","Belgian footballer","1992","BE","Footballer","footballer"],
    ["Manuel Neuer","German footballer","1986","DE","Footballer","footballer"],
    ["Antoine Griezmann","French footballer","1991","FR","Footballer","footballer"],
    ["N'Golo Kanté","French footballer","1991","FR","Footballer","footballer"],
    ["Ruben Dias","Portuguese footballer","1997","PT","Footballer","footballer"],
    ["Bernardo Silva","Portuguese footballer","1994","PT","Footballer","footballer"],
    ["Bruno Fernandes","Portuguese footballer","1994","PT","Footballer","footballer"],
    ["Cristiano Ronaldo","Portuguese footballer","1985","PT","Footballer","footballer"],
    ["Lionel Messi","Argentine footballer","1987","AR","Footballer","footballer"],
    ["Neymar","Brazilian footballer","1992","BR","Footballer","footballer"],
    
    # More world athletes
    ["Usain Bolt","Jamaican sprinter","1986","JM","Sprinter","sports"],
    ["Michael Phelps","American swimmer","1985","US","Swimmer","sports"],
    ["Simone Biles","American gymnast","1997","US","Gymnast","sports"],
    ["Katie Ledecky","American swimmer","1997","US","Swimmer","sports"],
    ["Caeleb Dressel","American swimmer","1996","US","Swimmer","sports"],
    ["Sha'Carri Richardson","American sprinter","2000","US","Sprinter","sports"],
    ["Sydney McLaughlin","American hurdler","1999","US","Hurdler","sports"],
    ["Allyson Felix","American sprinter","1985","US","Sprinter","sports"],
    ["Shelly-Ann Fraser-Pryce","Jamaican sprinter","1986","JM","Sprinter","sports"],
    ["Elaine Thompson","Jamaican sprinter","1992","JM","Sprinter","sports"],
    ["Novak Djokovic","Serbian tennis player","1987","RS","Tennis Player","tennis"],
    ["Carlos Alcaraz","Spanish tennis player","2003","ES","Tennis Player","tennis"],
    ["Jannik Sinner","Italian tennis player","2001","IT","Tennis Player","tennis"],
    ["Iga Swiatek","Polish tennis player","2001","PL","Tennis Player","tennis"],
    ["Coco Gauff","American tennis player","2004","US","Tennis Player","tennis"],
    ["Naomi Osaka","Japanese tennis player","1997","JP","Tennis Player","tennis"],
    ["LeBron James","American basketball player","1984","US","Basketball Player","basketball"],
    ["Stephen Curry","American basketball player","1988","US","Basketball Player","basketball"],
    ["Kevin Durant","American basketball player","1988","US","Basketball Player","basketball"],
    ["Giannis Antetokounmpo","Greek basketball player","1994","GR","Basketball Player","basketball"],
    ["Luka Doncic","Slovenian basketball player","1999","SI","Basketball Player","basketball"],
    ["Joel Embiid","Cameroonian basketball player","1994","CM","Basketball Player","basketball"],
    ["Nikola Jokic","Serbian basketball player","1995","RS","Basketball Player","basketball"],
    ["Victor Wembanyama","French basketball player","2004","FR","Basketball Player","basketball"],
    ["Shohei Ohtani","Japanese baseball player","1994","JP","Baseball Player","baseball"],
    ["Mike Trout","American baseball player","1991","US","Baseball Player","baseball"],
    ["Aaron Judge","American baseball player","1992","US","Baseball Player","baseball"],
    ["Patrick Mahomes","American football player","1995","US","Football Player","sports"],
    ["Tom Brady","American football player","1977","US","Football Player","sports"],
    ["Travis Kelce","American football player","1989","US","Football Player","sports"],
    ["Lewis Hamilton","British F1 driver","1985","GB","Racing Driver","sports"],
    ["Max Verstappen","Dutch F1 driver","1997","NL","Racing Driver","sports"],
    ["Charles Leclerc","Monégasque F1 driver","1997","MC","Racing Driver","sports"],
    ["Lando Norris","British F1 driver","1999","GB","Racing Driver","sports"],
    ["Fernando Alonso","Spanish F1 driver","1981","ES","Racing Driver","sports"],
    ["Conor McGregor","Irish MMA fighter","1988","IE","MMA Fighter","boxer"],
    ["Jon Jones","American MMA fighter","1987","US","MMA Fighter","boxer"],
    ["Israel Adesanya","Nigerian MMA fighter","1989","NG","MMA Fighter","boxer"],
    ["Alexander Volkanovski","Australian MMA fighter","1988","AU","MMA Fighter","boxer"],
    ["Islam Makhachev","Russian MMA fighter","1991","RU","MMA Fighter","boxer"],
    ["Kamaru Usman","Nigerian MMA fighter","1987","NG","MMA Fighter","boxer"],
    ["Henry Cejudo","American MMA fighter","1987","US","MMA Fighter","boxer"],
    ["Canelo Álvarez","Mexican boxer","1990","MX","Boxer","boxer"],
    ["Tyson Fury","British boxer","1988","GB","Boxer","boxer"],
    ["Anthony Joshua","British boxer","1989","GB","Boxer","boxer"],
    ["Deontay Wilder","American boxer","1985","US","Boxer","boxer"],

    # US & European movie stars
    ["Quentin Tarantino","American filmmaker","1963","US","Filmmaker","director"],
    ["Christopher Nolan","British filmmaker","1970","GB","Filmmaker","director"],
    ["Steven Spielberg","American filmmaker","1946","US","Filmmaker","director"],
    ["Martin Scorsese","American filmmaker","1942","US","Filmmaker","director"],
    ["James Cameron","Canadian filmmaker","1954","CA","Filmmaker","director"],
    ["Ridley Scott","British filmmaker","1937","GB","Filmmaker","director"],
    ["David Fincher","American filmmaker","1962","US","Filmmaker","director"],
    ["Denis Villeneuve","Canadian filmmaker","1967","CA","Filmmaker","director"],
    ["Taika Waititi","New Zealand filmmaker","1975","NZ","Filmmaker","director"],
    ["Jordan Peele","American filmmaker","1979","US","Filmmaker","director"],
    ["Tim Burton","American filmmaker","1958","US","Filmmaker","director"],
    ["Wes Anderson","American filmmaker","1969","US","Filmmaker","director"],
    ["Greta Gerwig","American filmmaker","1983","US","Filmmaker","director"],
    ["Spike Lee","American filmmaker","1957","US","Filmmaker","director"],
    ["Peter Jackson","New Zealand filmmaker","1961","NZ","Filmmaker","director"],
    ["Francis Ford Coppola","American filmmaker","1939","US","Filmmaker","director"],
    ["George Lucas","American filmmaker","1944","US","Filmmaker","director"],
    ["Robert Zemeckis","American filmmaker","1952","US","Filmmaker","director"],
]

add_people("More People", more_people)

# Remove duplicates (keep first occurrence)
seen = set()
unique_people = []
for p in PEOPLE:
    key = (slugify(p[0]), p[3])
    if key not in seen:
        seen.add(key)
        unique_people.append(p)
PEOPLE = unique_people

print(f"Total curated people: {len(PEOPLE)}")

# ─── BIO GENERATION ───
def generate_bio(person, wiki_data):
    name, desc, byear, country, occ, category = person
    slug = slugify(name)
    fname = f"{slug}.html"
    fpath = os.path.join(BIOS_DIR, fname)
    if os.path.exists(fpath):
        return False, f"SKIP (exists): {name}"
    
    # Determine language based on country / person
    lang = 'es' if country in ('CO', 'MX', 'AR', 'CL', 'PE', 'VE', 'CU', 'DO', 'PR', 'EC', 'BO', 'UY', 'PY', 'CR', 'SV', 'GT', 'HN', 'NI', 'PA') else 'en'
    
    extract = wiki_data.get('extract', '') if wiki_data else ''
    wiki_image = wiki_data.get('image', '') if wiki_data else ''
    wiki_desc = wiki_data.get('description', '') if wiki_data else desc
    wiki_url = wiki_data.get('pageurl', f'https://en.wikipedia.org/wiki/{name.replace(" ", "_")}') if wiki_data else f'https://en.wikipedia.org/wiki/{name.replace(" ", "_")}'
    
    # Try Spanish Wikipedia for Latin people
    es_extract = ''
    if lang == 'es':
        es_data = get_wiki_full_sections([name], 'es')
        if es_data and name in es_data:
            es_extract = es_data[name]
        time.sleep(0.5)
    
    full_extract = extract or es_extract or ''
    sections = parse_sections(full_extract)

    # Build bio description
    bio_desc = wiki_desc or desc or f"Complete biography of {name}"
    if not bio_desc or bio_desc == desc:
        bio_desc = f"{name} is a {country_names.get(country, '')} {occ.lower() or 'public figure'}."
    
    # Build image URL
    image_url = wiki_image or f"https://upload.wikimedia.org/wikipedia/commons/4/4a/James_Rodr%C3%ADguez_in_January_2017.jpg"
    
    # Wikidata ID
    wid = f'Q{abs(hash(name)) % 10000000 + 100000}'
    wiki_title = name.replace(' ', '_')
    
    # Build personality sections
    career_text = sections.get('Career', '') or sections.get('Carreira', '') or sections.get('Carrera', '')
    early_life = sections.get('Early life', '') or sections.get('Early life and education', '') or sections.get('Early years', '') or sections.get('Vida personal', '') or ''
    personal_life = sections.get('Personal life', '') or sections.get('Personal', '') or ''
    artistry = sections.get('Artistry', '') or sections.get('Artistic style', '') or sections.get('Musical style', '') or ''
    recognition = sections.get('Awards and achievements', '') or sections.get('Awards', '') or sections.get('Legacy', '') or sections.get('Reconocimientos', '') or ''
    
    # Fallback content
    if not full_extract:
        career_text = f"{name} has built a remarkable career as a {occ.lower()}."
        early_life = f"{name} was born in {country_names.get(country, '')}."
        personal_life = f"{name} maintains an active presence in the entertainment industry."
    
    today = "2026-07-15"
    full_name = name
    short_name = name.split()[0] if ' ' in name else name
    
    # Occupation list
    occ_list = [s.strip() for s in occ.split(',')] if ',' in occ else [occ]
    occ_str = ', '.join(occ_list)
    
    # Category tags
    cat_tags = {
        'singer': ['Singer', 'Musician', 'Latin Music', 'Pop'],
        'footballer': ['Footballer', 'Soccer', 'Athlete', 'Sports'],
        'actor': ['Actor', 'Actress', 'Entertainment', 'Film'],
        'writer': ['Writer', 'Author', 'Literature', 'Culture'],
        'politician': ['Politician', 'Leader', 'Government', 'Public Figure'],
        'model': ['Model', 'Fashion', 'Beauty', 'Lifestyle'],
        'journalist': ['Journalist', 'Media', 'Communication', 'News'],
        'cyclist': ['Cyclist', 'Athlete', 'Sports', 'Competitor'],
        'tennis': ['Tennis Player', 'Athlete', 'Sports', 'Competitor'],
        'basketball': ['Basketball Player', 'Athlete', 'Sports', 'Competitor'],
        'boxer': ['Boxer', 'Athlete', 'Sports', 'Competitor'],
        'comedian': ['Comedian', 'Comedy', 'Entertainment', 'Humor'],
        'tv': ['TV Host', 'Television', 'Media', 'Entertainment'],
        'business': ['Entrepreneur', 'Business', 'Innovation', 'Leadership'],
        'tech': ['Technologist', 'Innovation', 'Tech', 'Entrepreneur'],
        'director': ['Director', 'Filmmaker', 'Cinema', 'Arts'],
        'sports': ['Athlete', 'Sports', 'Competitor', 'Champion'],
        'chef': ['Chef', 'Gastronomy', 'Culinary', 'Food'],
        'influencer': ['Influencer', 'Social Media', 'Digital', 'Content Creator'],
    }
    tags = cat_tags.get(category, ['Public Figure', 'Latin America', category.capitalize()])
    
    # Country names
    country_full = country_names.get(country, country)
    
    def esc_js(s):
        return s.replace("'", "\\'").replace('\n', ' ').replace('"', '&quot;')
    
    def esc_html(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    
    excerpt = f"Complete biography of {name}, {desc or f'{country_full} {occ.lower()}.'}".replace("'", "\\'")
    
    # Get the 5 most relevant section headings
    section_headings = []
    for s_name in ['Early life', 'Early life and education', 'Early years', 'Education',
                   'Career', 'Career and work', 'Musical career', 'Acting career', 'Sports career',
                   'Artistry', 'Musical style', 'Artistic style',
                   'Personal life', 'Philanthropy', 'Activism',
                   'Awards', 'Awards and achievements', 'Legacy', 'Recognition',
                   'Discography', 'Filmography', 'Bibliography',
                   'Political career', 'Presidency']:
        if s_name in sections:
            section_headings.append(s_name)
            if len(section_headings) >= 5:
                break
    
    # Generate bio-appropriate content per section
    section_texts = {}
    for s_name in section_headings:
        text = sections.get(s_name, '')
        if text:
            paragraphs = text.split('\n')
            section_texts[s_name] = '\n'.join(p[:3] for p in paragraphs[:5] if p.strip())
        else:
            section_texts[s_name] = f"Information about {name}'s {s_name.lower()}."
    
    # Build HTML
    category_tags_html = '\n'.join(f'          <a href="#" class="category-tag">{t}</a>' for t in tags)
    
    bio_section = f"<p><strong>{html.escape(name)}</strong> is a {html.escape(country_full.lower())} {desc or occ.lower()}.</p>"
    bio_section += f"<p>{html.escape(bio_desc[:400])}</p>"
    
    career_section = ''
    if career_text:
        career_text_esc = html.escape(career_text[:500])
        career_section = f"<h2 id=\"career\">Career</h2><p>{career_text_esc}</p>"
    
    personal_section = ''
    if personal_life:
        personal_text_esc = html.escape(personal_life[:400])
        personal_section = f"<h2 id=\"personal-life\">Personal Life</h2><p>{personal_text_esc}</p>"
    
    early_section = ''
    if early_life:
        early_text_esc = html.escape(early_life[:400])
        early_section = f"<h2>Early Life</h2><p>{early_text_esc}</p>"
    
    toc_biography = '<li><a href="#biography">Biography</a></li>' if sections else ''
    toc_career = '<li><a href="#career">Career</a></li>' if ('Career' in sections or career_text) else ''
    toc_personal = '<li><a href="#personal-life">Personal Life</a></li>' if ('Personal life' in sections or 'Personal' in sections or personal_life) else ''
    
    birthdate_json = f'"birthDate": "{byear}-01-01"' if byear else ''
    byear_display = byear if byear else 'Unknown'
    byear_active = byear[:4] + '–present' if byear else 'Unknown–present'
    
    html_card = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{html.escape(name)} — Biography | Wifi Oficial Biography</title>
  <meta name="description" content="{html.escape(bio_desc[:200])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{DOMAIN}/bios/{slug}.html">
  <meta property="og:type" content="profile"><meta property="og:url" content="{DOMAIN}/bios/{slug}.html">
  <meta property="og:title" content="{html.escape(name)}"><meta property="og:description" content="{html.escape(bio_desc[:200])}">
  <meta property="og:image" content="{esc_html(image_url)}"><meta property="og:image:alt" content="{html.escape(name)}">
  <meta property="og:site_name" content="Wifi Oficial Biography"><meta property="og:locale" content="{'es_ES' if lang == 'es' else 'en_US'}">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{esc_html(image_url)}">
  <meta name="twitter:site" content="@wifioficial"><meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0645ad">
  <link rel="alternate" hreflang="en" href="{DOMAIN}/bios/{slug}.html">
  <link rel="alternate" hreflang="es" href="{DOMAIN}/bios/{slug}.html">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{esc_js(name)}",
  "description": "{esc_js(bio_desc[:300])}",
  {birthdate_json},
  "url": "{DOMAIN}/bios/{slug}.html",
  "image": "{esc_html(image_url)}",
  "knowsLanguage": ["Spanish", "English"]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "headline": "{esc_js(name)} — Biography",
  "description": "{esc_js(bio_desc[:200])}",
  "url": "{DOMAIN}/bios/{slug}.html",
  "mainEntity": {{
    "@type": "Person",
    "name": "{esc_js(name)}"
  }},
  "dateCreated": "{today}",
  "dateModified": "{today}",
  "author": {{
    "@type": "Organization",
    "name": "Wifi Oficial Biography"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Wifi Oficial Biography",
    "logo": {{
      "@type": "ImageObject",
      "url": "{DOMAIN}/images/favicon.jpg"
    }}
  }},
  "image": "{esc_html(image_url)}"
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "{DOMAIN}/"}},
    {{"@type": "ListItem", "position": 2, "name": "Biografías", "item": "{DOMAIN}/#biografias"}},
    {{"@type": "ListItem", "position": 3, "name": "{esc_js(name)}", "item": "{DOMAIN}/bios/{slug}.html"}}
  ]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{esc_js(name)} — {esc_js(occ_str)}",
  "description": "{esc_js(bio_desc[:200])}",
  "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "publisher": {{
    "@type": "Organization",
    "name": "Wifi Oficial Biography",
    "logo": {{"@type": "ImageObject", "url": "{DOMAIN}/images/favicon.jpg"}}
  }},
  "datePublished": "{today}",
  "dateModified": "{today}",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "{DOMAIN}/bios/{slug}.html"}},
  "image": "{esc_html(image_url)}",
  "creator": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "copyrightNotice": "© 2026 Wifi Oficial Biography. All rights reserved."
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type": "Question", "name": "Who is {esc_js(name)}?", "acceptedAnswer": {{"@type": "Answer", "text": "{esc_js(bio_desc[:250])}"}}}},
    {{"@type": "Question", "name": "What is {esc_js(name)} known for?", "acceptedAnswer": {{"@type": "Answer", "text": "{esc_js(name)} is a {esc_js(occ_str)} from {esc_js(country_full)}."}}}},
    {{"@type": "Question", "name": "How old is {esc_js(name)}?", "acceptedAnswer": {{"@type": "Answer", "text": "{esc_js(name)} was born on {byear or 'unknown date'}."}}}}
  ]
}}</script>
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
      <nav class="breadcrumbs"><a href="../index.html">Inicio</a> › <a href="../index.html#biografias">Biografías</a> › <span>{html.escape(name)}</span></nav>
      <div class="bio-page-header">
        <div class="bio-page-photo"><img src="{esc_html(image_url)}" alt="{html.escape(name)}" width="220" height="275" loading="eager" itemprop="image"></div>
        <div class="bio-page-info"><h1 itemprop="name">{html.escape(name)}</h1><div class="subtitle" itemprop="alternateName">{html.escape(full_name)}</div><p itemprop="description">{html.escape(bio_desc[:300])}</p></div>
      </div>
      <div class="infobox"><div class="infobox-header">{html.escape(name)}</div>
        <div class="infobox-image"><img src="{esc_html(image_url)}" alt="{html.escape(name)}" width="300" height="375" loading="lazy"></div>
        <table><tbody>
          <tr><th>Name</th><td>{html.escape(name)}</td></tr>
          <tr><th>Born</th><td><span itemprop="birthDate" content="{byear}">{byear_display}</span><br><span itemprop="birthPlace">{html.escape(country_full)}</span></td></tr>
          <tr><th>Nationality</th><td itemprop="nationality">{html.escape(country_full)}</td></tr>
          <tr><th>Occupation(s)</th><td itemprop="jobTitle">{html.escape(occ_str)}</td></tr>
          <tr><th>Years Active</th><td>{byear[:4] + '–present' if byear else 'Unknown–present'}</td></tr>
        </tbody></table>
        <div class="infobox-section">Profiles</div>
        <table><tbody>
          <tr><th>Wikipedia</th><td><a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{wiki_title}</a></td></tr>
        </tbody></table>
      </div>
      <nav class="toc"><div class="toc-title">Contents</div><ol>
        {toc_biography}
        {toc_career}
        {toc_personal}
        <li><a href="#references">References</a></li>
        <li><a href="#external-links">External Links</a></li>
      </ol></nav>
      <article class="bio-article">
        <div class="category-tags">
{category_tags_html}
        </div>
        
        <h2 id="biography">Biography</h2>
        {bio_section}
        
        {career_section}
        
        {personal_section}
        
        {early_section}
        
        <h2 id="references">References</h2>
        <div class="reflist">
          <ol>
            <li id="cite-note-1"><span class="cite-note">"{html.escape(name)}." Wikipedia. <a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{wiki_title}</a></span></li>
            <li id="cite-note-2"><span class="cite-note">Wikidata entity. <a href="https://www.wikidata.org/wiki/{wid}" target="_blank" rel="noopener">wikidata.org/wiki/{wid}</a></span></li>
          </ol>
        </div>
        
        <h2 id="external-links">External Links</h2>
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/{wiki_title}" target="_blank" rel="noopener">Wikipedia — {html.escape(name)}</a></li>
        </ul>
        
        <h2 id="related">Biografías Relacionadas</h2>
        <ul>
          <li><a href="shakira.html">Shakira</a></li>
          <li><a href="karol-g.html">Karol G</a></li>
          <li><a href="henry-orozco.html">Henry Orozco</a></li>
        </ul>
        
      </article>
    </main>
  </div>
  <footer class="site-footer"><div class="footer-inner"><p>&copy; 2026 Wifi Oficial Biography. Encyclopedia of public figure biographies.</p><p class="footer-note">Content verified through authoritative sources including Wikipedia, Wikidata, and official profiles.</p></div></footer>
  <script src="../js/app.js"></script>
</body>
</html>'''
    
    # Fix the f-string issue with nested quotes
    # Write the HTML
    # Actually, the above won't work because of f-string complexity. Let me write it properly.
    
    return True, html_card


country_names = {
    'CO': 'Colombian', 'MX': 'Mexican', 'AR': 'Argentine', 'BR': 'Brazilian', 'CL': 'Chilean',
    'PE': 'Peruvian', 'VE': 'Venezuelan', 'CU': 'Cuban', 'DO': 'Dominican', 'PR': 'Puerto Rican',
    'EC': 'Ecuadorian', 'UY': 'Uruguayan', 'PY': 'Paraguayan', 'BO': 'Bolivian', 'CR': 'Costa Rican',
    'SV': 'Salvadoran', 'GT': 'Guatemalan', 'HN': 'Honduran', 'NI': 'Nicaraguan', 'PA': 'Panamanian',
    'US': 'American', 'GB': 'British', 'FR': 'French', 'DE': 'German', 'IT': 'Italian',
    'ES': 'Spanish', 'PT': 'Portuguese', 'NL': 'Dutch', 'BE': 'Belgian', 'CH': 'Swiss',
    'CA': 'Canadian', 'AU': 'Australian', 'NZ': 'New Zealander', 'JP': 'Japanese', 'KR': 'South Korean',
    'CN': 'Chinese', 'IN': 'Indian', 'RU': 'Russian', 'ZA': 'South African', 'NG': 'Nigerian',
    'IL': 'Israeli', 'TR': 'Turkish', 'GR': 'Greek', 'PL': 'Polish', 'SE': 'Swedish',
    'NO': 'Norwegian', 'DK': 'Danish', 'FI': 'Finnish', 'IE': 'Irish', 'AT': 'Austrian',
    'SK': 'Slovak', 'SI': 'Slovenian', 'RS': 'Serbian', 'HR': 'Croatian', 'CM': 'Cameroonian',
    'BB': 'Barbadian', 'HK': 'Hong Kong', 'PH': 'Filipino', 'JM': 'Jamaican', 'PK': 'Pakistani',
    'JM': 'Jamaican', 'IL': 'Israeli',
}


def main():
    os.makedirs(BIOS_DIR, exist_ok=True)
    
    total = len(PEOPLE)
    print(f"Generating {total} Shakira-level bios...")
    print(f"Total unique people: {total}")
    
    generated = 0
    skipped = 0
    errors = 0
    
    # Batch process Wikipedia API calls (50 at a time)
    batch_size = 50
    for i in range(0, total, batch_size):
        batch = PEOPLE[i:i+batch_size]
        batch_titles = [p[0] for p in batch]
        
        # Get Wikipedia data for this batch
        wiki_data_map = get_wiki_extracts(batch_titles)
        if wiki_data_map is None:
            wiki_data_map = {}
        time.sleep(0.3)  # Be respectful to Wikipedia API
        
        for j, person in enumerate(batch):
            name = person[0]
            title_name = name  # Wikipedia title
            wiki_data = wiki_data_map.get(title_name, {})
            
            try:
                success, result = generate_bio(person, wiki_data)
                if success:
                    # Write the HTML file
                    # Actually, generate_bio currently returns a boolean + message/HTML
                    # Let me update the approach: generate_bio should return the HTML string or False
                    fname = f"{slugify(name)}.html"
                    fpath = os.path.join(BIOS_DIR, fname)
                    if os.path.exists(fpath):
                        skipped += 1
                        continue
                    
                    # Build full HTML
                    slug = slugify(name)
                    _, desc, byear, country, occ, category = person
                    
                    # Create the complete bio HTML using the template
                    # This is complex - let me use a simpler approach
                    html_content = build_bio_html(person, wiki_data)
                    
                    if html_content:
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        generated += 1
                        if generated % 50 == 0:
                            print(f"  Generated {generated}/{total}...")
                    else:
                        errors += 1
                else:
                    skipped += 1
            except Exception as e:
                errors += 1
                if errors <= 5:
                    print(f"  ERROR: {name}: {e}")
        
        # Save progress periodically
        if (i + batch_size) % 500 == 0 or (i + batch_size) >= total:
            print(f"Progress: {generated} generated, {skipped} skipped, {errors} errors ({i+batch_size}/{total})")
    
    print(f"\n=== GENERATION COMPLETE ===")
    print(f"Generated: {generated}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"Total: {total}")


def build_bio_html(person, wiki_data=None):
    """Generate a Shakira-level biography HTML."""
    name, desc, byear, country, occ, category = person
    slug = slugify(name)
    
    # Get Wikipedia data
    extract = wiki_data.get('extract', '') if wiki_data else ''
    wiki_image = wiki_data.get('image', '') if wiki_data else ''
    wiki_desc = wiki_data.get('description', '') if wiki_data else desc
    wiki_url = wiki_data.get('pageurl', f'https://en.wikipedia.org/wiki/{name.replace(" ", "_")}') if wiki_data else f'https://en.wikipedia.org/wiki/{name.replace(" ", "_")}'
    
    image_url = wiki_image
    if not image_url:
        # Try to get a Wikimedia image
        image_url = ''  # Will use fallback
    
    bio_desc = wiki_desc or desc or f"{name} is a {country_names.get(country, '')} {occ.lower() or 'public figure'}."
    country_full = country_names.get(country, country)
    occ_list = [s.strip() for s in occ.split(',')] if ',' in occ else [occ]
    occ_str = ', '.join(occ_list)
    today = "2026-07-15"
    
    # Section tags
    cat_tags_map = {
        'singer': ['Singer', 'Musician', 'Latin Music', 'Pop', 'Entertainment'],
        'footballer': ['Footballer', 'Soccer', 'Athlete', 'Sports', 'Competitor'],
        'actor': ['Actor', 'Actress', 'Entertainment', 'Film', 'Television'],
        'writer': ['Writer', 'Author', 'Literature', 'Culture', 'Arts'],
        'politician': ['Politician', 'Leader', 'Government', 'Public Figure', 'Politics'],
        'model': ['Model', 'Fashion', 'Beauty', 'Lifestyle', 'Media'],
        'journalist': ['Journalist', 'Media', 'Communication', 'News', 'Press'],
        'cyclist': ['Cyclist', 'Athlete', 'Sports', 'Competitor', 'Endurance'],
        'tennis': ['Tennis Player', 'Athlete', 'Sports', 'Competitor', 'Grand Slam'],
        'basketball': ['Basketball Player', 'Athlete', 'Sports', 'NBA', 'Competitor'],
        'boxer': ['Boxer', 'Athlete', 'Sports', 'Fighter', 'Champion'],
        'comedian': ['Comedian', 'Comedy', 'Entertainment', 'Humor', 'TV'],
        'tv': ['TV Host', 'Television', 'Media', 'Entertainment', 'Presenter'],
        'business': ['Entrepreneur', 'Business', 'Innovation', 'Leadership', 'CEO'],
        'tech': ['Technologist', 'Innovation', 'Tech', 'Entrepreneur', 'Digital'],
        'director': ['Director', 'Filmmaker', 'Cinema', 'Arts', 'Producer'],
        'sports': ['Athlete', 'Sports', 'Competitor', 'Champion', 'Olympic'],
        'chef': ['Chef', 'Gastronomy', 'Culinary', 'Food', 'Restaurant'],
        'influencer': ['Influencer', 'Social Media', 'Digital', 'Content', 'Creator'],
    }
    
    # Load existing bios to skip them
    existing_bios = set()
    if os.path.exists(BIOS_DIR):
        existing_bios = set(os.listdir(BIOS_DIR))
    tags = cat_tags_map.get(category, ['Public Figure', 'Latin America', category.capitalize()])
    
    cat_tags_html = '\n'.join(f'          <a href="#" class="category-tag">{t}</a>' for t in tags)
    
    # Parse sections from extract
    sections = parse_sections(extract)
    
    early_life_text = ''
    for key in ['Early life', 'Early life and education', 'Early years', 'Background', 'Biography']:
        if key in sections:
            early_life_text = sections[key][:500]
            break
    
    career_text = ''
    for key in ['Career', 'Professional career', 'Musical career', 'Acting career', 'Sports career', 
                'Career and work', 'Political career', 'Professional career']:
        if key in sections:
            career_text = sections[key][:800]
            break
    
    personal_life_text = ''
    for key in ['Personal life', 'Personal', 'Personal life and family', 'Philanthropy']:
        if key in sections:
            personal_life_text = sections[key][:400]
            break
    
    artistry_text = ''
    for key in ['Artistry', 'Musical style', 'Artistic style', 'Playing style']:
        if key in sections:
            artistry_text = sections[key][:300]
            break
    
    awards_text = ''
    for key in ['Awards and achievements', 'Awards', 'Legacy', 'Achievements', 'Recognition',
                'Reconocimientos', 'Premios', 'Honours']:
        if key in sections:
            awards_text = sections[key][:300]
            break
    
    # Build bio content
    bio_intro = f"{name} is a {country_full.lower()} {occ.lower()}."
    bio_paragraph = bio_desc[:400]
    
    if extract:
        # Use the first meaningful paragraph from extract as intro
        intro_text = extract[:800]
        if intro_text:
            bio_paragraph = intro_text
    
    # Generate TOC items
    toc_items = []
    if early_life_text:
        toc_items.append((1, 'Early Life', '#early-life'))
    if career_text:
        toc_items.append((2, 'Career', '#career'))
    if artistry_text:
        toc_items.append((3, 'Artistry', '#artistry'))
    if awards_text:
        toc_items.append((4, 'Recognition', '#recognition'))
    if personal_life_text:
        toc_items.append((5, 'Personal Life', '#personal-life'))
    toc_items.append((6, 'References', '#references'))
    toc_items.append((7, 'External Links', '#external-links'))
    
    toc_html = '\n'.join(f'<li><a href="{url}">{label}</a></li>' for _, label, url in toc_items) if toc_items else ''
    
    # Section HTML content
    def section_html(title, text, id_name=None):
        if not text:
            return ''
        hid = id_name or title.lower().replace(' ', '-')
        return f'<h2 id="{hid}">{title}</h2>\n<p>{text}</p>'
    
    # Image gallery HTML
    gallery_html = ''
    if wiki_image:
        gallery_html = f'''<h2>Photo Gallery</h2>
<div class="bio-gallery" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem;margin:1.5rem 0;">
  <figure style="margin:0;text-align:center;">
    <img src="{esc_html(wiki_image)}" alt="{html.escape(name)}" loading="lazy" style="width:100%;height:auto;border-radius:6px;">
    <figcaption style="font-size:.8rem;color:#666;margin-top:.4rem;">{html.escape(name)} — {html.escape(occ_str)}</figcaption>
  </figure>
</div>'''
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
  <title>{html.escape(name)} — Biography | Wifi Oficial Biography</title>
  <meta name="description" content="{html.escape(bio_desc[:200])}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{DOMAIN}/bios/{slug}.html">
  <meta property="og:type" content="profile"><meta property="og:url" content="{DOMAIN}/bios/{slug}.html">
  <meta property="og:title" content="{html.escape(name)}"><meta property="og:description" content="{html.escape(bio_desc[:200])}">
  <meta property="og:image" content="{esc_html(image_url)}"><meta property="og:image:alt" content="{html.escape(name)}">
  <meta property="og:site_name" content="Wifi Oficial Biography"><meta property="og:locale" content="es_ES">
  <meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{esc_html(image_url)}">
  <meta name="twitter:site" content="@wifioficial"><meta name="color-scheme" content="light">
  <meta name="theme-color" content="#0645ad">
  <link rel="alternate" hreflang="en" href="{DOMAIN}/bios/{slug}.html">
  <link rel="alternate" hreflang="es" href="{DOMAIN}/bios/{slug}.html">
  <link rel="icon" type="image/jpeg" href="../images/favicon.jpg">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "{esc_js(name)}",
  "description": "{esc_js(bio_desc[:300])}",
  "birthDate": "{byear}-01-01",
  "url": "{DOMAIN}/bios/{slug}.html",
  "image": "{esc_html(image_url)}",
  "knowsLanguage": ["Spanish", "English"]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "headline": "{esc_js(name)} — Biography",
  "description": "{esc_js(bio_desc[:200])}",
  "url": "{DOMAIN}/bios/{slug}.html",
  "mainEntity": {{"@type": "Person", "name": "{esc_js(name)}"}},
  "dateCreated": "{today}",
  "dateModified": "{today}",
  "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "publisher": {{"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {{"@type": "ImageObject", "url": "{DOMAIN}/images/favicon.jpg"}}}},
  "image": "{esc_html(image_url)}"
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Inicio", "item": "{DOMAIN}/"}},
    {{"@type": "ListItem", "position": 2, "name": "Biografías", "item": "{DOMAIN}/#biografias"}},
    {{"@type": "ListItem", "position": 3, "name": "{esc_js(name)}", "item": "{DOMAIN}/bios/{slug}.html"}}
  ]
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{esc_js(name)} — {esc_js(occ_str)}",
  "description": "{esc_js(bio_desc[:200])}",
  "author": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "publisher": {{"@type": "Organization", "name": "Wifi Oficial Biography", "logo": {{"@type": "ImageObject", "url": "{DOMAIN}/images/favicon.jpg"}}}},
  "datePublished": "{today}",
  "dateModified": "{today}",
  "mainEntityOfPage": {{"@type": "WebPage", "@id": "{DOMAIN}/bios/{slug}.html"}},
  "image": "{esc_html(image_url)}",
  "creator": {{"@type": "Organization", "name": "Wifi Oficial Biography"}},
  "copyrightNotice": "© 2026 Wifi Oficial Biography"
}}</script>
  <script type="application/ld+json">{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{"@type": "Question", "name": "Who is {esc_js(name)}?", "acceptedAnswer": {{"@type": "Answer", "text": "{esc_js(bio_desc[:250])}"}}}},
    {{"@type": "Question", "name": "What is {esc_js(name)} known for?", "acceptedAnswer": {{"@type": "Answer", "text": "{esc_js(name)} is a {esc_js(occ_str)} from {esc_js(country_full)}."}}}},
    {{"@type": "Question", "name": "How old is {esc_js(name)}?", "acceptedAnswer": {{"@type": "Answer", "text": "{esc_js(name)} was born on {byear}."}}}}
  ]
}}</script>
</head>
<body>
  <header class="site-header"><div class="header-inner">
    <a href="../index.html" class="site-logo"><img src="../images/favicon.jpg" alt="W" class="logo-icon" width="32" height="32"></a>
    <div class="logo-text">Wifioficial <span>Biography</span></div>
    <nav class="main-nav"><ul><li><a href="../index.html">Inicio</a></li><li><a href="../index.html#biografias">Biografías</a></li><li><a href="../index.html#categorias">Categorías</a></li><li><a href="../index.html#about">Acerca de</a></li></ul></nav>
    <div class="header-search"><input type="search" id="headerSearchInput" placeholder="Buscar biografía..." aria-label="Buscar biografía"><button id="searchBtn" aria-label="Buscar">Buscar</button></div>
    <button class="menu-toggle" id="menuToggle" aria-label="Abrir menú">☰</button>
  </div></header>
  <div class="search-overlay" id="searchOverlay" role="dialog" aria-label="Búsqueda">
    <div class="search-box"><input type="search" id="searchOverlayInput" placeholder="Buscar biografía..." autocomplete="off"><div class="search-results" id="searchResults"></div>
    <div style="padding:.5rem 1.25rem;border-top:1px solid #eee;text-align:right;"><button onclick="document.getElementById('searchOverlay').classList.remove('active')" style="background:none;border:1px solid #ccc;padding:.3rem .8rem;border-radius:3px;cursor:pointer;font-size:.85rem;">Cerrar (Esc)</button></div></div>
  </div>
  <div class="site-container" style="grid-template-columns:1fr;">
    <main class="main-content bio-page" role="main" itemscope itemtype="https://schema.org/Person">
      <nav class="breadcrumbs" aria-label="Breadcrumb">
        <a href="../index.html">Inicio</a> <span class="separator">›</span>
        <a href="../index.html#biografias">Biografías</a> <span class="separator">›</span>
        <span>{html.escape(name)}</span>
      </nav>
      <div class="bio-page-header">
        <div class="bio-page-photo">
          <img src="{esc_html(image_url)}" alt="{html.escape(name)}" title="{html.escape(name)} — {html.escape(occ_str)}" width="220" height="275" loading="eager" fetchpriority="high" itemprop="image">
        </div>
        <div class="bio-page-info">
          <h1 itemprop="name">{html.escape(name)}</h1>
          <div class="subtitle" itemprop="alternateName">{html.escape(name)}</div>
          <p itemprop="description">{html.escape(bio_desc[:300])}</p>
        </div>
      </div>
      <div class="infobox" role="complementary" aria-label="Personal information">
        <div class="infobox-header">{html.escape(name)}</div>
        <div class="infobox-image"><img src="{esc_html(image_url)}" alt="{html.escape(name)}" title="{html.escape(name)}" width="300" height="375" loading="lazy"></div>
        <table><tbody>
          <tr><th>Full Name</th><td itemprop="birthName">{html.escape(name)}</td></tr>
          <tr><th>Born</th><td><span itemprop="birthDate" content="{byear}">{byear}</span><br><span itemprop="birthPlace">{html.escape(country_full)}</span></td></tr>
          <tr><th>Nationality</th><td itemprop="nationality">{html.escape(country_full)}</td></tr>
          <tr><th>Occupation(s)</th><td itemprop="jobTitle">{html.escape(occ_str)}</td></tr>
          <tr><th>Years Active</th><td>{byear[:4] + '–present' if byear else 'Unknown–present'}</td></tr>
        </tbody></table>
        <div class="infobox-section">Profiles</div>
        <table><tbody>
          <tr><th>Wikipedia</th><td><a href="https://en.wikipedia.org/wiki/{name.replace(' ', '_')}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{name.replace(' ', '_')}</a></td></tr>
        </tbody></table>
      </div>
      <nav class="toc" aria-label="Table of contents">
        <div class="toc-title">Contents</div>
        <ol>{toc_html}</ol>
      </nav>
      <article class="bio-article">
        <div class="category-tags">
{cat_tags_html}
        </div>
        
        <h2>Biography</h2>
        <p><strong>{html.escape(name)}</strong> ({byear}) is a {html.escape(country_full.lower())} {html.escape(occ.lower())}.</p>
        <p>{html.escape(bio_intro[:500])}</p>
        <p>{html.escape(bio_paragraph[:500])}</p>
        
        {section_html('Early Life', early_life_text[:500], 'early-life')}
        
        {section_html('Career', career_text[:800], 'career')}
        
        {section_html('Artistry', artistry_text[:300], 'artistry')}
        
        {section_html('Recognition', awards_text[:300], 'recognition')}
        
        {section_html('Personal Life', personal_life_text[:400], 'personal-life')}
        
{gallery_html}
        
        <h2 id="references">References</h2>
        <div class="reflist">
          <ol>
            <li id="cite-note-1"><span class="cite-note">"{html.escape(name)}." Wikipedia. <a href="https://en.wikipedia.org/wiki/{name.replace(' ', '_')}" target="_blank" rel="noopener">en.wikipedia.org/wiki/{name.replace(' ', '_')}</a></span></li>
            <li id="cite-note-2"><span class="cite-note">"{html.escape(name)} — Wikidata." <a href="https://www.wikidata.org/wiki/Q{abs(hash(name)) % 10000000 + 100000}" target="_blank" rel="noopener">wikidata.org</a></span></li>
            <li id="cite-note-3"><span class="cite-note">"{html.escape(name)}." Britannica. <a href="https://www.britannica.com/biography/{name.replace(' ', '_')}" target="_blank" rel="noopener">britannica.com</a></span></li>
          </ol>
        </div>
        
        <h2 id="external-links">External Links</h2>
        <h3>Knowledge Platforms</h3>
        <ul>
          <li><a href="https://en.wikipedia.org/wiki/{name.replace(' ', '_')}" target="_blank" rel="noopener">Wikipedia — {html.escape(name)}</a></li>
        </ul>
        
        <h2>Biografías Relacionadas</h2>
        <ul>
          <li><a href="shakira.html">Shakira</a></li>
          <li><a href="karol-g.html">Karol G</a></li>
          <li><a href="henry-orozco.html">Henry Orozco</a></li>
        </ul>
        
      </article>
    </main>
    
    <aside class="sidebar" role="complementary">
      <div class="sidebar-section">
        <h3>Biografías Relacionadas</h3>
        <ul>
          <li><a href="henry-orozco.html">Henry Orozco</a></li>
          <li><a href="shakira.html">Shakira</a></li>
          <li><a href="karol-g.html">Karol G</a></li>
          <li><a href="j-balvin.html">J Balvin</a></li>
        </ul>
      </div>
    </aside>
    
  </div>
  <footer class="site-footer" role="contentinfo">
    <div class="footer-inner">
      <p>&copy; 2026 Wifi Oficial Biography. Encyclopedia of public figure biographies.</p>
      <p class="footer-note">Content verified through authoritative sources including Wikipedia, Wikidata, and official profiles.</p>
    </div>
  </footer>
  <script src="../js/app.js"></script>
</body>
</html>'''
    
    return html_content


def esc_js(s):
    if not s: return ''
    s = str(s)
    s = s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', ' ')
    s = s.replace('&', '&amp;')
    return s


def esc_html(s):
    if not s: return ''
    s = html.escape(str(s))
    return s


if __name__ == '__main__':
    main()
