#!/usr/bin/env python3
"""bk-cg-list.py N : the 3D CG era files of episode N for their own branch transfer/zt-cg-e00N (owner 2026-11-08:
「3D CG 時期的全部檔案就另外開分支吧 不要跟真人的混再一起」), as <absolute file>\t<path in the branch>.
- zhong-tian-qu-qi-e90N-dh without the live runs (runpod/live), the old voice versions (audio-old, audio-v1-ids),
  the edit intermediates (segments-v4) and music (in transfer/zt-shared): the CG drafts and refines (runpod/a), the CG
  clips, cut, first frames, review sheets and logs
- the recorded lines (audio/), which a CG re-cut needs as much as a live one (the same blobs as in the live branch)
- the CG cut sent to the admin before the live remake (import .../cg-old) and the r2 publish folder's CG review previews
"""
import os, sys
N = int(sys.argv[1]); V = os.path.expanduser('~/mokaair-work/videos'); EP = f'{N:03d}'
C = f'{V}/zhong-tian-qu-qi-e90{N}-dh'
skip = tuple(f'{C}/{d}' for d in ('runpod/live', 'audio-old', 'audio-v1-ids', 'segments-v4', 'music'))
out = set()
def tree(d, skip=()):
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if not any(os.path.join(root, x).startswith(s) for s in skip)]
        for x in files:
            p = os.path.join(root, x)
            if os.path.isfile(p) and not os.path.islink(p): out.add(p)
tree(C, skip)
tree(f'{V}/zhong-tian-qu-qi-import/zhong-tian-qu-qi-e{EP}-r2/cg-old')
tree(f'{V}/zhong-tian-qu-qi-e{EP}-r2')
for f in sorted(out):
    print(f'{f}\t{os.path.relpath(f, V)}')
