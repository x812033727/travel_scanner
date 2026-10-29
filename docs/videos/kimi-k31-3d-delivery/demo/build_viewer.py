#!/usr/bin/env python3
"""Build the self-contained offline viewer from the actual CC0 STL bytes."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
data = {
    'ring': (BASE / 'kimi-official-audit.fixture-ring.stl').read_text(),
    'filled': (BASE / 'kimi-official-audit.fixture-filled-hole-counterexample.stl').read_text(),
    'spec_text': (BASE / 'kimi-official-audit.geometry-spec.json').read_text(),
    'spec': json.loads((BASE / 'kimi-official-audit.geometry-spec.json').read_text()),
}
template = (BASE / 'viewer.template.html').read_text()
assert template.count('__EXACT_FIXTURE_JSON__') == 1
(BASE / 'index.html').write_text(template.replace('__EXACT_FIXTURE_JSON__', json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')))
print('Built index.html from two actual ASCII STL files and the external specification.')
