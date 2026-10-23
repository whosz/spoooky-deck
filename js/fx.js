// Tło: canvas o niskiej rozdzielczości (wysokość 180 px) skalowany bez wygładzania:
// mgła, dwie świece po bokach i unoszące się iskry. Przy reduced-motion jedna statyczna klatka.
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const H = 180;
const SPARK = ['#ffb347', '#ffb347', '#d8aa48', '#b794f6'];

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
