// node tools/test_oracle.mjs: checks that the oracle composes valid readings for all combinations.
import fs from 'node:fs'; import vm from 'node:vm'; import assert from 'node:assert';
for (const f of ['seedrandom.min.js', 'tracery.js']) vm.runInThisContext(fs.readFileSync(`js/vendor/${f}`, 'utf8') + (f === 'tracery.js' ? ';globalThis.tracery=tracery' : ''));
const { compose, INDUSTRIES, STAGES } = await import('../js/oracle.js');
const read = f => JSON.parse(fs.readFileSync(f, 'utf8'));
const cards = read('data/cards.json'); let n = 0;
for (const lang of ['pl', 'en']) {
  const grammar = read(`data/grammar.${lang}.json`), zodiac = read(`data/zodiac.${lang}.json`), ui = read(`data/ui.${lang}.json`);
  // every industry and stage needs at least 3 sentences and a label in the UI
  for (const i of INDUSTRIES) { assert(grammar['branza_' + i]?.length >= 3 && ui['ind_' + i], 'industry ' + i); }
  for (const s of STAGES) { assert(grammar['etap_' + s]?.length >= 3 && ui['stg_' + s], 'stage ' + s); }
  const combos = INDUSTRIES.flatMap(i => STAGES.map(s => [i, s]));   // 24 industry x stage pairs, each with every card and position; the zodiac sign cycles
  let zi = 0;
  for (const [industry, stage] of combos) for (const card of cards) for (const reversed of [false, true]) { const z = zodiac[zi++ % zodiac.length];
    const { parts } = compose({ seed: 'abc' + n, card, reversed, name: 'A#[x]', zodiac: z, company: 'Br#ow[ar]', industry, stage, lang, grammar, ui });
    const t = parts.map(p => p.text).join(' ');
    assert(parts.length === (card.suit ? 7 : 6), 'parts');
    const ko = parts.find(x => x.id === 'kontekst'); assert(ko && ko.text.length > 40, 'kontekst: ' + industry + '/' + stage);
    assert(parts.findIndex(x => x.id === 'kontekst') === parts.findIndex(x => x.id === 'puenta') - 1, 'context paragraph right before the punchline');
    assert(parts[2].id === 'omen', 'omen at index 2 (the Key tab uses it)');
    assert(parts.some(x => x.id === 'zywiol') === !!card.suit, 'zywiol only for minor arcana');
    assert(!/[#\[\]]|undefined/.test(t), t);
    assert(t.includes('Browar') && /\bAx?\b/.test(t), 'vars: ' + t);
    const pu = parts.find(x => x.id === 'puenta'); assert(/projektant|designer/.test(pu.text), 'puenta: ' + pu.text);
    const zy = parts.find(x => x.id === 'zywiol'); if (zy) assert(zy.text.toLowerCase().includes(ui[z.element].toLowerCase()), 'zywiol names the element: ' + zy.text);
    n++;
  }
  // the same input gives the same reading, and a different industry or stage changes the text
  const base = { seed: 'det', card: cards[5], reversed: false, name: 'A', zodiac: zodiac[0], company: 'F', lang, grammar, ui };
  const txt = o => compose({ ...base, ...o }).parts.map(p => p.text).join(' ');
  assert(txt({ industry: 'it', stage: 'start' }) === txt({ industry: 'it', stage: 'start' }), 'deterministyczne');
  assert(new Set(INDUSTRIES.map(i => txt({ industry: i, stage: 'start' }))).size === INDUSTRIES.length, 'industry changes the reading');
  assert(new Set(STAGES.map(s => txt({ industry: 'it', stage: s }))).size === STAGES.length, 'stage changes the reading');
  assert(txt({ industry: 'bad', stage: 'bad' }) === txt({ industry: 'inne', stage: 'rozwoj' }), 'unknown values fall back to the default');
  assert(txt({}) === txt({ industry: 'inne', stage: 'rozwoj' }), 'missing values fall back to the default');
}
console.log('ok', n); console.log(compose({ seed: 'x1', card: cards[2], reversed: true, name: 'Anna', zodiac: read('data/zodiac.pl.json')[7], company: 'Browar Kruk', industry: 'gastro', stage: 'zmiana', lang: 'pl', grammar: read('data/grammar.pl.json'), ui: read('data/ui.pl.json') }).parts.map(p => p.text).join('\n'));
