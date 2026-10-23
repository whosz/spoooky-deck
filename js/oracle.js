// Składa wróżbę z gramatyki Tracery. Dane użytkownika są oczyszczone ze znaków specjalnych Tracery.
const clean = s => s.replace(/[#\[\]]/g, '').trim();
const pick = (r, a) => a[Math.floor(r() * a.length)];

export function compose({ seed, card, reversed, name, zodiac, company, lang, grammar, ui }) {
  const r = new Math.seedrandom('o' + seed);
  tracery.setRng(r);
  const side = reversed ? card.rev : card.up;
  const service = pick(r, card.services);
  const g = tracery.createGrammar({
    ...grammar,
    name: [clean(name) || ui.anon],
    company: [clean(company)],
    zodiac: [zodiac.name],
    card: [card.name[lang]],
    pos: [reversed ? ui.reversed : ui.upright],
    keywords: [side.keywords[lang].join(', ')],
    meaning: [pick(r, side.sentences[lang])],
    business: [card.business[lang]],
    omen: [pick(r, zodiac.omens)],
    puenta: [`#puenta_${service}#`],
  });
  g.addModifiers(tracery.baseEngModifiers);
  return ['wezwanie', 'znaczenie', 'omen', 'puenta', 'cta'].map(id => ({ id, text: g.flatten(`#${id}#`) }));
}
