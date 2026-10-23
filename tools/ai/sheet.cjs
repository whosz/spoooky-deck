// node tools/ai/sheet.cjs <plik.png> id1 id2 ...: arkusz z wariantami (kolumna = karta, wiersze = ziarna 1,2,3)
const sharp = require('/home/matt/work/agency-portfolio/node_modules/sharp'); const fs = require('fs');
(async () => {
  const [out, ...ids] = process.argv.slice(2), comps = [];
  for (let c = 0; c < ids.length; c++) {
    const vars = fs.readdirSync('tools/ai/out').filter(f => f.startsWith(ids[c] + '_')).sort();
    for (let r = 0; r < vars.length; r++) comps.push({ input: 'tools/ai/out/' + vars[r], left: 8 + c * 152, top: 8 + r * 224 });
  }
  await sharp({ create: { width: ids.length * 152 + 8, height: 3 * 224 + 8, channels: 3, background: '#0b0d17' } }).composite(comps).png().toFile(out);
})();
