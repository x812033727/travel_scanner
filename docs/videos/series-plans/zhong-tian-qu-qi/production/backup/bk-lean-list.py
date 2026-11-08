#!/usr/bin/env python3
"""bk-lean-list.py N : the files a re-cut of live episode N needs (owner 2026-11-08: 「只留重剪需要的 但不能漏」),
as <absolute file>\t<path in the branch>, paths relative to ~/mokaair-work/videos.
- picks.json and the live refine prompts (live-clips-e90N.json, st2 manifests and prompts): which take, trims, crops
- the 39 current refined pictures (refined/sNN.mp4; replaced takes in refined/v*/ are left out)
- the 39 picked drafts (their soundtrack is the model's voice) with their prompt and retake.json (to reshoot one shot)
- every recorded line (zhong-tian-qu-qi-e90N-dh/audio)
- the current cut (cut/*.mp4|srt|json|log, not cut/v*/) and the admin import folder without cg-old/
Music, sound effects and pictures are in transfer/zt-shared; scripts, prompts' sources and edit lists in the repo.
"""
import glob, json, os, sys
N = int(sys.argv[1]); V = os.path.expanduser('~/mokaair-work/videos'); EP = f'{N:03d}'
L = f'{V}/_live-e90{N}/zhong-tian-qu-qi-e90{N}-dh'; C = f'{V}/zhong-tian-qu-qi-e90{N}-dh'
out = set()
def add(f):
    f = os.path.realpath(f) if os.path.islink(f) else f
    if os.path.isfile(f): out.add(f)
def tree(d, skip=()):
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if not any(os.path.join(root, x).startswith(s) for s in skip)]
        for x in files: add(os.path.join(root, x))
picks = json.load(open(f'{L}/picks.json', encoding='utf-8'))
add(f'{L}/picks.json'); add(f'{L}/live-clips-e90{N}.json')
for f in glob.glob(f'{L}/runpod/a/st2/*.json') + glob.glob(f'{L}/runpod/a/st2/prompts/*') + glob.glob(f'{L}/runpod/a/st2/skip.txt'): add(f)
for shot, p in picks.items():
    r = f'{L}/runpod/a/st2/refined/{shot}.mp4'
    if not os.path.isfile(r): sys.exit(f'{shot}: no refined picture {r}')
    add(r); d = p['draft']; add(d)
    run = os.path.dirname(os.path.dirname(d)); name = os.path.basename(d)[:-4]
    add(f'{run}/prompts/ref-{name}.txt'); add(f'{run}/retake.json')
tree(f'{C}/audio')
for f in glob.glob(f'{L}/cut/*'): add(f)
# (the r2 publish folder holds only the CG-era review previews)
I = f'{V}/zhong-tian-qu-qi-import/zhong-tian-qu-qi-e{EP}-r2'; tree(I, skip=(f'{I}/cg-old',))
# owner 2026-11-08: also keep what may be wanted later — every draft of the live runs (the 93 not picked included) with
# their prompts, logs and progress; the replaced refines (refined/v*); pick sheets, logs and the st1/st2 copies.
# Left out: the CG-era files (their own branch, bk-cg-list.py), old voice versions, and the edit intermediates the tools
# rebuild (segments-v4/, cut/v*/).
tree(f'{C}/runpod/live')
# the clips that went into the cut are kept as well (DRAMA-BACKUP-BRANCHES.md: some are hand-cut and cannot be rebuilt)
tree(L, skip=(f'{L}/segments-v4', f'{L}/cut/v'))
for f in sorted(out):
    print(f'{f}\t{os.path.relpath(f, V)}')
