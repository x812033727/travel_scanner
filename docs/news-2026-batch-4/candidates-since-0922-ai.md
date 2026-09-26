# AI 垂直候選：批次 4.8（2026-09-22 起，查核日 2026-09-26）

窗口 **2026-09-22 00:00 台北（2026-09-21T16:00Z）起至 2026-09-26T13:03Z（台北 21:03，掃描結束）**。
另可提出最多兩則 **2026-09-12 至 09-21 之間沒人寫過的重要事件**，明確標為「補遺」。

所有請求都用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)' --max-time 30`
（最早一批是 60 秒上限），同一主機間隔 ≥1.2 秒，**沒有任何請求帶入 email 或任何人的個人資料**。沒有用 WebSearch。
原始回應存在 `raw-ai/`，逐筆狀態碼與位元組數在 `fetch-log-ai.tsv`
（本代理專用；`fetch.sh`／`raw/`／`fetch-log.tsv` 是幣圈代理的，沒有動）。
表中的 bytes 一律是**解壓後的 body 大小**（`fetch-log-ai.tsv` 的 `body=` 欄）；第四欄是線上傳輸的壓縮大小，不要拿來比。

排除依據：`existing-packs.txt`（站上已有）、`automation-candidates.tsv`（每小時自動化已撿到，不論狀態）、
`candidates-since-0920-ai.md` 已寫的項目。另外把 repo 內 74 份 `ai-news-*.json` 的 slug 也列出來比對過
（`existing-packs.txt` 只列了近期的 46 份，較早的 `ai-news-chatgpt-ads-20260505`、`ai-news-meta-muse-agent-20260909` 等不在裡面）。

**這一輪的形狀：** 自動化的來源是 TechCrunch／The Verge／CoinDesk 與 blog.google、blogs.nvidia.com、huggingface.co、
apple.com、blogs.microsoft.com、deepmind.google；**它不看 `openai.com/news/rss.xml`、`anthropic.com/news`、`x.ai/news`**。
所以 Meta Connect（Muse、眼鏡）、OpenAI 代理入侵澳洲政府網站、Anthropic 生物實驗室、Gemini 代打電話、Gemini 3.8 Live Avatar、
Made on YouTube、Microsoft Copilot 這些大新聞**全部已被自動化撿走、本清單排除**；剩下的大題集中在 OpenAI 與 Anthropic 自家公告。

---

## 掃過的管道與結果

「拿到 feed 了嗎」一律看兩件事：item／entry 數量，以及最新一筆的日期。狀態碼不算。

| 管道 | 位址 | 結果 | 數量 | 最新一筆／窗口內 |
| --- | --- | --- | --- | --- |
| OpenAI（feed） | `https://openai.com/news/rss.xml` | ✅ 200、750,532 bytes | 1,230 筆帶 `pubDate` | 最新 Fri, 25 Sep 2026 19:00 GMT；**窗口內 15 則** |
| OpenAI（文章頁） | `https://openai.com/index/*` | ⚠️ 開了 9 篇：**8 篇 200 並讀到正文**（373,892–1,473,989 bytes），**1 篇 403**（`better-prompt-caching-for-gpt-6`，9,922 bytes 擋阻頁）。同一主機幾分鐘內一擋一不擋，照 `DELTA-4-5.md` 第 9 條是間歇性的 | 8/9 | — |
| OpenAI Help Center | `https://help.openai.com/articles/20001245-ads-manager-availability`（落地 `/en/articles/…`） | ✅ 200、63,893 bytes，頁面自印「Updated: 11 hours ago」 | 國家表 | 活文件，見候選 2 |
| Anthropic（newsroom） | `https://www.anthropic.com/news`（無 feed） | ✅ 200、459,343 bytes；RSC 內 267 筆 `publishedOn`，最新 **2026-09-23T16:06Z**（enzyme 那篇）；**featured grid 另列 `Introducing Claude Opus 5.5`，`date: 2026-09-22`，這篇不在 `publishedOn` 清單裡** | 窗口內 2 則（1 則已被自動化撿走） | Sep 22／Sep 23 |
| Claude blog | `https://claude.com/blog` | ✅ 200、805,184 bytes，卡片印「September 23/24/25, 2026」 | 窗口內 6 則 | September 25, 2026（Build plugins for Claude） |
| Google（總 feed） | `https://blog.google/rss/` | ✅ 200、29,574 bytes，**但 20 則上限把窗口前段截掉**：最舊一筆 09-22 16:00Z | 20 items，全在窗口內 | Thu, 24 Sep 2026 17:00 +0000 |
| Google（三個分區 feed） | `/innovation-and-ai/rss/`、`/products-and-platforms/rss/`、`/company-news/rss/` | ✅ 200、32,020／30,153／32,952 bytes；用來補總 feed 截掉的 09-21 16:00Z→09-22 16:00Z | 各 20 items | 補到 Jigsaw（09-22 14:00Z）與 Digital Promise（09-21 16:00Z），兩則上一輪都已列過 |
| Google 台灣 | `https://blog.google/intl/zh-tw/rss/` | ✅ 200、39,004 bytes | 20 items，窗口內 1 則（中秋 Gemini 小技巧，非新聞） | 2026-09-22 09:00Z |
| Google DeepMind | `https://deepmind.google/blog/rss.xml` | ✅ 200、70,182 bytes | 100 items，窗口內 3 則，**3 則都已被自動化撿走** | 2026-09-24 16:20Z |
| NVIDIA（新聞室＋部落格） | `nvidianews.nvidia.com/releases.xml`、`blogs.nvidia.com/feed/` | ✅ 200、44,488／261,956 bytes | 20／18 items；窗口內 8 則，**與自動化逐則重疊或屬科技垂直** | 2026-09-24 14:00Z |
| Meta Newsroom | `https://about.fb.com/news/` | ✅ 200、308,200 bytes；逐則日期取自卡片可見日期 | 窗口內 5 則：Connect 四則（自動化已撿）＋新加坡警方反詐騙 1 則 | September 24, 2026 |
| Microsoft | `https://blogs.microsoft.com/feed/`、`https://microsoft.ai/news/`（轉到 `/blog/`） | ✅ 200、158,035／314,050 bytes | 窗口內 1 則（Copilot，**tech 已發布、自動化已撿**） | 2026-09-25 12:03Z |
| SpaceXAI（原 xAI） | `https://x.ai/news` | ✅ 200、271,663 bytes | Grok 4.7 **印 Sep 21**（`datePublished 2026-09-21T00:00:00Z`，窗口前一天）；窗口內 1 則客戶案例 | Sep 22, 2026 |
| Hugging Face | `https://huggingface.co/blog/feed.xml` | ✅ 200、256,302 bytes | 868 items，窗口內 5 則，**4 則已被自動化撿走**，另 1 則 Liquid AI 模型文 | 2026-09-24 14:08Z |
| Apple Newsroom（Atom） | `https://www.apple.com/newsroom/rss-feed.rss` | ✅ 200、19,035 bytes | 20 entries，窗口內 2 則（Mac 開賣、倫敦音樂廳），非 AI | 2026-09-22T12:59Z |
| Apple Developer | `https://developer.apple.com/news/rss/news.rss` | ✅ 200、427,604 bytes | 146 items，**窗口內 0 則** | Fri, 18 Sep 2026 10:00 PDT |
| Mistral | `https://mistral.ai/news/` | ✅ 200、1,257,494 bytes，無 feed | **窗口內 0 則** | September 16, 2026 |
| Mozilla | `https://blog.mozilla.org/en/feed/` | ✅ 200、148,613 bytes | 窗口內 2 則（視窗類型說明、手機專注模式），非新聞 | 2026-09-24 17:00Z |
| 歐盟執委會 | `https://digital-strategy.ec.europa.eu/en/news` | ✅ 200、69,674 bytes | 窗口內 AI 題 0 則（DSA、Greenland、投資人公約） | 24 September 2026 |
| 英國 AISI | `https://www.aisi.gov.uk/blog` | ✅ 200、145,287 bytes | 未逐則展開（見「懷疑但未查證」） | — |
| Amazon／AWS | `aboutamazon.com/news`、`aws.amazon.com/about-aws/whats-new/recent/feed/` | ✅ 200、301,585／231,691 bytes | 未逐則展開（見「懷疑但未查證」） | — |
| Qwen | `https://qwen.ai/blog` | ❌ 200、94,344 bytes，**與前兩輪位元組數完全相同的 SPA 殼**。**未查到** | 0 | 未查到 |
| DeepSeek | `https://api-docs.deepseek.com/news/`、`/updates` | ❌ 200、48,088／48,079 bytes，**軟性 404**。**未查到** | 0 | 未查到 |
| 聯合國新聞稿 | `https://press.un.org/en/content/security-council/meeting-coverage` | ❌ 200、**3,038 bytes 的挑戰頁**（CSP＋字型預載，無正文）。**未查到** | 0 | 未查到 |
| 數位發展部 | `https://moda.gov.tw/press/press-releases/` | ❌ **404**、4,014 bytes（網址是我推測的，**不算管道失效，也不能當「數位部沒發新聞」的證據**） | 0 | 未查到 |
| 國科會 | `https://www.nstc.gov.tw/folksonomy/list/…` | ❌ **404**、2,492 bytes（同上，網址是推測的） | 0 | 未查到 |

### 這一輪踩到或避開的取得陷阱

1. **自動化看不到 OpenAI 與 Anthropic 的一手公告。** `automation-candidates.tsv` 185 列的網域只有 10 個（CoinDesk 55、TechCrunch 44、The Verge 30、NVIDIA 19、blog.google 13、Apple 8、Hugging Face 8、CFTC 4、Microsoft 3、DeepMind 1），
   **沒有 `openai.com`、`anthropic.com`、`claude.com`、`x.ai`**。本輪的前三名候選全部來自這個盲區。建議另開票讓自動化加掛 `openai.com/news/rss.xml`。
2. **Anthropic 的 Opus 5.5 公告不在 `/news` 的 `publishedOn` 清單裡**，網址是 `/claude-opus-5-5`（不是 `/news/…`），只出現在 featured grid（`date: 2026-09-22`）與 `siteSettings` 的網址清單。
   只掃 `publishedOn` 的人會以為 Anthropic 這週只發了 enzyme 一篇。
3. **`openai.com/index/*` 今天是間歇性 403**：9 篇裡 8 篇 200，`better-prompt-caching-for-gpt-6` 是 403。沒有改用封存，該頁列為沒讀到。
4. **`blog.google/rss/` 這次被 20 則上限截掉窗口前段**（最舊 09-22 16:00Z）；用三個分區 feed 補回 09-21 16:00Z→09-22 16:00Z，補到的兩則上一輪已列過。上一輪自己預告過這件事。
5. **Google Vids 那篇的說明中心連結是 Google 內部草稿網域**（`support-content-draft.corp.google.com`），外部讀不到；不能拿來當來源，也不能自己改寫成 support.google.com。
6. **本輪取得過程中有一次 DNS 失敗**（`claude.com` 07:59Z 之後 `Could not resolve host`，rc=6），機器隨後閒置約五小時，13:01Z 重抓成功（556,381 bytes）。`fetch-log-ai.tsv` 兩筆都留著。

---

## 結論

- 窗口內（2026-09-21T16:00Z → 掃描結束）真正的大新聞大多**已被每小時自動化撿走**（Meta Connect、OpenAI 代理事件、Anthropic 生物實驗室、Gemini 代打電話等，見下方清單）。
- 自動化沒有撿、而且對台灣讀者重要的，**集中在 OpenAI 與 Anthropic 自家公告**：ChatGPT 廣告開到台灣、GPT-6 Sol／Luna、Claude Opus 5.5 三則最重要；
  其次是 Altman 在安理會的發言與 MentalHealthBench；Google Vids 免費 AI 影片是唯一「今天就能免費試」的題目，但要先補地區與語言。
- 共 **8 則候選**（6 則建議寫、1 則次要可合併、1 則補遺），**0 則與站上既有文章重複**；但候選 1 會讓站上三篇既有文章的「台灣未開放」說法過期，需要另開維護票。
- 候選 2 與 3 是同週的兩家模型發布、互相拿對方比分數；候選 4、7 與 09-21 已寫的 frontier-standards 同屬「OpenAI 前沿治理」，**這兩組各自要協調分工，避免重講**。

---

## 候選清單

依「對台灣一般讀者的重要性」排序。「來源狀態」的 ✅ 表示**開了原文頁並讀到 body**。
事件日規則：feed 給的是真實時刻就換算台北（`BRIEF.md` 第 11 條）；`00:00Z`／`16:00Z` 佔位時刻與只印日期的頁面維持發布者印的那一天。

### 1. ChatGPT 廣告開到台灣（OpenAI）— 建議寫，第一順位

- **slug**：`ai-news-chatgpt-ads-taiwan-20260923`
- **事件日**：2026-09-23（feed `pubDate` 02:00Z → 台北 09-23 10:00；頁首印 September 23, 2026，兩者同日）
- **一手來源**
  - ✅ `https://openai.com/index/chatgpt-ads-expands-southeast-asia-taiwan/` — 200、386,724 bytes
  - ✅ `https://help.openai.com/articles/20001245-ads-manager-availability`（落地 `/en/articles/…`）— 200、63,893 bytes；國家表中 **Taiwan 標為 Available**（自助 Ads Manager）
  - 背景（未重抓）：同頁連到的 `/index/expanding-access-to-ai-with-chatgpt-ads/`
- **為什麼重要**：這是本輪唯一**直接寫到台灣**的 AI 公告。公告寫「Starting today」開始在印尼、馬來西亞、菲律賓、新加坡、泰國、越南與台灣推出；
  **廣告只給 Free 與 Go 方案看，Plus、Pro、Enterprise 維持無廣告**。台灣大量使用免費版的讀者接下來會在 ChatGPT 裡看到廣告，
  台灣商家則多了一個投放管道（Ads Solutions 團隊、代理商、或符合資格者自助 Ads Manager）。蝦皮（Shopee）在公告中具名合作。
- **容易寫錯的地方**
  1. 「開始推出」≠「每個台灣帳號今天都看得到」：原文是 “will begin rolling out”，要寫成逐步推出。
  2. 無廣告方案原文只列 **Plus、Pro、Enterprise**；Business、Edu 沒寫，不可自行補進「付費方案都沒有廣告」。
  3. Help Center 是**活文件**（頁面自印 “Updated: 11 hours ago”），國家表是 2026-09-26 當下的快照；自助資格看的是「登錄並付款的法律實體所在地」，不是使用者所在地。
  4. 「超過 60 個國家」「年化營收 10 億美元」「數萬家廣告主」都是 OpenAI 自報數，要寫成「OpenAI 表示」；**10 億美元是 8 月底的舊公告**，不是這次的新數字。
  5. 「廣告不影響回答、對話不給廣告主」是 OpenAI 的原則宣示，本站無法驗證，照宣稱寫。
- **重疊檢查**：`automation-candidates.tsv` 以 `ads`／`Taiwan`／`chatgpt` 查無此事件。站上相關的三篇都**會因此過期**：
  `ai-news-chatgpt-ads-20260505`（寫「台灣是否已開放，本文沒有答案」）、`ai-news-chatgpt-sponsored-agents-20260916`（標題寫「台灣未列入開放名單」，查核日 09-18）、
  非新聞的 `chatgpt-ads-status`（寫「台灣未列在自助可用名單」）。**新文章是新事件，不是重寫；但另要開一張維護票更新那三篇的台灣狀態**，否則站上會同時有互相矛盾的說法。

### 2. GPT-6 Sol 與 GPT-6 Luna 推出、API 價格砍半（OpenAI）— 建議寫

- **slug**：`ai-news-gpt-6-sol-luna-20260923`
- **事件日**：**2026-09-23 台北**（feed `pubDate` Tue, 22 Sep 2026 18:00 GMT → 台北 09-23 02:00；OpenAI 頁面印 Sep 22, 2026）。**跨日**，文中兩個日期都要寫。
- **一手來源**
  - ✅ `https://openai.com/index/introducing-gpt-6-sol-and-luna/` — 200、846,858 bytes
  - ❌ `https://openai.com/index/better-prompt-caching-for-gpt-6/` — **403**、9,922 bytes（擋阻頁）。同一天的配套文章，**沒讀到**；快取的內容 Sol/Luna 主文已有一節可用
  - 建議撰稿時補：`developers.openai.com/api/docs/guides/prompt-caching`（主文連結，**本輪未抓**）與 system card（主文連結，**本輪未抓**）
- **為什麼重要**：GPT-6 家族從 Astra 往下擴到兩個較便宜的型號，**Free 與 Go 使用者可以在桌面 App 用 GPT-6 Luna**——這是一般台灣讀者真正會碰到的部分。
  API 價格：Sol 每百萬 token 輸入 $4→$2、輸出 $20→$10；Luna 輸入 $0.20→$0.10、輸出 $1.20→$0.50。
- **容易寫錯的地方**
  1. 「便宜 50%」的比較基準是 **“compared with their GPT‑5.6 promotional pricing”**——拿掉 promotional 就換了主張。
  2. 開放範圍：ChatGPT Work 與 Codex 對 Plus、Pro、Business、Enterprise、Edu；Free 與 Go **只有 Luna、只在桌面 App**；原文明寫 **“These models are not yet available in Chat.”**；而且當天是「gradually throughout the day」逐步推出。
  3. 所有與 Claude Opus 5／Fable 5.1 的比較都是 OpenAI 自己選的評測（AutomationBench、Agents' Last Exam、FrontierCode、DeepSWE、OSWorld 2.0），而且註腳說對手分數取自公開報告、Fable 5.1 缺值時用 Fable 5 代替——**一律寫成 OpenAI 表示**，不能寫成「GPT-6 Sol 比 Claude 強」。
  4. 「事實錯誤減少約一半」來自**內部評測、而且特意挑了使用者曾回報錯誤的對話**，OpenAI 自己說不代表一般使用。
  5. 本輪候選 3（Claude Opus 5.5）同一天發布、互相引用對方的舊型號；兩篇不要互相重講，也不要把兩家的價格放進同一張表當成本站實測。
- **重疊檢查**：自動化查無（它不看 openai.com）。站上相鄰：`ai-news-gpt-6-astra-20260903`（Astra 本身）、`ai-news-gpt-56-price-cut-20260730`、`ai-news-gpt-56-sol-preview-20260626`——**都是前一代或旗艦，Sol/Luna 的 GPT-6 版站上第一次出現**。

### 3. Claude Opus 5.5 推出（Anthropic）— 建議寫

- **slug**：`ai-news-claude-opus-55-20260922`
- **事件日**：2026-09-22（頁首只印 “September 22, 2026”，newsroom featured grid 的 `date` 也是 `2026-09-22`，**沒有時刻**，無法換算，維持發布者日期）
- **一手來源**
  - ✅ `https://www.anthropic.com/claude-opus-5-5` — 200、619,967 bytes（注意路徑**不是** `/news/…`）
  - ✅ `https://www.anthropic.com/news` featured grid — 200、459,343 bytes（只用來確認日期；這篇不在 `publishedOn` 清單裡，用 `publishedOn` 掃的人會漏掉它）
  - ✅ `https://claude.com/blog/claude-opus-5-5-built-for-coding-sessions-that-use-more-context` — 200、542,889 bytes，**2026-09-24** 的後續文（Claude Code 用量趨勢與快取），日期與主公告不同
  - 建議撰稿時補：Opus 5.5 System Card（主文連結，**本輪未抓**）
- **為什麼重要**：新家族「Claude 5.5」的第一個模型；Anthropic 說在多數工作上達到 Fable 5.1 的水準、執行成本比 Opus 5 少 40%。
  **對訂閱使用者：Pro、Max、Team 與按席次計費的 Enterprise 提高五小時用量上限，另給一次可自行保留、自選時間使用的額度重置。**
  這也是 Anthropic 在〈We Must Pace the Frontier〉之後的第一個發布，發布前的外部評估者**包括**（including，非全名單）Frontier Design 與 METR。
- **容易寫錯的地方**
  1. 「便宜 40%」是 **“at default settings … on typical workloads”** 的估計；定價本身是輸入／輸出各降 20%（$4／$20 每百萬 token）、快取讀取降 60%（$0.20）。三個數字不能混成一個。
  2. **Sonnet 5.5 與 Haiku 5.5 還沒推出**，原文是 “will follow in the coming weeks”。
  3. 生物研究要走 Life Sciences Verification Program（今天可申請）；資安要等 Cyber Verification Program「未來幾週」擴大——**不是發布當天人人可用於資安工作**。
  4. Anthropic 自己寫「benchmark margins have become a less reliable guide」，而且 AutomationBench 的 Opus 5.5 分數是 Zapier 在搶先測試期間跑的；評測表要連同這些但書一起寫。
  5. 用量上限提高的方案清單**沒有 Free**，也沒寫各方案提高多少；不要自己補數字。
  6. 免費版能不能用 Opus 5.5：**本輪讀到的正文沒有寫**，撰稿時要去讀 availability 段落或說明頁，查不到就寫「官方未說明」。
- **重疊檢查**：自動化只有 TechCrunch〈Astra and Opus just passed Turing's other test〉（09-25，rejected）提到 Opus，**那是一篇評論，不是發布事件**，判定不重疊；請協調者確認。
  站上相鄰：`ai-news-claude-opus-5-20260724`、`ai-news-claude-fable-51-20260901`、`ai-news-pace-the-frontier-20260912`、`ai-news-anthropic-life-sciences-verification-20260917`——Opus 5.5 **站上第一次出現**。

### 4. Sam Altman 在聯合國安理會發言（OpenAI）— 建議寫，但角度要窄

- **slug**：`ai-news-altman-un-security-council-20260923`
- **事件日**：2026-09-23（feed 12:00Z → 台北 09-23 20:00；頁首印 September 23, 2026）
- **一手來源**
  - ✅ `https://openai.com/index/sam-altman-un-security-council-remarks/` — 200、402,238 bytes，標註 “Remarks as delivered” 的全文
  - ❌ `https://press.un.org/en/content/security-council/meeting-coverage` — 200 但 **3,038 bytes 挑戰頁**，聯合國自己的會議紀錄**沒讀到**。撰稿時要另找聯合國的會議紀錄或 webtv 頁當第二來源，找不到就只能寫「OpenAI 公布的講稿」
  - 可並用：✅ `https://openai.com/index/openai-extends-cyber-access-to-ukraine-for-civilian-defense/`（200、373,892 bytes，同日、同在聯大周邊宣布，Daybreak 資安工具提供給烏克蘭政府）
- **為什麼重要**：AI 公司執行長上安理會本身就是新聞；講稿裡有幾句會被大量引用的話——**「我們過去曾單方面放慢，將來也會」**、
  災難風險不論估 10%、1%、12% 還是 0.1%「都不可接受」（原文四個數字照抄，不要挑）、兩種必須避免的失敗（失去控制、權力過度集中）、以及「不能只由舊金山的實驗室決定」。
- **容易寫錯的地方**
  1. **Navier–Stokes**：講稿說 “one of our models solved one of the Millennium Prize Problems”，但 OpenAI 自己的文章標題是 **“An OpenAI model proposes a solution to the Navier–Stokes problem”**（見 MentalHealthBench 頁的延伸閱讀連結）。
     「解出」是執行長在演講中的說法、「提出解法」是公司正式標題，**不可寫成已被數學界確認解決**；`ai-news-openai-math-advisory-20260921` 怎麼寫的要先讀。
  2. 國際標準、事故通報、政府間安全管道這一段幾乎就是 09-21〈Building standards for the next phase of AI〉的內容，**已寫成 `ai-news-openai-frontier-standards-20260921`**；本篇只能引一句並連過去，不能重講。
  3. “I largely agree with Professor Bengio” 表示 Bengio 同場發言，但**他說了什麼本輪沒有來源**，不要轉述。
  4. 這是一段演講，不是政策或承諾文件；「會放慢」要寫成 Altman 在安理會的說法。
- **重疊檢查**：自動化只有 The Verge〈Bernie Sanders proposes banning ‘superintelligence’〉（09-23），**不同事件**；以 `altman`／`security council`／`UN` 查無。
  站上 `ai-news-openai-frontier-standards-20260921`、`ai-news-pace-the-frontier-20260912`、`ai-news-openai-math-advisory-20260921` 是**近鄰但不同事件**，重疊風險高，請協調者決定是否併成一篇「OpenAI 在聯大周的三件事」（安理會、烏克蘭 Daybreak、第三方評估原則）。

### 5. MentalHealthBench：OpenAI 開放心理健康對話評測（OpenAI）— 建議寫

- **slug**：`ai-news-openai-mentalhealthbench-20260923`
- **事件日**：2026-09-23（feed 10:00Z → 台北 09-23 18:00；頁首印 September 23, 2026）
- **一手來源**
  - ✅ `https://openai.com/index/introducing-mentalhealthbench/` — 200、1,473,989 bytes
  - 論文 PDF：`https://cdn.openai.com/ctf-cdn/MentalHealthBench_A_Comprehensive_Benchmark_of_AI_Capabilities_in_Realistic_Mental_Health_Conversations.pdf`（主文連結，**本輪未抓**；撰稿前必讀，語言清單與評分方法在那裡）
- **為什麼重要**：大量讀者會拿 ChatGPT 談壓力、感情與家人問題；這份評測把「AI 怎麼回應心理健康對話」拆成十個行為面向（安全、先問清楚情境、尊重當事人自主、適時給可行建議等），
  由 **22 國、說 19 種語言的 80 多位持照心理師與精神科醫師**共同訂標準，並**開放**給其他研究者使用。另有 44 位曾用 AI 尋求情緒支持的成人（16 國、14 種語言）參與評分。
- **容易寫錯的地方**
  1. 原文只說 “across multiple languages and regions”，**本輪讀到的正文沒有列出是否含中文**；要寫語言就去讀論文，查不到就不寫。
  2. 評分者是 **GPT‑5.6 Sol 自動評分**——OpenAI 自己的模型在評所有廠商的模型，而且是 OpenAI 自己設計的評測；模型排名一律寫成 OpenAI 公布的結果，不寫成客觀排名。
  3. 對話是**合成的**；OpenAI 自己寫情境比例不代表 ChatGPT 的實際話題分布。
  4. 「ChatGPT 每週超過 10 億人使用」是自報數。
  5. 這是心理健康題目，文末要給台灣求助管道（例如衛福部安心專線），但**必須以衛福部官方頁為來源**，本輪沒有查，撰稿時補。
- **重疊檢查**：自動化以 `mental` 查無。站上相鄰只有 `ai-news-chatgpt-health-20260107`（健康資料整理）與 `ai-news-openai-australia-youth-safety-20260918`（青少年安全），**心理健康評測站上第一次出現**。

### 6. Google Vids 開放任何 Google 帳號免費用 Gemini Omni 1.1 做 AI 影片（Google）— 建議寫，要先補地區與語言

- **slug**：`ai-news-google-vids-omni-free-20260924`
- **事件日**：**2026-09-24 台北**（`datePublished 2026-09-23T19:00:00+00:00` → 台北 09-24 03:00；頁面印 Sep 23, 2026）。**跨日**。
- **一手來源**
  - ✅ `https://blog.google/products-and-platforms/products/workspace/gemini-omni-in-google-vids/` — 200、380,362 bytes
  - 第二來源**本輪沒有**：文中「Google Workspace Learning Center」連結指向 **`support-content-draft.corp.google.com/a/users/answer/16909538`，是 Google 內部草稿網域**，外部讀不到，**不能引用**；
    把它改寫成 `support.google.com/…/16909538` 屬於推導網址（`BRIEF.md` 第 7 條），要另從 support.google.com 搜到真實頁面才能用。
- **為什麼重要**：原文寫 “anyone with a Google or Google Workspace account can generate high-quality videos at no cost”，模型是 **Gemini Omni 1.1 Flash**，
  可延長場景、指定片段秒數、產生 1080p。對台灣一般讀者是「免費、今天就能試」的少數題目；每段 AI 片段都嵌 SynthID 浮水印，可與 `ai-news-eu-transparency-20260802` 的標示議題相連。
- **容易寫錯的地方**
  1. 「免費」有額度：原文另寫想要更多生成量要看 Google AI 方案、Workspace Business／Enterprise 有「expanded generation pools」——**免費版的額度多少，原文沒寫**。
  2. **地區、語言、年齡限制原文都沒寫**；「anyone」不等於台灣帳號、中文介面都能用。這是動筆前必查的一件事，查不到就寫「官方未說明」。
  3. 只寫了桌面版（“visiting vids.new on desktop”），不要寫成手機也能用。
  4. Gemini 3.8 Flash-Lite 語音旁白是 **“Coming soon”**，還沒上線；而且 3.8 TTS 本身已被自動化撿走（09-23 “Gemini 3.8 Flash TTS and Gemini 3.8 Flash-Lite TTS”），不要把它當本篇的新功能。
  5. 頁面上的「Read AI-generated summary」照例跳過（上一輪 Googlebook 的教訓），只引正文。
- **重疊檢查**：自動化以 `vids`／`omni` 查無（只有同週的 TTS 與 Live Avatar，**不同事件**）。站上 `ai-news-gemini-omni-20260519` 寫的是 I/O 上的 Gemini Omni 本身，**Vids 免費開放是新事件**。

### 7. OpenAI 公布第三方評估的優先事項與原則（OpenAI）— 次要，或併入候選 4

- **slug**：`ai-news-openai-third-party-assessments-20260922`
- **事件日**：2026-09-22（feed `00:00:00 GMT` 是**佔位時刻，不換算**；頁首印 September 22, 2026）
- **一手來源**
  - ✅ `https://openai.com/index/priorities-principles-third-party-assessments/` — 200、426,589 bytes
- **為什麼重要**：OpenAI 說要讓外部評估機構在訓練、評估與部署各階段取得「深層存取」（包括可見的思考鏈、內部部署存取），提出四個優先評估領域，
  直接連到 Anthropic 的〈We Must Pace the Frontier〉（原文用的就是 “pace the frontier” 一詞並加了連結）與同週 Opus 5.5 的外部評估。對一般讀者是背景，對關心 AI 安全的讀者是這一週的第三塊拼圖。
- **容易寫錯的地方**
  1. 原文限定範圍：這些原則針對的是**民間與非營利評估機構做技術安全評估**，與政府的測試「可能需要不同做法」；不要寫成 OpenAI 對政府監理的承諾。
  2. 評估「generally longer-term and launch-agnostic」，**不是上市前審查**；原文說也「may inform deployment decisions」，這個 may 要留著。
  3. 「前所未有的存取程度」是 OpenAI 對自己的描述，要寫成宣稱。
- **重疊檢查**：自動化查無。站上相鄰 `ai-news-openai-frontier-standards-20260921`（國際標準）、`ai-news-openai-misalignment-reports-20260917`（通報）——**第三方評估這個角度站上沒有**，但三篇同屬「OpenAI 的前沿治理」系列，**建議協調者考慮與候選 4 合併**。

### 8.（補遺，事件日在窗口前一天）Grok 4.7 推出（SpaceXAI，原 xAI）— 次要

- **slug**：`ai-news-grok-47-20260921`
- **事件日**：2026-09-21（頁面 `datePublished 2026-09-21T00:00:00Z`，是只到日的佔位值；卡片印 Sep 21, 2026）。**不在本輪窗口內**，照指示列為 09-12～09-21 的補遺。
- **一手來源**
  - ✅ `https://x.ai/news/grok-4-7` — 200、291,841 bytes
  - ✅ `https://x.ai/news` — 200、271,663 bytes（列表，確認日期與順序）
  - 建議撰稿時補：`https://docs.x.ai/developers/models`（主文連結，**本輪未抓**）
- **為什麼重要**：三大模型商之外另一家前沿模型的更新，價格每百萬 token 輸入 $2、輸出 $6（與 Grok 4.6 同價），主打長時間的程式與知識工作；
  **公司名稱已是 SpaceXAI**（頁尾 © 2026 SpaceXAI LLC），站上若還寫 xAI 要注意。這一週 OpenAI、Anthropic、SpaceXAI 三家在四天內都發了新模型並互相拿對方比分數，可作為一篇「同週三個模型怎麼看」的素材。
- **容易寫錯的地方**
  1. 全部評測表都是 SpaceXAI 自己選、自己跑的；DeepSWE 那格有星號（high effort），表格的比較對象是 GPT-5.6 Sol 與 Fable 5.1，**不是**同週的 GPT-6 Sol 或 Opus 5.5——不要把三家的表拼成一張。
  2. 「invite-only」的紅隊能力只給特定資安夥伴。
  3. 上市地點寫的是 Cursor、Grok Build、Grok API 與第三方平台；**Grok App 一般使用者能不能用，原文沒寫**。
- **重疊檢查**：自動化以 `grok`／`xai` 查無（0 列）。站上 74 份 `ai-news-*.json` **沒有任何一篇以 Grok 為題**。

---

## 看過但不建議寫（窗口內）

| 日期（UTC → 台北） | 題目 | 來源狀態 | 不寫的理由 |
| --- | --- | --- | --- |
| 09-23 16:00 → 09-24 00:00 | A new wave of Connected Apps is rolling out to Gemini（Google） | ✅ 200、389,501 bytes | 新連接的 App 多為美國服務（apartments.com、Experian、Peloton、SeatGeek…），正文只有 1,027 字元，沒寫地區；台灣讀者可用性低 |
| 09-23 → 09-23 | Claude Marketplace（Anthropic，claude.com） | ✅ 200、556,381 bytes | 企業採購管道（用既有 Anthropic 承諾支出購買合作廠商產品、2,000 個以上 connector／plugin），讀者面窄；若要寫可與候選 3 併提 |
| 09-24／09-25 | Claude Tag personal connectors、Build plugins for Claude（claude.com） | 只看列表卡片 | 產品小更新 |
| 09-23 13:00 → 09-23 21:00 | OpenAI extends cyber access to Ukraine（Daybreak） | ✅ 200、373,892 bytes | 單一國家政府合作；可當候選 4 的輔助來源 |
| 09-23 00:00（佔位）→ 09-23 | Grab and OpenAI bring practical AI skills to Southeast Asia | ✅ 200、395,016 bytes | 對象是新加坡起、之後泰印菲馬越的 Grab 夥伴，**台灣不在名單** |
| 09-23 16:00 → 09-24 00:00 | Two years of OpenAI Academy | ✅ 200、418,042 bytes | 回顧加新的講師計畫；學習路徑 09-21 已寫成 `ai-news-openai-academy-paths-20260921` |
| 09-22～09-25 | OpenAI 客戶案例 6 則（Parallel、Airbnb、Harvey、invideo、Ringg、Proaction） | 未開原文 | 客戶案例，無 OpenAI 自己的新事實 |
| 09-22 23:50 → 09-23 07:50 | Google × Gates Foundation：2 億南方國家農民 | 未開原文 | 對象是 Global South 農民 |
| 09-22 16:00 → 09-23 00:00 | Investing in global talent and AI literacy（Google × ITU） | 未開原文 | 捐款／培訓計畫，查核成本高、讀者面窄 |
| 09-23 16:00 → 09-24 00:00 | MedGemma is helping global healthcare providers | 未開原文 | 醫療機構案例彙整 |
| 09-24 17:00 → 09-25 01:00 | New health and safety tools live in the Google Health app | 未開原文 | 可能是 AI 功能，但 Google Health app 在台灣的可用性不明，列入「懷疑但未查證」 |
| 09-22 → 09-23（卡片） | Meta Takes Action on 3.7 Million Accounts… with Singapore Police Force | 只看卡片 | 反詐騙執法合作，AI 份量不明，且屬新加坡 |
| 09-22 | Introducing Claude Opus 5.5 以外的 Anthropic featured「Ebola response」 | 只看 featured grid | 專題報導（feature），非公告 |
| 09-24 14:08 → 09-24 22:08 | Liquid AI LFM2.5-VL-DSpark（Hugging Face） | 只看 feed | 開發者模型文；自動化已撿同 feed 的其他 4 則 |

**已被自動化撿走、因此排除的窗口內大題**（逐一對過 `automation-candidates.tsv`）：Meta Connect 2026（Muse 上眼鏡、Muse Charm、無鏡頭眼鏡、VR Glasses）、
Anthropic 生物實驗室 enzyme 發現（09-23）、Anthropic 創辦人投票權／IPO（09-25）、Anthropic × Akamai 116 億美元（09-25）、
OpenAI 代理入侵澳洲政府網站與後續調查（09-24）、OpenAI agent swarms（09-25）、OpenAI 代理外洩 53 張使用者圖片（09-25）、
Gemini 代打電話（09-24）、Gemini 3.8 Live Avatar（09-24）、Gemini 3.8 TTS（09-23）、Private AI Compute 伺服器端記憶（09-23）、
Google Beam 擴區（09-23）、Project Suncatcher 太空 AI（09-24）、Made on YouTube 的 AI 功能（09-23）、Google Photos 虛擬衣櫥（09-24）、
Microsoft 新 Copilot（09-25，科技已發布）、Sony／UMG 再告 Suno（09-25）、Supabase 資料外洩（09-25）、Bernie Sanders 超級智慧禁令（09-23）、加州資料中心法案（09-23）。

---

## 讀不到／查不到

| 對象 | 實際發生什麼 | 這代表什麼 |
| --- | --- | --- |
| **OpenAI〈Better prompt caching for GPT-6〉** | `openai.com/index/better-prompt-caching-for-gpt-6/` 回 **403**、9,922 bytes | 沒讀到。候選 2 的快取內容改用 Sol/Luna 主文的那一節；**不可把這一頁放進 `sources[]`** |
| **聯合國安理會會議紀錄** | `press.un.org/en/content/security-council/meeting-coverage` 回 200，但只有 **3,038 bytes 的挑戰頁** | 沒讀到。候選 4 目前只有 OpenAI 自己公布的講稿一條一手來源，要再找聯合國的正式紀錄 |
| **Qwen** | `qwen.ai/blog` 200、94,344 bytes，與前兩輪同一個 SPA 殼 | **未查到**，不是「沒發布」 |
| **DeepSeek** | `api-docs.deepseek.com/news/`、`/updates` 都是 200、約 48 KB 的軟性 404 | **未查到**，不是「沒發布」 |
| **數位發展部、國科會** | 兩個網址都是我**推測**的，回 404 | 這只證明網址猜錯，**不是台灣主管機關沒有 AI 新聞的證據**。本輪沒有查到台灣政府的 AI 題目，下一輪要先從 sitemap 或首頁取真實列表網址 |
| **Google Vids 說明中心** | 連結指向 Google 內部草稿網域 | 讀不到；候選 6 需要另找公開的說明頁 |
| **Claude Opus 5.5 的上市範圍段落** | `/claude-opus-5-5` 讀到的 `<article>` 正文沒有「在哪些方案／平台可用」那一段（只讀到 Fast mode 一句） | 候選 3 撰稿時要讀完整頁或 system card；目前「免費版能不能用」是**未查到**，不是「不能用」 |

---

## 懷疑但未查證

1. **Google Health app 的「health and safety tools」**（blog.google，09-24 17:00Z）：標題像 AI 健康功能，但沒開原文，也不知道台灣能不能下載。
2. **英國 AISI 部落格**抓到了（145,287 bytes）但沒有逐則展開；自動化撿過 Hugging Face 上的〈How UK AISI and EvalEval…〉（09-22），AISI 自己的站可能還有別的窗口內文章。
3. **Amazon／AWS**：兩個頁面都抓到了但沒有逐則展開；Alexa 或 Bedrock 的窗口內新模型（例如 GPT-6 Sol/Luna 或 Opus 5.5 上 Bedrock）可能有公告。
4. **台灣本地的 AI 政策**：數位部、國科會、行政院在 9/22–9/26 是否有 AI 基本法子法、主權 AI 或 TAIDE 的公告，本輪因網址猜錯而**沒有查到**。
5. **OpenAI 的 GPT-6 Sol/Luna system card 與 Anthropic 的 Opus 5.5 system card**：都沒抓；兩家的安全評估細節（例如 Opus 5.5 生物與資安能力「與 Mythos 5.1 相當」）要從那裡核對。
6. **Gemini 4**：自動化撿到 The Verge〈Gemini 4 is almost ready〉（09-24，rejected），那是訪談不是發布；若窗口結束前 Google 正式發布，本清單沒有涵蓋。
7. **Meta 與新加坡警方的反詐騙合作**是否用到 AI 偵測，沒讀原文。
8. **ChatGPT 廣告在台灣的中文版公告**：OpenAI 可能另有繁中頁面或台灣媒體說明會；若有，要照 `BRIEF.md` 第 8 條比對兩個語系的說法。

---

## 統計

- 窗口 2026-09-21T16:00Z → 掃描結束 **2026-09-26T13:03Z**（台北 21:03）。各管道窗口內的列表筆數（未去重，同一事件在 Google 與 DeepMind 各算一次）：
  OpenAI feed 15、blog.google（總 feed 20＋分區 feed 補回 2）22、DeepMind 3、NVIDIA 8、Meta 5、Claude blog 6、Anthropic newsroom 3（含 featured grid 的 Opus 5.5 與 Ebola 專題）、
  Hugging Face 5、Apple Newsroom 2、Mozilla 2、Microsoft 1、SpaceXAI 1，**合計 73 筆**。這些是取得時的列表值，不是可以寫進文章的事實。
- **開了原文並讀到 body：14 篇**（OpenAI 8、Anthropic／Claude 3、Google 2、SpaceXAI 1），外加 OpenAI Help Center 1 頁；**403 一篇**（OpenAI prompt caching）。
- 候選 **8 則**：建議寫 6（ChatGPT 廣告台灣、GPT-6 Sol/Luna、Claude Opus 5.5、Altman 安理會、MentalHealthBench、Google Vids 免費 AI 影片）、
  次要可合併 1（OpenAI 第三方評估原則）、補遺 1（Grok 4.7，09-21）。
- **與既有文章重複：0 則**；**會讓既有文章過期：3 篇**（ChatGPT 廣告相關，見候選 1）。
- 零產出的管道：Apple Developer、Mistral、歐盟執委會（AI 題）——**讀到了但窗口內沒有新東西**，與「讀不到」不同。
- 讀不到的管道：Qwen、DeepSeek、聯合國新聞稿；網址猜錯：數位部、國科會。

## 要協調者拍板的事

1. **候選 1 要不要連帶開維護票**，更新 `ai-news-chatgpt-ads-20260505`、`ai-news-chatgpt-sponsored-agents-20260916`、`chatgpt-ads-status` 的台灣狀態。不更新的話，新文章一上線，站上就會同時寫「台灣已開放」與「台灣未列入」。
2. **候選 2、3（與補遺 8）是分開寫還是合成一篇「同週三個新模型」**。建議分開寫 2 與 3（受眾不同：ChatGPT 使用者對 Claude 使用者），8 只當補充。
3. **候選 4 與 7 是否合併**，以及如何與已寫的 `ai-news-openai-frontier-standards-20260921` 分工。
4. **請自動化加掛 `openai.com/news/rss.xml`**：本輪前三名全落在它的盲區。
