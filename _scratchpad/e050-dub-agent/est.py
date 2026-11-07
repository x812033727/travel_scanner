import json,os,re,sys
R='/home/user/travel_scanner/docs/videos/zhong-tian-qu-qi-e050'
W=os.path.expanduser('~/mokaair-work/videos/zhong-tian-qu-qi-e050-dh/segments-v4/lines')
RATE=dict(en=15,ja=5.5,ko=4.8,es=10,pt=9.5,id=10,vi=12.5,th=10.5)
v=json.load(open(R+'/video.json'))
lines=[l for s in v['scenes'] for l in s.get('lines',[])]
loc=sys.argv[1] if len(sys.argv)>1 else None
dub=json.load(open(f'{R}/dub.{loc}.json')) if loc and os.path.exists(f'{R}/dub.{loc}.json') else {}
for l in lines:
    f=f"{W}/{l['id']}.wav"
    zh=(os.path.getsize(f)-44)/(48000*4) if os.path.exists(f) else -1
    out=f"{l['id']} {zh:4.2f}s {l['speaker']:14} {l['text']}"
    if l['id'] in dub:
        d=dub[l['id']]; say=d.get('say',d['text'])
        n=len(re.sub(r"[\s…—,.!?;:'\"、。！？「」]","",say))
        est=0.6+n/RATE[loc]; flag='LONG' if est>zh*1.3+0.35 else ''
        out+=f" | {est:.1f} {flag} {say}"
    print(out)
