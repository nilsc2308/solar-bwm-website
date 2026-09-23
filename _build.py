# -*- coding: utf-8 -*-
"""Generator für die Website von Solar Technik BwM (Photovoltaik, Lontzen): gemeinsamer Kopf/Fuß, alle Seiten, Sitemap.
Aufruf: python3 _build.py   (erzeugt die HTML-Dateien neben dieser Datei)"""
import json, os, math, html as H
OUT = os.path.dirname(os.path.abspath(__file__)) + '/'
DOMAIN = 'https://solar-bwm.com'
TODAY = '2026-09-23'
VER = '20260923-2'
CO = dict(name='Solar Technik BwM', short='Solar BwM', person='Malte Behrenswerth', street='Schmalgraf 48', zip='4710', city='Lontzen',
          country='Belgien', tel='+49 1575 5232254', telh='+4915755232254', mail='info@solar-bwm.com', vat='BE 0768.628.988',
          lat='50.69998', lon='5.98361')

# ---------- Zeichen ----------
# Querschnitt der Montageschiene (40 x 40 mm) mit T-Nut oben und unten, 100er-Raster
PROFILE = 'M0 0H38V8H28V24H72V8H62V0H100V100H62V92H72V76H28V92H38V100H0Z'
PROFILE_HOLES = 'M8 8H20V92H8ZM80 8H92V92H80Z'
MARK = f'<svg viewBox="-6 -6 112 112" aria-hidden="true"><path d="{PROFILE} {PROFILE_HOLES}" fill="currentColor" fill-rule="evenodd"/></svg>'
LOGO = f'<span class="plate"><span class="mark">{MARK}</span><span class="wordmark"><b>Solar Technik BwM</b><i>Photovoltaik</i></span></span>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
TEL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.9 2z"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'

# ---------- Fotos (Name: Breite/Höhe der großen Fassung, Breite der mittleren) ----------
DIMS = {'schiene': (1600, 1456, 800)}
for n in ['blechdach', 'blechdach-weit', 'flachdach-stadt', 'flachdach-reihen', 'flachdach-ballast', 'flachdach-hof', 'ziegeldach', 'bruchsteinhaus']:
    DIMS[n] = (1600, 1200, 800)
DIMS['backsteinhaus'] = (1200, 1600, 600)
for n in ['mittelklemme', 'endklemme', 'dachhaken', 'dachhaken-2']:
    DIMS[n] = (768, 1024, 480)
DIMS['kran'] = (1024, 768, 640)
DIMS['p-wechselrichter'] = (539, 702, 360)
DIMS['p-datenblatt'] = (787, 1071, 400)
DIMS['p-modul'] = (789, 1075, 400)
SINGLE = {'p-bms': (355, 127), 'p-speicher': (355, 219), 'p-sensor': (231, 327)}


def pic(n, alt, sizes='100vw', lazy=True, cls='', late=False):
    """Foto mit srcset in zwei Größen. late=True: erst nach dem load-Ereignis laden (Szene ab Foto 2)."""
    if n in SINGLE:
        w, h = SINGLE[n]
        return f'<img class="{cls}" src="img/{n}.webp" width="{w}" height="{h}" alt="{H.escape(alt)}" loading="lazy" decoding="async">'
    lw, lh, mw = DIMS[n]
    src, ss = f'img/{n}-m.webp', f'img/{n}-m.webp {mw}w, img/{n}-l.webp {lw}w'
    c = f' class="{cls}"' if cls else ''
    if late:
        return f'<img{c} data-late data-src="{src}" data-srcset="{ss}" sizes="{sizes}" width="{lw}" height="{lh}" alt="{H.escape(alt)}" decoding="async">'
    lz = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img{c} src="{src}" srcset="{ss}" sizes="{sizes}" width="{lw}" height="{lh}" alt="{H.escape(alt)}"{lz}>'


# ---------- Seitenstruktur ----------
SERVICES = [  # Datei, Titel, Einzeiler, Foto für das Menü
    ('planung-beratung.html', 'Planung & Beratung', 'Dach, Verbrauch und Wünsche aufnehmen, die passende Anlage auslegen.', 'bruchsteinhaus'),
    ('montage.html', 'Montage', 'Gestell, Schienen und Module auf Flachdach, Satteldach, Pultdach oder Wiese.', 'flachdach-reihen'),
    ('anschliessen.html', 'Anschließen', 'Wechselrichter, Speicher und Energiezähler verbinden und in Betrieb nehmen.', 'blechdach'),
    ('wartung.html', 'Wartung', 'Befestigung, Kabel und Ertrag prüfen, damit die Anlage Jahre läuft.', 'ziegeldach'),
]
PRODUCTS = [
    ('module.html', 'Module', 'JA Solar JAM72S10 mit 405 W, auf Wunsch andere Hersteller.', 'flachdach-hof'),
    ('befestigung.html', 'Befestigung', 'Schiene, Dachhaken, Trapezblechschuh, End- und Mittelklemme.', 'dachhaken'),
    ('wechselrichter.html', 'Wechselrichter', 'Einphasige Huawei SUN2000 mit 3, 3,68 und 4 kW.', 'blechdach-weit'),
    ('speicher.html', 'Batteriespeicher', 'Huawei LUNA2000 mit Steuereinheit für den Strom am Abend.', 'backsteinhaus'),
    ('energiezaehler.html', 'Energiezähler', 'Smart Power Sensor DTSU666-H misst Bezug und Einspeisung.', 'flachdach-ballast'),
]
TOOLS = [  # Seite, Frage, Werkzeug, Symbol (SVG-Pfade 32x32)
    ('planung-beratung.html', 'Was braucht BwM von mir für ein Angebot?', 'Anfrage-Steckbrief', '<rect x="6" y="4" width="20" height="24" rx="2"/><path d="M11 11h10M11 16h10M11 21h6"/>'),
    ('montage.html', 'Wie wird auf meinem Dach befestigt?', 'Befestigung nach Eindeckung', '<path d="M3 20 16 8l13 12"/><path d="M8 16v10h16V16"/>'),
    ('befestigung.html', 'Wie viele Schienen und Klemmen braucht mein Dach?', 'Stückliste', '<path d="M4 12h24M4 20h24"/><path d="M10 9v6M22 9v6M16 17v6"/>'),
    ('module.html', 'Warum liefern Module im Hochsommer weniger?', 'Hitze-Rechner', '<circle cx="16" cy="16" r="5"/><path d="M16 3v4M16 25v4M3 16h4M25 16h4M7 7l3 3M22 22l3 3M7 25l3-3M22 10l3-3"/>'),
    ('wechselrichter.html', 'Welcher Wechselrichter passt zu meiner Modulzahl?', 'Wechselrichter-Finder', '<rect x="7" y="4" width="18" height="24" rx="2"/><path d="M12 12h8M12 17h8"/><circle cx="16" cy="23" r="1.5"/>'),
    ('speicher.html', 'Reicht ein Speicher durch die Nacht?', 'Nacht-Rechner', '<path d="M22 20a9 9 0 0 1-10-13 10 10 0 1 0 10 13z"/>'),
    ('anschliessen.html', 'Wann sollte die Waschmaschine laufen?', 'Tagesplan der Geräte', '<path d="M3 26h26"/><path d="M5 26c3-14 19-14 22 0"/><path d="M16 4v4"/>'),
    ('wartung.html', 'Meine Anlage liefert weniger – was tun?', 'Symptom-Wegweiser', '<path d="M4 16h5l3-7 5 14 3-7h8"/>'),
]
ALLNAV = [('index.html', 'Start'), ('leistungen.html', 'Leistungen')] + [(s[0], s[1]) for s in SERVICES] + [('produkte.html', 'Produkte')] + \
         [(p[0], p[1]) for p in PRODUCTS] + [('referenzen.html', 'Referenzen'), ('ueber-uns.html', 'Über uns'), ('ratgeber.html', 'Ratgeber'), ('faq.html', 'Häufige Fragen'), ('kontakt.html', 'Kontakt')]


def ld_business():
    return {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": DOMAIN + "/#business", "name": CO['name'],
        "description": "Planung, Montage, Anschluss und Wartung von Photovoltaikanlagen im Dreiländereck Deutschland, Belgien und Niederlande, Raum Aachen.",
        "url": DOMAIN + "/", "telephone": CO['telh'], "email": CO['mail'], "image": DOMAIN + "/img/og.jpg", "logo": DOMAIN + "/favicon.svg",
        "founder": {"@type": "Person", "name": CO['person']}, "vatID": CO['vat'],
        "address": {"@type": "PostalAddress", "streetAddress": CO['street'], "postalCode": CO['zip'], "addressLocality": CO['city'], "addressCountry": "BE"},
        "geo": {"@type": "GeoCoordinates", "latitude": float(CO['lat']), "longitude": float(CO['lon'])},
        "areaServed": ["Aachen", "Städteregion Aachen", "Ostbelgien", "Eupen", "Lontzen", "Kelmis", "Raeren", "Provinz Limburg (NL)", "Dreiländereck"],
    }


def head(p):
    ld = [ld_business()]
    if p.get('ld'): ld.extend(p['ld'] if isinstance(p['ld'], list) else [p['ld']])
    f = p['file']
    url = DOMAIN + '/' + ('' if f == 'index.html' else f)
    cur = lambda x: ' aria-current="page"' if f == x or p.get('parent') == x else ''
    on = lambda group: ' class="on"' if f in group else ''
    svc_files = ['leistungen.html'] + [s[0] for s in SERVICES]
    prd_files = ['produkte.html'] + [x[0] for x in PRODUCTS]
    def drop(items, overview, label, idd):
        li = ''.join(f'<li><a href="{a}"{cur(a)}><span class="dd-img">{pic(ph, "", "96px")}</span><span><b>{t}</b><small>{d}</small></span></a></li>' for a, t, d, ph in items)
        return f'<div class="dd" id="{idd}"><ul>{li}</ul><a class="dd-all" href="{overview}">{label} {ARROW}</a></div>'
    return f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{p['title']}</title>
<meta name="description" content="{p['desc']}">
<link rel="canonical" href="{url}">
{'<meta name="robots" content="noindex, follow">' if p.get('noindex') else ''}
<meta property="og:type" content="{'article' if p.get('article') else 'website'}">
<meta property="og:site_name" content="{CO['name']}">
<meta property="og:locale" content="de_DE">
<meta property="og:title" content="{p['title']}">
<meta property="og:description" content="{p['desc']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/img/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#18213d">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/barlow-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/barlow-condensed-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
{'<link rel="preload" as="image" href="img/schiene-l.webp" imagesrcset="img/schiene-m.webp 800w, img/schiene-l.webp 1600w" imagesizes="100vw">' if f == 'index.html' else ''}
<link rel="stylesheet" href="styles.css?v={VER}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body class="{p.get('body', '')}">
<a class="skip" href="#main">Zum Inhalt springen</a>
<div class="curtain intro" aria-hidden="true"><div class="intro-mark">{MARK}<span>Solar Technik BwM</span></div></div>
<div class="curtain leave" aria-hidden="true"></div>
<div class="progress" id="progress" aria-hidden="true"></div>
<header class="head" id="head">
  <div class="head-in">
    <a class="logo" href="index.html" aria-label="Solar Technik BwM – Startseite">{LOGO}</a>
    <nav class="nav" aria-label="Hauptnavigation"><ul>
      <li class="has-dd"><button type="button"{on(svc_files)} aria-expanded="false" aria-controls="dd-l">Leistungen {CHEV}</button>{drop(SERVICES, 'leistungen.html', 'Alle Leistungen', 'dd-l')}</li>
      <li class="has-dd"><button type="button"{on(prd_files)} aria-expanded="false" aria-controls="dd-p">Produkte {CHEV}</button>{drop(PRODUCTS, 'produkte.html', 'Alle Produkte', 'dd-p')}</li>
      <li><a href="referenzen.html"{cur('referenzen.html')}>Referenzen</a></li>
      <li><a href="ueber-uns.html"{cur('ueber-uns.html')}>Über uns</a></li>
      <li><a href="ratgeber.html"{cur('ratgeber.html')}>Ratgeber</a></li>
      <li><a href="kontakt.html"{cur('kontakt.html')}>Kontakt</a></li>
    </ul></nav>
    <div class="right"><a class="tel" href="tel:{CO['telh']}" aria-label="Anrufen: {CO['tel']}">{TEL}<span>{CO['tel']}</span></a><a class="btn cu mag" href="kontakt.html">Anlage anfragen</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu"><span class="lbl">Menü</span><span class="lines"><span></span><span></span></span></button></div>
  </div>
</header>
<div class="menu" id="menu">
  <div class="menu-in">
    <ul>{''.join(f'<li><a href="{a}"{cur(a)}>{t}</a></li>' for a, t in ALLNAV)}</ul>
    <div class="menu-foot"><b>{CO['name']}</b><span>{CO['person']} · {CO['street']}, B-{CO['zip']} {CO['city']}</span><a href="tel:{CO['telh']}">{CO['tel']}</a><a href="mailto:{CO['mail']}">{CO['mail']}</a></div>
  </div>
</div>
<main id="main">
'''


def foot(p):
    return f'''</main>
<div class="sticky-cta"><a class="btn cu" href="kontakt.html">Anlage anfragen {ARROW}</a><a class="btn line" href="tel:{CO['telh']}" aria-label="Anrufen">{TEL}</a></div>
<footer class="footer">
  <div class="wrap">
    <div class="top">
      <div class="brand"><a class="logo" href="index.html" aria-label="Solar Technik BwM – Startseite">{LOGO}</a><p>Planung und Installation von Photovoltaikanlagen im Raum Aachen – für Kunden in Deutschland, Belgien und den Niederlanden.</p></div>
      <div><h4>Leistungen</h4><ul>{''.join(f'<li><a href="{s[0]}">{s[1]}</a></li>' for s in SERVICES)}</ul></div>
      <div><h4>Produkte</h4><ul>{''.join(f'<li><a href="{x[0]}">{x[1]}</a></li>' for x in PRODUCTS)}</ul></div>
      <div><h4>Solar Technik BwM</h4><ul><li><a href="referenzen.html">Referenzen</a></li><li><a href="ueber-uns.html">Über uns</a></li><li><a href="ratgeber.html">Ratgeber</a></li><li><a href="faq.html">Häufige Fragen</a></li><li><a href="kontakt.html">Kontakt</a></li></ul></div>
      <div><h4>Kontakt</h4><ul><li>{CO['person']}</li><li>{CO['street']}</li><li>B-{CO['zip']} {CO['city']}</li><li><a href="tel:{CO['telh']}">{CO['tel']}</a></li><li><a href="mailto:{CO['mail']}">{CO['mail']}</a></li></ul></div>
    </div>
    <div class="bottom"><span>© 2026 {CO['name']} · USt-ID {CO['vat']}</span><span class="legal"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></span><a class="totop" href="#">Nach oben</a></div>
  </div>
</footer>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.3.11/dist/lenis.min.js"></script>
<script src="main.js?v={VER}"></script>
</body>
</html>
'''


def ph(title, lead, dim, photo, alt, crumbs=None):
    """Bemaßungs-Kopf: Maßlinie mit dem Schlüsselmaß der Seite über dem Titel, rechts ein Foto im Umriss des Schienenprofils."""
    cr = f'<p class="crumb"><a href="index.html">Start</a> / {crumbs}</p>' if crumbs else ''
    ph_ = f'''<figure class="bh-photo" aria-hidden="true"><svg class="bh-clip" viewBox="0 0 100 100" preserveAspectRatio="none" width="0" height="0"><defs><clipPath id="prof" clipPathUnits="objectBoundingBox"><path d="{PROFILE}" transform="scale(.01)"/></clipPath></defs></svg><div class="bh-img">{pic(photo, alt, '(max-width: 900px) 70vw, 34vw', lazy=False)}</div><svg class="bh-line" viewBox="-2 -2 104 104" preserveAspectRatio="none"><path d="{PROFILE}" vector-effect="non-scaling-stroke"/></svg><span class="bh-dim-v"><i></i><b>40 mm</b></span></figure>''' if photo else ''
    return f'''<section class="bh{'' if photo else ' no-photo'}"><div class="wrap bh-grid">
  <div class="bh-text">{cr}
    <div class="dimline" aria-hidden="true"><i class="dl-a"></i><span>{dim}</span><i class="dl-b"></i></div>
    <h1 class="split">{title}</h1>
    <p class="lead reveal">{lead}</p>
  </div>
  {ph_}
</div></section>'''


def cta(h, t, btn='Anlage anfragen', href='kontakt.html'):
    return f'''<section class="sec tight"><div class="wrap"><div class="cta-band reveal"><div><h2>{h}</h2><p>{t}</p></div><div class="cta-act"><a class="btn cu big mag" href="{href}">{btn} {ARROW}</a><a class="cta-tel" href="tel:{CO['telh']}">{TEL}{CO['tel']}</a></div></div></div></section>'''


def more(file, group, title):
    others = [x for x in group if x[0] != file]
    return f'''<section class="sec tight more"><div class="wrap"><h2 class="h3">{title}</h2><ul class="more-list">{''.join(f'<li class="reveal"><a href="{x[0]}"><span class="ml-img">{pic(x[3], "", "120px")}</span><span class="ml-t">{x[1]}</span><span class="ml-d">{x[2]}</span>{ARROW}</a></li>' for x in others)}</ul></div></section>'''


def spec(rows, cap=None):
    r = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td></tr>' for a, b in rows)
    c = f'<caption>{cap}</caption>' if cap else ''
    return f'<div class="spec reveal"><table>{c}<tbody>{r}</tbody></table></div>'


def tool_icon(paths):
    return f'<svg class="ti" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'


def tool_head(t, lead):
    return f'<div class="tool-head"><p class="kicker">{tool_icon(next(x[3] for x in TOOLS if x[2] == t))} Selbst ausprobieren</p><h2>{t}</h2><p>{lead}</p></div>'


def faq_list(items):
    return '<div class="faq">' + ''.join(f'<details class="reveal"><summary><span>{q}</span><i aria-hidden="true"></i></summary><div class="a"><p>{a}</p></div></details>' for q, a in items) + '</div>'


def ld_faq(items):
    import re
    strip = lambda s: re.sub('<[^>]+>', '', s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}


def ld_crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + '/' + u} for i, (u, n) in enumerate(items)]}


ROOFS = [('flachdach', 'Flachdach'), ('satteldach', 'Satteldach'), ('pultdach', 'Pultdach'), ('freiflaeche', 'Freifläche')]
TOPICS = [('', 'Bitte wählen'), ('planung', 'Planung & Beratung'), ('montage', 'Montage'), ('anschliessen', 'Anschließen'), ('wartung', 'Wartung'), ('speicher', 'Speicher nachrüsten'), ('sonstiges', 'Etwas anderes')]


def form(idp='f', dark=False):
    """Anfrageformular mit den Feldern der alten Seite (Stromverbrauch, Warmwasserspeicher, Heizungsart) plus Dachform. Netlify-Forms-fertig."""
    roofs = ''.join(f'<label class="rc"><input type="radio" name="dachform" value="{t}"><span>{t}</span></label>' for k, t in ROOFS)
    topics = ''.join(f'<option value="{k}">{t}</option>' for k, t in TOPICS)
    return f'''<form class="form{' on-dark' if dark else ''}" name="anfrage" method="POST" action="danke.html" data-netlify="true" netlify-honeypot="bot-field" data-form novalidate>
  <input type="hidden" name="form-name" value="anfrage">
  <p class="hp"><label>Nicht ausfüllen: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <div class="fgrid">
    <label class="fld"><span>Name *</span><input name="name" autocomplete="name" required></label>
    <label class="fld"><span>E-Mail *</span><input type="email" name="email" autocomplete="email" required></label>
    <label class="fld"><span>Telefon</span><input type="tel" name="telefon" autocomplete="tel"></label>
    <label class="fld"><span>Adresse der Anlage</span><input name="adresse" autocomplete="street-address" placeholder="Straße, Ort"></label>
    <fieldset class="fld wide"><legend>Dachform</legend><div class="rcs">{roofs}</div></fieldset>
    <label class="fld"><span>Stromverbrauch pro Jahr</span><span class="unit"><input name="stromverbrauch" inputmode="numeric" placeholder="z. B. 4200"><i>kWh</i></span></label>
    <label class="fld"><span>Ihr Warmwasserspeicher</span><select name="warmwasser"><option value="">Bitte wählen</option><option>elektrisch (Boiler/Durchlauferhitzer)</option><option>über die Heizung</option><option>Wärmepumpe</option><option>weiß ich nicht</option></select></label>
    <label class="fld"><span>Heizungsart</span><select name="heizung"><option value="">Bitte wählen</option><option>Gas</option><option>Öl</option><option>Wärmepumpe</option><option>Strom (Nachtspeicher/Direkt)</option><option>Holz/Pellets</option><option>Fernwärme</option><option>andere</option></select></label>
    <label class="fld"><span>Thema</span><select name="thema">{topics}</select></label>
    <label class="fld wide"><span>Nachricht *</span><textarea name="nachricht" rows="4" required placeholder="Was haben Sie vor? Gern auch Dachgröße, Ausrichtung oder Wünsche zum Speicher."></textarea></label>
    <label class="chk wide"><input type="checkbox" name="datenschutz" required><span>Ich bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage gespeichert werden. Mehr in der <a href="datenschutz.html">Datenschutzerklärung</a>. *</span></label>
  </div>
  <div class="f-act"><button class="btn cu big mag" type="submit">Anfrage senden {ARROW}</button><p class="f-err" role="alert" aria-live="assertive"></p></div>
</form>'''


def write(p, body):
    html = head(p) + body + foot(p)
    open(OUT + p['file'], 'w', encoding='utf-8').write(html)
    return p['file']


PAGES = []


# =====================================================================
# STARTSEITE
# =====================================================================
SCENE = [  # Foto, Alt, Maß-Zeile, Titel, Text
    ('schiene', 'Querschnitt einer Montageschiene aus Aluminium mit T-Nut', 'Montageschiene · Aluminium · 40 × 40 × 6000 mm', 'Photovoltaik, die hält.', 'Planung und Installation von Photovoltaikanlagen im Dreiländereck. Solar Technik BwM aus Lontzen, für Kunden rund um Aachen.'),
    ('blechdach', 'Solarmodule auf einem Trapezblechdach, im Hintergrund Wiesen', 'Blechdach · Trapezblechschuh aus Edelstahl', 'Blechdach: der Trapezblechschuh.', 'Verstellbar, mit eingeklebtem EPDM-Gummi, passend für die meisten Trapezbleche.'),
    ('flachdach-stadt', 'Aufgeständerte Modulreihen auf einem Flachdach zwischen Stadthäusern', 'Flachdach · aufgeständert', 'Flachdach: in Reihen aufgeständert.', 'Die Gestelle stehen auf dem Dach und sind mit Betonsteinen beschwert, wie hier auf einem Dach in der Stadt.'),
    ('ziegeldach', 'Solarmodule auf einem dunklen Ziegeldach neben einem Dachfenster', 'Satteldach · Dachhaken aus Edelstahl', 'Ziegeldach: der Dachhaken.', 'Grundplatte 140 × 56 mm, dreifach verstellbar, für Standardpfannen. Auf den Haken läuft die Schiene.'),
    ('bruchsteinhaus', 'Bruchsteinhaus mit Photovoltaikanlage auf dem Satteldach', 'Jede Dachform', 'Planen, montieren, anschließen, warten.', 'Alles rund um Photovoltaik aus einer Hand, mit Produkten namhafter Hersteller. Auf Flachdach, Satteldach, Pultdach oder Freifläche.'),
]


def proj(lat, lon):
    return round((lon - 5.6) * 1000, 1), round((50.95 - lat) * 1580, 1)


def poly(pts):
    return 'M' + ' L'.join(f'{proj(a, b)[0]} {proj(a, b)[1]}' for a, b in pts)


BORDER_DE_BE = [(50.7543, 6.0207), (50.735, 6.040), (50.718, 6.052), (50.700, 6.085), (50.680, 6.110), (50.662, 6.140), (50.640, 6.170), (50.615, 6.190), (50.585, 6.220), (50.555, 6.260)]
BORDER_DE_NL = [(50.7543, 6.0207), (50.772, 6.030), (50.795, 6.018), (50.820, 6.030), (50.845, 6.055), (50.862, 6.075), (50.880, 6.088), (50.905, 6.070), (50.930, 6.040), (50.950, 6.010)]
BORDER_BE_NL = [(50.7543, 6.0207), (50.757, 5.975), (50.762, 5.910), (50.754, 5.845), (50.758, 5.780), (50.752, 5.720), (50.770, 5.695), (50.800, 5.690), (50.830, 5.650), (50.860, 5.640), (50.900, 5.660), (50.950, 5.640)]
PLACES = [('Lontzen', 50.69998, 5.98361, 'home'), ('Aachen', 50.776, 6.084, 'big'), ('Eupen', 50.630, 6.035, ''), ('Maastricht', 50.851, 5.691, 'big'), ('Heerlen', 50.888, 5.980, ''), ('Verviers', 50.589, 5.862, ''), ('Stolberg', 50.770, 6.228, '')]


RING = '<circle class="ring" r="18"/>'


def map_svg():
    pl = ''
    for n, la, lo, k in PLACES:
        x, y = proj(la, lo)
        dx, dy, anchor = {'Lontzen': (-18, 6, 'end'), 'Verviers': (-14, 5, 'end'), 'Stolberg': (0, 28, 'middle')}.get(n, (14, 5, 'start'))
        pl += f'<g transform="translate({x} {y})"><g class="pl {k}"><circle r="{9 if k == "home" else 5}"/>{RING if k == "home" else ""}<text x="{dx}" y="{dy}" text-anchor="{anchor}">{n}{" (Sitz)" if k == "home" else ""}</text></g></g>'
    ct = ''.join(f'<text class="ctry" x="{x}" y="{y}">{t}</text>' for t, x, y in [('DEUTSCHLAND', 480, 196), ('BELGIEN', 90, 470), ('NEDERLAND', 90, 90)])
    tp = proj(50.7543, 6.0207)
    return f'''<svg class="map" viewBox="0 0 700 632" role="img" aria-label="Schematische Karte des Dreiländerecks: Lontzen in Belgien, Aachen in Deutschland, Maastricht und Heerlen in den Niederlanden">
  {ct}
  <path class="border" pathLength="1" d="{poly(BORDER_DE_BE)}"/><path class="border" pathLength="1" d="{poly(BORDER_DE_NL)}"/><path class="border" pathLength="1" d="{poly(BORDER_BE_NL)}"/>
  <circle class="tri" cx="{tp[0]}" cy="{tp[1]}" r="6"/><text class="tri-l" x="{tp[0] + 12}" y="{tp[1] - 10}">Dreiländerpunkt</text>
  {pl}
</svg>'''


LAYERS = [  # Schicht, Titel, Angabe, Link, Versatz beim Auseinanderfahren
    ('klemme', 'End- und Mittelklemme', 'Aluminium schwarz eloxiert, Klemmlänge 70 mm, Modulabstand 2 cm', 'befestigung.html#klemmen', -250),
    ('modul', 'Solarmodul', 'JA Solar JAM72S10, 405 W, 2015 × 996 × 40 mm, 22,7 kg', 'module.html', -175),
    ('schiene', 'Montageschiene', 'Aluminium, 40 × 40 × 6000 mm, Befestigung M8 oder M10', 'befestigung.html#schiene', -105),
    ('haken', 'Dachhaken', 'Edelstahl 1.4016, Grundplatte 140 × 56 mm, dreifach verstellbar', 'befestigung.html#dachhaken', -45),
    ('dach', 'Ihr Dach', 'Pfanne, Blech, Bitumen oder Wiese: die Befestigung richtet sich danach', 'montage.html#werkzeug', 0),
]


def layers_svg():
    tiles = ''.join(f'<path d="M{x} 392q30-24 60 0"/>' for x in range(40, 860, 60))
    hatch = ''.join(f'<path d="M{x} 420l22-28"/>' for x in range(46, 860, 26))
    def hook(x):
        return f'<path class="hk" d="M{x - 34} 392H{x + 8}V372q0-10 10-10H{x + 26}V344"/>'
    cells = ''.join(f'<path d="M{x} 298v12"/>' for x in list(range(96, 444, 26)) + list(range(482, 830, 26)))
    def endclamp(x, d):
        return f'<path d="M{x} 290h{16 * d}v6h{-10 * d}v16h{-6 * d}z"/><path class="bolt" d="M{x + 6 * d} 296v24"/>'
    return f'''<svg class="layers-svg" viewBox="0 150 900 290" role="img" aria-label="Schnittzeichnung einer Photovoltaik-Montage: Dach, Dachhaken, Schiene, Modul und Klemmen fahren auseinander">
  <g class="ly" data-l="dach" data-dy="0"><rect class="rafter" x="40" y="392" width="820" height="28"/><g class="hatch">{hatch}</g><g class="tiles">{tiles}</g></g>
  <g class="ly" data-l="haken" data-dy="-45">{hook(210)}{hook(670)}</g>
  <g class="ly" data-l="schiene" data-dy="-105"><rect class="rail" x="60" y="312" width="780" height="32" rx="2"/><path class="rail-l" d="M60 320H840M60 336H840"/></g>
  <g class="ly" data-l="modul" data-dy="-175"><rect class="mod" x="70" y="296" width="374" height="16"/><rect class="mod" x="456" y="296" width="374" height="16"/><g class="cells">{cells}</g></g>
  <g class="ly" data-l="klemme" data-dy="-250"><g class="clamp">{endclamp(58, 1)}{endclamp(842, -1)}<path d="M432 290h36v6h-14v16h-8v-16h-14z"/><path class="bolt" d="M450 296v24"/></g></g>
  <g class="dims"><path d="M70 100H444M456 100H830M70 92v16M444 92v16M456 92v16M830 92v16"/><text x="257" y="84">996 mm</text><text x="643" y="84">996 mm</text><text class="gap" x="450" y="84">2 cm</text></g>
</svg>'''


def home():
    frames = ''
    for i, (ph_, alt, spec_, t, d) in enumerate(SCENE):
        img = pic(ph_, alt, '100vw', lazy=False) if i == 0 else pic(ph_, alt, '100vw', late=True)
        tag = 'h1' if i == 0 else 'h2'
        act = f'<div class="cap-act"><a class="btn cu big mag" href="kontakt.html">Anlage anfragen {ARROW}</a><a class="btn ghost" href="montage.html">So befestigen wir</a></div>' if i == 4 else ''
        frames += f'<div class="frame f{i}"><div class="fimg">{img}</div><div class="shade"></div></div>'
        frames += f'<div class="cap c{i}"><div class="wrap"><p class="spec-l">{spec_}</p><{tag}>{t}</{tag}><p>{d}</p>{act}</div></div>'
    static = ''.join(f'<figure>{pic(ph_, alt, "(max-width: 700px) 100vw, 50vw")}<figcaption><b>{t}</b> {d}</figcaption></figure>' for ph_, alt, s, t, d in SCENE)
    static = static.replace(' src="img/', ' data-st-src="img/').replace(' srcset="', ' data-st-srcset="')
    clamps = ''.join(f'<i style="left:{k * 25}%"></i>' for k in range(5))
    rail_items = ''.join(f'''<li class="ri" style="--k:{k}"><a href="{s[0]}"><svg class="ri-clamp" viewBox="0 0 60 40" aria-hidden="true"><path d="M4 4h52v8H36v24h-12V12H4z"/></svg><span class="ri-t">{s[1]}</span><span class="ri-d">{s[2]}</span><span class="ri-go">Mehr {ARROW}</span></a></li>''' for k, s in enumerate(SERVICES))
    ltab = ''.join(f'<li data-l="{l}"><a href="{u}"><b>{t}</b><span>{d}</span>{ARROW}</a></li>' for l, t, d, u, dy in LAYERS)
    roof_tabs = ''.join(f'<button type="button" role="tab" id="rt-{k}" aria-controls="rp" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-roof="{k}">{t}</button>' for i, (k, t) in enumerate(ROOFS))
    shots = [('flachdach-stadt', 'Flachdach in der Stadt', 'Aufgeständerte Reihen, Dezember 2022'), ('flachdach-ballast', 'Flachdach, Detail', 'Gestell mit Betonsteinen als Ballast'),
             ('blechdach-weit', 'Blechdach auf dem Land', 'Trapezblech, August 2022'), ('backsteinhaus', 'Backsteinhaus', 'Satteldach, Dezember 2022'),
             ('ziegeldach', 'Ziegeldach', 'Module neben dem Dachfenster, Dezember 2022'), ('flachdach-hof', 'Flachdach mit Ausblick', 'Zwei Reihen, Dezember 2022')]
    thumbs = ''.join(f'<li><button type="button" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}" aria-label="Foto zeigen: {t}">{pic(n, "", "120px")}</button></li>' for i, (n, t, d) in enumerate(shots))
    big = ''.join(f'<figure class="bs-f{" on" if i == 0 else ""}" data-i="{i}">{pic(n, t + ": " + d, "(max-width: 900px) 100vw, 60vw")}<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>' for i, (n, t, d) in enumerate(shots))
    tools = ''.join(f'<li class="tl"><a href="{a}#werkzeug">{tool_icon(ic)}<span class="tl-q">{q}</span><span class="tl-t">{t}</span>{ARROW}</a></li>' for a, q, t, ic in TOOLS)
    body = f'''
<section class="scene" aria-label="Was eine Anlage trägt">
  <div class="scene-pin">
    {frames}
    <div class="srail" aria-hidden="true"><span class="sr-bar"><b></b></span>{clamps}</div>
  </div>
  <div class="scene-static wrap">{static}</div>
</section>

<section class="sec region" id="region"><div class="wrap region-grid">
  <div class="region-text">
    <p class="kicker">Raum Aachen · Ostbelgien · Südlimburg</p>
    <h2 class="split">Ein Betrieb, drei Länder.</h2>
    <p class="lead reveal">Wir haben uns auf die Planung und Installation hochwertiger Photovoltaikanlagen im Raum Aachen spezialisiert. Unser Kundenkreis liegt im Dreiländereck Deutschland, Belgien und Niederlande.</p>
    <p class="reveal">Um Ihnen ein hohes Maß an Investitionssicherheit für viele Jahre zu bieten, arbeiten wir ausschließlich mit namhaften Herstellern und deren Qualitätsprodukten.</p>
    <a class="link reveal" href="ueber-uns.html">Über Solar Technik BwM {ARROW}</a>
  </div>
  <div class="region-map">{map_svg()}<p class="map-note">Schematische Darstellung</p></div>
</div></section>

<section class="layers" id="aufbau" aria-labelledby="ly-h">
  <div class="layers-pin"><div class="wrap layers-grid">
    <div class="layers-head"><p class="kicker">Der Aufbau</p><h2 id="ly-h">Was eine Anlage trägt.</h2><p>Von der Pfanne bis zur Klemme: fünf Schichten, und jede muss sitzen. Die Maße stammen aus unserem Material.</p></div>
    <div class="layers-draw">{layers_svg()}<p class="nts">Nicht maßstäblich</p></div>
    <ol class="layers-list">{ltab}</ol>
  </div></div>
</section>

<section class="sec rail-sec" id="leistungen"><div class="wrap">
  <div class="sec-head"><p class="kicker">Leistungen</p><h2 class="split">Wir machen alles rund um Photovoltaik.</h2></div>
  <div class="rail-wrap"><div class="rail-bar" aria-hidden="true"><i></i></div><ul class="rail-items">{rail_items}</ul></div>
</div></section>

<section class="sec roofs dark" id="dachformen"><div class="wrap">
  <div class="sec-head"><p class="kicker">Dachformen</p><h2 class="split">Flachdach, Satteldach, Pultdach oder Wiese.</h2><p class="lead reveal">Jegliche Wünsche der Anbringung sind möglich. Was sich ändert, ist das, was die Module hält.</p></div>
  <div class="roof-ui">
    <div class="roof-tabs" role="tablist" aria-label="Dachform wählen">{roof_tabs}</div>
    <div class="roof-panel" id="rp" role="tabpanel" aria-labelledby="rt-flachdach">
      <div class="roof-draw">
        <svg viewBox="0 0 400 210" aria-hidden="true"><path class="ground" d="M10 190H390"/><polygon class="house" points="60,190 60,95 200,95 200,95 340,95 340,190"/>
          <g class="rm rm-flachdach"><path d="M92 95l26-18v18M150 95l26-18v18M208 95l26-18v18M266 95l26-18v18"/><path class="rm-p" d="M92 95l26-18M150 95l26-18M208 95l26-18M266 95l26-18"/></g>
          <g class="rm rm-satteldach"><path class="rm-p" d="M92 94l100-48M214 50l96 47"/></g>
          <g class="rm rm-pultdach"><path class="rm-p" d="M84 64l232 34"/></g>
          <g class="rm rm-freiflaeche"><path d="M70 190v-34M150 190v-34M230 190v-34M310 190v-34"/><path class="rm-p" d="M50 168l60-40M130 168l60-40M210 168l60-40M290 168l60-40"/></g>
        </svg>
      </div>
      <div class="roof-info">
        <div class="roof-photo">{pic('flachdach-reihen', 'Aufgeständerte Modulreihen auf einem Flachdach', '(max-width: 900px) 100vw, 40vw', cls='rp-img')}</div>
        <h3 class="roof-t">Flachdach</h3>
        <p class="roof-d">Die Module stehen in Reihen auf Gestellen, beschwert mit Betonsteinen. Neigung und Reihenabstand planen wir so, dass sich die Reihen nicht verschatten.</p>
        <a class="link" href="montage.html#werkzeug">Befestigung für Ihr Dach finden {ARROW}</a>
      </div>
    </div>
  </div>
</div></section>

<section class="sec shots" id="baustellen"><div class="wrap">
  <div class="sec-head row"><div><p class="kicker">Referenzen</p><h2 class="split">Von unseren Dächern.</h2></div><a class="link reveal" href="referenzen.html">Alle Referenzen {ARROW}</a></div>
  <div class="bs">
    <div class="bs-stage"><span class="reg tl" aria-hidden="true"></span><span class="reg tr" aria-hidden="true"></span><span class="reg bl" aria-hidden="true"></span><span class="reg br" aria-hidden="true"></span>
      <div class="bs-dim h" aria-hidden="true"><i></i></div><div class="bs-dim v" aria-hidden="true"><i></i></div>
      <div class="bs-frame">{big}</div>
    </div>
    <ul class="bs-thumbs" aria-label="Fotos wählen">{thumbs}</ul>
  </div>
</div></section>

<section class="sec tools-sec" id="ausprobieren"><div class="wrap tools-grid">
  <div class="sec-head sticky-h"><p class="kicker">Selbst ausprobieren</p><h2 class="split">Acht Fragen, acht kleine Werkzeuge.</h2><p class="reveal">Jede Frage führt direkt zum passenden Rechner oder Wegweiser auf der Unterseite. Die Ergebnisse sind Richtwerte, keine Planung.</p></div>
  <div class="tools-list"><span class="tape" aria-hidden="true"><i></i></span><ul>{tools}</ul></div>
</div></section>

<section class="sec ask dark" id="anfrage"><div class="wrap ask-grid">
  <div class="ask-text"><p class="kicker">Anfrage</p><h2 class="split">Erzählen Sie uns von Ihrem Dach.</h2>
    <p class="reveal">Mit Stromverbrauch, Heizung und Warmwasser können wir die Anlage schon grob auslegen, bevor wir vorbeikommen.</p>
    <ul class="ask-contact reveal"><li>{TEL}<a href="tel:{CO['telh']}">{CO['tel']}</a></li><li>{MAIL}<a href="mailto:{CO['mail']}">{CO['mail']}</a></li><li>{PIN}<span>{CO['person']}, {CO['street']}, B-{CO['zip']} {CO['city']}</span></li></ul>
  </div>
  <div class="ask-sheet"><span class="reg tl" aria-hidden="true"></span><span class="reg tr" aria-hidden="true"></span><span class="reg bl" aria-hidden="true"></span><span class="reg br" aria-hidden="true"></span>{form('h', True)}</div>
</div></section>
'''
    p = dict(file='index.html', title='Photovoltaik im Dreiländereck | Solar Technik BwM', body='home',
             desc='Solar Technik BwM aus Lontzen plant, montiert, schließt an und wartet Photovoltaikanlagen im Raum Aachen, in Ostbelgien und Südlimburg.')
    return write(p, body)


PAGES.append(home)


# =====================================================================
# LEISTUNGEN
# =====================================================================
def chips(name, items, on=0, label=''):
    b = ''.join(f'<button type="button" class="chip{" on" if i == on else ""}" data-v="{v}" aria-pressed="{"true" if i == on else "false"}">{t}</button>' for i, (v, t) in enumerate(items))
    return f'<div class="chips" data-k="{name}" role="group" aria-label="{label}">{b}</div>'


def leistungen():
    rows = ''
    for i, (a, t, d, ph_) in enumerate(SERVICES):
        tool = next(x for x in TOOLS if x[0] == a)
        rows += f'''<article class="lrow reveal{' flip' if i % 2 else ''}"><a class="lrow-img" href="{a}" tabindex="-1" aria-hidden="true">{pic(ph_, '', '(max-width: 900px) 100vw, 45vw')}</a>
  <div class="lrow-t"><h2><a href="{a}">{t}</a></h2><p>{d}</p><p class="lrow-tool">{tool_icon(tool[3])}<a href="{a}#werkzeug">{tool[2]}: {tool[1]}</a></p><a class="btn line" href="{a}">{t} ansehen {ARROW}</a></div></article>'''
    body = ph('Leistungen', 'Wir machen alles rund um Photovoltaik: von der ersten Beratung über die Montage und den Anschluss bis zur Wartung. Alles aus einer Hand, im ganzen Dreiländereck.', 'Planen · Montieren · Anschließen · Warten', 'flachdach-stadt', 'Aufgeständerte Modulreihen auf einem Flachdach in der Stadt', 'Leistungen') + \
        f'<section class="sec"><div class="wrap lrows">{rows}</div></section>' + cta('Welche Leistung brauchen Sie?', 'Eine neue Anlage, ein Speicher zum Nachrüsten oder eine Wartung: Schreiben Sie uns kurz, worum es geht.')
    p = dict(file='leistungen.html', title='Leistungen: Planung, Montage, Anschluss, Wartung | Solar BwM',
             desc='Planung und Beratung, Montage, Anschließen und Wartung von Photovoltaikanlagen im Raum Aachen und in Ostbelgien: alles aus einer Hand.',
             ld=ld_crumbs([('', 'Start'), ('leistungen.html', 'Leistungen')]))
    return write(p, body)


def planung():
    looks = [('Dachfläche und Ausrichtung', 'Wie groß ist die Fläche, wohin zeigt sie, was wirft Schatten: Kamin, Gaube, Baum, Nachbarhaus?'),
             ('Eindeckung und Unterkonstruktion', 'Pfanne, Blech oder Bitumen, dazu Sparren und Lattung. Davon hängt ab, womit wir befestigen.'),
             ('Stromverbrauch, Heizung und Warmwasser', 'Die Jahresabrechnung zeigt, wie viel Strom Sie brauchen. Heizung und Warmwasser zeigen, wohin er künftig fließen kann.'),
             ('Speicher, E-Auto, Wärmepumpe', 'Was heute schon da ist und was in den nächsten Jahren dazukommen soll, planen wir gleich mit ein.'),
             ('Zählerschrank und Anschluss', 'Wo Wechselrichter, Speicher und Energiezähler Platz finden und wie die Kabel dorthin kommen.')]
    lk = ''.join(f'<li class="reveal"><h3>{a}</h3><p>{b}</p></li>' for a, b in looks)
    steps = [('Anfrage', 'Sie schreiben oder rufen an, am besten mit Verbrauch, Dachform und ein paar Fotos.'), ('Gespräch vor Ort', 'Wir sehen uns Dach, Zählerschrank und Wünsche an.'),
             ('Angebot', 'Sie bekommen eine Auslegung mit Modulen, Befestigung, Wechselrichter und auf Wunsch Speicher.'), ('Montage und Anschluss', 'Wir bauen auf, schließen an und nehmen die Anlage in Betrieb.')]
    st = ''.join(f'<li class="reveal"><b>{a}</b><span>{b}</span></li>' for a, b in steps)
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Anfrage-Steckbrief', 'Die Felder unseres Anfrageformulars zum Durchklicken. Am Ende steht Ihr Steckbrief, den Sie mit einem Klick ins Formular übernehmen.')}
  <div class="tool card" data-tool="brief">
    <div class="tq"><p class="tl-l">Dachform</p>{chips('dach', [(t, t) for k, t in ROOFS], 1, 'Dachform')}</div>
    <div class="tq"><label class="tl-l" for="b-kwh">Stromverbrauch pro Jahr (von der Jahresabrechnung)</label><span class="unit"><input id="b-kwh" inputmode="numeric" placeholder="z. B. 4200" data-in="kwh"><i>kWh</i></span></div>
    <div class="tq"><p class="tl-l">Heizung</p>{chips('heizung', [(x, x) for x in ['Gas', 'Öl', 'Wärmepumpe', 'Strom', 'Holz/Pellets', 'andere']], 0, 'Heizung')}</div>
    <div class="tq"><p class="tl-l">Warmwasser</p>{chips('ww', [(x, x) for x in ['über die Heizung', 'elektrisch', 'Wärmepumpe', 'weiß ich nicht']], 0, 'Warmwasser')}</div>
    <div class="tq"><p class="tl-l">E-Auto</p>{chips('auto', [(x, x) for x in ['vorhanden', 'geplant', 'nein']], 2, 'E-Auto')}</div>
    <div class="tq"><p class="tl-l">Speicher</p>{chips('speicher', [(x, x) for x in ['gewünscht', 'vielleicht', 'nein']], 1, 'Speicher')}</div>
    <div class="brief-out" aria-live="polite"><p class="bo-h">Ihr Steckbrief</p><dl class="bo-dl"></dl><p class="bo-hint"></p><a class="btn cu mag" href="kontakt.html" data-brief-link>In die Anfrage übernehmen {ARROW}</a></div>
  </div>
</div></section>'''
    body = ph('Planung & Beratung', 'Bevor ein Modul aufs Dach kommt, sehen wir uns Ihr Dach, Ihren Verbrauch und Ihre Pläne an. Daraus entsteht eine Anlage, die zu Ihnen passt.', 'Dach · Verbrauch · Wünsche', 'bruchsteinhaus', 'Bruchsteinhaus mit Photovoltaikanlage auf dem Satteldach', '<a href="leistungen.html">Leistungen</a> / Planung & Beratung') + f'''
<section class="sec"><div class="wrap two">
  <div class="sec-head sticky-h"><p class="kicker">Was wir uns ansehen</p><h2 class="split">Fünf Dinge entscheiden über die Anlage.</h2></div>
  <ol class="looks">{lk}</ol>
</div></section>
<section class="sec grey"><div class="wrap"><div class="sec-head"><p class="kicker">Ablauf</p><h2 class="split">Von der Anfrage bis zur laufenden Anlage.</h2></div><ol class="flow">{st}</ol><p class="note reveal">Der genaue Ablauf richtet sich nach Ihrem Vorhaben und nach dem Land, in dem die Anlage steht.</p></div></section>
{tool}
<section class="sec tight"><div class="wrap quote-line reveal"><p>„Um Ihnen ein hohes Maß an Investitionssicherheit für viele Jahre bieten zu können, arbeiten wir ausschließlich mit namhaften Herstellern und deren Qualitätsprodukten.“</p><a class="link" href="produkte.html">Unsere Produkte {ARROW}</a></div></section>
''' + more('planung-beratung.html', SERVICES, 'Weitere Leistungen') + cta('Lassen Sie uns Ihr Dach ansehen.', 'Schicken Sie uns Verbrauch, Dachform und ein paar Fotos. Wir melden uns mit einem Termin.')
    p = dict(file='planung-beratung.html', parent='leistungen.html', title='Photovoltaik planen lassen, Raum Aachen | Solar Technik BwM',
             desc='Planung und Beratung für Ihre Photovoltaikanlage: Dach, Verbrauch, Heizung und Speicher. Mit Anfrage-Steckbrief zum Durchklicken.',
             ld=ld_crumbs([('', 'Start'), ('leistungen.html', 'Leistungen'), ('planung-beratung.html', 'Planung & Beratung')]))
    return write(p, body)


COVERS = [  # Eindeckung, Titel, Befestigung, Foto, Text, Teile
    ('pfanne', 'Tonziegel oder Betondachstein', 'Dachhaken aus Edelstahl', 'dachhaken', 'Der Haken wird auf den Sparren geschraubt und läuft unter der Pfanne hindurch nach außen. Er ist dreifach verstellbar, damit die Schiene trotz unebener Dachfläche gerade liegt.', ['Dachhaken, Grundplatte 140 × 56 mm', 'Montageschiene 40 × 40 mm', 'End- und Mittelklemmen']),
    ('blech', 'Trapezblech', 'Trapezblechschuh aus Edelstahl', 'blechdach-weit', 'Der Schuh sitzt auf der Hochsicke des Blechs. Ein eingeklebtes EPDM-Gummi dichtet ab. Er ist verstellbar und passt auf die meisten Trapezbleche.', ['Trapezblechschuh mit EPDM-Gummi', 'Montageschiene 40 × 40 mm', 'End- und Mittelklemmen']),
    ('flach', 'Bitumen oder Folie (Flachdach)', 'Aufständerung mit Ballast', 'flachdach-ballast', 'Die Module stehen geneigt in Reihen auf Gestellen. Betonsteine beschweren das Gestell. Wie viel Ballast nötig ist, hängt von Dachhöhe, Lage und Windlast ab.', ['Gestell zur Aufständerung', 'Ballast aus Betonsteinen', 'End- und Mittelklemmen']),
    ('wiese', 'Wiese (Freifläche)', 'Gestell auf dem Boden', 'flachdach-hof', 'Auf der Freifläche bestimmen wir Neigung und Ausrichtung frei. Das Gestell steht auf dem Grundstück, die Module werden wie auf dem Dach geklemmt.', ['Freiflächen-Gestell', 'Montageschiene 40 × 40 mm', 'End- und Mittelklemmen']),
]


def montage():
    seq = [('dachhaken', 'Haken setzen', 'Auf Ziegeldächern schrauben wir Dachhaken aus Edelstahl auf die Sparren. Auf Blech kommt der Trapezblechschuh, auf dem Flachdach das Gestell.'),
           ('schiene', 'Schienen ausrichten', 'Die Aluminiumschienen 40 × 40 mm laufen quer über die Haken. Sie werden mit M8- oder M10-Schrauben befestigt und gerade ausgerichtet.'),
           ('mittelklemme', 'Module klemmen', 'Zwischen zwei Modulen sitzt die Mittelklemme mit 2 cm Abstand, am Rand die Endklemme. Beide sind schwarz eloxiert und 70 mm lang.'),
           ('flachdach-reihen', 'Kabel führen', 'Die Leitungen laufen geschützt unter den Modulen zur Hauswand und weiter zum Wechselrichter.')]
    sq = ''.join(f'<li class="sq reveal"><div class="sq-img">{pic(n, t, "(max-width: 900px) 100vw, 25vw")}</div><h3>{t}</h3><p>{d}</p></li>' for n, t, d in seq)
    opts = ''.join(f'<button type="button" class="chip{" on" if i == 0 else ""}" data-v="{k}" aria-pressed="{"true" if i == 0 else "false"}">{t}</button>' for i, (k, t, *_r) in enumerate(COVERS))
    data = json.dumps({k: dict(t=t, b=b, img=f'img/{ph_}-m.webp', d=d, parts=parts) for k, t, b, ph_, d, parts in COVERS}, ensure_ascii=False)
    c0 = COVERS[0]
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Befestigung nach Eindeckung', 'Wählen Sie, womit Ihr Dach gedeckt ist. Sie sehen, womit wir die Anlage darauf befestigen und welche Teile dazugehören.')}
  <div class="tool card" data-tool="cover">
    <div class="chips" data-k="cover" role="group" aria-label="Dacheindeckung">{opts}</div>
    <div class="cover-out" aria-live="polite">
      <div class="co-img">{pic(c0[3], c0[2], '(max-width: 900px) 100vw, 30vw', cls='co-photo')}</div>
      <div><p class="co-k">Befestigung</p><h3 class="co-b">{c0[2]}</h3><p class="co-d">{c0[4]}</p><ul class="co-parts">{''.join(f'<li>{x}</li>' for x in c0[5])}</ul></div>
    </div>
    <script type="application/json" class="co-data">{data}</script>
  </div>
</div></section>'''
    body = ph('Montage', 'Flachdach, Satteldach, Pultdach oder Freifläche: Wir montieren auf jeder Dachform. Was sich ändert, ist das Gestell darunter. Darauf kommt es an.', 'Flach · Sattel · Pult · Frei', 'flachdach-reihen', 'Aufgeständerte Modulreihen auf einem Flachdach', '<a href="leistungen.html">Leistungen</a> / Montage') + f'''
<section class="sec"><div class="wrap"><div class="sec-head"><p class="kicker">Von unten nach oben</p><h2 class="split">Wie eine Anlage aufs Dach kommt.</h2></div><ol class="seq">{sq}</ol></div></section>
{tool}
<section class="sec tight"><div class="wrap media-row reveal"><div class="mr-img">{pic('kran', 'Kran-LKW auf einem Hof', '(max-width: 900px) 100vw, 50vw')}</div><div class="mr-t"><h2 class="h3">Material bis aufs Dach</h2><p>Schienen sind sechs Meter lang, ein Modul wiegt 22,7 kg. Wo es eng oder hoch wird, bringen wir das Material mit dem Kran-LKW nach oben.</p><a class="link" href="befestigung.html">Unser Befestigungsmaterial {ARROW}</a></div></div></section>
''' + more('montage.html', SERVICES, 'Weitere Leistungen') + cta('Welche Dachform haben Sie?', 'Schicken Sie uns ein Foto Ihres Daches. Wir sagen Ihnen, wie wir darauf montieren würden.')
    p = dict(file='montage.html', parent='leistungen.html', title='PV-Montage auf Flach-, Sattel- und Pultdach | Solar Technik BwM',
             desc='Montage von Photovoltaik auf Flachdach, Satteldach, Pultdach und Freifläche: Dachhaken, Trapezblechschuh oder Aufständerung mit Ballast.',
             ld=ld_crumbs([('', 'Start'), ('leistungen.html', 'Leistungen'), ('montage.html', 'Montage')]))
    return write(p, body)


def anschliessen():
    chain = [('Module', 'Die Module erzeugen Gleichstrom. Mehrere hintereinander bilden einen Strang, der zum Wechselrichter führt.', 'module.html'),
             ('Wechselrichter', 'Er macht aus dem Gleichstrom Wechselstrom für Ihr Hausnetz und sucht über zwei MPP-Tracker den besten Arbeitspunkt.', 'wechselrichter.html'),
             ('Batteriespeicher', 'Was tagsüber übrig bleibt, lädt den Speicher. Abends gibt er es wieder ab.', 'speicher.html'),
             ('Energiezähler', 'Am Netzanschlusspunkt misst der Smart Power Sensor, wie viel Strom Sie beziehen und einspeisen. Danach richten sich Wechselrichter und Speicher.', 'energiezaehler.html'),
             ('Inbetriebnahme', 'Wir prüfen die Stränge, stellen die Geräte ein und zeigen Ihnen, wo Sie Ertrag und Meldungen ablesen.', None)]
    ch = ''.join(f'<li class="reveal"><b>{t}</b><p>{d}</p>{f"<a class=link href={u}>{t} ansehen {ARROW}</a>" if u else ""}</li>' for t, d, u in chain)
    devs = [('wasch', 'Waschmaschine'), ('spuel', 'Spülmaschine'), ('trock', 'Trockner'), ('auto', 'E-Auto laden'), ('ww', 'Warmwasser elektrisch')]
    slots = [('morgens', 'morgens'), ('mittags', 'mittags'), ('nachmittags', 'nachm.'), ('abends', 'abends'), ('nachts', 'nachts')]
    start = {'wasch': 3, 'spuel': 3, 'trock': 2, 'auto': 3, 'ww': 0}
    rows = ''.join(f'<div class="dv" data-d="{k}"><p class="dv-n">{t}</p>{chips(k, slots, start[k], "Uhrzeit für " + t)}</div>' for k, t in devs)
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Tagesplan der Geräte', 'Wann laufen Ihre großen Verbraucher? Wählen Sie für jedes Gerät die übliche Tageszeit und sehen Sie, wie viel davon in die Sonnenstunden fällt.')}
  <div class="tool card" data-tool="day">
    <svg class="day-svg" viewBox="0 0 500 170" aria-hidden="true"><path class="day-axis" d="M20 140H480"/><path class="day-sun" d="M20 140C120 140 150 30 250 30S380 140 480 140"/>
      <g class="day-ticks"><text x="20" y="162">0 Uhr</text><text x="137" y="162">6</text><text x="250" y="162">12</text><text x="363" y="162">18</text><text x="480" y="162" text-anchor="end">24</text></g><g class="day-marks"></g></svg>
    <div class="dvs">{rows}</div>
    <p class="day-out" aria-live="polite"></p>
    <p class="note">Schematische Sonnenkurve für einen hellen Tag. Wie viel Ihre Anlage wirklich liefert, hängt von Jahreszeit, Wetter und Ausrichtung ab.</p>
  </div>
</div></section>'''
    body = ph('Anschließen', 'Eine Anlage ist erst fertig, wenn sie Strom ins Haus liefert. Wir verbinden Module, Wechselrichter, Speicher und Energiezähler und nehmen alles in Betrieb.', 'Gleichstrom → Wechselstrom', 'blechdach', 'Solarmodule auf einem Blechdach in der Sonne', '<a href="leistungen.html">Leistungen</a> / Anschließen') + f'''
<section class="sec"><div class="wrap two">
  <div class="sec-head sticky-h"><p class="kicker">Vom Dach bis zum Zähler</p><h2 class="split">Was wir alles verbinden.</h2><p class="reveal">Die Anmeldung beim Netzbetreiber besprechen wir mit Ihnen vorab. In Deutschland, Belgien und den Niederlanden gelten dafür unterschiedliche Regeln.</p></div>
  <ol class="chain">{ch}</ol>
</div></section>
{tool}
''' + more('anschliessen.html', SERVICES, 'Weitere Leistungen') + cta('Die Anlage ist schon da?', 'Auch einen Speicher oder einen Energiezähler schließen wir nachträglich an. Fragen Sie uns.', 'Anschluss anfragen', 'kontakt.html?thema=anschliessen')
    p = dict(file='anschliessen.html', parent='leistungen.html', title='PV-Anlage anschließen und in Betrieb nehmen | Solar BwM',
             desc='Wir schließen Module, Wechselrichter, Batteriespeicher und Energiezähler an und nehmen die Photovoltaikanlage in Betrieb. Mit Tagesplan-Werkzeug.',
             ld=ld_crumbs([('', 'Start'), ('leistungen.html', 'Leistungen'), ('anschliessen.html', 'Anschließen')]))
    return write(p, body)


SYMPTOMS = [
    ('weniger', 'Der Ertrag ist deutlich gesunken', ['Mit dem gleichen Monat im Vorjahr vergleichen, nicht mit dem Vormonat.', 'In der App nachsehen, ob beide Stränge Leistung melden.', 'Vom Boden aus schauen: Laub, Moos oder neue Schatten durch Bäume?'], 'Wenn ein Strang dauerhaft deutlich weniger liefert als der andere oder der Ertrag auch bei Sonne einbricht.'),
    ('meldung', 'Der Wechselrichter zeigt eine Meldung', ['Meldung mit Text oder Code notieren oder fotografieren.', 'In der App prüfen, seit wann sie ansteht.', 'Nicht wiederholt aus- und einschalten.'], 'Bei jeder Meldung, die nach einem sonnigen Tag noch ansteht, und immer bei Isolations- oder Erdschlussmeldungen.'),
    ('app', 'Die App zeigt keine Daten', ['WLAN-Router und Stromversorgung des Wechselrichters prüfen.', 'Nachsehen, ob der Wechselrichter selbst Leistung anzeigt.', 'Passwort des WLANs geändert? Dann muss die Verbindung neu eingerichtet werden.'], 'Wenn der Wechselrichter selbst keine Leistung anzeigt oder die Verbindung sich nicht wieder einrichten lässt.'),
    ('sturm', 'Nach Sturm oder Hagel', ['Vom Boden aus nach verrutschten Modulen, gelösten Kabeln oder Glasbruch sehen.', 'Fotos machen, für die Versicherung.', 'Nicht aufs Dach steigen.'], 'Sofort, wenn ein Modul verrutscht, Glas gebrochen oder ein Kabel sichtbar gelöst ist.'),
    ('speicher', 'Der Speicher lädt nicht mehr voll', ['In der App den Ladestand über mehrere Tage ansehen.', 'Im Winter ist ein nicht ganz voller Speicher normal.', 'Prüfen, ob der Energiezähler Werte liefert.'], 'Wenn der Speicher auch an sonnigen Sommertagen nicht mehr lädt oder eine Meldung zeigt.'),
]


def wartung():
    checks = [('Befestigung', 'Sitzen Dachhaken, Schienen und Klemmen fest? Hat sich nach Sturm oder Schnee etwas verschoben?'), ('Module', 'Sichtprüfung auf Glasbruch, Verfärbungen und Verschmutzung.'),
              ('Kabel und Stecker', 'Leitungen, Steckverbinder und Kabelführung auf Scheuerstellen und festen Sitz.'), ('Wechselrichter und Speicher', 'Meldungen, Lüftung und Einstellungen, Stand der Software.'),
              ('Ertrag', 'Wir vergleichen den Ertrag mit den Vorjahren und zwischen den Strängen.')]
    ck = ''.join(f'<li class="reveal"><h3>{a}</h3><p>{b}</p></li>' for a, b in checks)
    opts = ''.join(f'<button type="button" class="sym{" on" if i == 0 else ""}" data-v="{k}" aria-pressed="{"true" if i == 0 else "false"}">{t}</button>' for i, (k, t, *_r) in enumerate(SYMPTOMS))
    panels = ''.join(f'<div class="sym-p{" on" if i == 0 else ""}" data-p="{k}"><h3>{t}</h3><div class="sp-2"><div><p class="sp-k">Das können Sie selbst prüfen</p><ul>{"".join(f"<li>{x}</li>" for x in own)}</ul></div><div class="sp-call"><p class="sp-k">Dann rufen Sie uns</p><p>{call}</p><a class="btn cu" href="kontakt.html?thema=wartung">Wartung anfragen {ARROW}</a></div></div></div>' for i, (k, t, own, call) in enumerate(SYMPTOMS))
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Symptom-Wegweiser', 'Was ist Ihnen aufgefallen? Sie sehen, was Sie gefahrlos selbst prüfen können und wann Sie uns rufen sollten.')}
  <div class="tool card" data-tool="sym"><div class="syms" role="group" aria-label="Was ist aufgefallen?">{opts}</div><div class="sym-ps" aria-live="polite">{panels}</div>
  <p class="note warn">Bitte nie selbst aufs Dach steigen und nichts an Steckern oder Kabeln lösen: Auf der Gleichstromseite liegen je nach Anlage mehrere hundert Volt an, auch wenn der Wechselrichter aus ist.</p></div>
</div></section>'''
    body = ph('Wartung', 'Eine Photovoltaikanlage soll viele Jahre laufen. Damit das so bleibt, prüfen wir Befestigung, Module, Kabel, Wechselrichter und Ertrag.', 'Jahr für Jahr', 'ziegeldach', 'Solarmodule auf einem dunklen Ziegeldach', '<a href="leistungen.html">Leistungen</a> / Wartung') + f'''
<section class="sec"><div class="wrap two">
  <div class="sec-head sticky-h"><p class="kicker">Was wir prüfen</p><h2 class="split">Von der Klemme bis zum Ertrag.</h2></div>
  <ol class="looks">{ck}</ol>
</div></section>
{tool}
''' + more('wartung.html', SERVICES, 'Weitere Leistungen') + cta('Ihre Anlage braucht einen Blick?', 'Auch Anlagen, die wir nicht selbst gebaut haben, sehen wir uns an. Schreiben Sie uns, was Ihnen aufgefallen ist.', 'Wartung anfragen', 'kontakt.html?thema=wartung')
    p = dict(file='wartung.html', parent='leistungen.html', title='Wartung von Photovoltaikanlagen | Solar Technik BwM',
             desc='Wartung Ihrer PV-Anlage: Befestigung, Module, Kabel, Wechselrichter und Ertrag. Mit Symptom-Wegweiser: Was Sie selbst prüfen können.',
             ld=ld_crumbs([('', 'Start'), ('leistungen.html', 'Leistungen'), ('wartung.html', 'Wartung')]))
    return write(p, body)


PAGES += [leistungen, planung, montage, anschliessen, wartung]


# =====================================================================
# PRODUKTE
# =====================================================================
def produkte():
    groups = [('Module', 'Solarmodule von JA Solar, Typ JAM72S10 mit 405 W. Auf Kundenwunsch auch von anderen Herstellern.', [PRODUCTS[0]], 'module'),
              ('Befestigung', 'Schienen, Dachhaken, Trapezblechschuhe und Klemmen: das Gestell, das die Module hält. Abmaße, Belastbarkeit, Befestigungsmöglichkeiten.', [PRODUCTS[1]], 'befestigung'),
              ('Elektronik', 'Wechselrichter, Speichermöglichkeit und Messung: alles, was den Strom vom Dach ins Haus bringt.', PRODUCTS[2:], 'elektronik')]
    sec = ''
    for i, (t, d, items, idd) in enumerate(groups):
        li = ''.join(f'<li class="reveal"><a href="{a}"><span class="pl-img">{pic(ph_, "", "(max-width: 700px) 40vw, 200px")}</span><span class="pl-t">{tt}</span><span class="pl-d">{dd}</span>{ARROW}</a></li>' for a, tt, dd, ph_ in items)
        sec += f'<section class="sec{" grey" if i == 1 else ""}" id="{idd}"><div class="wrap two"><div class="sec-head"><p class="kicker">{t}</p><h2 class="split">{t}</h2><p class="reveal">{d}</p></div><ul class="plist">{li}</ul></div></section>'
    body = ph('Produkte', 'Wir verbauen ausschließlich Produkte von namhaften Herstellern und deren Qualitätsprodukte. Hier finden Sie, was in unseren Anlagen steckt, mit den technischen Daten.', 'Modul · Gestell · Elektronik', 'flachdach-hof', 'Zwei Modulreihen auf einem Flachdach', 'Produkte') + sec + cta('Fragen zu einem Produkt?', 'Wir erklären Ihnen gern, warum wir welches Teil verbauen und was es für Ihre Anlage bedeutet.')
    p = dict(file='produkte.html', title='Produkte: Module, Befestigung, Elektronik | Solar Technik BwM',
             desc='Was in unseren Photovoltaikanlagen steckt: JA-Solar-Module, Montagesystem aus Aluminium und Edelstahl, Huawei-Wechselrichter, Speicher, Energiezähler.',
             ld=ld_crumbs([('', 'Start'), ('produkte.html', 'Produkte')]))
    return write(p, body)


def module():
    rows = [('Typ', 'JA Solar JAM72S10-405/PR/1500V'), ('Zellen', 'Mono, 144 Halbzellen (6 × 24)'), ('Nennleistung (Pmax)', '405 W, Toleranz 0 bis +5 W'), ('Modulwirkungsgrad', '20,2 %'),
            ('Leerlaufspannung (Voc)', '49,81 V'), ('Spannung im MPP (Vmp)', '41,46 V'), ('Kurzschlussstrom (Isc)', '10,32 A'), ('Strom im MPP (Imp)', '9,77 A'),
            ('Temperaturkoeffizient Pmax', '−0,350 % pro °C'), ('Nennbetriebstemperatur (NOCT)', '45 ± 2 °C'), ('Maße', '2015 × 996 × 40 mm'), ('Gewicht', '22,7 kg'),
            ('Maximale Systemspannung', '1000 V DC'), ('Statische Last, Vorderseite', '3600 Pa'), ('Statische Last, Rückseite', '1600 Pa'), ('Betriebstemperatur', '−40 °C bis +85 °C')]
    temps = [(25, '25 °C'), (45, '45 °C'), (60, '60 °C'), (70, '70 °C')]
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Hitze-Rechner', 'Die 405 W gelten bei 25 °C Zelltemperatur. Im Sommer werden Module auf dem Dach deutlich heißer. Wählen Sie eine Temperatur und sehen Sie, was davon übrig bleibt.')}
  <div class="tool card" data-tool="heat">
    <div class="tq"><p class="tl-l">Zelltemperatur</p>{chips('t', temps, 2, 'Zelltemperatur')}<label class="own">oder eigene: <span class="unit sm"><input inputmode="numeric" data-in="t" aria-label="Eigene Zelltemperatur in Grad Celsius" placeholder="z. B. 55"><i>°C</i></span></label></div>
    <div class="heat-out" aria-live="polite"><div class="ho-bar"><i></i><span class="ho-ref">405 W bei 25 °C</span></div><p class="ho-big"><b data-o="w">–</b> W</p><p class="ho-eq" data-o="eq"></p></div>
    <p class="note">Rechnung nach dem Temperaturkoeffizienten aus dem Datenblatt (−0,350 % pro °C über 25 °C). Richtwert für ein Modul unter voller Einstrahlung, ohne Wechselrichter- und Kabelverluste.</p>
  </div>
</div></section>'''
    body = ph('Module', 'Wir verbauen Solarmodule von JA Solar, Typ JAM72S10 mit 405 W. Auf Kundenwunsch liefern wir auch Module anderer Hersteller.', '2015 × 996 mm', 'flachdach-hof', 'Zwei Modulreihen auf einem Flachdach', '<a href="produkte.html">Produkte</a> / Module') + f'''
<section class="sec"><div class="wrap two">
  <div class="sec-head"><p class="kicker">Technische Daten</p><h2 class="split">JA Solar JAM72S10, 405 W.</h2><p class="reveal">Angaben aus dem Datenblatt des Herstellers bei Standard-Testbedingungen (1000 W/m², 25 °C Zelltemperatur).</p>
    <a class="dsheet reveal" href="img/p-datenblatt-l.webp" target="_blank" rel="noopener">{pic('p-datenblatt', 'Datenblatt JA Solar JAM72S10, Seite 2', '220px')}<span>Datenblatt ansehen {ARROW}</span></a></div>
  {spec(rows)}
</div></section>
{tool}
''' + more('module.html', PRODUCTS, 'Weitere Produkte') + cta('Lieber ein anderes Modul?', 'Sagen Sie uns, welchen Hersteller Sie sich wünschen. Wir liefern auch nach Kundenwunsch.')
    p = dict(file='module.html', parent='produkte.html', title='Solarmodule JA Solar JAM72S10 405 W | Solar Technik BwM',
             desc='Technische Daten der JA-Solar-Module JAM72S10 mit 405 W, dazu ein Hitze-Rechner: Wie viel Leistung bleibt bei 60 °C auf dem Dach?',
             ld=ld_crumbs([('', 'Start'), ('produkte.html', 'Produkte'), ('module.html', 'Module')]))
    return write(p, body)


def befestigung():
    parts = [('schiene', 'Montageschiene', 'schiene', 'Solarmontageschiene aus Aluminium', [('Material', 'Aluminium'), ('Maße', '40 × 40 × 6000 mm'), ('Befestigung', 'M8 oder M10')]),
             ('dachhaken', 'Dachhaken', 'dachhaken', 'Dachhaken aus Edelstahl auf Montageschienen', [('Material', 'Edelstahl 1.4016'), ('Grundplatte', '140 × 56 mm'), ('Haken', '30 × 5 mm'), ('Verstellung', 'dreifach verstellbar'), ('Für', 'Standardpfannen')]),
             ('trapezblechschuh', 'Trapezblechschuh', None, '', [('Material', 'Edelstahl'), ('Verstellung', 'verstellbar'), ('Dichtung', 'eingeklebtes EPDM-Gummi'), ('Für', 'die meisten Trapezbleche')]),
             ('klemmen', 'End- und Mittelklemme', 'mittelklemme', 'Schwarze Mittelklemme auf einer Aluminiumschiene', [('Material', 'Aluminium, schwarz eloxiert'), ('Endklemme', 'für 30 mm Modulrahmen, Klemmbreite 70 mm'), ('Mittelklemme', '70 mm breit, Modulabstand 2 cm'), ('Klemmlänge', '70 mm')])]
    sec = ''
    for i, (idd, t, ph_, alt, rows) in enumerate(parts):
        img = f'<div class="part-img">{pic(ph_, alt, "(max-width: 900px) 80vw, 30vw")}</div>' if ph_ else f'<div class="part-img drawn"><svg viewBox="0 0 200 160" aria-hidden="true"><path class="tb-sheet" d="M0 120h30l15-30h30l15 30h20l15-30h30l15 30h30"/><path class="tb-shoe" d="M42 88h36v-40h-36zM48 48v-12h24v12"/><path class="tb-gum" d="M42 92h36"/></svg><span>Schematische Zeichnung</span></div>'
        extra = f'<div class="part-img second">{pic("endklemme", "Schwarze Endklemme an einer Schiene", "(max-width: 900px) 40vw, 15vw")}</div>' if idd == 'klemmen' else ''
        sec += f'<article class="part reveal{" flip" if i % 2 else ""}" id="{idd}">{img}{extra}<div class="part-t"><h2>{t}</h2>{spec(rows)}</div></article>'
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Stückliste', 'Wie viele Module liegen in einer Reihe, wie viele Reihen gibt es? Die Stückliste rechnet Schienen und Klemmen für JA-Solar-Module aus.')}
  <div class="tool card" data-tool="bom">
    <div class="bom-in"><label class="fld"><span>Module pro Reihe</span><input type="number" min="1" max="30" value="8" data-in="n"></label><label class="fld"><span>Reihen</span><input type="number" min="1" max="10" value="2" data-in="r"></label>
      <div class="tq"><p class="tl-l">Lage der Module</p>{chips('o', [('hoch', 'hochkant'), ('quer', 'quer')], 0, 'Lage der Module')}</div></div>
    <svg class="bom-svg" viewBox="0 0 600 220" aria-hidden="true"></svg>
    <dl class="bom-out" aria-live="polite"></dl>
    <p class="note">Richtwert: je Reihe zwei Schienen, 5 cm Überstand an jedem Ende, 2 cm Modulabstand, Schienenstücke zu 6 m. Die Zahl der Dachhaken legen wir nach Sparrenabstand, Schnee- und Windlast fest.</p>
  </div>
</div></section>'''
    body = ph('Befestigung', 'Das Gestell sieht man später kaum, aber es trägt die Anlage über viele Jahre. Wir verbauen Schienen aus Aluminium, Haken aus Edelstahl und schwarz eloxierte Klemmen.', '40 × 40 × 6000 mm', 'schiene', 'Querschnitt einer Montageschiene aus Aluminium', '<a href="produkte.html">Produkte</a> / Befestigung') + \
        f'<section class="sec"><div class="wrap parts">{sec}</div></section>' + tool + more('befestigung.html', PRODUCTS, 'Weitere Produkte') + cta('Welches Gestell braucht Ihr Dach?', 'Schicken Sie uns ein Foto der Dacheindeckung. Wir sagen Ihnen, was passt.')
    p = dict(file='befestigung.html', parent='produkte.html', title='PV-Befestigung: Schiene, Dachhaken, Klemmen | Solar BwM',
             desc='Montageschiene 40 × 40 mm, Dachhaken aus Edelstahl, Trapezblechschuh, End- und Mittelklemme. Mit Stückliste für Schienen und Klemmen.',
             ld=ld_crumbs([('', 'Start'), ('produkte.html', 'Produkte'), ('befestigung.html', 'Befestigung')]))
    return write(p, body)


INVERTERS = [  # Typ, DC max kW, AC kW, AC max kW, DC-Strom, DC-Spannung, Wirkungsgrad EU, Maße, Gewicht, Garantie
    ('SUN2000-3KTL-L1', 4.5, '3,0', '3,3', '25,0 A', '360 V (max. 600 V)', '97,3 %', '365 × 365 × 156 mm', '12 kg', '10 Jahre'),
    ('SUN2000-3.68KTL-L1', 4.2, '3,68', '4,0', '11,5 A', '360 V (max. 600 V)', '97,0 %', '390 × 300 × 140 mm', '9,5 kg', '10 Jahre'),
    ('SUN2000-4KTL-L1', 5.0, '4,0', '4,4', '25,0 A', '500 V (max. 600 V)', '97,5 %', '455 × 455 × 205 mm', '16,2 kg', '5 Jahre'),
]


def wechselrichter():
    head_ = ''.join(f'<th scope="col">{x[0]}</th>' for x in INVERTERS)
    lab = ['DC-Leistung (max.)', 'AC-Leistung', 'AC-Leistung (max.)', 'DC-Strom', 'DC-Spannung', 'MPP-Tracker / Stringeingänge', 'Wirkungsgrad (EU)', 'Maße', 'Gewicht', 'Herstellergarantie']
    vals = [[f'{str(x[1]).replace(".", ",")} kW' for x in INVERTERS], [x[2] + ' kW' for x in INVERTERS], [x[3] + ' kW' for x in INVERTERS], [x[4] for x in INVERTERS], [x[5] for x in INVERTERS],
            ['2 / 2'] * 3, [x[6] for x in INVERTERS], [x[7] for x in INVERTERS], [x[8] for x in INVERTERS], [x[9] for x in INVERTERS]]
    trs = ''.join(f'<tr><th scope="row">{l}</th>{"".join(f"<td>{v}</td>" for v in vs)}</tr>' for l, vs in zip(lab, vals))
    data = json.dumps([dict(t=x[0], dc=x[1], ac=x[2]) for x in INVERTERS])
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Wechselrichter-Finder', 'Wie viele Module sollen aufs Dach? Der Finder rechnet die Modulleistung zusammen und zeigt, welcher unserer einphasigen Wechselrichter dafür ausgelegt ist.')}
  <div class="tool card" data-tool="inv">
    <div class="tq"><label class="tl-l" for="inv-n">Anzahl Module (je 405 W)</label><div class="stepper"><button type="button" data-step="-1" aria-label="Ein Modul weniger">−</button><input id="inv-n" type="number" min="1" max="40" value="10" data-in="n"><button type="button" data-step="1" aria-label="Ein Modul mehr">+</button></div></div>
    <p class="inv-sum" aria-live="polite"></p>
    <ul class="inv-list"></ul>
    <p class="note">Richtwert nach der maximalen DC-Leistung laut Hersteller. Die Aufteilung auf die Stränge und die Spannung an kalten Tagen prüfen wir bei der Planung.</p>
    <script type="application/json" class="inv-data">{data}</script>
  </div>
</div></section>'''
    body = ph('Wechselrichter', 'Der Wechselrichter macht aus dem Gleichstrom der Module Wechselstrom für Ihr Haus. Wir verbauen einphasige Geräte der Serie Huawei SUN2000-L1 mit zwei MPP-Trackern.', '3 bis 4 kW', 'blechdach-weit', 'Photovoltaikanlage auf einem Blechdach', '<a href="produkte.html">Produkte</a> / Wechselrichter') + f'''
<section class="sec"><div class="wrap">
  <div class="inv-top"><div class="sec-head"><p class="kicker">Technische Daten</p><h2 class="split">Drei Größen, eine Serie.</h2><p class="reveal">Alle drei sind einphasige Wechselrichter mit zwei MPP-Trackern und zwei Stringeingängen. Angaben laut Hersteller.</p></div><div class="inv-img reveal">{pic('p-wechselrichter', 'Wechselrichter Huawei SUN2000-L1', '220px')}</div></div>
  <div class="tbl-wrap reveal" tabindex="0" role="region" aria-label="Technische Daten der Wechselrichter, seitlich scrollbar"><table class="tbl"><thead><tr><th scope="col">Kategorie</th>{head_}</tr></thead><tbody>{trs}</tbody></table></div>
</div></section>
{tool}
''' + more('wechselrichter.html', PRODUCTS, 'Weitere Produkte') + cta('Größere Anlage geplant?', 'Für mehr als zwölf Module oder dreiphasigen Anschluss planen wir passende Geräte. Sprechen Sie uns an.')
    p = dict(file='wechselrichter.html', parent='produkte.html', title='Wechselrichter Huawei SUN2000-L1 | Solar Technik BwM',
             desc='Technische Daten der Huawei-Wechselrichter SUN2000-3KTL, -3.68KTL und -4KTL-L1. Mit Finder: Welches Gerät passt zu Ihrer Modulzahl?',
             ld=ld_crumbs([('', 'Start'), ('produkte.html', 'Produkte'), ('wechselrichter.html', 'Wechselrichter')]))
    return write(p, body)


def speicher():
    bms = [('Typ', 'Huawei LUNA2000-5KW-C0 (Leistungsmodul mit Batteriemanagement)'), ('Nennleistung', '5 kW'), ('Nennspannung', '48 V'), ('Max. Ladestrom', '100 A'), ('Max. Entladestrom', '100 A'), ('Batterietyp', 'Lithium-Ionen'), ('Maße (L × B × H)', '415 × 330 × 130 mm'), ('Garantie', '2 Jahre')]
    inv = [('Nennleistung', '5 kW'), ('Max. DC-Spannung', '1000 V'), ('MPP-Tracker', '2'), ('Max. DC-Strom', '11 A'), ('AC-Nennleistung', '5 kW'), ('AC-Spannungsbereich', '184–276 V'), ('AC-Frequenz', '50 / 60 Hz'), ('Max. Wirkungsgrad', '98,0 %'), ('Euro-Wirkungsgrad', '97,3 %'), ('Maße (B × H × T)', '330 × 607 × 155 mm'), ('Gewicht', '15,9 kg'), ('Garantie', '5 Jahre')]
    tool = f'''<section class="sec tool-sec" id="werkzeug"><div class="wrap tool-grid">
  {tool_head('Nacht-Rechner', 'Wie lange reicht ein voller Speicher, wenn die Sonne weg ist? Wählen Sie die Speichergröße und wie viel Ihr Haus abends und nachts ungefähr braucht.')}
  <div class="tool card" data-tool="night">
    <div class="tq"><p class="tl-l">Speichergröße</p>{chips('cap', [(5, '5 kWh'), (10, '10 kWh'), (15, '15 kWh')], 1, 'Speichergröße')}</div>
    <div class="tq"><p class="tl-l">Verbrauch nach Sonnenuntergang</p>{chips('w', [(250, 'sparsam, 250 W'), (500, 'normal, 500 W'), (900, 'viel, 900 W')], 1, 'Verbrauch')}<label class="own">oder eigener Wert: <span class="unit sm"><input inputmode="numeric" data-in="w" aria-label="Eigener Verbrauch in Watt" placeholder="z. B. 400"><i>W</i></span></label></div>
    <div class="night-out" aria-live="polite"><svg class="night-svg" viewBox="0 0 600 90" aria-hidden="true"><path class="nx" d="M10 60H590"/><rect class="nb" x="10" y="44" width="0" height="32" rx="4"/><g class="nt"></g></svg><p class="no-big"><b data-o="h">–</b> Stunden</p><p class="no-t" data-o="t"></p></div>
    <p class="note">Rechnerisch bei voll geladenem Speicher und gleichmäßigem Verbrauch, ohne Umwandlungsverluste. Die Speichergrößen sind Beispiele; welche Kapazität zu Ihnen passt, klären wir bei der Planung.</p>
  </div>
</div></section>'''
    body = ph('Batteriespeicher', 'Tagsüber liefert die Anlage oft mehr, als Sie brauchen. Ein Speicher hebt den Überschuss für den Abend auf. Wir verbauen Speicher der Serie Huawei LUNA2000.', '5 kW', 'backsteinhaus', 'Backsteinhaus mit Photovoltaik auf dem Satteldach', '<a href="produkte.html">Produkte</a> / Batteriespeicher') + f'''
<section class="sec"><div class="wrap two">
  <div class="sec-head"><p class="kicker">Batterie-Steuereinheit</p><h2 class="split">LUNA2000-5KW-C0.</h2><p class="reveal">Das Leistungsmodul mit Batteriemanagement sitzt oben auf den Batteriemodulen und steuert Laden und Entladen.</p><div class="prod-img reveal">{pic('p-bms', 'Huawei LUNA2000 Leistungsmodul', '355px')}{pic('p-speicher', 'Huawei LUNA2000 Batteriemodul', '355px')}</div></div>
  {spec(bms)}
</div></section>
<section class="sec grey"><div class="wrap two">
  <div class="sec-head"><p class="kicker">Für den Speicherbetrieb</p><h2 class="split">Wechselrichter mit 5 kW.</h2><p class="reveal">Für Anlagen mit Speicher setzen wir einen Wechselrichter mit 5 kW Nennleistung und hohem Wirkungsgrad ein.</p></div>
  {spec(inv)}
</div></section>
{tool}
''' + more('speicher.html', PRODUCTS, 'Weitere Produkte') + cta('Speicher nachrüsten?', 'Ob Ihr vorhandener Wechselrichter einen Speicher aufnehmen kann, prüfen wir gern für Sie.', 'Speicher anfragen', 'kontakt.html?thema=speicher')
    p = dict(file='speicher.html', parent='produkte.html', title='Batteriespeicher Huawei LUNA2000 | Solar Technik BwM',
             desc='Batteriespeicher Huawei LUNA2000 mit Steuereinheit LUNA2000-5KW-C0: technische Daten und Nacht-Rechner, wie lange ein voller Speicher reicht.',
             ld=ld_crumbs([('', 'Start'), ('produkte.html', 'Produkte'), ('speicher.html', 'Batteriespeicher')]))
    return write(p, body)


def energiezaehler():
    rows = [('Typ', 'Huawei Smart Power Sensor DTSU666-H 250A/50mA'), ('Nennstrom', '250 A'), ('Max. zulässiger Strom', '300 A'), ('Genauigkeitsklasse', '0,5S'), ('Nennspannung', '50 V AC/DC'),
            ('Ansprechzeit', '≤ 0,5 s'), ('Auflösung', '16 Bit'), ('Abtastzeit', '≤ 10 s'), ('Garantie', '2 Jahre')]
    uses = [('Einspeisung begrenzen', 'Wenn der Netzbetreiber nur eine bestimmte Einspeiseleistung erlaubt, regelt der Wechselrichter danach.'),
            ('Speicher richtig laden', 'Der Speicher lädt nur mit dem, was wirklich übrig ist, und entlädt, wenn das Haus Strom aus dem Netz ziehen würde.'),
            ('Verbrauch sehen', 'In der App sehen Sie nicht nur, was die Anlage erzeugt, sondern auch, was Ihr Haus verbraucht.')]
    us = ''.join(f'<li class="reveal"><h3>{a}</h3><p>{b}</p></li>' for a, b in uses)
    body = ph('Energiezähler', 'Der Smart Power Sensor sitzt am Netzanschlusspunkt im Zählerschrank. Er misst, wie viel Strom Ihr Haus aus dem Netz bezieht und wie viel es einspeist.', '0,5S', 'flachdach-ballast', 'Modulgestell mit Betonsteinen auf einem Flachdach', '<a href="produkte.html">Produkte</a> / Energiezähler') + f'''
<section class="sec"><div class="wrap two">
  <div class="sec-head"><p class="kicker">Technische Daten</p><h2 class="split">DTSU666-H.</h2><p class="reveal">Ein Präzisions-Stromsensor für Ströme bis 250 A in Genauigkeitsklasse 0,5S. Angaben laut Hersteller.</p><div class="prod-img reveal">{pic('p-sensor', 'Huawei Smart Power Sensor DTSU666-H', '160px')}</div></div>
  {spec(rows)}
</div></section>
<section class="sec grey"><div class="wrap two"><div class="sec-head sticky-h"><p class="kicker">Wozu</p><h2 class="split">Warum eine Anlage messen muss.</h2></div><ol class="looks">{us}</ol></div></section>
''' + more('energiezaehler.html', PRODUCTS, 'Weitere Produkte') + cta('Zähler nachrüsten?', 'Auch in bestehende Anlagen bauen wir den Smart Power Sensor ein, etwa wenn ein Speicher dazukommt.', 'Anfrage senden', 'kontakt.html?thema=anschliessen')
    p = dict(file='energiezaehler.html', parent='produkte.html', title='Energiezähler Smart Power Sensor DTSU666-H | Solar BwM',
             desc='Der Smart Power Sensor DTSU666-H misst Netzbezug und Einspeisung am Hausanschluss, damit Wechselrichter und Speicher richtig regeln.',
             ld=ld_crumbs([('', 'Start'), ('produkte.html', 'Produkte'), ('energiezaehler.html', 'Energiezähler')]))
    return write(p, body)


PAGES += [produkte, module, befestigung, wechselrichter, speicher, energiezaehler]


# =====================================================================
# REFERENZEN, ÜBER UNS
# =====================================================================
REFS = [
    ('Flachdach in der Stadt', 'Dezember 2022', 'Aufgeständerte Modulreihen zwischen Stadthäusern, das Gestell mit Betonsteinen beschwert.', ['flachdach-stadt', 'flachdach-reihen', 'flachdach-ballast', 'flachdach-hof']),
    ('Satteldächer', 'Dezember 2022', 'Module auf einem Bruchsteinhaus, einem Backsteinhaus und einem dunklen Ziegeldach, befestigt mit Dachhaken.', ['bruchsteinhaus', 'backsteinhaus', 'ziegeldach']),
    ('Blechdach auf dem Land', 'August 2022', 'Module auf Trapezblech, befestigt mit Trapezblechschuhen.', ['blechdach', 'blechdach-weit']),
    ('Montagematerial', 'Dezember 2022', 'Schiene, Dachhaken, Mittel- und Endklemme, bevor sie aufs Dach gehen.', ['schiene', 'dachhaken', 'mittelklemme', 'endklemme']),
]


def referenzen():
    sec = ''
    k = 0
    for t, d, txt, photos in REFS:
        li = ''
        for n in photos:
            li += f'<li><button type="button" class="lb-open" data-k="{k}" data-full="img/{n}-l.webp" aria-label="Foto vergrößern: {t}">{pic(n, t + ", " + d, "(max-width: 700px) 50vw, 25vw")}</button></li>'
            k += 1
        sec += f'<article class="proj reveal"><div class="proj-h"><h2>{t}</h2><p class="proj-d">{d}</p><p>{txt}</p></div><ul class="proj-g g{len(photos)}">{li}</ul></article>'
    body = ph('Referenzen', 'Ein paar Dächer, auf denen unsere Anlagen stehen: Flachdach, Satteldach, Blechdach. Alle Fotos stammen von unseren Baustellen.', 'Flach · Sattel · Blech', 'flachdach-stadt', 'Modulreihen auf einem Flachdach in der Stadt', 'Referenzen') + \
        f'<section class="sec"><div class="wrap projs">{sec}</div></section>' + \
        '<div class="lb" role="dialog" aria-modal="true" aria-label="Fotoansicht" hidden><button class="lb-x" type="button" aria-label="Schließen">×</button><button class="lb-p" type="button" aria-label="Vorheriges Foto">‹</button><figure><img alt=""><figcaption></figcaption></figure><button class="lb-n" type="button" aria-label="Nächstes Foto">›</button></div>' + \
        cta('Ihr Dach als nächste Referenz?', 'Schicken Sie uns ein Foto Ihres Daches und Ihren Stromverbrauch. Wir melden uns.')
    p = dict(file='referenzen.html', title='Referenzen: PV auf Flach-, Sattel- und Blechdach | Solar BwM',
             desc='Fotos von Photovoltaikanlagen von Solar Technik BwM: Flachdach in der Stadt, Satteldächer, Blechdach auf dem Land und unser Montagematerial.',
             ld=ld_crumbs([('', 'Start'), ('referenzen.html', 'Referenzen')]))
    return write(p, body)


def ueber_uns():
    facts = [('Inhaber', CO['person']), ('Sitz', f'{CO["street"]}, B-{CO["zip"]} {CO["city"]}, {CO["country"]}'), ('Region', 'Raum Aachen, Ostbelgien, Südlimburg'), ('USt-ID', CO['vat'])]
    fx = ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in facts)
    body = ph('Über uns', 'Solar Technik BwM ist ein Photovoltaik-Fachbetrieb aus Lontzen in Ostbelgien. Wir planen und installieren Anlagen für Kunden in Deutschland, Belgien und den Niederlanden.', 'Lontzen · Aachen · Maastricht', 'bruchsteinhaus', 'Bruchsteinhaus mit Photovoltaikanlage', 'Über uns') + f'''
<section class="sec"><div class="wrap two">
  <div class="sec-head"><p class="kicker">Wer wir sind</p><h2 class="split">Spezialisiert auf Photovoltaik.</h2></div>
  <div class="prose reveal"><p>Wir haben uns auf die Planung und Installation von hochwertigen Photovoltaikanlagen im Raum Aachen spezialisiert. Um Ihnen ein hohes Maß an Investitionssicherheit für viele Jahre bieten zu können, arbeiten wir ausschließlich mit namhaften Herstellern und deren Qualitätsprodukten.</p>
  <p>Für Ihren Traum von einer Solaranlage stehen Ihnen alle Wünsche der Anbringung offen, ob auf Flachdach, Satteldach, Pultdach oder Freifläche. Unser Kundenkreis liegt im Dreiländereck Deutschland, Belgien und Niederlande.</p>
  <p>Von der Beratung über die Montage bis zum Anschluss und zur Wartung kommt alles aus einer Hand. Ansprechpartner ist Inhaber {CO['person']}.</p>
  <dl class="facts">{fx}</dl></div>
</div></section>
<section class="sec grey"><div class="wrap"><div class="sec-head"><p class="kicker">Worauf wir Wert legen</p><h2 class="split">Material, das man kennt.</h2></div>
  <div class="values">
    <div class="val reveal">{pic('dachhaken', 'Dachhaken aus Edelstahl', '(max-width: 900px) 45vw, 22vw')}<h3>Namhafte Hersteller</h3><p>Module von JA Solar, Wechselrichter und Speicher von Huawei, Gestell aus Aluminium und Edelstahl.</p></div>
    <div class="val reveal">{pic('flachdach-ballast', 'Modulgestell mit Ballast auf einem Flachdach', '(max-width: 900px) 45vw, 22vw')}<h3>Jede Dachform</h3><p>Flachdach, Satteldach, Pultdach, Blechdach oder Wiese: Wir wählen die Befestigung nach dem Dach.</p></div>
    <div class="val reveal">{pic('kran', 'Kran-LKW auf einem Hof', '(max-width: 900px) 45vw, 22vw')}<h3>Aus einer Hand</h3><p>Planung, Montage, Anschluss und Wartung ohne Übergabe an andere Firmen.</p></div>
  </div></div></section>
''' + cta('Sprechen wir über Ihr Dach.', f'Rufen Sie {CO["person"]} direkt an oder schreiben Sie uns.')
    p = dict(file='ueber-uns.html', title='Über uns: PV-Fachbetrieb aus Lontzen | Solar Technik BwM',
             desc='Solar Technik BwM, Inhaber Malte Behrenswerth, plant und installiert Photovoltaikanlagen im Dreiländereck Deutschland, Belgien, Niederlande.',
             ld=ld_crumbs([('', 'Start'), ('ueber-uns.html', 'Über uns')]))
    return write(p, body)


# =====================================================================
# RATGEBER
# =====================================================================
ARTICLES = [
    ('ratgeber-dachformen.html', 'Welche Befestigung passt zu welchem Dach?', 'Flachdach, Satteldach, Pultdach, Blechdach und Wiese: womit Photovoltaik jeweils befestigt wird und worauf es ankommt.', 'flachdach-ballast', '5 Minuten', [
        ('Das Gestell entscheidet', '<p>Die Module sehen auf jedem Dach ähnlich aus. Was sich unterscheidet, ist das Gestell darunter. Es muss die Module über viele Jahre gegen Wind und Schnee halten, ohne das Dach zu beschädigen. Deshalb fragen wir immer zuerst: Womit ist Ihr Dach gedeckt?</p>'),
        ('Satteldach und Pultdach mit Pfannen', '<p>Auf Tonziegeln und Betondachsteinen setzen wir <a href="befestigung.html#dachhaken">Dachhaken aus Edelstahl</a>. Der Haken wird auf den Sparren geschraubt und läuft unter der Pfanne hindurch nach außen. Unsere Haken sind dreifach verstellbar, damit die Schiene auch auf einer unebenen Dachfläche gerade liegt. Auf die Haken kommen die <a href="befestigung.html#schiene">Montageschienen</a>, auf die Schienen die Module.</p><p>Ob Satteldach oder Pultdach, spielt für die Befestigung kaum eine Rolle. Wichtig sind Neigung und Ausrichtung, denn sie bestimmen, wie viel Sonne die Module abbekommen.</p>'),
        ('Trapezblech', '<p>Auf Blechdächern wäre ein Haken unter der Pfanne nicht möglich. Hier sitzt ein <a href="befestigung.html#trapezblechschuh">Trapezblechschuh</a> auf der Hochsicke des Blechs. Ein eingeklebtes EPDM-Gummi dichtet die Stelle ab. Die Schuhe sind verstellbar und passen auf die meisten Trapezbleche.</p>'),
        ('Flachdach', '<p>Auf dem Flachdach werden die Module in Reihen aufgeständert, also schräg gestellt. Das Gestell wird mit Betonsteinen beschwert. Wie viel Ballast nötig ist, hängt von Gebäudehöhe, Lage und Windlast ab. Den Abstand zwischen den Reihen planen wir so, dass sich die Reihen möglichst nicht gegenseitig verschatten.</p>'),
        ('Freifläche', '<p>Auf einer Wiese stehen die Module auf einem Gestell am Boden. Neigung und Ausrichtung lassen sich hier frei wählen, weil kein Dach sie vorgibt.</p>'),
        ('Was Sie vorab tun können', '<p>Machen Sie ein Foto der Dacheindeckung aus der Nähe und eines vom ganzen Dach. Damit können wir schon vor dem ersten Termin einschätzen, welches Gestell passt. Im <a href="montage.html#werkzeug">Werkzeug „Befestigung nach Eindeckung“</a> sehen Sie die Varianten nebeneinander.</p>')]),
    ('ratgeber-hitze.html', 'Warum Solarmodule im Hochsommer weniger leisten', 'Mehr Sonne heißt nicht automatisch mehr Strom: Was der Temperaturkoeffizient im Datenblatt bedeutet, am Beispiel unserer 405-W-Module.', 'blechdach', '4 Minuten', [
        ('Die 405 W gelten bei 25 °C', '<p>Auf jedem Modul steht eine Nennleistung, bei unseren <a href="module.html">JA-Solar-Modulen</a> 405 W. Gemessen wird sie unter Standard-Testbedingungen: 1000 W Einstrahlung pro Quadratmeter und 25 °C Zelltemperatur. Auf einem Dach im Juli sind die Zellen aber deutlich wärmer als 25 °C.</p>'),
        ('Was der Temperaturkoeffizient sagt', '<p>Im Datenblatt steht für die Leistung ein Temperaturkoeffizient von −0,350 % pro °C. Das heißt: Für jedes Grad über 25 °C sinkt die Leistung um 0,35 Prozent. Bei 60 °C Zelltemperatur sind das 35 Grad mehr, also 12,25 Prozent weniger. Aus 405 W werden rechnerisch rund 355 W.</p>'),
        ('Die Nennbetriebstemperatur', '<p>Das Datenblatt nennt außerdem eine Nennbetriebstemperatur (NOCT) von 45 °C. Sie gilt bei 800 W Einstrahlung, 20 °C Luft und leichtem Wind. Das ist ein guter Anhaltspunkt für einen normalen sonnigen Tag. An heißen, windstillen Tagen liegt die Zelltemperatur darüber.</p>'),
        ('Warum der Sommer trotzdem der beste Monat ist', '<p>Im Sommer scheint die Sonne länger und steht höher. Das gleicht den Hitzeverlust mehr als aus. Die besten Stunden sind oft klare, kühle Tage im Frühjahr mit viel Sonne und wenig Wärme.</p>'),
        ('Was hilft', '<p>Luft unter den Modulen kühlt. Deshalb achten wir bei der Montage darauf, dass die Module mit Abstand über dem Dach liegen und die Luft darunter zirkulieren kann. Probieren Sie es im <a href="module.html#werkzeug">Hitze-Rechner</a> selbst aus.</p>')]),
    ('ratgeber-anfrage.html', 'Was wir für ein Angebot von Ihnen brauchen', 'Stromverbrauch, Dach, Heizung, Warmwasser: welche Angaben eine Anfrage schnell machen und wo Sie sie finden.', 'backsteinhaus', '3 Minuten', [
        ('Der Stromverbrauch', '<p>Die wichtigste Zahl steht auf Ihrer letzten Jahresabrechnung: der Verbrauch in Kilowattstunden (kWh) pro Jahr. Daraus leiten wir ab, wie groß die Anlage sein sollte und ob sich ein Speicher lohnt.</p>'),
        ('Das Dach', '<p>Dachform, Eindeckung und ungefähre Größe. Am einfachsten sind zwei, drei Fotos: eines vom ganzen Dach, eines von der Eindeckung aus der Nähe und, wenn möglich, eines vom Dachboden mit Sparren. Stehen Bäume, Kamine oder Gauben im Weg, gehören sie mit aufs Foto.</p>'),
        ('Heizung und Warmwasser', '<p>Wird mit Gas, Öl, Wärmepumpe oder Strom geheizt? Kommt das Warmwasser aus der Heizung oder aus einem elektrischen Boiler? Das zeigt, wohin Solarstrom im Haus fließen kann, heute oder nach einem späteren Umbau.</p>'),
        ('Pläne für die nächsten Jahre', '<p>Ein E-Auto, eine Wärmepumpe oder ein Speicher, der später dazukommt, verändern die Auslegung. Wenn wir es vorher wissen, planen wir Wechselrichter und Leitungen gleich passend.</p>'),
        ('Der Zählerschrank', '<p>Ein Foto vom geöffneten Zählerschrank hilft uns, den Anschluss einzuschätzen: Wo passen Energiezähler und Sicherungen hin?</p>'),
        ('So geht es am schnellsten', '<p>Klicken Sie sich durch den <a href="planung-beratung.html#werkzeug">Anfrage-Steckbrief</a>. Er übernimmt Ihre Angaben direkt in unser <a href="kontakt.html">Anfrageformular</a>. Die Fotos können Sie danach per E-Mail an <a href="mailto:' + CO['mail'] + '">' + CO['mail'] + '</a> schicken.</p>')]),
]


def ratgeber():
    li = ''.join(f'<li class="reveal"><a href="{a}"><span class="rg-img">{pic(ph_, "", "(max-width: 900px) 100vw, 30vw")}</span><span class="rg-m">Ratgeber · {mins}</span><span class="rg-t">{t}</span><span class="rg-d">{d}</span><span class="rg-go">Lesen {ARROW}</span></a></li>' for a, t, d, ph_, mins, parts in ARTICLES)
    body = ph('Ratgeber', 'Kurze Antworten auf Fragen, die uns bei der Planung oft gestellt werden: zu Dächern, Modulen und dem Weg zum Angebot.', 'Kurz erklärt', None, '', 'Ratgeber') + \
        f'<section class="sec"><div class="wrap"><ul class="rg-list">{li}</ul><p class="rg-faq reveal">Mehr kurze Antworten stehen bei den <a href="faq.html">häufigen Fragen</a>.</p></div></section>' + cta('Ihre Frage war nicht dabei?', 'Rufen Sie an oder schreiben Sie uns. Wir antworten persönlich.')
    p = dict(file='ratgeber.html', title='Ratgeber Photovoltaik: Dach, Module, Anfrage | Solar BwM',
             desc='Ratgeber von Solar Technik BwM: welche Befestigung zu welchem Dach passt, warum Module bei Hitze weniger leisten und was wir für ein Angebot brauchen.',
             ld=ld_crumbs([('', 'Start'), ('ratgeber.html', 'Ratgeber')]))
    return write(p, body)


def article(a):
    f, t, d, ph_, mins, parts = a
    toc = ''.join(f'<li><a href="#a{i}">{h}</a></li>' for i, (h, x) in enumerate(parts))
    txt = ''.join(f'<h2 id="a{i}">{h}</h2>{x}' for i, (h, x) in enumerate(parts))
    others = ''.join(f'<li><a href="{x[0]}">{x[1]} {ARROW}</a></li>' for x in ARTICLES if x[0] != f)
    body = ph(t, d, 'Ratgeber · ' + mins, ph_, t, '<a href="ratgeber.html">Ratgeber</a> / Artikel') + f'''
<section class="sec"><div class="wrap art">
  <aside class="art-toc"><p class="kicker">Inhalt</p><ol>{toc}</ol></aside>
  <article class="prose art-body">{txt}<p class="art-meta">Stand: September 2026 · Solar Technik BwM, {CO['city']}</p></article>
</div></section>
<section class="sec tight"><div class="wrap"><h2 class="h3">Weiterlesen</h2><ul class="art-more">{others}</ul></div></section>
''' + cta('Lieber persönlich besprechen?', 'Wir sehen uns Ihr Dach an und beantworten Ihre Fragen vor Ort.')
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d, "image": f"{DOMAIN}/img/{ph_}-l.webp", "datePublished": TODAY, "dateModified": TODAY,
           "author": {"@type": "Organization", "name": CO['name']}, "publisher": {"@type": "Organization", "name": CO['name'], "logo": {"@type": "ImageObject", "url": DOMAIN + "/apple-touch-icon.png"}}, "mainEntityOfPage": DOMAIN + "/" + f},
          ld_crumbs([('', 'Start'), ('ratgeber.html', 'Ratgeber'), (f, t)])]
    title = t if len(t) <= 44 else t[:44].rsplit(' ', 1)[0]
    p = dict(file=f, parent='ratgeber.html', article=True, title=f'{title} | Solar Technik BwM', desc=d, ld=ld)
    return write(p, body)


FAQ = [
    ('In welcher Region bauen Sie Photovoltaikanlagen?', 'Im Raum Aachen und im ganzen Dreiländereck: in Deutschland, in Ostbelgien und in Südlimburg in den Niederlanden. Unser Sitz ist in Lontzen.'),
    ('Auf welchen Dächern montieren Sie?', 'Auf Flachdach, Satteldach, Pultdach und Blechdach sowie auf Freiflächen. Die Befestigung richtet sich nach der Eindeckung: Dachhaken auf Pfannen, Trapezblechschuhe auf Blech, Aufständerung mit Ballast auf dem Flachdach.'),
    ('Welche Module verbauen Sie?', 'In der Regel Module von JA Solar, Typ JAM72S10 mit 405 W. Auf Wunsch liefern wir auch Module anderer Hersteller.'),
    ('Welche Wechselrichter und Speicher setzen Sie ein?', 'Einphasige Wechselrichter der Serie Huawei SUN2000-L1 mit 3, 3,68 oder 4 kW und Batteriespeicher der Serie Huawei LUNA2000 mit Steuereinheit.'),
    ('Kann ich einen Speicher später nachrüsten?', 'Oft ja. Ob Ihr vorhandener Wechselrichter einen Speicher aufnehmen kann, prüfen wir vorab. Wenn Sie einen Speicher schon planen, legen wir die Anlage von Anfang an darauf aus.'),
    ('Was brauchen Sie für ein Angebot?', 'Ihren Jahresstromverbrauch, die Dachform und Eindeckung, Heizungsart und Warmwasser. Fotos vom Dach und vom Zählerschrank helfen sehr. Der <a href="planung-beratung.html#werkzeug">Anfrage-Steckbrief</a> fragt alles ab.'),
    ('Was kostet eine Anlage?', 'Das hängt von Dach, Größe, Befestigung und Speicher ab. Einen Preis nennen wir nach einem Blick auf Ihr Dach, nicht pauschal vorab.'),
    ('Wofür ist der Energiezähler?', 'Der Smart Power Sensor misst am Hausanschluss, wie viel Strom Sie beziehen und einspeisen. Danach regeln Wechselrichter und Speicher, und Sie sehen Ihren Verbrauch in der App.'),
    ('Warten Sie auch Anlagen anderer Firmen?', 'Ja. Wir prüfen Befestigung, Module, Kabel, Wechselrichter und Ertrag, auch wenn wir die Anlage nicht selbst gebaut haben.'),
    ('Wie erreiche ich Sie?', f'Telefonisch unter <a href="tel:{CO["telh"]}">{CO["tel"]}</a>, per E-Mail an <a href="mailto:{CO["mail"]}">{CO["mail"]}</a> oder über das <a href="kontakt.html">Anfrageformular</a>.'),
]


def faq():
    body = ph('Häufige Fragen', 'Die kurzen Antworten auf das, was uns am häufigsten gefragt wird. Ausführlicher steht es im Ratgeber und auf den Seiten zu Leistungen und Produkten.', 'Zehn Antworten', None, '', 'Häufige Fragen') + \
        f'<section class="sec"><div class="wrap narrow">{faq_list(FAQ)}</div></section>' + cta('Noch eine Frage offen?', 'Rufen Sie an oder schreiben Sie uns.')
    p = dict(file='faq.html', title='Häufige Fragen zu Photovoltaik | Solar Technik BwM',
             desc='Antworten zu Region, Dachformen, Modulen, Wechselrichtern, Speichern, Kosten und Wartung von Photovoltaikanlagen bei Solar Technik BwM.',
             ld=[ld_faq(FAQ), ld_crumbs([('', 'Start'), ('faq.html', 'Häufige Fragen')])])
    return write(p, body)


# =====================================================================
# KONTAKT, DANKE, 404, RECHTLICHES
# =====================================================================
def kontakt():
    bbox = '5.9636,50.6900,6.0036,50.7100'
    body = ph('Kontakt', 'Erzählen Sie uns von Ihrem Dach. Mit Stromverbrauch, Heizung und Warmwasser können wir die Anlage schon grob auslegen, bevor wir vorbeikommen.', 'Lontzen · Raum Aachen', None, '', 'Kontakt') + f'''
<section class="sec"><div class="wrap k-grid">
  <div class="k-form"><div class="ask-sheet light"><span class="reg tl" aria-hidden="true"></span><span class="reg tr" aria-hidden="true"></span><span class="reg bl" aria-hidden="true"></span><span class="reg br" aria-hidden="true"></span>{form('k')}</div></div>
  <aside class="k-side">
    <div class="k-card reveal"><h2 class="h3">{CO['name']}</h2><ul class="ask-contact"><li>{TEL}<a href="tel:{CO['telh']}">{CO['tel']}</a></li><li>{MAIL}<a href="mailto:{CO['mail']}">{CO['mail']}</a></li><li>{PIN}<span>{CO['person']}<br>{CO['street']}<br>B-{CO['zip']} {CO['city']}, {CO['country']}</span></li></ul></div>
    <div class="k-map reveal" data-map="https://www.openstreetmap.org/export/embed.html?bbox={bbox}&amp;layer=mapnik&amp;marker={CO['lat']},{CO['lon']}">
      <button type="button" class="btn line">{PIN} Karte laden</button><p>Die Karte kommt von OpenStreetMap. Erst mit dem Klick wird eine Verbindung dorthin aufgebaut.</p>
    </div>
  </aside>
</div></section>'''
    p = dict(file='kontakt.html', title='Kontakt und Anfrage | Solar Technik BwM, Lontzen',
             desc='Photovoltaik anfragen bei Solar Technik BwM: Telefon +49 1575 5232254, info@solar-bwm.com, Schmalgraf 48, 4710 Lontzen. Mit Anfrageformular.',
             ld=ld_crumbs([('', 'Start'), ('kontakt.html', 'Kontakt')]))
    return write(p, body)


def danke():
    body = f'''<section class="bh no-photo solo"><div class="wrap"><div class="dimline" aria-hidden="true"><i class="dl-a"></i><span>Anfrage angekommen</span><i class="dl-b"></i></div><h1 class="split">Danke für Ihre Anfrage.</h1><p class="lead reveal">Wir melden uns so bald wie möglich. Wenn Sie Fotos von Dach oder Zählerschrank haben, schicken Sie sie gern an <a href="mailto:{CO['mail']}">{CO['mail']}</a>.</p><p class="reveal"><a class="btn cu mag" href="index.html">Zur Startseite {ARROW}</a> <a class="btn line" href="ratgeber-anfrage.html">Was wir noch brauchen</a></p></div></section>'''
    return write(dict(file='danke.html', title='Danke für Ihre Anfrage | Solar Technik BwM', desc='Ihre Anfrage an Solar Technik BwM ist angekommen.', noindex=True), body)


def notfound():
    li = ''.join(f'<li><a href="{a}">{t}</a></li>' for a, t in [('index.html', 'Startseite'), ('leistungen.html', 'Leistungen'), ('produkte.html', 'Produkte'), ('referenzen.html', 'Referenzen'), ('kontakt.html', 'Kontakt')])
    body = f'''<section class="bh no-photo solo"><div class="wrap"><div class="dimline" aria-hidden="true"><i class="dl-a"></i><span>Fehler 404</span><i class="dl-b"></i></div><h1 class="split">Diese Seite sitzt nicht auf der Schiene.</h1><p class="lead reveal">Die Adresse gibt es nicht (mehr). Vielleicht hilft einer dieser Wege weiter:</p><ul class="nf reveal">{li}</ul></div></section>'''
    return write(dict(file='404.html', title='Seite nicht gefunden | Solar Technik BwM', desc='Diese Seite gibt es nicht. Weiter zur Startseite von Solar Technik BwM.', noindex=True, body='quiet'), body)


def impressum():
    body = ph('Impressum', 'Angaben zum Anbieter dieser Website.', 'Anbieter', None, '', 'Impressum') + f'''
<section class="sec"><div class="wrap narrow prose legal">
<h2>Anbieter</h2><p>{CO['name']}<br>Inhaber: {CO['person']}<br>{CO['street']}<br>B-{CO['zip']} {CO['city']}<br>{CO['country']}</p>
<h2>Kontakt</h2><p>Telefon: <a href="tel:{CO['telh']}">{CO['tel']}</a><br>E-Mail: <a href="mailto:{CO['mail']}">{CO['mail']}</a></p>
<h2>Unternehmens- und Mehrwertsteuernummer</h2><p>{CO['vat']}</p>
<h2>Verantwortlich für den Inhalt</h2><p>{CO['person']}, Anschrift wie oben.</p>
<h2>Haftung für Inhalte und Links</h2><p>Wir erstellen die Inhalte dieser Seiten mit Sorgfalt, können für Richtigkeit, Vollständigkeit und Aktualität aber keine Gewähr übernehmen. Die Werkzeuge auf dieser Website liefern Richtwerte und ersetzen keine Planung. Für Inhalte verlinkter fremder Seiten sind deren Betreiber verantwortlich.</p>
<h2>Bildnachweis</h2><p>Fotos: {CO['name']}. Produktabbildungen und Datenblatt: Huawei Technologies und JA Solar.</p>
<h2>Streitschlichtung</h2><p>Wir sind nicht verpflichtet und nicht bereit, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
</div></section>'''
    return write(dict(file='impressum.html', title='Impressum | Solar Technik BwM', desc='Impressum von Solar Technik BwM, Malte Behrenswerth, Schmalgraf 48, 4710 Lontzen, Belgien.', body='legal-page'), body)


def datenschutz():
    body = ph('Datenschutz', 'Wie wir mit Ihren Daten umgehen, wenn Sie diese Website besuchen oder uns eine Anfrage schicken.', 'DSGVO', None, '', 'Datenschutz') + f'''
<section class="sec"><div class="wrap narrow prose legal">
<h2>Verantwortlicher</h2><p>{CO['name']}, {CO['person']}, {CO['street']}, B-{CO['zip']} {CO['city']}, {CO['country']}. E-Mail: <a href="mailto:{CO['mail']}">{CO['mail']}</a>, Telefon: {CO['tel']}.</p>
<h2>Kurz gesagt</h2><p>Diese Website setzt keine Cookies, nutzt kein Tracking und keine Analyse-Werkzeuge. Schriften werden von unserem eigenen Server geladen. Eine Karte wird nur geladen, wenn Sie darauf klicken.</p>
<h2>Hosting und Server-Protokolle</h2><p>Beim Aufruf der Website verarbeitet unser Hosting-Anbieter technisch notwendige Daten (IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browser). Das ist nötig, um die Seite auszuliefern und vor Angriffen zu schützen (Art. 6 Abs. 1 lit. f DSGVO). Die Protokolle werden nach kurzer Zeit gelöscht. Hosting-Anbieter: [wird vor dem Start eingetragen].</p>
<h2>Skripte für Animationen</h2><p>Für Animationen laden wir die Bibliotheken GSAP und Lenis vom Dienst jsDelivr. Dabei wird Ihre IP-Adresse an jsDelivr übermittelt (Art. 6 Abs. 1 lit. f DSGVO). Es werden keine Cookies gesetzt.</p>
<h2>Anfrageformular und E-Mail</h2><p>Wenn Sie uns über das Formular oder per E-Mail schreiben, verarbeiten wir Ihre Angaben (Name, Kontaktdaten, Angaben zu Dach, Verbrauch, Heizung und Warmwasser, Nachricht), um Ihre Anfrage zu beantworten und ein Angebot zu erstellen (Art. 6 Abs. 1 lit. b DSGVO). Wir löschen die Daten, wenn sie dafür nicht mehr gebraucht werden und keine Aufbewahrungspflichten bestehen.</p>
<h2>Karte (OpenStreetMap)</h2><p>Auf der Kontaktseite können Sie eine Karte von OpenStreetMap laden. Erst mit Ihrem Klick wird eine Verbindung zu den Servern der OpenStreetMap Foundation hergestellt und Ihre IP-Adresse übertragen (Art. 6 Abs. 1 lit. a DSGVO).</p>
<h2>Ihre Rechte</h2><p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch. Eine Einwilligung können Sie jederzeit widerrufen. Sie können sich bei einer Datenschutz-Aufsichtsbehörde beschweren, in Belgien bei der Datenschutzbehörde (Autorité de protection des données / Gegevensbeschermingsautoriteit), Rue de la Presse 35, 1000 Brüssel.</p>
<p class="art-meta">Stand: September 2026</p>
</div></section>'''
    return write(dict(file='datenschutz.html', title='Datenschutz | Solar Technik BwM', desc='Datenschutzerklärung von Solar Technik BwM: keine Cookies, kein Tracking, Umgang mit Anfragen, Karte erst per Klick.', body='legal-page'), body)


PAGES += [referenzen, ueber_uns, ratgeber] + [(lambda a=a: article(a)) for a in ARTICLES] + [faq, kontakt, danke, notfound, impressum, datenschutz]


if __name__ == '__main__':
    files = [fn() for fn in PAGES]
    skip = {'danke.html', '404.html'}
    urls = ''.join(f'<url><loc>{DOMAIN}/{"" if f == "index.html" else f}</loc><lastmod>{TODAY}</lastmod></url>\n' for f in files if f not in skip)
    open(OUT + 'sitemap.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    open(OUT + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\nDisallow: /danke.html\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    print(len(files), 'Seiten:', ', '.join(files))
