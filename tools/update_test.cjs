// node tools/update_test.cjs: checks that users get a new version without clearing the cache.
// Copies the app to a temp directory, starts a server, "releases" a new version and watches whether the page reloads:
// immediately on the intro screen, and during a draw only after returning to the form. Needs Playwright (PLAYWRIGHT_PATH).
const pw = require(process.env.PLAYWRIGHT_PATH || 'playwright'), { execSync, spawn } = require('child_process'), fs = require('fs'), os = require('os'), path = require('path');
const D = fs.mkdtempSync(path.join(os.tmpdir(), 'sd-update-')), PORT = 8124, U = `http://localhost:${PORT}/index.html?lang=pl`;
fs.cpSync('.', D, { recursive: true, filter: s => !/(^|\/)(\.git|node_modules|ai|docs)(\/|$)/.test(s) });
execSync('python3 tools/build_sw.py', { cwd: D });
const srv = spawn('python3', ['-m', 'http.server', String(PORT)], { cwd: D, stdio: 'ignore' });
const bump = () => { fs.appendFileSync(D + '/css/theme.css', `\n/* ${Math.random()} */`); execSync('python3 tools/build_sw.py', { cwd: D }); };
const results = []; const check = (n, ok) => { results.push(ok); console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}`); };
(async () => {
  await new Promise(r => setTimeout(r, 1000));
  const b = await pw.chromium.launch(), ctx0 = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true }); await ctx0.addInitScript(() => { try { localStorage.setItem('sd_consent', 'denied'); } catch {} });
  const p = await ctx0.newPage();
  const loaded = async () => { await p.waitForSelector('#loader', { state: 'detached', timeout: 15000 }); await p.waitForTimeout(800); };
  const stale = () => p.evaluate(() => { document.dispatchEvent(new Event('visibilitychange')); });
  await p.goto(U); await loaded(); await p.waitForTimeout(1200); await p.reload(); await loaded();
  check('service worker controls the page', await p.evaluate(() => !!navigator.serviceWorker.controller));
  await p.evaluate(() => { window.__old = 1; }); bump(); await stale(); await p.waitForTimeout(3500);
  check('new version on the intro screen: the page reloads by itself', await p.evaluate(() => window.__old === undefined));
  await loaded(); await p.click('#enter'); await p.waitForTimeout(900); await p.fill('#f-name', 'A'); await p.fill('#f-company', 'K'); await p.click('#form .cta'); await p.waitForTimeout(3000);
  await p.evaluate(() => { window.__old = 1; }); bump(); await stale(); await p.waitForTimeout(3500);
  check('new version during a draw: no interruption', await p.evaluate(() => window.__old === 1 && !document.querySelector('#s-pick').hidden));
  await p.click('#back'); await p.waitForTimeout(2500);
  check('after returning to the form the page reloads', await p.evaluate(() => window.__old === undefined));
  // A user on an old version (a commit from before the changes) reloads after a new deploy: there must be no mix of old and new modules.
  const OLD = '286a626', D2 = fs.mkdtempSync(path.join(os.tmpdir(), 'sd-old-')), P2 = PORT + 1;
  try {
    execSync(`git archive ${OLD} | tar -x -C ${D2}`, { shell: '/bin/bash' }); execSync('python3 tools/build_sw.py', { cwd: D2 });
    const srv2 = spawn('python3', ['-m', 'http.server', String(P2)], { cwd: D2, stdio: 'ignore' }); await new Promise(r => setTimeout(r, 1000));
    const ctx2 = await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true }); await ctx2.addInitScript(() => { try { localStorage.setItem('sd_consent', 'denied'); } catch {} });
    const q = await ctx2.newPage(), U2 = `http://localhost:${P2}/index.html?lang=pl`;
    await q.goto(U2); await q.waitForSelector('#loader', { state: 'detached', timeout: 15000 }); await q.waitForTimeout(1500); await q.reload(); await q.waitForSelector('#loader', { state: 'detached', timeout: 15000 }); await q.waitForTimeout(800);
    execSync(`git ls-files -z | tar --null -T - -cf - | tar -x -C ${D2}`, { shell: '/bin/bash' }); execSync('python3 tools/build_sw.py', { cwd: D2 });
    await q.reload(); await q.waitForTimeout(5000);
    check(`old version (${OLD}) loads the new one after a single reload without hanging`, await q.evaluate(() => !document.querySelector('#loader') && !!document.querySelector('#clear-form')));
    srv2.kill();
  } finally { fs.rmSync(D2, { recursive: true, force: true }); }
  await b.close(); srv.kill(); fs.rmSync(D, { recursive: true, force: true });
  const failed = results.filter(x => !x).length; console.log(`\n${results.length - failed}/${results.length} tests passed`); process.exit(failed ? 1 : 0);
})();
