# ai-news-openai-frontier-standards-20260921 查核報告（第二輪）

- 查核者：獨立查核代理（第二輪），沒有參與撰稿，也沒有參與第一輪
- 查核日：2026-09-23（與內容包四條 `sources[].checked_on`、研究紀錄 `checked_on` 一致）
- 內容包：`apps/api/app/guides/content/ai-news-openai-frontier-standards-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-openai-frontier-standards-20260921.json`
- 第一輪報告：`ai-news-openai-frontier-standards-20260921-round1.md`（主張 109 條、CHANGED 22、文字 18 處）
- **本輪逐條重查 60 條｜再確認 52｜CHANGED 8｜NOT FOUND 0｜另做 51 條 `verbatim_quote` 機械比對（0 MISS）**
- 結論：**ok**。第一輪那 18 處文字全部回原文重查後成立，沒有一處被推翻；本輪另改 8 處（含協調者指定的「規格」措辭兩處）。

---

## 1. 來源重抓（2026-09-23 台北 01:29，同一主機間隔 ≥2 秒）

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`；
UA、標頭、查詢字串、暫存檔名都沒有任何人的姓名或 email。原始檔在
`C:\Users\x8120\mokaair-work\news47\_r2raw\ai-news-openai-frontier-standards-20260921\`（與第一輪的 `_raw\` 分開存放）。

| # | URL | HTTP | bytes（本輪／第一輪） | 讀到正文？ |
| --- | --- | --- | --- | --- |
| A | `https://openai.com/index/building-standards-next-phase-ai/` | 200 | 418,052／418,047 | 是。抽取後 13,985 字元，五節齊全（RSI／International standards／(1) A mechanism…／(2) Common measurements…／The United States should lead）。本輪同樣沒有遇到 `openai.com/index/*` 的 403 |
| F | `https://openai.com/news/rss.xml` | 200 | 741,570／741,570 | 是。1,215 個 item；本篇 `link` = `…/building-standards-next-phase-ai`、`pubDate` = `Mon, 21 Sep 2026 10:00:00 GMT`、`category` = `Global Affairs` |
| N | `https://www.nist.gov/…/international-network-advanced-ai-measurement-evaluation-and-science` | 200 | 85,196／85,197 | 是。頁面自印 `February 13, 2026` 與 `Released February 13, 2026` |
| R | `https://openai.com/index/research-acceleration-view-inside-openai/` | 200 | 2,315,093／2,315,095 | 是（文字段落）。頁面自印 `September 6, 2026`；圖表仍由前端載入 |

bytes 的個位數差異是 Next.js build id 之類的快取字串。四條都是逐段讀正文，不是只看狀態碼。

---

## 2. 範圍與抽樣方法（FACTCHECK-47 第 9 行）

1. 第一輪改動的 **22 條主張／18 處文字**：每一處回一手來源重查（第 3 節）。
2. 第一輪**新寫進去的每一句**：逐句比對原文（第 4 節）。
3. 第一輪 85 條 CONFIRMED 的**隨機三分之一**：把 85 條按第一輪編號排序後**每三條取一條**（機械抽樣，不挑好查的），共 **29 條**（第 5 節）。
4. 指派訊息另外點名的疑點（「規格」措辭）與第二輪自己新查的面向（第 6 節）。
5. 研究紀錄的 `summary` 與 `suggested_table` 依協調者指示視為過時，**以內容包為準，沒有據以回改**。

---

## 3. 第一輪 22 條改動主張的覆核

判定：**R = 第一輪的改法成立（re-confirmed）**、X = 本輪再改。

| 第一輪 # | 改後的說法 | 一手原文 | 判定 |
| --- | --- | --- | --- |
| 7、14、22 | 支柱一＝「建立讓國家標準與國際標準互補的機制」，AI 安全研究所網絡只是達成手段之一、而且是「正在成形」 | `(1) A mechanism that facilitates complementary national and international frontier standards`；`One way of accomplishing this would be to leverage the emerging network of AI safety institutes` | R |
| 23 | 支柱二「用來管理 AI 研究日益增加的自主程度與 RSI」（不是「管理風險」） | `International AI standards will be particularly crucial in managing increasing autonomy in AI research and recursive self-improvement.` | R |
| 28 | 「範圍包含 RSI 在內」（不是「必須包含」） | `develop global technical standards for frontier AI, including for RSI` | R |
| 30 | 「維持有意義人類監督的能力」 | `maintain meaningful human oversight` | R |
| 33、85 | `pacing the frontier`／`Pacing AI development` 譯成「調節前沿發展步調」「調節步調」，不是「放慢」 | `may be as important to pacing the frontier as alignment research itself`；`Pacing AI development is not about maintaining a predetermined speed.` | R（原文自己否定「速度」框架，譯「放慢」會把 Anthropic 那篇的主張安到 OpenAI 頭上） |
| 38 | 「OpenAI 只寫了其中一種做法」 | `One way of accomplishing this would be` | R |
| 39 | 「舉例點名十個已經成立這類機構的國家」 | `such as those already established in …` | R |
| 40 | 「透過 CAISI 與各國產業機構促成標準制定」（不是「與 CAISI 合作」） | `to facilitate standard setting through the CAISI and national industry bodies` | R |
| 45 | 被交付任務的是 **CAISI**（設在 NIST 之內），受詞是 AI 系統的**資安** | `In June 2025, Secretary of Commerce Howard Lutnick charged the Center for AI Standards and Innovation (CAISI) within NIST with developing guidelines and best practices to measure and improve the security of AI systems and assist industry to develop voluntary standards.` | R |
| 52 | 表格第一列加「（舉例）」 | 同 #39 | R |
| 57、58 | 表格第三列改成「公告主張要合作的組織」，並把 Appia Foundation 與標準組織分開 | `It should also work closely with established and newer standards bodies such as ISO, the Frontier Model Forum, Agentic AI Foundation, and the Open Secure AI Alliance, as well as implementation focused organizations, like the Appia Foundation` | R（本輪再補「（舉例）」，見第 7 節第 6 點） |
| 60 | 「日益增加的自主程度」 | `increasing autonomy` | R |
| 62 | 「三個方向裡，OpenAI 目前為**其中兩個**各放上桌一份自己的文件」 | 第一個方向後接 `Our recent report on research acceleration is an initial contribution`；第三個方向後接 `Our misalignment reporting framework is an early contribution`；**第二個方向（Human oversight over automated AI research）原文沒有列任何貢獻** | R |
| 65 | `initial contribution` 譯「初步貢獻」，與第三個方向的 `early` 區分 | 同上 | R |
| 83、84、93、99 | 台灣／歐盟 AI 法案的否定句從「四條來源」限縮成「公告、NIST 那一頁與研究加速報告」 | 本輪重測：公告的 `Taiwan`／`Taipei`／`台灣`／`Europe`／`EU`／`European`／`AI Act` 全部 **0**；NIST 與研究加速報告的 `Taiwan` 皆 **0**；**RSS feed 裡 `Taiwan` 命中 1 次**（2025-06-01 中國影響力行動那則，原文寫 `a Taiwanese social media influencer`）、**`EU AI Act` 命中 1 次**（2026-07-31 歐洲那則） | R（四條全稱句確實站不住；限縮後逐一點名三份文件，比 `must_not_write` 第 7 條規定的句型更精確） |

**22 條全部 re-confirmed，0 條推翻。**

---

## 4. 第一輪新寫進去的句子，逐句回原文

第一輪動過字的 18 處，改寫後的**每一個新句子**都重新落回原文（不只看改動的那幾個詞）：

| 位置 | 新句子 | 對應原文 | 判定 |
| --- | --- | --- | --- |
| description | 「文章提出兩個支柱：讓國家標準與國際標準互補的機制，以及共同量測與事故通報協定」 | 兩個小標 `(1)`／`(2)` | R |
| block[0] | 「一是建立讓國家標準與國際標準互補的機制」 | 同上 | R |
| summary[1] | 「…二是建立共同量測與事故通報協定，用來管理 AI 研究日益增加的自主程度與 RSI」 | `(2) Common measurements and incident reporting protocols…`＋`managing increasing autonomy…` | R |
| block[4] | 「範圍包含 RSI 在內」 | `including for RSI` | R |
| block[5] | 「維持有意義人類監督的能力」 | `maintain meaningful human oversight` | R |
| block[6] | 「對調節前沿發展步調的重要性可能不亞於對齊研究本身」 | `may be as important to pacing the frontier as alignment research itself` | R |
| block[8] | 整段改寫（「只寫了其中一種做法」「舉例點名」「透過 CAISI…促成標準制定」「這條機制聚焦兩個面向：以能力基準衡量的前沿 AI 模型與開發者，以及自動化 AI 研究（含 RSI）的利益與風險管理」） | `One way… such as… to facilitate standard setting through the CAISI and national industry bodies, with a specific focus on (1) frontier AI models and developers, as measured by capability benchmarks; and (2) benefit-risk management for automated AI research, including RSI.` | R |
| block[9] | 新句「CAISI 設在 NIST 之內，2025 年 6 月由美國商務部長 Howard Lutnick 交付任務，發展指引與最佳實務以量測並提升 AI 系統的資安，並協助產業發展自願性標準」 | NIST 頁 Lutnick 那一段逐項對上；`within NIST`＝設在 NIST 之內 | R |
| 表格 row1 | 「已成立的 AI 安全研究所（舉例）」 | `such as those already established in` | R |
| 表格 row3 | 「公告主張要合作的組織」／「標準組織 …；實作機構 Appia Foundation」 | `should also work closely with … as well as implementation focused organizations, like the Appia Foundation` | R |
| block[13] | 「日益增加的自主程度」 | `increasing autonomy` | R |
| block[14] | 「這三個方向裡，OpenAI 目前為其中兩個各放上桌一份自己的文件」「初步貢獻」 | 三個 bullet 的原文（第二個沒有貢獻句） | R |
| block[22] | 「查核到 2026 年 9 月 23 日」「公告、NIST 那一頁與研究加速報告都未見台灣，公告也未見歐盟《人工智慧法》字樣」 | 本輪關鍵字掃描（第 9 節） | R |
| block[23] | 「自己說的『調節步調』（pacing）不是維持預定速度」 | `Pacing AI development is not about maintaining a predetermined speed.` | R |
| FAQ[4] | 「查核到 2026 年 9 月 23 日，未見台灣。」 | 同 block[22] | R |
| callout | 「公告也沒有提到台灣，這幾點都是查核到 2026 年 9 月 23 日為止的狀態。」 | 同上 | R |

---

## 5. 隨機抽樣的 29 條 CONFIRMED（每三條取一條）

| 第一輪 # | 主張 | 一手核對 | 判定 |
| --- | --- | --- | --- |
| 1 | slug 後綴 = `news_date` = 第一段日期，三者都是 2026-09-21 | 公告自印 `September 21, 2026`；RSS `pubDate` 台北 9/21 18:00，不跨日 | R |
| 4 | 四條 `sources[].checked_on` 全 2026-09-23、與紀錄一致、今天四條都重抓成功 | 第 1 節 | R |
| 8 | description「標準不是許可證、不是上市前審查，各國自行決定要不要入法」 | `These technical standards would not be licenses, mandatory prerelease review, or approval requirements…`＋`National governments would decide whether and how…` | R |
| 11 | 在 **Global Affairs** 分類發表 | 頁面標籤＋RSS `category` | R |
| 15 | 支柱二＝共同量測與事故通報協定 | 小標 `(2)` | R |
| 18 | 查核日出現在前兩段（checker 要求） | block[1]；`check_article.py` 通過 | R |
| 24 | 兩份名單都沒有出現台灣 | 公告十國／NIST 十個成員逐字比對 | R |
| 27 | RSI 定義 | `As AI systems take on more of the work of developing successive generations of AI, they can increasingly drive a process of recursive self-improvement (RSI), even while people remain involved.` | R |
| 32 | RSI 引句的中文括號譯文 | 逐字對照，語氣照 ASSIGNMENTS.md A2 的要求 | R |
| 36 | 「對開放模型與封閉模型都適用」 | `These challenges apply to both open and closed models.` | R |
| 42 | 兩個聚焦面向 | `with a specific focus on (1)… and (2) benefit-risk management…` | R |
| 46 | Lutnick 交付任務的內容三項 | NIST 原句逐項 | R |
| 49 | 「能力量測與評估、風險評估、防護是否足夠的共同技術基礎」 | `a common technical foundation for capability measurement and evaluation, risk assessment, and safeguard sufficiency` | R |
| 53 | 表格第一列「台灣：未見」 | 十國清單無台灣 | R |
| 56 | 表格第二列「台灣：未見」 | NIST 十個成員無台灣 | R |
| 63 | 研究加速報告：2026 年 9 月 6 日、《Research acceleration: The view inside OpenAI》 | 該頁自印 `OpenAI September 6, 2026`＋標題 | R |
| 67 | 關鍵基礎設施營運者與各國政府應建立安全溝通管道 | `critical infrastructure operators and governments worldwide to establish secure channels of communication to share national security concerns, emerging vulnerabilities and threats, and best practices…` | R |
| 70 | `image.caption` 與研究紀錄 `diagram.caption` 逐字相同 | `check_article.py` 也在比對這一條 | R |
| 73 | 諮詢開放／封閉模型開發者、獨立技術專家與學界 | `by consulting open model and closed model developers, independent technical experts, and academia` | R |
| 76 | 航空與金融穩定的類比 | `draw lessons from areas such as aviation and financial stability, where countries have developed common technical standards and trusted channels for cooperation without giving up national authority` | R |
| 79 | 沒有時程 | 全文無任何日期／期限 | R |
| 82 | 沒有前沿 AI 模型的門檻數字 | 只有 `as measured by capability benchmarks` | R |
| 88 | 「可以直接看 openai.com 的 Global Affairs 分類，或 NIST／CAISI 的網頁」 | 分類頁 `/news/global-affairs/` 存在；NIST 頁自己連 CAISI | R |
| 91 | FAQ Q3：完全自主的 RSI 今天沒有發生＋RSI 定義 | 同 #27、#31 | R |
| 95 | 五題答案都是純文字、沒有連結 | `check_article.py` 也在檢查這一條 | R |
| 98 | callout「公告沒有寫時程、主辦機構或法律效力」 | 全文無時程／主辦機構／`binding`／`treaty` | R |
| 103 | source 1 標題／網址／`checked_on` | 與頁面 `<title>` 一致 | R |
| 106 | source 4 標題 | 見第 10 節第 4 點（措辭疑慮，不是事實錯誤） | R |
| 109 | 沒有購買建議、沒有未歸因的廠商宣稱 | 全篇操作性句子都帶狀態（主張／構想／公告沒有寫） | R |

**29 條全部 re-confirmed。**

---

## 6. 第二輪自己新查的 9 個面向

| # | 面向 | 結果 |
| --- | --- | --- |
| S1 | block[5] 說「原文**接著**劃出現況的界線」 | **X**——原文順序相反（引句在前、`Done without appropriate care…` 在後，「有意義人類監督」又來自更後面的 Collective action 條目）。已改 |
| S2 | block[6] 三個問題第一項壓掉 `incident definitions` | **X**——第一輪列為 open question、理由是字數餘裕只剩 86 字；本輪刪掉 block[14] 的編輯自述後有餘裕，補回 |
| S3 | block[14] 的歸因密度與編輯自述 | **X**——同段 3 個歸因詞（超過 FACTCHECK-47「任一段最多兩個」），且「這是另一篇文章的題目，這一篇只帶一句」是編輯過程的自述（DELTA-4-7 第 14 條）。已改，改後 2 個 |
| S4 | block[23]「讓對齊研究與部署走在能力前面」 | **X**——原文是 `alignment research and deployment of that research`，走在前面的是對齊研究**及其部署**。已改 |
| S5 | 表格第三列沒標示是舉例 | **X**——原文 `standards bodies such as ISO…`，與第一列同一種句型。已改 |
| S6 | 圖解 `alt` 的支柱一用語 | **X**——仍寫「各國標準互補機制」，與第一輪修正後的正文與小標互相矛盾。已改；研究紀錄 `diagram.nodes` 同步改（那一欄會被畫進圖裡） |
| S7 | 指派訊息點名的「規格」 | **X**——block[1] 與 callout 各一處指涉政策主張，已依協調者裁定改成「標準」；block[20]「實務規格」對應原文 `practical specifications`，**保留** |
| S8 | 全篇歸因密度逐段計數 | 只有 block[14] 超標（已改）。block[10] 的 4 個標記裡兩個是 `must_not_write` 第 6 條硬性要求的清單出處標示，真正的「X 表示」只有 1 個；開頭段真正的歸因詞只有「文章同時寫明」1 個 |
| S9 | `description` 字數、`summary` 數字是否都在正文、段落字數 | description 179 字（120–200）✓；`summary` 無正文沒有的數字（checker 也在比）✓；段落 2,888 字（1,800–3,000）✓ |

---

## 7. 本輪改掉的 8 處（before → after ＋ 來源）

> 全部用「一次只命中一次」的字串取代寫回，沒有用 `json.dump`。

1. **block[1]、callout（協調者指定）｜來源 `https://openai.com/index/building-standards-next-phase-ai/`**
   - before：`以下規格與主張，一律標明是 OpenAI 自己的說法` ／ `文中的規格與主張都是 OpenAI 自己的說法`
   - after：`以下標準與主張，一律標明是 OpenAI 自己的說法` ／ `文中的標準與主張都是 OpenAI 自己的說法`
   - 這是一篇政策主張，沒有任何規格。**block[20] 的「實務規格」不動**——它對應原文 `practical specifications`，是正確用法。

2. **block[5]｜同上**
   - before：`原文接著劃出現況的界線` → after：`原文也劃出現況的界線`
   - 原文順序是：`Fully autonomous RSI is not happening today…`（引句）→ `Whether and how to proceed…` → `Done without appropriate care and caution, RSI could result in humans losing practical control…`。引句在**前**，「接著」是對原文結構的錯誤描述。

3. **block[6]｜同上**
   - before：`各國評估與通報要求可能互相衝突` → after：`各國評估、通報要求與事故定義可能互相衝突`
   - 原文：`Evaluations, reporting requirements, and incident definitions by different nations could conflict`。第一輪的 open question 第 3 條，本輪補回。

4. **block[14]｜同上**
   - before：`；第三個方向的早期貢獻則是失準通報框架——這是另一篇文章的題目，這一篇只帶一句：OpenAI 把它列為支柱二的早期貢獻。`
   - after：`；第三個方向的早期貢獻則是 OpenAI 的失準通報框架。`
   - 原文只有一句 `Our misalignment reporting framework is an early contribution.`；`must_not_write` 第 2 條也只允許一句。刪掉的是編輯過程的自述，事實一句不少，歸因詞由 3 個降為 2 個。

5. **block[23]｜同上**
   - before：`而是讓對齊研究與部署走在能力前面` → after：`而是讓對齊研究及其部署走在能力前面`
   - 原文：`it is about ensuring that alignment research and deployment of that research stay ahead of capabilities`。原句會被讀成「對齊研究與（產品）部署」。

6. **表格第三列｜同上**
   - before：`公告主張要合作的組織` → after：`公告主張要合作的組織（舉例）`
   - 原文：`standards bodies such as ISO, the Frontier Model Forum, Agentic AI Foundation, and the Open Secure AI Alliance`——與第一列十國同一種 `such as` 句型，第一輪替第一列加了、第三列漏了。

7. **block[16] 圖解 `alt`｜同上**
   - before：`支柱一寫各國標準互補機制` → after：`支柱一寫國家與國際標準互補機制`
   - 互補的是 `national and international frontier standards`，不是「各國之間」。舊字與第一輪修正後的正文、小標「支柱一：讓國家標準與國際標準互補」互相矛盾。

8. **研究紀錄 `diagram.nodes[1]`｜同上**
   - before：`["支柱一", "各國標準互補機制"]` → after：`["支柱一", "國家與國際標準互補機制"]`
   - 這一欄是 `build_assets.py` 出圖時真正畫在圖上的字（DELTA-4-7 第 15 條，圖還沒畫），留著舊說法就會畫出與正文矛盾的圖。
   - **`summary` 與 `suggested_table` 依協調者指示維持原狀、不得據以回改內容包。**

---

## 8. 讀者優先檢查（DELTA-4-7 第 14 條、FACTCHECK-47）

| 項目 | 結果 |
| --- | --- |
| 「本文」 | 0 次（全份 JSON） |
| 「官方」 | 2 次，都是來源名「OpenAI 官方新聞頻道 RSS」；另有 1 次「官網」是敘述發表地點 |
| description | 179 字，句尾只帶「（2026 年 9 月查證）」，不是查證流水帳 |
| title／description／summary 的挑選篇數 | 無 |
| 開頭段歸因詞 | 1 個（「文章同時寫明」）。「OpenAI 提出兩個支柱」是新聞主角本身在做的動作，不是「X 表示」式的贅述 |
| 任一段歸因詞 ≤ 2 | 改後成立。改前 block[14] 是 3 個（已改）；block[10] 的計數含兩個 `must_not_write` 第 6 條硬性要求的清單出處標示（NIST 頁面／OpenAI 文中），真正的「X 表示」只有「OpenAI 形容為」1 個 |
| 第一段是否讓讀者知道與自己的距離 | 是——第一段就寫明標準不是許可證、各國自己決定要不要入法；台灣「未見」在 summary 第三句、表格兩列與 FAQ 第五題各有一處 |
| 購買／訂閱／投資建議、未歸因的廠商宣稱 | 都沒有；`topics` 只有 ai／ai-news，沒有 finance，只有一個一般 callout |
| 範圍不明的否定句 | 都已限縮到具名的文件與查核日（第一輪修的四處，本輪覆核成立） |

---

## 9. 機械檢查

1. **`verified_facts` 的 51 條 `verbatim_quote`**：對今天重抓的正文做**連續字串**比對（先正規化 NBSP、U+2011、彎引號與空白），**51/51 命中、0 MISS**；沒有一條含 `...`／`…`／`|` 的拼接引文，因此沒有「把不同段落拼成一句」的情形。`url` 也都在 `sources[]` 裡。
2. **關鍵字掃描（四份原始檔，去 `<!-- -->` 後 `html.unescape`）**：
   - 公告：`Taiwan` 0、`Taipei` 0、`台灣` 0、`Europe`／`EU`／`European` 0、`AI Act` 0、`binding` 0、`treaty` 0。
   - NIST：`Taiwan` 0；`European Union` 1（成員清單）；`AI Act` 的 1 次命中是 `America's AI Action Plan` 的子字串。
   - 研究加速報告：`Taiwan` 0。
   - RSS：**`Taiwan` 1**（`a Taiwanese social media influencer`）、**`EU AI Act` 1**——這正是第一輪必須把否定句限縮的理由。
3. **兩個結尾連結**與目標內容包 zh-TW `title` 逐字比對：兩條都 `True`（長度也相同，32／28 字）。
4. **圖解**：`diagram.nodes` 四格、`alt` 四格，改後一致；節點沒有任何數字（DELTA-4-7 第 15 條「圖上不可出現正文沒有的數字」）。
5. **`sources` 與紀錄**：四條 URL 與順序一致、`checked_on` 全為 2026-09-23（`check_article.py` 也在比這兩條）。

---

## 10. 留給協調者的事

1. **block[1] 整段是「我們讀了哪幾頁」的查證紀律**，DELTA-4-7 第 14 條說這不是內容；但它同時是本批所有文章的共同格式，而且 `check_article.py` 要求查核日出現在前兩段。本輪只換掉「規格」二字，沒有動段落結構。同段的「本站沒有做任何實測」對一篇政策主張也讀不太通——**要不要全批一起改，是協調者的決定**。
2. **FAQ 第一題仍寫「以這幾條來源查核到 2026 年 9 月 23 日，公告沒有寫啟動時間」**。這一句的否定範圍本來就限縮在「公告」，不是第一輪修掉的那種四條來源全稱句，所以沒有動；但「這幾條來源」四個字在這裡是多餘的。
3. **block[13] 第三個方向壓掉了 `for alignment and automated AI research issues`**（事故分類追蹤通報回應的適用範圍）。不是錯誤、只是壓縮。
4. **`sources[3]` 的標題寫「（公告點名的第一份貢獻）」**：原文 `initial contribution` 掛在第一個方向、`early contribution` 掛在第三個方向，「第一份」指的是「第一個方向的那一份」而不是「時間上最早的那一份」，讀者看標題可能誤解。屬於來源標題措辭，本輪沒有改。
5. **`summary` 第五句後半（「預期會隨時間大幅演變」）只出現在 FAQ 第一題與 callout**，沒有落在任何正文段落。checker 的 `body_without_summary` 涵蓋 callout 所以不會 FAIL，事實本身也有 `verbatim_quote` 撐著（`While we expect this concept to evolve substantially over time`），本輪沒有為此加字。
6. **研究紀錄的 `summary` 與 `suggested_table` 仍是第一輪修正前的說法**（「借用各國已成立的 AI 安全研究所網絡」、第一列沒有「（舉例）」、第三列把 Appia Foundation 併進標準組織）。依協調者指示本輪不動，**定稿一律以內容包為準**。
7. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 仍沒有這個 slug。照 `diagram.nodes` 畫（支柱一那格已改為「國家與國際標準互補機制」），圖上不要出現十國這個數字。

---

## 11. 自檢輸出（原樣）

`…\_tools\ai-news-openai-frontier-standards-20260921-r2\check-r2-final.log`：

```
OK ai-news-openai-frontier-standards-20260921 zh-TW paragraphs 2888
check_article exit=0
```

`…\lint-r2-final.log`：

```
ai-news-openai-frontier-standards-20260921
  error: image_missing: zh-TW: /guides/ai-news-openai-frontier-standards-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-openai-frontier-standards-20260921/diagram-1.svg
1 entries checked
pack_cli lint exit=1
```

`image_missing` 是出圖前的預期狀態（FACTCHECK-47 明列），沒有 `raw_internal_url`。
本輪開始前的基準是 `check-r2-before.log`：`OK … paragraphs 2914 / exit=0`——**全綠的狀態下仍找到這 8 處**。

## 12. 結論

**ok。** 第一輪的 22 條改動全部回一手來源重查後成立，18 處文字沒有一處被推翻；隨機抽樣的 29 條 CONFIRMED 也全部成立。
本輪另改 **8 處**：兩處是協調者指定的「規格」措辭，六處是新查到的事實或其相依處（原文順序、`incident definitions`、
編輯自述與歸因密度、`deployment of that research`、表格第三列的 `such as`、圖解與 `diagram.nodes` 的支柱一用語）。
沒有 NOT FOUND，沒有需要站主裁定的事實爭議；第 10 節七條是措辭與全批格式的問題，交協調者定稿時處理。
