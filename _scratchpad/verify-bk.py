import subprocess,sys,os
# verify-bk.py BRANCH DIR... : every non-rebuildable file under ~/mokaair-work/videos/DIR is in transfer/BRANCH with the same blob hash
V=os.path.expanduser('~/mokaair-work/videos'); br=sys.argv[1]; dirs=sys.argv[2:]
R='/home/user/travel_scanner'
subprocess.run(['git','fetch','-q','--depth=1','--filter=blob:none','origin',f'+refs/heads/transfer/{br}:refs/bkcheck/{br}'],cwd=R,check=True)
tree={}
for line in subprocess.run(['git','ls-tree','-r',f'refs/bkcheck/{br}'],cwd=R,capture_output=True,text=True).stdout.splitlines():
    meta,path=line.split('\t',1); tree[path]=meta.split()[2]
miss=bad=ok=0; parts=0
for d in dirs:
    for root,_,files in os.walk(os.path.join(V,d)):
        for f in files:
            full=os.path.join(root,f); rel=os.path.relpath(full,V)
            if any(x in rel for x in ('/clips/','/segments-v4/')) or (('/cut/' in rel) and rel.endswith('.mp4')) or ('/review/' in rel and rel.endswith(('.mp4','.jpg','.png'))): continue
            if os.path.getsize(full)>95_000_000:
                ps=[k for k in tree if k.startswith(rel+'.part')]
                if ps: parts+=1; ok+=1
                else: miss+=1; print('MISSING(split)',rel)
                continue
            h=subprocess.run(['git','hash-object',full],capture_output=True,text=True).stdout.strip()
            if rel not in tree: miss+=1; print('MISSING',rel)
            elif tree[rel]!=h: bad+=1; print('DIFF',rel)
            else: ok+=1
print(f'{br}: ok={ok} missing={miss} differ={bad} split={parts}')
