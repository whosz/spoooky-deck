// node tools/ai/assets.cjs: obrobka wybranych zasobów AI -> img/ui (rewers 72x108, świeca z przezroczystością, hero 144x96).
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp'); const fs = require('fs');
const BACK = process.env.BACK || 'back_1', CANDLE = process.env.CANDLE || 'candle_1', HERO = process.env.HERO || 'hero_1';
(async () => {
  if (fs.existsSync(`tools/ai/raw/${BACK}.png`)) {
    const m = await sharp(`tools/ai/raw/${BACK}.png`).metadata(), cx = Math.round(m.width * .045), cy = Math.round(m.height * .03);
    await sharp(`tools/ai/raw/${BACK}.png`).extract({ left: cx, top: cy, width: m.width - 2 * cx, height: m.height - 2 * cy }).resize(72, 108, { kernel: 'nearest', fit: 'fill' }).png({ palette: true, colours: 24, dither: 0 }).toFile('img/ui/back.png'); console.log('back');
  }
  if (fs.existsSync(`tools/ai/raw/${CANDLE}.png`)) {   // zielone tło -> przezroczystość, przycięcie, wysokość 56
    const { data, info } = await sharp(`tools/ai/raw/${CANDLE}.png`).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    for (let i = 0; i < data.length; i += 4) if (data[i + 1] > data[i] + 50 && data[i + 1] > data[i + 2] + 50) data[i + 3] = 0;
    await sharp(data, { raw: info }).trim().resize({ height: 56, kernel: 'nearest' }).png().toFile('img/ui/candle.png'); console.log('candle');
  }
  if (fs.existsSync(`tools/ai/raw/${HERO}.png`)) {
    await sharp(`tools/ai/raw/${HERO}.png`).resize(144, 96, { kernel: 'nearest', fit: 'fill' }).png({ palette: true, colours: 32, dither: 0 }).toFile('img/ui/hero.png'); console.log('hero');
  }
})();
