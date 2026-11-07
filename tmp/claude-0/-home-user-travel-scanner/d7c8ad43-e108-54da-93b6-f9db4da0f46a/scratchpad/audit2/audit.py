import os, sys, subprocess, hashlib, json, re, fnmatch, collections, stat
REPO="/home/user/travel_scanner"
S="/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad"
ROOTS=[S,"/root/mokaair-work/videos/_series/tai-nainai","/root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx","/root/mokaair-work/videos/tai-nainai-import"]
BR=["tn-e001-work","tn-e002-work","tn-e003-work","tn-series-assets"]
PART=94371840
def git(*a): return subprocess.run(["git","-C",REPO,*a],capture_output=True,check=True).stdout.decode()
ctime={}; tree={}  # path -> list of (branch,mode,sha)
for b in BR:
    ref="origin/transfer/"+b
    ctime[b]=int(git("log","-1","--format=%ct",ref).strip())
    out=subprocess.run(["git","-C",REPO,"ls-tree","-r","-z",ref],capture_output=True,check=True).stdout.decode()
    for ent in out.split("\0"):
        if not ent: continue
        meta,p=ent.split("\t",1); mode,_,sha=meta.split()
        tree.setdefault(p,[]).append((b,mode,sha))
def owner(full):
    if full.startswith(S+"/"):
        r=full[len(S)+1:]
        m=re.match(r"(?:own/)?(e00[123])(?:-post)?(/|$)",r)
        if m: return "tn-"+m.group(1)+"-work"
        if r.startswith("pilot/"): return "tn-e001-work"
    return "tn-series-assets"
def bh(data): return hashlib.sha1(b"blob %d\0"%len(data)+data).hexdigest()
def fhash(full):
    h=hashlib.sha1(); n=os.path.getsize(full); h.update(b"blob %d\0"%n)
    with open(full,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()
res=[]; emptydirs=[]; other=[]
for root in ROOTS:
    for dp,dns,fns in os.walk(root,followlinks=False):
        if dp==S:
            dns[:]=[d for d in dns if not (fnmatch.fnmatch(d,"tn*.git") or fnmatch.fnmatch(d,"tn*-parts") or d=="audit2")]
        if root==S and (dp.startswith("/root/")): pass
        if not dns and not fns: emptydirs.append(dp)
        for n in fns+[d for d in dns if os.path.islink(os.path.join(dp,d))]:
            full=os.path.join(dp,n); rel=full.lstrip("/"); st=os.lstat(full)
            ents=tree.get(rel,[]); status=None; detail=""
            if stat.S_ISLNK(st.st_mode):
                tgt=os.readlink(full); th=bh(tgt.encode())
                status="ok" if any(m=="120000" and s==th for _,m,s in ents) else ("different" if ents else "missing")
                kind="link"
            elif stat.S_ISREG(st.st_mode):
                kind="file"
                if ents:
                    h=fhash(full)
                    status="ok" if any(m in("100644","100755") and s==h for _,m,s in ents) else "different"
                else:
                    parts=collections.defaultdict(dict)
                    for k in range(0,1000):
                        e=tree.get(f"{rel}.part{k:02d}")
                        if not e: break
                        for b,m,s in e: parts[b][k]=s
                    if not parts: status="missing"
                    else:
                        hs=[]
                        with open(full,"rb") as f:
                            for c in iter(lambda:f.read(PART),b""): hs.append(bh(c))
                        good=[b for b,d in parts.items() if len(d)==len(hs) and all(d.get(i)==h for i,h in enumerate(hs))]
                        status="ok" if good else "different"; detail="split:%d"%len(hs)
                        if good: ents=[(b,"split","") for b in good]
            else:
                other.append(full); continue
            ob=owner(full)
            if status!="ok" and st.st_mtime>ctime[ob]: status="after-backup"
            res.append(dict(root=root,path=full,kind=kind,status=status,owner=ob,mtime=st.st_mtime,size=st.st_size,branches=sorted({e[0] for e in ents}),detail=detail))
json.dump(dict(res=res,ctime=ctime,emptydirs=emptydirs,other=other),open(sys.argv[1],"w"))
c=collections.Counter((r["root"],r["status"]) for r in res)
for root in ROOTS: print(root, {k[1]:v for k,v in c.items() if k[0]==root})
print("empty dirs",len(emptydirs),"other",len(other))
