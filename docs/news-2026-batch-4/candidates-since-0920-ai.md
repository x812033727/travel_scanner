# AI 垂直候選：2026-09-20 起（查核日 2026-09-22）

窗口 **2026-09-20 00:00 台北（2026-09-19T16:00Z）起至 2026-09-22T15:33Z**（掃描結束時刻）。
既有 AI 內容包 **60 篇**加一份月份索引與一份來源清單，最新事件日 **2026-09-18**（批次 4.6 的五篇），
`display_order` 最大值 **170**（`ai-news-kimi-k3-bedrock-20260918`），新文章從 **171** 接續。

所有請求都用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，
同一主機間隔 ≥1 秒，**沒有任何請求帶入 email 或任何人的個人資料**。沒有用 WebSearch。

**這一輪的形狀：9/19（五）16:00Z 到 9/21（一）之間是週末，所有指派管道在 9/19 與 9/20 兩天都是零則。
窗口內的東西全部擠在 9/21 與 9/22 兩天。**

---

## 掃過的管道與結果

「拿到 feed 了嗎」一律看兩件事：item／entry 數量，以及最新一筆的日期。狀態碼不算。

| 管道 | 位址 | 結果 | 數量 | 最新一筆 |
| --- | --- | --- | --- | --- |
| OpenAI（feed） | `https://openai.com/news/rss.xml` | ✅ 200、741,570 bytes | 1,215 筆帶 `pubDate` | Mon, 21 Sep 2026 12:00:00 GMT |
| OpenAI（文章頁） | `https://openai.com/index/*` | ✅ **今天不擋**，5 篇全部 200 並讀到正文（356,688–423,673 bytes） | 5/5 | — |
| OpenAI Alignment | `https://alignment.openai.com/misalignment-reports/` | ✅ 200、8,976 bytes，**與上一輪相同**：3 則 Notice ＋ 6 份 Report | 窗口內 0 則 | Notice 最新 2026-09-11（RubyGems） |
| Google（總 feed） | `https://blog.google/rss/` | ✅ 200、29,808 bytes，涵蓋 09-16 05:01Z → 09-22 14:00Z，**沒有被 20 則上限截掉窗口** | 20 items，窗口內 5 則 | Tue, 22 Sep 2026 14:00:00 +0000 |
| Google（AI 分區 feed） | `https://blog.google/innovation-and-ai/rss/` | ✅ 200、32,005 bytes，但只收研究／科學類分區，**最新一筆停在 09-15**，窗口內 0 則 | 20 items | Tue, 15 Sep 2026 16:00:00 +0000 |
| NVIDIA | `https://nvidianews.nvidia.com/releases.xml` | ✅ 200、44,637 bytes | 20 items，窗口內 6 則 | Tue, 22 Sep 2026 12:00:41 GMT |
| Anthropic | `https://www.anthropic.com/news`（無 feed） | ✅ 200、462,323 bytes，RSC JSON 內 240 筆 `publishedOn`，另有 featured grid | **窗口內 0 則** | `publishedOn` 最新 2026-09-18T16:00:00Z（Accenture，已寫） |
| Anthropic Institute | `https://www.anthropic.com/institute` | ⚠️ 200、140,954 bytes，carousel 列出三篇，**整頁與內頁都不印日期** | 3 篇，無法判定是否落在窗口 | 未查到日期（見下方「讀不到／查不到」） |
| Apple Developer | `https://developer.apple.com/news/rss/news.rss` | ✅ 200、427,604 bytes | 146 items，窗口內 0 則 | Fri, 18 Sep 2026 10:00:57 PDT |
| Meta Newsroom | `https://about.fb.com/news/` | ✅ 200、307,920 bytes；**列表頁的 JSON-LD 只有頁面自己的日期**，逐則日期要從卡片 markup 取 | 窗口內 1 則 | September 21, 2026 |
| Microsoft | `https://blogs.microsoft.com/feed/` | ✅ 200、155,504 bytes；再抓首頁 `blogs.microsoft.com`（148,748 bytes）交叉比對，最新一樣是 09-17 | 10 items，窗口內 0 則 | Thu, 17 Sep 2026 14:00:05 GMT |
| Mistral | `https://mistral.ai/news/` | ✅ 200、1,257,494 bytes，無 feed、無 ISO 日期 | 窗口內 0 則 | September 16, 2026（Mozilla 合作案，已寫） |
| Mozilla | `https://blog.mozilla.org/en/feed/` | ✅ 200、150,550 bytes | 20 items，窗口內 1 則（非 AI） | Mon, 21 Sep 2026 17:00:00 +0000 |
| Qwen | `https://qwen.ai/blog` | ❌ 200、94,344 bytes，但**可取出的文字只有 4 個字元**（與上一輪完全一致的殼）。**未查到** | 0 | 未查到 |
| DeepSeek | `https://api-docs.deepseek.com/news/` | ❌ **軟性 404**：回的是「Your First API Call」文件頁（45,814 bytes）。**未查到** | 0 | 未查到 |

### 這一輪踩到或避開的取得陷阱

1. **`openai.com/index/*` 今天完全不擋**，五篇一次到位。與上一輪同樣的結論：被擋要現場重測，不能沿用舊紀錄。
2. **`blog.google/innovation-and-ai/rss/` 不是 AI 總表。** 它的最新一筆停在 09-15，而總 feed
   `blog.google/rss/` 在窗口內明明有 AI 題目。**只掃分區 feed 會整個漏掉這一輪的 Googlebook 與 Jigsaw。**
   總 feed 這次剛好涵蓋 09-16→09-22，沒有被 20 則上限截掉，但這是運氣，下一輪要重新確認 feed 的最舊一筆。
3. **`about.fb.com/news/` 的 JSON-LD 只有一塊**，`datePublished` 是 2019 年（頁面自己的建立日），
   `dateModified` 才是 2026-09-21T18:51:48Z。**逐則日期必須從 `<article>` 卡片的可見日期取**，
   拿 JSON-LD 當逐則日期會全部錯。
4. **Anthropic `/institute/` 的文章沒有日期。** `When AI builds itself`（`/institute/recursive-self-improvement`）
   內頁 243,775 bytes 讀得到全文，但整頁唯一的 2026-09 時間戳是 `siteSettings._updatedAt`（2026-09-18T00:02:35Z），
   **那是網站設定的更新時間，不是文章日期**。`/news` 的 featured grid 這次也沒有收這一篇。
   上一輪靠 featured grid 補到 `/institute/measuring-pace-of-ai-development`（Sep 17），這一輪那招失效。
5. **`blog.google` 的「Read AI-generated summary」照例要跳過。** Googlebook 那篇的摘要寫
   「shipping to select countries beginning October 4」，正文寫的是 **10/4 美國、10/5 加拿大／英國／愛爾蘭／法國／德國／澳洲**，
   摘要沒說哪幾國，直接抄會漏掉「台灣不在名單上」這個對讀者最重要的事實。
6. **兩則 OpenAI 的 `00:00Z` 與五則 `16:00Z` 是佔位時刻**，照 `DELTA-4-5.md` 第 6 條**不換算**，
   事件日維持發布者印的那一天。真正跨日的只有 NVIDIA DSX Ready（18:00Z → 台北 09-22 02:00）
   與 Mozilla 那則（17:00Z → 台北 09-22 01:00），兩者都不是本輪建議寫的題目。

---

## 候選清單

「來源狀態」的 ✅ 表示**開了原文頁並讀到 body**；「未開原文」表示只有 feed／列表給的日期與標題。

| 日期（UTC → 台北＝事件日） | 標題 | 來源狀態 | 建議 | 與既有文章重疊 | 建議 slug／不寫的理由 |
| --- | --- | --- | --- | --- | --- |
| 09-21 12:00 → 09-21 20:00 | Advisory Group on Mathematics and Artificial Intelligence（OpenAI） | ✅ 200、356,688 bytes | **重要** | **站上 60 篇沒有任何一篇提過數學、Navier–Stokes 或這個顧問小組**；可與 `ai-news-pace-the-frontier-20260912` 互相對照 | `ai-news-openai-math-advisory-20260921`（`display_order` 171）。核心事實：8/28 開始訓練的一個**內部未發布模型**，除了 Navier–Stokes 千禧年問題外**已解出 100 題以上長年未解的數學問題**；OpenAI 自己說進展「讓內部數學家吃驚」。回應數學界公開信〈A Severe Misalignment of AI in Mathematics〉，與數學家另組**獨立**顧問小組（掛在 Institute for Advanced Study，成員不支薪、可發表未經 OpenAI 要求的意見、**但不負責建議 OpenAI 放慢內部數學進度**），九位初始成員含 Gowers、Hairer、Witten。背景來源 `https://openai.com/index/navier-stokes-solution`（2026-09-08，**窗口外、站上也沒寫過**）可當第二來源 |
| 09-21 10:00 → 09-21 18:00 | Building standards for the next phase of AI（OpenAI，Global Affairs） | ✅ 200、418,012 bytes | **重要** | 直接續 `ai-news-pace-the-frontier-20260912`（Amodei 的「放慢前沿」）、`ai-news-openai-misalignment-reports-20260917`、`ai-news-anthropic-pace-metrics-20260917`；也引用 `ai-news-nvidia-hugging-face-20260903` 寫過的 Hugging Face 事件 | `ai-news-openai-frontier-standards-20260921`（172）。核心：OpenAI 主張**美國帶頭制定前沿 AI 的國際技術標準**，含遞迴自我改進（RSI）；明說「完全自主的 RSI 今天沒有發生，而且在能安全進行之前不應該做」；提出兩個支柱（借用各國 AI 安全研究所網絡＋CAISI／共同量測與事故通報協定），並指**標準不是license、不是上市前審查**，各國自行決定是否入法；文末提到**美中對話「時機正好」**。**注意分工**：這篇是「要建立什麼制度」，misalignment 那篇是「已經通報了什麼」，pace-the-frontier 是「Anthropic 的主張」，三者不可互相重講 |
| 09-21 13:00 → 09-21 21:00 | Googlebook 開放預購：內建 Gemini 的筆電（Google，同日三篇） | ✅ 兩篇讀到正文（372,293／376,349 bytes），第三篇（外觀設計）未開原文 | **重要（跨垂直，建議協調者裁定歸屬）** | **站上沒有任何一篇提過 Googlebook**，連 2026-05-12 的首度發表（`/platforms/android/meet-googlebook/`，已查證日期）也沒寫過 | `ai-news-googlebook-gemini-laptop-20260921`（173）。對台灣讀者最重要的事實：**首波 10/4 美國、10/5 加拿大／英國／愛爾蘭／法國／德國／澳洲，台灣不在名單內**；899 美元起，Acer／ASUS／Dell／HP／Lenovo 代工，Intel 與 Qualcomm 處理器搭 45 TOPS 以上 NPU，**每台附 12 個月 Google AI Pro（含 5TB 空間）**。AI 功能三件：Magic Pointer（抖游標叫出 Gemini，「只在你要求時才動作」且可關）、Rambler（口述轉結構化文字，支援多語）、Create My Widget。另含 Antigravity 代理開發平台與可跑 Claude Code 的 Linux 終端。**這一則的硬體半邊（機殼、螢幕、pKVM hypervisor、GeForce NOW）屬科技垂直**，若科技代理同時撈到，請指定由誰寫、另一邊只當輔助來源 |
| 09-21 07:00 → 09-21 15:00 | Expanding OpenAI Academy with new learning paths（OpenAI） | ✅ 200、404,956 bytes | 次要 | 與 `ai-news-chatgpt-work-20260709` 相鄰（那篇已提過 Academy） | `ai-news-openai-academy-paths-20260921`（174）。新增四條角色別學習路徑（開發者 Build with AI、主管 Lead AI Adoption、教師 AI for Educators、大學生 AI for College Students），加上既有的 Apply AI at Work；**通過測驗可拿課程徽章**。**動筆前必須先確認台灣是否能註冊與課程語言**——公告全篇沒寫開放地區，這正是這一則被降為次要的原因 |
| 09-22 14:00 → 09-22 22:00 | Using AI to help local governments connect with constituents（Google.org × Jigsaw） | ✅ 200、384,244 bytes | 次要 | 無 | `ai-news-jigsaw-sensemaking-ai-20260922`（175）。Jigsaw 的 Sensemaking AI 工具開放給地方政府免費使用，成立 Partner Program，公告說**全球地方官員都可報名**（若屬實，是這一輪少數台灣可直接用到的東西）。要寫必須先查證：報名是否真的不限國家、工具支援哪些語言。案例是美國 Bowling Green |
| 09-22 12:00 → 09-22 20:00 | NVIDIA Isaac ROS 5.0（ROSCon，多倫多） | ✅ 200、128,675 bytes | 次要 | 無 | `ai-news-nvidia-isaac-ros-5-20260922`（176）。GPU 加速的 ROS 套件，主打「人與 AI 代理一起造機器人」的 agentic workflow，官方稱 ROS 使用者近 130 萬人。**讀者面窄（機器人開發者），照 `ai.md` 的界線建議轉科技垂直**；若 AI 要寫，角度只能是「代理式開發進到機器人領域」 |
| 09-21 16:00（**佔位時刻，不換算**）→ 09-21 | Why Deploying Physical AI at Scale Demands Safety at Every Layer（NVIDIA HALOS） | ✅ 200、121,712 bytes | 次要 | 可與 `ai-news-openai-frontier-standards-20260921` 的「標準」主題對照 | `ai-news-nvidia-physical-ai-safety-20260921`（177）。實體 AI 的分層安全論述，引用 ABI Research（2035 年 4,900 萬台 L3–L5 自駕車）與 Omdia（2026–2035 年約 6,000 萬台工業機器人）兩份**第三方預測**。**不寫的理由若成立就是這個**：全篇的量化數字都是外部預測機構的，NVIDIA 自己沒有給可查證的承諾 |
| 09-21 00:00（**佔位時刻**）→ 09-21 | How V7 gives AI agents institutional memory（OpenAI） | ✅ 200、423,673 bytes | — | 無 | **不寫**：客戶案例（V7 Go 用 GPT-5.6 Luna 做 Context Graph），全篇是單一 B2B 廠商的產品介紹，沒有 OpenAI 自己的新事實 |
| 09-21 12:00 → 09-21 20:00 | Higgsfield AI ships new video features in a day with GPT-6 Astra（OpenAI） | ✅ 200、380,396 bytes | — | 無 | **不寫**：客戶案例，唯一的「數字」是創辦人受訪說一天內一個工程師就做完新功能，無法查證 |
| 09-21 16:00（**佔位時刻**）→ 09-21 | Expanding free AI training for educators（Google.org × Digital Promise） | ✅ 200、355,688 bytes | — | 無 | **不寫**：400 萬美元捐給 Digital Promise，對象寫死是**美國 600 萬名 K-12 與高教教師**，台灣讀者參與不到。發布場合是聯合國大會周邊活動，這點也不足以撐起一篇 |
| 09-21 13:00 → 09-21 21:00 | Premium materials and striking design set Googlebook apart（Google） | 未開原文 | — | 同一事件 | **不單獨寫**：與上面 Googlebook 那則同日同批，照 A1／A2 前例列為**輔助來源**，寫進 `ai-news-googlebook-gemini-laptop-20260921` 的 `sources` |
| 09-21 18:00 → **09-22 02:00（跨日）** | NVIDIA Launches DSX Ready（AI 工廠電力與散熱認證） | ✅ 200、109,776 bytes | — | 無 | **不寫**：資料中心供應鏈的零組件認證方案（儲能與冷卻分配單元兩類），完全是 B2B 基礎建設，照 `ai.md` 建議轉科技垂直。**官方頁印 September 21，台北是 9/22，兩個日期不同** |
| 09-21 14:51 → 09-21 22:51 | AI Security Is an Engineering Problem（NVIDIA） | 未開原文 | — | 無 | **不寫**：代理堆疊的資安工程觀念文，不是新聞事件 |
| 09-21 16:00（**佔位時刻**）→ 09-21 | From Enablement to Execution, Egypt's AI Ecosystem Reaches Production Scale（NVIDIA） | 未開原文 | — | 無 | **不寫**：單一國家的生態系宣傳稿 |
| 09-21 10:00 → 09-21 18:00 | 5 Companies Using NVIDIA AI for Clean Energy（NVIDIA） | 未開原文 | — | 無 | **不寫**：客戶案例合輯 |
| 09-21（Meta 新聞室印的日期） | Announcing Petal, a First-of-its-Kind Transoceanic Subsea Cable（Meta） | 未開原文 | — | 與 `tech-news-taiwan-matsu-cable-20260623`、`tech-news-taiwan-matsu-cable-tm4-20260918` 同題材（海纜） | **不寫（建議轉科技垂直）**：跨洋海纜的容量突破，AI 只出現在「為什麼需要這麼大頻寬」的動機段。科技垂直已經有兩篇海纜文章，這一則接得上 |
| 09-21 17:00 → **09-22 01:00（跨日）** | Stay focused wherever you work with Firefox mobile browsers（Mozilla） | 未開原文 | — | 無 | **不寫**：**整則 feed entry 裡「AI」出現 0 次**，是手機瀏覽器的專注模式功能，非 AI |

---

## 上一輪留下、窗口外

以下是 `candidates-since-0916-ai.md` 列過、但到 2026-09-22 為止**內容包裡仍然沒有**的項目
（逐一用 slug／來源網址比對過 `apps/api/app/guides/content/*.json`，不是憑印象）。

| 事件日 | 題目 | 上一輪為什麼留著 | 現在的狀態 |
| --- | --- | --- | --- |
| 2026-09-17 | **Introducing the Life Sciences Verification Program（Anthropic）** | 上一輪自己寫「本輪上限 6 則已滿…**建議下一輪優先補**」 | **仍然沒寫**，而且 4.6 那一輪也沒補。這是碳留最久、上一輪評為「重要（值得寫）」的唯一一則。題目：為通過驗證的生科團隊放寬生物類安全限制，分 Standard Use 與 High-risk Use，後者只給單一研究專案、半年續約。**建議 4.7 第一順位吸收** |
| 2026-09-16 | How workers are unlocking new ways of working（OpenAI 經濟研究） | 上限已滿；且結論掛在一份上一輪沒讀的 report | 仍然沒寫。要吸收就必須把那份 report 讀完，否則不能當來源 |
| 2026-09-15（`dateModified` 09-16） | **Meta One 訂閱服務** | 上一輪明確標為「邊界項目，交協調者裁定」，**當時沒有裁定** | 仍然沒寫。發布日落在窗口外、更新日落在窗口內；站上 Meta 只有 `ai-news-meta-muse-spark-20260408` 一篇。**這個裁定到今天還欠著** |
| 2026-09-16 | 5 things to know about teens' views on AI today（Google） | 上一輪判 **不寫**（受訪者全是美國青少年、Google 自己委託、無方法論） | 理由未變，建議維持不寫 |
| 2026-09-16 | NVIDIA Vera Rubin NVL72 在 MLPerf Inference v6.1 | 上一輪判 **不寫**，建議轉科技垂直 | 理由未變 |
| 2026-09-16 | Emerald AI／Google／NVIDIA 的 AI Energy Management Alliance | 上一輪判 **不寫**（美國電網、無量化承諾） | 理由未變 |
| 2026-09-17 | Making global data easier to explore（UN System Data Commons） | 上一輪判 **不寫**（AI 份量偏輕） | 理由未變 |
| 2026-09-16／09-17 | OpenAI 三則（business value 教學、helping older adults、Cooley） | 分別是教學文、美國實體工作坊、已併入 Astra for Law 的 `sources` | 理由未變 |

### 另外三個縫隙：9/18 之後、9/19 16:00Z 之前

上一輪的查核日是 **2026-09-18**，它的清單收到 09-18 04:00 台北為止；本輪窗口從 **09-19 16:00Z** 起。
中間這段有三則 Google AI 題目**兩份清單都沒收過，內容包裡也沒有**，列在這裡供站主一併決定：

| UTC | 題目 | 網址 |
| --- | --- | --- |
| 09-18 13:00 | Co-creating the future of fashion with Google（Flow × 時裝周） | `https://blog.google/innovation-and-ai/technology/ai/google-flow-fashion-week/` |
| 09-18 14:00 | New experts join Google's AI & Economy team | `https://blog.google/innovation-and-ai/technology/ai/expanding-ai-economy-research-bench/` |
| 09-18 16:00 | Earn continuing education and college credits for AI educator training | `https://blog.google/products-and-platforms/products/education/college-credit-ai-educator-series/` |

同一段縫隙還有兩篇 **Anthropic Institute** 文章（`When AI builds itself`／`Scenarios for our Economic Future`），
站上都沒寫過，但**兩篇都查不到日期**，細節見下一節。

---

## 讀不到／查不到

| 對象 | 實際發生什麼 | 這代表什麼 |
| --- | --- | --- |
| **Qwen** | `https://qwen.ai/blog` 回 200、94,344 bytes，但可取出的純文字只有 **4 個字元**，是純 SPA 殼 | **未查到**，不是「沒發布」。與上一輪同樣的殼，狀況沒有改善 |
| **DeepSeek** | `https://api-docs.deepseek.com/news/` 回 200、45,814 bytes，但內容是「Your First API Call」文件頁 = **軟性 404** | **未查到**，不是「沒發布」 |
| **Anthropic Institute 的兩篇** | `/institute/recursive-self-improvement`（`When AI builds itself`，內頁 243,775 bytes，全文讀得到）與 `/institute/econ-scenarios`（`Scenarios for our Economic Future`）**都不印日期**；`/institute` carousel 不印、`/news` 的 featured grid 這次沒收、`publishedOn` 清單裡也沒有 | **無法判定是否落在窗口**。唯一的 2026-09 時間戳是 `siteSettings._updatedAt`，那是站台設定的更新時間，**不能當文章日期**。兩篇站上都沒寫過，若站主要收，必須另外找官方出處（例如公司社群貼文）把日期釘死，否則 `event_date` 沒有依據 |
| **NCC／其他主管機關** | 本輪沒有 AI 監理題目進入窗口，未觸發 | — |

窗口內**沒有任何一則讀得到日期卻讀不到正文**：這一輪沒有 `sourcing_verdict: blocked` 的項目。

---

## 統計

- 窗口內（2026-09-19T16:00Z → 2026-09-22T15:33Z）**掃到 17 則**，其中**開了原文並讀到 body：11 則**
  （OpenAI 5、Google 3、NVIDIA 3），另 6 則只有 feed／列表資訊。
- 建議分類：**重要 3 則**（OpenAI 數學顧問小組、OpenAI 國際標準主張、Googlebook 開賣）、
  **次要 4 則**（OpenAI Academy、Jigsaw Sensemaking、NVIDIA Isaac ROS 5.0、NVIDIA 實體 AI 安全）、
  **不寫 10 則**（客戶案例 3、美國限定 1、同事件輔助來源 1、B2B 基礎建設 3、非 AI 1、轉科技垂直 1）。
- **與既有文章重複：0 則。** 逐一用官方網址與關鍵字比對過全部 62 份 `ai-news-*.json`，
  Googlebook、Navier–Stokes、OpenAI Academy、數學顧問小組、國際標準、Sensemaking、Isaac ROS、
  HALOS、Petal **在站上都是第一次出現**。沒有任何一則要走「不寫（重複）」或「不寫（改維護票）」。
- **零產出的管道：6 個**（Anthropic `/news`、Apple Developer、Microsoft、Mistral、
  `blog.google/innovation-and-ai/rss/`、OpenAI Alignment）——都是**讀到了但窗口內沒有新東西**，與「讀不到」不同。
- **查不到的管道：2 個**（Qwen、DeepSeek），**日期查不到的文章：2 篇**（Anthropic Institute）。
- `display_order` 從 **171** 起（現行最大值 170 是 `ai-news-kimi-k3-bedrock-20260918`）。
- 掃描結束時刻（＝窗口結束）：**2026-09-22T15:33:25Z**（台北 2026-09-22 23:33）。

## 兩件要協調者拍板的事

1. **Googlebook 歸 AI 還是科技。** 這一則同時是「AI PC」與「筆電上市」，科技垂直的代理幾乎一定也會撈到。
   **不要兩邊各寫一篇。** 建議：AI 寫 Gemini 三功能與 12 個月 AI Pro 綁約、科技寫硬體與上市節奏，
   另一邊只列為 `sources`；或直接指定一邊寫完整篇。
2. **Meta One 的裁定從上一輪欠到現在。** 上一輪把它標為邊界項目送交裁定就沒有下文了，
   今天它既不在任何內容包裡，也不在任何待辦票裡。請在 4.7 一併決定收或不收。
