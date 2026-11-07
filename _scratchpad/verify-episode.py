# verify-episode.py BRANCH : every file bk-episode.sh listed for transfer/BRANCH (scratchpad/bk-list-BRANCH.tsv) is on the
# branch with the same content (git blob hash); a file over 95 MB is split into the same 90 MiB chunks and each compared.
# Also checks the list against the disk again, so a file added after the backup shows up as missing.
import os, subprocess, sys
br = sys.argv[1]; R = '/home/user/travel_scanner'
S = '/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad'
subprocess.run(['git', 'fetch', '-q', '--depth=1', '--filter=blob:none', 'origin', f'+refs/heads/transfer/{br}:refs/bkcheck/{br}'], cwd=R, check=True)
tree = {}
for line in subprocess.run(['git', 'ls-tree', '-r', f'refs/bkcheck/{br}'], cwd=R, capture_output=True, text=True).stdout.splitlines():
    meta, path = line.split('\t', 1); tree[path] = meta.split()[2]
pairs = [l.rstrip('\n').split('\t', 1) for l in open(f'{S}/bk-list-{br}.tsv', encoding='utf-8') if l.strip()]
CH = 90 * 1024 * 1024; ok = bad = 0; problems = []
for full, rel in pairs:
    if not os.path.exists(full): continue  # removed from disk since; the branch keeps it
    if os.path.getsize(full) > 95_000_000:
        good = True
        with open(full, 'rb') as fh:
            i = 0
            while chunk := fh.read(CH):
                h = subprocess.run(['git', 'hash-object', '--stdin'], input=chunk, capture_output=True).stdout.decode().strip()
                good &= tree.get(f'{rel}.part{i:02d}') == h; i += 1
    else:
        good = tree.get(rel) == subprocess.run(['git', 'hash-object', full], capture_output=True, text=True).stdout.strip()
    if good: ok += 1
    else: bad += 1; problems.append(rel)
print(f'{br}: listed={len(pairs)} ok={ok} missing_or_different={bad}')
for p in problems[:30]: print('  ', p)
sys.exit(1 if bad else 0)
