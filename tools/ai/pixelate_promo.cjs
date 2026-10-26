// node tools/ai/pixelate_promo.cjs <in.png> <out.png>: reduces a promo scene to a 270 px wide grid with 32 colours and scales it x4 with nearest neighbour (crisp pixels, 1080 px wide).
const sharp = require(process.env.SHARP_PATH || 'sharp');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const small = await sharp(inp).resize(270, 338, { fit: 'cover', kernel: 'lanczos3' }).png({ palette: true, colors: 32, dither: 0 }).toBuffer();
  await sharp(small).resize(1080, 1352, { kernel: 'nearest' }).extract({ left: 0, top: 0, width: 1080, height: 1350 }).png().toFile(out);
  console.log('ok', out);
})();
