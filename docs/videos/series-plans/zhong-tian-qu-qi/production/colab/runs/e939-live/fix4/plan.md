# 第 39 集真人版 fix4：s40b 重寫——村民一齊回頭、許硯從畫右走進來

fix4 準備代理 2026-11-25 寫。依據：`../cut-review-2.md` major 2（fix3 的 s40b 六個村民背影幾乎沒轉頭、看著空穀倉門，許硯沒入鏡，讀成「大家看穀倉」不是「大家回頭看許硯」；
審片的根本修法：「許硯從畫右走進田埂，村民一齊轉頭看他」）、協調者交辦、聖經 `r2-bible-e031-e040.md`〈接點〉39→40（所有人回頭看跑到的許硯；第 40 集第一鏡他一步站到秦霜與村民中間、面向左）、
`../fix3/{plan.md,mkspec.py,mkjobs.py}`、`../picks-final.tsv`。**本代理沒有送 Colab**、沒用 RunPod、沒付費圖、沒有新圖；只做了 DRY／PRECHECK；只 commit 文字檔。

## 這一鏡（1 鏡 2 支、10 秒）

種子 **9391601／9391602**（93912xx–93915xx 都用過）。買 5 秒，剪接用約 2–3 秒。固定鏡。

| 項目 | 寫法（英文原句在 `mkspec.py`） |
|---|---|
| 圖 | 許硯定妝照＋angle-a（`check939`：兩張、定妝照在前，從 d1 s35 工作取路徑）＋穀倉前整張 `set-gucang-wai-l1`（s36 那張）；表頭 3 張 |
| 村民 | s36 同樣六人（白髮小髻灰長袍老人、炭灰瘦中年、舊靛藍十五歲少年、深橄欖綠胖五十歲、深灰配靛藍頭巾婦人、本色麻短衣頭巾寬背四十歲），**背對鏡頭**、腰以上、站在畫面左邊與中間；畫右留空：踩實的土路從右緣進來、第一格空著 |
| 轉頭 | 開頭六人**同時、明顯地**轉頭看畫右、肩膀跟著轉，仍背對鏡頭、最多露一點頰邊，之後一直朝他到最後一格（fix3 寫「中段轉頭」太弱，改「開頭、清楚、同一刻」） |
| 許硯 | 第一秒後從**畫右緣沿土路走進來**、膝以上、快而穩的步子，在畫右停在離他們幾步的地方，臉三分之四朝畫左看著他們（接第 40 集第一鏡面向左）；**嚴肅不笑**：咬緊牙關、眉平而鎖、嘴唇緊閉＋NOSMILE；不說話句（嘴唇從頭到尾閉著） |
| 服裝 | 本集**早上的服裝**（s24–s35）：舊藍灰書生袍、手肘補丁、袍子下半截白石灰粉、髮髻綁布帶。**沒有寫灰外衣**：協調者交辦寫了 grey coat，但外衣從 s23 起蓋在阿令肩上（s26「這件外衣是你蓋的」，s24–s35 的他都沒有外衣，`check939.py` 對早上的鏡斷言不寫外衣）；要讓他穿回外衣，改 `mkspec.py` 一句即可，但會跟 s35 他出門時的樣子接不上 |
| 人數 | 「七個人、六個村民只見背影」與「只有許硯和六個背影」各一次；不點名別人；不寫 villagers／crowd（用 people of the village） |
| 光 | 同一個清晨低角度暖陽從右來、晴空；固定鏡 |

**怎麼接進成片**：取代 fix3 的 s40b。挑完後 `../picks-final.tsv` 的 s40b 列改成 `s40b	fix4	<種子>	<start>	<end_before>	<note>`
（片源 `/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live/fix4/out/s40b-<種子>.mp4`；fix3 那支留作備案）。沒有台詞、沒有錄音。
審片另外要的「畫面與聲音一起收、最後一格停 0.5–1 秒再淡黑」是剪接的事，不在這輪。

## 檔案與指令（2026-11-25，全部跑過、0 錯）

```
python3 -I mkspec.py                                    # 1 shot -> spec.json (5 s per seed, 10 s)
python3 -I mkjobs.py <live>/fix4                        # scan 0；colab-jobs.json 2 支、10 秒
python3 -I <scratchpad>/tools/check939f4.py <live>/fix4 # check939.py 的斷言（tools/mkcheck939f4.py 從 mkcheck939f3.py 改：s40b 的人是許硯、fix4 斷言），通過
python3 -I ../../_scripts/preflight-prompts.py <live>/fix4/colab-jobs.json                          # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix4/colab-jobs.json   # 0／0
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix4/colab-jobs.json  # 0／0
bash <scratchpad>/e939f4/scan.sh                        # 否定名詞／會長字的名詞／掛著的東西／舊字：全 0
DRY=1 bash <scratchpad>/e939f4.sh                       # rc 0（另測 GPU=A100＋帳號 A）
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e939-dh/runpod/live`。`e939f4.sh`：`COLAB_GPU=${GPU:-G4}`、`SESSION` 預設 `zt-live3`、不設帳號、`REL` 可覆寫；
送前重跑 mkspec／mkjobs 與全部檢查；單輪（已有 mp4 的跳過）；跑完 `ONLY_SELF=1 bash $REL $SESSION`。

**估價**：10 秒 × 約 0.043 CU／秒 ≈ 0.4 CU，加開機與載模型，約 **0.5–1 CU、約 0.15 小時（G4）**。

**跑的指令**（先確認 `zt-live3` 上沒有別的集在跑）：
```
bash /tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/acctA-run.sh bash /tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/e939f4.sh
```

## 送出後挑片要看的

- 六人都背對鏡頭、開頭就一齊明顯轉頭看畫右；沒有人正面對鏡頭。
- 許硯從畫右緣沿土路走進來、停下、三分之四朝畫左看他們；不笑、不說話；長相與髮髻照定妝照；沒有外衣、袍子下半截有白石灰。
- 只有七個人（沒有第二個許硯、沒有多出來的人）；穀倉與水田照 s36、清晨暖陽。
- 走進來與停下之間留得下 2–3 秒。結果寫在 `review-picks.tsv`。
