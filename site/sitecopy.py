"""Namaste Incense (namasteincense.com): the full incense shop. All copy on this site is written for this site only."""
import re
E = __import__('html').escape

AISLES = {
 'sticks':  ('Incense Sticks', 'Sticks', 'incense-sticks', 'Masala, dhoop and charcoal-free sticks from India, Japan, Tibet and the American Southwest.', '#e8a33d'),
 'cones':   ('Cones & Backflow Cones', 'Cones', 'cones-backflow', 'Classic cones and backflow cones that send smoke pouring down a fountain burner.', '#c8662f'),
 'resins':  ('Sacred Resins', 'Resins', 'sacred-resins', "Frankincense, myrrh, copal, benzoin, dragon's blood, amber and bakhoor to burn on charcoal.", '#b8862b'),
 'smudge':  ('Sage, Palo Santo & Smudge', 'Sage & Palo Santo', 'sage-palo-santo', 'White sage, blue sage, cedar, sweetgrass, palo santo and ready-made cleansing kits.', '#6f8f5a'),
 'holders': ('Holders & Ash Catchers', 'Holders', 'holders-ash-catchers', 'Wood boats, coffin boxes, ceramic and brass holders that catch every bit of ash.', '#8a6a4f'),
 'burners': ('Burners, Backflow & Charcoal', 'Burners & Charcoal', 'burners-charcoal', 'Censers, cauldrons, smudge bowls, backflow fountains, charcoal tablets and tongs.', '#5b4a6b'),
 'candles': ('Ritual & Aromatherapy Candles', 'Candles', 'ritual-candles', 'Herbal, smudge, chakra, intention and ritual candles to burn beside your incense.', '#b5532a'),
}
def assign(x): return x['base']

FAM_BLURB = {
 'nag-champa': 'The sweet, powdery champaca and sandalwood blend most people picture when they think of incense.',
 'resinous': "Frankincense, myrrh, copal, benzoin, dragon's blood and amber: the oldest scents in the temple.",
 'woods': 'Sandalwood, cedar, palo santo, pine and patchouli for grounding, warm smoke.',
 'herbal': 'White sage, eucalyptus, rosemary, mint and green tea: clean, bright and clearing.',
 'floral': 'Rose, jasmine, lavender, lotus and gardenia for soft, sweet rooms.',
 'sweet': 'Vanilla, cinnamon, coconut and fruit notes for cozy, gourmand smoke.',
}
FAM_COLOR = {'nag-champa': '#e8a33d', 'resinous': '#b8862b', 'woods': '#8a6a4f', 'herbal': '#6f8f5a', 'floral': '#c9748f', 'sweet': '#c8662f'}

VISIT_EYEBROW = 'Visit the incense shop'
def STORE_DESC(S): return f'Incense shop steps from Union Square in Manhattan with about {S.ABOUT_N:,} incense sticks, cones, resins, sage, palo santo, holders and burners.'
REVIEW_TITLE = 'Shopped with us on 14th Street?'
REVIEW_TEXT = 'Tell other New Yorkers what you found. A short Google review helps people searching for incense near Union Square find the shop.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><path d="M20 36V24" stroke="#e8a33d" stroke-width="2.6" stroke-linecap="round"/><path d="M20 22c-6-4 5-7-1-12s4-6 2-9M24 20c3-3-2-5 1-8" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="20" cy="23" r="2" fill="#e8a33d"/></svg>'
WORDMARK = 'Namaste <b>Incense</b>'
BAR_TEXT = '2 West 14th Street, steps from Union Square'
SEARCH_PLACEHOLDER = 'Search scents, brands, resins, burners'

QUIZ = {
 'slug': 'scent-finder', 'nav': 'Scent finder', 'cta': 'Find my scent',
 'title': 'Incense Scent Finder Quiz', 'desc': 'Answer three quick questions and get incense picks from what is in stock today at 2 West 14th Street, near Union Square.',
 'h1': 'Find your incense scent', 'lead': 'Three questions, then we pull matching incense from what is on the shelves today. Nothing is saved or sent anywhere; it runs in your browser.',
 'submit': 'Show my matches',
 'questions': [
  {'q': 'What feeling do you want in the room?', 'options': [
    {'label': 'Calm and grounded', 'filter': {'fam': ['woods', 'resinous']}},
    {'label': 'Fresh and cleared out', 'filter': {'fam': ['herbal']}},
    {'label': 'Soft and romantic', 'filter': {'fam': ['floral']}},
    {'label': 'Warm, sweet and cozy', 'filter': {'fam': ['sweet', 'nag-champa']}}]},
  {'q': 'How do you like to burn it?', 'options': [
    {'label': 'Sticks: easy, no extra gear', 'filter': {'aisle': ['sticks']}},
    {'label': 'Cones or backflow cones', 'filter': {'aisle': ['cones']}},
    {'label': 'Resin on charcoal', 'filter': {'aisle': ['resins']}},
    {'label': 'A smudge bundle', 'filter': {'aisle': ['smudge']}}]},
  {'q': 'What would you like to spend?', 'options': [
    {'label': 'Under $5', 'filter': {'maxp': 5}}, {'label': 'Under $15', 'filter': {'maxp': 15}}, {'label': 'Whatever it takes', 'filter': {}}]},
 ]}

def FOOTER_EXPLORE(S):
    return [('Scent finder quiz', '/scent-finder/'), ('Where to buy incense in Manhattan', '/where-to-buy-incense-in-manhattan/'), ('How to burn resin incense', '/guide/how-to-burn-resin-incense/'),
            ('Incense styles explained', '/guide/incense-styles-explained/'), ('Indian incense', '/indian-incense/'), ('Japanese incense', '/japanese-incense/'), ('Gifts under $10', '/gifts-under-10/')]
FOOT_BLURB = 'The incense shop on 14th Street: sticks, cones, sacred resins, sage, palo santo and everything you need to burn them.'
HERO_BASES = ('sticks', 'resins', 'cones', 'smudge')
def HERO(S):
    return {'eyebrow': '2 West 14th Street &middot; Union Square &middot; New York City',
            'h1': 'Incense, sacred resins and sage, <em>steps from Union Square.</em>',
            'lede': f'About {S.ABOUT_N:,} incense sticks, cones, resins, smudge bundles, holders, burners and ritual candles at 2 West 14th Street. Sticks from {S.money(S.MIN_STICK)}. Open daily from 11 AM.' + (f' Reserve online and pick up in store; orders are {S.READY.lower()}.' if S.PICKUP_ON else ''),
            'shop_cta': 'Shop online'}

def _scents(S):
    tiles = ''.join(f'<a class="scent" href="/scents/{k}/" style="--c:{FAM_COLOR[k]}"><b>{E(S.FAM_NAME[k])}</b><span>{E(FAM_BLURB[k])}</span><small>{S.fam_count[k]} items</small></a>' for k in FAM_BLURB if S.fam_count[k])
    return f'<section class="wrap"><div class="sechead"><h2>Shop by scent family</h2><a href="/scent-finder/">Not sure? Take the quiz &rarr;</a></div><div class="scents">{tiles}</div></section>'
def _whys(S):
    return [(f'About {S.ABOUT_N:,} items', 'Sticks, cones, resins, sage, palo santo, holders, burners and candles, all listed online so you can pick your scents before you come in.'),
            (f'Sticks from {S.money(S.MIN_STICK)}', f'Every listing shows its price, and {S.UNDER10:,} items are under $10.'),
            (('Reserve, then pick up', f'Buy online, choose Pickup at checkout and collect on 14th Street. Orders are {S.READY.lower()}.') if S.PICKUP_ON else ('', '')),
            ('Open daily from 11 AM', 'Until 8 PM Monday to Thursday, 9 PM Friday and Saturday, and 7 PM Sunday.'),
            ('Brands people ask for', ', '.join(S.BRAND_NAME[k] for k, _ in S.brand_count.most_common(6)) + ' and more.'),
            ('On 14th Street', 'About 0.2 miles from both the 14 St&ndash;Union Square and 14 St/6 Av subway stations, and on the M14 bus routes.')]
def _new(S): return S.leaders[:8]
def _best(S): return S.by_rank(S.leaders)[:8] if S.HAS_RANK else []
def _value(S): return S.by_rank([x for x in S.leaders if x['price'] < 5 and x['aisle'] in ('sticks', 'cones', 'resins', 'smudge')])[:8]
HOME_SECTIONS = [
 {'type': 'html', 'html': _scents},
 {'type': 'grid', 'title': 'Best sellers this month', 'select': _best, 'href': '/shop/', 'link': 'Shop all', 'intro': 'Ranked by what sells most at namastebookshop.com, refreshed every day.'},
 {'type': 'visit'},
 {'type': 'collections', 'title': 'Featured collections', 'items': [
   {'title': 'Sacred resins', 'blurb': 'Frankincense, myrrh, copal and more for charcoal.', 'href': '/shop/sacred-resins/', 'filter': {'aisle': ['resins']}},
   {'title': 'Nag Champa', 'blurb': 'The classic, from Satya to HEM.', 'href': '/scents/nag-champa/', 'filter': {'fam': ['nag-champa']}},
   {'title': 'Japanese incense', 'blurb': 'Thin, low-smoke sticks for small rooms.', 'href': '/japanese-incense/', 'filter': {'style': ['Japanese']}},
   {'title': 'Sage & palo santo', 'blurb': 'Bundles, sticks and cleansing kits.', 'href': '/shop/sage-palo-santo/', 'filter': {'aisle': ['smudge']}},
   {'title': 'Backflow cones', 'blurb': 'Smoke that pours like a waterfall.', 'href': '/backflow-incense/', 'filter': {'q': 'backflow'}},
   {'title': 'Gifts under $10', 'blurb': 'Easy add-ons and stocking stuffers.', 'href': '/gifts-under-10/', 'filter': {'maxp': 10}}]},
 {'type': 'grid', 'title': 'New arrivals', 'select': _new, 'href': '/shop/?sort=new', 'link': 'See what is new'},
 {'type': 'whys', 'title': 'Why stop by', 'items': _whys},
 {'type': 'grid', 'title': 'Best value: favorites under $5', 'select': _value, 'href': '/shop/?price=0-5', 'link': 'All under $5'},
 {'type': 'quiz', 'title': 'Not sure which scent?', 'text': 'Three questions, a handful of real in-stock picks.'},
 {'type': 'brands', 'title': 'Brands we carry', 'n': 14},
 {'type': 'review'},
 {'type': 'band', 'title': 'Reserve online, pick up in store', 'text': lambda S: 'Every listing has its own photos, price and live stock. Reserve online and collect it on 14th Street, or have it shipped from New York City.',
  'steps': lambda S: [('Find your scent', 'Filter by aisle, scent family, brand, style or price.'), ('Choose Pickup at checkout', f'Pay securely on Shopify. Orders are {S.READY.lower() or "usually ready the same day"}.'), ('Collect it', S.STORE_ADDR + '.')]},
]
def HOME_TITLE(S): return 'Namaste Incense | Incense Shop near Union Square, NYC | 2 W 14th St'
def HOME_DESC(S): return f'Incense shop at {S.STORE_ADDR}, steps from Union Square. About {S.ABOUT_N:,} incense sticks, cones, resins, sage, palo santo and burners, sticks from {S.money(S.MIN_STICK)}. In-store pickup, open daily from 11 AM.'
def SHOP_TITLE(S): return 'Shop Incense Online, Pick Up near Union Square | Namaste Incense'
def SHOP_DESC(S): return f'Browse {S.N:,} incense sticks, cones, resins, sage, palo santo, holders, burners and ritual candles. Sticks from {S.money(S.MIN_STICK)}. Pick up at 2 West 14th Street, NYC, or ship.'
SHOP_H1 = 'Shop all incense'
def SHOP_SUB(S): return f'{S.N:,} items in stock across {len(S.AISLE_KEYS)} aisles. Reserve online and pick up at 2 West 14th Street, or have it shipped.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} in NYC near Union Square | Namaste Incense'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} items at Namaste Incense, 2 West 14th Street, NYC. Pick up in store or ship.'

def LANDINGS(S):
    L = []
    for k, b in FAM_BLURB.items():
        n = S.FAM_NAME[k]
        L.append({'path': f'/scents/{k}/', 'title': f'{n} Incense in NYC | Namaste Incense', 'desc': f'{b} {S.fam_count[k]} {n.lower()} incense, resin and smudge items at 2 West 14th Street near Union Square, or shipped from NYC.',
                  'h1': f'{n} incense', 'sub': b, 'filter': {'fam': [k]}})
    L.append({'path': '/gifts-under-10/', 'title': 'Incense Gifts Under $10 in NYC | Namaste Incense', 'desc': f'{S.UNDER10} incense sticks, cones, sage bundles, holders and candles under $10 at 2 West 14th Street, steps from Union Square.',
              'h1': 'Gifts under $10', 'sub': f'{S.UNDER10} items under $10: stocking stuffers, hostess gifts and first-time incense kits.', 'filter': {'maxp': 10}})
    L.append({'path': '/indian-incense/', 'title': 'Indian Incense: Nag Champa, Masala & Dhoop in NYC | Namaste Incense', 'desc': f'Hand-rolled masala sticks, dhoop and Nag Champa from India: {S.style_count["Indian"]} Indian incense items at 2 West 14th Street, steps from Union Square.',
              'h1': 'Indian incense', 'sub': 'Masala, dhoop and Nag Champa from Indian makers such as Satya, HEM, Auroshikha and Kamini.', 'filter': {'style': ['Indian']},
              'intro': '<p class="intro">Indian incense is usually rolled by hand: a bamboo core coated in a paste of resins, woods, herbs and oils (masala), or dipped in fragrance. Start with <a href="/scents/nag-champa/">Nag Champa</a>, then try the intention blends such as Money, Protection and Good Luck that many Indian brands make.</p>'})
    L.append({'path': '/japanese-incense/', 'title': 'Japanese Incense in NYC: Low-Smoke Sticks | Namaste Incense', 'desc': f'Thin, low-smoke Japanese sticks, including Morning Star and Herb & Earth by Nippon Kodo: {S.style_count["Japanese"]} items at 2 West 14th Street.',
              'h1': 'Japanese incense', 'sub': 'Thin, low-smoke sticks for apartments, offices and meditation corners.', 'filter': {'style': ['Japanese']},
              'intro': '<p class="intro">Japanese incense is usually pressed without a bamboo core, so it burns cleaner and gives off less smoke than most Indian sticks. Morning Star and Herb &amp; Earth are both made by Nippon Kodo.</p>'})
    L.append({'path': '/tibetan-incense/', 'title': 'Tibetan Incense in NYC | Namaste Incense', 'desc': 'Tibetan and Nepalese herbal incense at 2 West 14th Street, steps from Union Square.',
              'h1': 'Tibetan incense', 'sub': 'Earthy, herbal sticks from Tibetan and Nepalese traditions.', 'filter': {'style': ['Tibetan']}})
    L.append({'path': '/backflow-incense/', 'title': 'Backflow Incense Cones & Waterfall Burners in NYC | Namaste Incense', 'desc': 'Backflow cones and waterfall burners that make smoke flow downward, at 2 West 14th Street near Union Square.',
              'h1': 'Backflow cones & burners', 'sub': 'Cones with a hollow core that send smoke pouring down a fountain burner.', 'filter': {'q': 'backflow'},
              'intro': '<p class="intro">A backflow cone has a channel through its center. Burned on a backflow burner, the cooled smoke sinks and flows down the burner like water. You need both the cones and a backflow burner.</p>'})
    return L

# ---- brands: written for this site; facts from the sources listed in scripts/brands.py ----
BRAND_TEXT = {
 'hem': 'HEM is made by HEM Corporation in India, which three Shah brothers founded in 1983 and which now runs factories in Mumbai and Bengaluru. Its HEM Precious range dates from 1988. Expect bright, strong-throw hexagonal boxes in just about every scent you can name.',
 'satya': 'Satya sticks come from Shrinivas Sugandhalaya of Bangalore, the house behind the original Sai Baba Nag Champa. They are hand-rolled masala sticks with a soft, powdery smoke, and the familiar blue box is often the first incense people ever buy.',
 'morning-star': 'Morning Star is a Japanese line by Nippon Kodo. The sticks are thin and give off little smoke, and most boxes come with a small holder, which makes them a favorite for apartments and desks.',
 'herb-earth': 'Herb & Earth is a low-smoke line from Nippon Kodo, made on bamboo sticks in natural scents such as sandalwood, lavender, frankincense, matcha and white sage.',
 'good-karma': 'Good Karma candles are made by Zensual, the Good Karma Candle Company in Southern California. They are soy-blend candles hand-poured in the USA in recyclable tins, each pairing a scent with an intention.',
 'escential-essences': 'Escential Essences, represented by Matchless Gifts, makes hand-dipped incense sticks and one-inch cones in the USA using cosmetic-grade oils. The scent list is long and leans sweet and fun.',
 'sonavi': 'SONAVI comes from New Age Imports in Placentia, California, which also makes incense sticks, bakhoor chips and beeswax candles.',
 'prabhujis': "Prabhuji's Gifts is a Green America certified business. Its incense is handmade by artisans in India's cottage industry and packed in recycled cardboard.",
 'coventry-creations': 'Coventry Creations, now Coventry Products, is a family- and female-owned candle maker in Ferndale, Michigan. It is best known for Blessed Herbal intention candles.',
 'wolf-spirit': 'Wolf Spirit Sage makes sage, natural resin incense, smudge sticks and smokeless sprays in the United States, with pickers in California and the High Plains.',
 'suns-eye': "Sun's Eye is based in Central Florida and makes incense, oils and sprays.",
 'little-smudgies': 'Little Smudgies are mini smudge candles from Soul Sticks: twelve soy-wax candles to a pack, made with lead-free wicks, herbs and crystals. Each one burns for about four hours.',
 'soul-sticks': 'Soul Sticks makes masala and plant-based incense along with smudge kits and intention kits.',
 'archangel-incense': 'Archangel Incense is made by Jabou in Canada: natural hand-dipped sticks, 20 to a pack, with one blend for each archangel.',
 'fred-soll': "Fred Soll's is based in Tijeras, New Mexico, about ten miles east of Albuquerque. Its Resin on a Stick incense is hand-dipped in pinon and other resins. Burn a stick lying flat; it lasts one to two and a half hours.",
 'aloha-bay': 'Aloha Bay has made candles in Lower Lake, California, since 1993. Its chakra candles use RSPO certified palm wax, and the company is a member of the World Fair Trade Organization.',
 'auroshikha': 'Auroshikha is a unit of the Sri Aurobindo Ashram in Pondicherry, India, and has made incense since 1973. Its sticks and cones are hand-rolled, and its fragrances follow IFRA guidelines.',
 'kamini': 'Kamini incense comes from Kamini Aromatics in Bangalore, India, which makes natural masala sticks and cones.',
 'swift-lite': 'Swift-Lite charcoal is made by Swift-Lite International in Ashford, Kent, in the UK, a company established in 1957. The tablets light fast and were designed for burning religious incense; they are what most people use for resin.',
 'song-of-india': 'Song of India is run by R. Expo from India and Auburn, Washington, with roots in a Delhi perfumery founded in 1932. India Temple is one of its best-known incense scents.',
}
def _aisle_list(S, st): return ', '.join(f'{c} {S.AISLES[a][0].lower()}' for a, c in st['aisles'].most_common(3))
def brand_intro(S, k, st):
    name = S.BRAND_NAME[k]
    t = BRAND_TEXT.get(k) or f'We currently carry {st["n"]} {E(name)} item{"s" if st["n"] != 1 else ""}, listed below with live prices.'
    tail = f' On the shelves right now: {_aisle_list(S, st)}, from {S.money(st["min"])}.'
    pk = ' Reserve any of them online and pick up at 2 West 14th Street, steps from Union Square.' if st['pickup'] else ' Call ahead to check stock before you visit 2 West 14th Street.'
    return f'<p>{E(t)}{tail}{pk}</p>'
def brand_faq(S, k, st):
    name = S.BRAND_NAME[k]
    q = [(f'Where can I buy {name} in New York City?', f'Namaste Incense carries {st["n"]} {name} items at 2 West 14th Street, New York, NY 10011, about a 4-minute walk from Union Square. Open daily from 11 AM.'),
         (f'How much does {name} cost?', (f'{name} items here run from {S.money(st["min"])} to {S.money(st["max"])}.' if st['max'] > st['min'] else f'{name} items here are {S.money(st["min"])} each.') + ' Prices on this page update every day.')]
    if st['pickup']: q.append((f'Can I reserve {name} online and pick it up?', 'Yes. Tap Buy now, choose Pickup at checkout, and collect your order at 2 West 14th Street.' + (f' Orders are {S.READY.lower()}.' if S.READY else '')))
    if k in BRAND_TEXT and st['n'] >= 5: q.append((f'Who makes {name}?', BRAND_TEXT[k].split('. ')[0] + '.'))
    return q
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} in New York City'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} Incense in NYC near Union Square | Namaste Incense'
def BRAND_DESC(S, k, st): return f'{S.BRAND_NAME[k]}: {st["n"]} item{"s" if st["n"] != 1 else ""} in stock from {S.money(st["min"])} at 2 West 14th Street, Manhattan. Pick up in store or ship.'
def BRANDS_TITLE(S): return 'Incense Brands A to Z | Namaste Incense, Union Square NYC'
def BRANDS_DESC(S): return 'Every incense, resin, sage and candle brand we stock at 2 West 14th Street, from Aloha Bay to Wolf Spirit, with live item counts.'
BRANDS_H1 = 'Incense brands A to Z'
def BRANDS_LEAD(S, n): return f'{n} brands are on our shelves today. Each page lists every item in stock with its price; counts update daily. Not seeing a brand? Call <a href="tel:{S.TEL}">{S.PHONE}</a>.'

PAIR = {'sticks': ['holders'], 'cones': ['burners', 'holders'], 'resins': ['burners'], 'smudge': ['burners', 'holders'], 'candles': ['smudge'], 'holders': ['sticks'], 'burners': ['resins', 'cones']}
REL_BRAND = 'More from {brand}'
REL_SCENT = 'More {scent} scents'
REL_PAIR = 'Burn it with'
REL_MORE = 'More {aisle}'
def describe(S, x):
    cat, fam, b = x['aisle'], x['family'], x['brand']
    by = f" from {S.BRAND_NAME[b]}" if b else ''
    s = []
    if cat in ('sticks', 'cones'):
        kind = 'stick incense' if cat == 'sticks' else ('backflow cone incense' if re.search('backflow', x['title'], re.I) else 'cone incense')
        s.append(f"{E(x['title'])} is {x['style'] + ' ' if x['style'] else ''}{kind}{by}.")
        if fam: s.append(f"It sits in our {S.FAM_NAME[fam].lower()} scent family.")
        s.append('Light the tip, let the flame catch for a few seconds, then blow it out so it glows and smokes. Burn it in a holder on a heat-safe surface, keep it away from anything that can catch fire, and never leave it burning unattended.')
    elif cat == 'resins':
        s.append(f"{E(x['title'])} is resin incense{by} for burning on a charcoal tablet or an electric resin warmer.")
        s.append('Light a charcoal tablet in a heat-proof burner with sand or ash, wait until it glows and turns gray, then add a small pinch of resin. A little goes a long way. Never leave burning charcoal unattended.')
    elif cat == 'smudge':
        s.append(f"{E(x['title'])}{by} is a smudge or cleansing bundle for clearing a room with smoke.")
        s.append('Light the end, let it smolder, and carry it over a shell or heat-safe bowl to catch embers. Press it out in sand or the bowl when you are done. Never leave smoldering herbs unattended.')
    elif cat == 'holders':
        s.append(f"{E(x['title'])} is an incense holder that keeps sticks or cones upright and catches the ash.")
        s.append('Set it on a stable, heat-safe surface away from curtains and paper. Handmade and natural materials vary slightly from the photo.')
    elif cat == 'burners':
        s.append(f"{E(x['title'])}{by} is built for burning incense, resin or charcoal safely.")
        s.append('Burners and charcoal get hot: use a heat-safe base, handle hot pieces with tongs, and never leave burning charcoal unattended.')
    else:
        s.append(f"{E(x['title'])}{by} is a ritual or aromatherapy candle to burn alongside your incense.")
        s.append('Trim the wick, burn it on a heat-safe surface away from drafts and anything flammable, and never leave a burning candle unattended.')
    s.append('Ships from New York City, or choose it in person at 2 West 14th Street, steps from Union Square. Secure checkout is completed on Shopify through namastebookshop.com.')
    return s
def PRODUCT_DESC(S, x, v0):
    return f"{x['title']} for {S.money(v0['price'])}. " + ('Reserve online and pick up at 2 West 14th Street near Union Square, or ship from NYC.' if x['pickup'] else 'At 2 West 14th Street near Union Square, or ship from NYC.')

def ABOUT_DESC(S): return 'About Namaste Incense, the incense shop at 2 West 14th Street, steps from Union Square. A brand of Wealth Edge Ventures Inc.'
ABOUT_H1 = 'About Namaste Incense'
def ABOUT(S):
    return f'''<p class="lead">Namaste Incense is an incense shop at {S.STORE_ADDR}, on 14th Street just west of Fifth Avenue and a few minutes' walk from Union Square.</p>
<p>We focus on one thing: smoke. Stick and cone incense, sacred resins and the charcoal to burn them, white sage and palo santo, holders and ash catchers, censers and backflow burners, and ritual candles to go alongside. About {S.ABOUT_N:,} items are listed online with their own photos and prices, and stock updates every day.{" Reserve online and choose Pickup at checkout to collect in store." if S.PICKUP_ON else ""}</p>
<h2>Visit</h2><p>{S.STORE_ADDR}. Call <a href="tel:{S.TEL}">{S.PHONE}</a>.</p>{S.hours_html()}{S.visit_buttons()}<p><a href="/visit/">Directions, subway lines and pickup details &rarr;</a></p>
<h2>Who we are</h2><p>{S.LEGAL} Online orders are checked out on Shopify through <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>, which processes payment and fulfills orders, including in-store pickups. Products ship from New York City.</p>
<p>Looking for books, tarot decks or crystals? Visit <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>.</p>
<h2>What we carry</h2><ul>{''.join(f'<li><a href="/shop/{AISLES[k][2]}/">{E(AISLES[k][0])}</a>: {E(AISLES[k][3])}</li>' for k in S.AISLE_KEYS)}</ul>
<h2>Burn safely</h2><p>Burn incense, resin, herbs and candles on heat-safe surfaces, away from anything flammable, in a ventilated room, and never leave them unattended. Traditional uses of incense are shared for interest only and are not medical advice.</p>
<h2>Get in touch</h2><p>Call <a href="tel:{S.TEL}">{S.PHONE}</a>, or see the <a href="{S.SHOP}/policies/contact-information">store contact page</a> for order questions.</p>'''
VISIT_TITLE = 'Visit Our Incense Shop near Union Square'
def VISIT_DESC(S): return f'Directions, hours, subway lines and in-store pickup for Namaste Incense at {S.STORE_ADDR}, steps from Union Square.'
def VISIT_LEAD(S): return f'We are at {S.STORE_ADDR}, on 14th Street just west of Fifth Avenue, where Union Square, Greenwich Village, Chelsea and the Flatiron District meet.'
def FAQ_DESC(S): return 'Answers about Namaste Incense: where we are, hours, in-store pickup, shipping, which incense to start with and how to burn resin and sage safely.'
FAQ_H1 = 'Questions we hear a lot'
def FAQ(S):
    return [('Where is Namaste Incense?', f'At {S.STORE_ADDR}, on 14th Street just west of Fifth Avenue, about a 4-minute walk from the 14 St&ndash;Union Square subway station.'),
            ('What are your hours?', 'Monday to Thursday 11 AM to 8 PM, Friday and Saturday 11 AM to 9 PM, and Sunday 11 AM to 7 PM. Holiday hours may differ, so call ahead before a special trip.'),
            ('Can I order online and pick up in store?', 'Yes. Tap Buy now on any product, choose Pickup at checkout and collect it at 2 West 14th Street.' + (f' Orders are {S.READY.lower()}.' if S.READY else '')),
            ('Do you ship?', 'Yes. Orders ship from New York City, and shipping options and costs are shown at checkout before you pay. Checkout runs on Shopify through namastebookshop.com.'),
            ('Which incense should I start with?', 'Nag Champa is the classic first stick. If you want less smoke, try Japanese incense; if you love church-like scents, try frankincense resin on charcoal. Our <a href="/scent-finder/">scent finder</a> suggests real in-stock picks.'),
            ('What do I need to burn resin?', 'Charcoal tablets, a heat-proof burner filled with sand or ash, and tongs. Our <a href="/guide/how-to-burn-resin-incense/">resin guide</a> walks through it step by step.'),
            ('What is the difference between masala, dipped and Japanese incense?', 'Masala sticks are hand-rolled in a paste of resins, woods and herbs; dipped sticks are blank sticks soaked in fragrance oil; Japanese sticks are usually pressed without a bamboo core and smoke less. See <a href="/guide/incense-styles-explained/">incense styles explained</a>.'),
            ('Which brands do you carry?', f'{len(S.brand_count)} brands including ' + ', '.join(S.BRAND_NAME[k] for k, _ in S.brand_count.most_common(6)) + '. See the <a href="/brands/">brand directory</a>.'),
            ('Is burning incense safe?', 'Burn it on a heat-safe surface in a ventilated room, away from anything flammable, and never leave it unattended. Traditional uses are shared for interest only and are not medical advice.')]

def GUIDES(S):
    resins = S.cat_count['resins']
    return [
     {'path': '/guide/how-to-burn-resin-incense/', 'title': 'How to Burn Resin Incense (Frankincense, Myrrh, Copal)', 'desc': 'A step-by-step guide to burning frankincense, myrrh, copal and other resins on charcoal, with what you need and safety tips.', 'h1': 'How to burn resin incense',
      'html': f'''<p class="lead">Resins such as frankincense, myrrh, copal and benzoin do not light on their own. They melt on a heat source and release their scent as smoke.</p>
<h2>What you need</h2><ul><li>Resin: see our <a href="/shop/sacred-resins/">{resins} sacred resins</a>.</li><li>Charcoal tablets made for incense, such as <a href="/brands/swift-lite/">Swift-Lite</a>, and a heat-proof <a href="/shop/burners-charcoal/">burner or censer</a>.</li><li>Sand, salt or ash to fill the burner, and tongs.</li></ul>
<h2>Step by step</h2><ol><li>Fill the burner about two-thirds with sand or ash so the heat does not reach the bottom.</li><li>Hold a charcoal tablet with tongs and light its edge. It will spark across the surface.</li><li>Set it on the sand and wait until it is covered in gray ash, usually a few minutes.</li><li>Place a small pinch of resin, about the size of a pea, on top. Add more as it burns away.</li><li>When you are done, let the charcoal burn out fully in the burner. Do not pour water on hot ceramic.</li></ol>
<h2>Safety</h2><ul><li>Charcoal and burners get very hot. Use a heat-proof surface and keep it away from children, pets, curtains and paper.</li><li>Burn in a ventilated room and never leave burning charcoal unattended.</li></ul><p><a class="btn" href="/shop/sacred-resins/">Shop sacred resins</a></p>'''},
     {'path': '/guide/incense-styles-explained/', 'title': 'Incense Styles Explained: Masala, Dipped, Japanese, Tibetan & Resin', 'desc': 'How masala, dipped, dhoop, Japanese, Tibetan and resin incense differ, and how to choose one, from the incense shop near Union Square.', 'h1': 'Incense styles explained',
      'html': f'''<p class="lead">Two sticks can look alike and burn completely differently. Here is how the main styles on our shelves compare.</p>
<h2>Masala sticks</h2><p>A bamboo core rolled by hand in a paste of resins, woods, herbs and oils. Soft, full smoke. <a href="/scents/nag-champa/">Nag Champa</a> from <a href="/brands/satya/">Satya</a> is the best-known example.</p>
<h2>Dipped sticks</h2><p>Blank sticks soaked in fragrance oil. Strong scent and huge variety; <a href="/brands/hem/">HEM</a> and <a href="/brands/escential-essences/">Escential Essences</a> make many.</p>
<h2>Dhoop</h2><p>Dense, coreless sticks or cones with a rich, heavy smoke. Look for the word dhoop in <a href="/indian-incense/">Indian incense</a>.</p>
<h2>Japanese incense</h2><p>Usually pressed without a bamboo core, so it burns cleaner with less smoke. <a href="/japanese-incense/">Shop Japanese incense</a>.</p>
<h2>Tibetan incense</h2><p>Earthy, herbal and often thick. <a href="/tibetan-incense/">Shop Tibetan incense</a>.</p>
<h2>Resin</h2><p>Raw tears of frankincense, myrrh or copal melted on charcoal. The oldest form of incense. <a href="/guide/how-to-burn-resin-incense/">How to burn resin</a>.</p>
<h2>Cones and backflow cones</h2><p>Cones burn faster and stronger than sticks. Backflow cones have a hollow center so the smoke flows down a <a href="/backflow-incense/">backflow burner</a>.</p>
<p>Still undecided? Try the <a href="/scent-finder/">scent finder</a>, or come smell a few at 2 West 14th Street.</p>'''},
     {'path': '/where-to-buy-incense-in-manhattan/', 'title': 'Where to Buy Incense in Manhattan: Union Square, East Village, Midtown', 'store_ld': True,
      'desc': f'Looking for an incense shop in Manhattan? Namaste Incense is at {S.STORE_ADDR}, steps from Union Square, with about {S.ABOUT_N:,} incense items, sticks from {S.money(S.MIN_STICK)} and in-store pickup.',
      'h1': 'Where to buy incense in Manhattan', 'html': f'''<p class="lead">Searching for an incense shop near you in Manhattan? We are on 14th Street at Fifth Avenue, one of the easiest corners in the city to reach by subway and bus. Here is what we stock and how to get here from your neighborhood.</p>
<h2>What you will find at 2 West 14th Street</h2><ul><li>About {S.ABOUT_N:,} incense items listed online across {len(S.AISLE_KEYS)} aisles, with {S.UNDER10:,} under $10 and sticks from {S.money(S.MIN_STICK)}.</li>
<li>Indian masala and dhoop incense, Nag Champa, Japanese incense, resin incense, sage, palo santo, charcoal, burners and holders.</li>
<li>Brands including {', '.join(f'<a href="/brands/{k}/">{E(S.BRAND_NAME[k])}</a>' for k, _ in S.brand_count.most_common(6))}.</li>{f"<li>Reserve online and pick up in store; orders are {S.READY.lower()}.</li>" if S.PICKUP_ON else ""}<li>Open daily from 11 AM. See <a href="/visit/">full hours</a>.</li></ul>
<h2>Getting here from your neighborhood</h2><ul>
<li><b>Union Square and Gramercy:</b> walk west on 14th Street past Union Square West and University Place to Fifth Avenue.</li>
<li><b>East Village and East 14th Street:</b> walk west along 14th Street, ride the M14A or M14D west, or take the L from First or Third Avenue to 14 St&ndash;Union Square or Sixth Avenue.</li>
<li><b>Midtown and Times Square:</b> take the N, Q, R or W from Times Sq&ndash;42 St to 14 St&ndash;Union Square, or the 1, 2 or 3 to 14 St and walk east on 14th Street.</li>
<li><b>Hell's Kitchen and Midtown West:</b> take the C or E from 50 St to 14 St, then the L one stop east to Sixth Avenue, or walk east along 14th Street from Eighth Avenue (about half a mile).</li>
<li><b>Chelsea:</b> take the 1, 2, 3, F, M or L to 14th Street at Seventh or Sixth Avenue and walk east.</li>
<li><b>Flatiron and NoMad:</b> walk south on Fifth Avenue to 14th Street.</li>
<li><b>Greenwich Village and the West Village:</b> walk north on Fifth Avenue, or take the 1, 2 or 3 to 14 St.</li></ul>
<h2>Tips for your visit</h2><ul><li>Browse the <a href="/shop/">online shop</a> first and note the scents you want, or try the <a href="/scent-finder/">scent finder</a>.</li><li>Shopping for one exact item? Call <a href="tel:{S.TEL}">{S.PHONE}</a> first, or reserve it online for pickup.</li><li>New to resin? Read <a href="/guide/how-to-burn-resin-incense/">how to burn resin incense</a>.</li></ul>{S.visit_block()}'''},
    ]
NOT_FOUND = 'That page went up in smoke'
