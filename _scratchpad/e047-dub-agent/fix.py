import json,sys
loc=sys.argv[1]; p=f'/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e047/dub.{loc}.json'
d=json.load(open(p))
for line in sys.stdin.read().strip().split('\n'):
  if not line.strip(): continue
  i,say,emo=[x.strip() for x in line.split('|')]
  i='zq47a'+i; e=d[i]
  if say=='-': e.pop('say',None)
  elif say: e['say']=say
  if emo: e['emotion']=emo
  d[i]={k:e[k] for k in ['text','emotion','say'] if k in e}
  if d[i].get('say')==d[i]['text']: d[i].pop('say')
open(p,'w').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
