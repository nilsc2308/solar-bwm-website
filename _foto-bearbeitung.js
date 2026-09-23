// Fotos der bisherigen Website aufbereiten: Zuschnitt, leichte Tonwertkorrektur, Schärfe, WebP in zwei Größen.
const sharp = require(process.env.HOME + '/Documents/website 1/co2-consulting-web/node_modules/sharp');
const S = '_quelle/alte-website/';
const J = [
  ['schiene', 'cropped-WhatsApp-Image-2022-11-23-at-15.20.39.jpeg', [1600, 800]],
  ['blechdach', 'WhatsApp-Image-2022-08-29-at-14.38.33.jpeg', [1600, 800]],
  ['blechdach-weit', 'WhatsApp-Image-2022-08-29-at-14.38.16.jpeg', [1600, 800]],
  ['flachdach-stadt', 'WhatsApp-Image-2022-12-09-at-14.23.27-1.jpeg', [1600, 800]],
  ['flachdach-reihen', 'WhatsApp-Image-2022-12-09-at-14.23.28.jpeg', [1600, 800]],
  ['flachdach-ballast', 'WhatsApp-Image-2022-12-09-at-14.23.27-2.jpeg', [1600, 800]],
  ['flachdach-hof', 'WhatsApp-Image-2022-12-09-at-14.23.27.jpeg', [1600, 800]],
  ['ziegeldach', 'WhatsApp-Image-2022-12-09-at-11.29.07.jpeg', [1600, 800]],
  ['bruchsteinhaus', 'WhatsApp-Image-2022-12-09-at-11.29.05.jpeg', [1600, 800]],
  ['backsteinhaus', 'WhatsApp-Image-2022-12-09-at-11.29.06.jpeg', [1200, 600]],
  ['mittelklemme', 'WhatsApp-Image-2022-12-12-at-12.03.35.jpeg', [768, 480]],
  ['endklemme', 'WhatsApp-Image-2022-12-12-at-12.03.37.jpeg', [768, 480]],
  ['dachhaken', 'WhatsApp-Image-2022-12-12-at-12.03.38.jpeg', [768, 480]],
  ['dachhaken-2', 'WhatsApp-Image-2022-12-12-at-12.03.39.jpeg', [768, 480]],
  ['kran', 'WhatsApp-Image-2023-04-27-at-21.02.36.jpeg', [1024, 640]],
];
const P = [ // Herstellerbilder (nur Freistellung, keine Bearbeitung)
  ['p-wechselrichter', 'Wechselrichter.webp', [539, 360]],
  ['p-bms', 'Batterie-Kopf.webp', [355]],
  ['p-speicher', 'Batteriespeicher.webp', [355]],
  ['p-sensor', 'Optimierer.webp', [231]],
  ['p-datenblatt', 'Jasolar-Datenblatt2-rotated.jpg', [787, 400]],
  ['p-modul', 'Jasolar-Datenblatt1-rotated.jpg', [789, 400]],
];
const U = ['dach-vorher', 'daecher-region', 'freiflaeche', 'giebel-pv', 'haus-fertig', 'modul-tragen', 'module-himmel', 'module-nah', 'montage-haende', 'sicherungskasten', 'steinhaus-pv', 'wartung-module', 'ziegel-pv'];
(async () => {
  // Branchen-Fotos von Unsplash (Platzhalter): nur verkleinern
  for (const n of U) for (const [suf, w, q] of [['-l', 1920, 68], ['-m', 900, 64]]) {
    const info = await sharp('_quelle/unsplash/' + n + '.jpg').resize({ width: w, withoutEnlargement: true }).webp({ quality: q, smartSubsample: true, effort: 6 }).toFile(`img/${n}${suf}.webp`);
    console.log(n + suf, info.width, info.height, Math.round(info.size / 1024) + 'KB');
  }
  for (const [n, f, ws] of J) for (const [i, w] of ws.entries()) {
    const suf = ws.length > 1 ? (i ? '-m' : '-l') : '';
    const img = sharp(S + f).rotate().resize({ width: w, withoutEnlargement: true })
      .modulate({ saturation: 1.12, brightness: 1.1 }).linear(1.06, 6).median(3).sharpen({ sigma: .6 });
    const info = await img.webp({ quality: i ? 60 : 62, smartSubsample: true, effort: 6 }).toFile(`img/${n}${suf}.webp`);
    console.log(n + suf, info.width, info.height, Math.round(info.size / 1024) + 'KB');
  }
  for (const [n, f, ws] of P) for (const [i, w] of ws.entries()) {
    const suf = ws.length > 1 ? (i ? '-m' : '-l') : '';
    const info = await sharp(S + f).resize({ width: w, withoutEnlargement: true }).webp({ quality: 82 }).toFile(`img/${n}${suf}.webp`);
    console.log(n + suf, info.width, info.height, Math.round(info.size / 1024) + 'KB');
  }
})();
