# usage: patch.py loc 'id|say|emotion' ...   (empty field = unchanged; say '-' = remove)
import json,sys
loc=sys.argv[1]; p=f'/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e050/dub.{loc}.json'
d=json.load(open(p))
for a in sys.argv[2:]:
    i,say,emo=(a.split('|')+['',''])[:3]
    if say=='-': d[i].pop('say',None)
    elif say: d[i]['say']=say
    if emo: d[i]['emotion']=emo
    # keep key order text, emotion, say
    d[i]={k:d[i][k] for k in ('text','emotion','say') if k in d[i]}
open(p,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
