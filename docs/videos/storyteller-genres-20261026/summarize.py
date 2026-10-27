"""Filter and summarize two rounds of measure.py output into results.json.

Usage: python3 summarize.py round-a.json round-b.json results.json
measure.py and its round-B copy must sit next to this file as measure.py and
measure_b.py (round B = measure.py with GENRES set to results.json queries_b).
"""

import json, re, statistics, sys
from pathlib import Path
here = Path(__file__).parent
round_a, round_b, out = sys.argv[1:4]
han = re.compile(r'[一-鿿]'); kana = re.compile(r'[぀-ヿ가-힯]')
noise_t = re.compile(r'主題曲|主题曲|\bMV\b|歌詞|歌词|Lyric|Official (Music )?Video|官方MV|預告|预告|Trailer|演唱|翻唱|cover', re.I)
noise_c = re.compile(r'唱片|Records|Music|Oldies|音樂|音乐|華納兄弟|电影|電影', re.I)
keep = lambda r: len(han.findall(r['title'])) >= 6 and not kana.search(r['title']) and not noise_t.search(r['title']) and not noise_c.search(r['channel'])
A = json.load(open(round_a, encoding='utf-8'))['raw']
B = json.load(open(round_b, encoding='utf-8'))['raw']
q = {}
for name, src in (('a', here / 'measure.py'), ('b', here / 'measure_b.py')):
    s = open(src, encoding='utf-8').read(); ns = {}
    exec(s[s.index('GENRES = {'):s.index('PER_QUERY')], {}, ns); q[name] = ns['GENRES']
def st(v):
    v = sorted(v)
    return {"videos": len(v), "median": int(statistics.median(v)), "p75": int(statistics.quantiles(v, n=4)[2]), "over_1m": sum(x >= 1_000_000 for x in v)}
res = []
for g in A:
    a = [r for r in A[g] if keep(r)]; b = [r for r in B[g] if keep(r)]
    u = {r['id']: r for r in a + b}
    top = sorted(u.values(), key=lambda r: -r['views'])[:5]
    res.append({"genre": g, "queries_a": q['a'][g], "queries_b": q['b'][g],
                "round_a": st([r['views'] for r in a]), "round_b": st([r['views'] for r in b]),
                "union": dict(st([r['views'] for r in u.values()]), channels=len({r['channel'] for r in u.values()})),
                "union_without_laogao": st([r['views'] for r in u.values() if '老高' not in r['channel']]),
                "laogao_in_over_1m": sum(r['views'] >= 1_000_000 and '老高' in r['channel'] for r in u.values()),
                "top5": [{"id": r['id'], "views": r['views'], "minutes": round(r['seconds'] / 60, 1), "channel": r['channel'], "title": r['title']} for r in top]})
res.sort(key=lambda r: -r['union']['median'])
json.dump({"measured_at": "2026-10-26T13:20–13:36Z", "method": "README.md §4 量法",
           "filters": {"chinese_title": "至少 6 個漢字、沒有假名與韓文", "noise_title": noise_t.pattern, "noise_channel": noise_c.pattern, "min_seconds": 240},
           "rows_before_filter": {"round_a": sum(map(len, A.values())), "round_b": sum(map(len, B.values()))},
           "genres": res}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in res:
    a, b, u, n = r['round_a'], r['round_b'], r['union'], r['union_without_laogao']
    print(f"{r['genre']} | {u['median']:,} | {u['p75']:,} | {u['over_1m']} (老高 {r['laogao_in_over_1m']}) | A {a['median']:,} B {b['median']:,} | 去老高 {n['median']:,} | n={u['videos']}")
