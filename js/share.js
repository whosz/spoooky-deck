// Reading image (canvas 1080x1920, stories format). The name does not go on the image, the company does.
// The card is drawn as in the app: a 64x96 illustration at an integer scale, gold frame, Roman numeral, name plate.
const GOLD = '#d8aa48', TEXT = '#e8dcc0', BG = '#0b0d17', K = 10;   // K: piksele grafiki karty na piksele obrazka
const ROMAN = ['0', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI', 'XVII', 'XVIII', 'XIX', 'XX', 'XXI'];

const loadImg = src => new Promise((res, rej) => { const i = new Image(); i.onload = () => res(i); i.onerror = rej; i.src = src; });

function wrap(g, text, maxW) {
  const lines = []; let cur = '';
  for (const w of text.split(' ')) { const t = cur ? cur + ' ' + w : w; if (g.measureText(t).width > maxW && cur) { lines.push(cur); cur = w; } else cur = t; }
  return cur ? [...lines, cur] : lines;
}

// 9-slice: a 24x24 image with an 8 px edge, drawn at scale s
function nine(g, img, x, y, w, h, s) {
  const e = 8, c = e * s, m = img.width - 2 * e;
  const put = (sx, sy, sw, sh, dx, dy, dw, dh) => g.drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh);
  put(0, 0, e, e, x, y, c, c); put(e + m, 0, e, e, x + w - c, y, c, c); put(0, e + m, e, e, x, y + h - c, c, c); put(e + m, e + m, e, e, x + w - c, y + h - c, c, c);
  put(e, 0, m, e, x + c, y, w - 2 * c, c); put(e, e + m, m, e, x + c, y + h - c, w - 2 * c, c);
  put(0, e, e, m, x, y + c, c, h - 2 * c); put(e + m, e, e, m, x + w - c, y + c, c, h - 2 * c);
  put(e, e, m, m, x + c, y + c, w - 2 * c, h - 2 * c);
}

async function drawCard(card, lang) {
  const [art, frame, plate] = await Promise.all([`img/cards/${card.id}.png`, 'img/ui/cardframe.png', 'img/ui/frame.png'].map(loadImg));
  const o = document.createElement('canvas'); o.width = 64 * K; o.height = 96 * K;
  const g = o.getContext('2d'); g.imageSmoothingEnabled = false;
  g.drawImage(art, 0, 0, o.width, o.height);
  g.drawImage(frame, 0, 0, o.width, o.height);
  // Roman numeral in the top left corner
  const num = card.arcana === 'major' ? ROMAN[card.number] : String(card.number);
  g.font = '40px "Olde Tome"'; g.textBaseline = 'middle'; g.textAlign = 'left';
  const nw = g.measureText(num).width + 24;
  g.fillStyle = '#0b0d17d9'; g.fillRect(52, 46, nw, 56); g.fillStyle = '#f0d27a'; g.fillText(num, 64, 76);
  // name plate
  const name = card.name[lang]; g.font = '52px "Olde Tome"';
  const lines = wrap(g, name, o.width - 160), lh = 58, ph = 32 + lines.length * lh, px = 40, pw = o.width - 80, py = o.height - 40 - ph;
  g.fillStyle = '#161a2a'; g.fillRect(px + 8, py + 8, pw - 16, ph - 16); nine(g, plate, px, py, pw, ph, 4);
  g.fillStyle = '#f0d27a'; g.textAlign = 'center';
  lines.forEach((l, i) => g.fillText(l, o.width / 2, py + 16 + lh / 2 + i * lh + 2));
  return o;
}

// Title as gold metal, as on the splash: hard light bands, dark outline, shadow and a soft glow (static, no animation).
function drawGoldTitle(g, text, x, baseline, px) {
  g.save(); g.font = `${px}px "Old English Gothic Pixel"`; g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  const top = baseline - .76 * px, h = 1.02 * px, d = Math.max(2, Math.round(px / 40));   // bands: from the top of the letters (0.75 em above the baseline), brown from the baseline down, so the descenders of p and y are brown
  g.shadowColor = '#ffb34766'; g.shadowBlur = px / 5; g.fillStyle = '#000'; g.fillText(text, x, baseline + d * 2.5); g.shadowBlur = 0;   // shadow underneath and glow
  g.fillStyle = '#3a1604';
  for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]) g.fillText(text, x + dx * d, baseline + dy * d);   // obrys
  const gr = g.createLinearGradient(0, top, 0, top + h);
  [['#fff6b0', 0], ['#fff6b0', .06], ['#ffd84a', .06], ['#ffd84a', .28], ['#f2a31f', .28], ['#f2a31f', .5], ['#c9690e', .5], ['#c9690e', .72], ['#8a3a08', .72], ['#8a3a08', 1]].forEach(([c, o]) => gr.addColorStop(o, c));
  g.fillStyle = gr; g.fillText(text, x, baseline); g.restore();
}

export async function makeShareImage({ card, reversed, quote, company, lang, ui }) {
  const glyphs = 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻ';
  await Promise.all([document.fonts.load('52px "Olde Tome"', glyphs), document.fonts.load('120px "Old English Gothic Pixel"'), document.fonts.load('40px "Geist Pixel"', glyphs)]);
  const [cardCanvas, bg] = await Promise.all([drawCard(card, lang), loadImg('img/ui/bg-intro.png')]);
  const c = document.createElement('canvas'); c.width = 1080; c.height = 1920;
  const g = c.getContext('2d'); g.imageSmoothingEnabled = false;
  // background as on the splash: bg-intro 72x128 at scale 15 (exactly 1080x1920) with the same opacity as in the app
  g.fillStyle = BG; g.fillRect(0, 0, 1080, 1920);
  g.globalAlpha = .55; g.drawImage(bg, 0, 0, 1080, 1920); g.globalAlpha = 1;
  const grad = g.createLinearGradient(0, 0, 0, 1920); grad.addColorStop(0, '#0b0d1700'); grad.addColorStop(.5, '#0b0d1733'); grad.addColorStop(1, '#0b0d17cc'); g.fillStyle = grad; g.fillRect(0, 0, 1080, 1920);
  for (let i = 0; i < 70; i++) { g.fillStyle = i % 3 ? '#ffb34766' : '#e8dcc055'; g.fillRect(Math.floor(((i * 7919) % 1080) / 6) * 6, Math.floor(((i * 104729) % 1920) / 6) * 6, 6, 6); }
  g.textAlign = 'center'; g.textBaseline = 'alphabetic';
  // measure the content block to centre it vertically within the whole image
  const q = lang === 'pl' ? `„${quote}”` : `“${quote}”`;
  g.font = '56px "Olde Tome"'; const qLines = wrap(g, q, 900).slice(0, 4);
  const co = (company || '').slice(0, 40);
  const TITLE = 120, GAP1 = 74, CARD = cardCanvas.height, GAP2 = 70, POS = 44, GAP3 = 46, QH = qLines.length * 72, GAP4 = 64, FOOT = co ? 38 + 20 + 38 : 38;
  const total = TITLE + GAP1 + CARD + GAP2 + POS + GAP3 + QH + GAP4 + FOOT;
  let y = Math.round((1920 - total) / 2);
  drawGoldTitle(g, 'Spoooky Deck', 540, y + TITLE - 18, TITLE);
  y += TITLE + GAP1;
  // card (rotated by 180 degrees if reversed) with a pixel red glow for reversed ones
  const cx = (1080 - cardCanvas.width) / 2, cy = y;
  if (reversed) [[20, '#b3243a'], [30, '#b3243a99'], [40, '#b3243a55'], [50, '#b3243a22']].forEach(([d, col]) => {   // 10 px bands: strongest next to the card, fading outward (like the frame in the app)
    g.fillStyle = col; g.beginPath(); g.rect(cx - d, cy - d, cardCanvas.width + 2 * d, cardCanvas.height + 2 * d); g.rect(cx - d + 10, cy - d + 10, cardCanvas.width + 2 * d - 20, cardCanvas.height + 2 * d - 20); g.fill('evenodd');
  });
  g.fillStyle = '#0b0d17'; g.fillRect(cx - 10, cy - 10, cardCanvas.width + 20, cardCanvas.height + 20);
  g.save(); g.translate(cx + cardCanvas.width / 2, cy + cardCanvas.height / 2); if (reversed) g.rotate(Math.PI); g.drawImage(cardCanvas, -cardCanvas.width / 2, -cardCanvas.height / 2); g.restore();
  y += CARD + GAP2;
  g.fillStyle = GOLD; g.font = '44px "Geist Pixel"'; g.fillText((reversed ? ui.reversed : ui.upright).toUpperCase(), 540, y + POS - 8);
  y += POS + GAP3;
  g.fillStyle = TEXT; g.font = '56px "Olde Tome"'; g.shadowColor = '#000'; g.shadowOffsetY = 4;
  qLines.forEach((l, i) => g.fillText(l, 540, y + 52 + i * 72)); g.shadowOffsetY = 0;
  y += QH + GAP4;
  g.fillStyle = GOLD; g.font = '38px "Geist Pixel"';
  if (co) { g.fillText((lang === 'pl' ? 'Wróżba dla firmy ' : 'Reading for ') + (lang === 'pl' ? `„${co}”` : `“${co}”`), 540, y + 34); y += 58; }
  g.fillStyle = '#e8dcc0bb'; g.fillText('whosz.pl/tarot', 540, y + 34);
  return new Promise(res => c.toBlob(res, 'image/png'));
}

export async function shareImage(data) {
  const blob = await makeShareImage(data), file = new File([blob], 'spoooky-deck.png', { type: 'image/png' });
  if (navigator.canShare && navigator.canShare({ files: [file] })) { try { await navigator.share({ files: [file], title: data.ui.title }); return; } catch (e) { if (e.name === 'AbortError') return; } }
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'spoooky-deck.png'; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}
