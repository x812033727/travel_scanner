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
| Apple Developer | `https://developer.apple.com/news/rss/news.rss` | ✅ 200 |
| Windows | `https://blogs.windows.com/feed/` | ✅ 200 |
| Anthropic | `/rss.xml`、`/news/rss.xml` | ❌ 都 404，**沒找到 feed**，要抓 `anthropic.com/news`（回 200） |
| 台灣 NCC | `ncc.gov.tw` | ⚠️ 擋在安全驗證後，搜尋引擎讀不到內文，要換管道 |

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

## ⚠️ 待驗（有官方日期，內容還沒讀原文）

| 事件日 | 題目 | 來源狀態 |
| --- | --- | --- |
| 2026-09-15 | September Pixel Drop：Pixel VIP、Pixel Watch 功能 | Google feed 已確認日期與標題，連結 `https://blog.google/products-and-platforms/devices/pixel/september-2026-pixel-drop/` |
| 2026-09-14 | More choice and possibility with Windows PCs at IFA | `blogs.windows.com` feed 已確認 |
| 2026-09-04 | Project Zenith：開發者機種的開箱即用 Windows 環境 | 同上 |
| 2026-06-24 | OpenAI 與 Broadcom 的 LLM 推論晶片 | OpenAI feed 已確認日期，**與 AI 垂直擇一** |

## 還沒查的方向

- **台積電**亞利桑那與德勒斯登擴產：**金額一定要回台積電新聞稿或公開資訊觀測站**，
  整合站給的累計數字（「追加 1,000 億、累計約 2,650 億美元」）不可信。
- **SIA 的半導體銷售統計**：**很容易寫成行情**。找不到產業結構的角度就跳過，
  不要寫成「景氣好不好」。
- **台灣 NCC 與數位發展部**：NCC 網站擋在安全驗證後面，要換管道
  （公報、法規查詢系統，或 NCC 的國際焦點 PDF）。
- **標準組織**：USB-IF、Wi-Fi Alliance、3GPP、IETF 在 2026 年的發布。
- **資安**：2026 年具名的重大漏洞與事件（CVE Program、NVD、CISA advisories）。
- **歐盟 DMA／DSA** 在 2026 年的執行動作。
- **Samsung、Google Pixel** 的硬體發表（Apple 以外的消費電子，避免整份都是 Apple）。

---

## 現況與缺口

目標是每個垂直 10–12 則重要 + 4–6 則次要。

| 垂直 | ✅ 已驗 | ⚠️ 有日期、待讀原文 | 還要補 |
| --- | --- | --- | --- |
| 幣圈 | 5 | 0 | 9–13 |
| 科技 | 3 | 4 | 7–11 |
| AI | 1（9/15 缺口） | 10（OpenAI feed） | 視站主選題而定 |

**下一步**：用上面那張 feed 表逐家掃過 Anthropic、Meta、DeepSeek、Qwen、Samsung、
標準組織與主管機關，把「已驗」的數量做上去。每一則都要有：
事件日、建議 slug、一手來源網址、來源原文載明的關鍵事實、讀者角度、以及**不要寫什麼**。
