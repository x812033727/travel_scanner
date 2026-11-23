#!/usr/bin/env python3
"""per episode: luma per frame over the last 14 s and first 4 s, black and freeze runs"""
import json, re, subprocess, sys
D='/root/mokaair-work/review-zt/deliver'
def lum(f, ss, t):
    r=subprocess.run(['ffmpeg','-v','error','-ss',str(ss),'-t',str(t),'-i',f,'-vf','scale=320:-2,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-','-f','null','-'],capture_output=True,text=True).stdout
    return [float(x) for x in re.findall(r'YAVG=([0-9.]+)', r)]
def freeze(f, ss):
    r=subprocess.run(['ffmpeg','-ss',str(ss),'-i',f,'-vf','freezedetect=n=0.003:d=0.4','-map','0:v','-f','null','-'],capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r'freeze_start: ([0-9.]+)',r)]; en=[float(x) for x in re.findall(r'freeze_end: ([0-9.]+)',r)]
    return [(round(a+ss,2), round((en[i] if i<len(en) else None) and en[i]+ss or 0,2)) for i,a in enumerate(st)]
out={}
for n in range(1,31):
    e=f'e0{n:02d}'; f=f'{D}/{e}/final.mp4'
    dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True).stdout)
    ss=max(0,dur-14); tail=lum(f,ss,14); head=lum(f,0,4)
    out[e]={'dur':dur,'tail_ss':ss,'tail':tail,'head':head,'freeze':freeze(f,ss)}
    # summary
    fr=24.0
    last_bright=max(i for i,v in enumerate(tail) if v>20) if any(v>20 for v in tail) else None
    first_bright=next((i for i,v in enumerate(head) if v>20),None)
    print(e, 'dur',round(dur,2),'head_black_s', None if first_bright is None else round(first_bright/fr,2),
          'tail_dark_from', None if last_bright is None else round(ss+(last_bright+1)/fr,2),
          'black_tail_s', None if last_bright is None else round(dur-(ss+(last_bright+1)/fr),2), 'freezes', out[e]['freeze'])
json.dump(out,open('probe.json','w'))
