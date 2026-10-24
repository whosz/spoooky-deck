// Test dymny: przechodzi cały przepływ aplikacji w przeglądarce i sprawdza, czy nic się nie psuje.
// Użycie:  node tools/smoke.cjs [adres=http://localhost:8123/]
// Wymaga Playwrighta: `npm i playwright` albo PLAYWRIGHT_PATH=/ścieżka/do/node_modules/playwright
// Sprawdza (PL i EN, telefon 390x844 i wąski 320x568): brak błędów w konsoli, brak odpowiedzi 4xx/5xx, wymagane pola formularza,
// wybór karty, ekran karty, trzy zakładki wróżby, menu i zmianę języka, poziome przewijanie oraz pobranie obrazka wróżby.
const pw = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const base = (process.argv[2] || 'http://localhost:8123/').replace(/\/?$/, '/');
const results = [];
const check = (name, ok, extra = '') => { results.push(ok); console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : '  ' + extra}`); };

(async () => {
  const browser = await pw.chromium.launch();
  for (const vp of [{ w: 390, h: 844 }, { w: 320, h: 568 }]) for (const lang of ['pl', 'en']) {
    const tag = `${vp.w}x${vp.h} ${lang}`;
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: 2, isMobile: true, acceptDownloads: true, hasTouch: false });
    const p = await ctx.newPage(); const errs = [], bad = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => m.type() === 'error' && errs.push(m.text()));
    p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
    const noOverflow = async step => check(`${tag}: brak poziomego przewijania (${step})`, await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1 && document.querySelector('#view').scrollWidth <= document.querySelector('#view').clientWidth + 1));
    const visible = id => p.evaluate(id => !document.querySelector(id).hidden, id);

    await p.goto(`${base}index.html?lang=${lang}`); await p.waitForSelector('#loader', { state: 'detached', timeout: 15000 });
    check(`${tag}: ekran startowy widoczny`, await visible('#s-intro')); await noOverflow('start');
    check(`${tag}: przycisk wejścia w widocznym obszarze`, await p.evaluate(() => { const r = document.querySelector('#enter').getBoundingClientRect(); return r.bottom <= innerHeight && r.top >= 0; }));
    await p.click('#enter'); await p.waitForSelector('#s-form:not([hidden])', { timeout: 3000 }).catch(() => {}); await p.waitForTimeout(600); check(`${tag}: formularz widoczny`, await visible('#s-form')); await noOverflow('formularz');
    await p.fill('#f-company', 'Kruk'); await p.click('#form .cta'); await p.waitForTimeout(300);
    check(`${tag}: brak imienia blokuje formularz`, await visible('#s-form') && !(await visible('#s-pick')));
    await p.fill('#f-name', '   '); await p.click('#form .cta'); await p.waitForTimeout(300);
    check(`${tag}: samo spacje w imieniu blokują formularz`, await visible('#s-form'));
    await p.fill('#f-name', 'Anna'); await p.click('#form .cta'); await p.waitForTimeout(2800);
    check(`${tag}: ekran wyboru karty`, await visible('#s-pick')); await noOverflow('wybór');
    const fb = await p.locator('#fan').boundingBox(); await p.mouse.click(fb.x + fb.width / 2, fb.y + fb.height * .4); await p.waitForTimeout(2300);
    check(`${tag}: ekran karty`, await visible('#s-card')); await noOverflow('karta');
    check(`${tag}: ilustracja karty się wczytała`, await p.evaluate(async () => { const u = getComputedStyle(document.querySelector('#card .front')).backgroundImage.match(/url\("?(.*?)"?\)/); if (!u) return false; const i = new Image(); i.src = u[1]; await i.decode().catch(() => {}); return i.naturalWidth === 64; }));
    check(`${tag}: nazwa karty nie wystaje poza kartę`, await p.evaluate(() => { const n = document.querySelector('#card .nm'), c = document.querySelector('#card'); return n.scrollWidth <= c.clientWidth; }));
    await p.click('#more'); await p.waitForTimeout(700); check(`${tag}: ekran wróżby`, await visible('#s-read')); await noOverflow('wróżba');
    check(`${tag}: trzy zakładki mieszczą się`, await p.evaluate(() => { const b = [...document.querySelectorAll('.tabs button')]; return b.length === 3 && b.every(x => x.scrollWidth <= x.clientWidth + 1); }));
    for (const t of ['fortune', 'card', 'key']) { await p.click(`[data-tab=${t}]`); await p.waitForTimeout(250); check(`${tag}: zakładka ${t} ma treść`, await p.evaluate(() => document.querySelectorAll('#tabtext p').length >= 3)); }
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 15000 }).catch(() => null), p.click('#share-img')]);
    check(`${tag}: obrazek wróżby się pobiera`, !!dl);
    await p.click('#menu-btn'); await p.waitForTimeout(300); check(`${tag}: menu się otwiera`, await p.evaluate(() => !document.querySelector('#menu').hidden)); await noOverflow('menu');
    const other = lang === 'pl' ? 'en' : 'pl'; await p.click(`.menu [data-lang=${other}]`); await p.waitForTimeout(800);
    check(`${tag}: zmiana języka`, await p.evaluate(l => document.documentElement.lang === l, other));
    await p.keyboard.press('Escape'); check(`${tag}: menu zamyka się klawiszem Esc`, await p.evaluate(() => document.querySelector('#menu').hidden));
    check(`${tag}: brak błędów w konsoli`, errs.length === 0, errs.join(' | '));
    check(`${tag}: brak odpowiedzi 4xx/5xx`, bad.length === 0, bad.join(' | '));
    await ctx.close();
  }
  await browser.close();
  const failed = results.filter(x => !x).length;
  console.log(`\n${results.length - failed}/${results.length} testów przeszło${failed ? `, ${failed} nie` : ''}`);
  process.exit(failed ? 1 : 0);
})();
