#!/usr/bin/env python3
"""Build the Namaste Incense static site into ./dist from data/all_products.json (+ data/pickup.json).
Usage: python3 scripts/build.py [--preview] [--base=/sub] [--site=https://namasteincense.com]
"""
import json, os, re, sys, html, shutil, datetime
from collections import Counter
sys.path.insert(0, os.path.dirname(__file__))
from catmap import CATS, category

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIST = os.path.join(ROOT, 'dist')
PREVIEW = '--preview' in sys.argv
SITE = 'https://namasteincense.com'
BASE = ''
for a in sys.argv:
    if a.startswith('--base='): BASE = a.split('=', 1)[1]
    if a.startswith('--site='): SITE = a.split('=', 1)[1].rstrip('/')
BASE = ('/' + BASE.strip('/')) if BASE.strip('/') else ''
SHOP = 'https://namastebookshop.com'
BRAND = 'Namaste Incense'
LEGAL = 'Namaste Incense is a brand of Wealth Edge Ventures Inc.'
# ---- store visit details (same verified facts as Manhattan Crystal Market, Oct 29, 2026) ----
STORE_STREET = '2 West 14th Street'
STORE_CITY, STORE_REGION, STORE_ZIP = 'New York', 'NY', '10011'
STORE_ADDR = f'{STORE_STREET}, {STORE_CITY}, {STORE_REGION} {STORE_ZIP}'
PHONE, TEL = '646-876-1401', '+16468761401'
GEO = (40.73602, -73.99404)
HOURS = [('Monday to Thursday', '11 AM to 8 PM'), ('Friday and Saturday', '11 AM to 9 PM'), ('Sunday', '11 AM to 7 PM')]
HOURS_LD = [(['Monday', 'Tuesday', 'Wednesday', 'Thursday'], '11:00', '20:00'), (['Friday', 'Saturday'], '11:00', '21:00'), (['Sunday'], '11:00', '19:00')]
MAP_Q = '2+West+14th+Street,+New+York,+NY+10011'
MAP_EMBED = f'https://www.google.com/maps/embed?origin=mfe&pb=!1m3!2m1!1s{MAP_Q}!6i16'
MAP_LINK = f'https://www.google.com/maps/search/?api=1&query={MAP_Q}'
DIRECTIONS = f'https://www.google.com/maps/dir/?api=1&destination={MAP_Q}'
CART_ATTR = '?attributes%5BStorefront%5D=Namaste%20Incense'
E = html.escape

CAT_SLUG = {'sticks': 'incense-sticks', 'cones': 'cones-backflow', 'resins': 'sacred-resins', 'smudge': 'sage-palo-santo',
            'holders': 'holders-ash-catchers', 'burners': 'burners-charcoal', 'candles': 'ritual-candles'}
CAT_SHORT = {'sticks': 'Sticks', 'cones': 'Cones', 'resins': 'Resins', 'smudge': 'Sage & Palo Santo',
             'holders': 'Holders', 'burners': 'Burners & Charcoal', 'candles': 'Candles'}
CAT_COLOR = {'sticks': '#e8a33d', 'cones': '#c8662f', 'resins': '#b8862b', 'smudge': '#6f8f5a',
             'holders': '#8a6a4f', 'burners': '#5b4a6b', 'candles': '#b5532a'}

# scent families (first match wins)
FAMILIES = [
 ('nag-champa', 'Nag Champa', r'nag ?champa|champa', 'The sweet, powdery champaca and sandalwood blend that most people picture when they think of incense.'),
 ('resinous', 'Resinous & Sacred', r'frankincense|myrrh|copal|benzoin|dragon.?s ?blood|amber|guggul|church|oud|bakhoor|agar', 'Frankincense, myrrh, copal, benzoin, dragon\'s blood and amber: the oldest scents in the temple.'),
 ('woods', 'Woods & Earth', r'sandal|chandan|cedar|palo santo|pine|pinon|pi\u00f1on|juniper|vetiver|patchouli|musk|earth|forest', 'Sandalwood, cedar, palo santo, pine and patchouli for grounding, warm smoke.'),
 ('herbal', 'Sage & Herbal', r'sage|eucalyptus|rosemary|mint|green tea|tulsi|lemongrass|sweet ?grass|cannabis|aloe|herbal|bamboo', 'White sage, eucalyptus, rosemary, mint and green tea: clean, bright and clearing.'),
 ('floral', 'Floral', r'rose|jasmine|lavender|lotus|gardenia|lilac|honeysuckle|violet|orchid|ylang|mimosa|magnolia|night queen|blossom|flower|floral|neroli', 'Rose, jasmine, lavender, lotus and gardenia for soft, sweet rooms.'),
 ('sweet', 'Sweet & Spice', r'vanilla|cinnamon|coconut|strawberry|cherry|apple|honey|chocolate|coffee|spice|orange|lemon|mango|fruit|opium|amber', 'Vanilla, cinnamon, coconut and fruit notes for cozy, gourmand smoke.'),
]
FAM_NAME = {k: n for k, n, _, _ in FAMILIES}
FAM_BLURB = {k: b for k, _, _, b in FAMILIES}
def family_of(title):
    for k, n, rx, _ in FAMILIES:
        if re.search(rx, title, re.I): return k
    return ''

# brands we actually carry (only those with a landing page get one; see BRAND_PAGES)
BRANDS = [
 ('hem', 'HEM', r'\bhem\b'), ('satya', 'Satya', r'\bsatya\b'), ('morning-star', 'Morning Star', r'morning star'),
 ('good-karma', 'Good Karma', r'good karma'), ('sonavi', 'SONAVI', r'sonavi'), ('prabhujis', "Prabhuji's Gifts", r'prabhuji'),
 ('coventry-creations', 'Coventry Creations', r'coventry|wicked witch mojo|blessed herbal'), ('wolf-spirit', 'Wolf Spirit', r'wolf.?s? spirit'),
 ('suns-eye', "Sun's Eye", r'sun.?s eye'), ('soul-sticks', 'Soul Sticks', r'soul sticks'), ('little-smudgies', 'Little Smudgies', r'smudgies'),
 ('fred-soll', 'Fred Soll', r'fred ?soll'), ('auroshikha', 'Auroshikha', r'auroshikha'), ('kamini', 'Kamini', r'kamini'),
 ('aloha-bay', 'Aloha Bay', r'aloha bay'), ('jens', "Jen's Reiki Candles", r"jen'?s"), ('swift-lite', 'Swift Lite', r'swift.?lite'),
 ('tulasi', 'Tulasi', r'tulasi'), ('song-of-india', 'Song of India', r'song of india'),
]
BRAND_NAME = {k: n for k, n, _ in BRANDS}
def brand_of(title):
    for k, n, rx in BRANDS:
        if re.search(rx, title, re.I): return k
    return ''
BRAND_INTRO = {
 'hem': 'HEM is a large incense house from India, known for affordable masala and charcoal sticks in hundreds of scents, from classic sandalwood to intention blends like Money and Protection.',
 'satya': 'Satya incense is made by Shrinivas Sugandhalaya in Bangalore, India, the house behind the original Sai Baba Nag Champa. Hand-rolled sticks and dhoop cones.',
 'morning-star': 'Morning Star is a line of Japanese stick incense by Nippon Kodo. The thin, low-smoke sticks are a good fit for small apartments, and most packs come with a small holder.',
 'good-karma': 'Good Karma intention candles pair a scent with a theme such as Love, Abundance or Protection. Small 1 oz travel tins and larger 4 oz candles.',
 'sonavi': 'SONAVI makes natural incense sticks, oud bakhoor chips and beeswax candles.',
 'prabhujis': "Prabhuji's Gifts incense is handmade by artisans in India's cottage industry, with herbal resin incense and chakra blends.",
 'coventry-creations': 'Coventry Creations makes herbal intention candles, including the Blessed Herbal and Wicked Witch Mojo lines.',
 'wolf-spirit': 'Wolf Spirit natural resin incense comes in 30 gram packs: frankincense, myrrh, copal, benzoin and blended intention resins for charcoal.',
 'suns-eye': "Sun's Eye makes natural stick incense in classic single-note scents.",
 'soul-sticks': 'Soul Sticks makes resin incense and stick incense, including Tibetan-style sticks.',
}
BRAND_PAGES = []  # filled after counting

# traditions
def tradition_of(title, brand):
    t = title.lower()
    if 'tibet' in t: return 'Tibetan'
    if brand == 'morning-star' or 'japan' in t: return 'Japanese'
    if brand in ('hem', 'satya', 'prabhujis', 'auroshikha', 'kamini', 'tulasi', 'song-of-india') or re.search(r'dhoop|masala|agarbatti|nag champa', t): return 'Indian'
    return ''

def img(url, w):
    if not url: return ''
    return f"{url}{'&' if '?' in url else '?'}width={w}"
def money(v): return f"${float(v):,.2f}"

def describe(x):
    cat, fam, brand, trad = x['cat'], x['family'], x['brand'], x['trad']
    b = f" from {BRAND_NAME[brand]}" if brand else ''
    s = []
    if cat in ('sticks', 'cones'):
        kind = 'stick incense' if cat == 'sticks' else ('backflow cone incense' if re.search('backflow', x['title'], re.I) else 'cone incense')
        s.append(f"{E(x['title'])} is {trad + ' ' if trad else ''}{kind}{b}.")
        if fam: s.append(f"It sits in our {FAM_NAME[fam].lower()} scent family.")
        s.append("Light the tip, let the flame catch for a few seconds, then blow it out so it glows and smokes. Burn it in a holder on a heat-safe surface, keep it away from anything that can catch fire, and never leave it burning unattended.")
    elif cat == 'resins':
        s.append(f"{E(x['title'])} is resin incense{b} for burning on a charcoal tablet or an electric resin warmer.")
        s.append("Light a charcoal tablet in a heat-proof burner with sand or ash, wait until it glows and turns gray, then add a small pinch of resin. A little goes a long way. Never leave burning charcoal unattended.")
    elif cat == 'smudge':
        s.append(f"{E(x['title'])}{b} is a smudge or cleansing bundle for clearing a room with smoke.")
        s.append("Light the end, let it smolder, and carry it over a shell or heat-safe bowl to catch embers. Press it out in sand or the bowl when you are done. Never leave smoldering herbs unattended.")
    elif cat == 'holders':
        s.append(f"{E(x['title'])} is an incense holder that keeps sticks or cones upright and catches the ash.")
        s.append("Set it on a stable, heat-safe surface away from curtains and paper. Handmade and natural materials vary slightly from the photo.")
    elif cat == 'burners':
        s.append(f"{E(x['title'])} is built for burning incense, resin or charcoal safely.")
        s.append("Burners and charcoal get hot: use a heat-safe base, handle hot pieces with tongs, and never leave burning charcoal unattended.")
    else:
        s.append(f"{E(x['title'])}{b} is a ritual or aromatherapy candle to burn alongside your incense.")
        s.append("Trim the wick, burn it on a heat-safe surface away from drafts and anything flammable, and never leave a burning candle unattended.")
    s.append(f"Ships from New York City, or choose it in person at {STORE_STREET}, steps from Union Square. Secure checkout is completed on Shopify through namastebookshop.com.")
    return s

# ---------- data ----------
raw = json.load(open(os.path.join(ROOT, 'data', 'all_products.json')))
products = []
for p in raw:
    cat = category(p)
    if not cat or not p.get('images'): continue
    vs = [v for v in p['variants'] if float(v['price']) > 0]
    avail = [v for v in vs if v['available']]
    if not avail: continue
    cmp_ = [float(v['compare_at_price']) for v in avail if v.get('compare_at_price') and float(v['compare_at_price']) > float(v['price'])]
    title = p['title'].strip()
    br = brand_of(title)
    products.append({'id': p['id'], 'handle': p['handle'], 'title': title, 'cat': cat, 'family': family_of(title) if cat != 'holders' and cat != 'burners' else '',
                     'brand': br, 'trad': tradition_of(title, br) if cat in ('sticks', 'cones') else '',
                     'price': min(float(v['price']) for v in avail), 'compare': max(cmp_) if cmp_ else None,
                     'images': [i['src'] for i in p['images'][:6]],
                     'variants': [{'id': v['id'], 'title': v['title'], 'price': v['price'], 'available': v['available'], 'sku': v.get('sku') or ''} for v in vs],
                     'created': p.get('created_at', '')})
products.sort(key=lambda x: x['created'], reverse=True)
_pk = os.path.join(ROOT, 'data', 'pickup.json')
PICKUP = json.load(open(_pk)) if os.path.exists(_pk) else {}
for x in products:
    x['pickup'] = next((PICKUP[str(v['id'])] for v in x['variants'] if v['available'] and PICKUP.get(str(v['id']), {}).get('available')), None)
PICKUP_ON = sum(1 for x in products if x['pickup']) >= 0.5 * max(1, len(products))
_ready = [x['pickup']['ready'] for x in products if x['pickup']]
READY = max(set(_ready), key=_ready.count) if _ready else ''
cat_count = Counter(x['cat'] for x in products)
fam_count = Counter(x['family'] for x in products if x['family'])
brand_count = Counter(x['brand'] for x in products if x['brand'])
trad_count = Counter(x['trad'] for x in products if x['trad'])
BRAND_PAGES = [k for k, n in brand_count.most_common() if n >= 10 and k in BRAND_INTRO]
MIN_PRICE = min(x['price'] for x in products)
MIN_STICK = min(x['price'] for x in products if x['cat'] == 'sticks')
UNDER10 = sum(1 for x in products if x['price'] < 10)
N = len(products)
ABOUT_N = int(round(N, -2)) if N >= 150 else N

# group near-identical listings (same title or same main photo)
parent = {}
def find(a):
    while parent.setdefault(a, a) != a:
        parent[a] = parent[parent[a]]; a = parent[a]
    return a
for x in products:
    h = ('h', x['handle'])
    parent[find(h)] = find(('t', x['cat'], re.sub(r'\s+', ' ', x['title'].lower())))
    parent[find(h)] = find(('i', x['cat'], x['images'][0].split('?')[0].rsplit('/', 1)[-1]))
groups = {}
for x in products: groups.setdefault(find(('h', x['handle'])), []).append(x)
for g in groups.values():
    g.sort(key=lambda y: y['price'])
    same = len({y['title'] for y in g}) == 1
    for y in g:
        y['group'] = g; y['label'] = (y['variants'][0]['sku'] or y['title']) if same else y['title']
leaders, seen = [], set()
for x in products:
    if id(x['group']) not in seen: seen.add(id(x['group'])); leaders.append(x['group'][0])

# ---------- shared pieces ----------
def hours_html():
    return '<dl class="hours">' + ''.join(f'<div><dt>{d}</dt><dd>{h}</dd></div>' for d, h in HOURS) + '</dl>'
def visit_buttons(light=False):
    return (f'<div class="cta"><a class="btn" href="{DIRECTIONS}" rel="noopener" target="_blank">Get directions</a>'
            f'<a class="btn{" ghost" if light else " alt"}" href="tel:{TEL}">Call {PHONE}</a></div>')
def visit_block(full=False):
    pk = (f'<p><b>Reserve online, pick up in store.</b> Choose Pickup at checkout; orders are {READY.lower()}.</p>' if PICKUP_ON else
          f'<p><b>Looking for one scent?</b> Call {PHONE} before you come in.</p>')
    return f'''<div class="visit"><div class="vinfo"><p class="eyebrow dark">Visit the incense shop</p><h2>{STORE_STREET}</h2>
<p class="addr">{STORE_ADDR}<br>On 14th Street just west of Fifth Avenue, about a 4-minute walk from Union Square.</p>
<h3>Hours</h3>{hours_html()}<p class="small">Holiday hours may differ. Call {PHONE} to check before a special trip.</p>
{pk}{visit_buttons()}{'' if full else '<p><a href="/visit/">Directions, subway lines and pickup details &rarr;</a></p>'}</div>
<div class="vmap"><iframe title="Map to {STORE_ADDR}" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div>'''
def store_ld():
    return {"@context": "https://schema.org", "@type": "Store", "name": BRAND, "url": SITE + '/',
            "image": products[0]['images'][0], "description": f"Incense, resins, sage, palo santo, burners and ritual candles at {STORE_ADDR}, steps from Union Square. {LEGAL}",
            "telephone": TEL, "priceRange": "$",
            "address": {"@type": "PostalAddress", "streetAddress": STORE_STREET, "addressLocality": STORE_CITY, "addressRegion": STORE_REGION, "postalCode": STORE_ZIP, "addressCountry": "US"},
            "geo": {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]}, "hasMap": MAP_LINK,
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": o, "closes": c} for d, o, c in HOURS_LD],
            "parentOrganization": {"@type": "Organization", "name": "Wealth Edge Ventures Inc."}}
def ldjson(o): return f'<script type="application/ld+json">{json.dumps(o)}</script>'

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;700&family=Karla:wght@400;500;700&display=swap" rel="stylesheet">'
LOGO = '<svg viewBox="0 0 40 40" width="34" height="34" aria-hidden="true"><path d="M20 38V24" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/><path d="M20 22c-6-4 5-7-1-12s4-6 2-9M24 20c3-3-2-5 1-8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="20" cy="23" r="1.8" fill="currentColor"/></svg>'

def nav():
    links = ''.join(f'<a href="/shop/{CAT_SLUG[k]}/"><i style="background:{CAT_COLOR[k]}"></i>{E(CAT_SHORT[k])}</a>' for k in CATS)
    return f'''<header class="top"><div class="bar"><a href="/visit/">Visit us: {STORE_STREET}, steps from Union Square</a><span>Open daily from 11 AM</span>{'<span>Reserve online, pick up in store</span>' if PICKUP_ON else ''}</div>
<div class="nav wrap"><a class="logo" href="/" aria-label="{BRAND} home">{LOGO}<span><b>Namaste</b> Incense</span></a>
<button class="menu" aria-label="Menu" aria-expanded="false" onclick="document.body.classList.toggle('open');this.setAttribute('aria-expanded',document.body.classList.contains('open'))"><span></span><span></span></button>
<nav class="links"><a href="/visit/" class="vlink">Visit</a><a href="/shop/">Shop all</a>{links}<a href="/brands/">Brands</a><a href="/about/">About</a></nav></div></header>'''

def footer():
    return f'''<footer class="foot"><div class="wrap grid4">
<div><a class="logo light" href="/">{LOGO}<span><b>Namaste</b> Incense</span></a><p class="legal">{LEGAL}</p>
<p class="small">Orders are checked out on Shopify through namastebookshop.com, which processes payment and ships each order from New York City.</p></div>
<div><h4>Shop</h4>{''.join(f'<a href="/shop/{CAT_SLUG[k]}/">{E(CATS[k][0])}</a>' for k in CATS)}<a href="/gifts-under-10/">Gifts under $10</a></div>
<div><h4>Explore</h4>{''.join(f'<a href="/scents/{k}/">{E(FAM_NAME[k])}</a>' for k, *_ in FAMILIES if fam_count[k])}<a href="/brands/">Brands</a><a href="/indian-incense/">Indian incense</a>{'<a href="/japanese-incense/">Japanese incense</a>' if trad_count['Japanese'] else ''}<a href="/guide/how-to-burn-resin-incense/">How to burn resin</a></div>
<div><h4>Visit</h4><p class="small foottxt">{STORE_ADDR}</p>{''.join(f'<p class="small foottxt">{d}: {h}</p>' for d, h in HOURS)}<a href="tel:{TEL}">Call {PHONE}</a><a href="{DIRECTIONS}" rel="noopener" target="_blank">Get directions</a><a href="/visit/">Visit &amp; pickup info</a><a href="/where-to-buy-incense-in-manhattan/">Where to buy incense in Manhattan</a>
<h4 class="mt">Help</h4><a href="/about/">About us</a><a href="/shipping/">Shipping</a><a href="/returns/">Returns</a><a href="/privacy/">Privacy</a><a href="/terms/">Terms</a></div>
</div><div class="wrap legalline">{LEGAL} &copy; {datetime.date.today().year} Wealth Edge Ventures Inc.</div></footer>'''

SITEMAP = []
def page(path, title, desc, body, extra_head='', canonical=True, index=True):
    url = SITE + path
    robots = '<meta name="robots" content="noindex,nofollow">' if PREVIEW else ''
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">{robots}{f'<link rel="canonical" href="{url}">' if canonical else ''}
<meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website">
<meta name="theme-color" content="#16302a"><link rel="icon" href="/favicon.svg" type="image/svg+xml">{FONTS}<link rel="stylesheet" href="/assets/site.css"><script>window.NI_BASE={json.dumps(BASE)}</script>{extra_head}</head>
<body>{nav()}<main>{body}</main>{footer()}<div class="actionbar"><a href="tel:{TEL}">Call</a><a href="{DIRECTIONS}" rel="noopener" target="_blank">Directions</a><a href="/visit/">Hours</a></div><script src="/assets/site.js" defer></script></body></html>'''
    if BASE: doc = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{BASE}/', doc)
    out = os.path.join(DIST, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(DIST, path.strip('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w').write(doc)
    if index and canonical: SITEMAP.append(path)

def tag_of(x):
    return FAM_NAME.get(x['family']) or CATS[x['cat']][0]
def card(x):
    n = len(x['group'])
    pre = f'<small>{n} options from</small> ' if n > 1 else (f'<s>{money(x["compare"])}</s> ' if x['compare'] else '')
    return (f'<a class="card" href="/products/{x["handle"]}/"><div class="ph"><img loading="lazy" src="{img(x["images"][0],400)}" alt="{E(x["title"])}" width="400" height="400"></div>'
            f'<div class="meta"><span class="tag" style="--c:{CAT_COLOR[x["cat"]]}">{E(tag_of(x))}</span><h3>{E(x["title"])}</h3><p class="price">{pre}{money(x["price"])}</p></div></a>')

# ---------- build ----------
if os.path.exists(DIST): shutil.rmtree(DIST)
os.makedirs(os.path.join(DIST, 'data'))
shutil.copytree(os.path.join(ROOT, 'src', 'assets'), os.path.join(DIST, 'assets'))
for f in os.listdir(os.path.join(ROOT, 'src', 'static')): shutil.copy(os.path.join(ROOT, 'src', 'static', f), DIST)
compact = [{'h': x['handle'], 't': x['title'], 'c': x['cat'], 'f': x['family'], 'b': x['brand'], 'p': x['price'],
            'k': x['compare'] if len(x['group']) == 1 else None, 'n': len(x['group']), 'i': img(x['images'][0], 400),
            'd': max(y['created'] for y in x['group'])[:10]} for x in leaders]
json.dump(compact, open(os.path.join(DIST, 'data', 'catalog.json'), 'w'), separators=(',', ':'))
json.dump({'cats': {k: {'name': CATS[k][0], 'slug': CAT_SLUG[k], 'color': CAT_COLOR[k]} for k in CATS}, 'fams': FAM_NAME,
           'brands': {k: BRAND_NAME[k] for k in brand_count}, 'built': datetime.datetime.now().isoformat(timespec='minutes')},
          open(os.path.join(DIST, 'data', 'meta.json'), 'w'))

def pick(pool, n): 
    pool = sorted(pool, key=lambda x: -x['price']); s = len(pool) // 5
    return pool[s:s + n]

# ---- Home ----
fam_tiles = ''.join(f'<a class="scent" href="/scents/{k}/" style="--c:{c}"><b>{E(FAM_NAME[k])}</b><span>{E(FAM_BLURB[k])}</span><small>{fam_count[k]} items</small></a>'
                    for (k, *_), c in zip(FAMILIES, ['#e8a33d', '#b8862b', '#8a6a4f', '#6f8f5a', '#c9748f', '#c8662f']) if fam_count[k])
tiles = ''.join(f'''<a class="tile" href="/shop/{CAT_SLUG[k]}/" style="--c:{CAT_COLOR[k]}"><img loading="lazy" src="{img(next(x for x in leaders if x['cat']==k)['images'][0],500)}" alt=""><div><h3>{E(CATS[k][0])}</h3><p>{cat_count[k]} items</p></div></a>''' for k in CATS)
resins = [x for x in leaders if x['cat'] == 'resins']
gifts = sorted([x for x in leaders if x['price'] < 10 and x['cat'] in ('sticks', 'cones', 'smudge', 'holders', 'resins')], key=lambda x: (x['cat'], -x['price']))
gifts = [g for i, g in enumerate(gifts) if i % max(1, len(gifts) // 8) == 0][:8]
brand_chips = ''.join(f'<a class="chip" href="/brands/{k}/">{E(BRAND_NAME[k])} <small>{brand_count[k]}</small></a>' for k in BRAND_PAGES)
home = f'''<section class="hero"><div class="wrap hero-in">
<p class="eyebrow">{STORE_STREET} &middot; Union Square &middot; New York City</p>
<h1>Incense, sacred resins and sage, <em>steps from Union Square.</em></h1>
<p class="lede">About {ABOUT_N:,} incense sticks, cones, resins, smudge bundles, holders, burners and ritual candles at {STORE_STREET}. Sticks from {money(MIN_STICK)}. Open daily from 11 AM.{f" Reserve online and pick up in store; orders are {READY.lower()}." if PICKUP_ON else ""}</p>
<div class="cta"><a class="btn" href="{DIRECTIONS}" rel="noopener" target="_blank">Get directions</a><a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a><a class="btn ghost" href="/shop/">Shop online</a></div></div></section>
<section class="wrap"><div class="sechead"><h2>Shop by scent family</h2><a href="/shop/">All incense &rarr;</a></div><div class="scents">{fam_tiles}</div></section>
<section class="wrap">{visit_block()}</section>
<section class="wrap"><div class="sechead"><h2>Why stop by</h2></div><ul class="whys">
<li><b>About {ABOUT_N:,} items</b><span>Sticks, cones, resins, sage, palo santo, holders, burners and candles, all listed online so you can pick your scents before you come in.</span></li>
<li><b>Sticks from {money(MIN_STICK)}</b><span>Every listing shows its price, and {UNDER10:,} items are under $10.</span></li>
{f'<li><b>Ready in about 2 hours</b><span>Buy online, choose Pickup at checkout, and collect at {STORE_STREET}. Orders are {READY.lower()}.</span></li>' if PICKUP_ON and '2 hour' in READY else (f'<li><b>Reserve, then pick up</b><span>Orders are {READY.lower()}.</span></li>' if PICKUP_ON else '')}
<li><b>Open daily from 11 AM</b><span>Until 8 PM Monday to Thursday, 9 PM Friday and Saturday, and 7 PM Sunday.</span></li>
<li><b>Brands people ask for</b><span>{', '.join(BRAND_NAME[k] for k in BRAND_PAGES[:6])} and more.</span></li>
<li><b>On 14th Street</b><span>About 0.2 miles from both the 14 St&ndash;Union Square and 14 St/6 Av subway stations, and on the M14 bus routes.</span></li></ul></section>
<section class="wrap"><div class="sechead"><h2>Sacred resins</h2><a href="/shop/{CAT_SLUG['resins']}/">All {cat_count['resins']} resins &rarr;</a></div>
<p class="intro">Frankincense, myrrh, copal, benzoin and dragon's blood have been burned on coals for thousands of years. New to resin? Read <a href="/guide/how-to-burn-resin-incense/">how to burn resin incense</a>, then pick up <a href="/shop/{CAT_SLUG['burners']}/">charcoal and a burner</a>.</p>
<div class="grid">{''.join(card(x) for x in pick(resins, 4))}</div></section>
<section class="wrap"><div class="sechead"><h2>Gifts under $10</h2><a href="/gifts-under-10/">See all {UNDER10} &rarr;</a></div><div class="grid">{''.join(card(x) for x in gifts)}</div></section>
<section class="wrap"><div class="sechead"><h2>Pick your aisle</h2><a href="/shop/">See everything &rarr;</a></div><div class="tiles">{tiles}</div></section>
<section class="wrap"><div class="sechead"><h2>Brands we carry</h2><a href="/brands/">All brands &rarr;</a></div><div class="chips">{brand_chips}</div></section>
<section class="band"><div class="wrap band-in"><div><h2>{"Reserve online, pick up in store" if PICKUP_ON else "Choose in person"}</h2><p>Every listing has its own photos, price and live stock. {"Reserve online and collect it on 14th Street, or have it shipped from New York City." if PICKUP_ON else "Call ahead, or order online and have it shipped from New York City."}</p>{visit_buttons(True)}</div>
<ol class="steps"><li><b>Find your scent</b><span>Filter by aisle, scent family, brand or price.</span></li>{"<li><b>Choose Pickup at checkout</b><span>Pay securely on Shopify. Orders are " + READY.lower() + ".</span></li><li><b>Collect it</b><span>" + STORE_ADDR + ".</span></li>" if PICKUP_ON else "<li><b>Call ahead</b><span>" + PHONE + "</span></li><li><b>Visit</b><span>" + STORE_ADDR + ".</span></li>"}</ol></div></section>'''
page('/', f'{BRAND} | Incense Shop near Union Square, NYC | 2 W 14th St',
     f'Incense shop at {STORE_ADDR}, steps from Union Square. About {ABOUT_N:,} incense sticks, cones, resins, sage, palo santo and burners, sticks from {money(MIN_STICK)}. In-store pickup, open daily from 11 AM.',
     home, ldjson({"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": SITE, "parentOrganization": {"@type": "Organization", "name": "Wealth Edge Ventures Inc."}}) + ldjson(store_ld()))

# ---- Shop pages ----
def shop_page(path, title, desc, h1, sub, cat='', fam='', brand='', under='', intro=''):
    chips = '<button class="f on" data-cat="">All</button>' + ''.join(f'<button class="f" data-cat="{k}" style="--c:{CAT_COLOR[k]}">{E(CAT_SHORT[k])} <small>{cat_count[k]}</small></button>' for k in CATS)
    fams = '<option value="">All scents</option>' + ''.join(f'<option value="{k}">{E(FAM_NAME[k])}</option>' for k, *_ in FAMILIES if fam_count[k])
    brands = '<option value="">All brands</option>' + ''.join(f'<option value="{k}">{E(BRAND_NAME[k])}</option>' for k, _ in sorted(brand_count.items(), key=lambda kv: BRAND_NAME[kv[0]]))
    pool = [x for x in leaders if (not cat or x['cat'] == cat) and (not fam or x['family'] == fam) and (not brand or x['brand'] == brand) and (not under or x['price'] < float(under))][:48]
    preset = 'y' if (cat or fam or brand or under) else ''
    body = f'''<section class="wrap shophead"><h1>{E(h1)}</h1><p>{E(sub)}</p>{intro}</section>
<section class="wrap shop" data-preset="{preset}" data-cat="{cat}" data-fam="{fam}" data-brand="{brand}" data-under="{under}">
<div class="filters"><div class="fcats">{chips}</div><div class="frow"><input type="search" id="q" placeholder="Search scents, brands, burners" aria-label="Search">
<select id="fam" aria-label="Scent family">{fams}</select><select id="brand" aria-label="Brand">{brands}</select>
<select id="price" aria-label="Price"><option value="">Any price</option><option value="0-5">Under $5</option><option value="0-10">Under $10</option><option value="10-25">$10 to $25</option><option value="25-99999">$25 and up</option></select>
<select id="sort" aria-label="Sort"><option value="new">Newest</option><option value="lo">Price: low to high</option><option value="hi">Price: high to low</option><option value="az">A to Z</option></select></div>
<p class="count" id="count"></p></div><div class="grid" id="grid">{''.join(card(x) for x in pool)}</div><div class="more"><button class="btn" id="more" hidden>Show more</button></div></section>'''
    page(path, title, desc, body)

shop_page('/shop/', f'Shop Incense Online, Pick Up near Union Square | {BRAND}', f'Browse {N:,} incense sticks, cones, resins, sage, palo santo, holders, burners and ritual candles. Sticks from {money(MIN_STICK)}. Pick up at {STORE_STREET}, NYC, or ship.',
          'Shop all incense', f'{N:,} items in stock across {len(CATS)} aisles. Reserve online and pick up at {STORE_STREET}, or have it shipped.')
for k in CATS:
    shop_page(f'/shop/{CAT_SLUG[k]}/', f'{CATS[k][0]} in NYC near Union Square | {BRAND}', f'{CATS[k][1]} {cat_count[k]} items at {BRAND}, {STORE_STREET}, NYC. Pick up in store or ship.',
              CATS[k][0], CATS[k][1], cat=k)
for k, n, _, b in FAMILIES:
    if fam_count[k]:
        shop_page(f'/scents/{k}/', f'{n} Incense in NYC | {BRAND}', f'{b} {fam_count[k]} {n.lower()} incense, resin and smudge items at {STORE_STREET} near Union Square, or shipped from NYC.',
                  f'{n} incense', b, fam=k)
shop_page('/gifts-under-10/', f'Incense Gifts Under $10 in NYC | {BRAND}', f'{UNDER10} incense sticks, cones, sage bundles, holders and candles under $10 at {STORE_STREET}, steps from Union Square.',
          'Gifts under $10', f'{UNDER10} items under $10: stocking stuffers, hostess gifts and first-time incense kits.', under='10')
# brand landing pages
brand_list = ''
for k in BRAND_PAGES:
    shop_page(f'/brands/{k}/', f'{BRAND_NAME[k]} Incense in NYC near Union Square | {BRAND}', f'{BRAND_NAME[k]}: {brand_count[k]} items in stock at {STORE_STREET}, Manhattan. {BRAND_INTRO[k][:110]}',
              f'{BRAND_NAME[k]} in New York City', f'{brand_count[k]} {BRAND_NAME[k]} items in stock. Pick up at {STORE_STREET} or have them shipped.', brand=k,
              intro=f'<p class="intro">{E(BRAND_INTRO[k])}</p>')
    brand_list += f'<li><a href="/brands/{k}/"><b>{E(BRAND_NAME[k])}</b></a> <span class="small">{brand_count[k]} items</span><br>{E(BRAND_INTRO[k])}</li>'
others = ', '.join(BRAND_NAME[k] for k, _ in brand_count.most_common() if k not in BRAND_PAGES)

# ---- Product pages ----
for x in products:
    cat = x['cat']
    avail = [v for v in x['variants'] if v['available']]; v0 = avail[0]
    gallery = ''.join(f'<button class="th{" on" if i==0 else ""}" data-src="{img(u,1000)}"><img loading="lazy" src="{img(u,160)}" alt="" width="80" height="80"></button>' for i, u in enumerate(x['images']))
    opts = ''
    if len(x['variants']) > 1:
        opts = '<label class="vlab">Option<select id="variant">' + ''.join(
            f'<option value="{v["id"]}"{" disabled" if not v["available"] else ""}{" selected" if v is v0 else ""}>{E(v["title"])}{"" if v["available"] else " (sold out)"}</option>' for v in x['variants']) + '</select></label>'
    facts = [('Aisle', f'<a href="/shop/{CAT_SLUG[cat]}/">{E(CATS[cat][0])}</a>')]
    if x['family']: facts.append(('Scent family', f'<a href="/scents/{x["family"]}/">{E(FAM_NAME[x["family"]])}</a>'))
    if x['brand']: facts.append(('Brand', f'<a href="/brands/{x["brand"]}/">{E(BRAND_NAME[x["brand"]])}</a>' if x['brand'] in BRAND_PAGES else E(BRAND_NAME[x['brand']])))
    if x['trad']: facts.append(('Style', E(x['trad'])))
    if v0['sku']: facts.append(('SKU', E(v0['sku'])))
    facts.append(('Ships from', 'New York City'))
    if x['pickup']: facts.append(('Pickup', f'<a href="/visit/">{STORE_STREET}</a>'))
    related = [y for y in leaders if y['cat'] == cat and y['family'] == x['family'] and y['group'] is not x['group']][:4]
    related += [y for y in leaders if y['cat'] == cat and y['group'] is not x['group'] and y not in related][:4 - len(related)]
    sibs = ''
    if len(x['group']) > 1:
        sibs = '<div class="sibs"><h3>Choose yours</h3><p class="small">Each option is a separate listing with its own price.</p>' + ''.join(
            f'<a class="sib{" on" if y is x else ""}" href="/products/{y["handle"]}/"><img loading="lazy" src="{img(y["images"][0],120)}" alt="" width="60" height="60"><span>{E(y["label"])}</span><b>{money(y["price"])}</b></a>' for y in x['group']) + '</div>'
    desc = describe(x)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": x['title'], "image": x['images'][:3], "sku": v0['sku'] or str(v0['id']),
          "brand": {"@type": "Brand", "name": BRAND_NAME.get(x['brand'], BRAND)}, "category": CATS[cat][0], "url": f"{SITE}/products/{x['handle']}/",
          "description": re.sub('<[^>]+>', '', ' '.join(desc)),
          "offers": {"@type": "Offer", "price": f"{float(v0['price']):.2f}", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
                     "itemCondition": "https://schema.org/NewCondition", "url": f"{SITE}/products/{x['handle']}/", "seller": {"@type": "Organization", "name": "Wealth Edge Ventures Inc."}}}
    cmp_ = f'<s id="cmp">{money(x["compare"])}</s>' if x['compare'] else '<s id="cmp" hidden></s>'
    btns = f'<div class="pbtns"><a href="{DIRECTIONS}" rel="noopener" target="_blank">Directions</a><a href="tel:{TEL}">Call</a><a href="/visit/">Hours</a></div>'
    if x['pickup']:
        pk = (f'<div class="pickup"><h3>Reserve online, pick up in store</h3><p>Pickup available at <b>{STORE_ADDR}</b>, steps from Union Square. {E(x["pickup"]["ready"])}.</p>'
              f'<p class="small">Tap Buy now, then choose <b>Pickup</b> at checkout. Questions? Call <a href="tel:{TEL}">{PHONE}</a>.</p>{btns}</div>')
    else:
        pk = (f'<div class="pickup"><h3>See it in person</h3><p>Visit us at <b>{STORE_ADDR}</b>, steps from Union Square. Call <a href="tel:{TEL}">{PHONE}</a> before you come to check it is in stock.</p>{btns}</div>')
    body = f'''<nav class="wrap crumbs"><a href="/shop/">Shop</a> / <a href="/shop/{CAT_SLUG[cat]}/">{E(CATS[cat][0])}</a></nav>
<section class="wrap pdp" data-handle="{x['handle']}"><div class="gallery"><div class="main"><img id="mainimg" src="{img(x['images'][0],1000)}" alt="{E(x['title'])}" width="1000" height="1000"></div><div class="thumbs">{gallery if len(x['images'])>1 else ''}</div></div>
<div class="info"><span class="tag" style="--c:{CAT_COLOR[cat]}">{E(CATS[cat][0])}</span><h1>{E(x['title'])}</h1>
<p class="pprice">{cmp_} <span id="price">{money(v0['price'])}</span></p><p class="stock" id="stock"><i></i><span>In stock</span></p>{opts}{sibs}
<a class="btn buy" id="buy" href="{SHOP}/cart/{v0['id']}:1{CART_ATTR}" rel="nofollow">Buy now</a>
<p class="note">Checkout opens on Shopify (namastebookshop.com), where you can choose shipping{" or in-store pickup" if x['pickup'] else ""} and review your order before paying.</p>
{pk}<div class="desc">{''.join(f'<p>{s}</p>' for s in desc)}</div><dl class="facts">{''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in facts)}</dl>
<p class="small"><a href="/shipping/">Shipping</a> &middot; <a href="/returns/">Returns</a></p></div></section>
<section class="wrap"><div class="sechead"><h2>More like this</h2></div><div class="grid">{''.join(card(y) for y in related)}</div></section>'''
    page(f"/products/{x['handle']}/", f"{x['title']} | {BRAND} NYC",
         f"{x['title']} for {money(v0['price'])}. " + (f"Reserve online and pick up at {STORE_STREET} near Union Square, or ship from NYC." if x['pickup'] else f"At {STORE_STREET} near Union Square, or ship from NYC."),
         body, ldjson(ld) + f'<script>window.NI_PRODUCT={json.dumps({"handle": x["handle"], "cartAttr": CART_ATTR, "shop": SHOP})}</script>')

# ---- Info pages ----
def info(path, title, desc, h1, body, extra_head=''):
    page(path, f'{title} | {BRAND}', desc, f'<section class="wrap prose"><h1>{h1}</h1>{body}<p class="legal">{LEGAL}</p></section>', extra_head)

info('/brands/', 'Incense Brands We Carry', f'HEM, Satya, Morning Star and more incense brands in stock at {STORE_STREET}, steps from Union Square in Manhattan.', 'Incense brands we carry', f'''
<p class="lead">These are the brands with the most items on our shelves right now. Counts update every day from live stock.</p><ul class="brandlist">{brand_list}</ul>
{f"<p>We also carry {E(others)}.</p>" if others else ""}<p><a class="btn" href="/shop/">Shop all incense</a></p>''')

def trad_page(path, trad, h1, title, lead, more):
    items = [x for x in leaders if x['trad'] == trad]
    info(path, title, f'{lead[:150]}', h1, f'<p class="lead">{lead}</p>{more}<div class="grid">{"".join(card(x) for x in items[:24])}</div><p><a class="btn" href="/shop/{CAT_SLUG["sticks"]}/">All incense sticks</a></p>')
info_brands = ', '.join(f'<a href="/brands/{k}/">{E(BRAND_NAME[k])}</a>' for k in BRAND_PAGES if k in ('hem', 'satya', 'prabhujis'))
trad_page('/indian-incense/', 'Indian', 'Indian incense in New York City', 'Indian Incense: Nag Champa, Masala & Dhoop in NYC',
          f'Hand-rolled masala sticks, dhoop and Nag Champa from India: {trad_count["Indian"]} Indian incense items in stock at {STORE_STREET}, steps from Union Square.',
          f'<h2>What to try</h2><ul><li><a href="/scents/nag-champa/">Nag Champa</a>: the classic sweet, powdery blend.</li><li>Dhoop cones and sticks: dense, rich and smoky.</li><li>Intention blends such as Money, Protection and Good Luck, sold under many brands.</li></ul><p>Brands: {info_brands}.</p>')
if trad_count['Japanese']:
    trad_page('/japanese-incense/', 'Japanese', 'Japanese incense in New York City', 'Japanese Incense in NYC',
              f'Thin, low-smoke Japanese sticks, including the Morning Star line by Nippon Kodo: {trad_count["Japanese"]} items in stock at {STORE_STREET}.',
              '<p>Japanese incense is usually burned without a bamboo core, so it gives off less smoke than most Indian sticks. It works well in small apartments and offices.</p>')

info('/guide/how-to-burn-resin-incense/', 'How to Burn Resin Incense (Frankincense, Myrrh, Copal)', 'A step-by-step guide to burning frankincense, myrrh, copal and other resins on charcoal, with what you need and safety tips.',
     'How to burn resin incense', f'''<p class="lead">Resins such as frankincense, myrrh, copal and benzoin do not light on their own. They melt on a heat source and release their scent as smoke.</p>
<h2>What you need</h2><ul><li>Resin: see our <a href="/shop/{CAT_SLUG['resins']}/">{cat_count['resins']} sacred resins</a>.</li><li>Charcoal tablets made for incense and a heat-proof <a href="/shop/{CAT_SLUG['burners']}/">burner or censer</a>.</li><li>Sand, salt or ash to fill the burner, and tongs.</li></ul>
<h2>Step by step</h2><ol><li>Fill the burner about two-thirds with sand or ash so the heat does not reach the bottom.</li><li>Hold a charcoal tablet with tongs and light its edge. It will spark across the surface.</li><li>Set it on the sand and wait until it is covered in gray ash, usually a few minutes.</li><li>Place a small pinch of resin, about the size of a pea, on top. Add more as it burns away.</li><li>When you are done, let the charcoal burn out fully in the burner. Do not pour water on hot ceramic.</li></ol>
<h2>Safety</h2><ul><li>Charcoal and burners get very hot. Use a heat-proof surface and keep it away from children, pets, curtains and paper.</li><li>Burn in a ventilated room and never leave burning charcoal unattended.</li></ul><p><a class="btn" href="/shop/{CAT_SLUG['resins']}/">Shop sacred resins</a></p>''')

info('/about/', 'About', f'About {BRAND}, the incense shop at {STORE_ADDR}, steps from Union Square. A brand of Wealth Edge Ventures Inc.', 'About Namaste Incense', f'''
<p class="lead">{BRAND} is an incense shop at {STORE_ADDR}, on 14th Street just west of Fifth Avenue and a few minutes' walk from Union Square.</p>
<p>We focus on one thing: smoke. Stick and cone incense, sacred resins and the charcoal to burn them, white sage and palo santo, holders and ash catchers, censers and backflow burners, and ritual candles to go alongside. About {ABOUT_N:,} items are listed online with their own photos and prices, and stock updates every day.{" Reserve online and choose Pickup at checkout to collect in store." if PICKUP_ON else ""}</p>
<h2>Visit</h2><p>{STORE_ADDR}. Call <a href="tel:{TEL}">{PHONE}</a>.</p>{hours_html()}{visit_buttons()}<p><a href="/visit/">Directions, subway lines and pickup details &rarr;</a></p>
<h2>Who we are</h2><p>{LEGAL} Online orders are checked out on Shopify through <a href="{SHOP}" rel="noopener">namastebookshop.com</a>, which processes payment and fulfills orders, including in-store pickups. Products ship from New York City.</p>
<p>Looking for books, tarot decks or crystals? Visit <a href="{SHOP}" rel="noopener">namastebookshop.com</a>.</p>
<h2>What we carry</h2><ul>{''.join(f'<li><a href="/shop/{CAT_SLUG[k]}/">{E(CATS[k][0])}</a>: {E(CATS[k][1])}</li>' for k in CATS)}</ul>
<h2>Burn safely</h2><p>Burn incense, resin, herbs and candles on heat-safe surfaces, away from anything flammable, in a ventilated room, and never leave them unattended. Traditional uses of incense are shared for interest only and are not medical advice.</p>
<h2>Get in touch</h2><p>Call <a href="tel:{TEL}">{PHONE}</a>, or see the <a href="{SHOP}/policies/contact-information">store contact page</a> for order questions.</p>''', ldjson(store_ld()))

TRANSIT = '''<ul class="transit"><li><b>14 St&ndash;Union Square</b> <span class="lines">4 5 6 L N Q R W</span><br>About 0.2 miles east, roughly a 4-minute walk west along 14th Street.</li>
<li><b>14 St/6 Av</b> <span class="lines">F M L</span>, connected to <b>14 St</b> <span class="lines">1 2 3</span><br>About 0.2 miles west at Sixth Avenue, roughly a 4-minute walk east along 14th Street.</li>
<li><b>PATH</b> 14th Street station at Sixth Avenue.</li><li><b>Bus</b> M14A and M14D Select Bus Service run along 14th Street.</li></ul>
<p class="small">Some lines run only at certain times (for example, the W runs weekdays and the M weekdays during the day). Check the MTA before you travel.</p>'''
info('/visit/', 'Visit Our Incense Shop near Union Square', f'Directions, hours, subway lines and in-store pickup for {BRAND} at {STORE_ADDR}, steps from Union Square.', 'Visit us at 2 West 14th Street', f'''
<p class="lead">We are at {STORE_ADDR}, on 14th Street just west of Fifth Avenue, where Union Square, Greenwich Village, Chelsea and the Flatiron District meet.</p>
{visit_block(full=True)}<h2>Getting here</h2>{TRANSIT}
<h2>{"Reserve online, pick up in store" if PICKUP_ON else "Looking for one scent?"}</h2>
{f"<ol><li>Find your incense in the <a href='/shop/'>online shop</a>.</li><li>Tap Buy now and choose <b>Pickup</b> at checkout.</li><li>Orders are {READY.lower()}. Come to {STORE_ADDR} during open hours.</li></ol><p>Questions about a pickup? Call <a href='tel:{TEL}'>{PHONE}</a>.</p>" if PICKUP_ON else f"<p>Call <a href='tel:{TEL}'>{PHONE}</a> before you come in.</p>"}''', ldjson(store_ld()))

info('/where-to-buy-incense-in-manhattan/', 'Where to Buy Incense in Manhattan: Union Square, East Village, Midtown',
     f'Looking for an incense shop in Manhattan? {BRAND} is at {STORE_ADDR}, steps from Union Square, with about {ABOUT_N:,} incense items, sticks from {money(MIN_STICK)} and in-store pickup.',
     'Where to buy incense in Manhattan', f'''<p class="lead">Searching for an incense shop near you in Manhattan? We are on 14th Street at Fifth Avenue, one of the easiest corners in the city to reach by subway and bus. Here is what we stock and how to get here from your neighborhood.</p>
<h2>What you will find at {STORE_STREET}</h2><ul><li>About {ABOUT_N:,} incense items listed online across {len(CATS)} aisles, with {UNDER10:,} under $10 and sticks from {money(MIN_STICK)}.</li>
<li>Indian masala and dhoop incense, Nag Champa, {"Japanese incense, " if trad_count['Japanese'] else ""}resin incense, sage, palo santo, charcoal, burners and holders.</li>
<li>Brands including {', '.join(BRAND_NAME[k] for k in BRAND_PAGES[:5])}.</li>{f"<li>Reserve online and pick up in store; orders are {READY.lower()}.</li>" if PICKUP_ON else ""}<li>Open daily from 11 AM. See <a href="/visit/">full hours</a>.</li></ul>
<h2>Getting here from your neighborhood</h2><ul>
<li><b>Union Square and Gramercy:</b> walk west on 14th Street past Union Square West and University Place to Fifth Avenue.</li>
<li><b>East Village and East 14th Street:</b> walk west along 14th Street, ride the M14A or M14D west, or take the L from First or Third Avenue to 14 St&ndash;Union Square or Sixth Avenue.</li>
<li><b>Midtown and Times Square:</b> take the N, Q, R or W from Times Sq&ndash;42 St to 14 St&ndash;Union Square, or the 1, 2 or 3 to 14 St and walk east on 14th Street.</li>
<li><b>Hell's Kitchen and Midtown West:</b> take the C or E from 50 St to 14 St, then the L one stop east to Sixth Avenue, or walk east along 14th Street from Eighth Avenue (about half a mile).</li>
<li><b>Chelsea:</b> take the 1, 2, 3, F, M or L to 14th Street at Seventh or Sixth Avenue and walk east.</li>
<li><b>Flatiron and NoMad:</b> walk south on Fifth Avenue to 14th Street.</li>
<li><b>Greenwich Village and the West Village:</b> walk north on Fifth Avenue, or take the 1, 2 or 3 to 14 St.</li></ul>
<h2>Tips for your visit</h2><ul><li>Browse the <a href="/shop/">online shop</a> first and note the scents you want.</li><li>Shopping for one exact item? Call <a href="tel:{TEL}">{PHONE}</a> first, or reserve it online for pickup.</li><li>New to resin? Read <a href="/guide/how-to-burn-resin-incense/">how to burn resin incense</a>.</li></ul>{visit_block()}''', ldjson(store_ld()))

def policy(path, title, slug, intro):
    info(path, title, f'{title} for {BRAND} orders.', title, f'<p class="lead">{intro}</p><p>Because checkout and fulfillment run through our Shopify store, the full and current {title.lower()} is published there:</p><p><a class="btn" href="{SHOP}/policies/{slug}">Read the full {title.lower()}</a></p>')
policy('/shipping/', 'Shipping Policy', 'shipping-policy', f'Orders ship from New York City. Shipping options and costs are shown at checkout before you pay.{" You can also choose Pickup at checkout and collect your order at " + STORE_ADDR + "." if PICKUP_ON else ""}')
policy('/returns/', 'Refund Policy', 'refund-policy', 'If something is not right with your order, the refund policy below explains eligibility, timing and how to start a return.')
policy('/privacy/', 'Privacy Policy', 'privacy-policy', 'This site does not use accounts or collect payment details; checkout and payment are handled by Shopify. The privacy policy below covers the data collected at checkout.')
policy('/terms/', 'Terms of Service', 'terms-of-service', 'Purchases made through this site are completed on Shopify and governed by the terms below.')
page('/404.html', f'Page not found | {BRAND}', 'Page not found', '<section class="wrap prose"><h1>That scent has drifted off</h1><p>The page you were looking for may have sold out or moved.</p><p><a class="btn" href="/shop/">Back to the shop</a></p></section>', canonical=False, index=False)

# ---- sitemap / robots / CNAME ----
open(os.path.join(DIST, '.nojekyll'), 'w').write('')
if not BASE and SITE.startswith('https://') and 'github.io' not in SITE:
    open(os.path.join(DIST, 'CNAME'), 'w').write(SITE.split('://', 1)[1] + '\n')
open(os.path.join(DIST, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{u}</loc></url>' for u in SITEMAP) + '</urlset>')
open(os.path.join(DIST, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n' if PREVIEW else f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
json.dump({'count': N, 'aisles': {CATS[k][0]: cat_count[k] for k in CATS}, 'families': dict(fam_count), 'brands': dict(brand_count), 'traditions': dict(trad_count),
           'pickup_on': PICKUP_ON, 'ready': READY, 'min_price': MIN_PRICE, 'min_stick': MIN_STICK, 'under10': UNDER10, 'brand_pages': BRAND_PAGES, 'pages': len(SITEMAP),
           'products': [{'title': x['title'], 'handle': x['handle'], 'gid': f"gid://shopify/Product/{x['id']}", 'aisle': CATS[x['cat']][0], 'price': x['price']} for x in products]},
          open(os.path.join(ROOT, 'data', 'ni_products.json'), 'w'), indent=1)
print(f"built {N} products ({len(leaders)} cards), {len(SITEMAP)} sitemap urls, preview={PREVIEW}, base={BASE!r}, site={SITE}", dict(cat_count))
