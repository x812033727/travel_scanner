import hashlib, os, subprocess, sys, json, datetime
REPO="/home/user/travel_scanner"; PART=90*1024*1024
branch, base, commit_ts = sys.argv[1], sys.argv[2], float(sys.argv[3])  # base: prefix stripped ("/" or "/root/mokaair-work/videos/")
roots = sys.argv[4:]
tree={}
out=subprocess.run(["git","-C",REPO,"ls-tree","-r","-z",f"refs/remotes/audit/{branch}"],capture_output=True,check=True).stdout
for rec in out.split(b"\0"):
    if not rec: continue
    meta,p=rec.split(b"\t",1); mode,_,sha=meta.decode().split(); tree[p.decode()]=(mode,sha)
def bh(b): return hashlib.sha1(b"blob %d\0"%len(b)+b).hexdigest()
def fh(path):
    h=hashlib.sha1(b"blob %d\0"%os.path.getsize(path))
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()
res={"ok":0,"missing":[],"diff":[],"after":[],"skipped":{},"split":[],"local":0,"errors":[]}
covered=set()
for root in roots:
    def onerr(e): res["errors"].append(str(e))
    for dp,dn,fn in os.walk(root,onerror=onerr):
        keep=[]
        for d in dn:
            full=os.path.join(dp,d)
            why = "segments-v4" if d=="segments-v4" else "refs(top)" if (d=="refs" and dp==root) else "*.git" if d.endswith(".git") else None
            if why: res["skipped"][full]=why; continue
            if os.path.islink(full): fn.append(d); continue
            keep.append(d)
        dn[:]=keep
        for n in fn:
            full=os.path.join(dp,n); rel=full[len(base):]; res["local"]+=1
            st=os.lstat(full); late = st.st_mtime>commit_ts
            if os.path.islink(full):
                e=tree.get(rel); good = e and e[0]=="120000" and e[1]==bh(os.readlink(full).encode())
            elif os.path.isfile(full):
                e=tree.get(rel)
                if e: good = e[1]==fh(full); covered.add(rel)
                else:
                    parts=sorted(p for p in tree if p.startswith(rel+".part"))
                    if not parts: good=None
                    else:
                        good=True;k=0
                        with open(full,"rb") as f:
                            for c in iter(lambda:f.read(PART),b""):
                                pk=f"{rel}.part{k:02d}"
                                if tree.get(pk,("",""))[1]!=bh(c): good=False
                                k+=1
                        good = good and k==len(parts); res["split"].append((rel,len(parts)))
            else: res["errors"].append("special "+full); continue
            if good: res["ok"]+=1
            elif late: res["after"].append(("MISSING" if good is None else "DIFF")+" "+full)
            elif good is None: res["missing"].append(full)
            else: res["diff"].append(full)
print(json.dumps(res,ensure_ascii=False,indent=0))
