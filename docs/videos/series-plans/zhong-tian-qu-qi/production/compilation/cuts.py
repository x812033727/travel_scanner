#!/usr/bin/env python3
import json, re, statistics
P=json.load(open('probe.json')); D='/root/mokaair-work/review-zt/deliver'; fr=24.0
def last_cue_end(e):
    t=0
    for a,b in re.findall(r'(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)', open(f'{D}/{e}/zh-TW.srt',encoding='utf-8-sig').read()):
        h,m,r=b.split(':'); s,ms=r.split(','); t=max(t,int(h)*3600+int(m)*60+int(s)+int(ms)/1000)
    return t
cuts={}
for e,p in P.items():
    ss,L,dur=p['tail_ss'],p['tail'],p['dur']
    # the fade is the final run where every frame is darker than the one before (or already black);
    # a cut to a darker shot is one step, not a ramp, so it is not taken for a fade (e008 s40)
    i=len(L)-1
    while i>0 and (L[i]<20 or L[i-1]-L[i]>0.15): i-=1
    i+=1
    fade=ss+i/fr
    held=[a for a,b in p['freeze'] if b==0]                   # a still frame that lasts to the end
    hold=dur
    if held:
        k=int(round((held[0]-ss)*fr)); k=min(max(k,0),len(L)-1)
        hold = held[0] if L[k] < 20 else held[0]+1.0           # black hold: cut at once; picture hold: keep 1.0 s
    cue=last_cue_end(e)
    cut=min(fade,hold,dur); cut=max(cut,cue+0.3)
    cut=round(round(cut*fr)/fr,4)
    cuts[e]={'cut':cut,'dur':round(dur,3),'removed':round(dur-cut,2),'fade':round(fade,2),'held':held[0] if held else None,'last_cue':round(cue,2)}
    print(e, cuts[e])
json.dump(cuts,open('cuts.json','w'),indent=1)
print('removed total', round(sum(c['removed'] for c in cuts.values()),1))
