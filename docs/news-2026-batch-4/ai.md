# 補充規格：AI 新聞（補到 9/16 與 1/1 起補漏）

先讀 [`BRIEF.md`](BRIEF.md)。這份只寫 AI 垂直**才有**的規則。

工作區 `docs/ai-news-2026-09-late/`，slug 前綴 `ai-news-`，
`topics` 是 `["ai", <橫向主題>, "ai-news"]`。

## 這一批和前三批的關係

站上已經有 38 篇 `ai-news-*`（事件日 2026-01-05 → 2026-09-14）與月份索引
`ai-news-2026-january-september-index`。**1/1 到 9/14 的 AI 重要新聞實質上已經做完了。**

這一批只補兩種：

1. **9/15–9/16 的缺口。** 既有內容查核止於 2026-09-15。
2. **1/1 起真正沒寫過的事件。** 動筆前**必讀既有索引的 38 篇標題**，
   確認題目沒有被寫過。批次 3 的 BRIEF 已經有這條規則
   （「不要重寫同一件事，例如 GPT-Live 篇不要重講 ChatGPT Work」），這裡再強調一次，
   因為補漏批次最容易踩到。

`display_order` 從 **148** 之後接續（148 是 `ai-news-siri-ai-ios-27-20260914`）。

## 索引要改，但 slug 不能改

`ai-news-2026-january-september-index` 的 slug **永遠不動**
（`docs/article-architecture.md`：「全部既有 URL 不變」）。

要改的是它的 title、description 與月份表格。兩個陷阱：

### 1. 標題裡的日期會過期

現在寫「1 月 1 日至 9 月 14 日」。加了 9/15 之後就是錯的。
建議改成不帶日的「1 月至 9 月」，這樣下次補到 9 月底還是對的。

### 2. 篇數是「會一直增加的數字」

description 現在寫「38 則」、正文寫「三十八則」。
站主 2026-09-16 的決定是**讀者看得到的地方一律不顯示會增加的數字**
（`docs/article-architecture.md` Phase 5：「顯示出來就一直是錯的」）。
所以正確做法是**把篇數拿掉**，不是把 38 改成 42。

### 3. 改標題會波及既有文章的連結文字

`ArticleInline` 的 `text` 是凍進內容包、原樣渲染的（這正是
`tasks/open/2026-09-16-retitled-guides-stale-link-text.md` 在處理的問題），
而 `check_article.py` 會斷言 `link.text == 目標的 title`。

索引標題一改，**所有指向它的既有文章的連結文字就全部過期**。
**2026-09-16 實測：30 個內容包、142 份語系文件**帶著指向這個索引的 `article` inline。
動手前重數一次（內容會變），並在票的 scope 裡把那 30 個 slug 逐一列出。
改的時候**走 JSON 結構**（只換 `inlines[].text` 中 `slug` 等於索引的那些），
**絕對不要對檔案下正規表示式**——各批次的欄位順序不一樣。

## 沒有免責 callout，B8 也一樣

AI 篇不帶 `finance` 主題，不要加投資免責。照 `BRIEF.md` 放一個一般 `callout`。

**`ai-news-chatgpt-financial-services-20260910`（B8）是唯一會讓人猶豫的一篇，它也照這條走。**
理由是主題該怎麼掛看的是文章在寫什麼，不是標題裡有沒有「financial」：
那篇寫的是 OpenAI 推出一個給金融機構用的產品，不是教讀者怎麼處理自己的錢。
掛上 `finance` 會讓一篇 AI 新聞出現在理財專區，那是分類錯誤，
而且會連帶觸發 `finance_no_disclaimer`（error 級）去要求一段它不需要的投資免責。

但這個題目**確實容易被讀成投資內容**，所以那篇的一般 `callout` 要明講：
本文寫的是一個給金融機構的工具，本站沒有試用，也不是投資建議。
用一般 callout 講清楚，而不是靠掛 `finance` 去換樣板。

**如果撰稿時發現文章實際寫進了「這個工具會產出什麼估值／建議」那類內容，
那就不再只是產品新聞，要停下來重新判斷主題與免責，不要自己改規則。**

## 既有篇目（動筆前逐一比對）

這張表是從 `apps/api/app/guides/content/ai-news-*.json` 的 slug 與 zh-TW title 直接產生的，
不是手抄的。要引用任何一篇的內容，讀那個內容包本身，不要只看標題。

| 事件日 | slug | 標題 |
| --- | --- | --- |
| 2026-01-05 | `ai-news-nvidia-rubin-20260105` | NVIDIA Rubin 在 CES 亮相：AI 算力升級會如何影響日常服務？ |
| 2026-01-07 | `ai-news-chatgpt-health-20260107` | ChatGPT Health 年初登場：整理健康資料之前先看懂用途與界線 |
| 2026-01-14 | `ai-news-gemini-personal-intelligence-20260114` | Gemini Personal Intelligence：AI 連結郵件與相簿後，便利從哪裡來？ |
| 2026-02-05 | `ai-news-claude-opus-46-20260205` | Claude Opus 4.6 與長上下文：大量資料讀得進去，也要找得回來 |
| 2026-02-05 | `ai-news-gpt-53-codex-20260205` | GPT-5.3-Codex 推出：AI 寫程式如何走向可交付的工作？ |
| 2026-02-16 | `ai-news-qwen-35-20260216` | Qwen3.5 開放權重：可下載模型，與能在自己電腦運作差在哪？ |
| 2026-02-19 | `ai-news-gemini-31-pro-20260219` | Gemini 3.1 Pro 發布：複雜問題如何轉成可驗證的答案？ |
| 2026-03-05 | `ai-news-gpt-54-20260305` | GPT-5.4 把推理與電腦操作放在一起：一般工作者該怎麼看？ |
| 2026-03-12 | `ai-news-claude-interactive-visuals-20260312` | Claude 對話開始畫互動圖：看懂概念之前，先看懂圖的假設 |
| 2026-03-25 | `ai-news-lyria-3-pro-20260325` | Lyria 3 Pro 延長 AI 音樂創作：從短片段到有段落的作品 |
| 2026-04-07 | `ai-news-project-glasswing-20260407` | Project Glasswing 與 Mythos Preview：AI 找到漏洞後，真正的工作才開始 |
| 2026-04-08 | `ai-news-meta-muse-spark-20260408` | Meta Muse Spark 登場：社群裡的 AI 助手如何改變搜尋與提問？ |
| 2026-04-21 | `ai-news-chatgpt-images-20-20260421` | ChatGPT Images 2.0：圖像開始加入思考，設計需求也要更清楚 |
| 2026-04-23 | `ai-news-gpt-55-20260423` | GPT-5.5 走向多步驟工作：把模糊需求變成能驗收的交付 |
| 2026-05-19 | `ai-news-gemini-omni-20260519` | Gemini Omni 在 I/O 亮相：用對話改影片，素材與連續性仍要自己把關 |
| 2026-05-19 | `ai-news-gemini-spark-20260519` | Gemini Spark 與 Daily Brief：AI 從晨間摘要走向背景辦事 |
| 2026-06-09 | `ai-news-claude-fable-5-access-20260609` | Claude Fable 5 的發布、暫停與恢復：AI 服務可用性也是選擇條件 |
| 2026-06-26 | `ai-news-gpt-56-sol-preview-20260626` | GPT-5.6 Sol 從有限預覽開始：模型發表與人人可用為何不同？ |
| 2026-06-30 | `ai-news-claude-sonnet-5-20260630` | Claude Sonnet 5：能力與成本之間，怎麼找日常工作的平衡？ |
| 2026-07-08 | `ai-news-gpt-live-voice-20260708` | GPT-Live 讓 ChatGPT 語音邊聽邊說：插話、方案用量與錄音設定 |
| 2026-07-09 | `ai-news-chatgpt-work-20260709` | ChatGPT Work 正式亮相：如何把跨檔案工作交代清楚？ |
| 2026-07-21 | `ai-news-gemini-36-flash-20260721` | Gemini 3.6 Flash 與 Flash-Lite：快速模型該如何分工？ |
| 2026-07-24 | `ai-news-claude-opus-5-20260724` | Claude Opus 5 推出：一般工作使用者值得注意哪些改變？ |
| 2026-07-30 | `ai-news-gpt-56-price-cut-20260730` | GPT-5.6 Luna、Terra 降價：哪些使用成本受到影響？ |
| 2026-08-02 | `ai-news-eu-transparency-20260802` | 歐盟 AI 透明度規則上路：聊天機器人與生成內容如何標示？ |
| 2026-08-06 | `ai-news-chatgpt-free-thinking-20260806` | ChatGPT 免費版與思考功能更新：日常使用有什麼不同？ |
| 2026-08-26 | `ai-news-gemini-live-20260826` | Gemini Live 生產力更新：用語音處理郵件與待辦 |
| 2026-09-01 | `ai-news-claude-fable-51-20260901` | Claude Fable 5.1 與 Mythos 5.1：功能、開放對象與限制 |
| 2026-09-02 | `ai-news-gemini-38-flash-20260902` | Gemini 3.8 Flash 推出：模型升級對日常工具意味著什麼？ |
| 2026-09-03 | `ai-news-gpt-6-astra-20260903` | GPT-6 Astra 發布：從回答問題到完成電腦工作 |
| 2026-09-04 | `ai-news-google-assistant-gemini-20260904` | Google Assistant 退場、Gemini 接手：手機、手錶與車上換手前後要檢查什麼 |
| 2026-09-04 | `ai-news-lyria-35-gemini-20260904` | Lyria 3.5 進入 Gemini：AI 音樂創作有哪些新選擇？ |
| 2026-09-08 | `ai-news-chatgpt-images-25-20260908` | ChatGPT Images 2.5：圖片生成、局部修改與草圖功能更新 |
| 2026-09-10 | `ai-news-anthropic-threat-report-20260910` | Anthropic 九月威脅情報報告：七類 AI 濫用與被盯上的 API 金鑰 |
| 2026-09-10 | `ai-news-deepseek-v41-flash-20260910` | DeepSeek-V4.1-Flash 上線、V4-Pro 去留有兩種說法：模型換手時該注意什麼 |
| 2026-09-10 | `ai-news-openai-agents-api-20260910` | OpenAI Agents API 公開 beta：委託 AI 自動化前，先看懂計費與資料位置 |
| 2026-09-12 | `ai-news-pace-the-frontier-20260912` | Amodei 呼籲放慢前沿 AI：〈We Must Pace the Frontier〉的主張與界線 |
| 2026-09-14 | `ai-news-siri-ai-ios-27-20260914` | Siri AI 隨 iOS 27 推出：先上英文 beta，台灣 iPhone 使用者能用到什麼？ |
