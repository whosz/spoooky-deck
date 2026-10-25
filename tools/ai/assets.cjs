// node tools/ai/assets.cjs: processes selected AI assets -> img/ui (card back 72x108, candle with transparency, hero 144x96).
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp'); const fs = require('fs');
const BACK = process.env.BACK || 'back_1', CANDLE = process.env.CANDLE || 'candle_1', HERO = process.env.HERO || 'hero_1';
(async () => {
  if (fs.existsSync(`tools/ai/raw/${BACK}.png`)) {
    const m = await sharp(`tools/ai/raw/${BACK}.png`).metadata(), cx = Math.round(m.width * .045), cy = Math.round(m.height * .03);
    await sharp(`tools/ai/raw/${BACK}.png`).extract({ left: cx, top: cy, width: m.width - 2 * cx, height: m.height - 2 * cy }).resize(72, 108, { kernel: 'nearest', fit: 'fill' }).png({ palette: true, colours: 24, dither: 0 }).toFile('img/ui/back.png'); console.log('back');
  }
  if (fs.existsSync(`tools/ai/raw/${CANDLE}.png`)) {   // green background -> transparency, trim, height 56
    const { data, info } = await sharp(`tools/ai/raw/${CANDLE}.png`).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
    for (let i = 0; i < data.length; i += 4) if (data[i + 1] > data[i] + 50 && data[i + 1] > data[i + 2] + 50) data[i + 3] = 0;
    await sharp(data, { raw: info }).trim().resize({ height: 56, kernel: 'nearest' }).png().toFile('img/ui/candle.png'); console.log('candle');
  }
  if (fs.existsSync(`tools/ai/raw/${HERO}.png`)) {
    await sharp(`tools/ai/raw/${HERO}.png`).resize(144, 96, { kernel: 'nearest', fit: 'fill' }).png({ palette: true, colours: 32, dither: 0 }).toFile('img/ui/hero.png'); console.log('hero');
  }
  const INTRO = process.env.INTRO || 'intro_1', BG = { form: process.env.BG_FORM || 'bg_form_1', pick: process.env.BG_PICK || 'bg_pick_1', card: process.env.BG_CARD || 'bg_card_1', read: process.env.BG_READ || 'bg_read_1' };
  if (fs.existsSync(`tools/ai/raw/${INTRO}.png`)) { await sharp(`tools/ai/raw/${INTRO}.png`).resize(108, 187, { kernel: 'nearest', fit: 'fill' }).png({ palette: true, colours: 48, dither: 0 }).toFile('img/ui/intro.png'); console.log('intro'); }
  for (const [k, f] of Object.entries(BG)) if (fs.existsSync(`tools/ai/raw/${f}.png`)) { await sharp(`tools/ai/raw/${f}.png`).resize(72, 128, { kernel: 'nearest', fit: 'fill' }).png({ palette: true, colours: 32, dither: 0 }).toFile(`img/ui/bg-${k}.png`); console.log('bg', k); }
})();
