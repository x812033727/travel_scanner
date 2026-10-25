#!/usr/bin/env python3
"""Original SVG teaching diagrams. Read recorded evidence; never rerun vendor proofs."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
PAPER, INK, RED = '#f6efe3', '#1f2a44', '#d8452f'
WHITE, RULE, PALE = '#fffdf8', '#c8bfaf', '#f0dfd0'
FONT = 'Noto Sans CJK TC, Noto Sans TC, sans-serif'
SOURCE = '本片原創教學程式／2026-10-25本地實跑'
OFFICIAL = 'https://github.com/theorem-labs/oss-verify-proofs/blob/main/'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cited_snapshot_hashes() -> dict:
    """Reuse pinned provenance on another machine; never silently fetch new facts."""
    previous = HERE / 'diagram-facts.json'
    recorded = json.loads(previous.read_text()).get('official_scope', {}).get('source_snapshot_sha256', {}) if previous.exists() else {}
    directory = Path('/workspace/work/ai-tech-next')
    names = ['third-topic-source-proofs-readme.txt', 'third-topic-source-proofs-origin.txt', 'third-topic-source-proofs-statements.txt', 'third-topic-source-proofs-checking.raw']
    for name in names:
        if (directory / name).exists():
            recorded[name] = sha(directory / name)
        elif name not in recorded:
            raise FileNotFoundError('Missing cited source snapshot: ' + name)
    return recorded


def source_dir(requested: str | None) -> Path:
    candidates = [Path(requested)] if requested else [HERE.parent / 'data', HERE.parent / 'data/formal-demo', Path('/workspace/work/ai-tech-next/formal-demo')]
    for p in candidates:
        if (p / 'all-256-cases.json').exists():
            return p
    raise FileNotFoundError('Pass --data-dir containing the recorded formal-demo files')


def evidence(p: Path) -> dict:
    read = lambda name: json.loads((p / name).read_text())
    rows, loop, summary, sat = read('all-256-cases.json'), read('loop-all-256.json'), read('loop-results.json'), read('sat-output.json')
    assert [r['n'] for r in rows] == list(range(256))
    assert [r['n'] for r in loop] == list(range(256))
    for r in rows:
        n = r['n']
        assert r['promoted_total'] == n + 1
        assert r['narrowed_total'] == (n + 1) % 256
        assert r['bad'] == int((n + 1) % 256 <= 8)
        assert r['widened'] == r['bound'] == r['mathematical_fits'] == int(n + 1 <= 8)
    counts = {}
    for name, key in [('bad', 'bad'), ('fixed', 'widened'), ('deny_all', None)]:
        accepted = [r['n'] for r in rows if (r[key] if key else False)]
        required = set(range(8))
        counts[name] = {'accepted': accepted, 'accept_count': len(accepted), 'false_accepts': sorted(set(accepted) - required), 'false_rejects': sorted(required - set(accepted))}
    assert [counts[k]['accept_count'] for k in ['bad', 'fixed', 'deny_all']] == [9, 8, 0]
    queries = {q['query']: q['result']['result'] for q in sat}
    assert queries['reject_everything_false_accept'] == 'UNSAT'
    assert queries['reject_everything_false_reject'] == 'SAT'
    for r in loop:
        assert r['fixed_model']['terminates'] and r['fixed_model']['exit_i'] == r['n'] + 1
        assert r['fixed_compiled_c']['returned_i'] == r['n'] + 1
        assert not r['fixed_compiled_c']['timed_out']
        if r['n'] < 255:
            assert r['bad_model']['terminates']
            assert r['bad_compiled_c']['returned_i'] == r['n'] + 1
    cycle = summary['bad_model_255_cycle']
    assert cycle['states_before_repeat'] == list(range(256))
    assert cycle['cycle_length'] == 256 and cycle['repeated_state'] == 0
    assert summary['bad_compiled_c_255_timeout_observed']['timeout_seconds'] == 0.25
    guard = (p / 'guard.c').read_text()
    loop_c = (p / 'loop.c').read_text()
    assert 'uint8_t total = (uint8_t)(n + 1);' in guard
    assert 'uint16_t total = (uint16_t)((uint16_t)n + 1u);' in guard
    assert 'volatile uint8_t i = 0;' in loop_c and 'volatile uint16_t i = 0;' in loop_c
    return {'domain': [0, 255], 'capacity_bytes': 8, 'terminator_bytes': 1, 'counts': counts,
            'n255': next(r for r in rows if r['n'] == 255), 'loop_cycle_length': 256,
            'fixed_actual_returns': 256, 'fixed_n255_exit': 256, 'observed_timeout_seconds': 0.25,
            'deny_all_method': 'symbolic model and propositional SAT, not a deny-all C run',
            'local_scope': 'guard only, no buffer writes; independent counter-only loop; no official checker rerun',
            'inputs': {f: {'sha256': sha(p / f)} for f in ['guard.c', 'loop.c', 'all-256-cases.json', 'loop-all-256.json', 'results.json', 'loop-results.json', 'sat-output.json']}}


class SVG:
    def __init__(self, name: str, title: str, desc: str):
        self.name, self.title = name, title
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" role="img" aria-labelledby="title desc">',
                      f'<title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc>',
                      '<defs><marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse"><path d="M1 1 L11 6 L1 11 Z" fill="'+INK+'"/></marker>',
                      '<marker id="red-arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse"><path d="M1 1 L11 6 L1 11 Z" fill="'+RED+'"/></marker></defs>',
                      f'<rect width="1600" height="900" fill="{PAPER}"/>']

    def rect(self, x, y, w, h, fill=WHITE, stroke=RULE, radius=18, sw=2):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, text, size=40, color=INK, weight=500, anchor='start'):
        assert size >= 36
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(str(text))}</text>')

    def lines(self, x, y, lines, size=40, color=INK, weight=500, anchor='start', leading=None):
        for i, line in enumerate(lines):
            self.text(x, y + i * (leading or size * 1.45), line, size, color, weight, anchor)

    def arrow(self, x1, y1, x2, y2, color=INK, width=5):
        marker = 'red-arrow' if color == RED else 'arrow'
        self.parts.append(f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"/>')

    def path(self, d, color=INK, width=5, arrow=True):
        marker = 'red-arrow' if color == RED else 'arrow'
        suffix = f' marker-end="url(#{marker})"' if arrow else ''
        self.parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{suffix}/>')

    def heading(self, kicker, title):
        self.text(80, 80, kicker, 36, RED, 700)
        self.text(80, 155, title, 60, INK, 800)
        self.parts.append(f'<path d="M80 186 H1520" stroke="{RULE}" stroke-width="2"/>')

    def footer(self, extra=None):
        if extra:
            self.text(80, 802, extra, 36)
        self.text(80, 862, SOURCE, 36)

    def save(self):
        (HERE / self.name).write_text('\n'.join(self.parts + ['</svg>']) + '\n')


def opening():
    s = SVG('d0-opening-guard.svg', '容量8 byte，255卻被接受', '原創教學程式A：容量8 byte，輸入長度255 byte，guard的本地實跑結果是接受。這個例子只執行條件檢查，沒有緩衝區寫入。')
    s.heading('原創教學程式 A｜先看輸出', '容量 8 byte，255 卻被接受')
    s.rect(80, 245, 670, 425)
    s.text(125, 313, '輸入長度 n', 44, weight=700)
    s.text(410, 505, '255', 172, weight=800, anchor='middle')
    s.text(410, 602, 'byte', 44, anchor='middle')
    s.arrow(780, 445, 885, 445)
    s.rect(925, 245, 595, 425, PALE, RED, sw=4)
    s.text(1220, 330, 'guard 實際輸出', 44, anchor='middle', weight=700)
    s.text(1220, 510, '接受', 116, RED, 800, 'middle')
    s.text(1220, 605, '容量：8 byte', 52, anchor='middle', weight=700)
    s.footer('本例只執行條件檢查，沒有緩衝區寫入')
    s.save()


def guard():
    s = SVG('d1-guard-narrowing-and-fix.svg', '加法先得到256，轉存才變成0', '原版n+1先整數提升為int並算出256，再轉存uint8_t成0而接受。修版用uint16_t總長保存256，與容量8比較後拒絕。8bit輸入型別和8byte資料容量不同。')
    s.heading('程式 A｜8 bit 輸入型別 ≠ 8 byte 資料容量', '加法先算對，轉存才改了值')
    s.text(80, 240, '原版', 44, RED, 800)
    s.text(850, 240, '保留完整總長', 44, INK, 800)
    s.rect(80, 270, 660, 410, WHITE, RED, sw=3)
    s.rect(860, 270, 660, 410, INK, INK)
    s.text(120, 330, '255 + 1 先以 int 算出', 42)
    s.text(410, 430, '256', 96, weight=800, anchor='middle')
    s.arrow(410, 455, 410, 497, RED)
    s.text(410, 555, '轉存 uint8_t → 0', 48, RED, 800, 'middle')
    s.text(410, 630, '0 ≤ 8：接受', 48, RED, 800, 'middle')
    s.text(900, 330, 'uint16_t 保留總長', 42, WHITE)
    s.text(1190, 460, '256', 116, WHITE, 800, 'middle')
    s.text(1190, 570, '256 > 8', 62, WHITE, 800, 'middle')
    s.text(1190, 640, '拒絕這個輸入', 46, WHITE, 700, 'middle')
    s.text(80, 746, 'uint16_t total = (uint16_t)((uint16_t)n + 1u);', 40, weight=700)
    s.footer('計算與儲存都保留 256；原版不是未定義的有號溢位')
    s.save()


def contract(f):
    s = SVG('d2-full-domain-and-two-directions.svg', '完整256例同時驗收誤接受與誤拒絕', '域0至255，容量8 byte，結尾另需1 byte，應且只應接受0至7。原版接受9例，修版接受8例，一律拒絕的符號模型接受0例且誤拒絕8例。')
    s.heading('程式 A｜完整 256 個輸入', '合法的要進來，不合法的要擋住')
    s.text(80, 242, 'n = 0…255｜容量 8 byte｜結尾另需 1 byte', 42)
    s.text(80, 313, '接受 ⇔ n + 1 ≤ 8 ⇔ n ∈ 0…7', 52, weight=800)
    cards = [('bad', '錯版 guard', '0…7 與 255', RED), ('fixed', 'uint16_t 修版', '只接受 0…7', INK), ('deny_all', '一律拒絕', '符號模型／SAT', INK)]
    for i, (key, title, interval, color) in enumerate(cards):
        x, c = 80 + i * 490, f['counts'][key]
        s.rect(x, 365, 460, 350, WHITE, color, sw=3)
        s.text(x + 28, 423, title, 42, color, 800)
        s.text(x + 28, 490, f"接受 {c['accept_count']} 個", 60, color, 800)
        s.text(x + 28, 550, interval, 36)
        s.text(x + 28, 620, f"誤接受：{len(c['false_accepts'])}", 40, color, 700)
        s.text(x + 28, 678, f"誤拒絕：{len(c['false_rejects'])}", 40, color, 700)
    s.footer('錯版／修版為 C 實跑；一律拒絕為符號對照，未另跑 C')
    s.save()


def cycle():
    s = SVG('d4-independent-loop-cycle.svg', '獨立計數程式的256狀態控制環', '第二個獨立程式，不由guard呼叫。固定n=255，uint8_t計數器i由0逐次加1，255後轉回0；控制模型有256步循環。0.25秒只是一項本次timeout觀察。')
    s.heading('獨立程式 B｜不是 guard 的下一步', '固定 n = 255，計數器回到 0')
    s.text(80, 245, 'volatile uint8_t i = 0;', 40, weight=700)
    s.text(80, 307, 'i = (uint8_t)(i + 1);', 40, weight=700)
    s.text(930, 245, '條件：i ≤ 255', 42)
    s.text(930, 307, '從 0 開始，反覆加 1', 40)
    xs, vals = [180, 650, 1120], ['0', '1…254', '255']
    for x, v in zip(xs, vals):
        s.rect(x - 90, 365, 300, 150, WHITE, RED if v == '0' else INK, radius=24, sw=3)
        s.text(x + 60, 465, v, 64, RED if v == '0' else INK, 800, 'middle')
    for i in range(2):
        s.arrow(xs[i] + 230, 440, xs[i + 1] - 110, 440)
    s.path('M1180 515 V610 H240 V515', RED, 6)
    s.text(710, 675, '256 個狀態後，更新轉型又回到 0', 48, RED, 800, 'middle')
    s.text(80, 738, '控制模型：固定 n，計數器沒有外部改寫', 40)
    s.footer('0.25 秒只是 timeout；不是單靠等待時間證明永不返回')
    s.save()


def exit_loop():
    s = SVG('d4-independent-loop-exit.svg', '加寬計數器後到256並返回', '獨立程式B只把計數器i改為uint16_t。n=255時i走到256，i<=255不成立而返回256。所有0至255輸入的256次實際C呼叫均返回n+1。')
    s.heading('獨立程式 B｜計數器與更新轉型都加寬', '保留 256，這次能走到出口')
    s.text(80, 245, 'volatile uint16_t i = 0;', 40, weight=700)
    s.text(80, 307, 'i = (uint16_t)(i + 1u);', 40, weight=700)
    s.text(1020, 245, '固定 n = 255', 42)
    s.text(1020, 307, '條件：i ≤ 255', 40)
    for x, v in [(80, '0…254'), (480, '255'), (880, '256')]:
        s.rect(x, 365, 300, 145, INK, INK)
        s.text(x + 150, 462, v, 68, WHITE, 800, 'middle')
    s.arrow(400, 438, 455, 438)
    s.arrow(800, 438, 855, 438)
    s.arrow(1200, 438, 1260, 438)
    s.text(1300, 409, '256 > 255', 42, weight=700)
    s.text(1300, 485, '離開', 58, RED, 800)
    s.rect(80, 575, 1440, 155, WHITE, INK, sw=3)
    s.text(120, 639, 'n = 255：預期返回 256，實際返回 256', 48, weight=800)
    s.text(120, 698, '完整 n = 0…255：256 次 C 呼叫全部返回 n + 1', 40)
    s.footer('這是另一個程式的返回要求，沒有把 guard 與迴圈串成因果')
    s.save()


def workflow():
    s = SVG('d5-official-proof-and-local-scope.svg', '官方證明驗收與本片本地檢查分開', '官方公開檢查器的順序：固定執行檔、待證命題及運作模型版本；AI產生候選證明；Rocq編譯時由核心檢查證明項；驗收檔核對指定型別並列出假設；最後以允許清單稽核假設。核心也檢查驗收檔的編譯。本片沒有執行官方檢查器。下方另列本片C程式實跑、命題SAT與獨立計數程式的有限控制圖。')
    s.heading('官方來源｜公開檢查流程', '先固定命題，再驗收交回的證明')
    names = [('固定對象', ['固定執行檔', '待證命題', '運作模型版本']), ('AI 產生', ['候選證明', '仍須通過檢查']), ('Rocq 編譯', ['核心查證明項', '編譯時進行']), ('驗收檔', ['對指定型別', '列出假設']), ('假設稽核', ['核對允許清單', '全通過才接受'])]
    for i, (title, labels) in enumerate(names):
        x = 80 + 294 * i
        s.rect(x, 245, 264, 245, WHITE, INK, sw=3)
        s.text(x + 132, 307, title, 40, INK, 800, 'middle')
        s.lines(x + 132, 377, labels, 36, anchor='middle', leading=49)
        if i < 4:
            s.arrow(x + 270, 360, x + 288, 360, width=3)
    s.text(80, 552, '此公開版本：保證指定行為相符；未證明一定結束', 40, RED, 700)
    s.text(80, 610, '候選證明與驗收檔編譯時，核心都檢查證明項；本片未執行官方檢查器', 36)
    for x, labels in [(80, ['本片實跑：GCC', '各 256 個輸入']), (570, ['本片實跑：命題 SAT', '接受判斷的兩方向查詢']), (1060, ['本片實跑：控制圖', '獨立計數程式返回'])]:
        s.rect(x, 655, 460, 118, PALE, RULE)
        s.lines(x + 24, 704, labels, 36, leading=46)
    s.text(80, 821, '官方來源：README／origin／checking／statements，2026-10-25查核', 36)
    s.text(80, 875, SOURCE, 36)
    s.save()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-dir')
    ap.add_argument('--render', action='store_true')
    args = ap.parse_args()
    data = source_dir(args.data_dir)
    facts = evidence(data)
    facts['official_scope'] = {'kind': 'CITED checker workflow, not rerun', 'urls': [OFFICIAL + f for f in ['README.md', 'docs/origin.md', 'docs/checking.md', 'docs/statements.md']], 'agreement_is_not_halts': True, 'checker_checks_in_order': ['Rocq compilation checks proof terms in the kernel', 'wrapper compilation also checks terms in the kernel and has the required fixed statement type', 'Print Assumptions lists dependencies', 'allowlist audit refuses unexpected assumptions'], 'source_snapshot_sha256': cited_snapshot_hashes()}
    facts['public_data_directory'] = 'https://github.com/x812033727/travel_scanner/tree/9c65d31a80ac9622676db460c9ed3d52716b6496/docs/videos/claude-formal-verification-255/data'
    facts['public_link_verification'] = 'Directory / actual raw source-file checks supplied by root; this asset generator makes no network calls.'
    (HERE / 'diagram-facts.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n')
    opening(); guard(); contract(facts); cycle(); exit_loop(); workflow()
    svgs = sorted(HERE.glob('d*.svg'))
    if args.render:
        for p in svgs:
            subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(p), '-frames:v', '1', str(p.with_suffix('.png'))], check=True)
    manifest = {'created_on': '2026-10-25', 'original': True, 'dimensions': [1600, 900], 'minimum_text_px': 36, 'palette': {'paper': PAPER, 'ink': INK, 'accent': RED}, 'renderer': 'ffmpeg librsvg', 'opening_spoilers': 'D0 contains only the observed acceptance of n255 and capacity8; no256/no0/no repair', 'local_source': SOURCE, 'input_sha256': facts['inputs'], 'files': {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'diagram-manifest.json'}, 'map': {'D0': ['d0-opening-guard.svg'], 'D1': ['d1-guard-narrowing-and-fix.svg'], 'D2+D3': ['d2-full-domain-and-two-directions.svg'], 'D4': ['d4-independent-loop-cycle.svg', 'd4-independent-loop-exit.svg'], 'D5': ['d5-official-proof-and-local-scope.svg'], 'D6': 'root can reuse the native record table; no seventh SVG'}}
    manifest['reveal_notes'] = {'d0-opening-guard.svg': 'Opening-safe: no solution, no n+1 value and no valid acceptance interval.', 'd1-guard-narrowing-and-fix.svg': 'Contains both the counterexample and the repair; show the complete diagram only after the repair is narrated.', 'd2-full-domain-and-two-directions.svg': 'Contains deny-all false rejection 8; use after the functional direction is revealed. Earlier 9/8-only results can use native cards.', 'd4-independent-loop-cycle.svg': 'A different, independent program. Do not draw an incoming arrow from the guard.', 'd4-independent-loop-exit.svg': 'Both the counter declaration and update cast change; never present declaration-only repair.', 'd5-official-proof-and-local-scope.svg': 'Cited official workflow, not a vendor rerun. Kernel checks terms in both proof and wrapper compilation; allowlist audit follows Print Assumptions.'}
    (HERE / 'diagram-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'diagrams': len(svgs), 'rendered': args.render, 'facts_from': str(data), 'accept_counts': [9, 8, 0], 'fixed_loop_returns': 256}))


if __name__ == '__main__':
    main()
