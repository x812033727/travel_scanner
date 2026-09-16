# 科技與 AI 候選題目（待站主圈選）

同 [`candidates-crypto.md`](candidates-crypto.md) 的狀態標記：
✅ 已驗（一手來源讀到，關鍵數字抄在下面）／⚠️ 待驗（有官方日期，但內容還沒讀原文）／
❌ 查否（查過一手來源，與線索不符）。

查核日 **2026-09-16**。

---

## 先讀：官方 feed 比抓網頁可靠

這一輪最有用的發現。`openai.com` 的網頁對 `curl` 與 WebFetch 都回 **403**，
但 **`https://openai.com/news/rss.xml` 回 200**——裡面有 1,193 筆帶 `pubDate` 的項目，
光 2026 年就有 407 筆。這正是 [`BRIEF.md`](BRIEF.md) 寫的 fallback（官方 RSS），
而且做候選清單比抓網頁更適合：**日期是官方給的，不必從版面猜**。

實測（2026-09-16）：

| 來源 | 位址 | 狀態 |
| --- | --- | --- |
| OpenAI | `https://openai.com/news/rss.xml` | ✅ 200（網頁本身 403，feed 可用） |
| Google | `https://blog.google/rss/` | ✅ 200 |
| Apple Newsroom | `https://www.apple.com/newsroom/rss-feed.rss` | ✅ 200，**Atom**（`<entry>`／`<updated>`，不是 `<item>`／`<pubDate>`） |
| Apple Developer | `https://developer.apple.com/news/rss/news.rss` | ✅ 142 筆、2026 年 57 筆。**平台政策變動的一手來源**，比 Newsroom 更早也更具體（T5 就是從這裡找到的） |
| Windows | `https://blogs.windows.com/feed/` | ✅ 200 |
| Anthropic | `/rss.xml`、`/news/rss.xml` | ❌ 都 404，**沒找到 feed**，要抓 `anthropic.com/news`（回 200） |
| 台灣 NCC | `ncc.gov.tw` | ⚠️ 擋在安全驗證後，搜尋引擎讀不到內文，要換管道 |
| NVIDIA Newsroom | `https://nvidianews.nvidia.com/releases.xml` | ✅ 20 筆，最新 2026-09-16 |
| Meta Engineering | `https://engineering.fb.com/feed/` | ✅ 200（工程部落格，不是 AI 產品消息） |
| IETF Blog | `https://www.ietf.org/blog/feed/` | ✅ 598 筆、2026 年 25 筆，但**多半是組織事務**，新聞價值低 |
| USB-IF | `https://www.usb.org/rss.xml` | ⚠️ 200、格式正確，但**最新一筆是 2018-07-31** |
| Samsung Newsroom | `https://news.samsung.com/global/feed` | ❌ **200 但 body 是 Akamai 的 Access Denied** |
| DeepSeek | `api.deepseek.com/news/rss` | ❌ 401 |
| TSMC | `pr.tsmc.com/rss/newsfeed` | ❌ 403 |
| CISA | `cisa.gov/cybersecurity-advisories/all.xml` | ❌ 403 |
| 新加坡 MAS | 網頁與 consultation 頁 | ❌ **這個容器連不到**（service unavailable） |
| 美國各機關 | Federal Register API | ✅ **最可靠的管道**，涵蓋 SEC／CFTC／FinCEN／OCC／FDIC／NCUA |

### 兩個陷阱

1. **HTTP 200 不代表拿到 feed。** Samsung 那一列回 200，
   但 body 是 `<TITLE>Access Denied</TITLE>`。只看狀態碼會把一頁拒絕當成資料。
2. **feed 可能是死的。** USB-IF 那一列格式完全正確、有 10 筆 item，
   但最新一筆停在 2018 年。拿它當「USB-IF 沒有新消息」的依據會錯。

檢查方式：**數 `<item>`／`<entry>` 的數量，並看最新一筆的日期**，兩者都合理才算拿到。

**feed 給的是日期與標題，不是內容。** 開稿時仍要讀該篇原文，
`sources` 放的是文章頁的網址，不是 feed 的網址。

---

# AI

## ✅ 已驗：9/15 的缺口

### A1 — Gemini 3.8 Live 與 3.8 Live Extended Thinking
- **事件日** 2026-09-15　**建議 slug** `ai-news-gemini-38-live-20260915`
- **一手來源**
  `https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/`
- **官方原文載明**：兩個模型。3.8 Live「built for scale and cost efficiency」，
  近即時處理視覺輸入、對話中偵測 **97 種語言**、可在不中斷對話的情況下執行背景工作；
  3.8 Live Extended Thinking「built for high-complexity tasks」，
  能「reasoning and speaking simultaneously」。
  開放範圍：開發者走 Gemini API 與 Google AI Studio；企業端是 Gemini Enterprise **私人預覽**，
  Gemini Enterprise for Customer Experience 與 Google Workspace 標為「coming soon」；
  一般使用者在 Search Live、Gemini Live，以及 Workspace（Docs／Gmail／Keep）的
  **AI Pro／Ultra 訂閱者**。
- **官方未說明地區範圍**，只寫「starting today」。
  照 `BRIEF.md` 的規則，**不可推定台灣帳號可用**，要寫成「官方未說明」。
- **相關新聞連結** 接既有的 `ai-news-gemini-38-flash-20260902`（同代模型的另一條線）。

### A2 — 同日的開發者側：Gemini 3.8 Live 與 3.5 Transcribe
- **事件日** 2026-09-15　**建議 slug** `ai-news-gemini-live-voice-api-20260915`
- **一手來源**
  `https://blog.google/innovation-and-ai/technology/developers-tools/build-real-time-voice-applications-gemini-audio/`
- **與 A1 同一天、同一組模型，只是開發者角度。**
  `BRIEF.md` 禁止重寫同一件事，所以**兩篇擇一**。
  建議只做 A1，把 API 與定價的內容收進 A1 的其中一節。

## ❌ 查否：OpenAI 在 9/15–9/16 沒有發布消息

官方 feed 的最後一筆是 **2026-09-14**（`Fyxer`、`Perplexity` 兩則客戶案例）。

整合站說 9/15 有「Microsoft 的 MAI 模型與 superintelligence 表態」與
「Altman 談 OpenAI 不在 2026 上市」：

- **Microsoft 那則查不到官方當日貼文。** MAI 系列（MAI-Thinking-1、MAI-Image-2.5、
  MAI-Transcribe-1.5、MAI-Voice-2、MAI-Code-1）的官方貼文在 techcommunity，
  但頁面是 JS 算繪的，WebFetch 只拿得到標題，**日期沒有確認**。要寫得換管道。
- **Altman 那則是 Fortune 專訪的轉述。** 當事人原文可以當一手來源，
  轉述不行——**要拿到 Fortune 原文**才能寫。

## ✅ 已驗：NVIDIA 併購 Hugging Face

### A3 — NVIDIA to Acquire Hugging Face
- **事件日** 2026-09-03　**建議 slug** `ai-news-nvidia-hugging-face-20260903`
- **一手來源** `https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/`
- **官方原文載明**：價格 **$12,930,300,000**；
  Hugging Face「remain an open platform for the entire AI ecosystem」，
  續支援 open source 與 open weight 模型、multi-cloud 與 multi-accelerator；
  平台規模 **1,800 萬**開發者／研究者／創作者、**300 萬**個模型、
  **50 萬**個資料集、**100 萬**個應用、**20 萬家以上**公司；
  NVIDIA 自己貢獻過 **500+ 個模型與 250+ 個開放資料集**。
- **官方沒說**：預計完成日、監理核准條件、人事安排、價格以外的財務細節。
  這幾點要寫成「官方未說明」，**不可推測會不會過關**。
- **為什麼重要**：既有 38 篇沒有任何一篇寫併購，
  而 Hugging Face 是讀者實際會用到的平台。
  9/3 當天站上已有 `ai-news-gpt-6-astra-20260903`，**是不同題目，不衝突**。

### ⚠️ NVIDIA 的其餘三則（feed 已確認日期與標題，內容待讀原文）

| 事件日 | 官方標題 | 備註 |
| --- | --- | --- |
| 2026-09-15 | AI Infra Summit: NVIDIA Vera Rubin and DSX Platform Advancements… | 接既有的 `ai-news-nvidia-rubin-20260105` |
| 2026-09-14 | NVIDIA Expands Open Source CUDA-Q Platform for Fault-Tolerant Quantum Computing | 量子運算，放科技垂直 |
| 2026-08-31 | NVIDIA and MediaTek Deepen Long-Standing Partnership… | **聯發科是台灣公司**，對本站讀者特別相關 |

## ⚠️ 1/1 起的補漏：日期已由官方 feed 確認，內容待讀原文

OpenAI 官方 feed 的 2026 年逐月筆數：
1月 35、2月 33、3月 38、4月 59、5月 56、6月 55、7月 42、8月 56、9月 33（至 9/14）。

對照 [`ai.md`](ai.md) 的既有篇目表，**站上覆蓋最薄的三個月（3 月 3 篇、5 月 2 篇、
6 月 3 篇）正好是官方發布最密的區間**，補漏空間很大。下列日期與標題來自官方 feed：

| 事件日 | 官方標題 | 為什麼值得寫 |
| --- | --- | --- |
| 2026-03-19 | OpenAI to acquire Astral | Astral 是 `uv`／`ruff` 的開發商，**本站 API 就在用**，對寫程式的讀者直接相關 |
| 2026-03-31 | Accelerating the next phase of AI | 募資公告。整合站說 1,220 億美元，**金額必須回原文核對** |
| 2026-05-05 | GPT-5.5 Instant: smarter, clearer, and more personalized | 站上只有 4/23 的 GPT-5.5，這是不同型號 |
| 2026-05-05 | New ways to buy ChatGPT ads | 「我在 ChatGPT 裡看到的東西怎麼來的」，對一般讀者很具體 |
| 2026-05-28 | OpenAI's Frontier Governance Framework | 與既有 `ai-news-pace-the-frontier-20260912` 同一條線 |
| 2026-06-08 | Confidential submission of draft S-1 to the SEC | 上市申請。**角度必須是「對使用者代表什麼」，不可寫成投資題材** |
| 2026-06-24 | OpenAI and Broadcom unveil LLM-optimized inference chip | 也可放科技垂直，**兩邊擇一**，不要兩邊都寫 |
| 2026-09-10 | Introducing ChatGPT for Financial Services | 站上 9/10 只寫了 Agents API |
| 2026-09-10 | Build more natural voice experiences with GPT‑Live‑1 in the API | 與 A1／A2 對照，可合併成一篇語音專題 |
| 2026-09-11 | Rapidly scaling online storage to serve over 1 billion ChatGPT users | 「十億使用者」這個數字要回原文確認 |

**這份清單只有 OpenAI。** Anthropic（沒有 feed，要抓網頁）、Google 更早的月份、
Meta、DeepSeek、Qwen 都還沒逐月掃過，開票前要補。

---

# 科技（非 AI）

## ✅ 已驗

### T1 — Apple iPhone Duo
- **事件日** 2026-09-09　**建議 slug** `tech-news-iphone-duo-20260909`
- **一手來源** `https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/`
- **官方新聞稿載明**：折疊機。內螢幕 **7.6 吋** Super Retina XDR
  （比 iPhone 18 Pro Max 大 **50%**），外螢幕 **5.4 吋**（約 iPhone 18 Pro 螢幕面積的 **90%**）；
  **A20 Pro** 晶片、雙 16 核神經網路引擎；48MP Fusion 主鏡頭含 2x 望遠、48MP 超廣角、
  內螢幕下隱藏式 FaceTime 鏡頭；雙電池架構，內螢幕影片最長 **31 小時**、
  外螢幕 **44 小時**、混合使用 **24 小時**；五級鈦金屬、Ceramic Shield 2、IP68；
  **256GB 起 1,999 美元**（24 期、每期 83.29 美元）；
  **10/16 預購、10/23 於 70 多個國家與地區開賣**。
- **官方新聞稿沒有逐一列出那 70 多個地區**，所以**不可推定台灣在內**，要寫成「官方未列出」。
- **讀者角度**：折疊機的取捨（重量、耐用、續航），以及怎麼查自己所在地的上市狀態。
- **界線**：[`tech.md`](tech.md) 禁止購買建議，不寫「值不值得買」。

### T2 — Apple 9/9 發表會的其餘硬體
- **事件日** 2026-09-09　**建議 slug** `tech-news-apple-september-hardware-20260909`
- **一手來源**：Apple Newsroom 同日的多篇新聞稿，feed 已確認標題與日期——
  「Apple debuts iPhone 18 Pro and iPhone 18 Pro Max」、
  「Introducing Apple Watch Series 12, with the all-new Health Sensing System」、
  「Apple unveils Apple Watch Ultra 4」、
  「Apple introduces AirPods 5 with best-in-class open-ear Active Noise Cancellation」。
- **與既有文章的分工**：`ai-news-siri-ai-ios-27-20260914` 已經寫過 iOS 27 與 Siri AI，
  **這篇只寫硬體**，軟體連回去那篇。
- 建議做成**一篇**「9/9 發表會的硬體」，不要每個產品一篇，否則會洗版。

### T3 — 歐盟《網路韌性法》通報義務上路
- **事件日** 2026-09-11　**建議 slug** `tech-news-eu-cra-reporting-20260911`
- **一手來源**
  - 歐盟執委會 `https://digital-strategy.ec.europa.eu/en/policies/cra-reporting`
  - ENISA Single Reporting Platform
    `https://www.enisa.europa.eu/topics/product-security-and-certification/single-reporting-platform-srp`
- **官方頁載明**：**2026-09-11 起**製造商必須通報
  「actively exploited vulnerabilities and severe incidents」；
  早期預警 **24 小時**內、完整通報 **72 小時**內、
  最終報告在修補措施可用後 **14 天**內（重大事故則是 72 小時通報後 **一個月**內）；
  ENISA 的 Single Reporting Platform **自 2026-09-11 起運作**，
  製造商與開源軟體管理者都要透過它通報；通報送往主要營業地的 CSIRT 並同步給 ENISA。
- **⚠️ 開稿要釐清的一點**：整合站寫「主要義務自 2027-12-11 起適用」，
  但執委會這一頁把 **2027-12-11 寫成開源軟體管理者的通報起始日**。
  兩者是不是同一件事，要讀 EUR-Lex 的法規原文確認，**不可照抄整合站**。
- **讀者角度**：在歐盟賣的智慧裝置都受這套規範，對台灣消費者代表韌體更新與漏洞揭露會怎麼變。

### T4 — 台灣數位發展部四則（✅ 日期與標題已驗）

從數發部自己的新聞發布頁讀到（`https://moda.gov.tw/press/press-releases/372`），**不是整合站**：

| 事件日 | 官方標題 |
| --- | --- |
| 2026-09-15 | 數發部啟動主權AI語料庫民間語料徵集 號召作家與出版業共襄盛舉 |
| 2026-09-10 | 數發部舉辦「頻譜政策領航 邁向6G新世代」國際研討會 聚焦6G前瞻布局與AI應用 |
| 2026-07-24 | 數發部「臺灣主權AI訓練語料庫」新增2000萬tokens客語語料 充實本土AI語言資料基礎 |
| 2026-06-23 | 數發部積極推動臺馬四號海纜及馬祖4鄉微波站建設 強化離島通訊韌性 |

**主權 AI 語料庫那條線（9/15 ＋ 7/24）是這一輪最適合本站讀者的題目**：
台灣自己的中文與客語語料，跨 AI 與公共政策，而且沒有任何既有文章寫過。
建議 slug `tech-news-taiwan-sovereign-ai-corpus-20260915`，
把 7/24 的客語語料當成同一條線的前情，寫在同一篇裡。

**⚠️ 又一次整合站與官方不符。** 搜尋摘要說「台馬**二**號海纜 2026-03-07 全斷、
2026-05-25 完成緊急修復」——**數發部的新聞發布頁上沒有這一則**，
只有 6/23 的**臺馬四號**海纜建設。要寫海纜必須自己找到那則公告，不能照抄。

### T5 — Apple 調整歐盟的 App 商業條款（✅ 已驗）

- **事件日** 2026-08-18，**生效日 2026-10-01**
- **建議 slug** `tech-news-apple-eu-business-terms-20260818`
- **一手來源** `https://developer.apple.com/news/?id=gmws0jgp`
- **官方原文載明**：Apple「following close collaboration with the European Commission」，
  把歐盟的開發者**全部移到單一套商業條款**。具體變動：
  - **Core Technology Fee（按安裝次數收的費用）改為 Core Technology Commission**，
    對「digital transactions in apps distributed outside the App Store」收 **5%**。
  - **取消 Initial Acquisition Fee 與 Store Services Fee**。
  - 調整 App Store、替代支付與替代散布 App 的抽成比率。
  - 允許 App 在 Apple In-App Purchase 之外**並行提供替代支付**。
  - App Store 的替代支付加上兒少保護措施。
  - 放寬經營替代 App 市集與透過網路散布 App 的資格。
- **⚠️ 最關鍵的一點：Apple 全文沒有提到《數位市場法》（DMA）。**
  這是一則對監理的回應，但官方沒有這樣說。
  **文章不可以把 DMA 寫成原因**，只能寫「Apple 表示是與歐盟執委會密切合作後的調整」。
  這正是 `BRIEF.md`「廠商說了什麼就寫什麼、沒說的不補」那條規則的典型案例。
- **官方也沒說**：調整後的各項抽成是多少、「extraordinary scale」的門檻怎麼算、
  兒少保護的細節。三項都要寫成「官方未說明」。
- **讀者角度**：台灣使用者不在歐盟，所以重點是**「為什麼同一個 App 在不同地區的條款不一樣」**，
  以及這對開發者定價的連動。**不要寫成「台灣也會這樣」。**

### T6 — Windows Project Zenith（✅ 已驗）

- **事件日** 2026-09-04，**建議 slug** `tech-news-windows-project-zenith-20260904`
- **一手來源**
  `https://blogs.windows.com/windowsdeveloper/2026/09/04/announcing-project-zenith-the-ready-to-code-windows-experience/`
- **官方原文載明**：給開發者機種的 Windows 11 預設組態，預裝語言、執行環境、
  版本控制與生產力工具；預設顯示副檔名與隱藏檔、關閉同步提供者提示、啟用 Command Palette；
  整合 WSL 容器跑 Linux 工作負載；**可在本機不限流量跑 30B+ 參數模型**；
  機器條件是 **64 GB 以上統一記憶體、250 GB/s 以上記憶體頻寬**；
  「first become available with AMD's Ryzen AI Halo, with more devices from our OEM and
  silicon partners available in the coming months」。
- **官方沒說**：價格、預覽或正式推出日期、地區、具體 OEM 名單、
  Windows 11 以外的版本需求。
- **讀者角度**：與站上既有的本機模型題材直接相扣，但這篇寫的是
  **硬體門檻與作業系統組態**，不是模型本身，兩者要分清楚。
- 界線：`tech.md` 禁止購買建議，不寫「該不該買這種機器」。

### T7 — September Pixel Drop（✅ 已驗，**建議當次要新聞**）

- **事件日** 2026-09-15，**建議 slug** `tech-news-pixel-drop-20260915`
- **一手來源** `https://blog.google/products-and-platforms/devices/pixel/september-2026-pixel-drop/`
- **官方原文載明**：Pixel 手機端有 VIP 首頁小工具（單擊撥號或傳訊）、底部浮動導覽選單、
  新的訊息通知標記、**美國**的 Gboard 行內詐騙警示、
  聊天 App 通知的詐騙偵測擴及更多地區、Harry Potter 有聲書套件、
  符合資格者兩個月 Audible 免費試用；Pixel Watch 有 Raise to Talk 改進、
  One Handed 手勢支援更多 App、錯誤修正。
- **官方沒說**：除了美國以外**哪些地區拿得到哪些功能**、適用哪些 Pixel 機型、分批時程。
- **這則份量偏輕，建議放「8/1 起的次要新聞」那一格**，不要當重要新聞。
  次要新聞每個垂直要 4–6 則，這是第一則。

### ⚠️ Apple Developer feed 裡還沒展開的平台政策

日期與標題已由 feed 確認，內容未讀：

| 事件日 | 官方標題 |
| --- | --- |
| 2026-03-12 | Adjustments to the China storefront of the App Store on iOS and iPadOS |
| 2026-03-26 | Update on regulated medical device apps in the European Economic Area, United Kingdom, and United States |
| 2026-03-31 | App Store expands support to 11 new languages |
| 2026-05-08 | Brazilian betting license requirement for App Store availability |

中國商店調整（3/12）對台灣讀者可能有參考價值，但**要小心政治敏感度**，
而且要確認官方到底說了什麼、沒說什麼，不要替它補上理由。

## ⚠️ 待驗（有官方日期，內容還沒讀原文）

（Pixel Drop 與 Project Zenith 已經驗完，移到上面的 T6、T7。）

| 事件日 | 題目 | 來源狀態 |
| --- | --- | --- |
| 2026-09-14 | More choice and possibility with Windows PCs at IFA | `blogs.windows.com` feed 已確認日期與標題 |
| 2026-06-24 | OpenAI 與 Broadcom 的 LLM 推論晶片 | OpenAI feed 已確認日期，**與 AI 垂直擇一** |

## 還沒查的方向

- **台積電**亞利桑那與德勒斯登擴產：**金額一定要回台積電新聞稿或公開資訊觀測站**，
  整合站給的累計數字（「追加 1,000 億、累計約 2,650 億美元」）不可信。
- **SIA 的半導體銷售統計**：**很容易寫成行情**。找不到產業結構的角度就跳過，
  不要寫成「景氣好不好」。
- **台灣 NCC**：網站擋在安全驗證後面，要換管道（公報、法規查詢系統，或 NCC 的國際焦點 PDF）。
  數位發展部已經掃過，見 T4。
- **標準組織**：Wi-Fi Alliance、3GPP 在 2026 年的發布。
  **USB-IF 的 feed 是死的（停在 2018），IETF 的多半是組織事務**，兩者都別再花時間。
- **資安**：2026 年具名的重大漏洞與事件（CVE Program、NVD、CISA advisories）。
- **歐盟 DMA／DSA** 在 2026 年的執行動作（T5 是 Apple 那一側，還缺執委會那一側）。
- **Samsung** 的硬體發表（**feed 被擋，要換管道**）。Google Pixel 已有 T7。

---

## 現況與缺口

目標是每個垂直 10–12 則重要 + 4–6 則次要。

| 垂直 | ✅ 已驗 | ⚠️ 有日期、待讀原文 | 距離 10–12 則 |
| --- | --- | --- | --- |
| 幣圈 | **11**（C1–C11） | 1（MAS，此容器連不到） | **已到量** |
| 科技 | **11**（Apple 3、NVIDIA 1、moda 4、T5–T7） | 6 | **已到量** |
| AI | **2**（Gemini 3.8 Live、NVIDIA×HF） | 13（OpenAI feed 10、NVIDIA 3） | 視站主選題 |

**三個垂直的重要新聞候選都夠站主圈選了。**

次要新聞（8/1–9/16）的現況見本頁最後一節：**AI 8 則、科技 8 則都夠了，
幣圈 0 則**——在「不碰行情」的界線內，那段期間的幣圈次要新聞查證後確實很稀薄。

還沒掃過：Anthropic（沒有 feed，要抓網頁）、Meta 的 AI 產品線、DeepSeek、Qwen、
Samsung（feed 被擋）、台積電（feed 403）、NCC。

**幣圈的重要新聞已經到量。** 科技與 AI 的「已驗」也夠站主圈第一批了。
還沒掃過的：Anthropic（沒有 feed，要抓網頁）、Meta 的 AI 產品消息、DeepSeek、
Qwen、Samsung（feed 被擋）、台積電（feed 403）、NCC。

**下一步**：用上面那張 feed 表逐家掃過 Anthropic、Meta、DeepSeek、Qwen、Samsung、
標準組織與主管機關，把「已驗」的數量做上去。每一則都要有：
事件日、建議 slug、一手來源網址、來源原文載明的關鍵事實、讀者角度、以及**不要寫什麼**。

---

# 次要新聞（8/1 → 9/16）

每個垂直要 4–6 則。下列日期與標題**全部來自官方 feed**，所以日期可信；
但除了標 ✅ 的，內容都還沒讀原文。

## AI 的次要新聞

OpenAI 官方 feed 在這段期間有 **89 筆**，站上既有文章只覆蓋其中 11 個日期。
下面挑的是「具體、對一般讀者有用，但不到頭條」的：

| 事件日 | 官方標題 | 為什麼適合當次要新聞 |
| --- | --- | --- |
| 2026-08-11 | Testing ads in ChatGPT | 與 8/18 是同一條線，**建議合成一篇**：ChatGPT 裡的廣告怎麼來的 |
| 2026-08-18 | ChatGPT Ads expands across Europe | 同上 |
| 2026-08-18 | Introducing ChatGPT for Teens: Built for learning, backed by protections | 家長與青少年，對本站讀者很具體 |
| 2026-08-19 | Offering Zero Data Retention for frontier models | 隱私與資料保留，可接既有的 `ai-safety` 題材 |
| 2026-08-13 | Previewing Ultrafast mode: GPT-5.6 Sol at up to 14X the speed | 「14X」是**廠商宣稱**，一定要寫成「OpenAI 表示」 |
| 2026-08-10 | Premium seats are coming to ChatGPT Business | 方案與計費 |
| 2026-08-25 | Disrupting a new covert influence campaign from Russia | 可與既有的 `ai-news-anthropic-threat-report-20260910` 對照 |
| 2026-09-09 | Paul Christiano joins OpenAI Foundation Board | 治理，份量輕但明確 |

**⚠️ 2026-08-26「The Hugging Face incident and the road ahead」**：
這則和 9/3 的 NVIDIA 併購 Hugging Face 是同一個平台的兩件事，很值得寫，
但 **`openai.com/index/...` 對 WebFetch 回 403**，內容讀不到。
feed 只給了日期與標題。要寫得換管道（官方 RSS 的 description 欄位、
或 Hugging Face 自己的公告）。

## 科技的次要新聞

### ✅ 已驗：Apple M6 與 M5 Ultra（8/25）——這則其實夠格當「重要新聞」

- **事件日** 2026-08-25　**建議 slug** `tech-news-apple-m6-m5-ultra-20260825`
- **一手來源**
  `https://www.apple.com/newsroom/2026/08/apple-introduces-m6-and-m5-ultra-for-a-big-leap-in-performance-and-ai-compute/`
- **官方原文載明**：
  - **M6 是 Apple 第一顆 2 奈米製程晶片**；12 核 CPU（2 個 super core、
    4 個效能核心、6 個節能核心）、12 核 GPU 含 Neural Accelerators、
    雙 16 核神經網路引擎；統一記憶體頻寬最高 **170GB/s**、記憶體最高 **32GB**；
    「up to 1.2x faster multithreaded performance as compared to M5」。
  - **M5 Ultra 是 M 系列第一個四晶粒架構**（UltraFusion）；最高 36 核 CPU
    （12 super core、24 效能核心）、最高 80 核 GPU、32 核神經網路引擎；
    統一記憶體頻寬 **1.2TB/s**、記憶體最高 **512GB**；
    「up to 1.3x higher multithreaded performance than M3 Ultra」。
  - M6 首發在新 Mac mini、M5 Ultra 首發在新 Mac Studio。
- **官方沒說**：售價與上市日期。兩項都要寫成「官方未說明」。
- **所有效能倍數都是 Apple 的宣稱**，一律寫成「Apple 表示」，本站沒有實測。
- **這則不該當次要新聞。** 第一顆 2nm 消費級晶片是這段期間最硬的科技題目之一，
  而且站上完全沒寫過。建議提到「重要新聞」那一格，次要新聞另外挑。
- 同日還有兩篇新聞稿（Mac Studio with M5 Max and M5 Ultra、
  Mac mini featuring the all-new M6 and M5 Pro），可以併進同一篇。

### ⚠️ 其餘科技次要新聞（feed 已確認日期與標題）

| 事件日 | 官方標題 | 來源 |
| --- | --- | --- |
| 2026-09-01 | Upcoming changes to Rosetta support for Intel-based macOS apps | Apple Developer |
| 2026-08-27 | Tax and price updates for apps, In-App Purchases, and subscriptions | Apple Developer |
| 2026-08-24 | Update: New domain for Sign in with Apple | Apple Developer |
| 2026-08-12 | Updates to age ratings for the Republic of Korea | Apple Developer |
| 2026-09-08 | Listening to families. Improving Microsoft Family.／Helping families and educators support safer experiences and healthier habits on Windows | Windows（兩篇同日，可合成一篇） |
| 2026-09-03 | Sparks Fly: NVIDIA Accelerates Local AI at IFA 2026 | NVIDIA，可與 T6 Project Zenith 對照 |
| 2026-09-14 | Perplexity Portable Computer Is Now Available on Windows, Powered by NVIDIA RTX | NVIDIA |

加上已列的 **T7 September Pixel Drop（9/15）**，科技的次要新聞候選已經超過 4–6 則。

**Rosetta 那則（9/1）對讀者最實用**：舊的 Intel Mac App 什麼時候會不能跑，
是使用者真的會遇到的事。

## 幣圈的次要新聞：這段期間**很稀薄**，這是查證結果不是偷懶

在站主定的界線內（只寫法規／技術／產業，不碰行情），8/1–9/16 幾乎沒有東西：

- **Federal Register**（涵蓋 SEC／CFTC／FinCEN／OCC／FDIC／NCUA）在這個窗口
  扣掉例行的 SRO 申報後**只有 3 筆**，其中一筆就是已列為重要新聞的 C4
  （8/21 Regulation Crypto Assets）。另一筆是 2026-09-04 的
  **Transfer Agent Rules**（SEC 提案，評論截止 2026-11-03），
  它出現在 crypto 關鍵字結果裡，但**要先確認它是否真的涉及代幣化證券**才能用。
  第三筆是聯邦法規統一議程的例行公告，沒有新聞價值。
- **台灣金管會**：用 `fsc.gov.tw` 限定搜尋，回來的都是 **2025 年**的新聞稿
  （最新一筆是 2025-09-22 的 VASP 洗錢防制登記名單），
  **沒有找到 2026 年 8–9 月的項目**。這是「沒查到」，不是「沒發生」——
  金管會的站內搜尋在這個環境不好用，要換管道（公報、法規查詢系統）再確認一次。

**結論**：幣圈的次要新聞目前 **0 則**，而且不是隨便找就有。
建議做法是把窗口放寬到 2026 年全年再挑「份量較輕」的項目
（例如 C10 日本 FSA 的工作小組報告就偏次要），
而不是為了湊 4–6 則去寫行情或整合站的內容。
