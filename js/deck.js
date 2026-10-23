// Losowanie karty: deterministyczne z ziarna (seedrandom), ziarno z crypto.
const rng = seed => new Math.seedrandom(seed);

export function draw(seed, cards) {
  const r = rng('d' + seed);
  return { card: cards[Math.floor(r() * cards.length)], reversed: r() < 0.3 };
}

export function loadHistory() {
  try { return JSON.parse(localStorage.getItem('sd_hist')) || []; } catch { return []; }
}

export function saveHistory(h) {
  try { localStorage.setItem('sd_hist', JSON.stringify(h.slice(-10))); } catch {}
}

// Nowe ziarno, którego karta nie powtarza ostatnich w historii (o ile talia na to pozwala).
export function newSeed(cards, history) {
  const recent = history.slice(-Math.min(10, cards.length - 1));
  for (;;) {
    const seed = Array.from(crypto.getRandomValues(new Uint8Array(4)), b => b.toString(36)).join('').slice(0, 6);
    if (!recent.includes(draw(seed, cards).card.id)) return seed;
  }
}
