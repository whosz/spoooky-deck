// node tools/make_field_icons.cjs: 16x16 form field icons (industry: briefcase, stage: sprout) in the palette of the existing field icons.
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp');
const P = { B: [138, 106, 46], G: [216, 170, 72], O: [255, 179, 71], R: [255, 127, 58], C: [230, 220, 192] };
const make = async (out, draw) => {
  const px = Buffer.alloc(16 * 16 * 4);
  const rect = (x, y, w, h, c) => { for (let j = y; j < y + h; j++) for (let i = x; i < x + w; i++) { const o = (j * 16 + i) * 4; px.set([...P[c], 255], o); } };
  draw(rect); await sharp(px, { raw: { width: 16, height: 16, channels: 4 } }).png().toFile(out);
};
(async () => {
  await make('img/ui/ic-industry.png', r => {   // briefcase
    r(5, 2, 6, 1, 'B'); r(5, 3, 1, 2, 'B'); r(10, 3, 1, 2, 'B');
    r(2, 5, 12, 9, 'B'); r(3, 6, 10, 2, 'G'); r(3, 9, 10, 4, 'G'); r(7, 8, 2, 2, 'O');
  });
  await make('img/ui/ic-stage.png', r => {   // sprout in soil
    r(7, 6, 2, 6, 'B');
    r(2, 4, 2, 1, 'G'); r(2, 5, 4, 1, 'G'); r(3, 6, 4, 1, 'G'); r(5, 7, 2, 1, 'G');
    r(10, 2, 4, 1, 'O'); r(9, 3, 5, 1, 'O'); r(9, 4, 4, 1, 'O'); r(9, 5, 3, 1, 'O'); r(9, 6, 2, 1, 'R'); r(9, 7, 1, 1, 'R');
    r(3, 12, 10, 1, 'B'); r(4, 13, 8, 1, 'G'); r(5, 14, 6, 1, 'B');
  });
  const im = await Promise.all(['candle', 'stars', 'tower', 'industry', 'stage'].map(n => sharp(`img/ui/ic-${n}.png`).resize({ width: 160, kernel: 'nearest' }).flatten({ background: '#222842' }).toBuffer()));
  await sharp({ create: { width: 800, height: 160, channels: 3, background: '#222842' } }).composite(im.map((b, i) => ({ input: b, left: i * 160, top: 0 }))).png().toFile('/tmp/ic2.png');
})();
