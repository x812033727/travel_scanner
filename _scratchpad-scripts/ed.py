# ed.py <locale> id say|- [emotion]
import json,sys
p=f'/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e045/dub.{sys.argv[1]}.json'
d=json.load(open(p))
a=sys.argv[2:]
for i in range(0,len(a),3):
    k,s,e=a[i],a[i+1],a[i+2]
    if s!='-': d[k]['say']=s
    if e!='-': d[k]['emotion']=e
    if d[k].get('say')==d[k]['text']: del d[k]['say']
    # keep key order text, emotion, say
    d[k]={x:d[k][x] for x in ('text','emotion','say') if x in d[k]}
open(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
