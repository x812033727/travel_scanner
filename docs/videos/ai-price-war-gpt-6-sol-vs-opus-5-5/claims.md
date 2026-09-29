> 2026-09-29 獨立 P1 查核已修正文稿；下方 2026-09-28 清單是原作者歷史紀錄，不代表現稿通過。現稿事實、刪除項與來源以 [verify-p1-20260929.md](verify-p1-20260929.md) 為準。第二輪覆核與站主企劃確認未完成。

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

## 2026-09-29 corrected claim register

- c1｜CONFIRMED｜Sol 標準短脈絡輸入/輸出 2/10 美元每 MTok｜未改數值｜https://developers.openai.com/api/docs/pricing｜2026-09-29｜three-list-prices; monthly-bill
- c2｜CONFIRMED｜Luna 輸入/快取讀取/輸出 .10/.01/.50｜未改數值｜https://developers.openai.com/api/docs/pricing｜2026-09-29｜three-list-prices; monthly-bill
- c3｜CONFIRMED｜Opus 5.5 輸入/快取讀取/輸出 4/.20/20｜未改數值｜https://claude.com/pricing｜2026-09-29｜three-list-prices; monthly-bill
- c4｜CHANGED｜Sol 比前代促銷單價少 50%；兩家公司同日發布｜改以 Sep 22 更新紀錄和 4→2、20→10 實算；移除未重新核實的發布文引語與 Luna 降幅宣稱｜https://developers.openai.com/api/docs/changelog https://developers.openai.com/api/docs/pricing https://www.anthropic.com/claude-opus-5-5｜2026-09-29｜ayvr; openai-quote; recap-three; youtube
- c5｜CHANGED｜Opus 輸入輸出少 20%、快取讀取少 60%；40% 是廠商預設工作量成本估計｜費用估算與單價無關 → 同時取決於各費率和 token 用量｜https://www.anthropic.com/claude-opus-5-5｜2026-09-29｜anthropic-quote; real-list-cut; what-percent-means
- c6｜CONFIRMED｜Sol、Opus 5.5 快取讀取同為 .20｜限定這兩模型及標準短脈絡｜https://developers.openai.com/api/docs/pricing https://claude.com/pricing｜2026-09-29｜output-is-the-gap; monthly-bill
- c7｜CONFIRMED｜Flash 3.8 .75/.075/3.75；促銷至 2026-12-31｜未改數值｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-29｜monthly-bill; gemini-flash-note
- c8｜CONFIRMED｜Opus 5 歷史對照 5/.50/25｜今日兩份官方資料直接列出，已不必只靠百分比反推｜https://claude.com/pricing https://www.anthropic.com/claude-opus-5-5｜2026-09-29｜compare-to-last-gen
- c9｜CHANGED｜Sol 代理 token 費 73.6；輸出 40 為 54.35%、快取 9.6 為 13.04%｜算式正確；把通用結論限縮為這組 Sol 用量｜https://developers.openai.com/api/docs/pricing｜2026-09-29｜output-share; scenario-walk
- c10｜OUT OF SCOPE｜每月 30 美元是否值得換模型｜條件式建議，非省錢承諾；需站主確認建議措辭｜https://developers.openai.com/api/docs/pricing｜2026-09-29｜thirty-dollar-case; switch-or-not
- c11｜CONFIRMED｜Flash 3.8 2027-01-01 變為 1.50/.15/7.50｜當日官方日期；上片前仍須重查｜https://ai.google.dev/gemini-api/docs/pricing｜2026-09-29｜gemini-flash-note; monthly-bill
- p12｜CONFIRMED｜Sonnet 5 輸入/快取讀取/輸出 2/.20/10｜官方 legacy 表仍列；不是 Sonnet 5.5 的誤植｜https://claude.com/pricing｜2026-09-29｜monthly-bill
- p13｜CHANGED｜聊天/代理/大量整理 15 格 token 費｜數值全可重算；排名三欄皆 Luna 最低；大量整理不是 Batch API 折扣｜https://developers.openai.com/api/docs/pricing https://claude.com/pricing https://ai.google.dev/gemini-api/docs/pricing｜2026-09-29｜monthly-bill; scenario-walk
- p14｜CHANGED｜Opus 對照 184→137.6，降 25.217%；Sol 聊天 40→20｜口播 180 → 184，圖上138為四捨五入｜https://developers.openai.com/api/docs/pricing https://claude.com/pricing｜2026-09-29｜compare-to-last-gen;68yw
- p15｜CHANGED｜token 與中文字數、可計價輸入輸出｜字數 → token；不宣稱一字一 token｜https://developers.openai.com/api/docs/pricing https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜three-tokens;kpte;4dsr;3rsz
- p16｜CHANGED｜同文件重問不保證快取命中；歷史不一定整段重送｜加入相同前綴、有效快取條件；每轮必重讀 → 可能｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜cache-example;why-agent-costs
- p17｜CHANGED｜費率期限、長脈絡與未列費用｜牌價不保證長期固定；長脈絡依模型；未含寫入/儲存/工具等｜https://developers.openai.com/api/docs/pricing https://ai.google.dev/gemini-api/docs/pricing｜2026-09-29｜three-words;short-context-note;youtube
- p18｜CHANGED｜不存在三種都最省的模型、聊天只看輸入｜與本片表格矛盾 → Luna 三欄最低，品質需另測，三種用量均需算｜https://developers.openai.com/api/docs/pricing https://claude.com/pricing https://ai.google.dev/gemini-api/docs/pricing｜2026-09-29｜gcyy;6mvh;j9h8;output-is-the-gap
- p19｜OUT OF SCOPE｜簡單任務選便宜模型、50/30 美元是否值得切換｜編輯建議而非測試結論；沒有獨立性能評測｜編輯建議或待驗內部內容｜2026-09-29｜luna-enough;switch-or-not;thirty-dollar-case;wrap
- p20｜NOT FOUND｜站內文章包含計算表且持續更新｜本輪未上正式站核對文章內容與更新承諾；不得當作已完成發佈驗收｜編輯建議或待驗內部內容｜2026-09-29｜article-cta;youtube.source_guide

## 2026-09-29 第二輪獨立查核

全部第一輪更正及隨機三分之一已確認主張完成覆核，殘留標題／說明／旁白依賴已同步修正。正式來源、逐項更正、算式及新 SHA 見 `verify-p1-20260929-round2.md`。仍有站主觀點、大綱、文章 CTA 與媒體驗收門檻，未核准製作或上架。
