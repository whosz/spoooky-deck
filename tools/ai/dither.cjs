// node tools/ai/dither.cjs <in.png> <out.png> [szerokość=144] [wysokość=216] [kolory=32] [rozpiętość=28]
// Styl "16-bit z ditheringiem": zmniejszenie, paleta k-means, uporządkowany dithering Bayera 4x4 (kropkowane gradienty jak w grach 16-bit).
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp');
const BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]];
(async () => {
  const [inp, out, W = 144, H = 216, K = 32, spread = 28, med = 0] = process.argv.slice(2).map((v, i) => i < 2 ? v : +v);   // med = promień filtra medianowego (grupuje piksele w czyste kępy)
  const { data } = await sharp(inp).trim({ background: '#ffffff', threshold: 14 }).resize(W, H, { kernel: 'lanczos3', fit: 'fill' }).median(med || 1).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const n = W * H;
  // k-means (inicjalizacja co n/K piksel po posortowanej jasności)
  const idx = [...Array(n).keys()].sort((a, b) => (data[a * 3] + data[a * 3 + 1] + data[a * 3 + 2]) - (data[b * 3] + data[b * 3 + 1] + data[b * 3 + 2]));
  let pal = Array.from({ length: K }, (_, k) => { const i = idx[Math.floor((k + .5) * n / K)]; return [data[i * 3], data[i * 3 + 1], data[i * 3 + 2]]; });
  const nearest = (r, g, b) => { let best = 0, bd = 1e9; for (let k = 0; k < pal.length; k++) { const d = (r - pal[k][0]) ** 2 + (g - pal[k][1]) ** 2 + (b - pal[k][2]) ** 2; if (d < bd) { bd = d; best = k; } } return best; };
  for (let it = 0; it < 8; it++) {
    const sum = pal.map(() => [0, 0, 0, 0]);
    for (let i = 0; i < n; i++) { const k = nearest(data[i * 3], data[i * 3 + 1], data[i * 3 + 2]); const s = sum[k]; s[0] += data[i * 3]; s[1] += data[i * 3 + 1]; s[2] += data[i * 3 + 2]; s[3]++; }
    pal = pal.map((p, k) => sum[k][3] ? [sum[k][0] / sum[k][3], sum[k][1] / sum[k][3], sum[k][2] / sum[k][3]] : p);
  }
  const o = Buffer.alloc(n * 3);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = y * W + x, t = (BAYER[y % 4][x % 4] + .5) / 16 - .5, d = t * spread;
    const k = nearest(Math.max(0, Math.min(255, data[i * 3] + d)), Math.max(0, Math.min(255, data[i * 3 + 1] + d)), Math.max(0, Math.min(255, data[i * 3 + 2] + d)));
    o[i * 3] = pal[k][0]; o[i * 3 + 1] = pal[k][1]; o[i * 3 + 2] = pal[k][2];
  }
  await sharp(o, { raw: { width: W, height: H, channels: 3 } }).png({ palette: true, colours: K, dither: 0 }).toFile(out);
  console.log(out);
})();
