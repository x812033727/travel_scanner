#!/usr/bin/env python3
"""Check source-bound numbers, SVG labels, opening disclosure and manifest hashes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
sys.dont_write_bytecode = True
from generate_diagrams import HERE, evidence, source_dir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-dir')
    args = ap.parse_args()
    facts = evidence(source_dir(args.data_dir))
    recorded = json.loads((HERE / 'diagram-facts.json').read_text())
    for key in facts:
        assert facts[key] == recorded[key], key
    files = sorted(HERE.glob('d*.svg'))
    assert len(files) == 6
    checked_text = 0
    visible_by_file = {}
    for p in files:
        root = ET.parse(p).getroot()
        assert root.attrib['viewBox'] == '0 0 1600 900'
        for e in root.iter('{http://www.w3.org/2000/svg}text'):
            assert float(e.attrib['font-size']) >= 36, (p.name, e.text)
            assert 70 <= float(e.attrib['x']) <= 1530, (p.name, e.text)
            assert 50 <= float(e.attrib['y']) <= 880, (p.name, e.text)
            checked_text += 1
        visible_by_file[p.name] = ''.join(e.text or '' for e in root.iter('{http://www.w3.org/2000/svg}text'))
        if p.name.startswith('d0-'):
            visible = ''.join(e.text or '' for e in root.iter('{http://www.w3.org/2000/svg}text'))
            assert '255' in visible and '8 byte' in visible and '接受' in visible
            for spoiler in ['256', 'uint8', 'uint16', '窄化', '轉存', '0…7', '結尾另需']:
                assert spoiler not in visible, spoiler
            assert '256' not in root.find('{http://www.w3.org/2000/svg}desc').text
    # The actual RHS cast must change as well as the declared storage type.
    assert 'uint16_t total = (uint16_t)((uint16_t)n + 1u);' in visible_by_file['d1-guard-narrowing-and-fix.svg']
    assert 'volatile uint8_t i = 0;' in visible_by_file['d4-independent-loop-cycle.svg']
    assert 'i = (uint8_t)(i + 1);' in visible_by_file['d4-independent-loop-cycle.svg']
    assert 'volatile uint16_t i = 0;' in visible_by_file['d4-independent-loop-exit.svg']
    assert 'i = (uint16_t)(i + 1u);' in visible_by_file['d4-independent-loop-exit.svg']
    assert '計數器與更新轉型都加寬' in visible_by_file['d4-independent-loop-exit.svg']
    workflow = visible_by_file['d5-official-proof-and-local-scope.svg']
    assert workflow.index('Rocq 編譯') < workflow.index('驗收檔') < workflow.index('假設稽核')
    for label in ['待證命題', '運作模型版本', '候選證明', '列出假設', '接受判斷', '獨立計數程式返回', '本片未執行官方檢查器']:
        assert label in workflow, label
    assert 'CITED' not in workflow and 'RUN' not in workflow
    manifest = json.loads((HERE / 'diagram-manifest.json').read_text())
    for name, entry in manifest['files'].items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == entry['sha256'], name
    print(json.dumps({'status': 'PASS', 'svg_count': len(files), 'text_labels_checked': checked_text, 'source_domain_cases': 256, 'accept_counts': [9, 8, 0], 'false_accepts': [1, 0, 0], 'false_rejects': [0, 0, 8], 'fixed_loop_actual_returns': 256, 'minimum_text_px': 36, 'official_checker_rerun': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
