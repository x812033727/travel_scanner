# Series rule check (README §4 ≥4.4 chars/s, §10.6–10.8) for 原來如此事務所 episodes (README §4 pace, §10.6 pauses, BRANDING bookends).
import json,os,sys
R='/home/user/travel_scanner/docs/videos/'; W='/root/mokaair-work/videos/'
for slug in sys.argv[1:]:
  v=json.load(open(R+slug+'/video.json')); bad=[]
  chars=v.get('characters',{}); cv=[c.get('voice',{}) for c in (chars.values() if isinstance(chars,dict) else chars)]
  for vc in [v.get('voice',{})]+cv:
    if vc.get('provider','gemini')=='gemini' and '一秒五個字以上' not in vc.get('style',''): bad.append('style not fast: '+vc.get('name',''))
  if v.get('pauses')!={'line_ms':0,'scene_ms':150}: bad.append('pauses %s'%v.get('pauses'))
  if v.get('still_motion')!='beat': bad.append('still_motion %s'%v.get('still_motion'))
  lines=[l for s in v['scenes'] for l in s['lines']]
  extra=[l['id'] for l in lines if l.get('pause_after_ms') not in (None,500)]
  if extra: bad.append('pause_after_ms not beat: %d lines'%len(extra))
  hc=lambda t: sum(1 for ch in t if '\u4e00'<=ch<='\u9fff')
  tot=sum(hc(l['text']) for l in lines); kid=sum(hc(l['text']) for l in lines if l.get('speaker')=='kid')
  share=kid/tot if tot else 0
  if share>0.20: bad.append('kid share %.0f%% > 20%%'%(share*100))
  t=W+slug+'/timeline.json'; c=W+slug+'/checks.json'; info=''
  if os.path.exists(t):
    tl=json.load(open(t)); sec=sum(x.get('audio_samples',0) for x in tl.get('lines',[]))/48000
    han=sum(len([ch for ch in l['text'] if '一'<=ch<='鿿']) for l in lines)
    pace=han/sec if sec else 0; info+=' pace %.2f'%pace
    if pace and pace<4.4: bad.append('pace %.2f < 4.4'%pace)
    if os.path.exists(c):
      fr=json.load(open(c)).get('metrics',{}).get('frames'); d=(fr or 0)-tl.get('total_frames',0); info+=' bookend frames %s'%d
      if d!=987: bad.append('bookends missing (frames diff %s, want 987)'%d)
  print(slug, 'OK' if not bad else 'FAIL '+'; '.join(bad), info+' kid %.0f%%'%(share*100))
