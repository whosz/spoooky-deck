// Builds a reading from the Tracery grammar. User input is stripped of Tracery special characters.
const clean = s => s.replace(/[#\[\]]/g, '').trim();
const pick = (r, a) => a[Math.floor(r() * a.length)];
const SUIT_EL = { wands: 'fire', cups: 'water', swords: 'air', pentacles: 'earth' };   // element of the minor arcana suit

export const INDUSTRIES = ['it', 'handel', 'uslugi', 'produkcja', 'gastro', 'inne'], STAGES = ['start', 'rozwoj', 'dojrzala', 'zmiana'];

export function compose({ seed, card, reversed, name, zodiac, company, industry = 'inne', stage = 'rozwoj', lang, grammar, ui }) {
  const r = new Math.seedrandom('o' + seed);
  tracery.setRng(r);
  const side = reversed ? card.rev : card.up;
  const meaning = pick(r, side.sentences[lang]);
  const service = pick(r, card.services);
  const g = tracery.createGrammar({
    ...grammar,
    name: [clean(name) || ui.anon],
    company: [clean(company)],
    zodiac: [zodiac.name],
    card: [card.name[lang]],
    pos: [reversed ? ui.reversed : ui.upright],
    keywords: [side.keywords[lang].join(', ')],
    meaning: [meaning],
    business: [card.business[lang]],
    omen: [pick(r, zodiac.omens)],
    puenta: [`#puenta_${service}#`],
    kontekst: [`#branza_${INDUSTRIES.includes(industry) ? industry : 'inne'}# #etap_${STAGES.includes(stage) ? stage : 'rozwoj'}#`],   // sentences about the company's industry and stage (independent of the card)
    zywiol: [(ui[zodiac.element] || '').toLowerCase()],
  });
  g.addModifiers(tracery.baseEngModifiers);
  // Minor arcana get an extra sentence about whether the sign's element matches the suit's element; major arcana have no single element.
  const ids = ['wezwanie', 'znaczenie', 'omen'];
  if (card.suit) ids.push(SUIT_EL[card.suit] === zodiac.element ? 'zywiol_zgodny' : 'zywiol_rozny');
  ids.push('kontekst', 'puenta', 'cta');
  const parts = ids.map(id => ({ id: id.startsWith('zywiol') ? 'zywiol' : id, text: g.flatten(`#${id}#`) }));
  return { parts, quote: meaning };
}
