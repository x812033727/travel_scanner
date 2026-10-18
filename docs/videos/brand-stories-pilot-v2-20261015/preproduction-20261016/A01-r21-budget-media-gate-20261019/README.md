# A01 r21 離線媒體與費用前檢 — HOLD

2026-10-19；僅讀取儲存庫及既有公開安全的唯讀收據，沒有連線正式機、供應商或帳戶，沒有送出付費請求。版本錨點：`A01-editorial-candidate-20261019-r21/manifest.json` SHA-256 `5131d53cef6f20184c1d5043cf63428602deb1551ffb9808ca42e940f190e900`；其 `candidate/video.json` SHA-256 `a9bdaa89d82c7d2a7e0d718ad02f41533d0412ac75841a9520ca7abe8a7f2eae`。`build.mjs --check` 回報 `OFFLINE_MECHANICAL_ONLY_HOLD_PENDING_R21_REVIEW`。下列計算只適用於這份離線候選，不表示正式機已採用或可開拍。r21 的 `turn-plan` 年份依據仍待釐清，獨立史料／故事審查及正式審稿收據關卡未完成。

## 靜態呼叫數與路線

| 項目 | r21 離線盤點 |
| --- | --- |
| 畫面 | 65 鏡：64 個 `shot` 均為 `still`、1 個 `outro`；0 生成 clip、0 end frame。`series.json` 指定 MiniMax `image-01`。 |
| 角色造型 | 2 個角色。若沒有經雜湊核對、同系列且已核准的 sheet，`look` 預設每角 3 候選、最多 2 輪，即最多 12 張圖及相應 judge；見 `tools/video/media/look.mjs`。 |
| 正文插圖 | 首張 64 張；`keyframes` 的程式預設每鏡最多 3 take，故最多 192 張及相應 judge。舊企劃的 25 張重畫上限不是程式硬上限；見 `tools/video/media/keyframes.mjs`。 |
| 中文旁白 | 77 句。以 r21 `candidate/video.json` 和 `candidate/lexicon.json` 實跑 `planRequests` 為 65 個初始 Gemini TTS 請求、2,463 個預估計費字元、0 個 `audio_ref`。11 個多句請求若全部切分失敗，最多再送 23 個逐句 fallback 請求；重配另計。 |
| 首輪聽音 | `check-audio` 按 77 句各轉錄一次；不符的句子才交 Jev，最多 40 句一批，極端 77 句全不符為 2 批。第二意見、重配、重查另計。 |
| 音樂 | 候選設定 `music.prompt`，未指定已有授權且已驗 hash 的 `music.track`；若維持此稿，需一首 Lyria 3.5。 |

數量演算法錨點：`tools/video/core/drama.mjs:196,312`（每角預設 3 候選）、`tools/video/media/look.mjs:23,108-111,162-208`（2 輪及限量選項）、`tools/video/media/keyframes.mjs:28,426-439,471-472`（每鏡 take 與正文圖；風格 plate 只屬投影片）、`tools/video/tts/requests.mjs:82-123` 與 `tts/synthesis.mjs:99-122`（請求、切分 fallback）、`tools/video/tts/check.mjs:56,299-375`（逐句轉錄及 40 句 Jev 批次）。65／77／2、`still`、音樂及來源數則直接取自上述 r21 候選；本報告沒有改變它的稿件或 manifest。

## 逐次最高預留，不是預計實支

現行程式的 A01 v2 帳戶上限為 **US$25**（`apps/api/app/video_budget/models.py`），所列價錢有效期寫到 2026-12-31（`video_budget/prices.py`），正式操作前仍須核對部署版本與模型。依 `video_media/catalog.py`、`video_media/admin_api.py`、`video_speech/admin_api.py` 的試作報價，單次最高預留為：MiniMax 圖 **$0.003500**；Gemini 圖片 judge 或定位 **$1.032192**；圖加 judge **$1.035692**；Gemini TTS **$0.151552**；Gemini 逐句轉錄 **$1.032192**；Jev **$0.002688**；Lyria 一首 **$0.080000**。judge／轉錄上限按模型完整 token 極值保守預留，不能把它當成實際帳單。

價格錨點：`apps/api/app/video_budget/models.py:33,46-53`、`video_budget/prices.py:10-14`、`video_media/catalog.py:99-107,194-201`、`video_media/admin_api.py:107-118,403-425`、`video_speech/admin_api.py:104-134,508-515,725-737,820-827`。帳本將 `reserved` 與 `uncertain` 都算入預留，見 `video_budget/service.py:34,129,144-226`。

- 完全沒有可重用素材，且每次請求均結算在最高預留時，首輪 64 張正文圖與最多 12 張造型圖、65 次 TTS、77 次轉錄、最多 2 次 Jev、一首音樂合計 **$168.127632**。這是分散於許多操作的壓力測試，**不是一次性預留，也不是預計花費**；未含 TTS fallback、改稿重配、第二意見、重畫、定位、其他評審及結果不明的請求。
- 最多 23 次 TTS fallback 另增加 **$3.485696** 的逐次上限。若只跑第一張正文圖與配對評審，單組上限 **$1.035692**；64 組為 **$66.284288**。角色預設 12 組為 **$12.428304**；若正文照每鏡 3 take 跑滿，192 組為 **$198.852864**。不同情境不要相加當成預算。
- 儲存庫帳本在每次供應商呼叫前檢查 `已結算 + 已預留（含結果不明） + 本次最高價 ≤ $25`，超出便拒絕派送；詳見 `video_budget/service.py`。它保護逐次派送，**不能證明整集能在 $25 內完成**。訂閱、已設定金鑰與舊 $18.45 企劃也不能替代此次實際帳本／可用權益讀回。

## 可重用素材：已知與未知

公開安全的 [2026-10-17 A01 唯讀收據](../A01-live-readback-20261017.md)當時觀察到 0 筆 A01 媒體工作、0 筆本片預算操作；其路徑清單也沒有常見媒體副檔名。這份清單並非完整語意媒體庫存，也已過期。**目前沒有一張可據此確認適用 r21 的已付費造型／插圖、TTS take、轉錄或音樂**；不等於證明這些素材在任何位置都不存在。開拍前須在新的唯讀主機前檢中比對本片 `media/cache.json`、`media/ledger.json`、`media/jobs.json`、speech journal、實際媒體檔 SHA、審核版次、工作 ID 與伺服器收據；不明工作不可盲重送。

## 僅在正式關卡全部通過後可考慮的小批次

1. 先完成 r21 事實及敘事獨立審查、正式六章與 104→105 銜接、公開來源過濾、`story/reviews/script-review.json`、目前 worker 的 A01 7–8 分鐘規則，以及正式機無 hold／鎖／執行中或結果不明的付費工作之新鮮前檢。此離線報告本身不放行任何一項。
2. 核對正式機實際選用的 MiniMax 圖、Gemini judge／TTS／轉錄、Jev、音樂模型、計價窗口、每月額度、本片 $25 的 `settled`／`reserved`／`uncertain`、既有可重用素材及唯一 operation ID。任一價格或雜湊不符即停。
3. 如需新造型且使用可選角色的手動 `look` 路線，第一批只做**一名角色、每輪一候選**。`--character` 加 `--candidates 1` 在現行程式最多自動跑 2 輪，最多 2 組圖加 judge，最高預留 **$2.071384**；第一輪通過則只需 1 組。每一呼叫仍按獨立 operation ID 預留。若正式 worker 路線無法精確限制該批數量，就先不要啟動整個自動 stage，改由審核過的限量控制器處理。
4. 一批完成後，讀回預算操作、伺服器 job、在地 ledger、快取及媒體 SHA。保留未結算／uncertain 上限，結果不明立即 HOLD 並核帳。兩角造型經審核後，才考慮 TTS／圖片；`tts` 現行 CLI 沒有逐句首輪選項，`check-audio` 也逐句巡遍全稿，不能口頭保證它們是單次小批。若要保證 TTS 整輪含最壞 fallback 可跑完，當時其他保留額外，至少需 **$13.336576** 可用最高價空間；逐句轉錄 77 次最高價共 **$79.478784**，依 $25 上限無法預先保證全輪完成。可用實際結算與續跑證據逐段推進，但不得越過 ledger 或對未知操作重送。
5. 實際 TTS 與剪輯要量到正文 420–480 秒，再驗 1080p 插圖聯絡表、可關閉的繁中 CC、完整成片與站主看片。文字估時及帳本可派送均不等於成片通過。

**狀態：HOLD。** 這份文件只提供 r21 離線成本和首批風險界線，沒有驗證供應商可用額度、正式機即時狀態或任何付費素材。
