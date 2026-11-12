#!/usr/bin/env bash
# 第 8 集：picks.txt（＋有重拍時 picks-hero.txt） → cut → v2/clips、takes、原聲（照 session-tools/assemble-v2.sh，但用工作用的 video/voice 副本）
set -e; W=$HOME/mokaair-work/videos/_tn-work; P=/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production
cd $W/e008-post; rm -rf cut cut-hero v2/clips v2/clips-plain v2/voice v2/segments-v4
python3 -I $P/session-tools/cut-picks.py picks.txt cut >/dev/null
[ -f picks-hero.txt ] && python3 -I $P/session-tools/cut-picks.py picks-hero.txt cut-hero >/dev/null
python3 - <<'PY'
import json,subprocess,os
W=os.path.expanduser('~/mokaair-work/videos/_tn-work'); E=W+'/e008-post'; V=E+'/v2'; os.makedirs(V+'/clips',exist_ok=True)
takes={}
for tj,cd in ((E+'/cut/takes.json',E+'/cut'),(E+'/cut-hero/takes.json',E+'/cut-hero')):
    if not os.path.exists(tj): continue
    for sid,t in json.load(open(tj)).items():
        off=max(0.0,t['window'][0]-t['from']); dur=t['window'][1]-t['window'][0]
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{off:.3f}','-t',f'{dur:.3f}','-i',f'{cd}/{sid}.mp4','-an','-c:v','libx264','-crf','14','-preset','fast',f'{V}/clips/{sid}-t1.mp4'],check=True)
        takes[sid]={'draft':t['draft'],'from':t['window'][0],'window_len':dur}
json.dump(takes,open(V+'/takes.json','w'),indent=1)
own=set(json.load(open('/home/user/travel_scanner/docs/videos/tai-nainai-e008/voice.json'))['own_voice']); v=json.load(open('/home/user/travel_scanner/docs/videos/tai-nainai-e008/video.json'))
shots={s['id'] for s in v['scenes'] if any(l['id'] in own for l in (s.get('lines') or []))}
json.dump({k:x for k,x in takes.items() if k in shots},open(V+'/takes-own.json','w'),indent=1)
e=json.load(open('/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post/edit-e008.json'))
for k,x in takes.items(): e['min'][k]=round(x['window_len'],3)
json.dump(e,open(V+'/edit.json','w'),ensure_ascii=False,indent=1); print(len(takes),'clips')
PY
# 門縫遮罩（c26、c28）
[ -f door-mask.png ] || python3 $P/session-tools/e008/door_mask.py door-mask.png
for c in c26 c28; do f=v2/clips/$c-t1.mp4; [ -f $f ] || continue; ffmpeg -v error -y -i $f -i door-mask.png -filter_complex '[0][1]overlay' -an -c:v libx264 -crf 14 -preset fast $f.m.mp4 && mv $f.m.mp4 $f; done
cd v2; mkdir -p clips-plain; for f in clips/*-t1.mp4; do ln -sf $PWD/$f clips-plain/$(basename $f -t1.mp4).mp4; done
ln -sfn $W/e008voice audio; ln -sfn $HOME/mokaair-work/videos/_series/tai-nainai/music music
python3 -I $P/post/voice.py --takes takes-own.json --clips clips-plain --out voice >/dev/null
mkdir -p $W/e008-post/v2/cut; cd /home/user/travel_scanner && VIDEO_WORKDIR=$HOME/mokaair-work/videos node $P/post/assemble-v4.mjs /home/user/travel_scanner/docs/videos/tai-nainai-e008/video.json - $W/e008-post/v2/edit.json $W/e008-post/v2 $W/e008-post/v2/cut/e008.mp4 > $W/e008-post/v2/cut.log 2>&1; echo "exit $?" >> $W/e008-post/v2/cut.log
tail -3 $W/e008-post/v2/cut.log
