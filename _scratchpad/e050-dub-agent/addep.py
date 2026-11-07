import json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from desc50 import D
B='/home/user/travel_scanner/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/youtube-locales'
for loc,desc in D.items():
    p=f'{B}/{loc}.json'; d=json.load(open(p,encoding='utf-8'))
    e=d['episodes']; t=e['49']['title']; assert t.count('49')==1
    e['50']={'title':t.replace('49','50'),'description':desc}
    d['episodes']=dict(sorted(e.items(),key=lambda kv:int(kv[0])))
    open(p,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(loc,e['50']['title'])
