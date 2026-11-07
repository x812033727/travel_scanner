# usage: set.py LOC 'id|say|emotion' ...   (empty field = unchanged; say '-' = remove say)
import json,sys
V='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e051/'
loc=sys.argv[1]; p=V+'dub.%s.json'%loc
d=json.load(open(p,encoding='utf-8'))
for a in sys.argv[2:]:
  i,s,e=(a.split('|')+['',''])[:3]
  if s=='-': d[i].pop('say',None)
  elif s: d[i]['say']=s
  if e: d[i]['emotion']=e
  if d[i].get('say')==d[i]['text']: d[i].pop('say')
  # keep key order text, emotion, say
  d[i]={k:d[i][k] for k in ('text','emotion','say') if k in d[i]}
open(p,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('ok',loc)
