// node tools/sample.mjs [pl|en] [n]: wypisuje n losowych wrozb do przegladu.
import fs from 'node:fs'; import vm from 'node:vm';
for (const f of ['seedrandom.min.js', 'tracery.js']) vm.runInThisContext(fs.readFileSync(`js/vendor/${f}`, 'utf8') + (f === 'tracery.js' ? ';globalThis.tracery=tracery' : ''));
const { compose } = await import('../js/oracle.js');
const read = f => JSON.parse(fs.readFileSync(f, 'utf8'));
const lang = process.argv[2] || 'pl', n = +process.argv[3] || 8;
const cards = read('data/cards.json'), grammar = read(`data/grammar.${lang}.json`), zodiac = read(`data/zodiac.${lang}.json`), ui = read(`data/ui.${lang}.json`);
for (let i = 0; i < n; i++) {
  const card = cards[Math.floor(Math.random() * 78)], z = zodiac[Math.floor(Math.random() * 12)];
  console.log(`--- ${card.id}\n` + compose({ seed: 's' + Math.random(), card, reversed: Math.random() < .3, name: 'Anna', zodiac: z, company: 'Browar Kruk', lang, grammar, ui }).map(p => p.text).join(' ') + '\n');
}
