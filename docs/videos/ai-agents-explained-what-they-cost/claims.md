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
