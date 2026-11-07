import json,os,sys
R='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e050'
S=os.path.dirname(os.path.abspath(__file__))
v=json.load(open(R+'/video.json'))
lines=[l for s in v['scenes'] for l in s.get('lines',[])]
for loc in sys.argv[1:]:
    rows=open(f'{S}/src/{loc}.txt',encoding='utf-8').read().rstrip('\n').split('\n')
    assert len(rows)==len(lines),(loc,len(rows))
    out=f'{R}/dub.{loc}.json'
    old=json.load(open(out)) if os.path.exists(out) else {}
    d={}
    for l,r in zip(lines,rows):
        t,_,say=r.partition('|')
        e={'text':t.strip(),'emotion':old.get(l['id'],{}).get('emotion',l['emotion'])}
        if say.strip(): e['say']=say.strip()
        d[l['id']]=e
    open(out,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(loc,'written',sum('say' in x for x in d.values()),'say')
