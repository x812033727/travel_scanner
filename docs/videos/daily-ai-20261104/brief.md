# Tech Signal 11/4：Anthropic 的算力帳單

企劃日期 2026-11-03。每日 Podcast《Tech Signal｜科技訊號》，照 `.agents/skills/youtube-video/references/daily-brief.md`：
`format: "slides"`、`category: "ai-news"`、`theme: "paper"`，slug `daily-ai-20261104`（播出 2026-11-04 星期三，新聞日 2026-11-03），
雙主持（Sola 講新聞、Kai 替觀眾問與翻白話），台灣國語旁白、字卡全英文，目標 20–25 分鐘，沒有開場濃縮（影片從片頭動畫接 Intro）。
這一集在工作階段裡手做。每則的事實只用站上 news_date 2026-11-03 已發布的文章與它列的來源（2026-11-03 以
`/api/travel/guides/life/<slug>?locale=zh-TW` 取得，17 篇皆 HTTP 200），沒有用到網路補充的新聞；站上文章網址放說明欄，卡片 `source` 寫原始來源。
選題依編輯指示（站主 2026-11-03：國際新聞為主，台灣新聞最多一則、不當主題）。

## 選題

排序依：影響多少台灣觀眾 → 今天能不能做什麼、有沒有日期 → 錢與帳戶安全 → 其他。同一件事的兩篇（FlashProve、Claude 文字浮水印）合成一則「證明 AI 寫了什麼」。

| 段落 | 新聞（來源：站上文章；原始來源） | 排在這裡的理由 |
| --- | --- | --- |
| Signal of the Day | Anthropic 更新 S-1：季度營收 170 億美元（前一季 115 億），運算占營收 48%→58%，營運虧損擴大（https://mokaair.com/zh-TW/life/ai-news-anthropic-compute-costs-20261103 ；TechCrunch）。錢的流向接：AMD 第三季資料中心 +97%（https://mokaair.com/zh-TW/life/tech-news-amd-q3-2026-results-20261103 ；AMD 新聞稿）、Fal 估值翻倍但毛利薄（https://mokaair.com/zh-TW/life/ai-news-fal-valuation-20261103 ；TechCrunch）、資料中心改用噴射引擎發電（https://mokaair.com/zh-TW/life/ai-news-data-center-jet-engine-power-20261103 ；TechCrunch） | 理由見下一節 |
| Headlines 1 | OpenAI 稱 ChatGPT 搜尋量約為 Google 的五分之一；ChatGPT 廣告將放贊助產品圖片（https://mokaair.com/zh-TW/life/ai-news-chatgpt-search-share-20261103 ；The Verge） | 台灣最多人用的 AI 服務，也是每天的搜尋習慣；數字是 OpenAI 自己說、Google 那邊來源不明，要講清楚 |
| Headlines 2 | Google 亞太反詐騙：Android 偽冒來電偵測、Pixel 詐騙警示、600 萬美元教育資助（https://mokaair.com/zh-TW/life/tech-news-google-apac-scams-20261103 ；Google 部落格） | 跟台灣聽眾最直接的一則（亞太、Android、Be Scam Ready 台灣已上線），又有今天能做的事（接 Try This）；不是台灣新聞，是區域新聞；全是 Google 自述 |
| Headlines 3 | 蘋果：約會與浪漫關係功能的 App 一律 18+，11/16 起補內容描述（https://mokaair.com/zh-TW/life/ai-news-apple-18-plus-ai-companions-20261103 ；TechCrunch） | 有日期，關係到家長與用 iPhone 的孩子；執行方式報導沒說 |
| Headlines 4 | 證明 AI 寫了什麼：Anthropic FlashProve 開源原型（https://mokaair.com/zh-TW/life/ai-news-anthropic-flashprove-20261103 ；Anthropic 研究文章、TechCrunch）＋ Claude 三個模型的文字浮水印（https://mokaair.com/zh-TW/life/ai-news-claude-text-watermark-20261103 ；Claude Platform 發行說明） | 合成一則；觀念值得講，但一個是研究原型、一個有平台與設定的例外，觀眾今天用不到，排中間 |
| Headlines 5 | GitBook 遭使用 AI 代理的攻擊，客戶須更換權杖（https://mokaair.com/zh-TW/life/crypto-news-gitbook-ai-agent-breach-20261103 ；Decrypt） | AI 代理被拿來攻擊的實例；直接影響的是用 GitBook 的開發者與加密專案，一般人較遠 |
| Headlines 6 | Netflix 電視版實驗性 AI Discover 分頁（https://mokaair.com/zh-TW/life/ai-news-netflix-ai-discover-20261103 ；The Verge） | 好懂、輕鬆，但只在美國、英文、支援的電視，台灣看不到，排最後 |
| Signal Number | 58%：Anthropic 營收用在運算的比例（同主題的站上文章；TechCrunch） | 今天最好記、也最能接到主題的一個數字；放在 Headlines 結尾當主題的引子，主題段只用「還記得剛剛那個訊號數字」回扣，不重講 |
| What People Are Saying | TechCrunch 記者 Russell Brandom（毛利變差）、Rystad Energy 分析師（盡快拿到電，經 TechCrunch 引紐約時報）、NAACP 的 Abre' Conner（改名解決不了問題，經 The Verge；https://mokaair.com/zh-TW/life/ai-news-openai-compute-campuses-20261103）、OpenAI 的 Adam Fry（多數人不介意廣告，經 The Verge） | 四句都是站上文章列的原始來源裡的原文：算力、電力、資料中心改名、廣告，正好把主題和 Headlines 1 串起來 |
| Money Signal | 北韓否認涉及幣安遭駭、幣安的備付證明（https://mokaair.com/zh-TW/life/crypto-news-binance-hack-north-korea-denial-20261103 ；Decrypt）；Tesla、SpaceX 等 56 家公司反對 OKX-ICE 代幣化股票平台（https://mokaair.com/zh-TW/life/crypto-news-okx-ice-tokenized-stock-objections-20261103 ；Decrypt）；金管會預告穩定幣發行許可辦法草案（https://mokaair.com/zh-TW/life/crypto-news-taiwan-stablecoin-rules-20261103 ；金管會新聞稿） | 交易所遭駭是「帳戶安全」；代幣化股票是發行公司說不的權利；穩定幣草案是本集唯一的台灣新聞，放 Money Signal 最後、不當主題。只講規則與誰說了什麼，不談價格、漲跌、買賣 |
| Try This | 接到熟悉聲音的求救電話：掛掉回撥、Android 設定搜尋「詐騙」、Be Scam Ready（台灣已有）；家長自己設家長控制（Google 部落格、TechCrunch＋節目建議） | Headlines 2 有觀眾今天就能做的事；標明是節目建議 |
| Noise of the Day | Steam 審核積壓，開發者猜是 AI 粗製遊戲塞爆（https://mokaair.com/zh-TW/life/tech-news-steam-review-delays-20261103 ；The Verge） | 輕鬆、跟「訊號／雜訊」呼應；照報導講清楚 AI 是開發者的猜測、Valve 沒立即回覆，不嘲笑人 |

## 為什麼是這一則當 Signal of the Day

- 國際上影響最大、背景最值得講：準備上市的 AI 實驗室第一次把「營收有多少被算力吃掉」攤開（S-1，TechCrunch）。
- 有一個要回答的問題：營收一季多了快五成，虧損卻擴大，錢去哪了？答案在文件裡（運算占比 58%、100 億美元帳單、一半是較貴的短期合約）。
- 錢的流向有同一天的佐證，不用推論：AMD 資料中心 +97%、AMD 自稱 Anthropic 等在它的機櫃上跑；推論新創 Fal 一樣被算力成本壓毛利；電力跟不上（噴射引擎、Nscale 的英國案）。
- 有場景：分析師這週一打開更新版 S-1，從第一行營收往下讀。
- 台灣與亞洲：今天的來源都沒有提到台灣廠商；只講 AMD 自己列的風險（出口管制、關稅、記憶體、第三方製造），明說不猜是誰。
- 接下來看什麼很清楚：支出還會增加、是短暫波動還是長期問題、債券市場與地方反對、上市日期未公布。

## 觀眾

每天通勤或午休聽 20 分鐘科技新聞的台灣上班族、學生與工程師：天天用 ChatGPT、Claude、Google 搜尋，用 Android 或 iPhone，
家裡有長輩或孩子；有些人用交易所或關心穩定幣法規，有些人在用 GitBook 或 AI 代理。他們要知道「這對我改變了什麼、今天要不要做什麼」。

## 觀眾看完能做到的事

- 說得出 AI 服務背後的成本結構：Anthropic 營收的 58% 用在運算，而且有一半是急著買的、較貴的短期合約（TechCrunch）。
- 接到熟悉聲音要匯錢的電話，先掛掉、用自己存的號碼回撥；Android 用戶去設定搜尋「詐騙」看有沒有防護可開；帶長輩玩 Be Scam Ready（節目建議；功能與遊戲依 Google 部落格）。
- 在 ChatGPT 查東西時分清楚回答與廣告（OpenAI 上個月宣布廣告會放產品圖片）。
- 知道「沒有浮水印」不等於人寫的（Claude 發行說明的例外）。
- 用 GitBook 的人去換權杖與密鑰（GitBook 的要求，經 Decrypt）。
- 交易所出事時，看它有沒有給自己能檢查的證明（幣安的零知識備付證明，經 Decrypt）。
- 知道台灣的穩定幣規則還是草案，可在公告翌日起 40 日內提意見（金管會）。

## 站主觀點

套用立場：2、4、5
（站主還沒在設定分頁存「頻道立場」，條號依 `docs/videos/HANDS-OFF.md` §頻道立場的草稿；這段是提案，給站主在大綱關卡看。）
今天最重要的是 Anthropic 的 S-1：它把「跑 AI 要花多少錢」攤開來，晶片、雲端、電力和廣告都是同一張帳單的不同面。
我不說 Anthropic 會出問題，也不猜 AI 訂閱會不會漲價；TechCrunch 認為這更像短暫波動，我老實說不確定，要看下一季。
台灣的角度不硬湊：來源沒有提到台灣廠商就說沒有。其他各則照實標出「公司自己說」「據報導」「開發者的猜測」；錢的段落只講帳戶安全與規則，不談價格。

## 不選

- CrowdStrike 與 Fiddler 的 AI kill switch（ai-news-crowdstrike-ai-kill-switch-fiddler-20261103）：企業資安產品，跟 GitBook 一則題材重疊，選了有實際事件、有客戶要做的事的 GitBook。
- OpenAI「compute campuses」改名不當 Noise：它跟主題的電力與社區問題直接相關，改放 What People Are Saying 的一句說法。
- AMD 第四季營收展望、Fal 的估值數字細節：純財務數字，只留跟算力流向有關的部分。
- 任何代幣價格、交易所資產規模的漲跌與買賣時機。

## 會過期的事實

- Anthropic 的 S-1 可能再更新；上市日期未公布。
- 幣安的補足比例（約 95%）、凍結金額、北韓與美方的說法。
- OKX-ICE 異議名單的家數（11/2 通知為 56 家）、平台是否上線。
- 金管會草案的預告日期、意見期與生效日（配合虛擬資產服務法施行日期）。
- Android 偽冒來電偵測與 Pixel 詐騙偵測擴大的機型與地區、蘋果新分級的執行方式。
- Steam 審核積壓的情況與 Valve 的回應。

## 不做的事

- 不說 Anthropic「快撐不下去」、不猜 IPO 日期或股價，不談任何估值走勢與投資。
- 不把台灣供應鏈硬接進主題；AMD 的「第三方製造」不替它點名。
- 不把公司自述（OpenAI 搜尋量、AMD 客戶、Google 防詐、Anthropic FlashProve、Netflix）講成已證實；不把 Steam 積壓講成 AI 造成的。
- 不編主持人的私人經驗；Try This 標明是節目建議，不是 Google 或蘋果的指示。
- 片尾不提下一集。

## 大綱

### 選項 A：最多人用的先講

一行說明：Intro 直接丟 ChatGPT 搜尋五分之一的問題，快訊照使用人數排，Anthropic 的 S-1 放在快訊之後當主題，Signal Number 用五分之一。
開場鉤子：這週一，OpenAI 說 ChatGPT 的搜尋量已經是 Google 的五分之一，可是 Google 那邊的數字從哪來，它沒說。

排序理由：搜尋是每個人每天做的事，最好懂。缺點：這則是 OpenAI 的單方說法，講透了也只有「先打個問號」，
撐不起 10 分鐘的主題；而且 Intro 的問題在快訊第一則就答完，整集沒有一個要等到最後才回答的問題。

### 選項 B：從 Anthropic 的算力帳單講（推薦）

一行說明：Intro 由 Kai 問「營收一直漲，虧損卻變大，錢花去哪了」，停在答案之前；快訊照對台灣聽眾的影響排，用 58% 收尾當 Signal Number，主題段從分析師打開更新版 S-1 講起，順著錢流到晶片、雲端與電力。
開場鉤子：今天的主題，是 Anthropic 上市前更新的一份文件，裡面那張算力的帳單：營收一直漲，虧損卻變大。

排序理由：國際上影響最大、資料最完整的一則，又能把同一天的 AMD、Fal、噴射引擎、OpenAI 改名、ChatGPT 廣告串成一條錢的線；
問題在片尾第一句回答。台灣唯一的一則（穩定幣草案）留在 Money Signal，符合「台灣新聞最多一則、不當主題」。

選定：選項 B（理由：有一個貫穿全集、片尾才回答的問題，主題撐得起五拍；選項 A 的主題是單方說法，問題在第一則就答完）。
