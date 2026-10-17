# A01 製作前唯讀關卡與成本重算（2026-10-17）

本報告只讀取 `snapshot-104` 與本機程式，沒有向供應商送出請求、修改正式機或核准劇本／媒體。報告的現稿基準是 A01 來源鏈 tip `e1499cd695f2f414d9379a8917b6b5b36e50ea0d046de495938157d8ff97add7`、104 筆完整鏈結，`video.json` SHA-256 `66fa192bc314a787a0ab66ec2a93976b4110138f4184747de7d3bfda2c5a6812`；檔案取自 `C:/Users/x8120/.codex/captures/A01-20261017-afternoon-fe35369c/snapshot-104/`，校驗結果見同層 `verified-review104.json`。本機程式分析取 `8a78` worktree HEAD `37e635dedcc3f7cb48be4d07b2f4f3dc67998ac8`；實際主機版本與設定要在發送付費請求前另查。後述刪除 `turn-08` 是編輯候選，**未套用到此快照**。

## 現稿與媒體容量

| 項目 | 現稿可證明的值 | 下一關 |
| --- | --- | --- |
| 作品 | `story-rolling-suitcase-v2`，`format: drama`、`series.kind: story`、`visual_tier: stills`；系列 `image_model: image-01`、`target_minutes: 10` | 主機 API 的作品模型及媒體 status 仍須相符 |
| 畫風與字幕 | `look` **恰好** `{ "preset": "cute-mystery" }`；`subtitles.burn_in: false`、`style: drama` | 成片實際關閉 CC 後須沒有燒字幕；繁中 CC 要對時 |
| 聲音 | Gemini `Sulafat`、台灣華語旁白；`video.json` 只有旁白，兩個匿名人物只作畫面設定 | 真實語音、發音、情緒與實際片長尚未測量 |
| 正文鏡頭 | 78 個 `shot`，全部 `data.visual: still`，0 個正文文字卡，另 1 個 `now-outro`；108 句、2287 spoken units | 本機 `cuteStoryVisualProblems` 與 `checkChapters` 均為空；不等於已看過圖片或成片 |
| 插畫需求 | 現稿 78 張關鍵影格；兩名 `characters` 會先走設定圖，只有 9 鏡引用其中一名，沒有雙人物參考鏡或 `end_frame` | 設定圖兩角色各預設 3 候選，過關後仍要逐鏡產圖／judge |
| 片長 | `estimateTimeline` 在 250 spoken units／分與工具停頓下為 **638.77 秒（10:38.8）**，估計正文 3.4–11.73 秒／鏡；10 分鐘 cute story 的實錄驗收帶是 **540–660 秒** | `timeline.json` 尚無；真 TTS 才能判定，片頭 5 秒／片尾 21 秒只在舊規劃記載，非本快照實際播放證據 |
| 動態片段 | `stills` 路線不買生成 clip；服務端對 pilot clip 亦拒絕 | `clips --dry-run` 應讀回 0 個需買片段；靜圖仍要有適當緩慢運鏡 |

第 11 輪真實敘事盲評仍是 `passed: false`，`one_line`、`no_recap` 都指 `turn-08` 的 `6i8x`。獨立編輯覆核建議只刪該鏡及句子並退役 `t19`，保留原審計和計數，再做新來源的真實查核／聽眾／盲評。若僅刪該 1 鏡，靜圖數會變 77、場景數 78、句數 107；其估計鏡長約 7.97 秒，概算降到約 10:30.8。這只是離線推算，未得到第 12 輪結果或正式稿件收據。舊 `A01-shot-plan.md` 的 **95 插畫＋11 卡、約 9:02** 是凍結編輯稿分鏡容量，不是現行工人實稿，不能直接作採購數或成片長度。

## 帳本證據與本地費用估算

`round12-budget-inspect.json` 是另一操作於正式機 HEAD `129f220`、2026-10-17 約 14:08 UTC，以 `python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2` 取得的**當時唯讀持久帳本**：`limit_usd=25.000000`、`remaining_usd=25.000000`、`reserved_usd=0`、`settled_usd=0`、`uncertain_operations=0`、`operations=[]`、`total_over_limit=false`。這是目前可指認的正式帳本證據；下一個付費請求前必須重新讀回。快照 104 沒有 `timeline.json`、圖片、`keyframes/manifest.json`、`media/ledger.json` 或成片；其匯出範圍本身不證明所有正式卷／供應商歷史均為零，但 `actual-104-readback-20261017.json` 記本次來源無媒體產出。

以下用**本機 catalog 的名目值** `image-01 US$0.0035／圖`、媒體 judge `US$0.01／次`，不是供應商實際結算，也不是主機已核定的整片報價：

| 階段 | 依快照 104 的基數 | 本機算式與估值 |
| --- | --- | --- |
| 匿名人物設定圖 | 2 人 × 預設每人 3 候選；全數需第二輪時最多再 6 張；若系列庫已有核定可重用的同設定圖，實際新圖會減少 | 首輪 6 × (0.0035 + 0.01) = **US$0.081**；兩輪 12 張為 **US$0.162** |
| 正文關鍵影格 | 78 張，每張先 1 take 並 judge；工具同一次呼叫最多 3 take／鏡 | 首輪 78 × 0.0135 = **US$1.053**；全部 3 take 為 **US$3.159**。若 `turn-08` 真刪除，改為 77 張：**US$1.0395**／最多 **US$3.1185** |
| 動態 clip | 全部是 `still` | **US$0** 的生成 clip；合成與運鏡仍須做 |
| 配樂 | `video.json` 有生成 prompt；本機 catalog 僅容許 pilot 使用 Lyria 3.5，或關閉生成 | 生成一首名目 **US$0.08**；主機 music 設定與授權素材須讀回 |
| 繁中 TTS | 估計旁白加停頓 638.77 秒 | 按舊企劃所引約 US$0.0135／分，僅粗估 **US$0.144**；真費用用供應商 token 用量結算，旁白、停頓與重錄都可改變值 |

因此「一輪設定圖＋一輪 78 張關鍵影格＋一首音樂＋概算 TTS」約 **US$1.36**，**不含**後續文字模型、轉錄／Jev 音訊審查、重配重畫、額外 judge、未知供應商結果與任何稅費。它不能當作「US$25 足以保證完片」的承諾。舊規劃 US$18.45 的總預留也不可直接當成新現稿報價。實際 API 的 pilot 帳戶在供應商請求前保守預留，媒體 judge／locate 以已核價 Gemini 模型單次上界 **US$1.032192** 先佔額，回答後才按真 token 結算；本地 `media/ledger.json` 的 US$0.01 只是階段估值。因而要**一次一鏡或小批次，確認前次操作結算與正式剩額，再送下一筆**；未知結果保持 `uncertain`，不可憑逾時重送。TTS、Jev 與文字模型亦各有獨立預留／停線，訂閱文字模型的用量不能假裝是零風險，正式 pilot 禁止無上界的 API 文字模型。

## 繼續製作的順序與硬關卡

1. **實稿**：以新來源雜湊完成 `turn` 最小修正、章查核及 listener，執行第 12 輪全稿盲評；必答項真實全 PASS。不得把第 11 輪失敗改寫為 PASS、重置失敗計數，或沿用舊 `video.json` 的審查雜湊。
2. **獨立稿審**：第二讀者把新六章、`script.md`、`video.json`、`series.json`、`claims.md`、`verify-1.md` 及新 narrative receipt 與凍結 `scripts/A01.md`（SHA `f91816021ebea28e1957199a5c73ccc588748e988730efc92e0486d09d5215c6`）對齊，逐項 PASS `reference_alignment`／`factual_claims`／`narrative`；只在真實審核後寫 hash-bound `story/reviews/script-review.json`。目前該收據不存在，worker 應保持 `STOPPED_HOLD`，不得進 TTS。
3. **付費前**：重新查主機 HEAD、已部署的 `story.mjs`／`flow.mjs`／`lexicon-store.mjs` 及媒體程式、A01 STOP、project lease、四個部署鎖／release hold、A01 與全站執行中付費工作；查 API `reconcile_cli` 的原始操作列、保留與不確定項，查 `media-status` 模型／key／月額／per-video cap，以及 TTS／Jev／訂閱 route。任何漂移或未知結果先停，不解除 STOP 後對全站跑 `auto`。
4. **角色設定圖**：依 `DRAMA_STEPS`，有兩名匿名人物的故事先走 look generation／approval，再進 TTS。確認人物只作情境示意，不畫品牌或真實人物肖像；若沒有可重用的核定圖，畫兩名角色的候選並保留 judge／選圖收據。
5. **旁白**：僅在稿審通過與限額確定後跑 TTS dry run，再以正式逐段工作日誌合成；用**實錄** `timeline.json` 驗 9:00–11:00。失敗時依 worker 允許的最多兩次來源支持的 resize，只改必要章並重新查核、聽審、稿件收據與語音，不用空白／慢播湊片長。接著 `check-audio`／Jev 全片及局部退件校音，保留逐句 WAV 雜湊與朗讀收據。
6. **正文插畫**：以 TTS 時軸做少量代表鏡頭驗主體、年代物件、畫風、文字錯誤及相鄰剪接，通過後按限額批量畫剩餘鏡頭。MiniMax image-01 只畫可愛的相關情境，不把插畫當歷史照片或證物重建；年份／專利／來源文字由後製核對。全部鏡頭看聯絡表與連續播放；圖審通過、焦點對旁白、無多餘空白或重複運鏡，才做 storyboard gate。現稿 100% 插畫符合至少 70% 和最多連續 3 卡的結構規則，但美術與內容仍未驗。
7. **成片與交付**：render → `clips` 靜圖 manifest（0 生成片段）→ 適用的 music → assemble → 繁中 captions／qa；對 `final.mp4` 做真實聲畫播放、開關 CC、片頭／片尾與結束畫面三個可點元素、音量、章節和縮圖檢查。成片審核／站主看片、語言選擇與 YouTube 私密上傳／公開是不同關卡；英／日／韓雖可先勾選，成片核准前不做其配音。本次授權不含 YouTube 上傳或其他集付費製作。

## 下一次唯讀指令（在正式容器，逐條且按關卡執行）

```sh
# 帳本讀回：API 容器、預設唯讀。主機操作者先確認 compose／HEAD／鎖／STOP。
python -m app.video_budget.reconcile_cli --slug story-rolling-suitcase-v2

# 工作階段：video-worker 容器，主機已設定 VIDEO_DOCS / VIDEO_WORKDIR。
node tools/video/cli.mjs status --slug story-rolling-suitcase-v2
node tools/video/cli.mjs media-status --slug story-rolling-suitcase-v2

# 以下只在新版獨立稿審 PASS、來源已固定後。dry-run 不購買。
node tools/video/cli.mjs look --slug story-rolling-suitcase-v2 --dry-run
# look 已核定、模型／角色設定與 project lease 已核對後：
node tools/video/cli.mjs tts --slug story-rolling-suitcase-v2 --dry-run
# 實錄旁白與音訊審查已核定後：
node tools/video/cli.mjs keyframes --slug story-rolling-suitcase-v2 --dry-run
# 真實 timeline 與 storyboard 已核定後：
node tools/video/cli.mjs clips --slug story-rolling-suitcase-v2 --dry-run
node tools/video/cli.mjs music --slug story-rolling-suitcase-v2 --dry-run
```

每次操作前要讀回的 **key**：精確 `slug`／`series.slug`／`episode`、來源鏈 tip 與 `video.json`／六章／`script.md`／`narrative.json`／`script-review.json` 雜湊；`auto.json` 的 `blocked_kind`、`narrative.rounds`／`failed`、章 `checked`／`listened`、`story.length`；A01 STOP 和執行中 `video_stage_jobs`／`video_media_jobs`；預算 `limit_usd`／`remaining_usd`／`reserved_usd`／`settled_usd`／`uncertain_operations`／每筆 `operation_id,status,max_usd,actual_usd`；`media-status` 的 `image.provider/model/configured`、`music.provider/model/enabled`、`judge` 模型、單支／每月限制；TTS `voice`／`model`／每月字額；`timeline.speech_hash`、`keyframes.visual_hash/look_hash`、`media/ledger.json`、`final.mp4`／CC 檔案 hash。現時無法核定**實際 TTS 秒數、每鏡成像成功率、供應商最後費用、主機當下月額、成片品質與最終觀看表現**。
