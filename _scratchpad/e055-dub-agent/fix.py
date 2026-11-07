# usage: python3 fix.py <locale> <id> say="..." emotion="..."   (edits dub.<locale>.json in place)
import json, sys
p=f'/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e055/dub.{sys.argv[1]}.json'
d=json.load(open(p)); e=d[sys.argv[2]]
for kv in sys.argv[3:]:
    k,v=kv.split('=',1); e[k]=v
if e.get('say')==e['text']: e.pop('say')
d[sys.argv[2]]={k:e[k] for k in ('text','emotion','say') if k in e}
open(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n'); print(sys.argv[2],d[sys.argv[2]])
