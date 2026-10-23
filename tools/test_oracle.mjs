// node tools/test_oracle.mjs: sprawdza, że oracle składa poprawne wróżby dla wszystkich kombinacji.
import fs from 'node:fs'; import vm from 'node:vm'; import assert from 'node:assert';
for (const f of ['seedrandom.min.js', 'tracery.js']) vm.runInThisContext(fs.readFileSync(`js/vendor/${f}`, 'utf8') + (f === 'tracery.js' ? ';globalThis.tracery=tracery' : ''));
const { compose } = await import('../js/oracle.js');
const read = f => JSON.parse(fs.readFileSync(f, 'utf8'));
const cards = read('data/cards.json'); let n = 0;
for (const lang of ['pl', 'en']) {
  const grammar = read(`data/grammar.${lang}.json`), zodiac = read(`data/zodiac.${lang}.json`), ui = read(`data/ui.${lang}.json`);
  for (const card of cards) for (const reversed of [false, true]) for (const z of zodiac) {
    const { parts } = compose({ seed: 'abc' + n, card, reversed, name: 'A#[x]', zodiac: z, company: 'Br#ow[ar]', lang, grammar, ui });
    const t = parts.map(p => p.text).join(' ');
    assert(parts.length === 5, 'parts');
    assert(!/[#\[\]]|undefined/.test(t), t);
    assert(t.includes('Browar') && /\bAx?\b/.test(t), 'vars: ' + t);
    assert(/projektant|designer/.test(parts[3].text), 'puenta: ' + parts[3].text);
    n++;
  }
}
console.log('ok', n); console.log(compose({ seed: 'x1', card: cards[2], reversed: true, name: 'Anna', zodiac: read('data/zodiac.pl.json')[7], company: 'Browar Kruk', lang: 'pl', grammar: read('data/grammar.pl.json'), ui: read('data/ui.pl.json') }).parts.map(p => p.text).join('\n'));
