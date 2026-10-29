# 10 月 28 日 AI／科技快報：Google 最強模型先不給你用、微軟一季從 OpenAI 收 100 億美元、Mac 終於能摸

企劃日期 2026-10-29。每日 AI／科技快報第一集（試做週第 1 集），照 `.agents/skills/youtube-video/references/daily-brief.md`：
`format: "slides"`、`category: "ai-news"`、slug `daily-ai-20261028`，一則一章，目標 10 分鐘（至少 8 分鐘）。
素材是站上 2026-10-28（`news_date`）已發布的 ai-news 與 tech-news（`daily_news_pick.mjs --date 2026-10-28`：32 則），
每則的事實只用站上文章與它列的官方來源；站上文章的網址放卡片 `source` 與說明欄。

## 選題

當天 32 則裡，GitHub Universe 一場發表就占了 9 則、Google 的 Carbon 與財報占 4 則；同一件事合成一則，選 7 則。
排序依：影響多少台灣觀眾 → 今天能不能做什麼 → 錢 → 資安。

| 順序 | 新聞（合併的站上文章） | 排在這裡的理由 |
| --- | --- | --- |
| 1 | Google 發表 Gemini 4 Carbon，先只給網路防禦人員；Gemini app 達 10 億使用者（`ai-news-gemini-4-carbon-20261028`、`tech-news-gemini-4-carbon-20261028`、`ai-news-alphabet-q3-earnings-gemini-carbon-20261028`） | 當天最大的 AI 新聞，而且反常：最強的模型先不給一般人。觀眾最想知道「我什麼時候能用」，答案是「還沒有時間表」，這本身就是新聞 |
| 2 | 新款 MacBook Pro：Mac 第一次支援觸控、PROLED XDR 螢幕（`tech-news-macbook-pro-proled-xdr-20261028`） | 台灣觀眾買得到的硬體，有日期有價格；但台灣在不在首批 30 個國家與地區，Apple 的說明沒列，要明說 |
| 3 | 微軟一季營收 923 億美元，其中 100 億來自 OpenAI（`ai-news-microsoft-q1-fy27-results-20261028`、`ai-news-microsoft-openai-revenue-20261028`） | 用一個數字說明 AI 的錢流到哪裡：兩家在搶同一批客戶，帳上卻綁在一起；Windows 與裝置營收下滑 22% 對一般使用者也有意思 |
| 4 | GitHub Universe：Copilot 自動幫你選模型、Enterprise 授權直接包含 Copilot、四成 pull request 由 AI 代理起草（`tech-news-github-universe-copilot-20261028`、`ai-news-github-copilot-fusion-ga-20261028`、`ai-news-github-enterprise-includes-copilot-20261028`、`tech-news-github-octoverse-2026-agents-20261028`） | 寫程式的觀眾今天就能用到；Octoverse 的「四成」是非工程師也聽得懂的一個數字 |
| 5 | Instagram 負責人說對 AI 的負面情緒會更糟，開始要求 AI 帳號自我標示（`ai-news-instagram-mosseri-ai-negativity-20261028`） | 台灣幾乎每個人都在用 Instagram；這是觀眾滑手機時會看到的改變 |
| 6 | Chrome 自動填入開始從 Gmail 帶入訂單與航班資料，先開放美國（`ai-news-chrome-autofill-gmail-20261028`） | 台灣還用不到，但它讀的是你的信箱：放在這裡講「開放之前先知道哪個開關」 |
| 7 | 南韓金融業再遭網路攻擊，大信證券外洩 3 萬餘名客戶個資（`tech-news-south-korea-finance-cyberattacks-20261028`） | 鄰國金融業連續出事，台灣觀眾能做的是檢查自己的通知與密碼；放最後，因為它跟前六則的 AI 主線不同，但跟觀眾最切身 |

不選：OpenRouter 路由、Replit ViBench、Cloud SQL 藍綠部署（只有開發者在意）；德州資料中心反彈、Meta 商業條款延後（離台灣觀眾太遠）；
XREAL AURA（台灣未上市，資訊太少）；Nvidia 轉錄模型、Anthropic AI for Science、Claude for Legal（當天容量有限，留給之後）。

## 觀眾

每天想用十分鐘跟上 AI 與科技新聞的台灣上班族與學生；用 Gemini、ChatGPT、Instagram、Chrome，有些人寫程式。
他們不想看財報與規格表，想知道「這跟我有什麼關係、我現在能不能用、要不要擔心」。

## 觀眾看完能做到的事

- 說得出 Gemini 4 Carbon 現在誰能用、一般人什麼時候能用（還沒有時間表），不被「最強模型」的標題騙去找下載（第 1 則；CITED：Google 說明與財報談話稿，站上兩篇文章）。
- 知道新款 MacBook Pro 的預購與供貨日期與美國起價，並知道台灣的上市與價格要等 Apple 台灣網站公布（第 2 則；CITED：Apple 新聞稿，站上文章）。
- 寫程式的人知道 Copilot Fusion 會自動選模型、公司若有 GitHub Enterprise 授權要問 IT 是否已含 Copilot（第 4 則；CITED：GitHub 公告，站上文章）。
- 在 Chrome 開放之前就知道「強化自動填入」讀的是 Gmail 內容、要在哪裡關（第 6 則；CITED：Google 說明，站上文章）。
- 收到疑似外洩通知時，先確認來源再改密碼（第 7 則；CITED：站上文章引用的報導）。

## 站主觀點

（試做週沒有隨啟動訊息帶進頻道立場的文字，這一段是提案，給站主在 outline 關卡看。）
今天的主線是「AI 的錢與權力集中在少數幾家，而一般人拿到的是排在最後的那一份」：Google 把最強的模型先給防禦者、微軟一季從 OpenAI 收 100 億、
GitHub 讓系統替你選模型。我不覺得這是壞事——Carbon 先給防禦者是負責任的順序——但觀眾該知道自己排在哪裡，
不要被標題的「最強」「上線」誤導。每一則我都只回答一件事：這對在台灣的你改變了什麼。答不出來的（台灣什麼時候能用、價格多少），我直接說還不知道。

## 會過期的事實

- Carbon 的開放範圍與價格（導入期每百萬輸入 token 2 美元、輸出 10 美元）會變。
- MacBook Pro 台灣上市日期與售價、Chrome 功能開放的國家。
- GitHub Enterprise 自助訂閱的開放日期（GitHub 說未來數週公布）。

## 不做的事

- 不推薦買或不買 MacBook Pro、不談股價。
- 不把公司自述的數字（10 億使用者、Cloud 成長 103%、排名第一）講成已獨立證實。
- 不示範任何攻擊手法；南韓事件只講時間、誰說了什麼、觀眾能做的防護。
