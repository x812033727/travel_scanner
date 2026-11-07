# verify-episode.py N : every file episode N needs (same folders and skips as bk-episode.sh) is on transfer/zt-live-e00N
# with the same content (git blob hash); a file over 95 MB is split into the same 90 MiB chunks and each chunk compared.
import os, subprocess, sys
V = os.path.expanduser('~/mokaair-work/videos'); R = '/home/user/travel_scanner'
import glob
if sys.argv[1] == 'shared':
    br = 'zt-shared'; music = True
    dirs = ['_series/zhong-tian-qu-qi', '_live-pilot', '_scratchpad-scripts'] + [os.path.relpath(m, V) for m in sorted(glob.glob(f'{V}/zhong-tian-qu-qi-e9*-dh/music'))]
else:
    N = int(sys.argv[1]); EP = f'{N:03d}'; br = f'zt-live-e{EP}'; music = False
    dirs = [f'zhong-tian-qu-qi-e90{N}-dh'] + ([f'zhong-tian-qu-qi-e{EP}-r2'] if os.path.isdir(f'{V}/zhong-tian-qu-qi-e{EP}-r2') else [])
subprocess.run(['git', 'fetch', '-q', '--depth=1', '--filter=blob:none', 'origin', f'+refs/heads/transfer/{br}:refs/bkcheck/{br}'], cwd=R, check=True)
tree = {}
for line in subprocess.run(['git', 'ls-tree', '-r', f'refs/bkcheck/{br}'], cwd=R, capture_output=True, text=True).stdout.splitlines():
    meta, path = line.split('\t', 1); tree[path] = meta.split()[2]
def skipped(rel):
    return ('/clips/' in rel or '/segments-v4/' in rel or ('/cut/' in rel and rel.endswith('.mp4'))
            or ('/review/' in rel and rel.endswith(('.mp4', '.jpg', '.png'))) or rel[-7:-2] == '.part'
            or (not music and '/music/' in rel))
ok = bad = 0; problems = []
CH = 90 * 1024 * 1024
for d in dirs:
    for root, _, names in os.walk(os.path.join(V, d)):
        for n in names:
            full = os.path.join(root, n); rel = os.path.relpath(full, V)
            if skipped(rel): continue
            if os.path.getsize(full) > 95_000_000:
                with open(full, 'rb') as fh:
                    i = 0; good = True
                    while chunk := fh.read(CH):
                        h = subprocess.run(['git', 'hash-object', '--stdin'], input=chunk, capture_output=True).stdout.decode().strip()
                        if tree.get(f'{rel}.part{i:02d}') != h: good = False
                        i += 1
                if good: ok += 1
                else: bad += 1; problems.append(rel)
                continue
            h = subprocess.run(['git', 'hash-object', full], capture_output=True, text=True).stdout.strip()
            if tree.get(rel) == h: ok += 1
            else: bad += 1; problems.append(rel)
print(f'{br}: ok={ok} missing_or_different={bad}')
for p in problems[:30]: print('  ', p)
sys.exit(1 if bad else 0)
