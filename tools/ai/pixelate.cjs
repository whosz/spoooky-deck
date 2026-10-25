// node tools/ai/pixelate.cjs [id_seed ...]: raw images from tools/ai/raw -> 72x108 tiles (nearest), quantisation to 20 colours without dithering, x2 scale to 144x216 -> tools/ai/out/<file>.png
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp');
const fs = require('fs');
(async () => {
  fs.mkdirSync('tools/ai/out', { recursive: true });
  const files = (process.argv.slice(2).length ? process.argv.slice(2).map(n => n + '.png') : fs.readdirSync('tools/ai/raw')).filter(f => f.endsWith('.png'));
  for (const f of files) {
    const src = await sharp('tools/ai/raw/' + f).trim({ background: '#ffffff', threshold: 14 }).toBuffer();   // trims white borders
    const small = await sharp(src).resize(72, 108, { kernel: 'nearest', fit: 'fill' }).png({ palette: true, colours: 20, dither: 0 }).toBuffer();
    await sharp(small).resize(144, 216, { kernel: 'nearest' }).png({ palette: true }).toFile('tools/ai/out/' + f);
    console.log(f);
  }
})();
