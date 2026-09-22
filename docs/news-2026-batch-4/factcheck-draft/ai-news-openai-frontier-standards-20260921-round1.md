# ai-news-openai-frontier-standards-20260921 查核報告（第一輪）

- 查核者：獨立查核代理（第一輪），沒有參與撰稿
- 查核日：2026-09-23（與內容包四條 `sources[].checked_on`、研究紀錄 `checked_on` 一致）
- 內容包：`apps/api/app/guides/content/ai-news-openai-frontier-standards-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-frontier-standards-20260921.json`
- 事件日 2026-09-21、`display_order` 172、`topics` = ai／ai-news（無 finance）
- **主張 109 條｜CONFIRMED 85｜CHANGED 22｜NOT FOUND 0｜OUT OF SCOPE 2｜實際文字修改 18 處**
- 結論：**needs_second_round**（第二輪本來就是 DELTA-4-7 第 12 條的硬規定；本輪改了 22 條事實主張）

---

## 1. 來源重抓結果（2026-09-23 台北 01:08，同一主機間隔 ≥2 秒）

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`；
UA、標頭、查詢字串、暫存檔名都沒有任何人的姓名或 email。

| # | URL | HTTP | bytes（本輪／研究紀錄） | 讀到正文？ |
| --- | --- | --- | --- | --- |
| 1 | `https://openai.com/index/building-standards-next-phase-ai/` | 200 | 418,047／418,012 | 是。抽取後正文 13,601 字元，五個小節齊全（RSI／International standards／(1) A mechanism…／(2) Common measurements…／The United States should lead）。本輪**沒有**遇到 `openai.com/index/*` 的 403 |
| 2 | `https://openai.com/news/rss.xml` | 200 | 741,570／741,570 | 是。1,215 個 item；本篇那一則 `link` = `…/building-standards-next-phase-ai`、`pubDate` = `Mon, 21 Sep 2026 10:00:00 GMT`、`category` = Global Affairs |
| 3 | `https://www.nist.gov/…/international-network-advanced-ai-measurement-evaluation-and-science` | 200 | 85,197／85,196 | 是。頁面自印 `February 13, 2026` 與 `Released February 13, 2026`，五段正文全讀到 |
| 4 | `https://openai.com/index/research-acceleration-view-inside-openai/` | 200 | 2,315,095／2,314,636 | 是（文字段落）。頁面自印 `September 6, 2026`；頁內圖表仍由前端載入、數字讀不到，與研究紀錄的 `live_data_warnings` 相同 |

bytes 的小幅差異是 Next.js build id 之類的快取字串，不是內容變動。

引文比對方式與研究代理相同（原始 HTML 去掉 `<!-- -->` 後 `html.unescape`，再做連續字串比對）：
**`sources[]` 四條與 `verified_facts` 51 條的 `verbatim_quote` 今天全部命中，0 個 MISS。**

另外四個機械檢查：

1. 關鍵字全文掃描（四份 body）：`Taiwan` 只在 RSS 命中 1 次、`Taipei`／`台灣` 0 次、`European Union` 只在 NIST 命中 1 次（成員清單）、`AI Act` 在 NIST 的命中是 `AI Action Plan` 的子字串、`binding`／`treaty` 四份皆 0。
2. 公告內所有超連結的 href 與錨文字對照：`Our recent report` → `/index/research-acceleration-view-inside-openai/`（確認報告的身分）；`Global Affairs` → `/news/global-affairs/`；`ISO` → `iso.org/committee/6794475.html`；`Agentic AI Foundation` → `aaif.io`；`Open Secure AI Alliance` → NVIDIA blog；`Appia Foundation` → `/index/helping-build-shared-standards-for-advanced-ai/`。
3. 兩個結尾連結的 text 與目標內容包 zh-TW `title` 的逐字比對：兩條都完全相同（見第 4 節）。
4. 「本文」字樣 0 次；「官方」2 次（都是來源名「OpenAI 官方新聞頻道 RSS」）。

---

## 2. 主張逐條對照（109 條）

判定：C = CONFIRMED、**X = CHANGED**、N = NOT FOUND、S = OUT OF SCOPE（風格，未改）。
來源代號：**A** = OpenAI 公告、**N** = NIST 頁、**R** = 研究加速報告、**F** = OpenAI 新聞 RSS。

### 2.1 中繼資料與來源（1–4）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 1 | slug 後綴 `20260921` = `news_date` 2026-09-21 = 第一段「2026 年 9 月 21 日」三者一致 | A／F | C |
| 2 | `display_order` 172 | DELTA-4-7 §5 | C |
| 3 | `topics` = ai／ai-news，沒有 finance、沒有投資免責 callout（`ai.md`） | — | C |
| 4 | 四條 `sources[].checked_on` 全為 2026-09-23，與研究紀錄 `checked_on` 一致，且今天四條都重抓成功 | — | C |

### 2.2 標題與 description（5–9）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 5 | title「OpenAI 主張美國帶頭訂前沿 AI 國際標準：兩個支柱與一條界線」（34 字，與研究紀錄 `title` 相同） | A | C |
| 6 | description 前半「2026 年 9 月 21 日，OpenAI 發表文章，主張由美國帶頭、與各國合作制定前沿 AI 的全球技術標準，範圍涵蓋 RSI」 | A | C |
| 7 | description「文章提出**讓國家標準互補**、共同量測與事故通報協定兩個支柱」 | A | **X** |
| 8 | description「標準不是許可證、不是上市前審查，各國自行決定要不要入法」 | A | C |
| 9 | description 句尾只帶「（2026 年 9 月查證）」、沒有查證流水帳；title／description／summary 沒有挑選篇數 | DELTA-4-7 §14 | C |

### 2.3 開頭兩段（10–20）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 10 | 2026 年 9 月 21 日發表 | A（`September 21, 2026`） | C |
| 11 | 在官網 **Global Affairs 分類**發表 | A（標籤連到 `/news/global-affairs/`）／F（`category`） | C |
| 12 | 篇名〈Building standards for the next phase of AI〉 | A | C |
| 13 | 主張由美國帶頭、與世界各國合作制定前沿 AI 的全球技術標準，範圍包含 RSI | A（`the United States should lead an effort … including for RSI`） | C |
| 14 | 支柱一＝「讓**各國既有的 AI 安全研究所網絡**與國際標準互補」 | A | **X** |
| 15 | 支柱二＝建立共同量測與事故通報協定 | A | C |
| 16 | 「不是許可證、不是強制上市前審查，也不是模型核准要求」 | A | C |
| 17 | 「各國政府自行決定要不要、以及如何把它們納入自己的法律體系」 | A | C |
| 18 | 「這一篇的資料在 2026 年 9 月 23 日查核」（查核日在前兩段，符合 checker） | — | C |
| 19 | 第二段列舉的四份東西＝內容包的四條 `sources[]` | — | C |
| 20 | 「以下**規格**與主張，一律標明是 OpenAI 自己的說法」——這篇沒有任何規格 | — | S |

### 2.4 summary 五句（21–26）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 21 | 第一句＝第一段的事實（日期、篇名、主張、含 RSI） | A | C |
| 22 | 第二句的支柱一敘述（同 #14） | A | **X** |
| 23 | 第二句「用來管理自動化 AI 研究與 RSI 的**風險**」 | A | **X** |
| 24 | 第三句「兩份名單都沒有出現台灣」（限於 OpenAI 十國與 NIST 十個成員兩份清單） | A／N | C |
| 25 | 第四句的界線 | A | C |
| 26 | 第五句「沒有時程、主辦機構或法律效力」＋「預期會隨時間大幅演變」 | A | C |

### 2.5 第一節「OpenAI 主張什麼，為什麼把 RSI 放在最前面」（27–37）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 27 | RSI 定義：AI 系統承擔越多開發下一代 AI 的工作，就越可能推動遞迴自我改進，即使人仍然參與其中 | A | C |
| 28 | 「美國要帶頭合作的技術標準，範圍**必須**包含 RSI 在內」 | A | **X** |
| 29 | 「人類可能失去對 AI 開發的實質控制」 | A | C |
| 30 | 「超出集體理解進展、評估風險與維持**有效監督**的能力」 | A | **X** |
| 31 | 英文引句 `Fully autonomous RSI is not happening today, and we should not pursue it unless and until it can be done safely.` 逐字 | A | C |
| 32 | 其中文括號譯文 | A | C |
| 33 | 「對**放慢前沿發展**的重要性可能不亞於對齊研究本身」 | A | **X** |
| 34 | 「能建立高品質證據的共同定義，以及技術防護嚴謹程度的共同基準」 | A | C |
| 35 | 「文中列出三個需要國際合作才解得開的問題」 | A | C |
| 36 | 「對開放模型與封閉模型都適用」 | A | C |
| 37 | 三個問題的內容（互相衝突／各自行動產生沒有一國想要的結果／專業分布不均） | A | C（第一項壓掉了 incident definitions，見第 5 節） |

### 2.6 第二節「支柱一」（38–49）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 38 | 「支柱一**要借用的，是**各國正在成形的 AI 安全研究所網絡」——原文是 One way of accomplishing this would be | A | **X** |
| 39 | 「OpenAI 點名十個已經成立這類機構的國家」——原文 such as，是舉例 | A | **X** |
| 40 | 「與 CAISI 及各國產業機構**合作**」——原文是 to facilitate standard setting **through** the CAISI and national industry bodies | A | **X** |
| 41 | CAISI 譯名「AI 標準與創新中心」 | N（Center for AI Standards and Innovation） | C |
| 42 | 兩個聚焦面向：以能力基準衡量的前沿 AI 模型與開發者／自動化 AI 研究（含 RSI）的利益與風險管理 | A | C |
| 43 | 「美國可以接著 CAISI 創立的『國際先進 AI 量測、評估與科學網絡』往下做」 | A | C |
| 44 | NIST 頁證實網絡存在、2024 年 11 月由 CAISI 創立、聚焦強化支撐 AI 評估的科學 | N | C |
| 45 | 「2025 年 6 月由美國商務部長 Howard Lutnick 交付任務」的**對象被寫成那個網絡** | N | **X** |
| 46 | 任務內容：發展指引與最佳實務、量測並提升 AI 系統的資安、協助產業發展自願性標準 | N | C |
| 47 | NIST 頁自印 2026 年 2 月 13 日 | N | C |
| 48 | 兩份名單不是同一份、都沒有出現台灣 | A／N | C |
| 49 | 「能力量測與評估、風險評估、防護是否足夠的共同技術基礎」 | A | C |

### 2.7 表格（50–59）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 50 | 表頭四欄（清單／出處與日期／名單內容／台灣），3 列 | — | C |
| 51 | 第一列十國與順序：澳洲、加拿大、德國、法國、肯亞、日本、韓國、新加坡、印度、英國 | A | C |
| 52 | 第一列欄名「已成立的 AI 安全研究所」（未標示是舉例） | A | **X** |
| 53 | 第一列「台灣：未見」 | A | C |
| 54 | 第二列十國與順序：澳洲、加拿大、歐盟、法國、日本、肯亞、大韓民國、新加坡、英國、美國 | N | C |
| 55 | 第二列出處日期 2026-02-13 | N | C |
| 56 | 第二列「台灣：未見」 | N | C |
| 57 | 第三列欄名「公告**點名的標準組織**」（原文是 should also work closely with） | A | **X** |
| 58 | 第三列名單把 **Appia Foundation** 併入標準組織 | A | **X** |
| 59 | caption「兩份清單不是同一份……這一篇的資料在 2026 年 9 月 23 日查核」 | — | C |

### 2.8 第三節「支柱二」（60–68）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 60 | 「支柱二在管理 AI 研究自主程度與 RSI 上尤其關鍵」（漏 increasing） | A | **X** |
| 61 | 三個標準方向逐項（RSI 相關進展與公司內自動研究量／人類監督與立刻觸發人工檢視／事故分類追蹤通報回應與嚴重程度分級、通報門檻） | A | C |
| 62 | 「這三個方向，OpenAI 目前**各**放上桌一份自己的文件」 | A | **X** |
| 63 | 研究加速報告：2026 年 9 月 6 日、《Research acceleration: The view inside OpenAI》 | R | C |
| 64 | 「那份報告寫明目的之一就是推動整個領域走向共同的量測標準」 | R | C |
| 65 | 「第一個方向的**早期**貢獻」——原文 an initial contribution | A | **X** |
| 66 | 「第三個方向的早期貢獻則是失準通報框架」（an early contribution），只帶一句、不展開 | A | C |
| 67 | 關鍵基礎設施營運者與各國政府應建立安全溝通管道，分享國安疑慮、新出現的弱點與威脅、前沿 AI 安全最佳實務 | A | C |
| 68 | 美中對話「會是正面的一步、即將到來的會談時機正好」，且沒有日期、層級或與會者 | A | C |

### 2.9 圖解（69–70）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 69 | `image.alt` 的四格＝研究紀錄 `diagram.nodes`（起點／支柱一／支柱二／界線） | — | C |
| 70 | `image.caption` 與研究紀錄 `diagram.caption` 逐字相同 | — | C |

### 2.10 第四節「這套標準『不是』什麼」（71–78）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 71 | 英文引句 `These technical standards would not be licenses, mandatory prerelease review, or approval requirements for AI models.` 逐字 | A | C |
| 72 | 其中文括號譯文，以及「是否、以及如何納入自己的法律體系，仍由各國政府自行決定」 | A | C |
| 73 | 制定過程要諮詢開放／封閉模型開發者、獨立技術專家與學界，以支持有競爭力的 AI 生態系 | A | C |
| 74 | 透明制定、不得圖利特定公司／國家／商業模式、不得讓新進者或開放權重開發者更難競爭 | A | C |
| 75 | 讓實驗室以外的更多利害關係人有發言權、提供不必依賴任何單一實驗室作法的公開原則 | A | C |
| 76 | 航空與金融穩定的類比：共同技術標準與可信賴的合作管道，同時沒有放棄國家主管權 | A | C |
| 77 | 點名 ISO、Frontier Model Forum、Agentic AI Foundation 與 Open Secure AI Alliance，措辭是「應該……密切合作」 | A | C |
| 78 | Appia Foundation「正在發展把國際標準接上真實世界 AI 評估的實務規格」 | A | C |

### 2.11 第五節「還沒有的東西」（79–88）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 79 | 沒有時程（何時開始談、何時有第一版文本） | A | C |
| 80 | 沒有指定主辦機構 | A | C |
| 81 | 沒有寫是否具拘束力、不遵守會怎樣（`binding`／`treaty` 全篇 0 次） | A | C |
| 82 | 沒有給前沿 AI 模型的門檻數字 | A | C |
| 83 | 「以**這四條來源**查核……未見台灣」 | F | **X** |
| 84 | 「也未見歐盟《人工智慧法》字樣」（範圍） | F | **X** |
| 85 | 「OpenAI……自己**主張的「放慢腳步」**（pacing）不是維持預定速度」 | A | **X** |
| 86 | 美國適合帶頭的理由：AI 產業站在技術前沿、在金融／貿易／國防／科技／資訊系統具全球網絡位置優勢 | A | C |
| 87 | 不帶頭「可能眼看分裂、不均、充滿衝突的體系在自己周圍成形」 | A | C |
| 88 | 「要追後續，可以直接看 openai.com 的 Global Affairs 分類，或 NIST／CAISI 的網頁」 | A（分類頁確實存在於 `/news/global-affairs/`） | C |

### 2.12 FAQ（89–95）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 89 | Q1：沒有拍板；預期大幅演變、沒有啟動時間、沒有主辦機構、是主張不是制度 | A | C |
| 90 | Q2：正好相反——不是許可證／強制上市前審查／核准要求；公告沒寫任何一國已經要這麼做 | A | C |
| 91 | Q3：完全自主的 RSI 今天沒有發生，以及 RSI 定義 | A | C |
| 92 | Q4：OpenAI 十國含德國與印度、沒有歐盟與美國；NIST 十個成員含歐盟與美國、沒有德國與印度 | A／N | C |
| 93 | Q5 第一句「以**這幾條來源**查核……未見台灣」 | F | **X** |
| 94 | Q5 第二句：公告、NIST 網頁、研究加速報告都沒有出現台灣或台北字樣 | A／N／R | C |
| 95 | 五題答案都是純文字、沒有連結 | — | C |

### 2.13 callout 與結尾連結（96–102）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 96 | 「這是 OpenAI 一家公司在 2026 年 9 月 21 日提出的主張」 | A | C |
| 97 | 「OpenAI 自己寫，預期這個構想會隨時間大幅演變」 | A | C |
| 98 | 「公告沒有寫時程、主辦機構或法律效力」 | A | C |
| 99 | 「也沒有提到台灣，這幾點都是以**四條來源**查核……」 | F | **X** |
| 100 | 「文中的**規格**與主張都是 OpenAI 自己的說法」 | — | S |
| 101 | 第一個連結 text =`2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用`，與 `ai-news-2026-january-september-index` 的 zh-TW title 逐字相同 | — | C |
| 102 | 第二個連結 text =`OpenAI 公布失準通報框架：6 份報告都出自訓練階段`，與 `ai-news-openai-misalignment-reports-20260917` 的 zh-TW title 逐字相同 | — | C |

### 2.14 sources 與讀者優先（103–109）

| # | 主張 | 來源 | 判定 |
| --- | --- | --- | --- |
| 103 | source 1 標題／網址／checked_on | A | C |
| 104 | source 2「OpenAI 官方新聞頻道 RSS（本篇 item 的 pubDate 紀錄）」 | F | C |
| 105 | source 3 NIST 標題與網址（與頁面 `<title>` 相同） | N | C |
| 106 | source 4「Research acceleration: The view inside OpenAI（公告點名的第一份貢獻）」 | R | C |
| 107 | 全篇沒有「本文」 | DELTA-4-7 §14 | C |
| 108 | 「官方」只出現 2 次，且都是來源名稱 | DELTA-4-7 §14 | C |
| 109 | 沒有購買建議、沒有推薦式比價、沒有未歸因的廠商宣稱（全篇主張句都掛在 OpenAI 身上，NIST 那三條標明是 NIST 頁面） | `ai.md` | C |

---

## 3. 改掉的 22 條主張（18 處文字，逐處 before → after）

以下每一處都附原文與理由。所有修改都用「一次只命中一次」的字串取代寫回內容包，沒有用 `json.dump`。

### 3.1 支柱一被寫成「AI 安全研究所網絡與國際標準互補」（#7、#14、#22，三處）

- before：`一是讓各國既有的 AI 安全研究所網絡與國際標準互補`（第一段與 summary 第二句）／
  `文章提出讓國家標準互補、共同量測與事故通報協定兩個支柱`（description）
- after：`一是建立讓國家標準與國際標準互補的機制`／
  `文章提出兩個支柱：讓國家標準與國際標準互補的機制，以及共同量測與事故通報協定`
- 原文：`(1) A mechanism that facilitates complementary national and international frontier standards`；
  網絡那段是 `One way of accomplishing this would be to leverage the emerging network of AI safety institutes`
- 理由：互補的是「國家標準」與「國際標準」，AI 安全研究所網絡只是達成手段之一；而且原文寫 **emerging**（正在成形），不是「既有的」。第二節小標本來就寫對，這三處與它自相矛盾。
- 來源：`https://openai.com/index/building-standards-next-phase-ai/`

### 3.2 支柱二被寫成「管理……的風險」（#23）

- before：`用來管理自動化 AI 研究與 RSI 的風險`
- after：`用來管理 AI 研究日益增加的自主程度與 RSI`
- 原文：`International AI standards will be particularly crucial in managing increasing autonomy in AI research and recursive self-improvement.`
- 理由：`benefit-risk management` 是支柱一第二個聚焦點的字眼，不是支柱二的。
- 來源：同上

### 3.3 「範圍必須包含 RSI」（#28）

- before：`範圍必須包含 RSI 在內` → after：`範圍包含 RSI 在內`
- 原文：`global technical standards for frontier AI, including for RSI` —— 是範圍，不是義務。
- 來源：同上

### 3.4 `meaningful human oversight` 被寫成「有效監督」（#30）

- before：`維持有效監督的能力` → after：`維持有意義人類監督的能力`
- 原文：`potentially beyond our collective ability to understand progress, assess risks, and maintain meaningful human oversight`
- 來源：同上

### 3.5 `pacing the frontier` 被譯成「放慢」（#33、#85，兩處）

- before：`對放慢前沿發展的重要性可能不亞於對齊研究本身`／`OpenAI 解釋，自己主張的「放慢腳步」（pacing）不是維持預定速度`
- after：`對調節前沿發展步調的重要性可能不亞於對齊研究本身`／`OpenAI 解釋，自己說的「調節步調」（pacing）不是維持預定速度`
- 原文：`International standards … may be as important to pacing the frontier as alignment research itself.`＋`Pacing AI development is not about maintaining a predetermined speed.`
- 理由：同一篇自己否定「速度」這個框架，譯成「放慢」與原文互相矛盾，也會把 `ai-news-pace-the-frontier-20260912`（Anthropic／Amodei）的主張安到 OpenAI 頭上——研究紀錄 `must_not_write` 第 2 條正是禁止這種混淆。
- 來源：同上

### 3.6 支柱一段落一次掉了三個限定詞（#38、#39、#40）

- before：`支柱一要借用的，是各國正在成形的 AI 安全研究所網絡：OpenAI 點名十個已經成立這類機構的國家（詳見下表），主張透過這個網絡，與 CAISI（AI 標準與創新中心）及各國產業機構合作，讓國家標準與國際標準互補。`
- after：`支柱一要怎麼做，OpenAI 只寫了其中一種做法：借用各國正在成形的 AI 安全研究所網絡，並舉例點名十個已經成立這類機構的國家（詳見下表），再透過 CAISI（AI 標準與創新中心）與各國產業機構促成標準制定，讓國家標準與國際標準互補。`
- 原文：`One way of accomplishing this would be to leverage the emerging network of AI safety institutes—such as those already established in Australia, Canada, Germany, France, Kenya, Japan, Korea, Singapore, India, and the United Kingdom—to facilitate standard setting through the CAISI and national industry bodies`
- 理由：`One way`（其中一種）、`such as`（舉例）兩個限定詞被刪掉；而且是「**透過** CAISI 與各國產業機構促成標準制定」，不是「**與** CAISI 合作」。
- 來源：同上

### 3.7 Lutnick 交付任務的對象被寫成國際網絡（#45）

- before：`……聚焦強化支撐 AI 評估的科學，2025 年 6 月由美國商務部長 Howard Lutnick 交付任務：發展量測與提升 AI 系統安全的指引與最佳實務，並協助產業發展自願性標準。`
- after：`……聚焦強化支撐 AI 評估的科學；CAISI 設在 NIST 之內，2025 年 6 月由美國商務部長 Howard Lutnick 交付任務，發展指引與最佳實務以量測並提升 AI 系統的資安，並協助產業發展自願性標準。`
- 原文：`In June 2025, Secretary of Commerce Howard Lutnick charged the Center for AI Standards and Innovation (CAISI) within NIST with developing guidelines and best practices to measure and improve the security of AI systems and assist industry to develop voluntary standards.`
- 理由：被交付任務的是 **CAISI**，不是國際網絡；受詞是 `the security of AI systems`（資安）。原句連著上一個子句讀，主詞會變成那個網絡。
- 來源：`https://www.nist.gov/news-events/news/2026/02/international-network-advanced-ai-measurement-evaluation-and-science`

### 3.8 表格第一列沒標示是舉例（#52）

- before：`已成立的 AI 安全研究所` → after：`已成立的 AI 安全研究所（舉例）`
- 理由：欄名是「清單」，而原文是 `such as those already established in …`；不加註會被讀成「全世界就這十國有」。
- 來源：OpenAI 公告

### 3.9 表格第三列把 Appia Foundation 併進標準組織（#57、#58）

- before：`公告點名的標準組織` ／ `ISO、Frontier Model Forum、Agentic AI Foundation、Open Secure AI Alliance、Appia Foundation`
- after：`公告主張要合作的組織` ／ `標準組織 ISO、Frontier Model Forum、Agentic AI Foundation、Open Secure AI Alliance；實作機構 Appia Foundation`
- 原文：`It should also work closely with established and newer standards bodies such as ISO, the Frontier Model Forum, Agentic AI Foundation, and the Open Secure AI Alliance, as well as implementation focused organizations, like the Appia Foundation, which is developing practical specifications…`
- 理由：原文把「標準組織」與「實作導向的組織」分開寫；而且措辭是 `should also work closely with`（主張要合作），欄名寫「點名的標準組織」會被讀成已經在合作，牴觸研究紀錄 `must_not_write` 第 17 條。內文那一段本來就分開寫，只有表格併掉了。
- 來源：OpenAI 公告

### 3.10 `increasing autonomy` 的 increasing 掉了（#60）

- before：`支柱二在管理 AI 研究自主程度與 RSI 上尤其關鍵` → after：`支柱二在管理 AI 研究日益增加的自主程度與 RSI 上尤其關鍵`
- 來源：OpenAI 公告

### 3.11 「三個方向各放上桌一份文件」（#62、#65）

- before：`這三個方向，OpenAI 目前各放上桌一份自己的文件：第一個方向的早期貢獻是`
- after：`這三個方向裡，OpenAI 目前為其中兩個各放上桌一份自己的文件：第一個方向的初步貢獻是`
- 原文：第一個方向後面接 `Our recent report on research acceleration is an initial contribution to this effort.`；第三個方向後面接 `Our misalignment reporting framework is an early contribution.`；**第二個方向（human oversight over automated AI research）原文沒有列任何貢獻**。
- 理由：三缺一；順帶把 `initial` 由「早期」改為「初步」，與第三個方向的 `early` 區分開。
- 來源：OpenAI 公告

### 3.12 「四條來源都未見台灣」不成立（#83、#84、#93、#99，四處）

- before（正文）：`以這四條來源查核到 2026 年 9 月 23 日，這份主張還沒有時程：`＋`沒有給前沿 AI 模型的門檻數字；以這幾條來源查核到 2026 年 9 月 23 日，未見台灣，也未見歐盟《人工智慧法》字樣。`
- after（正文）：`查核到 2026 年 9 月 23 日，這份主張還沒有時程：`＋`沒有給前沿 AI 模型的門檻數字；公告、NIST 那一頁與研究加速報告都未見台灣，公告也未見歐盟《人工智慧法》字樣。`
- before（FAQ 第五題）：`以這幾條來源查核到 2026 年 9 月 23 日，未見台灣。` → after：`查核到 2026 年 9 月 23 日，未見台灣。`
- before（callout）：`也沒有提到台灣，這幾點都是以四條來源查核到 2026 年 9 月 23 日為止的狀態。` → after：`公告也沒有提到台灣，這幾點都是查核到 2026 年 9 月 23 日為止的狀態。`
- 理由：第四條來源 `https://openai.com/news/rss.xml` 是 1,215 筆的新聞 feed，全文掃描後 **`Taiwan` 命中 1 次**（2025-06-01 的 `Operation “Sneer Review”: China-origin influence activity`）、**`EU AI Act` 命中 1 次**（2026-07-31 的 `Advancing responsible AI across Europe`），兩則都與本篇無關。「四條來源都未見台灣」因此是錯的。研究紀錄 `not_said` 第 4 條本來就只寫三份文件，內容包放大了範圍。FAQ 第五題的第二句（列出三份文件）本來就是對的，兩句因此也不再互相矛盾。
- 來源：`https://openai.com/news/rss.xml`

---

## 4. 查過而且正確、值得記下來的幾件事

- **兩份十國名單沒有被合併**（`must_not_write` 第 5 條）：表格兩列分別標了出處與日期，FAQ 第四題把差異（德國、印度 vs 歐盟、美國）講清楚，台灣兩列都寫「未見」而不是「被排除」。
- **分工沒有越界**（ASSIGNMENTS.md A2）：沒有重述失準通報框架的 6 份報告／2.15%／0.27%／SAG／三條分軌，沒有提 Amodei 或 Anthropic，沒有 50 人／10 億美元門檻，沒有展開 Hugging Face 事件，也沒有引用研究加速報告的營運數字或圖表數字。
- **RSI 的官方語氣照抄**：英文原句與中文括號譯文並列，逐字無誤。
- **兩個結尾連結**的 text 與目標內容包的 zh-TW `title` 逐字相同，兩個目標 JSON 都已存在於 worktree，`check_article.py` 對它們沒有 FAIL。
- **事件日**：RSS 的 `pubDate` 是 `Mon, 21 Sep 2026 10:00:00 GMT`（台北 9/21 18:00），換算後不跨日，不是 4.6 第 7 條那種整點佔位時刻的爭議；slug 後綴、`news_date`、第一段三者一致。
- **`verified_facts` 全數仍可驗證**：51 條 `verbatim_quote` 今天在重抓的 body 裡全部命中，`url` 也都在 `sources[]` 裡。

---

## 5. 留給協調者的事（也寫進研究紀錄的 `factcheck.open_questions`）

1. **研究紀錄自己的 `summary` 與 `suggested_table` 還留著修正前的說法**（「借用各國已成立的 AI 安全研究所網絡」、表格第三列把 Appia Foundation 併進標準組織）。本輪依規格只改內容包並附加 `factcheck` 物件，沒有動那兩欄。**第二輪與定稿請以內容包為準，不要照 `suggested_table` 把內容包改回去。**
2. **「規格」二字**：第二段與 callout 各有一句「以下規格與主張，一律標明是 OpenAI 自己的說法」「文中的規格與主張都是 OpenAI 自己的說法」。這是一篇政策主張，沒有任何規格；屬於措辭不是事實，本輪沒有改。
3. **第三節第一句壓掉了原文第三項 `incident definitions`**（原文是 `Evaluations, reporting requirements, and incident definitions by different nations could conflict`）。不是錯誤、只是壓縮；段落字數只剩 86 字餘裕（2,914／3,000），所以沒有補回去。
4. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 目前沒有這個 slug（DELTA-4-7 第 15 條說明是刻意的）。圖上四格的字（起點／支柱一／支柱二／界線）與本輪定稿一致，可以照畫；圖上不要出現十國這個數字。

## 6. 讀者優先檢查（DELTA-4-7 第 14 條）

| 項目 | 結果 |
| --- | --- |
| 正文／callout 出現「本文」 | 0 次 |
| 「官方」次數 | 2 次，且都是來源名「OpenAI 官方新聞頻道 RSS」 |
| description 是否寫成查證流水帳 | 否；句尾只帶「（2026 年 9 月查證）」 |
| title／description／summary 是否放挑選篇數 | 否 |
| 第一段是否讓讀者知道與自己的距離 | 是——第一段寫清楚標準不是許可證、各國自己決定要不要入法；台灣「未見」在 summary 第三句、表格與 FAQ 第五題各出現一次 |
| 每段的歸因密度 | 有五段各掛了兩到三次「OpenAI 主張／寫明／列出」。OpenAI 是新聞主角本身，不是「官方表示」式的贅述，本輪沒有改寫；若協調者認為仍太密，可在定稿時合併 |
| 購買建議／推薦式比價／未歸因的廠商宣稱／缺狀態的句子 | 都沒有。全篇每個操作性句子都帶著「主張／構想／公告沒有寫」的狀態 |

## 7. 自檢輸出（原樣）

`C:\Users\x8120\mokaair-work\news47\_tools\ai-news-openai-frontier-standards-20260921\check-final.log`：

```
OK ai-news-openai-frontier-standards-20260921 zh-TW paragraphs 2914
check_article exit=0
```

`…\lint-final.log`：

```
ai-news-openai-frontier-standards-20260921
  error: image_missing: zh-TW: /guides/ai-news-openai-frontier-standards-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-frontier-standards-20260921/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

`image_missing` 是出圖前的預期狀態（FACTCHECK-47 明列）；沒有 `raw_internal_url`。
修改前的基準是 `check-before.log`：`OK … zh-TW paragraphs 2890 / exit=0`——**過了機械檢查不等於查證過**，本輪就是在全綠的狀態下找到這 22 條。

## 8. 結論

**needs_second_round。** 第二輪是 DELTA-4-7 第 12 條的硬規定，而且本輪改了 **22 條事實主張／18 處文字**，
其中四處動到骨幹敘述（支柱一是什麼、Lutnick 交付任務的對象、三個方向只有兩份文件、四條來源都未見台灣）。
第二輪請把第 3 節每一處的 after 逐句回一手來源重查，並抽查第 2 節 CONFIRMED 的三分之一。
