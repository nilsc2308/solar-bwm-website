# Launch-Checkliste – Solar Technik BwM (Stand 23.9.2026)

Unbeauftragter Entwurf nach der alten Seite solar-bwm.com (WordPress). 24 Seiten, statisch, Generator `_build.py`.

## Geprüft (mit Messwerten)

| Punkt | Ergebnis |
|---|---|
| JS-Fehler | 0 auf allen 24 Seiten – Chromium und WebKit, je 1400 px und 390 px (Playwright, komplett durchgescrollt) |
| Horizontales Scrollen | keins: scrollWidth = clientWidth auf allen Seiten, beide Engines, beide Größen |
| Szene (Startseite) | 41 Schritte Desktop + 41 Schritte Handy (Chromium), 17 + 17 (WebKit) fotografiert: kein Text überlagert einen anderen, fester Ablauf Text raus → Blende → Text rein |
| Überlappende Texte | Leistungs-Schiene gefunden und behoben (alle Klemmen gleicher Weg, vordere zuerst); Kartenbeschriftungen verschoben (Maastricht, Stolberg, Lontzen), Foto überdeckte auf „Befestigung“ die Tabelle – behoben |
| Ladegröße bis „load“ | Startseite Desktop 755 KB (Ziel < 900), Handy 324 KB (Ziel < 500) |
| Formular | leer → „Bitte prüfen: Name, E-Mail, Einverständnis“; falsche Mail erkannt; gültig → danke.html; Vorbelegung per `?thema=`, `?dach=`, `?kwh=`, `?heizung=`, `?ww=`, `?notiz=` funktioniert; Honeypot `bot-field`; Netlify-Forms-Attribute gesetzt |
| Werkzeuge | Steckbrief → Link ins Formular; Finder 13 Module → alle drei „zu klein“ + Hinweis; Hitze 60 °C → 355 W; Stückliste 8 × 2 → 32,8 m Schiene, 8 Stücke, 4 Verbinder, 8 End-, 28 Mittelklemmen (nachgerechnet); Nacht-Rechner 10 kWh / 500 W → 20 h |
| Links intern | 0 kaputte Links und Sprungziele (#werkzeug, #klemmen, #schiene …) |
| Links extern | jsDelivr (GSAP, ScrollTrigger, Lenis) 200 |
| Reduzierte Bewegung | Szene wird statische Fotoreihe mit Bildunterschriften, kein Pin, kein Lenis; Reveals als 150-ms-Blende; Schichtaufbau fertig auseinandergezogen |
| Meta | alle Titel ≤ 65, alle Beschreibungen ≤ 155 Zeichen, je Seite genau eine H1 |
| Alt-Texte | alle `<img>` mit alt (Deko-Vorschaubilder im Menü leer) |
| Canonical, OG, Twitter | auf allen Seiten, eigenes `img/og.jpg` 1200 × 630 |
| JSON-LD | HomeAndConstructionBusiness auf allen Seiten, BreadcrumbList, FAQPage (faq.html), Article (3 Ratgeber) |
| Favicon | `favicon.svg` (Schienenprofil) + `apple-touch-icon.png` 180 px |
| sitemap.xml / robots.txt | 22 URLs (ohne danke/404), danke.html gesperrt |
| 404 | eigene Seite, in netlify.toml hinterlegt |
| Weiterleitungen | alle alten WordPress-Adressen in `netlify.toml` (dienstleistung, Produkt, module, befestigung, elektrokomponenten, wechselrichter, batterie-*, optimierer, referenzen, kontakt, kontakt-bwm, impressum, events) |
| Sicherheits-Header | netlify.toml: CSP, HSTS, X-Frame-Options, nosniff, Referrer-, Permissions-Policy |
| Cookies / Tracking | keine; Schriften lokal (Barlow), Karte erst per Klick (OpenStreetMap) → kein Cookie-Banner nötig |
| Analytics | bewusst keins |
| Barrierefreiheit | Tastatur: Ausklappmenüs (Esc), Dachform-Tabs (Pfeiltasten), Lightbox (Pfeile, Esc, Fokusfalle), Handy-Menü (Fokusfalle); Fokus-Ringe; Kupfer #a8561d auf Weiß ≈ 5 : 1 (AA) |

## Offen – vom Kunden zu klären

1. **Einverständnis** von Malte Behrenswerth für den Entwurf und die Nutzung der Fotos (alle von solar-bwm.com). Das Schienenprofil-Foto ist im Original nur 513 px groß → schärfere Aufnahme erbitten.
2. **E-Mail-Adresse**: alte Seite nennt `info@solar-bwm.com` (Impressum, Fuß) und `info@solar-bwm.de` (Kontakt BwM). Verwendet: .com – bestätigen.
3. **Impressum nach belgischem Recht** prüfen lassen (Unternehmensnummer/USt BE 0768.628.988 übernommen; Rechtsform, ggf. Berufsbezeichnung fehlen). Datenschutz: Hoster eintragen.
4. **Technische Daten der alten Seite widersprüchlich**: „Batterie Speicher“ beschreibt einen 5-kW-Wechselrichter (1000 V, 2 MPPT) – auf speicher.html als „Wechselrichter für den Speicherbetrieb“ übernommen; LUNA2000-5KW-C0 mit „48 V“ Nennspannung und 2 Jahren Garantie wirkt falsch; Seite „Optimierer“ zeigt in Wahrheit den Smart Power Sensor DTSU666-H (jetzt energiezaehler.html). SUN2000-3KTL-L1 Maße/Gewicht und DC-Strom 25 A von der alten Seite übernommen – mit Datenblättern abgleichen.
5. **Aussagen bestätigen**: Ablauf Anfrage → Gespräch vor Ort → Angebot → Montage; Kran-LKW gehört zum Betrieb?; Wartung auch für Fremdanlagen; Speichergrößen 5/10/15 kWh im Nacht-Rechner; Ballast statt Dachdurchdringung auf Flachdächern.
6. **Fotos unklarer Herkunft** nicht übernommen: Solar-Freiland, Solar-Industrie, Solar-Befestigung (evtl. eigene Anlagen? nachfragen) sowie die Pixabay-Bilder und 3D-Männchen.
7. **Sprachen**: Die alte Seite bot per GTranslate Niederländisch/Englisch/Französisch an. Bewusst weggelassen (Maschinenübersetzung). Bei Bedarf NL/FR-Fassung als eigene Seiten.
8. **Porträt/Teamfoto** fehlt – würde „Über uns“ stark aufwerten.
9. **Domain und Hoster**: bisher WordPress auf solar-bwm.com. Formular braucht Netlify (oder ein Formular-Backend); auf GitHub Pages springt das Formular nur zur Danke-Seite.
10. Nach dem Umzug: Google Search Console / Unternehmensprofil anlegen, Sitemap einreichen.
