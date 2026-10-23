// Obrazek z wróżbą (canvas 1080x1920, format stories). Imię nie trafia na obrazek, firma tak.
const GOLD = '#d8aa48', TEXT = '#e8dcc0', BG = '#0b0d17';

const loadImg = src => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = src; });

function wrap(g, text, maxW) {
  const lines = []; let cur = '';
  for (const w of text.split(' ')) { const t = cur ? cur + ' ' + w : w; if (g.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t; }
  return cur ? [...lines, cur] : lines;
}

export async function makeShareImage({ card, reversed, quote, company, lang, ui }) {
  await Promise.all([document.fonts.load('72px "Jacquard 12"', 'ąćęłńóśźż'), document.fonts.load('96px "Cross Stitch"'), document.fonts.load('40px "Geist Pixel"', 'ąćęłńóśźż')]);
  const art = await loadImg(`img/cards/${card.id}.png`);
  const c = document.createElement('canvas'); c.width = 1080; c.height = 1920;
  const g = c.getContext('2d'); g.imageSmoothingEnabled = false;
  g.fillStyle = BG; g.fillRect(0, 0, 1080, 1920);
  for (let i = 0; i < 90; i++) { g.fillStyle = i % 3 ? '#ffb34766' : '#e8dcc055'; g.fillRect(Math.floor(((i * 7919) % 1080) / 6) * 6, Math.floor(((i * 104729) % 1920) / 6) * 6, 6, 6); }
  g.strokeStyle = GOLD; g.lineWidth = 12; g.strokeRect(30, 30, 1020, 1860);
  g.textAlign = 'center'; g.fillStyle = GOLD; g.font = '96px "Cross Stitch"'; g.fillText('Spoooky Deck', 540, 170);
  // karta 5x (720x1080), odwrócona = obrót o 180 stopni
  g.save(); g.translate(540, 250 + 540); if (reversed) g.rotate(Math.PI); g.drawImage(art, -360, -540, 720, 1080); g.restore();
  g.strokeStyle = reversed ? '#b3243a' : GOLD; g.lineWidth = 12; g.strokeRect(174, 244, 732, 1092);
  g.fillStyle = TEXT; g.font = '84px "Jacquard 12"'; g.fillText(card.name[lang], 540, 1450);
  g.fillStyle = GOLD; g.font = '40px "Geist Pixel"'; g.fillText((reversed ? ui.reversed : ui.upright).toUpperCase(), 540, 1505);
  g.fillStyle = TEXT; g.font = '48px "Jacquard 12"';
  const q = lang === 'pl' ? `„${quote}”` : `“${quote}”`;
  wrap(g, q, 860).slice(0, 4).forEach((l, i) => g.fillText(l, 540, 1590 + i * 62));
  g.fillStyle = GOLD; g.font = '36px "Geist Pixel"';
  const co = (company || '').slice(0, 40); if (co) g.fillText((lang === 'pl' ? 'Wróżba dla firmy ' : 'Reading for ') + (lang === 'pl' ? `„${co}”` : `“${co}”`), 540, 1808);
  g.fillStyle = '#e8dcc099'; g.fillText('whosz.pl/tarot', 540, 1875);
  return new Promise(res => c.toBlob(res, 'image/png'));
}

export async function shareImage(data) {
  const blob = await makeShareImage(data), file = new File([blob], 'spoooky-deck.png', { type: 'image/png' });
  if (navigator.canShare && navigator.canShare({ files: [file] })) { try { await navigator.share({ files: [file], title: data.ui.title }); return; } catch (e) { if (e.name === 'AbortError') return; } }
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'spoooky-deck.png'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}
