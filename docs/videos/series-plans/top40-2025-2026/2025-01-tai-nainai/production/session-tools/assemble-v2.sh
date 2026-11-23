#!/usr/bin/env bash
# 種田拍法的成片：assemble-v2.sh <ep> <picks/cut 資料夾…>（每個資料夾有 cut/takes.json 與 refined/<鏡>.mp4 或 refined 在另一層）
# 片段 = 精修後的片段從「選定的起點」開始（精修片段是從 cut 的起點起，所以再剪掉 window[0]-from）；原聲 = 草稿從 window[0] 起的音軌。
set -uo pipefail; shopt -s nullglob
E=$1; shift
S=${TN_WORK:-$HOME/mokaair-work/videos/_tn-work}
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post
W=$S/$E-post/v2; rm -rf $W/clips $W/segments-v4 $W/voice; mkdir -p $W/clips $W/cut $W/voice-takes
python3 - $W "$@" <<'PY'
import json,subprocess,sys,os
W=sys.argv[1]; srcs=sys.argv[2:]; takes={}
for spec in srcs:   # spec = "<takes.json>:<refined dir>"
    tj,rd=spec.split(':')
    for sid,t in json.load(open(tj)).items():
        ref=os.path.join(rd,f'{sid}.mp4')
        if not os.path.exists(ref): print('missing refined',sid,ref); continue
        off=max(0.0,t['window'][0]-t['from'])
        dur=t['window'][1]-t['window'][0]  # 只用選定的那一段；片段裡選定範圍之後可能有硬切（第 1 集 c42）
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{off:.3f}','-t',f'{dur:.3f}','-i',ref,'-an','-c:v','libx264','-crf','14','-preset','fast',f'{W}/clips/{sid}-t1.mp4'],check=True)
        takes[sid]={'draft':t['draft'],'from':t['window'][0],'window_len':t['window'][1]-t['window'][0]}
json.dump(takes,open(f'{W}/takes.json','w'),indent=1); print(len(takes),'clips')
PY
rm -rf $W/clips-plain; mkdir -p $W/clips-plain; for f in $W/clips/*-t1.mp4; do ln -sf $f $W/clips-plain/$(basename $f -t1.mp4).mp4; done
ln -sfn $S/$E-post/audio $W/audio; ln -sfn $HOME/mokaair-work/videos/_series/tai-nainai/music $W/music
python3 - $W $R/docs/videos/tai-nainai-$E/voice.json $R/docs/videos/tai-nainai-$E/video.json <<'PY'
import json,sys
W,vj,vv=sys.argv[1:4]
own=set(json.load(open(vj))['own_voice']); v=json.load(open(vv))
shots={s['id'] for s in v['scenes'] if any(l['id'] in own for l in (s.get('lines') or []))}
t=json.load(open(f'{W}/takes.json')); json.dump({k:x for k,x in t.items() if k in shots},open(f'{W}/takes-own.json','w'),indent=1)
print(len(shots),'own-voice shots')
PY
python3 -I $P/voice.py --takes $W/takes-own.json --clips $W/clips-plain --out $W/voice || exit 1
# 剪接表的 min 不能比選定的那一段長（不然停格）：沒台詞的鏡改成選定長度，存一份到工作資料夾給這次合成用
python3 - $P/edit-$E.json $W <<'PY2'
import json,sys
e=json.load(open(sys.argv[1],encoding='utf-8')); t=json.load(open(sys.argv[2]+'/takes.json'))
for sid,x in t.items():
    w=x.get('window_len')
    if w and sid in e.get('min',{}) and e['min'][sid]>w: e['min'][sid]=round(w,3)
json.dump(e,open(sys.argv[2]+'/edit.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
PY2
cd $R && node $P/assemble-v4.mjs docs/videos/tai-nainai-$E/video.json - $W/edit.json $W $W/cut/$E.mp4 > $W/cut/final.log 2>&1; echo "exit $?" >> $W/cut/final.log
tail -3 $W/cut/final.log; grep held $W/cut/final.log | head
A=$S/asm2038; V=$R/docs/videos/tai-nainai-$E/video.json
python3 -I $A/cut-qa.py $W/cut --stem $E | grep -v "^ok"; python3 -I $A/cut-jumps.py $W/cut | tail -2; python3 -I $A/audio-qa.py $W/cut $V | grep -v "^note"
python3 -I $A/continuity-sheets.py $W/cut $V $W/cont | tail -3
