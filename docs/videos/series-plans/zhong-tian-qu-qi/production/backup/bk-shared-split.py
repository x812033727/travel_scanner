#!/usr/bin/env python3
"""bk-shared-split.py live|cg : the cross-episode files, split between transfer/zt-shared (live action and what both
versions use) and transfer/zt-cg-shared (the 3D CG era), owner 2026-11-08: 「照你的建議拆分支」.
Live action began with the first screen test, 2026-11-07 12:11 UTC (CUT). A scratchpad folder or loose file whose files
all predate CUT is CG; one that starts after it is live; one that straddles it goes to both (the same blobs twice cost
nothing on GitHub, and nothing can fall between the two). Both versions use: sound effects, music, the scripts.
Left out of both, with the owner's leave (2026-11-08): scratchpad/wv, the Python packages faster-whisper was installed
into (reinstalled with pip in a minute); and as before the pod token (h3r-state) and this script's temp repos.
"""
import os, sys, datetime
which = sys.argv[1]
V = os.path.expanduser('~/mokaair-work/videos')
S = os.path.dirname(os.path.abspath(__file__))
CUT = datetime.datetime(2026, 11, 7, 12, 0, tzinfo=datetime.timezone.utc).timestamp()
out = set()
def files(d):
    for r, ds, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            if os.path.isfile(p) and not os.path.islink(p): yield p
def put(paths, rel_root, rel_prefix):
    for p in paths: out.add((p, rel_prefix + os.path.relpath(p, rel_root)))
def era(paths):
    t = [os.path.getmtime(p) for p in paths]
    if not t: return 'both'
    return 'cg' if max(t) < CUT else 'live' if min(t) >= CUT else 'both'
want = lambda e: e == 'both' or e == which
Z = f'{V}/_series/zhong-tian-qu-qi'
SER = {'sfx': 'both', 'music': 'both', 'refs-dh': 'cg', 'refs-paint-e044': 'cg', 'portrait-redraws-20261107': 'cg'}
for name in sorted(os.listdir(Z)):
    e = SER.get(name, 'live' if name.startswith('live') else None)
    if e is None: e = era(list(files(f'{Z}/{name}')))
    if want(e): put(files(f'{Z}/{name}'), V, '')
for d in (f'{V}/_live-pilot',):
    if which == 'live': put(files(d), V, '')
for d in (f'{V}/zhong-tian-qu-qi-compilations',):
    if which == 'cg': put(files(d), V, '')
put(files(f'{V}/_scratchpad-scripts'), V, '')                       # my scripts: both
for name in sorted(os.listdir(V)):
    if name.startswith('zhong-tian-qu-qi-e9') and os.path.isdir(f'{V}/{name}/music'):
        put(files(f'{V}/{name}/music'), V, '')                       # each episode's music: both
for name in sorted(os.listdir(V)):
    p = f'{V}/{name}'
    if os.path.isfile(p) and want(era([p])): out.add((p, name))
SKIP = ('h3r-state', 'wv', 'bk-split')
for name in sorted(os.listdir(S)):
    p = f'{S}/{name}'
    if name in SKIP or name.startswith('bk-split') or (name.startswith('bk-') and name.endswith('.git')): continue
    if os.path.islink(p): continue
    if os.path.isdir(p):
        fs = list(files(p))
        if want(era(fs)): put(fs, S, '_scratchpad/')
    elif os.path.isfile(p):
        e = 'both' if name.endswith(('.py', '.sh', '.mjs', '.md')) else era([p])
        if want(e): out.add((p, f'_scratchpad/{name}'))
for p, rel in sorted(out):
    print(f'{p}\t{rel}')
