// node tools/ai/candles.cjs: zielone tło -> przezroczystość, przycięcie, kwantyzacja do 20 kolorów bez ditheringu, wysokość 64 px (skala całkowita) -> img/ui/candle-<A-E>.png
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp'); const fs = require('fs');
(async () => {
  for (const k of ['A', 'B', 'C', 'D', 'E']) {
    const f = `tools/ai/raw/s5_candle${k}_1.png`; if (!fs.existsSync(f)) continue;
    const { data, info } = await sharp(f).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    for (let i = 0; i < data.length; i += 4) { const r = data[i], g = data[i + 1], b = data[i + 2]; if (g > 120 && g > r * 1.35 && g > b * 1.35) data[i + 3] = 0; }
    const trimmed = await sharp(data, { raw: info }).trim().png().toBuffer();
    const small = await sharp(trimmed).resize({ height: 64, kernel: 'lanczos3' }).png({ palette: true, colours: 20, dither: 0 }).toBuffer();
    await sharp(small).toFile(`img/ui/candle-${k}.png`);
    const m = await sharp(small).metadata(); console.log(k, m.width + 'x' + m.height);
  }
})();
