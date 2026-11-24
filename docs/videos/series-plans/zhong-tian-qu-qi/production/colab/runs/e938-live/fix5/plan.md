# 第 38 集真人版 fix5 重拍計畫（REVIEW 3 之後：s18 s19 s20 s29，加上換鞍連帶的 s30 s32）＋a22 重錄

fix5 準備代理 2026-11-24 寫。站主：「有問題就修，真的修不好再跟我講，品質比較重要。」
依據：`../review3-plan.md`（A13 s19 熊、A16 s18 走出院門、A18 s20 正面跑、A19 西式鞍、A20 a22「宵禁」）、`../cut-review.md`、`../cut-review-2.md`、
`../cut-notes.md` 的 REVIEW 3 一節（下一集的鞍句）、`../fix4/plan.md`（**fix4 正在跑，它的檔沒動**）、現在剪接用哪一支以 `../picks-final.tsv`＋`../review3-trims.tsv` 為準。
**本代理沒有送 Colab**、沒用 RunPod、沒付費圖、沒 commit、沒動第 37 集以前；只做 DRY／PRECHECK。站台 TTS 的事見〈a22 重錄〉。

## 重拍清單（6 鏡 12 支、76 秒）

種子 **9381701／9381702**。底稿是**現在剪接用的那一支實際送出的工作與提示詞**（`mkjobs.py` 核 sha256、底稿那一輪 `spec.json` 的每條修改都在底稿裡）：
s18 s19 s29 s30 s32 是 d1 9381101，s20 是 fix1 9381302。d1 的加圖（五個騎馬鏡的棗紅馬圖、s18 唐小棠的夜版雙丸子背影圖）照舊在最後、句子跟著，張數不變、表頭不動。
秒數照底稿（＝BUY）。每個替換在底稿裡剛好一次。

| 鏡 | 底稿 | 秒 × 支 | 問題 | 改什麼（英文原句在 `mkspec.py`） | 運鏡 |
|---|---|---|---|---|---|
| s18 | d1 9381101 | 8 × 2 | 馬是走出院門（剪接只能剪短＋疊快馬蹄） | 馬**第一格就在全速跑**、從背後偏側面看、由右往院門**空著的左半**衝出去（門扇掛右柱往內半開，左半就是開著的路）；動作「全速穿過門洞左半、蹄聲重、不減速、阿令伏在馬頸上」；拿掉「肩膀撞門扇」（衝左半碰不到門扇）；唐小棠照 d1：背影、雙丸子、頭不動、背影圖在最後；換鞍 | 固定 |
| s19 | d1 9381101 | 8 × 2 | 床前半空浮著一隻布偶熊（稿子寫的是「枕邊一隻草兔子」） | 草兔子**只寫一次**、寫成實物：「一隻手掌大、扁扁的、淡色乾草編的兔子，躺在枕頭上、貼著她的臉頰」；**不寫別的玩偶、也不寫『沒有熊』**；燭光句加「房裡唯一的一朵火」；全身、雙膝著地照 d1 | 固定（推鏡會把膝蓋推出框） |
| s20 | fix1 9381302 | 5 × 2 | 馬朝鏡頭三分之二正面跑（聖經第 41 條只拍側面與側後） | 「鏡頭正對路、與路同高、**嚴格側面**」；路「沿畫面下緣平行、從右緣橫到左緣」；馬「完全側面、整個身體橫對鏡頭、頭朝左」，動作加「始終側面對鏡頭、離鏡頭始終同樣距離」；第一格全速、阿令第一格就伏在馬頸上；**官道不亮**：路寫成「月光下暗灰、跟田一樣暗」（拿掉 fix1 的 `pale beaten earth path`）；換鞍 | 固定 |
| s29 | d1 9381101 | 5 × 2 | 帶亮銀鞍角的西式鞍（下馬後空鞍整個露出來） | 只換鞍句（見下） | 照 d1 慢推 |
| s30 | d1 9381101 | 6 × 2 | 同一副西式鞍，在畫左大大地入鏡 | 只換鞍句 | 照 d1 慢推 |
| s32 | d1 9381101 | 6 × 2 | 同一副西式鞍與馬鐙在全景正中 | 只換鞍句 | 照 d1 慢推 |

**鞍句**（五個騎馬鏡一起換，`cut-notes` REVIEW 3 給第 39 集的寫法再加木框）：
`an old plain brown leather saddle on a folded dark cloth` →
`a low flat old saddle of plain dark brown leather stretched over a plain wooden frame, its front low, smooth and rounded, all of it dark and worn, on a folded dark cloth`。
全部正面寫（拍法第 18 條：不寫否定名詞）；不寫 silver、horn、pommel 這類字（`mkjobs.py`、`check938f5.py` 都擋）。

### s30、s32 為什麼一起重拍（協調者要我判斷）

看了現在剪接用的 d1 9381101（scratchpad `e938f1/saddle.jpg`）：
- 騎著的時候鞍被她的衣裙蓋住、只看到灰白一塊：s16 s18 s20 s21 s22 s25 s27b 都看不出鞍的樣子，**不用重拍**。
- 鞍空著、整副露出來的只有三鏡，而且前後相連：**s29**（下馬後 c3.5 起）→ **s30**（畫左一副帶鞍角的大西式鞍）→ **s32**（全景正中、鞍角＋馬鐙）。
  只換 s29，下一鏡又跳回亮鞍角，比現在更顯眼。所以三鏡一起，值得：每鏡兩支 5–6 秒、合計約 1.2 CU。
- **採用規則**：s29、s30、s32 **三鏡都有一支鞍對、其他也過得去才一起換**；任何一鏡兩支都不行，就三鏡都留 d1（現狀，列已知瑕疵、問站主），不要混用。
- 風險：s32 是九個人加一匹馬的全景，重拍可能弄壞人數或弩；挑片時對照 d1 9381101（隊長同臉同盔、弩手一排、火把一支拿在手上、馬拴在樁上、阿令在石階上按門）。

## 挑片要看的、退路

| 鏡 | 挑片要看 | 兩支都不行時 |
|---|---|---|
| s18 | 第一格就在跑、從院門左半衝出去、不減速；唐小棠只有背影、雙丸子、不露臉；只有一匹馬兩個人；鞍深色低平 | 現用 d1 9381101 2.0–6.5＋快馬蹄（REVIEW 3） |
| s19 | 床前沒有浮著的玩偶；草兔子一隻在枕邊；只有凳上一朵火；雙膝與小腿著地、全身入鏡；兩手握著小禾的手；台詞對嘴（a20＋a21，a21 是片中原聲） | 現用 d1 9381101（熊接受，REVIEW 3 A13） |
| s20 | 嚴格側面、右往左橫過畫面、離鏡頭距離不變；第一格全速、阿令伏身；路暗 | 現用 fix1 9381302 2.0–5.167（斜向朝鏡頭） |
| s29 s30 s32 | 鞍低平、深色、沒有亮金屬；其他照 d1 選定支的標準；s30 a27 對嘴、s32 a29 對嘴 | 三鏡都留 d1 9381101（見上面的採用規則） |

挑片寫 `review-picks.tsv`（同 fix1–fix4 的欄位），選中的改 `../picks-final.tsv`（source `fix5`），再進精修。

## 檔案與指令（2026-11-24，全部跑過、0 錯）

```
cd docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e938-live/fix5
python3 -I mkspec.py                                    # 6 shots -> spec.json (38 s per seed, 76 s)；每個替換在底稿裡剛好一次
python3 -I mkjobs.py <live>/fix5                        # scan 0；colab-jobs.json 12 支、76 秒
python3 -I <scratchpad>/tools/check938f5.py <live>/fix5 # mkcheck938f5.py 從 check938f1.py 再改 7 處（鞍句、s18 衝左半、s19 一隻草兔子與唯一的火、s20 側面暗路、每鏡運鏡），通過
python3 -I ../../_scripts/preflight-prompts.py <live>/fix5/colab-jobs.json                          # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix5/colab-jobs.json   # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix5/colab-jobs.json  # 0／0
bash <scratchpad>/e938f1/scan5.sh                       # prep938 的否定名詞／會長字的名詞／掛著的東西／舊字：全 0
DRY=1 bash <scratchpad>/e938f5.sh                       # rc 0（帳號 A 的 COLAB_ACCOUNT_SLOT=a＋PATH 也 rc 0；REL 不存在時 rc 2）
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e938-dh/runpod/live`。`check938f1.py`～`f3` 重新生成後對 fix1～fix3 仍通過。
`e938f5.sh` 照 `e938f3.sh`：G4、`SESSION` 預設 `zt-live3`、帳號由外部設定、`REL` 可覆寫、送前再跑檢查、兩輪補缺、跑完只釋放自己的 session。
**fix4 還在跑時不要在同一個 session 送 fix5**（換 `SESSION=zt-live2` 或等它跑完）。

## 估價

- 重拍：12 支 76 秒，照第 37 集第一輪重拍的實數（每秒 0.043 CU）約 3.3 CU，加開機約 **3.5–4.2 CU、30–40 分鐘**。
- 精修（選中的才精修；照 `../fix4/plan.md` 的做法，每格約 0.0032 CU）：六鏡都換的話 38 秒約 900 格、約 2.9 CU，加開機約 **3.0–3.8 CU**；
  可以跟 fix4 的精修（s09 s17 s22 s34 s36，約 2.3–3.0 CU）**同一批送**，省一次開機。
- fix5 合計約 **6.5–8 CU**（另加 fix4＋它的精修約 4–5.5 CU）。餘額剩約 100 CU 時先問站主。

## a22 重錄（s23 隊長「宵禁！有流寇，天亮以前誰都不准進城！」）

站台錄音原檔不帶稿聽寫本來就是「小徑」（`tools/fw938.txt`：plain r0.87「小徑,有流寇…」；帶稿 r1.00）。
做法照 `tools/rec938-retake.sh`、`rec937-slow.sh`：`lines.mjs` 一句一呼叫、間隔 12 秒、429 等 90 秒重試、最多 4 次；同一個聲音（Iapetus）、同一個情緒（吼）；
三種**只給 TTS 看**的寫法（字幕照稿），各錄進自己的資料夾 `audio/a22r/<v>/zq938a22.wav`，**原檔 `audio/zq938a22.wav` 不動**：
- v1「宵禁——！有流寇，…」（宵禁後拉一個停頓，讓它自己成一個吼出來的詞）
- v2「xiāojìn！有流寇，…」（拼音提示，同 `mkhints938.py` 的多音字做法）
- v3「宵——禁！有流寇，…」（兩個字拉開，最後的手段）

指令：`bash <scratchpad>/tools/rec938-a22.sh`（錄完自動用 `fw938.py` faster-whisper medium int8 不帶稿／帶稿聽寫三支，寫 `tools/fw938-a22r.txt`）。
挑法：不帶稿聽寫是「宵禁」的那支；音高照 REVIEW 3：s23 的下一句是年輕守軍 a23（約 230–235 Hz），隊長這句要 **≤ 約 195 Hz**（≥ 3 半音；原檔 188 Hz），高了就 rubberband 降（`-pNN`）。
選定後把 `audio/a22r/<v>/zq938a22.wav` 複製成 `audio/zq938a22-r5.wav`，`e938cut.sh` 的 a22 改指這個檔，重跑 `rec938-check.sh` 那三項（聽寫、f0、人聲長度對 BUY 8 秒）。

**結果（2026-11-24 04:25–04:35 UTC）：沒錄到。** 站台 TTS 可以呼叫（憑證在、`lines.mjs` 照常送出），但 v1 四次都回 `video_speech_upstream_busy`（Gemini TTS 上游忙／共用的每日額度），
腳本照規則在第 4 次後停下，沒有無限重試；v2、v3 沒送。`audio/zq938a22.wav` 沒動，`audio/a22r/v1/` 是空的。原因與第 37 集一樣是共用額度，換時間再跑就好：
`bash <scratchpad>/tools/rec938-a22.sh`（已錄的會跳過；只想先試一種用 `VARIANTS=v1`，想多等用 `TRIES=6`）。錄完看 `tools/fw938-a22r.txt` 的 plain 那行，再照上面挑法量音高。
