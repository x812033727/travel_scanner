#!/usr/bin/env python3
"""Join zhong-tian live e001-e030 with no end black: each episode is cut where its final fade to black starts
(a held picture keeps at most 1.0 s; never before the last line ends + 0.3 s), cuts.json from cuts.py. Each
trimmed episode is encoded once (x264 crf 16, identical settings, so the parts are stream-copied together);
audio of each part gets a 0.15 s fade-out at the cut and a 0.05 s fade-in. Captions and chapters follow."""
import json, re, subprocess
from pathlib import Path
D=Path('/root/mokaair-work/review-zt/deliver'); C=json.load(open('cuts.json')); fr=24.0
eps=sorted(C); Path('parts').mkdir(exist_ok=True)
starts=[]; t=0.0
for e in eps:
    cut=C[e]['cut']; out=Path('parts')/f'{e}.mp4'; starts.append(t)
    if not out.exists():
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(D/e/'final.mp4'),'-t',f'{cut:.4f}',
          '-vf','setpts=PTS-STARTPTS','-af',f'aresample=async=1:first_pts=0,apad,atrim=0:{cut:.4f},afade=t=in:d=0.05,afade=t=out:st={cut-0.15:.4f}:d=0.15,asetpts=N/SR/TB',
          '-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-r','24','-g','48','-c:a','aac','-b:a','192k','-ar','48000','-ac','2',
          str(out)+'.tmp.mp4'],check=True)
        Path(str(out)+'.tmp.mp4').rename(out)
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(out)],capture_output=True,text=True).stdout)
    C[e]['part_seconds']=d; t+=d
    print(e, round(cut,3), round(d,3), flush=True)
Path('parts.txt').write_text(''.join(f"file 'parts/{e}.mp4'\n" for e in eps))
NAME='種田娶妻打天下-重製版-第1-30集'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','parts.txt','-c','copy','-movflags','+faststart',NAME+'.mp4'],check=True)
def ts(x):
    ms=round(x*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000); return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
def pt(s):
    h,m,r=s.split(':'); sec,ms=r.split(','); return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
cues=[]; k=1
for e,st in zip(eps,starts):
    cut=C[e]['cut']
    for blk in re.split(r'\n\s*\n',(D/e/'zh-TW.srt').read_text(encoding='utf-8-sig').strip()):
        L=blk.splitlines(); i=next(j for j,x in enumerate(L) if '-->' in x)
        a,b=[pt(p.strip()) for p in L[i].split('-->')]
        if a>=cut: continue
        cues.append(f'{k}\n{ts(a+st)} --> {ts(min(b,cut)+st)}\n'+'\n'.join(L[i+1:])); k+=1
Path(NAME+'.zh-TW.srt').write_text('\n\n'.join(cues)+'\n',encoding='utf-8')
ch=[]
for n,(e,st) in enumerate(zip(eps,starts),1):
    title=json.loads((D/e/'meta.json').read_text(encoding='utf-8'))['title'].split('｜')[0].strip()
    s=int(st); h,r=divmod(s,3600); m,sec=divmod(r,60); ch.append(f'{h}:{m:02d}:{sec:02d} 第{n}集 {title}')
Path('chapters.txt').write_text('\n'.join(ch)+'\n',encoding='utf-8')
json.dump({'episodes':[{'ep':e,'start':round(st,3),'cut_at':C[e]['cut'],'removed_tail':C[e]['removed'],'part_seconds':round(C[e]['part_seconds'],3)} for e,st in zip(eps,starts)],'total_seconds':round(t,3)},open('timeline.json','w'),indent=1)
print('total',round(t,2),'cues',k-1)
