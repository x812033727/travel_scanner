#!/usr/bin/env bash
# e933 成片（真人版第一版）：照 e932cut.sh。剪接表 hailuo/edit-dh-e933-live.json 由 scratchpad e933c/（mkov933.py＋music／beds／spots.json → overrides.json，
# mkedit933.py＋note.txt → 剪接表）產生；所有決定與量測寫在剪接表的 _note。本腳本不花錢：不用 Colab、RunPod、站台 TTS，不重做精修。
set -u
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e933/zhong-tian-qu-qi-e933-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e033-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e933-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e933-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# 精修片由 live-action/stage.py 33 放好（精修畫面＋草稿原聲＋剪點 -> clips/sNN-t1.mp4；s01 s03 s05 s07 s22 s33 s35 s36 是 fix1、s34 是 fix2 9331313 的精修）；
# 缺片或 picks.json 比片新（重跑過 refine-prep.py 33）就重跑。stage.py 把 $E/audio、$E/music 連到 zhong-tian-qu-qi-e933-dh/audio、music；
# music/ 是一個目錄（e933 第一版手做，同 e932）：_series/zhong-tian-qu-qi/music 的 cue-*.mp3 各一個連結，cue-drone31／tension31／comedy31.mp3 ->
# assets/music/e031-e032/cue-suspense／tension／comedy.mp3，另 cue-imperial-court／farming-montage／scheming／farewell／night-village.mp3 ->
# _series/zhong-tian-qu-qi/music/flow-music-20261118/zhongtian-bed-<名>-take1.m4a（Flow Music 庫，ffmpeg 照內容讀，副檔名不影響）。
# 沒有片段帶 crop（s21 s25 的靜態裁切、s40 淡出都是剪接表的 vf）。
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 33 || exit 1; }
# REVIEW 3 s34（review3-plan.md〈2〉）：放好的 s34-t1.mp4（0–6.750）改速——第 0–6 格原速、第 7–124 格（c0.29–5.17，輪子轉的那段）
# setpts÷2.5 再 fps=24 抽格（不補格、不 minterpolate）、第 125 格（停死）起原速，共 91 格 3.792 秒；原檔移到 clips-src/s34-t1.mp4（不能留在 clips/：assemble-v4 會挑到它）。
# 聲音取原檔前 3.792 秒的水聲（片中聲音照例靜音，剪接表另放 water-s34a）。stage.py 重放過（s34-t1.mp4 比 .sped 新）就重做。
if [ ! -f $E/clips/s34-t1.sped ] || [ $E/clips/s34-t1.mp4 -nt $E/clips/s34-t1.sped ]; then
  mkdir -p $E/clips-src; mv $E/clips/s34-t1.mp4 $E/clips-src/s34-t1.mp4 || exit 1
  ffmpeg -nostdin -v error -y -i $E/clips-src/s34-t1.mp4 -filter_complex "[0:v]split=3[a][b][c];[a]trim=start_frame=0:end_frame=7,setpts=PTS-STARTPTS[a1];[b]trim=start_frame=7:end_frame=125,setpts=(PTS-STARTPTS)/2.5,fps=24[b1];[c]trim=start_frame=125:end_frame=162,setpts=PTS-STARTPTS[c1];[a1][b1][c1]concat=n=3:v=1:a=0,fps=24,format=yuv420p[v];[0:a]atrim=0:3.7917,asetpts=PTS-STARTPTS[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset fast -c:a aac -b:a 192k $E/clips/s34-t1.mp4 || exit 1
  touch $E/clips/s34-t1.sped
fi
[ -d /root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/music ] || { echo "zhong-tian-qu-qi-e933-dh/music/ 不在（見上面的說明）"; exit 1; }
# 本集自己的音效（剪接表 sfx_dirs 第二個目錄 $E/sfx-local/）：s33、s34 片中的水聲。s33 的片中原聲因石木匠的聲音太高整支靜音（voice_off），
# 水聲從放好的片子 c4.40 起切出來（淡入 0.3 秒）放回去；s34 沒有台詞、片中聲音照例靜音，整支 7.5 秒的水聲也切出來放回去，s35–s40 再循環當鋪底。
# 片子重放過或檔不在就重切。
mkdir -p $E/sfx-local
# REVIEW 3：s33 起點 0.125 → 3.875，同一段水聲（原片 4.525 起）在新的 c0.65。s34 的整段水聲（鋪底循環用）從改速前的 clips-src/s34-t1.mp4 切（6.75 秒），
# s34 本鏡用 water-s34a（改速後鏡長 3.792 秒）。
[ $E/sfx-local/water-s33.wav -nt $E/clips/s33-t1.mp4 ] || ffmpeg -nostdin -v error -y -ss 0.65 -i $E/clips/s33-t1.mp4 -vn -ac 2 -ar 48000 -af "afade=t=in:d=0.3" $E/sfx-local/water-s33.wav || exit 1
[ $E/sfx-local/water-s34.wav -nt $E/clips-src/s34-t1.mp4 ] || ffmpeg -nostdin -v error -y -i $E/clips-src/s34-t1.mp4 -vn -ac 2 -ar 48000 $E/sfx-local/water-s34.wav || exit 1
[ $E/sfx-local/water-s34a.wav -nt $E/clips/s34-t1.mp4 ] || ffmpeg -nostdin -v error -y -i $E/clips/s34-t1.mp4 -vn -ac 2 -ar 48000 $E/sfx-local/water-s34a.wav || exit 1
# 剪接表假設的剪點與種子（picks.json 由 colab/runs/e933-live 的 refine-prep.py 33 picks-merged.tsv fix1/review-picks.tsv
# fix2/review-picks.tsv cut-trims.tsv review3-trims.tsv fix3/review-picks.tsv 產生；印出的 refine 沒跑；REVIEW 3 起 fix3 的 s05 9331411、s30 9331414
# 由 scratchpad e933refine.sh ONLY=s05,s30 精修過，其他 38 鏡的精修不動）。cut-trims.tsv 是第一版剪接改的剪點：s30 終點 10.125→8.125
# （8 秒後手離開葉板、葉板明顯移動；開閘前輪子不能轉，挑片 B 交代「明顯就剪短到兩句放得下」）；s16 終點 10.125→7.5、
# s17 6.542→4.5（run1 句後空 3.43／3.17 秒）。review3-trims.tsv 是 REVIEW 3 的 8 刀（s01 s13 s16 s25 s29 s32 s33 s34，見 review3-plan.md〈1〉），
# fix3/review-picks.tsv 換 s05（0.125–4.458）與 s30（0–8.125）。
# 整格：起點往下、終點往上取到小數三位，容差 0.001；只警告不停。
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.0,5.0),'s02':(0.75,8.0),'s03':(0.5,8.0),'s04':(0.75,8.0),'s05':(0.125,4.458),'s06':(1.0,6.917),'s07':(0.25,6.125),'s08':(2.0,10.083),'s09':(1.0,7.833),'s10':(0.375,7.583),'s11':(1.25,7.75),'s12':(0.0,4.625),'s13':(0.875,5.167),'s14':(1.25,6.583),'s15':(1.0,6.583),'s16':(0.0,7.083),'s17':(0.0,4.5),'s18':(1.125,6.542),'s19':(0.0,4.583),'s20':(0.0,8.0),'s21':(1.125,7.917),'s22':(0.75,6.542),'s23':(0.75,6.583),'s24':(0.0,6.542),'s25':(0.5,5.875),'s26':(0.375,7.833),'s27':(1.5,7.5),'s28':(0.5,6.583),'s29':(0.875,5.25),'s30':(0.0,8.125),'s31':(1.125,7.917),'s32':(1.25,4.0),'s33':(3.875,8.0),'s34':(0.0,6.75),'s35':(0.75,8.0),'s36':(0.875,8.0),'s37':(3.0,6.583),'s38':(0.75,7.917),'s39':(0.0,8.0),'s40':(0.0,8.0)}
seed={'s01':9331211,'s03':9331211,'s05':9331411,'s07':9331212,'s15':9331102,'s18':9331102,'s19':9331102,'s21':9331102,'s22':9331211,'s24':9331102,'s25':9331102,'s30':9331414,'s31':9331102,'s33':9331211,'s34':9331313,'s35':9331212,'s36':9331212,'s37':9331102,'s38':9331102,'s39':9331102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9331101)' for s in p if s not in seed and p[s]['seed']!=9331101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# 剪接表鋪的錄音在 audio/ 改寫過（原檔在 audio/orig/；_note〈錄音〉）：整平到 −13.5 LUFS 的 a04 a12 a13 a17 a20 a32 a33 a38、
# a28（來源 zq933a28-p85.wav）、a35（來源 zq933a35-p119.wav），系統 a07 a16 a31 到 −13.7。少了改寫就停。
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e933-dh/audio
for n in 04 07 12 13 16 17 20 28 31 32 33 35 38; do [ -f $A/orig/zq933a$n.wav ] || { echo "audio/zq933a$n.wav is not the leveled file (no orig/ copy)"; exit 1; }; done
# e933 沒有拿掉的鏡（DROP 空，40 鏡全用）；$VL 是 video.json 去掉 DROP 的鏡。
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos nice node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e033-r2/overlays.json $P/hailuo/edit-dh-e933-live.json $E $E/cut/e933-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e933-live.mp4 ] || exit 1
# loudnorm2 之前的取樣峰值限制器（e923 起 limit 0.55、attack 8 ms），聲音最後 1.0 秒淡出（結尾 s40 淡出後的黑畫面）。
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e933-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e933-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e933-live.lim.mp4 && mv $E/cut/e933-live.lim.mp4 $E/cut/e933-live.mp4
ffmpeg -hide_banner -i $E/cut/e933-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e933-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e933-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
