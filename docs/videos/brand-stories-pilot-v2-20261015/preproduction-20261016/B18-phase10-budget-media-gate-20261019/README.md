# B18 Phase 10 離線費用與媒體前檢 — HOLD

2026-10-19；只讀儲存庫、現有公開安全的審查文件與草稿 PR 狀態，沒有連正式機、供應商或帳戶，沒有付費或改動既有稿件／任務票。此報告綁定 `B18-route-b-phase10-story-candidate-20261019/manifest.json` SHA-256 `269641f1b5b01f288cce24b6258a987ffdee7818eb43692aeb5619612ef11acb`、獨立[來源審查](../B18-route-b-phase10-story-candidate-20261019/independent-source-review-20261019.md) SHA-256 `72de458dc73f1adbdc1cffde1b415230b46e771cc66227b11c25f8939dcc53f2` 與[故事盲讀](../B18-route-b-phase10-story-candidate-20261019/blind-story-review-20261019.md) SHA-256 `c851d44526d182408dc551d18c02a40ed29614c835308d2595b1ce46a7137601`。`build.mjs --check` 回報 `B18_PHASE10_OFFLINE_HOLD`。來源路由審查 P0/P1/P2=0、故事盲讀 P0/P1=0 且 P2=3，兩者都**沒有**核准正式史實、實音、媒體或付費。

## 數量：已知和不能推定的部分

| 項目 | Phase 10 已知 | 正式製作仍未知 |
| --- | --- | --- |
| 故事／語音 | 六章、22 個**口播段**、正文 2,833 個漢字／數字／〇。紙上 300 字／分約 566.6 秒，310 字／分約 548.3 秒，後者只比 9 分鐘多 8.3 秒。 | 沒有逐鏡 `video.json`／口播 `lines`，所以不能把 22 段算成 22 次 TTS 請求；實際 TTS 請求、逐句轉錄數、fallback／重配及實音正文時長均未知。 |
| 畫面 | `visual-proposal.json` 有 21 個**未生成的差異提案**：9 個舊鏡 prompt、5 個新場景、7 個新來源卡。它們不是 21 次圖片採購，也不是整片完整分鏡。 | 最終 `shot`／卡片總數、不同圖片數、重用／重畫數、縮圖圖像、judge／定位次數均未知；需完整定稿 `video.json` 和前後鏡頭／快取映射。 |
| 舊企劃基線 | 已有[本機 row](../../episodes/B18.json)為六章、1 名 cast，SHA-256 `c9aab2d7c9ebc1e0bb23d779a411deae9f9526b0f8ef7720af74754031ed3681`；[系列設定](../../series.json) SHA-256 `b2cdb40dd5c6b9e7723ae76fd5fb9992ca66fc0baebabc4ae0f5caabdb38502b`，目標 10 分鐘、`cute-mystery`、MiniMax `image-01`、`visual_tier: stills`。較早成本表使用 85 景／66 插畫／19 卡／88 句。 | Phase 10 未採用到 row 或 worker；舊景數、句數、造型和素材不能轉算成此版實際待買量。現有 row 沒有音樂設定，Phase 10 也沒有最終 `video.json`，是否用已授權曲、生成 Lyria 或不用配樂未知。 |
| 審稿 | 76 項主張仍為 `UNCHECKED`；21 份畫面提案沒有生成媒體。 | 正式逐章 fact/verifier、完整 `script-review.json`、實圖逐鏡判讀、字幕、成片和站主看片都未完成。 |

21 項提案分別是文字修訂／新場景／新來源卡。來源卡若在最終分鏡使用，通常由後製渲染；不可默默把它們算成 MiniMax 生圖，也不可據此扣掉其他未列的插圖。舊[成本刷新](../B18-cost-refresh-candidate-20261017/README.md)的 66 插畫＋3 張造型候選、正常重試後 US$2.08798 稅前，是 2026-10-17 的**舊數量與小額 judge 規劃假設**；不是 Phase 10 的定稿報價、保證上限或已核准支出。

## 目前程式的逐筆最高預留

若正式機模型和本工作樹相同，程式對 MiniMax `image-01` 一圖採 **US$0.003500**，Gemini 3.8 Flash 每次圖片 judge／定位 **US$1.032192**，一組圖加 judge **US$1.035692**；Gemini 3.8 Flash TTS 每請求 **US$0.151552**、逐句轉錄每請求 **US$1.032192**、Jev 1.13.0 每請求 **US$0.002688**、Lyria 3.5 每首 **US$0.080000**。這些是每次供應商呼叫前的保守最高預留，judge／轉錄按模型 token 極值推得，**不是實際帳單或訂閱抵扣後費用**；價格窗口只寫到 2026-12-31。正式模型、實際額度、稅費、已用金額、外部帳務和此版請求數未查。

程式錨點：`apps/api/app/video_media/catalog.py:99-107,194-201`、`video_media/admin_api.py:107-118,403-425`、`video_speech/admin_api.py:104-134,508-515,725-737,820-827`、`video_budget/prices.py:10-14`。如仍用舊 66 張插畫與 1 名 cast 的**純比較情境**，首輪 66 張正文圖加 3 張造型候選、各一次 judge 的逐筆上限總和為 **$71.462748**；角色預設每角 3 候選、最多 2 輪，單角最壞 6 組另為 **$6.214152**。兩個造型情境不能相加。這些高額是多個操作各達最高預留的壓力值，不能當 Phase 10 預計支出。Phase 10 確切圖片、TTS、轉錄與音樂合計目前**無法精算**。

## $5 程式規則與正式授權是兩道關卡

本工作樹 `video_budget/models.py:33-53` 把 B18 v2 列為 **$5 擬定逐片上限**；`0133_story_followon_budget.py` 將既有 B18 v2 帳戶由 $25 下調到 $5，保留舊操作，並新增後五支帳戶。`video_budget/service.py:212-215` 對仍是 $25 的 B18 v2 帳戶拒絕新付費；同檔 `summary()` 會在 migration 前就顯示目標 $5，故**摘要顯示 $5 不足以證明資料庫已升級**。帳本 `reserved`／`uncertain` 都占用上限，`reserved + settled + next ceiling > limit` 便拒絕派送（`service.py:34,129,218-226`）。

唯讀查到 [PR #1510](https://github.com/x812033727/travel_scanner/pull/1510)於本次觀察為 `OPEN`、draft、`no-auto-merge`；本次沒有正式機 schema／帳戶／工作讀回。草稿內有 migration 或程式碼，**不能當成已合併、已部署、帳戶可用或站主核准 B18 付費**。本批公開[試作規格](../../README.md)明確只記 A01 全項最多 $25 的付費授權；B18 與後五支每集 $5、六集 $30 仍是待核准提案。A01 授權不能轉用 B18。即使將來帳戶為 $5，單張圖加 judge 的最高預留 $1.035692 仍須逐筆核當時剩額；不能靠舊 $0.01／judge 規劃值預告整片可做完。

## 可重用媒體與後續前檢

Phase 10 manifest 記 `media_generated: false`，21 個畫面提案均屬未生成文字；既有公開文件沒有一份把可重用 B18 圖像、聲音、轉錄、曲目或其 hash 驗證到 Phase 10。這只支持「**未證實可重用素材**」，不證明正式主機或其他位置完全沒有 cache。本次未查媒體磁碟、speech journal、供應商帳戶或正式機。B18 目前的持久化 row／worker 採用、預算帳戶、已結算／預留／結果不明操作與實際媒體存量都須新鮮唯讀核對。

先完成正式逐章史實與劇本審查、完整鎖定分鏡及 `video.json`，再對**最終位元組**實跑 `planRequests`、計算首輪圖／look／TTS／轉錄／judge 和可能重試，對照可驗 SHA 的已付費 cache。B18 明確付費上限核准、相符 migration／worker 已部署及帳戶讀回、無 hold／鎖／執行中或不明付費工作、供應商模型與價格窗口一致後，才可討論限量試拍。每次都用唯一 operation ID 及本片帳本驗證 `已結算 + 已預留（含 uncertain） + 下次最高預留 ≤ 核准上限`；結果不明先核帳，不重送。此次狀態維持 **HOLD**，不授權匯入、配音、生圖、配樂、成片或上傳。
