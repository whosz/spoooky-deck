// Tło: canvas o niskiej rozdzielczości (wysokość 180 px) skalowany bez wygładzania:
// mgła, dwie świece po bokach i unoszące się iskry. Przy reduced-motion jedna statyczna klatka.
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const H = 180;
const SPARK = ['#ffb347', '#ffb347', '#d8aa48', '#f4efe6'];

export function startBg() {
  const c = document.createElement('canvas');
  c.id = 'bg';
  document.body.prepend(c);
  const g = c.getContext('2d');
  let W, fog, sparks, last = 0;
  const rnd = (a, b) => a + Math.random() * (b - a);

  const size = () => {
    W = c.width = Math.max(100, Math.round(H * innerWidth / innerHeight)); c.height = H;
    fog = Array.from({ length: 7 }, () => ({ x: rnd(0, W), y: rnd(H * .4, H), r: rnd(40, 90), v: rnd(.05, .2) * (Math.random() < .5 ? -1 : 1) }));
    sparks = Array.from({ length: 36 }, () => ({ x: rnd(0, W), y: rnd(0, H), v: rnd(.1, .4), d: rnd(0, 6.28), c: SPARK[Math.floor(rnd(0, SPARK.length))] }));
  };

  const candle = (x, t) => {
    const fl = Math.floor(2 + Math.sin(t / 130 + x) * 1 + Math.random());
    const glow = g.createRadialGradient(x, H - 52, 2, x, H - 52, 46);
    glow.addColorStop(0, 'rgba(255,179,71,.28)'); glow.addColorStop(1, 'rgba(255,179,71,0)');
    g.fillStyle = glow; g.fillRect(x - 50, H - 100, 100, 100);
    g.fillStyle = '#8a6a2e'; g.fillRect(x - 6, H - 8, 12, 8);
    g.fillStyle = '#e8dcc0'; g.fillRect(x - 4, H - 40, 8, 34);
    g.fillStyle = '#b8ab8c'; g.fillRect(x + 2, H - 40, 2, 34);
    g.fillStyle = '#0b0d17'; g.fillRect(x, H - 44, 1, 4);
    g.fillStyle = '#ff7a2e'; g.fillRect(x - 1, H - 48 - fl, 3, 4 + fl);
    g.fillStyle = '#ffb347'; g.fillRect(x, H - 47 - fl, 1, 3 + fl);
  };

  const frame = t => {
    g.fillStyle = '#0b0d17'; g.fillRect(0, 0, W, H);
    for (const f of fog) {
      const grd = g.createRadialGradient(f.x, f.y, 0, f.x, f.y, f.r);
      grd.addColorStop(0, 'rgba(70,84,130,.16)'); grd.addColorStop(1, 'rgba(70,84,130,0)');
      g.fillStyle = grd; g.fillRect(f.x - f.r, f.y - f.r, f.r * 2, f.r * 2);
      f.x += f.v; if (f.x < -f.r) f.x = W + f.r; if (f.x > W + f.r) f.x = -f.r;
    }
    if (innerWidth >= 700) { candle(22, t); candle(W - 22, t); }
    for (const s of sparks) {
      g.fillStyle = s.c; g.globalAlpha = .4 + .6 * Math.abs(Math.sin(t / 400 + s.d));
      g.fillRect(Math.round(s.x), Math.round(s.y), 1, 1);
      s.y -= s.v; s.x += Math.sin(t / 900 + s.d) * .15;
      if (s.y < -2) { s.y = H + 2; s.x = rnd(0, W); }
    }
    g.globalAlpha = 1;
  };

  const loop = t => { if (t - last > 50) { frame(t); last = t; } requestAnimationFrame(loop); };
  size(); addEventListener('resize', () => { size(); frame(0); });
  frame(0);
  if (!reduced) requestAnimationFrame(loop);
}

// ---- efekty odkrycia karty: błysk, trzęsienie, wybuch pikselowych iskier ----
const PX = 3;   // 1 piksel iskry = 3 px ekranu
let top, tg, parts = [], running = false;
const FLAME = ['#ffb347', '#ffe08a', '#ffffff', '#d8aa48'], BLOOD = ['#b3243a', '#e0506a', '#7a1c2c', '#ffffff'];

function ensureTop() {
  if (top) return;
  top = document.createElement('canvas'); top.id = 'fxtop';
  $phone().append(top); tg = top.getContext('2d');
}
const $phone = () => document.querySelector('#phone');

function sizeTop() { const r = $phone().getBoundingClientRect(); top.width = Math.ceil(r.width / PX); top.height = Math.ceil(r.height / PX); return r; }

function loopTop() {
  tg.clearRect(0, 0, top.width, top.height);
  for (const p of parts) {
    p.x += p.vx; p.y += p.vy; p.vy += .05; p.vx *= .985; p.life--;
    tg.globalAlpha = Math.min(1, p.life / 20); tg.fillStyle = p.c;
    const s = Math.round(p.s), x = Math.round(p.x), y = Math.round(p.y);
    if (p.star) { tg.fillRect(x - s, y, 2 * s + 1, 1); tg.fillRect(x, y - s, 1, 2 * s + 1); } else tg.fillRect(x, y, s, s);
  }
  tg.globalAlpha = 1;
  parts = parts.filter(p => p.life > 0 && p.y < top.height + 4);
  if (parts.length) requestAnimationFrame(loopTop); else { running = false; tg.clearRect(0, 0, top.width, top.height); }
}

export function revealFx(reversed, cardEl) {
  if (reduced) return;
  ensureTop(); const pr = sizeTop(), cr = cardEl.getBoundingClientRect();
  const cx = (cr.left + cr.width / 2 - pr.left) / PX, cy = (cr.top + cr.height / 2 - pr.top) / PX, cols = reversed ? BLOOD : FLAME;
  for (let i = 0; i < 90; i++) {
    const a = Math.random() * Math.PI * 2, v = .6 + Math.random() * 2.4, edge = Math.random() < .5;
    const x = cx + (edge ? Math.cos(a) * cr.width / PX / 2 : (Math.random() - .5) * cr.width / PX), y = cy + (edge ? Math.sin(a) * cr.height / PX / 2 : (Math.random() - .5) * cr.height / PX);
    parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v - .6, life: 35 + Math.random() * 45, s: Math.random() < .2 ? 2 : 1, star: Math.random() < .15, c: cols[Math.floor(Math.random() * cols.length)] });
  }
  if (!running) { running = true; requestAnimationFrame(loopTop); }
  const f = document.createElement('div'); f.className = 'flash' + (reversed ? ' rev' : ''); $phone().append(f); setTimeout(() => f.remove(), 420);
  const ph = $phone(); ph.classList.remove('shake'); void ph.offsetWidth; ph.classList.add('shake'); setTimeout(() => ph.classList.remove('shake'), 350);
}

// ---- pochylanie karty za kursorem i połysk ----
export function tiltCard(slot) {
  if (reduced) return () => {};
  const move = e => {
    const r = slot.getBoundingClientRect();
    const dx = Math.max(-1, Math.min(1, (e.clientX - (r.left + r.width / 2)) / (innerWidth / 2))), dy = Math.max(-1, Math.min(1, (e.clientY - (r.top + r.height / 2)) / (innerHeight / 2)));
    slot.style.setProperty('--ry', (dx * 12).toFixed(1) + 'deg'); slot.style.setProperty('--rx', (-dy * 9).toFixed(1) + 'deg'); slot.style.setProperty('--sx', (50 + dx * 60).toFixed(0) + '%');
  };
  document.addEventListener('pointermove', move);
  return () => { document.removeEventListener('pointermove', move); slot.style.removeProperty('--ry'); slot.style.removeProperty('--rx'); };
}
