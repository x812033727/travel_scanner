# AI 垂直候選：2026-09-16 起（查核日 2026-09-18）

窗口 **2026-09-16 00:00 UTC 起至 2026-09-18**。既有 AI 內容包 50 篇加一份索引與一份來源清單，
最新事件日 **2026-09-15**（`ai-news-gemini-38-live-20260915`），`display_order` 最大值 **160**
（`ai-news-nvidia-hugging-face-20260903`），新文章從 **161** 接續。

所有請求都用 `curl -sL -A "Mokaair-editorial"`，沒有任何請求帶入 email 或個人資料。

---

## 掃過的管道與結果

「拿到 feed 了嗎」一律看兩件事：item／entry 數量，以及最新一筆的日期。狀態碼不算。

| 管道 | 位址 | 結果 | 數量 | 最新一筆 |
| --- | --- | --- | --- | --- |
| OpenAI（feed） | `https://openai.com/news/rss.xml` | ✅ 200、737,319 bytes | 1,208 筆帶 `pubDate` | Thu, 17 Sep 2026 12:00:00 GMT |
| OpenAI（文章頁） | `https://openai.com/index/*` | ✅ **今天不擋**，7 篇全部 200 並讀到正文（349,657–516,081 bytes） | 7/7 | — |
| OpenAI Alignment | `https://alignment.openai.com/misalignment-reports/` | ✅ 200、9,009 bytes | 3 則 Notice ＋ 6 份 Report（2026-09-18 當下） | Notice 2026-09-11；兩份 Report 印 `Report updated: Sep 16, 2026` |
| Google | `https://blog.google/rss/` | ✅ 200、30,544 bytes | 20 items | Thu, 17 Sep 2026 20:00:00 +0000 |
| NVIDIA | `https://nvidianews.nvidia.com/releases.xml` | ✅ 200、68,385 bytes | 20 items | Thu, 17 Sep 2026 13:00:55 GMT |
| Anthropic | `https://www.anthropic.com/news`（無 feed） | ✅ 200、462,587 bytes | RSC JSON 內 265 筆 `publishedOn`，另有獨立的 featured grid | `publishedOn` 最新 2026-09-17T15:56:00.000Z |
| Apple Developer | `https://developer.apple.com/news/rss/news.rss` | ✅ 200、425,692 bytes | 145 items | Wed, 16 Sep 2026 10:03:39 PDT |
| Meta AI Blog | `https://ai.meta.com/blog/` | ⚠️ 200、206,195 bytes，但**列表停在 2026-07-27**，窗口內 0 則 | 5 則列表 | 2026-07-27 |
| Meta Newsroom | `https://about.fb.com/news/` | ✅ 200、307,142 bytes，JSON-LD 有 `datePublished`／`dateModified` | — | 2026-09-16 |
| Microsoft | `https://blogs.microsoft.com/feed/` | ✅ 200、155,516 bytes（非指派清單，順手掃的） | 10 items | Thu, 17 Sep 2026 14:00:05 GMT |
| Mistral | `https://mistral.ai/news/` | ✅ 200、1,255,433 bytes，**無 feed、無 ISO 日期**，只有 `September 16, 2026` 這種人讀字串 | — | September 16, 2026 |
| Mozilla | `https://blog.mozilla.org/en/feed/` | ✅ 200、145,922 bytes（Mistral 案的另一個一手方） | 20 items | Thu, 17 Sep 2026 19:30:00 +0000 |
| Qwen（現站） | `https://qwen.ai/blog` | ❌ 200、94,358 bytes，但**可取出的文字只有 4 個字元**；`/sitemap.xml` 與 `/robots.txt` 回**同一份 94,358 bytes 的殼**。**未查到** | 0 | 未查到 |
| Qwen（舊站） | `https://qwenlm.github.io/blog/` | ⚠️ 200、13,828 bytes，但**最新一篇 2025-09-23**，頁面自己寫著已搬到 qwen.ai。`qwenlm.github.io/index.xml` 回 404 | 停更 | 2025-09-23 |
| DeepSeek | `https://api-docs.deepseek.com/news/` | ❌ **軟性 404**：回的是「Your First API Call」文件頁（46,114 bytes）；`/news/news260914` 回同一份。**未查到** | 0 | 未查到 |

### 這一輪踩到或避開的取得陷阱

1. **`openai.com/index/*` 的 403 是間歇性的。** `candidates-tech-and-ai.md` 記的 403、以及前幾輪
   改抓 `web.archive.org` 的做法，今天都不需要：七篇全部 200 並讀到正文。
   「被擋」要現場重測，不能沿用。
2. **`openai.com/zh-TW/index/...` 會轉回英文頁**（最終網址是英文的那一個），所以這批 OpenAI 題目
   **沒有官方繁中版可比對**，正文裡任何中文都是本站自己的翻譯。
3. **Anthropic 的新聞頁是 Next.js RSC**：可用的清單是 HTML 裡的 JSON，markup 上只有 10 個
   `/news/` 連結。**而且 9/17 那則「pace of AI development」根本不在 `publishedOn` 清單裡**——
   它在 `/institute/` 路徑下，只出現在另一塊 featured grid。只掃 `/news/` 會整個漏掉 Anthropic Institute。
4. **`labs.google/cc` 是登入殼**：轉到 `labs.google.com/cc/`，200、127,091 bytes，
   可取出的文字只有「CC Sign in」。不能當來源，也不能拿它的「沒出現」當證據。
5. **猜網址會回滿版的軟性 404。** `mistral.ai/news/mistral-mozilla-firefox` 回 404 但仍送
   241,752 bytes，`blog.mozilla.org/en/firefox/firefox-smart-window-mistral/` 回 404 送 51,186 bytes，
   `help.openai.com/en/articles/12263849-ads-in-chatgpt` 回 404 送 25,629 bytes。**bytes 數不能當成功判準。**
6. **blog.google 的「Read AI-generated summary」又出包一次。** CC 那篇的摘要寫
   「look for an email... to start using it today」，正文寫的是既有使用者「in the coming days」收信、
   新使用者排候補。這個陷阱 `ai-news-gemini-38-live-20260915` 的研究紀錄已經記過，
   建議寫進 `ai.md`，因為這批每碰一篇 blog.google 就會遇到一次。
7. **官方文字裡的隱形字元。** `openai.com/index/astra-for-law/` 全篇的 `GPT‑6 Astra` 用的是
   **U+2011 不斷行連字號**，連引號裡的 `“GPT‑6 Astra Law”` 也是；同一行的 API 代號
   `gpt-6-astra-law` 卻是 ASCII 連字號。**用 ASCII 的 `GPT-6` 去 grep 這頁會查無此字**——
   那正是 `BRIEF.md` 第 2 條說的負面證據陷阱。

---

## 候選清單

「來源狀態」的 ✅ 表示**開了原文頁並讀到 body**；「未開原文」表示只有 feed／列表給的日期與標題。

**事件日照 `agents/DELTA-4-5.md` 第 6 條換算成台北時間。** 這批有兩則因此跨日，
slug 尾碼與發布者自己印的日期**不一樣**，兩份研究紀錄的 `event_date_basis` 都把兩個日期寫清楚了，
文章正文也必須兩個都寫，否則讀者回頭對來源會以為日期錯了。下表的第一欄就是換算前後。

| 日期（UTC → 台北＝事件日） | 標題 | 來源狀態 | 建議 | 重疊 | 研究紀錄／不寫的理由 |
| --- | --- | --- | --- | --- | --- |
| 09-16 13:00 → 09-16 21:00 | Reimagining advertising with AI（OpenAI） | ✅ 200、380,345 bytes | **重要** | 接 `ai-news-chatgpt-ads-20260505`（那篇只寫怎麼買廣告） | `research/ai-news-chatgpt-sponsored-agents-20260916.json` |
| 09-16 17:00 → **09-17 01:00（跨日）** | Our framework for reporting model misalignment（OpenAI） | ✅ 200、418,494 bytes | **重要** | 接 `ai-news-pace-the-frontier-20260912`；要與 `ai-news-anthropic-threat-report-20260910` 明確區分 | `research/ai-news-openai-misalignment-reports-20260917.json`（官方頁印 9/16） |
| 09-17 00:00（**佔位時刻，不可換算**） → 09-17 | Introducing Astra for Law（OpenAI） | ✅ 200、516,081 bytes | **重要** | 與 `ai-news-chatgpt-financial-services-20260910` 是結構孿生，分工要寫死 | `research/ai-news-astra-for-law-20260917.json` |
| 09-17 18:15 → **09-18 02:15（跨日）** | The new CC, an AI agent built for families（Google Labs） | ✅ 200、373,855 bytes | **重要** | 接 `ai-news-gemini-spark-20260519`（CC 在 5 月變成 Daily Brief） | `research/ai-news-google-cc-family-agent-20260918.json`（官方頁印 9/17） |
| 09-17（**頁面不印日期，也不印時刻**，日期取自官方新聞室的 featured grid） | Measurements for understanding the pace of AI development inside frontier labs（Anthropic） | ✅ 200、217,865 bytes | **重要** | `ai-news-pace-the-frontier-20260912` 的直接續篇 | `research/ai-news-anthropic-pace-metrics-20260917.json` |
| 09-16 08:00 → 09-16 16:00 | Mistral x Mozilla：Firefox Smart Window 換上 Mistral 模型 | ✅ 三頁全 200（243,456／69,671／71,906 bytes） | **次要** | **站上 50 篇沒有任何一篇提過 Mistral**；手法可接 `ai-news-deepseek-v41-flash-20260910` | `research/ai-news-firefox-smart-window-mistral-20260916.json` |
| 09-17 15:56 → 09-17 23:56 | Introducing the Life Sciences Verification Program（Anthropic） | ✅ 200、173,407 bytes | **重要（值得寫）** | 接 `ai-news-anthropic-threat-report-20260910`（同一份威脅報告被它引用） | **未寫**：本輪上限 6 則已滿。題目扎實——為通過驗證的生科團隊放寬生物類安全限制，分 Standard Use 與 High-risk Use 兩種授權、後者只給單一研究專案且半年續約，Mythos 的高風險授權「與美國政府合作中、目前僅限少數經額外審查的機構」。建議下一輪優先補 |
| 09-16 15:00 → 09-16 23:00 | 5 things to know about teens' views on AI today（Google） | ✅ 200、357,825 bytes | 次要 | 無 | **不寫**：受訪者全是**美國**青少年（RXN 執行，逾 1,000 人加六州各 1,000 人），對台灣讀者只能當對照；且是 Google 自己委託的調查，全篇沒有方法論細節可查 |
| 09-16 15:00 → 09-16 23:00 | NVIDIA Vera Rubin NVL72 在 MLPerf Inference v6.1 首度送測 | ✅ 200、118,710 bytes | 次要 | 接 `ai-news-nvidia-rubin-20260105` | **不寫**：整篇是機櫃級吞吐量倍數（3.7x、99% scaling、1.6x），屬硬體效能，照 `ai.md` 的界線**建議轉科技垂直**；倍數全是 NVIDIA 自報且各有不同基準 |
| 09-16 13:00 → 09-16 21:00 | Emerald AI、Google 與 NVIDIA 成立 AI Energy Management Alliance | ✅ 200、110,377 bytes | 次要 | 無 | **不寫**：主題是**美國電網**的併網程序與資料中心用電彈性，對台灣讀者要另外補一整段本地脈絡才成立，這一輪做不到；且無任何量化承諾 |
| 09-16 09:00 → 09-16 17:00 | How workers are unlocking new ways of working（OpenAI 經濟研究） | ✅ 200、406,178 bytes | 次要 | 與 `ai-news-chatgpt-work-20260709` 題材相鄰 | **不寫**：上限已滿。題目可用——分析 2026 年 4–7 月逾 150 萬則工作相關 ChatGPT 訊息，發現跨職務任務會固定下來；但正文把結論掛在一份要另開的 report，本輪沒讀那份 report，不能當來源 |
| 09-17 20:00 → **09-18 04:00** | Making global data easier to explore（UN System Data Commons，Google） | ✅ 200、369,873 bytes | 次要 | 無 | **不寫**：聯合國統計資料整合平台，主體是資料工程與國際組織，AI 只佔「AI-ready knowledge graph」與自然語言查詢兩段，當 AI 新聞份量偏輕 |
| 09-16 12:00 → 09-16 20:00 | How to connect AI usage to business value（OpenAI） | ✅ 200、483,629 bytes | — | 無 | **不寫**：這是 ChatGPT Admin Console 的操作教學，不是新聞事件；全篇截圖標明「All screenshots use illustrative demo data」 |
| 09-16 16:00 → **09-17 00:00** | Helping older adults use AI in everyday life（OpenAI） | ✅ 200、349,657 bytes | — | 無 | **不寫**：美國 10 個城市的**實體工作坊**，台灣讀者無法參與。唯一可用的數字（55 歲以上訊息占比一年內由 6% 升到近 10%）是 OpenAI 自報且限美國 |
| 09-17 12:00 → 09-17 20:00 | How Cooley is accelerating IPO work with ChatGPT（OpenAI） | ✅ 200、382,611 bytes | — | 同一事件 | **不單獨寫**：與 Astra for Law 同日同批，照 A1／A2 前例**列為輔助來源**，已進 `ai-news-astra-for-law-20260917` 的 `sources`。它還推翻了公告的隱含說法——GO Public 是建在 **ChatGPT Work** 上，不是 Astra for Law |
| 09-16 05:00 → 09-16 13:00 | University of Manchester 用 NVIDIA Earth-2 預測英國空污 | 未開原文（feed 給日期與標題） | — | 無 | **不寫**：單一學術機構的應用案例，地域與題材都太窄 |
| 09-17 13:00 → 09-17 21:00 | Aniimo 上架 GeForce NOW（NVIDIA） | 未開原文 | — | 無 | **不寫**：雲端遊戲，非 AI |
| 09-16 14:00 → 09-16 22:00 | Boost your holiday sales with these agentic commerce updates（Google） | 未開原文 | — | 無 | **不寫**：商家行銷導向的購物功能公告，讀者角度薄 |
| 09-16 18:59 → 09-17 02:59 | Microsoft's commitment for AI in education（Microsoft） | 未開原文 | — | 無 | **不寫**：Microsoft 不在指派的管道清單內，順手掃到；內容為教育政策表態，若要寫需另查美國以外的適用範圍 |
| 09-17 14:00 → 09-17 22:00 | What we've learned from Microsoft's own AI transformation | 未開原文 | — | 無 | **不寫**：企業自述型文章，同上 |
| 09-17 19:30 → 09-18 03:30 | Mila 與 Mozilla 的開源 AI 計畫（加拿大政府支持） | 未開原文 | — | 與 Mistral 案同一發布方 | **不寫**：加拿大在地研究計畫 |
| 09-16 | Canadian Start-up smartARM Uses AI to Create Intuitive Bionic Prosthetics（Meta） | 未開原文 | — | 無 | **不寫**：Meta 地區編輯室的客戶故事 |
| 09-16 17:00／17:02／17:03 → 09-17 01:00 起 | Apple Developer 三則（歐盟 App 追蹤透明度、iOS 27 訂閱、beta 版本） | 未開原文 | — | 無 | **不寫**：三則**都不是 AI**；歐盟 ATT 那則屬科技垂直，值得轉過去 |

### 一則邊界項目，交協調者裁定

| 項目 | 事實 | 為什麼放在這裡 |
| --- | --- | --- |
| **Meta One 訂閱服務**（`about.fb.com/news/2026/09/introducing-meta-one-subscription-service-more-features-ai/`） | ✅ 200、713,199 bytes，讀到正文。JSON-LD：`datePublished` **2026-09-15T15:00:59Z**、`dateModified` **2026-09-16T20:22:09Z**。官方摘要寫「more than 50 features launched and 15 million subscriptions and trials to-date」、「The core experience across our apps and Meta AI will stay free」 | **發布日 9/15 落在窗口外，但更新日 9/16 落在窗口內**，指派的收錄規則（`pubDate`／`updated` 其一在 9/16 後）會把它撈進來。事件日應為 **2026-09-15**，正好與站上最新一篇 `ai-news-gemini-38-live-20260915` 同日但不同題目，**沒有任何既有文章寫過**。Meta 在站上只有 `ai-news-meta-muse-spark-20260408` 一篇。要不要補，請協調者決定 |

---

## 統計

- 窗口內**開了原文並讀到 body 的候選：15 則**（OpenAI 7、Google 3、NVIDIA 2、Anthropic 2、Mistral／Mozilla 1），
  另有 1 則邊界項目（Meta One）也讀到正文。
- **寫了研究紀錄：6 則**（重要 5、次要 1），檔案都在 `docs/news-2026-batch-4/research/`。
- **值得寫但因 6 則上限沒寫：2 則** — Anthropic 生命科學驗證方案（建議下一輪第一順位）、OpenAI 工作型態經濟研究。
- **查不到的管道：2 個** — Qwen（現站是 SPA 殼，舊站停在 2025-09-23）、DeepSeek（news 路徑是軟性 404）。兩者都是「沒查到」，**不是「沒發布」**。
- 窗口內**沒有任何一則讀不到正文**：這一輪沒有 `sourcing_verdict: blocked` 的項目。

## 事件日：照 DELTA-4-5 換算台北時間（已處理，不必再決定）

`agents/DELTA-4-5.md` 第 6 條寫明前期研究紀錄的 `event_date` **是換算過台北時間的**，
指派訊息也是這樣要求，所以六份紀錄一律照台北時間。**這與站上 50 篇既有內容包的慣例不同**——
既有包用發布者自己印的日期，`ai-news-gemini-38-live-20260915` 的 feed 時刻是
`Tue, 15 Sep 2026 17:00:00 +0000`（台北已是 9/16 凌晨 1 點），slug 仍是 `20260915`。
差異結果如下，每份紀錄的 `event_date_basis` 都完整寫了 UTC 時刻、換算與「若協調者反悔要改回哪一天」：

| 題目 | 官方頁印的日期 | UTC 時刻 | 台北＝事件日 |
| --- | --- | --- | --- |
| OpenAI 失準通報框架 | September 16, 2026 | 09-16 17:00 GMT | **2026-09-17** |
| Google CC 家庭代理人 | Sep 17, 2026 | 09-17 18:15 UTC | **2026-09-18** |
| OpenAI ChatGPT 廣告 | September 16, 2026 | 09-16 13:00 GMT | 2026-09-16（不變） |
| OpenAI Astra for Law | September 17, 2026 | 09-17 00:00 GMT 為佔位值，不可換算 | 2026-09-17（不變） |
| Anthropic 前沿指標 | 頁面不印日期 | 完全沒有時刻 | 2026-09-17（不變） |
| Mistral × Mozilla | September 16, 2026 | 09-16 08:00 UTC | 2026-09-16（不變） |

同一天（9/16）的兩則 OpenAI 公告因此**落在不同事件日**，這是換算的正常結果，不是錯。
跨日的那兩篇，**正文必須把官方印的日期與台北日期都寫出來**。

## 一件要協調者拍板的事

**OpenAI 失準框架與 Anthropic 指標是否合併成一篇。** 兩件事不同公司、不同公告、相隔一天，
主題同樣是「前沿實驗室對外揭露什麼」，而且**兩邊都沒有提到對方**。
兩份紀錄各自成立、也各自寫了合併時該怎麼分工：若要合併，建議以 OpenAI 那篇為骨幹
（它有六個具體案例），Anthropic 的三項指標收成其中一節。**不要既各寫一篇、又寫一篇合併版。**

## 給撰稿代理的三個補充

- `display_order` 從 **161** 起（現行最大值 160 是 `ai-news-nvidia-hugging-face-20260903`），照 `DELTA-4-5.md` 第 2 條。
- 第一個結尾連結的文字照 `DELTA-4-5.md` 第 3 條逐字抄
  `2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用`；這批索引標題不改。
  六份紀錄的 `overlaps_existing_article` 裡寫的「寫稿時再打開索引內容包確認標題」是保險說法，兩者不衝突。
- 六份紀錄的 `checked_on` 一律 `2026-09-18`，那是**探索階段**的日期；撰稿時要照 `DELTA-4-5.md`
  第 5 條重抓來源，換成自己實際重抓那一天。**其中三頁是活文件，重抓不是形式**：
  `openai.com/index/testing-ads-in-chatgpt/`（堆疊式更新，最新一筆 2026-08-11）、
  `alignment.openai.com/misalignment-reports/`（會新增 Notice 與 Report）、
  `gemini.google/overview/daily-brief/`（沒有日期的推出狀態橫幅）。
