# usage: python3 build.py <locale> < tsv  (id \t text \t say(optional) \t emotion override(optional))
import json,sys
loc=sys.argv[1]
v=json.load(open('/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e046/video.json'))
lines=[l for s in v['scenes'] for l in s.get('lines',[])]
rows={}
for raw in sys.stdin.read().splitlines():
    if not raw.strip(): continue
    p=raw.split('\t')
    rows[p[0]]=p
out={}
for l in lines:
    p=rows[l['id']]
    e={"text":p[1].strip(),"emotion":l['emotion']}
    if len(p)>2 and p[2].strip(): e["say"]=p[2].strip()
    if len(p)>3 and p[3].strip(): e["emotion"]=p[3].strip()
    out[l['id']]=e
assert len(rows)==len(lines), (len(rows),len(lines))
open('/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e046/dub.%s.json'%loc,'w').write(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('wrote',loc,len(out))
