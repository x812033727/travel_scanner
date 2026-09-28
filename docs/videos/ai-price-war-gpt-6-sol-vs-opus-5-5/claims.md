# claims — ai-price-war-gpt-6-sol-vs-opus-5-5

一行一個可查證的說法：`id｜說法｜官方來源｜查核日｜出現的場景`。金額都是每百萬 token、短脈絡、標準處理、美元；情境帳單為官方單價實算。

c1｜GPT-6 Sol 輸入 2、輸出 10｜https://developers.openai.com/api/docs/pricing｜2026-09-28｜three-list-prices, monthly-bill
c2｜GPT-6 Luna 輸入 0.10、輸出 0.50（快取讀取 0.01）｜https://developers.openai.com/api/docs/pricing｜2026-09-28｜three-list-prices, monthly-bill
c3｜Claude Opus 5.5 輸入 4、輸出 20、快取讀取 0.20｜https://www.anthropic.com/pricing｜2026-09-28｜three-list-prices, monthly-bill
c4｜OpenAI：便宜 50% 比的是 GPT-5.6 促銷價，不是原價｜https://openai.com/index/introducing-gpt-6-sol-and-luna/｜2026-09-28｜openai-quote
c5｜Opus 5.5 輸入與輸出牌價比 Opus 5 少 20%；快取讀取少 60%；「40% less to run」是預設設定、一般工作負載下的成本估計｜https://www.anthropic.com/claude-opus-5-5｜2026-09-28｜real-list-cut, anthropic-quote, compare-to-last-gen
c6｜Sol 與 Opus 5.5 的快取讀取都是 0.20｜https://developers.openai.com/api/docs/pricing 、 https://www.anthropic.com/pricing｜2026-09-28｜output-is-the-gap, monthly-bill
c7｜Gemini 3.8 Flash 輸入 0.75、輸出 3.75、快取 0.075，促銷價至 2026-12-31｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-28｜monthly-bill, gemini-flash-note
c8｜Opus 5（對照）輸入 5、輸出 25、快取讀取 0.50；由官方 20%／60% 降幅反推，正式站文章亦記此值｜https://www.anthropic.com/claude-opus-5-5｜2026-09-28｜compare-to-last-gen, anthropic-quote
c9｜代理型情境（1,200 萬新輸入、4,800 萬快取讀取、400 萬輸出）GPT-6 Sol 帳單 73.6 美元，其中輸出 40 佔 54%、快取讀取 9.6 佔 13%｜實算自 c1、c6｜2026-09-28｜output-share
c10｜小用量換模型每月只省幾塊：以每月 30 美元帳單為例的說明性判斷，非單一官方數字｜實算自 c1–c3｜2026-09-28｜thirty-dollar-case
c11｜Gemini 3.8 Flash 目前價為促銷價，2027-01-01 起漲為 1.50／7.50｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-28｜monthly-bill, gemini-flash-note

## 與企劃不同的地方

- 無。腳本照 brief 的選項 A（推薦）與示範表，未改角度或章節。

## 我懷疑但沒動的事

- Opus 5 是否仍列在 anthropic.com/pricing 的可見表上：2026-09-28 我抓到的頁面只列 Fable 5.1、Opus 5.5、Sonnet 5、Haiku 4.5，沒看到 Opus 5。腳本只在對照用到 Opus 5 的 5／25／0.50，這三個數字可由官方明載的「輸入輸出少 20%、快取讀取少 60%」反推，正式站文章也記此值，故保留並在 c8 註明來源為反推。撰稿日若頁面已明確下架 Opus 5，維持反推並保留註記即可。
- 表格金額四捨五入到易讀位數（73.6→$74、137.6→$138、3.68→$3.7、27.6→$28、187.5→$188）；精確值在 c9 與說明欄文章。
