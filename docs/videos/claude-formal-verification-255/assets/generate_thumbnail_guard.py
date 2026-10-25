#!/usr/bin/env python3
"""Create a dedicated original thumbnail subject; never modify video.json."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
EPISODE = HERE.parent
PAPER, INK, RED = '#f6efe3', '#1f2a44', '#d8452f'
FONT = 'Noto Sans CJK TC, Noto Sans TC, sans-serif'


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    sources = {name: digest(EPISODE / name) for name in ['video.json', 'claims.md']}
    rows_file = EPISODE / 'data/all-256-cases.json'
    summary_file = EPISODE / 'data/results.json'
    rows = json.loads(rows_file.read_text())
    summary = json.loads(summary_file.read_text())
    row = next(r for r in rows if r['n'] == 255)
    assert row['bad'] == 1 and row['mathematical_fits'] == 0
    assert summary['domain']['capacity_bytes'] == 8

    # All visible strokes and text sit within x=120..1320/y=120..1240.
    # This is a conceptual boolean guard, not a filled memory buffer or a UI.
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1360" viewBox="0 0 1440 1360" role="img" aria-labelledby="title desc">
<title id="title">原創長度檢查縮圖：容量8byte，255卻被接受</title>
<desc id="desc">本片原創guard的實際接受判斷。僅示意容量、輸入與接受結果，沒有執行資料寫入，沒有展示修正機制。</desc>
<rect width="1440" height="1360" fill="{PAPER}"/>
<rect x="120" y="120" width="1200" height="1120" rx="66" fill="{PAPER}" stroke="{INK}" stroke-width="10"/>
<rect x="240" y="180" width="960" height="210" rx="36" fill="{INK}"/>
<text x="720" y="325" fill="{PAPER}" font-family="{FONT}" font-size="138" font-weight="900" text-anchor="middle">容量8byte</text>
<text x="720" y="750" fill="{INK}" font-family="{FONT}" font-size="380" font-weight="900" text-anchor="middle">255</text>
<path d="M720 812 V914" fill="none" stroke="{RED}" stroke-width="28" stroke-linecap="round"/>
<path d="M659 877 L720 945 L781 877" fill="none" stroke="{RED}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="250" y="990" width="940" height="220" rx="38" fill="{RED}"/>
<path d="M410 1100 L462 1150 L555 1048" fill="none" stroke="{PAPER}" stroke-width="28" stroke-linecap="round" stroke-linejoin="round"/>
<text x="840" y="1145" fill="{PAPER}" font-family="{FONT}" font-size="160" font-weight="900" text-anchor="middle">接受</text>
</svg>
'''
    node = ET.fromstring(svg)
    labels = [n.text for n in node.findall('{http://www.w3.org/2000/svg}text')]
    assert labels == ['容量8byte', '255', '接受']
    assert min(float(n.attrib['font-size']) for n in node.findall('{http://www.w3.org/2000/svg}text')) == 138
    assert not any(x in ''.join(labels) for x in ['256', '0', '修正', '證明'])
    output = HERE / 'thumbnail-guard.svg'
    output.write_text(svg)
    png = output.with_suffix('.png')
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y',
               '-c:v', 'librsvg', '-i', str(output), '-frames:v', '1', str(png)]
    result = subprocess.run(command, text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    assert struct.unpack('>II', png.read_bytes()[16:24]) == (1440, 1360)
    assert all(digest(EPISODE / name) == expected for name, expected in sources.items())
    scale = max(700 / 1440, 638 / 1360)
    crop_y = (1360 - 638 / scale) / 2
    proof = {
        'kind': 'original_thumbnail_subject_not_final_media_qa',
        'created_on': '2026-10-25', 'dimensions': [1440, 1360],
        'visible_labels': labels, 'minimum_text_px': 138,
        'content_bounds_including_strokes': [115, 115, 1325, 1245],
        'requested_safe_margin_px': 80, 'actual_minimum_margin_px': 115,
        'native_panel_reference': [700, 638],
        'cover_scale': scale, 'center_crop_source_y_each_side_px': crop_y,
        'minimum_margin_after_reference_crop_source_px': 115 - crop_y,
        'meaning': 'Original guard-only conceptual input/result; no buffer writing, no vendor checker or proof seal.',
        'spoilers': 'No 256, narrowed zero, repair or valid-input answer.',
        'source': {'capacity_bytes': 8, 'n': 255, 'bad_guard_accepts': bool(row['bad']),
                   'row_file_sha256': digest(rows_file), 'summary_sha256': digest(summary_file)},
        'render': {'command': command, 'returncode': result.returncode,
                   'renderer': 'ffmpeg explicit librsvg decoder'},
        'files': {p.name: {'sha256': digest(p), 'bytes': p.stat().st_size}
                  for p in [Path(__file__), output, png]},
        'unchanged_source_sha256': sources,
        'actual_visual_review': 'pending; inspect PNG and native cloned-document preview before handoff',
    }
    (HERE / 'thumbnail-guard.proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'output': str(output), 'png': str(png),
                      'labels': labels, 'unchanged_video_and_claims': True}))


if __name__ == '__main__':
    main()
