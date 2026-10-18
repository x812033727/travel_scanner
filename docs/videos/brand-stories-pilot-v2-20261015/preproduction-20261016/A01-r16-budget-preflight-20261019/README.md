# A01 r16 付費前成本核對 — HOLD

2026-10-19，純本機唯讀核對。對象是 `story-rolling-suitcase-v2` 的離線 r16 候選；`A01-editorial-candidate-20261019-r16/manifest.json` SHA-256 為 `5dade9fcd0f76c03b2c463addef935b0764d8d78eda9c621bb18e9bff462edef`，其中 `candidate/video.json` SHA-256 為 `2c095cab5f92aa50e55e8035e4bdc8de4ca8b8bdba6c82f15a0ea009d5f19ff1`。這是成本試算的版本錨點，**不是正式機已採用的稿件或付費放行收據**。未查詢主機、供應商或帳戶，未送出付費請求。

## r16 路線與呼叫數

| 項目 | r16 靜態數量與路線 | 依據 |
| --- | --- | --- |
| 畫面 | 65 個 scene：64 個 `shot` 全為 `visual: "still"`，0 個正文卡片，1 個 `outro`；0 個 end frame、0 個生成 clip | r16 `candidate/video.json`；`tools/video/media/keyframes.mjs:426-439` |
| 角色外觀 | 2 個 `characters`；即使只有旁白，`keyframes` 會先要求各角色選定且核准的 look sheet。系列已核准素材若完全相符才可重用 | `tools/video/media/keyframes.mjs:448-462`；`tools/video/media/look.mjs:146-154` |
| look 上限 | 預設每角色 3 個候選、最多 2 輪，若無可重用圖，最多 `2 × 3 × 2 = 12` 次生圖與配對 judge | `tools/video/core/drama.mjs:196,312`；`tools/video/media/look.mjs:23,108-111,162-208` |
| 正文圖上限 | 首張 64 次；現行 keyframes 預設每鏡最多 3 take，原程式最多 `64 × 3 = 192` 次生圖與配對 judge。舊 A01 企劃另規劃最多 25 次必要重畫，但不是此程式預設的硬上限 | `tools/video/media/keyframes.mjs:28,439,616-664`；`A01-shot-plan.md`「付費前帳」 |
| 旁白 | 77 句；用 r16 `video.json` 與 `lexicon.json` 跑 `planRequests`，得到 65 個初始 Gemini TTS 請求、2,438 個預估計費字元、0 個 `audio_ref`。11 個多句 scene 若全部分割失敗，尚可追加 23 個逐句 fallback 請求；局部重配另計 | `tools/video/tts/requests.mjs:77-123`；`tools/video/tts/synthesis.mjs:99-121` |
| 聽音 | 首次 `check-audio` 每句轉錄一次，最多 77 次 Gemini transcribe；Jev 只讀不相符的句子，每批至多 40 句，若 77 句全不符則 2 次 Jev 請求。音訊重配及再次檢查會增加請求 | `tools/video/tts/check.mjs:1-17,56,222-227,299-375` |
| 配樂 | r16 設定的是 `music.prompt`，不是既有授權 `music.track`；若維持這份配置，須用經核價的 Lyria 3.5 生成一首 | r16 `candidate/video.json`；`tools/video/media/music.mjs:47-95`；`apps/api/app/video_media/jobs.py:345-373` |

## 每次預留與總量壓力測試

以下是儲存庫於本日期採用的**保守每次請求美元上限**，不是供應商即時牌價、現金餘額或預期實支。`video_pilot_budgets` 對 A01 v2 上限為 **US$25**（`apps/api/app/video_budget/models.py:33,46-53`）。價格有效期在程式中只寫到 2026-12-31（`apps/api/app/video_budget/prices.py:10-14`）；啟動前仍要核對正式部署與實際模型。

| 呼叫 | 單次帳本最高預留 | 儲存庫依據 |
| --- | ---: | --- |
| MiniMax `image-01` 一張 | US$0.003500 | `apps/api/app/video_media/catalog.py:99-107`；`apps/api/app/video_media/jobs.py:528-540` |
| Gemini 3.8 Flash 圖片 judge 一次 | US$1.032192 | `apps/api/app/video_media/admin_api.py:107-118,399-425` |
| 圖片加 judge 一組 | **US$1.035692** | 上兩項相加；兩次請求實際依序預留與結算，並非同時必定占用此額 |
| Gemini 3.8 Flash TTS 一次 | US$0.151552 | `apps/api/app/video_speech/admin_api.py:104-113,508-515` |
| Gemini 3.8 Flash 轉錄一次 | US$1.032192 | `apps/api/app/video_speech/admin_api.py:114-129,725-737`；實際音檔另受 75 秒格式限制 |
| Jev 1.13.0 一次 | US$0.002688 | `apps/api/app/ai/jev.py:53` 的 64,000 token × `apps/api/app/video_speech/admin_api.py:130-134` 的 US$0.042／百萬輸入 token |
| Lyria 3.5 一首 | US$0.080000 | `apps/api/app/video_media/catalog.py:194-201` |

只把**無素材可重用、全部請求成功且各自達到程式所預留價格上限**作壓力測試：

- 首張正文圖 64 組，加最多 12 組角色候選圖，共 76 組：`76 × 1.035692 = US$78.712592`。
- 若沿舊企劃另容許 25 次正文圖重畫，共 101 組：`101 × 1.035692 = US$104.604892`。若放任現行 keyframes 預設每鏡 3 take，加 12 組 look，則 204 組：`204 × 1.035692 = US$211.281168`。這些是不同情境，不能相加。
- 初始旁白：`65 × 0.151552 = US$9.850880`。11 個多句請求全部落入逐句 fallback，還可能增加 `23 × 0.151552 = US$3.485696`；未計改稿重配。
- 一次逐句轉錄：`77 × 1.032192 = US$79.478784`；若 77 句全須 Jev 判，`2 × 0.002688 = US$0.005376`；一首配樂 US$0.080000。
- **僅首張 76 組＋初始 TTS＋首次逐句轉錄＋最多兩次聽音 Jev＋一首配樂的請求上限合計 US$168.127632**。它還沒有涵蓋 TTS fallback、重配／重查、重畫、正式劇本與成片其他評審、可能的定位請求、失敗且結果不明的操作，也不是預計支出。

舊 `A01-shot-plan.md` 的 US$18.45 規劃根據舊 9:02 文字與 **95 張**正文圖，將媒體 judge 以每次 US$0.01 作*估計*；沒有用後端 US$1.032192 的最壞預留，也未按目前 r16 的 64 張圖、兩個角色與 65 次 TTS 請求重算。不得以該 US$18.45 當成此次付款證明。

## 帳本保護及結論

帳本在供應商呼叫前提交單一 operation 的預留；`reserved + settled + next ceiling > 25` 時拒絕發送。`reserved`／`uncertain` 都占用上限，只有核對後的結算或有證據的未收費釋放才能回收；同一不明操作不得盲目重送（`apps/api/app/video_budget/service.py:144-251,309-364`）。這能**逐筆**防止已知報價的請求越過上限，不能保證所有計畫步驟最終都買得完。儲存庫程式對 A01 的 API 計價文字模型因無已核對最高價而拒絕派送；訂閱代理是程式允許的文字路線，正式機當下的選用與可用狀態須重新讀回設定和工作證據。既有金鑰或訂閱身分本身不證明可用權益或外部帳戶餘額（`apps/api/app/video_automation/ai.py:190-208`）。

**結論：HOLD。** 單靠離線稿及 2026-10-18 的 US$25／零預留／零結算主機快照，不能證明 2026-10-19 當下可呼叫，更不能證明完整 A01 在 US$25 內完成。上面的高額是多次「每筆最壞價」的理論加總，絕非將該總額一次預留、預計帳單或需付的現金。

## 任何新付費請求前的精確前檢

1. 鎖定已獨立審查的最終稿及 manifest；正式採用六章、公開來源與重編主張 ID 後，對**正式保存位元組**完成 verifier、listener、兩名獨立敘事讀者及 hash 綁定的 `story/reviews/script-review.json`。r16 離線畫面差異 PASS 不能替代這些收據。先核對正式 worker 已含 A01 `[7,8]` 規則和公開來源過濾。
2. 用新鮮的正式機唯讀證據核對 release／schema、104→105 稽核鏈、A01 STOP／LEASE、部署 hold／鎖、全域與 A01 running／queued／uncertain 工作、媒體資產與 speech journal；任何正在執行的付費工作或不明操作先停。2026-10-18 快照曾觀察到全域付費工作進行中；該快照已過時，不能沿用作當下放行。
3. 連續讀回同一 slug 帳戶的 `limit_usd`、`reserved_usd`、`settled_usd`、每筆 uncertain／overrun 及可用餘額；對照本機媒體 ledger 與已保存素材，確定 64 張正文圖、兩個角色 sheet、65 次 TTS／77 句轉錄有多少可以沿用。不得把已設 API key 當成供應商權益或可用額度證明。
4. 讀回 `/video/media/status`、speech/status 與自動化設定：實際 image `minimax/image-01`、judge `gemini-3.8-flash`、TTS `gemini-3.8-flash-tts`、轉錄 `gemini-3.8-flash`、Jev `jev-1.13.0`，配樂為 `gemini/lyria-3.5` 或已授權可驗 hash 的曲目；核對每月／每日額度、接入狀態與價格窗口。任何模型或計價缺失即按程式拒絕，不借用其他模型。
5. 把此次實際要買的**下一小批**列出唯一 operation ID、數量、每筆上限與可重用 cache；至少保留下一張圖及其評審的 US$1.035692 空間，其他同步請求逐筆相加。先確認 `settled + reserved + 本批各請求 ceiling ≤ US$25`，小批完成後核對帳本及素材 SHA；未知結果保持 HOLD 並核帳，不重送。確定重畫上限、TTS fallback／重配及失敗緩衝，若剩額不足完整下一階段則停下重新規劃。
6. 實測 TTS 正文 420–480 秒，檢查 1080p 聯絡表和完整成片；這些驗收不能由文字估時或帳本允許派送替代。所有正式機寫入及媒體開拍仍依本片已核准範圍與當時前檢執行。
