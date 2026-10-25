// node tools/ai/apply.cjs: copies the chosen variants (tools/ai/picks.json: id -> seed number) from tools/ai/out to img/cards/<id>.png
const fs = require('fs'); const picks = JSON.parse(fs.readFileSync('tools/ai/picks.json', 'utf8'));
for (const [id, seed] of Object.entries(picks)) { fs.copyFileSync(`tools/ai/out/${id}_${seed}.png`, `img/cards/${id}.png`); }
console.log('applied', Object.keys(picks).length);
