// node tools/update_test.cjs: sprawdza, że użytkownik dostaje nową wersję bez czyszczenia cache.
// Kopiuje aplikację do katalogu tymczasowego, uruchamia serwer, "wydaje" nową wersję i patrzy, czy strona się przeładowuje:
// od razu na ekranie startowym, a w trakcie losowania dopiero po powrocie do formularza. Wymaga Playwrighta (PLAYWRIGHT_PATH).
const pw = require(process.env.PLAYWRIGHT_PATH || 'playwright'), { execSync, spawn } = require('child_process'), fs = require('fs'), os = require('os'), path = require('path');
const D = fs.mkdtempSync(path.join(os.tmpdir(), 'sd-update-')), PORT = 8124, U = `http://localhost:${PORT}/index.html?lang=pl`;
fs.cpSync('.', D, { recursive: true, filter: s => !/(^|\/)(\.git|node_modules|ai|docs)(\/|$)/.test(s) });
execSync('python3 tools/build_sw.py', { cwd: D });
const srv = spawn('python3', ['-m', 'http.server', String(PORT)], { cwd: D, stdio: 'ignore' });
const bump = () => { fs.appendFileSync(D + '/css/theme.css', `\n/* ${Math.random()} */`); execSync('python3 tools/build_sw.py', { cwd: D }); };
const results = []; const check = (n, ok) => { results.push(ok); console.log(`${ok ? 'PASS' : 'FAIL'}  ${n}`); };
(async () => {
  await new Promise(r => setTimeout(r, 1000));
  const b = await pw.chromium.launch(), p = await (await b.newContext({ viewport: { width: 390, height: 844 }, isMobile: true })).newPage();
  const loaded = async () => { await p.waitForSelector('#loader', { state: 'detached', timeout: 15000 }); await p.waitForTimeout(800); };
  const stale = () => p.evaluate(() => { document.dispatchEvent(new Event('visibilitychange')); });
  await p.goto(U); await loaded(); await p.waitForTimeout(1200); await p.reload(); await loaded();
  check('service worker steruje stroną', await p.evaluate(() => !!navigator.serviceWorker.controller));
  await p.evaluate(() => { window.__old = 1; }); bump(); await stale(); await p.waitForTimeout(3500);
  check('nowa wersja na ekranie startowym: strona przeładowuje się sama', await p.evaluate(() => window.__old === undefined));
  await loaded(); await p.click('#enter'); await p.waitForTimeout(900); await p.fill('#f-name', 'A'); await p.fill('#f-company', 'K'); await p.click('#form .cta'); await p.waitForTimeout(3000);
  await p.evaluate(() => { window.__old = 1; }); bump(); await stale(); await p.waitForTimeout(3500);
  check('nowa wersja w trakcie losowania: bez przerywania', await p.evaluate(() => window.__old === 1 && !document.querySelector('#s-pick').hidden));
  await p.click('#back'); await p.waitForTimeout(2500);
  check('po powrocie do formularza strona się przeładowuje', await p.evaluate(() => window.__old === undefined));
  await b.close(); srv.kill(); fs.rmSync(D, { recursive: true, force: true });
  const failed = results.filter(x => !x).length; console.log(`\n${results.length - failed}/${results.length} testów przeszło`); process.exit(failed ? 1 : 0);
})();
