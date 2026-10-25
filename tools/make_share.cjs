// node tools/make_share.cjs: favicon (16/32/48 + .ico) z rewersu karty oraz grafika do udostępniania linku (img/og.png 1200x630).
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp');
const { chromium } = require('/home/matt/work/agency-portfolio/node_modules/playwright');
const fs = require('fs');
(async () => {
  const BGF = process.env.BG || 'img/og-bg.png', OUT = process.env.OUT, [W, H] = (process.env.SIZE || '1200x630').split('x').map(Number);   // SIZE: np. 1280x640 dla podglądu repozytorium na GitHubie   // BG: własne tło 120x63 (skala 10), OUT: gdzie zapisać podgląd bez nadpisywania img/og.png
  if (!OUT) {
  // favicon: środkowy kwadrat rewersu 64x64 (słońce), skalowany bez wygładzania
  const crop = await sharp('img/ui/back.png').extract({ left: 0, top: 16, width: 64, height: 64 }).toBuffer();
  const sizes = [16, 32, 48], pngs = [];
  for (const s of sizes) { const b = await sharp(crop).resize(s, s, { kernel: 'nearest' }).png().toBuffer(); pngs.push(b); if (s === 32) fs.writeFileSync('img/icons/favicon-32.png', b); if (s === 16) fs.writeFileSync('img/icons/favicon-16.png', b); }
  const head = Buffer.alloc(6); head.writeUInt16LE(0, 0); head.writeUInt16LE(1, 2); head.writeUInt16LE(pngs.length, 4);
  let off = 6 + 16 * pngs.length; const dir = [];
  pngs.forEach((b, i) => { const e = Buffer.alloc(16); e[0] = sizes[i]; e[1] = sizes[i]; e.writeUInt16LE(1, 4); e.writeUInt16LE(32, 6); e.writeUInt32LE(b.length, 8); e.writeUInt32LE(off, 12); dir.push(e); off += b.length; });
  fs.writeFileSync('favicon.ico', Buffer.concat([head, ...dir, ...pngs]));
  }
  // grafika udostępniania: tło ekranu wyboru + rewers karty + tytuł i hasło (render w Chromium)
  const html = `<!doctype html><meta charset=utf-8><style>
  @font-face{font-family:CS;src:url(http://localhost:8123/fonts/OldEnglishGothicPixel.ttf)}
  @font-face{font-family:GP;src:url(http://localhost:8123/fonts/geistpixel-latin.woff2)}
  html,body{margin:0;width:${W}px;height:${H}px;background:#0b0d17;overflow:hidden;font-family:GP;image-rendering:pixelated}
        .bg{position:absolute;inset:0;background:url(http://localhost:8123/${BGF || 'img/ui/bg-pick.png'}) ${BGF ? 'center/cover' : '-364px -376px/1224px auto'} no-repeat;opacity:${BGF ? 1 : .9};image-rendering:pixelated}
    .fade{position:absolute;inset:0;background:linear-gradient(90deg,#0b0d1700 0,#0b0d1700 52%,#0b0d17 76%)}
  .sh{position:absolute;inset:0;background:linear-gradient(90deg,#0b0d1799 0,#0b0d1766 45%,#0b0d1733 100%)}
  .card{position:absolute;left:96px;top:75px;width:320px;height:480px;background:url(http://localhost:8123/img/ui/back.png) 0 0/100% 100%;image-rendering:pixelated;box-shadow:0 18px 0 #0008}
  .t{position:absolute;left:520px;top:150px;right:60px}
  .stage{position:absolute;left:${(W - 1200) / 2}px;top:${(H - 630) / 2}px;width:1200px;height:630px}
  /* tytuł jak w aplikacji: twarde pasy złota na wiersz, ciemny obrys i cień */
  h1{font:400 120px/1 CS;margin:0 0 28px;color:transparent;-webkit-background-clip:text;background-clip:text;
    background:linear-gradient(#fff6b0 0 16%,#ffd84a 16% 38%,#f2a31f 38% 60%,#c9690e 60% 82%,#8a3a08 82%) 0 0/100% 1em repeat-y;-webkit-background-clip:text;background-clip:text;
    filter:drop-shadow(3px 0 0 #3a1604) drop-shadow(-3px 0 0 #3a1604) drop-shadow(0 -3px 0 #3a1604) drop-shadow(0 3px 0 #3a1604) drop-shadow(0 8px 0 #000) drop-shadow(0 0 24px #ffb34766)}
  p{font:400 42px/1.3 GP;margin:0;color:#e8dcc0;text-shadow:0 4px 0 #000}
  </style><div class=bg></div>${BGF ? '' : '<div class=fade></div>'}<div class=sh></div>
  <div class=stage><div class=card></div><div class=t><h1>Spoooky Deck</h1><p>Losuj · Czytaj · Zaufaj intuicji</p></div></div>`;
  fs.writeFileSync('tools/_share.html', html);
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto('http://localhost:8123/tools/_share.html'); await p.waitForTimeout(1500);
  await p.screenshot({ path: OUT || 'img/og.png' }); await b.close(); fs.unlinkSync('tools/_share.html');
  console.log('ok');
})();
