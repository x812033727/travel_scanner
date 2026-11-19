# 第 34 集真人版 fix2：s28 韓伯磕頭、s32 錢員外撂話（未送出）

fix2 準備代理 2026-11-19 寫。依據：`../fix1/review-picks.tsv` s28、s32 列（挑片者寫的 fix2 改法）、`../fix1/{plan.md,mkspec.py,mkjobs.py,spec.json}`、
`../picks-merged.tsv`、`../PREP.md` §6、範本 `../../e933-live/fix2/`、route-a.md 與任務檔的教訓。
**只寫好、跑過免費檢查，沒有送出任何生成**（Colab、RunPod 都沒開），沒用站台 TTS，沒 commit。

## 基底

以 **fix1 實際送出的工作與提示詞** 為基底（不是 d1）：s28 用 fix1 **9341212**、s32 用 fix1 **9341211**（兩支都是目前的備案）。`mkjobs.py` 先比對
基底提示詞的 sha256 與 `<live>/fix1/colab-jobs.json` 一致，再核對 d1（`../spec.json`）與 fix1（`../fix1/spec.json`）這兩鏡的每條修改都在基底裡，
每句 fix2 替換在 fix1 提示詞裡剛好一次。圖、解析度、秒數照 fix1。

## 重拍清單（2 鏡 4 支、32 秒）

| 鏡 | 種子 | 秒 | fix1 的問題 | 改什麼（英文原句在 `mkspec.py`） |
|---|---|---|---|---|
| s28 | 9341311、9341312 | 8 | 框、固定鏡、悲痛的眉、磕頭都做到，但說話時仍咧嘴笑（1212 在「給您磕個頭」5.5–6.75 秒嘴大開、上排牙全露、臉頰上抬）；磕頭在句尾才開始（7.0 秒） | (a) **結果提前**：「By the middle of the line Elder Han has already bowed low: …兩手從膝上滑到前面的草上、頭低向地面、整個人在畫裡, and he says the last words with his face turned down toward the grass, only his white topknot and brow toward the camera」，路徑改「he starts to bend forward with the first word」（拿掉 slowly）；(b) **嘴小、遮住**：`lips, jaw and cheeks moving clearly` 改「lips moving … in small natural talking mouth shapes, his mouth parting only a little on each word under the white moustache, his upper teeth covered, his cheeks slack and hanging, his lips trembling」；說話視線「先看畫右上緣外那一點，往下時看前面的草」；(c) **身分句**加「a worn, grieving old face」。保留：膝以上的框、草地留給磕頭、固定鏡、眉頭中間往上、嘴角往下、NOSMILE、磕頭結果句 |
| s32 | 9341313、9341314 | 8 | 1211 站位與動作都對（第一格背對四分之三往右走、右肩回頭、第一秒甩袖、說完在右三分之一），但整鏡得意地笑；視線平看畫左，不是往左下的田 | (a) **臉露更少**：「so that we see only the side of his face past his right shoulder: his ear, his cheek and the tip of his moustache」；(b) **具體苦臉**取代 `sour and dark: his face fallen, brows pulled down hard, … jaw clenched`：「sulking and sour: his lower lip pushed out in a sulk, the corners of his mouth dragged down hard, his eyes narrowed under the heavy brows, his cheeks hanging flat and heavy, his nostrils flared」；(c) 構圖句拿掉重複的 `short and portly with a round face and a thin eight-shaped moustache`（身分句照留 round face）；(d) 兩處視線都改「cast down toward the field below the lower left edge of the frame」（說話句保留 `eyes on`，preflight 的 gaze 檢查要它）。保留：1211 的站位與動作句全部、固定鏡、NOSMILE |

拿掉會引出笑的字：mkjobs 的掃描把笑字擴大到 smil／grin／laugh／smirk／smug／sneer／cheer／pleased／kind／warm（`low warm golden sunset light` 除外）／
shrewd／gleeful／amused／gritted，兩鏡 0 命中。s28 第一版寫了 `mouth opening`，被「會打開東西的字（open）」掃描擋下，改 `parting`。

**PREP.md §6 照做**：兩鏡都在田裡、在 s27–s40 範圍，POOLMARK（` below the deep pool`）由 d1 拿掉、fix1 承接，fix2 再核對基底已沒有它、全文沒有 pool／pond；
XQ_GEN→XQ_LIVE 只動 s26，不涉及；兩鏡都不在 clear-air（s01–s03、s34、s38、s40）與鞋句（s12、s19）名單，掃描核對 clear 句是 d1 原句一次、沒有鞋句。
d1 的 GAZE_REFINE 句被 fix1 換掉的部分（s28 `his face lifted …`、s32 `his face looking back …`）視為 fix1 承接，不算漏。

## 檔案與指令（2026-11-19，全部免費）

```
python3 -I mkspec.py                                    # 2 shots -> spec.json (32 s)
python3 -I mkjobs.py <live>/fix2                        # 掃描 0 命中；colab-jobs.json 4 支、32 秒
python3 -I ../../_scripts/preflight-prompts.py <live>/fix2/colab-jobs.json            # 0 error(s), 0 warning(s)
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py <live>/fix2/colab-jobs.json   # 0 error(s), 0 warning(s)
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest <live>/fix2/colab-jobs.json  # 0 error(s), 0 warning(s)
```

`<live>` = `/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/runpod/live`。種子 9341311–9341314 在 repo 與 `<live>` 都沒用過。

**預估**：4 支、32 秒（8 秒 × 4）。fix1 8 支 64 秒從開 session 到跑完約 24 分（含冷啟動約 7 分），估價約 3.5 CU；fix2 按秒數約 1.4–1.7 CU，
加冷啟動約 **2 CU、約 15 分**（約 US$0.2）。
**跑在哪**：Colab 一個 session 一次一件事（route-a 2026-11-09），送出時帶 `--session <閒著的 session>`、`--detached`，背景執行帶 `timeout: 7200000`，
輸出 `<live>/fix2/out/s28-93413{11,12}.mp4`、`s32-93413{13,14}.mp4`。

## 送出後挑片要看的

- **s28**：每 0.125–0.25 秒放大嘴：開口小、上排牙不露、臉頰不上抬、嘴角往下（不像笑）；句子一半（約 4 秒）時已俯身、兩手在草上，最後幾字臉朝地面
  （只見髮髻與額）；整個人在畫裡；台詞 6.1 秒，句尾離片尾留得下；聽寫核對整句沒有多唸。若兩支都不行，仍用 fix1 9341212 start 0.875、end-before 8.000。
- **s32**：只見耳、頰、鬍尖，整鏡沒有一格正視鏡頭；苦臉（下唇噘、嘴角往下）、不笑；眼睛往畫左下外的田看下去；甩袖在前段、說完時仍在畫內右三分之一；
  臉露太少可能讓嘴看不到——那樣更好（台詞可放錄音或原聲）。若兩支都不行，仍用 fix1 9341211 start 0.000、end-before 7.500。
