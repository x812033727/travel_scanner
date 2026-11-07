# audit-all.py : every file under ~/mokaair-work/videos (except what the tools rebuild for free) must exist, by content
# (git blob hash), in at least one transfer/* branch on GitHub. Prints what is not, grouped by folder.
import os, subprocess, collections
V = os.path.expanduser('~/mokaair-work/videos'); R = '/home/user/travel_scanner'
refs = [l.split()[1] for l in subprocess.run(['git', 'ls-remote', 'origin', 'refs/heads/transfer/*'], cwd=R, capture_output=True, text=True).stdout.splitlines()]
have = set(); split_parts = set()
for ref in refs:
    br = ref.split('refs/heads/')[1]
    subprocess.run(['git', 'fetch', '-q', '--depth=1', '--filter=blob:none', 'origin', f'+{ref}:refs/audit/{br}'], cwd=R, check=True)
    for line in subprocess.run(['git', 'ls-tree', '-r', f'refs/audit/{br}'], cwd=R, capture_output=True, text=True).stdout.splitlines():
        meta, path = line.split('\t', 1); have.add(meta.split()[2])
        if '.part' in path: split_parts.add(path.rsplit('.part', 1)[0])
skip = lambda rel: ('/clips/' in rel or '/segments-v4/' in rel or (('/cut/' in rel) and rel.endswith('.mp4'))
                    or ('/review/' in rel and rel.endswith(('.mp4', '.jpg', '.png'))) or rel.endswith('.log') and '/' not in rel)
files = []
for root, _, names in os.walk(V):
    for n in names:
        full = os.path.join(root, n); rel = os.path.relpath(full, V)
        if not skip(rel): files.append((full, rel))
out = subprocess.run(['git', 'hash-object', '--stdin-paths'], cwd=R, input='\n'.join(f for f, _ in files), capture_output=True, text=True).stdout.split()
missing = collections.defaultdict(list); big = 0
for (full, rel), h in zip(files, out):
    if h in have: continue
    if os.path.getsize(full) > 95_000_000 and rel in split_parts: big += 1; continue
    missing[rel.split('/')[0] + '/' + (rel.split('/')[1] if rel.count('/') > 1 else '')].append(rel)
print(f'{len(refs)} backup branches, {len(files)} files checked, {sum(map(len, missing.values()))} not in any backup')
for k, v in sorted(missing.items()):
    print(f'  {len(v):5d}  {k}  e.g. {v[0]}')
