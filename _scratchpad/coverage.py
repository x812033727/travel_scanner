# coverage.py : every file under ~/mokaair-work/videos and the scratchpad is in some bk-list-*.tsv (so in some branch),
# except the pod token, the backup script's own temp repos, and the old season 1 episodes 43-55 (owner 2026-11-07:
# 「舊的第 43–55 集先不管了」).
import re
OLD = re.compile(r'zhong-tian-qu-qi-e0(4[3-9]|5[0-5])(/|$)')
import glob, os
V = os.path.expanduser('~/mokaair-work/videos'); S = os.path.dirname(os.path.abspath(__file__))
listed = set()
for f in glob.glob(f'{S}/bk-list-*.tsv'):
    listed |= {l.split('\t', 1)[0] for l in open(f, encoding='utf-8') if l.strip()}
miss = []
for root in (V, S):
    for d, _, names in os.walk(root):
        if d.startswith(f'{S}/h3r-state') or '/bk-' in d and d.split('/bk-')[1].split('/')[0].endswith('.git') or d.startswith(f'{S}/bk-split'): continue
        for n in names:
            p = os.path.join(d, n)
            if OLD.search(p): continue
            if p not in listed and not (p.startswith(S) and os.path.basename(p).startswith('bk-list-')): miss.append(p)
print(f'files not in any backup list: {len(miss)}')
for p in miss[:40]: print('  ', p)
