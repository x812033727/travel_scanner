> 2026-09-29 獨立 P1 查核已修正文稿；下方 2026-09-28 清單是原作者歷史紀錄，不代表現稿通過。現稿事實、刪除項與來源以 [verify-p1-20260929.md](verify-p1-20260929.md) 為準。第二輪覆核與站主企劃確認未完成。

# claims — ai-agents-explained-what-they-cost

一行一個可查證的說法：`id｜說法｜官方來源｜查核日｜出現的場景`。

c1｜「An agent may make several model calls while completing a task」；每次呼叫的輸入含指示、工具定義、對話歷史、使用者輸入、檔案與工具結果；「repeated calls can process a large history」｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-28｜why-expensive, bill-table, openai-quote
c2｜子代理也會呼叫模型；估算要算主代理與子代理、重試、工具、沙箱與第三方服務費用｜同上｜2026-09-28｜why-expensive, subagents
c3｜五輪帳單為示意：以 GPT-6 Sol 短脈絡牌價輸入 2、輸出 10 美元（每百萬 token）實算，假設沒有快取命中；合計輸入 40 萬、輸出 1.45 萬、約 0.95 美元；一次問答約 0.06 美元｜https://developers.openai.com/api/docs/pricing（單價）；數字為示意｜2026-09-28｜one-vs-five, bill-table
c4｜Anthropic 的區分：workflow 是預先寫好的路徑，agent 是「LLMs dynamically direct their own processes and tool usage」｜https://www.anthropic.com/engineering/building-effective-agents｜2026-09-28｜chat-vs-agent
c5｜委託前四問（權限、紀錄、停止、預算）：依 Agents API 文件，工具由開發方提供、可在後台查工作階段的回合、工具呼叫與子代理｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-28｜four-questions, logs
c6｜可設每月支出上限；硬上限會讓請求失敗，支出警示只通知｜https://help.openai.com/en/articles/9186755-managing-projects-in-the-api-platform｜2026-09-28｜budget-switch
c7｜「The Agents API currently supports data residency only in the United States and does not support Zero Data Retention (ZDR). Choosing a self-hosted sandbox does not make the Agents API ZDR-eligible.」｜https://developers.openai.com/api/docs/guides/agents-api/overview｜2026-09-28｜data-note
c8｜用量欄位是 best-effort、可能為 null、「These counts are not a final bill」｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-28｜logs

## 與企劃不同的地方

- 五輪帳單加註「假設沒有快取命中」：官方文件寫同一工作階段內的快取可以重用先前的處理，所以表格是最貴情況，旁白也這樣說。

## 我懷疑但沒動的事

- 「預算上限是唯一能自動擋住費用的東西」是站主觀點的建議語氣；官方只說硬上限會讓請求失敗。旁白以「最能救命」表述，屬意見。
- c6 的說明頁本次代理抓取可能 403，內容取自站內文章〈保護你的 AI 帳號〉2026-09-15 的查核；撰稿日用瀏覽器再確認。

## source_guide 變更（2026-09-28）

- `source_guide` 由 `ai-agents-explained` 改為 `ai-news-openai-agents-api-20260910`：main 上 Codex 的 `ai-agent-vs-chatbot` 已使用前者，產線拒收同一篇文章的第二支影片。本片的成本、紀錄、資料落地內容都出自 Agents API 那篇，說明欄第一行的連結因此也指向它。兩支影片角度不同（那支講代理與聊天機器人的差別，這支講代理的費用與委託），但第一章都談「代理跟聊天差在哪」，上架前可考慮互相連結。

## 2026-09-29 corrected claim register

- c1｜CHANGED｜多次模型呼叫、輸入包含歷史與工具內容｜每次必讀整段 → 可能反覆處理歷史，保留示意假設｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜why-expensive;bill-table;openai-quote;wrap
- c2｜CHANGED｜子代理、重試、工具、沙箱、第三方服務費須分項計算｜一定翻倍 → 實際用量加總｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜subagents;why-expensive
- c3｜CHANGED｜Sol 2/10；五輪示意 .06/.115/.18/.25/.34，合計 .945｜六輪/14,000/中文字 → 五輪/14,500/token；縮圖標為示意，未計工具等｜https://developers.openai.com/api/docs/pricing｜2026-09-29｜one-vs-five;bill-table;thumbnail
- c4｜CONFIRMED｜固定流程預設路徑、代理動態決定流程/工具｜概念性區分與官方文章相符｜https://www.anthropic.com/engineering/building-effective-agents｜2026-09-29｜chat-vs-agent
- c5｜OUT OF SCOPE｜權限、紀錄、停止、預算四問｜站主的委託建議，不當作官方強制清單｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜four-questions;logs;start-safe
- c6｜CHANGED｜OpenAI API 硬每月支出上限與警示不同｜唯一/保證即時擋住 → 硬上限須啟用，警示不擋，延遲可能少量超額｜https://developers.openai.com/api/docs/guides/spend-limits｜2026-09-29｜budget-switch;hook;wrap;youtube
- c7｜CONFIRMED｜Agents API 僅美國資料落地、不支援 ZDR，自架不改變｜投影片補產品名稱，避免被當成所有代理共同限制｜https://developers.openai.com/api/docs/guides/agents-api/overview｜2026-09-29｜data-note
- c8｜CONFIRMED｜用量是盡力記錄、可空值、非最終帳單｜未改數值/結論｜https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜logs
- a9｜CHANGED｜所有代理必須沙箱才能執行｜沙箱為程式執行方式之一；工具亦能連外部服務｜https://www.anthropic.com/engineering/building-effective-agents https://developers.openai.com/api/docs/guides/agents-api/overview｜2026-09-29｜what-makes-agent
- a10｜CHANGED｜更便宜模型倍數不變、無快取為最貴情況｜依不同輸入輸出率重算，未計工具等，不能稱最貴｜https://developers.openai.com/api/docs/pricing https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜yuae;yug2;ucxc
- a11｜OUT OF SCOPE｜會說完成不代表真的完成；權限與可查結果｜委託與驗收建議；情境不是實測｜https://www.anthropic.com/engineering/building-effective-agents｜2026-09-29｜says-done;agent-example;autonomy
- a12｜CONFIRMED｜長任務可能累計歷史；自主不保證可靠｜條件式風險陳述；沒有可靠度百分比｜https://www.anthropic.com/engineering/building-effective-agents https://developers.openai.com/api/docs/guides/agents-api/observability｜2026-09-29｜autonomy;start-safe;wrap
- a13｜CONFIRMED｜外部工具服務有各自資料規則｜概覽區分第三方工具資料邊界｜https://developers.openai.com/api/docs/guides/agents-api/overview｜2026-09-29｜data-note.dx6f
- a14｜NOT FOUND｜站內文章有完整算法與委託清單｜本輪未做正式站文章內容驗收；保留發佈前阻擋｜編輯建議或待驗內部內容｜2026-09-29｜article-cta;youtube.source_guide

## 2026-09-29 第二輪獨立查核

全部第一輪更正及隨機三分之一已確認主張完成覆核，殘留標題／說明／旁白依賴已同步修正。正式來源、逐項更正、算式及新 SHA 見 `verify-p1-20260929-round2.md`。仍有站主觀點、大綱、文章 CTA 與媒體驗收門檻，未核准製作或上架。
