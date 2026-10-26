// Smoke test: walks the whole app flow in a browser and checks that nothing breaks.
// Usage:  node tools/smoke.cjs [url=http://localhost:8123/]
// Needs Playwright: `npm i playwright` or PLAYWRIGHT_PATH=/path/to/node_modules/playwright
// Checks (PL and EN, phone 390x844 and a narrow 320x568): no console errors, no 4xx/5xx responses, required form fields,
// card pick, card screen, three reading tabs, the menu and language switch, horizontal scrolling and downloading the reading image.
const pw = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const base = (process.argv[2] || 'http://localhost:8123/').replace(/\/?$/, '/');
const results = [];
const check = (name, ok, extra = '') => { results.push(ok); console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${ok ? '' : '  ' + extra}`); };

(async () => {
  const browser = await pw.chromium.launch();
  for (const vp of [{ w: 390, h: 844 }, { w: 320, h: 568 }]) for (const lang of ['pl', 'en']) {
    const tag = `${vp.w}x${vp.h} ${lang}`;
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, deviceScaleFactor: 2, isMobile: true, acceptDownloads: true, hasTouch: false });
    await ctx.addInitScript(() => { try { if (!localStorage.sd_consent) localStorage.setItem('sd_consent', 'denied'); } catch {} });   // the consent banner would cover the bottom buttons
    const p = await ctx.newPage(); const errs = [], bad = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => m.type() === 'error' && errs.push(m.text()));
    p.on('response', r => { if (r.status() >= 400) bad.push(r.status() + ' ' + r.url()); });
    const noOverflow = async step => check(`${tag}: no horizontal scrolling (${step})`, await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1 && document.querySelector('#view').scrollWidth <= document.querySelector('#view').clientWidth + 1));
    const visible = id => p.evaluate(id => !document.querySelector(id).hidden, id);

    await p.goto(`${base}index.html?lang=${lang}`); await p.waitForSelector('#loader', { state: 'detached', timeout: 15000 });
    check(`${tag}: intro screen visible`, await visible('#s-intro')); await noOverflow('intro');
    check(`${tag}: the enter button is within the visible area`, await p.evaluate(() => { const r = document.querySelector('#enter').getBoundingClientRect(); return r.bottom <= innerHeight && r.top >= 0; }));
    await p.click('#enter'); await p.waitForSelector('#s-form:not([hidden])', { timeout: 3000 }).catch(() => {}); await p.waitForTimeout(600); check(`${tag}: form visible`, await visible('#s-form')); await noOverflow('form');
    await p.fill('#f-company', 'Kruk'); await p.click('#form .cta'); await p.waitForTimeout(300);
    check(`${tag}: a missing name blocks the form`, await visible('#s-form') && !(await visible('#s-pick')));
    await p.fill('#f-name', '   '); await p.click('#form .cta'); await p.waitForTimeout(300);
    check(`${tag}: a name of only spaces blocks the form`, await visible('#s-form'));
    check(`${tag}: industry and stage fields have options`, await p.evaluate(() => document.querySelector('#f-industry').options.length === 6 && document.querySelector('#f-stage').options.length === 4 && [...document.querySelectorAll('#f-industry option, #f-stage option')].every(o => o.text.trim())));
    check(`${tag}: defaults are Other industry and Growing`, await p.evaluate(() => document.querySelector('#f-industry').value === 'inne' && document.querySelector('#f-stage').value === 'rozwoj'));
    await p.selectOption('#f-industry', 'gastro'); await p.selectOption('#f-stage', 'zmiana');
    await p.fill('#f-name', 'Tymczas'); await p.click('#clear-form');
    check(`${tag}: the Clear form button clears the fields and restores defaults`, await p.evaluate(() => ['#f-name', '#f-company'].every(i => !document.querySelector(i).value) && document.querySelector('#f-industry').value === 'inne' && document.querySelector('#f-stage').value === 'rozwoj' && localStorage.sd_form === '{}'));
    await p.fill('#f-company', 'Kruk'); await p.selectOption('#f-industry', 'gastro'); await p.selectOption('#f-stage', 'zmiana');
    await p.fill('#f-name', 'Anna'); await p.click('#form .cta'); await p.waitForTimeout(2800);
    check(`${tag}: card pick screen`, await visible('#s-pick')); await noOverflow('pick');
    const fb = await p.locator('#fan').boundingBox(); await p.mouse.click(fb.x + fb.width / 2, fb.y + fb.height * .4); await p.waitForTimeout(2300);
    check(`${tag}: card screen`, await visible('#s-card')); await noOverflow('card');
    check(`${tag}: card illustration loaded`, await p.evaluate(async () => { const u = getComputedStyle(document.querySelector('#card .front')).backgroundImage.match(/url\("?(.*?)"?\)/); if (!u) return false; const i = new Image(); i.src = u[1]; await i.decode().catch(() => {}); return i.naturalWidth === 64; }));
    check(`${tag}: card name does not overflow the card`, await p.evaluate(() => { const n = document.querySelector('#card .nm'), c = document.querySelector('#card'); return n.scrollWidth <= c.clientWidth; }));
    await p.click('#more'); await p.waitForTimeout(700); check(`${tag}: reading screen`, await visible('#s-read')); await noOverflow('reading');
    check(`${tag}: the reading has industry and stage sentences, and the choice is remembered`, await p.evaluate(() => { const f = JSON.parse(localStorage.sd_form || '{}'); return f.industry === 'gastro' && f.stage === 'zmiana' && document.querySelectorAll('#tabtext p').length >= 6; }));
    check(`${tag}: three tabs fit`, await p.evaluate(() => { const b = [...document.querySelectorAll('.tabs button')]; return b.length === 3 && b.every(x => x.scrollWidth <= x.clientWidth + 1); }));
    for (const t of ['fortune', 'card', 'key']) { await p.click(`[data-tab=${t}]`); await p.waitForTimeout(250); check(`${tag}: tab ${t} has content`, await p.evaluate(() => document.querySelectorAll('#tabtext p').length >= 3)); }
    const [dl] = await Promise.all([p.waitForEvent('download', { timeout: 15000 }).catch(() => null), p.click('#share-img')]);
    check(`${tag}: the reading image downloads`, !!dl);
    await p.click('#menu-btn'); await p.waitForTimeout(300); check(`${tag}: the menu opens`, await p.evaluate(() => !document.querySelector('#menu').hidden)); await noOverflow('menu');
    const other = lang === 'pl' ? 'en' : 'pl'; await p.click(`.menu [data-lang=${other}]`); await p.waitForTimeout(800);
    check(`${tag}: language switch`, await p.evaluate(l => document.documentElement.lang === l, other));
    await p.keyboard.press('Escape'); check(`${tag}: the menu closes with Esc`, await p.evaluate(() => document.querySelector('#menu').hidden));
    check(`${tag}: no console errors`, errs.length === 0, errs.join(' | '));
    check(`${tag}: no 4xx/5xx responses`, bad.length === 0, bad.join(' | '));
    await ctx.close();
  }
  // Regressions: bugs fixed earlier that are easy to reintroduce by accident.
  {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
    await ctx.addInitScript(() => { try { if (!localStorage.sd_consent) localStorage.setItem('sd_consent', 'denied'); } catch {} });   // the consent banner would cover the bottom buttons
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
    const cls = () => p.evaluate(() => document.querySelector('#fan').className);
    const trans = () => p.evaluate(() => getComputedStyle(document.querySelector('.fcard')).transitionProperty);
    const toForm = async () => { if (await p.evaluate(() => !document.querySelector('#s-intro').hidden)) await p.click('#enter'); await p.waitForSelector('#s-form:not([hidden])'); await p.waitForTimeout(600); await p.fill('#f-name', 'Anna'); await p.fill('#f-company', 'Kruk'); };
    await p.goto(`${base}index.html?lang=pl`); await p.waitForSelector('#loader', { state: 'detached', timeout: 15000 });
    check('regression: the offer button has a gold background (not white)', await p.evaluate(() => /btn\.png/.test(getComputedStyle(document.querySelector('#offer')).borderImageSource) && !/white/.test(getComputedStyle(document.querySelector('#offer')).borderImageSource)));
    check('regression: the menu has a Licenses button in the Application section that links to GitHub', await p.evaluate(() => { const a = document.querySelector('#app-sec a[data-ui=licensesLink]'); return !!a && /github\.com\/whosz\/spoooky-deck/.test(a.href) && !document.querySelector('.lic'); }));
    await toForm(); await p.click('#form .cta'); await p.waitForTimeout(2800);
    // a quick fan drag and a tap during inertia
    const fb = await p.locator('#fan').boundingBox(), y = fb.y + fb.height * .5;
    await p.mouse.move(fb.x + 30, y); await p.mouse.down(); for (let i = 1; i <= 6; i++) { await p.mouse.move(fb.x + 30 + i * 50, y); await p.waitForTimeout(12); } await p.mouse.up(); await p.waitForTimeout(20);
    await p.mouse.move(fb.x + fb.width / 2, y); await p.mouse.down(); await p.mouse.up(); await p.waitForTimeout(3200);
    await p.click('#more'); await p.waitForTimeout(800); await p.click('#again'); await p.waitForTimeout(800); await toForm(); await p.click('#form .cta'); await p.waitForTimeout(400);
    check('regression: after a tap during inertia the next shuffle has transitions', !/drag|glide/.test(await cls()) && (await trans()) !== 'none', await cls() + ' ' + await trans());
    // going back during a shuffle and drawing again: the shuffling class must not disappear before the animation ends
    await p.waitForTimeout(2200); await p.click('#back'); await p.waitForTimeout(700); await p.click('#form .cta'); await p.waitForTimeout(950);
    check('regression: going back during a shuffle does not interrupt the new shuffle', (await cls()).includes('shuffling'), await cls());
    await p.waitForTimeout(1800);
    check('regression: the drag hint is visible, and hidden while the menu is open', await p.evaluate(async () => { const h = document.querySelector('#s-pick .hint'), v = () => getComputedStyle(h).visibility; const a = v(); document.querySelector('#menu-btn').click(); await new Promise(r => setTimeout(r, 150)); const b = v(); return a === 'visible' && b === 'hidden'; }));
    check('regression: no console errors', errs.length === 0, errs.join(' | '));
    await ctx.close();
    // installed app (standalone mode): the install button is hidden, Licenses stays
    const c2 = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true }); await c2.addInitScript(() => { try { if (!localStorage.sd_consent) localStorage.setItem('sd_consent', 'denied'); } catch {} });   // the consent banner would cover the bottom buttons
    const q = await c2.newPage();
    await q.addInitScript(() => { const mm = matchMedia.bind(window); window.matchMedia = x => /standalone/.test(x) ? { matches: true, media: x, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} } : mm(x); });
    await q.goto(`${base}index.html?lang=pl`); await q.waitForSelector('#loader', { state: 'detached', timeout: 15000 });
    check('regression: in the installed app only the install button is hidden', await q.evaluate(() => document.querySelector('#install').hidden && !document.querySelector('#app-sec').hidden && !document.querySelector('#app-sec a[data-ui=licensesLink]').hidden));
    await c2.close();
    // Share text: filled templates with the card details, varied between clicks, nothing personal in them or in the link.
    {
      const c = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true }); await c.addInitScript(() => { try { localStorage.setItem('sd_consent', 'denied'); } catch {} });
      const g = await c.newPage(); await g.addInitScript(() => { window.__shared = []; navigator.share = async d => { window.__shared.push(d); }; });
      await g.goto(`${base}index.html?lang=pl`); await g.waitForSelector('#loader', { state: 'detached', timeout: 15000 });
      await g.click('#enter'); await g.waitForSelector('#s-form:not([hidden])'); await g.waitForTimeout(600); await g.fill('#f-name', 'Anna'); await g.fill('#f-company', 'Tajna Firma');
      await g.selectOption('#f-industry', 'gastro'); await g.selectOption('#f-stage', 'zmiana'); await g.click('#form .cta'); await g.waitForTimeout(2800);
      const fan = await g.locator('#fan').boundingBox(); await g.mouse.click(fan.x + fan.width / 2, fan.y + fan.height * .4); await g.waitForTimeout(2500); await g.click('#more'); await g.waitForTimeout(800);
      for (let i = 0; i < 24; i++) await g.evaluate(() => document.querySelector('#share').click());
      const sh = await g.evaluate(() => window.__shared), cardName = await g.evaluate(() => document.querySelector('#rname').textContent.trim());
      const texts = sh.map(d => d.text);
      check('share text: every message names the card, its position and a quote, with the link kept separate', sh.length === 24 && texts.every(t => t.includes(cardName) && /prosta|odwrócona/.test(t) && /„.+”/.test(t) && !/[{}]/.test(t)) && sh.every(d => /\?s=[a-z0-9]+&lang=pl$/i.test(d.url)));
      check('share text: several templates are used at random', new Set(texts.map(t => t.split(cardName)[0] + t.slice(-30))).size >= 2);
      check('share text: no name, company, industry or stage anywhere', !/Anna|Tajna|Firma|gastro|Gastronomia|zmiana|Zmiana kierunku/i.test(JSON.stringify(sh)));
      await c.close();
    }
    // Analytics: nothing is loaded without a measurement ID or without consent; events carry no personal data.
    const gaPage = async (withId, pre) => {
      const c = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true }), g = await c.newPage(), reqs = [];
      await c.addInitScript(([w, v]) => { window.SD_GA_ID = w ? 'G-TEST123' : ''; try { if (v) localStorage.setItem('sd_consent', v); } catch {} }, [withId, pre]);
      await g.route('**googletagmanager.com**', r => { reqs.push(r.request().url()); r.fulfill({ contentType: 'application/javascript', body: '' }); });
      await g.goto(`${base}index.html?lang=pl`); await g.waitForSelector('#loader', { state: 'detached', timeout: 15000 }); await g.waitForTimeout(500);
      return { c, g, reqs };
    };
    let t = await gaPage(false, null);
    check('analytics: with no measurement ID the banner and the menu button stay hidden and nothing is requested', await t.g.evaluate(() => document.querySelector('#consent').hidden && document.querySelector('#consent-btn').hidden) && t.reqs.length === 0); await t.c.close();
    t = await gaPage(true, null);
    check('analytics: on a first visit the banner shows and nothing is requested before consent', await t.g.evaluate(() => !document.querySelector('#consent').hidden) && t.reqs.length === 0);
    await t.g.click('#consent-yes'); await t.g.waitForTimeout(600);
    check('analytics: after consent the banner hides and gtag.js is requested', await t.g.evaluate(() => document.querySelector('#consent').hidden) && t.reqs.some(u => /gtag\/js\?id=G-TEST123/.test(u)));
    await t.g.evaluate(() => { window.__ev = []; const f = window.gtag; window.gtag = function () { window.__ev.push([...arguments]); return f.apply(this, arguments); }; });
    await t.g.click('#enter'); await t.g.waitForSelector('#s-form:not([hidden])'); await t.g.waitForTimeout(600); await t.g.fill('#f-name', 'Anna'); await t.g.fill('#f-company', 'Tajna Firma'); await t.g.click('#form .cta'); await t.g.waitForTimeout(2800);
    const fan = await t.g.locator('#fan').boundingBox(); await t.g.mouse.click(fan.x + fan.width / 2, fan.y + fan.height * .4); await t.g.waitForTimeout(2500);
    check('analytics: the draw event carries the card but not the name or the company', await t.g.evaluate(() => { const e = window.__ev.filter(a => a[1] === 'draw'); return e.length === 1 && !!e[0][2].card_id && !/Anna|Tajna/.test(JSON.stringify(window.__ev)); }));
    await t.g.click('#menu-btn'); await t.g.waitForTimeout(300); await t.g.click('#consent-btn'); await t.g.waitForTimeout(300);
    check('analytics: consent can be withdrawn in the menu', await t.g.evaluate(() => localStorage.sd_consent === 'denied')); await t.c.close();
    t = await gaPage(true, 'denied');
    check('analytics: a declined choice is remembered (no banner, no requests)', await t.g.evaluate(() => document.querySelector('#consent').hidden) && t.reqs.length === 0); await t.c.close();
  }
  await browser.close();
  const failed = results.filter(x => !x).length;
  console.log(`\n${results.length - failed}/${results.length} tests passed${failed ? `, ${failed} failed` : ''}`);
  process.exit(failed ? 1 : 0);
})();
