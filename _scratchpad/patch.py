# usage: patch.py <locale> then lines: id \t field \t value
import json,sys
loc=sys.argv[1]; f='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e046/dub.%s.json'%loc
d=json.load(open(f))
for raw in sys.stdin.read().splitlines():
    if not raw.strip(): continue
    i,k,val=raw.split('\t')
    if val=='-': d[i].pop(k,None)
    else: d[i][k]=val
    # keep key order text, emotion, say
    d[i]={kk:d[i][kk] for kk in ['text','emotion','say'] if kk in d[i]}
open(f,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('patched')
