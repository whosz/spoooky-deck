// node tools/ai/icons.cjs: ikony PWA z nowego rewersu (img/ui/back.png 72x108) na ciemnym tle ze złotą ramką.
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp');
const mk = async (size, cardH, border, out) => {
  const back = await sharp('img/ui/back.png').resize({ height: cardH, kernel: 'nearest' }).toBuffer();
  const bw = Math.round(size * .02), parts = [{ input: back, gravity: 'centre' }];
  let img = sharp({ create: { width: size, height: size, channels: 4, background: '#0b0d17' } });
  if (border) img = img.composite([{ input: { create: { width: size - 2 * bw, height: size - 2 * bw, channels: 4, background: '#0b0d17' } }, left: bw, top: bw, blend: 'over' }, ...parts]);
  else img = img.composite(parts);
  await img.png().toFile(out);
};
(async () => {
  const gold = async (size, out) => {   // ramka złota: złote tło + ciemny środek
    const bw = Math.round(size * .025), back = await sharp('img/ui/back.png').resize({ height: Math.round(size * .84), kernel: 'nearest' }).toBuffer();
    await sharp({ create: { width: size, height: size, channels: 4, background: '#d8aa48' } }).composite([{ input: { create: { width: size - 2 * bw, height: size - 2 * bw, channels: 4, background: '#0b0d17' } }, left: bw, top: bw }, { input: back, gravity: 'centre' }]).png().toFile(out);
  };
  await gold(192, 'img/icons/icon-192.png'); await gold(512, 'img/icons/icon-512.png'); await gold(180, 'img/icons/apple-touch-icon.png');
  await mk(512, 330, false, 'img/icons/icon-maskable-512.png');
  console.log('icons ok');
})();
