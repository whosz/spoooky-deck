// Tło: canvas o niskiej rozdzielczości (wysokość 180 px) skalowany bez wygładzania:
// mgła, dwie świece po bokach i unoszące się iskry. Przy reduced-motion jedna statyczna klatka.
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let H = 180;   // logiczna wysokość tła; dobierana tak, by 1 piksel = całkowita liczba pikseli urządzenia
const SPARK = ['#ffb347', '#ffb347', '#d8aa48', '#f4efe6'];

export function startBg() {
  const c = document.createElement('canvas');
  c.id = 'bg';
  document.body.prepend(c);
  const g = c.getContext('2d');
  let W, fog, sparks, last = 0;
  const rnd = (a, b) => a + Math.random() * (b - a);

  const size = () => {
    const dpr = devicePixelRatio || 1, kd = Math.max(1, Math.round(innerHeight * dpr / 180));   // pikseli urządzenia na piksel tła
    W = c.width = Math.max(100, Math.ceil(innerWidth * dpr / kd)); H = c.height = Math.ceil(innerHeight * dpr / kd);
    c.style.width = W * kd / dpr + 'px'; c.style.height = H * kd / dpr + 'px';
    fog = Array.from({ length: 7 }, () => ({ x: rnd(0, W), y: rnd(H * .4, H), r: rnd(40, 90), v: rnd(.05, .2) * (Math.random() < .5 ? -1 : 1) }));
    sparks = Array.from({ length: 36 }, () => ({ x: rnd(0, W), y: rnd(0, H), v: rnd(.1, .4), d: rnd(0, 6.28), c: SPARK[Math.floor(rnd(0, SPARK.length))] }));
  };

  const candleImg = new Image(); candleImg.src = 'img/ui/candle.png';
  const candle = (x, t) => {   // sprite świecy (AI) + animowany płomień i poświata
    if (!candleImg.complete || !candleImg.naturalWidth) return;
    const w = candleImg.naturalWidth, h = candleImg.naturalHeight, top = H - h, fx = x + Math.round(w * .05);
    const fl = Math.floor(2 + Math.sin(t / 130 + x) * 1 + Math.random());
    const glow = g.createRadialGradient(fx, top - 4, 2, fx, top - 4, 52);
    glow.addColorStop(0, 'rgba(255,179,71,.30)'); glow.addColorStop(1, 'rgba(255,179,71,0)');
    g.fillStyle = glow; g.fillRect(fx - 56, top - 60, 112, 110);
    g.drawImage(candleImg, Math.round(x - w / 2), top);
    const sway = Math.round(Math.sin(t / 260 + x)), tip = fl > 2 ? 1 : 0;
    const rows = (a, c, o) => a.forEach((hw, i) => { if (hw < 0) return; g.fillStyle = c; g.fillRect(fx - hw - o + (i < 2 ? sway : 0), top - 5 - tip + i - o, 2 * (hw + o) + 1, 1 + 2 * o * (i === 0 ? 1 : 0)); });
    rows([0, 1, 2, 2, 2, 1], '#07080f', 1);                      // kontur płomienia
    rows([0, 1, 2, 2, 2, 1], '#ff7a2e', 0);                      // zewnętrzny
    rows([-1, 0, 1, 1, 1, 0], '#ffb347', 0);                     // środek
    rows([-1, -1, 0, 0, 0, -1], '#fff0b0', 0);                   // rdzeń
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

// ---- efekty odkrycia karty: trzęsienie i wybuch pikselowych iskier ----
let PX = 3;   // 1 piksel iskry w px CSS (całkowita liczba pikseli urządzenia)
let top, tg, parts = [], running = false;
const FLAME = ['#ffb347', '#ffe08a', '#ffffff', '#d8aa48'], BLOOD = ['#b3243a', '#e0506a', '#7a1c2c', '#ffffff'];

function ensureTop() {
  if (top) return;
  top = document.createElement('canvas'); top.id = 'fxtop';
  $phone().append(top); tg = top.getContext('2d');
}
const $phone = () => document.querySelector('#phone');

function sizeTop() {
  const r = $phone().getBoundingClientRect(), dpr = devicePixelRatio || 1; PX = Math.max(1, Math.round(3 * dpr)) / dpr;
  top.width = Math.ceil(r.width / PX); top.height = Math.ceil(r.height / PX); top.style.width = top.width * PX + 'px'; top.style.height = top.height * PX + 'px'; return r;
}

function loopTop() {
  tg.clearRect(0, 0, top.width, top.height);
  for (const p of parts) {
    p.x += p.vx; p.y += p.vy; if (!p.amb) { p.vy += .05; p.vx *= .985; } else p.x += Math.sin((p.life + p.y) / 14) * .12; p.life--;
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
  const ph = $phone(); ph.classList.remove('shake'); void ph.offsetWidth; ph.classList.add('shake'); setTimeout(() => ph.classList.remove('shake'), 350);
}

// ---- złote iskry i błyski na krawędziach karty podczas ruchu ----
const GOLD = ['#8a6a2e', '#d8aa48', '#f0d27a', '#fff6c8'];
function goldDust(cardEl, n) {
  if (reduced || !cardEl) return;
  ensureTop(); const pr = sizeTop(), cr = cardEl.getBoundingClientRect();
  for (let i = 0; i < n; i++) {
    const side = Math.floor(Math.random() * 4), t = Math.random();
    const x = (side === 0 ? cr.left + t * cr.width : side === 1 ? cr.right : side === 2 ? cr.left + t * cr.width : cr.left) - pr.left;
    const y = (side === 0 ? cr.top : side === 1 ? cr.top + t * cr.height : side === 2 ? cr.bottom : cr.top + t * cr.height) - pr.top;
    parts.push({ x: x / PX, y: y / PX, vx: (Math.random() - .5) * .8, vy: -Math.random() * .6, life: 28 + Math.random() * 22, s: 1, star: Math.random() < .2, c: GOLD[1 + Math.floor(Math.random() * 3)] });
  }
  if (!running) { running = true; requestAnimationFrame(loopTop); }
}
function glint(slot) {
  const g = document.createElement('i'); g.className = 'glint';
  const side = Math.floor(Math.random() * 4), t = (8 + Math.random() * 84).toFixed(0) + '%';
  g.style.left = side === 1 ? '100%' : side === 3 ? '0' : t; g.style.top = side === 0 ? '0' : side === 2 ? '100%' : t;
  slot.append(g); setTimeout(() => g.remove(), 750);
}

// ---- pochylanie karty za kursorem lub żyroskopem i połysk ----
let gyroOk = false;
// Na iOS zgodę na ruch urządzenia trzeba wywołać w geście użytkownika (np. wysłanie formularza); na Androidzie nie jest potrzebna.
export async function enableGyro() {
  if (reduced || gyroOk || !('DeviceOrientationEvent' in window)) return;
  const D = window.DeviceOrientationEvent;
  if (typeof D.requestPermission === 'function') { try { if (await D.requestPermission() !== 'granted') return; } catch { return; } }
  gyroOk = true;
}

export function tiltCard(slot) {
  if (reduced) return () => {};
  let ry = 0, rx = 0, drag = null;
  let lastRy = 0, lastRx = 0, lastGlint = 0;
  const apply = () => {
    const delta = Math.abs(ry - lastRy) + Math.abs(rx - lastRx), now = performance.now(); lastRy = ry; lastRx = rx;
    if (delta > 1.4 && now - lastGlint > 130) { lastGlint = now; glint(slot); goldDust(slot.querySelector('.card'), 3); }
    slot.style.setProperty('--ry', ry.toFixed(1) + 'deg'); slot.style.setProperty('--rx', rx.toFixed(1) + 'deg');
    slot.style.setProperty('--sx', (50 + Math.sin(ry * Math.PI / 180) * 60).toFixed(0) + '%');
    const m = ((ry % 360) + 360) % 360; slot.classList.toggle('behind', m > 90 && m < 270);   // widok od tyłu: pokazujemy rewers
  };
  const set = (dx, dy) => { ry = dx * 12; rx = -dy * 9; apply(); };   // dx, dy w zakresie -1..1
  const clamp = v => Math.max(-1, Math.min(1, v));
  let idle;
  const move = e => {
    if (drag) return;
    clearTimeout(idle); idle = setTimeout(() => { if (!drag) set(0, 0); }, 700);   // po chwili bez ruchu karta wraca do ostrego ułożenia
    const r = slot.getBoundingClientRect();
    set(clamp((e.clientX - (r.left + r.width / 2)) / (innerWidth / 2)), clamp((e.clientY - (r.top + r.height / 2)) / (innerHeight / 2)));
  };
  let base = null, cx = 0, cy = 0;
  const gyro = e => {   // pozycja neutralna = ułożenie telefonu przy odkryciu karty; wygładzanie
    if (drag || !gyroOk || e.gamma == null || e.beta == null) return;
    if (!base) base = { b: e.beta, g: e.gamma };
    const tx = clamp((e.gamma - base.g) / 30), ty = clamp((e.beta - base.b) / 30);
    cx += (tx - cx) * .25; cy += (ty - cy) * .25; set(cx, cy);
  };
  // Przytrzymanie i przeciąganie obraca kartę swobodnie (także tyłem); po puszczeniu sprężyście wraca do najbliższego ułożenia.
  const down = e => { drag = { x: e.clientX, y: e.clientY, ry, rx }; slot.setPointerCapture(e.pointerId); slot.classList.add('grab'); slot.style.transition = 'none'; };
  const dmove = e => { if (!drag) return; ry = drag.ry + (e.clientX - drag.x) * .6; rx = Math.max(-40, Math.min(40, drag.rx - (e.clientY - drag.y) * .4)); apply(); };
  const up = () => {
    if (!drag) return; drag = null; slot.classList.remove('grab');
    slot.style.transition = 'transform .7s cubic-bezier(.3,1.5,.5,1)';
    ry = Math.round(ry / 360) * 360; rx = 0; apply();
    setTimeout(() => { if (drag) return; slot.style.transition = 'none'; ry = 0; apply(); void slot.offsetWidth; slot.style.transition = ''; }, 760);
  };
  slot.addEventListener('pointerdown', down); slot.addEventListener('pointermove', dmove); slot.addEventListener('pointerup', up); slot.addEventListener('pointercancel', up);
  document.addEventListener('pointermove', move); window.addEventListener('deviceorientation', gyro);
  return () => {
    document.removeEventListener('pointermove', move); window.removeEventListener('deviceorientation', gyro); clearTimeout(idle);
    slot.removeEventListener('pointerdown', down); slot.removeEventListener('pointermove', dmove); slot.removeEventListener('pointerup', up); slot.removeEventListener('pointercancel', up);
    ['--ry', '--rx'].forEach(p => slot.style.removeProperty(p)); slot.style.transition = ''; slot.classList.remove('behind');
  };
}

// ---- ambient: złote drobinki unoszące się za wachlarzem (ekran wyboru) ----
let ambient = false, ambTimer = 0;
export function startAmbient() {
  if (reduced || ambient) return; ambient = true; ensureTop();
  const tick = () => {
    if (!ambient) return;
    const pr = sizeTop();
    for (let i = 0; i < 2; i++) parts.push({ x: Math.random() * top.width, y: top.height * (.55 + Math.random() * .45), vx: (Math.random() - .5) * .25, vy: -(.15 + Math.random() * .35), life: 80 + Math.random() * 90, s: 1, star: Math.random() < .1, c: GOLD[1 + Math.floor(Math.random() * 3)], amb: true });
    if (!running) { running = true; requestAnimationFrame(loopTop); }
    ambTimer = setTimeout(tick, 120);
  };
  tick();
}
export function stopAmbient() { ambient = false; clearTimeout(ambTimer); }
