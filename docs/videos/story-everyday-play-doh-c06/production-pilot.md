# C06 Play-Doh｜本機試片執行紀錄

本片依 [站主核准收據](reviews/owner-script-production-approval.md)執行：80 張插圖、每張最多三次，94 句旁白、一首配樂，整支 US$25 停線。僅製作本機試片；不匯入、不上傳、不發布。舊的 [製作前報價](production-quote.md)保留為核准前快照，凡稱「尚未核准」之處，以本紀錄與核准收據的較新狀態為準。

## 專屬發音字典

- 從 C06 Treatment 的確切提交 `3e49a964aa61f20fcf12743140984588a6a1c488` 建立隔離工作樹；在其 `video.json` 尚不存在時，以 PR #1676 `series.json` 的 16 個 `names` 呼叫 `initializeStoryLexicon`。本集工作資料夾在呼叫前不存在，影片工作資料夾的全域 `STOP` 不存在。
- 嚴格讀回 `videoLexicon({requireSnapshot:true})`：`mode=snapshot`，`sequence=1`，字典 SHA-256 `7dfd45e09466d424522c405627249ae59c42716572c7246979507bfff09c2477`，事件 SHA-256 `42b422ea8a45c866fb5fabd0a29e18ae74a15412a39dde1802a721dd13f8caa7`。
- 隨後合入 PR #1676 的逐字稿與逐鏡；`script.md`、`video.json`、`visual-plan.tsv` 三個 SHA-256 均與站主核准版本相同。沒有以偽造 `auto.json` 或遷移舊故事來越過字典關卡。

## 停線與讀回

| 階段 | 實際結果 | 可核算支出 |
| --- | --- | ---: |
| 字典初始化與稿件合入 | 完成，嚴格讀回 sequence 1 | US$0 |
| 配音 dry run／額度預檢 | 已通過：94 個請求，約 2,716 個本輪計費字元；伺服器回報 `gemini:Sulafat` 可用、本月餘額 7,887,491 字元 | US$0（唯讀） |
| 94 句配音、正文量長與音訊查核 | 2026-10-22 05:33 UTC 首次正式執行碰到供應商 429 `video_speech_upstream_busy`，CLI 顯示「Gemini 語音暫時忙碌或達到用量上限，請稍後重試」；未生成任何 WAV、timeline 或 narration；本輪停止，不再重送 | 供應商拒絕；無可見音檔或計費收據 |
| 最多 80 張插圖及最多各三次品質評審 | **須先通過正文 480 秒與音訊關卡** | 待帳本讀回 |
| 一首配樂、組片與本機 QA | 待前階段通過 | 待帳本讀回 |

原報價可見圖片、評審與配樂上界約 US$3.32；正文旁白及其餘實際費用尚未拆定價，不能用差額推算可花額度。`media-status` 讀回本片圖片、片段、配樂、評審均為零，該媒體帳本為 **US$0.00**；它不涵蓋旁白供應商的美元帳。實際工作目錄只有 `approvals.json` 與字典交易收據，`audio/` 無檔，`LEASE` 已釋放。本次 429 由 API 將供應商 HTTP 429 映射到 `video_speech_upstream_busy`；沒有證據表明已完成任何一段旁白，也沒有正文時長可量。待供應商額度恢復後，應先讀回工作目錄與配音日誌，再按同一核准稿件做有界續跑，不可買圖越過 480 秒關卡。
