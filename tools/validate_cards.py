"""python3 tools/validate_cards.py [plik.json] [--partial]: waliduje karty schematem; --partial pomija wymóg 78 kart."""
import json, sys, re
from jsonschema import Draft202012Validator
path = next((a for a in sys.argv[1:] if not a.startswith('--')), 'data/cards.json')
schema = json.load(open('schema/cards.schema.json'))
if '--partial' in sys.argv:
    schema.pop('minItems'); schema.pop('maxItems')
data = json.load(open(path))
errs = [f"{'/'.join(map(str, e.absolute_path))}: {e.message[:120]}" for e in Draft202012Validator(schema).iter_errors(data)]
bad = re.compile(r'[#\[\]–—]')
for c in data:
    for lang in ('pl', 'en'):
        for t in [c['name'][lang], c['business'][lang]] + c['up']['sentences'][lang] + c['rev']['sentences'][lang] + c['up']['keywords'][lang] + c['rev']['keywords'][lang]:
            if bad.search(t): errs.append(f"{c['id']} {lang}: zakazany znak (# [ ] lub myslnik) w: {t[:50]}")
ids = [c['id'] for c in data]
if len(ids) != len(set(ids)): errs.append('duplikaty id')
print('\n'.join(errs) or f'ok {len(data)}'); sys.exit(bool(errs))
