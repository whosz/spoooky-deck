// node tools/ai/alpha_fade.cjs <in.png> <out.png>: pikselowe (Bayer) zanikanie krawędzi do PRZEZROCZYSTOŚCI, więc obraz wtapia się w dowolne tło
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp');
const B = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]];
(async () => {
  const { data, info } = await sharp(process.argv[2]).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const { width: W, height: H } = info, o = Buffer.from(data);
  const fx = W * .18, ft = H * .16, fb = H * .22;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const a = Math.min(1, Math.min(x, W - 1 - x) / fx, y / ft, (H - 1 - y) / fb), t = (B[y % 4][x % 4] + .5) / 16;
    const k = Math.pow(a, 1.3); o[(y * W + x) * 4 + 3] = k > t ? 255 : 0;
  }
  await sharp(o, { raw: { width: W, height: H, channels: 4 } }).png().toFile(process.argv[3]);
})();
