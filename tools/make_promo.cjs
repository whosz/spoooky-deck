// node tools/make_promo.cjs [out=docs/promo/linkedin-1080x1350.png]: a promotional image (LinkedIn, 4:5) in the style of the app.
// Needs a server on :8123 (python3 -m http.server 8123) and Playwright. The Olde Tome font is only on the author's machine.
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const fs = require('fs');
const OUT = process.argv[2] || 'docs/promo/linkedin-1080x1350.png', W = 1080, H = 1350, U = 'http://localhost:8123/';
const html = `<!doctype html><meta charset=utf-8><style>
@font-face{font-family:OE;src:url(${U}fonts/OldEnglishGothicPixel.ttf)}
@font-face{font-family:OT;src:url(${U}fonts/OldeTome.ttf)}
@font-face{font-family:JQ;src:url(${U}fonts/jacquard12-latin.woff2)}
@font-face{font-family:JQ;src:url(${U}fonts/jacquard12-latin-ext.woff2);unicode-range:U+0100-02AF,U+1E00-1EFF,U+2020,U+20A0-20AB,U+20AD-20CF,U+2113,U+2C60-2C7F,U+A720-A7FF}
@font-face{font-family:GP;src:url(${U}fonts/geistpixel-latin.woff2)}
*{box-sizing:border-box}
html,body{margin:0;width:${W}px;height:${H}px;background:#0b0d17;overflow:hidden;image-rendering:pixelated;font-family:GP}
.bg{position:absolute;inset:0;background:url(${U}img/ui/bg-pick.png) 0 -150px/1080px auto no-repeat;opacity:.6}
.shade{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 46%,#0b0d1700 30%,#0b0d17cc 100%),linear-gradient(#0b0d1799 0,#0b0d1700 22%,#0b0d1700 70%,#0b0d17ee 100%)}
.glow{position:absolute;left:50%;top:640px;width:1100px;height:1100px;margin:-550px 0 0 -550px;background:radial-gradient(circle,#ffb34755 0,#ffb34722 38%,#0000 66%)}
.dot{position:absolute;width:6px;height:6px;background:#f0d27a}
h1{position:absolute;left:0;right:0;top:56px;margin:0;text-align:center;font:400 160px/1.02 OE;color:transparent;
  background:linear-gradient(#fff6b0 0 6%,#ffd84a 6% 28%,#f2a31f 28% 50%,#c9690e 50% 72%,#8a3a08 72%) 0 .105em/100% 1.02em repeat-y;-webkit-background-clip:text;background-clip:text;
  filter:drop-shadow(5px 0 0 #3a1604) drop-shadow(-5px 0 0 #3a1604) drop-shadow(0 -5px 0 #3a1604) drop-shadow(0 5px 0 #3a1604) drop-shadow(0 14px 0 #000) drop-shadow(0 0 40px #ffb34777);padding-bottom:.12em}
.hook{position:absolute;left:40px;right:40px;top:262px;text-align:center;font:400 72px/1.1 JQ;color:#e8dcc0;text-shadow:0 5px 0 #000,0 0 18px #000}
.hook b{font-weight:400;color:#ffb347}
.ring{position:absolute;left:348px;top:456px;width:384px;height:576px;box-shadow:0 0 0 10px #0b0d17,0 0 0 20px #ffb347,0 0 0 30px #ffb34799,0 0 0 40px #ffb34755,0 0 0 50px #ffb34722}
.back{position:absolute;top:546px;width:288px;height:432px;background:url(${U}img/ui/back.png) 0 0/100% 100%;box-shadow:0 20px 0 #0009}
.b1{left:92px;transform:rotate(-11deg)} .b2{right:92px;transform:rotate(11deg)}
.card{position:absolute;left:348px;top:456px;width:384px;height:576px;box-shadow:0 0 0 10px #0b0d17}
.card .art{position:absolute;inset:0;background:url(${U}img/cards/ar16.png) 0 0/100% 100%}
.card .fr{position:absolute;inset:0;background:url(${U}img/ui/cardframe.png) 0 0/100% 100%}
.card .num{position:absolute;left:34px;top:30px;padding:0 10px;background:#0b0d17d9;color:#f0d27a;font:400 34px/1.15 OT;text-shadow:0 3px 0 #000}
.card .nm{position:absolute;left:24px;right:24px;bottom:24px;border:24px solid transparent;border-image:url(${U}img/ui/frame.png) 8 fill/24px stretch;padding:0;text-align:center;color:#f0d27a;font:400 44px/1.1 OT;text-shadow:0 3px 0 #000;height:96px}
.quote{position:absolute;left:40px;right:40px;top:1046px;text-align:center;font:400 56px/1.18 OT;color:#e8dcc0;text-shadow:0 4px 0 #000,0 0 14px #000}
.cta{position:absolute;left:110px;right:110px;top:1160px;height:132px;border:32px solid transparent;border-image:url(${U}img/ui/btn.png) 8 fill/32px stretch;display:flex;flex-direction:column;gap:6px;align-items:center;justify-content:center;color:#1a1204;font:400 44px/1 JQ;text-shadow:0 2px 0 #ffe2a8;filter:drop-shadow(0 0 22px #ffb347aa)}
.cta small{font:400 26px/1 GP;color:#3a2606;text-shadow:none}
</style>
<div class=bg></div><div class=shade></div><div class=glow></div>
${[[40,240],[1020,230],[160,420],[930,430],[50,1020],[1030,1010],[70,1170],[1010,1160],[540,36],[40,1300],[1030,1310]].map(([x,y]) => `<i class=dot style="left:${x}px;top:${y}px"></i>`).join('')}
<h1>Spoooky Deck</h1>
<div class=hook>Co karty mówią o <b>Twojej firmie?</b></div>
<div class=ring></div><div class="back b1"></div><div class="back b2"></div>
<div class=card><div class=art></div><div class=fr></div><div class=num>XVI</div><div class=nm style="display:flex;align-items:center;justify-content:center">Wieża</div></div>
<div class=cta>Wylosuj kartę dla swojej firmy<small>whosz.pl/tarot</small></div>`;
(async () => {
  fs.mkdirSync('docs/promo', { recursive: true }); fs.writeFileSync('tools/_promo.html', html);
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: W, height: H } });
  await p.goto(U + 'tools/_promo.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(1200);
  await p.screenshot({ path: OUT }); await b.close(); fs.unlinkSync('tools/_promo.html'); console.log('ok', OUT);
})();
