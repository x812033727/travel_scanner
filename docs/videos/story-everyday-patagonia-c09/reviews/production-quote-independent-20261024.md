# C09 v8 whole-film quote｜independent read-only arithmetic audit

2026-10-24（Asia/Taipei）。覆核者：獨立唯讀子任務 `c09_price_audit`；未開新 worktree，未呼叫付費端點，未改動稿件。範圍是[條件式報價](../production-quote.md)的張數、嘗試次數、公開價格及與現行庫內預算預留邏輯的差異。**PASS：算式與停線措辭；付費準備狀態仍 HOLD。**

| 量／費 | 獨立重算 | 結果 |
| --- | --- | --- |
| 插圖 | 67 個凍結 `shot` × 最多 3 次 | 201 次圖片請求上限 |
| MiniMax 圖片 | 201 × [官方 US$0.0035／張](https://platform.minimax.io/docs/pricing/overview) | US$0.7035 |
| 圖片評審 | 201 × 本庫 `tools/video/media/stages.mjs` US$0.01／次 | US$2.01 **內部估額**，不是 Gemini 供應商保證價 |
| 配樂 | 1 × [官方 Lyria 3.5 US$0.08／首](https://ai.google.dev/gemini-api/docs/pricing) | US$0.08 |
| 可見媒體估額 | 0.7035 + 2.01 + 0.08 | **US$2.7935**；US$25 − 2.7935 = US$22.2065，不能當作語音／轉寫已定價 |
| 逐句聲音及轉寫 | 77 句首錄＋每句最多一次有證據的重錄；每個新音檔最多一次轉寫 | 各至多 154 次；稿件 2,313 Unicode 字元非計費 token |
| Jev | 每批最多 40 行；兩輪全數疑點時各 2 批 | 最多 4 批。依[官方 US$0.042／百萬輸入 token](https://typesafe.ai/blog/introducing-system-one-models-and-jev)及本庫 64,000 token／批預留，4 × 0.002688 = US$0.010752 預留 |

本庫 `apps/api/app/video_speech/admin_api.py` 對 Gemini 3.8 Flash TTS 每次預留 US$0.151552；154 次完整預留的機械乘積是 US$23.339008。轉寫每次預留 US$1.032192，154 次為 US$158.957568；`apps/api/app/video_media/admin_api.py` 圖審每次也可預留 US$1.032192，201 次為 US$207.470592。這些是模型請求的**保守安全預留**，不是預測帳單；但足以證明各項最大嘗試次數不能當作 US$25 下的保證供貨量。正確條件是逐筆先預留、用供應商 token 結算，未知結果保留全額，餘額不足停止。Google 的 TTS、Gemini 3.8 Flash token 單價見[官方 Gemini API 價目](https://ai.google.dev/gemini-api/docs/pricing)。

現行本庫 `apps/api/app/video_budget/models.py` 的 `C_SERIES_PILOT_LIMITS_USD` 未列 C09；`service.py` 對所有 `story-everyday-` 付費請求均維持 `video_budget_preproduction_hold`。本機無 C09 媒體帳本，正式帳號／資料庫與舊費用未讀回；這些觀察不能證明歷史花費是零。報價尚未獲站主整支付費核准，實測正文語音是否達 480 秒也未知。故**不核准任何首筆付費呼叫**。
