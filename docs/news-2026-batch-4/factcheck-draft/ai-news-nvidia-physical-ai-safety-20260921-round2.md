# `ai-news-nvidia-physical-ai-safety-20260921` 查核報告（第二輪）

> 協調者複製進 `docs/news-2026-batch-4/factcheck-draft/<slug>.md` 時，這一份是「第二輪」那一節。

- 查核者：independent factcheck agent, round 2（沒有參與撰稿，也沒有參與第一輪）
- 查核日：2026-09-23（與第一輪同一天重抓，`checked_on` 不動）
- 垂直／順序：AI，`display_order` 176，事件日 2026-09-21（16:00 是佔位時刻，不換算）
- 內容包：`apps/api/app/guides/content/ai-news-nvidia-physical-ai-safety-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-nvidia-physical-ai-safety-20260921.json`
- 第一輪報告：`factcheck/ai-news-nvidia-physical-ai-safety-20260921-round1.md`（124 條、8 處編輯）
- 結論：**ok**（121 條主張，3 處事實／一致性修正、2 處為了騰字數刪掉的重複敘述；沒有任何一句因為查不到而刪除）

## 1. 我自己重抓的結果（2026-09-23 台北）

六條全部用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥2 秒；
UA、標頭、查詢字串一律沒有帶入任何人的姓名或 email。HTML 先刪 `<!-- -->`、去 `script`／`style`、再 `html.unescape`、`&nbsp;` 換空白；
PDF 用系統 `python` 的 pypdf（`apps/api/.venv` 沒有 pypdf）。

| # | URL | HTTP | bytes | 抽出正文 | 與研究紀錄／第一輪 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://blogs.nvidia.com/blog/physical-ai-halos-safety/` | 200 | 121,824 | 9,790 字元 | bytes 相同 |
| 2 | `https://www.nvidia.com/en-us/ai-trust-center/physical-ai/safety-certification/` | 200 | 665,291 | 23,192 字元 | bytes 相同 |
| 3 | `https://www.nvidia.com/en-us/ai-trust-center/halos/robotics/` | 200 | 761,431 | 35,276 字元 | bytes 相同 |
| 4 | `https://search.anab.org/public/organization_files/NVIDIA-Corporation-Cert-and-Scope-File-06-06-2025_1749243349.pdf` | 200 | 434,445 | 6 頁／8,592 字元 | bytes 相同 |
| 排除 | `https://my.abiresearch.com/research/15976/` | 200 | 17,744 | 388 字元（登入牆） | 相同 |
| 排除 | `https://omdia.tech.informa.com/om146251/robotics-hardware-market-forecast--2026` | 200 | 221,965 | 10,859 字元（訂閱牆） | 相同（第一輪已改掉研究紀錄寫的 403） |

**一個方法上的更正，給後面幾輪參考**：純粹用「壓縮空白後的連續子字串」比對，我第一次跑出 **7 個 MISS**
（`Physical AI safety means proving…`、`By 2035, ABI Research…`、`Deployment is ongoing.…`、`In autonomous vehicles, Geely…`、
`Members of the … Inspection Lab include…`、`In robotics, acontis and QNX…`、以及 `sources[1]` 同一句）。
逐一回去看原始 HTML，**全部是 nvidia.com 行內 `<a>` 造成的**：標籤剝掉之後會在字中或標點前留下空白，
抽出來長成 `AVs , humanoid robots ,`、`Bosch , Gatik ,`，`Agility` 甚至被拆成 `Agilit y`。
改用「去掉所有空白」再比對，**42 條研究紀錄引文（4 條 `sources` ＋ 38 條 `verified_facts`）與內容包 15 段英文引文全部命中，0 失敗**，
`verified_facts` 的 `url` 全部在 `sources[]` 裡，沒有一條引文含 `...`／`…`／`|`，也沒有把兩段拼成一句的情形。
第一輪報「0 失敗」是對的，但如果哪一輪只用壓縮空白比對又沒有回頭看 HTML，很可能會誤刪七條正確的引文。

事件日覆核：`article:published_time` 2026-09-21T16:00:46+00:00、`article:modified_time` 2026-09-21T16:06:14+00:00，
JSON-LD 的 `datePublished`／`dateModified` 相同，頁面自印 `September 21, 2026`，抽出的正文裡沒有任何時刻字串。
slug 尾碼、`news_date`、正文第一段三者都是 2026-09-21——DELTA-4-7 第 10 條維持原判，不換算。

## 2. 主張表（121 條）

判定：C＝CONFIRMED（第二輪回一手來源覆核後仍成立）、CH＝CHANGED（本輪改掉）。

### A. 第一輪改動過的 13 條，逐條回一手來源重驗

| # | 第一輪的判定 | 第二輪覆核 | 判定 | 我看到的原文 |
| --- | --- | --- | --- | --- |
| A1 | 標題的「評估」全篇沒有對應 | 內容包的「評估」出現 **0 次**（本輪一度因第 8 段的意譯變成 1 次，協調者裁定改用「經第三方查驗」後回到 0）；部落格確實有一項評估 `TÜV Rheinland also performed an independent UNECE safety assessment of NVIDIA DRIVE AV`，而文章從頭到尾沒有寫它 | C | 部落格 `How Is NVIDIA Halos Independently Assessed?` 一節 |
| A2 | 新標題三種強度都指得出來 | 「已認證」＝表格第 1 列與第 7 段、「檢驗中」＝第 2 列與第 8 段、「機構認可」＝第 3 列與第 9 段，第 13 段四種強度一起列 | C | 內容包自身 |
| A3 | 標題長度 36（≤60） | 36 | C | checker |
| A4 | 摘要第二句 ASIL D 的對象 | `TÜV SÜD certified NVIDIA's Automotive Product Lifecycle software process and DriveOS 6.0 to ISO 26262 ASIL D, as well as NVIDIA's automotive engineering processes to ISO/SAE 21434.` ——ASIL D 掛在「軟體流程＋DriveOS 6.0」，21434 掛在「車用工程流程」，第一輪改對了 | C | 部落格 |
| A5 | 表格第一列拆開兩個標準 | 同上；拆開後的第 2、3 欄與原文一一對應，沒有把 DriveOS 6.0 也寫成通過 21434 | C | 部落格 |
| A6 | 刪掉「市場研究機構」 | 四條來源全文搜 `market research`／`research firm`／`analyst firm` 各 **0 筆**；原文只有 `ABI Research projects` 與 `Omdia estimates` | C | 四條來源 |
| A7 | 「到 2035 年前」→「到 2035 年」 | 原文 `By 2035,` | C | 部落格 |
| A8 | 刪掉 Omdia 那句的「全球」 | 原文 `roughly 60 million industrial robots will be deployed between 2026 and 2035`，沒有地理範圍 | C | 部落格 |
| A9 | 「Omdia 連結被拒絕存取」已不成立 | 今天仍是 200／221,965 bytes，頁面自印 `A subscription is required to view this content.` | C | Omdia |
| A10 | 改寫成「兩份原始報告都要訂閱才讀得到」 | Omdia 如上；ABI 頁面自印 `Log in now to access` 與 `Subscriber Content ✓ Full Reports`——原始報告確實要訂閱才讀得到，敘述撐得住（細節見 §5 待決 4） | C | ABI／Omdia |
| A11 | 正文第 9 段：ANAB 的證書開給 NVIDIA Corporation | ANAB PDF 六頁全文 `Halos` 0 次、`Inspection Lab` 0 次、`NVIDIA Corporation` 2 次；第 1 頁印 `The ANSI National Accreditation Board Hereby attests that NVIDIA Corporation … Fulfills the requirements of ISO/IEC 17020:2012`、`Expiry Date: 02 January 2027`、`Certificate Number: AI-3345` | C | ANAB PDF |
| A12 | FAQ 第三題同一件事 | 同上 | C | ANAB PDF |
| A13 | 研究紀錄 `title` 同步 | 第二輪進場時已同步（`check_article.py` 第 305 行會比對），本輪沒有再動 | C | 兩檔比對 True |

### B. 第一輪新寫進去、沒有人查過的 8 段字串（逐字回來源）

| # | 新寫的字串 | 判定 | 依據 |
| --- | --- | --- | --- |
| B1 | 標題「已認證、檢驗中與機構認可是三件不同的事」 | C | 三個詞在正文與表格都指得出來（A2） |
| B2 | 摘要「與車用產品生命週期軟體流程認證到 ISO 26262 ASIL D」 | C | `Automotive Product Lifecycle software process and DriveOS 6.0 to ISO 26262 ASIL D` |
| B3 | 表格 r1c2「DriveOS 6.0、車用產品生命週期軟體流程與車用工程流程」 | C | 同上句＋`as well as NVIDIA's automotive engineering processes` |
| B4 | 表格 r1c3「…通過 ISO 26262 ASIL D；車用工程流程通過 ISO/SAE 21434」 | C | 同上 |
| B5 | 正文第 4 段「查核當下兩份原始報告都要訂閱才讀得到」 | C | A10 |
| B6 | FAQ4「查核當下兩份原始報告都要訂閱才讀得到」 | C | A10 |
| B7 | 正文第 9 段「ANAB 的證書開給 NVIDIA Corporation，符合 ISO/IEC 17020，登記類別是…」 | C | A11 |
| B8 | FAQ3「ANAB 的證書與認可範圍檔案開給的是 NVIDIA Corporation」 | C | A11。範圍檔案第 1 頁之後同樣印 `NVIDIA Corporation`，`TYPE C (SECOND PARTY) BODY` 在範圍頁 | 

### C. 112 條 CONFIRMED 抽樣三分之一（seed 20260923，37 條）

抽到的編號（沿用第一輪報告的號碼）：2、5、6、9、12、21、26、29、31、34、40、45、46、50、54、56、60、71、72、75、77、81、82、84、92、94、95、97、98、104、109、113、114、115、117、120、122。

| 第一輪 # | 主張 | 判定 | 第二輪依據 |
| --- | --- | --- | --- |
| 2 | 「認證」與「檢驗中」是不同的事 | C | 同一節同時有 `TÜV SÜD certified…` 與 `TÜV Rheinland is inspecting…` |
| 5 | 對象含自駕車與機器人 | C | `AVs, humanoid robots, industrial robots and more` |
| 6 | 橫跨硬體、軟體、AI、運作環境與部署生命週期 | C | 逐字命中 |
| 9 | `description` 句尾只帶「（2026 年 9 月查證）」、沒有查證流水帳 | C | 實際字串為「…效期到何時（2026 年 9 月查證）。」，長度 152（120–200） |
| 12 | slug 尾碼＝`news_date`＝第一段 | C | 三處都是 2026-09-21 |
| 21 | 依據 NVIDIA 官方部落格 | C | `sources[0]` 今日 200 且讀到正文 |
| 26 | 不是部署前檢查一次就結束 | C | `not a one-time check before deployment` |
| 29 | ANAB 認可為 ISO/IEC 17020 檢驗機構 | C | 部落格逐字 |
| 31 | 檢驗方式是審閱文件 | C | ANAB `Verification of conformity of inspected items by review of documentation` |
| 34 | 80 國、包含中國（NVIDIA 說法） | C | 認證頁逐字 |
| 40 | 第 3 段英文引文 | C | 逐字 |
| 45 | `may require additional safety testing`（可能，非必然） | C | 逐字，括號註解保留 |
| 46 | 測試要搭配模擬與合成資料 | C | 逐字 |
| 50 | 兩個數字是外部機構預測 | C | `ABI Research projects` / `Omdia estimates` |
| 54 | `the platforms, standards and evidence remain specific to each domain` | C | 逐字 |
| 56 | IGX Thor 帶專用功能安全島 | C | `with a dedicated Functional Safety Island` |
| 60 | 「level 4-ready」還不是已上路載客的 L4 | C | 第 6 段但書原文仍在，本輪一個字都沒動 |
| 71 | 也把車用工程流程認證到 ISO/SAE 21434 | C | 逐字 |
| 72 | `TÜV Rheinland is inspecting …readiness` | C | 逐字 |
| 75 | ANAB 認可的是實驗室不是車或機器人 | C | `The lab inspects scoped Halos integrations and helps companies prepare for final certification by independent third-party bodies` |
| 77 | `review of documentation` | C | ANAB |
| 81 | 圖解四格：硬體層／軟體層／驗證層／檢驗報告 | C | 研究紀錄 `diagram.nodes` |
| 82 | 「檢驗報告不等於最終系統認證」 | C | 同上＋第 9 段 |
| 84 | 圖上沒有任何數字 | C | `diagram` 與 `hero_label` 掃描 0 個數字 |
| 92 | `the first and only full-stack safety system for physical AI` 有歸因 | C | 逐字，第 11 段寫「NVIDIA 自稱」 |
| 94 | `early access for registered developers` | C | 機器人頁逐字 |
| 95 | 不是公開上市產品 | C | 同上 |
| 97 | 第 12 段重述 level 4-ready 但書 | **CH** | 事實成立，但與第 6 段重複；為了騰出第二組落差的字數刪掉重述，但書本身留在第 6 段（見 §3 改動 4） |
| 98 | 可到 AI Trust Center 查元件、從常見問題連到 ANAB 檔案 | C | 機器人頁 `A Path for Safety Certification`；認證頁常見問題有 `Read the complete ANAB accreditation scope here.` |
| 104 | 官方用的字是「正在檢驗」不是「已經認證」 | C | `is inspecting` |
| 109 | FAQ3 沒有價值判斷、沒有自行解釋 Type A／B／C | C | 全文沒有出現 Type A、Type B 的定義敘述 |
| 113 | 支援 Linux 與 Linux 加 QNX | C | `in Linux and Linux plus QNX configurations` |
| 114 | Digit 官方寫的是「將會是」 | C | `will be the first production robot shipping with NVIDIA Halos OS` |
| 115 | 完全沒有提到價格、上市日或台灣供貨時程 | C | 部落格與 ANAB PDF 價格字串 0 筆；**兩個 nvidia.com 頁面各有 1 筆 `pricing`，出處是網站地區切換視窗那句 `Visit your regional NVIDIA website for local content, pricing, and where to buy partners specific to your country.`**，是版面不是內容——文章的說法不受影響，但第一輪「四頁全文 0 筆」的說法要修正（見 §5 待決 3） |
| 117 | 「台灣 (Taiwan)」是網站自己的地區選單 | C | 認證頁與機器人頁各 2 筆，一筆在地區切換視窗（`… 中国大陆 (Mainland China) / 台灣 (Taiwan) / 日本 (Japan) / Continue`）、一筆在表單國家下拉（`Syria / Taiwan / Tajikistan`）；部落格與 ANAB PDF 各 0 筆 |
| 120 | callout「原始報告查核當下都讀不到」 | C | 今天兩份仍在牆後 |
| 122 | 第一個結尾連結 text 與索引 zh-TW `title` 逐字相同 | C | 直接讀 `ai-news-2026-january-september-index.json` 比對 True |

### D. 引文比對（57 條）

| 類別 | 條數 | 結果 |
| --- | --- | --- |
| 研究紀錄 `sources[].verbatim_quote` | 4 | 全部命中，`url` 與內容包 `sources` 一致 |
| 研究紀錄 `verified_facts[].verbatim_quote` | 38 | 全部命中各自的 `url`；沒有一條含刪節號或直線符號，沒有跨段拼接 |
| 內容包裡的英文逐字引文 | 15 | 全部命中 |

### E. 第二輪自己新增的 6 條檢查

| # | 檢查 | 判定 | 說明 |
| --- | --- | --- | --- |
| E1 | 摘要第三句是否跟上第一輪的 ANAB 修正 | **CH** | 沒有跟上。第一輪改了正文與 FAQ，摘要仍把 Type C 直接掛在實驗室名下，違反「`summary` ⊆ 正文」。已改 |
| E2 | 表格第三列是否跟上 | **CH** | 同樣沒跟上，涵蓋對象只寫實驗室、狀態欄卻掛 ANAB 檔案上的登記類別。已改 |
| E3 | 協調者點名的第二組措辭落差 | **CH** | 機器人頁常見問題「Is the NVIDIA IGX SoC safety certified?」答句是 `The NVIDIA IGX is a third-party assessed, safety-compliant System-on-a-Chip…`，與部落格 `designed to support systems developed for standards including IEC 61508 and ISO 13849` 不一致。已用一個子句補進第 8 段，字數從別處騰出（見 §3） |
| E4 | `summary` ⊆ 正文、FAQ 答案 ⊆ 正文、圖解數字 ⊆ 正文 | C | 摘要的每個數字都在正文（checker 也會擋）；FAQ 六題的答案內容都在正文找得到；圖解與 `hero_label` 沒有數字 |
| E5 | 否定句的範圍 | C | 「四個官方來源都沒提到台灣」「四個來源裡沒有出現任何…事故、召回或主管機關調查」「查核到的四個官方頁面都沒有提到台灣」全部限縮在四條來源與查核日，沒有寫成「NVIDIA 沒有／從未」 |
| E6 | 界線與版型 | C | 只有 1 個 callout、沒有投資免責段落、`topics` 是 `["ai","ai-news"]`（不帶 `finance`）；沒有購買／升級／訂閱建議；沒有推定台灣可用；廠商宣稱（`first and only`、80 國、`safety-certified`）都有歸因 |

**統計：121 條 → CONFIRMED 118、CHANGED 3（E1／E2／E3）；另有 2 處為了騰字數刪掉的重複敘述（C97 與第 11 段）。沒有 NOT FOUND，沒有整句刪除。**

## 3. 改了什麼（5 處編輯，全部在內容包）

段落字數 **2,982 → 2,996**（上限 3,000）。加了 68 字、刪了 44＋10 字，**刪掉的兩處都是重複敘述，沒有動任何但書、限定詞或歸因**。

### 1. 摘要第三句：把 ANAB 的持證者補上（第一輪漏掉的連動）

- 原：`NVIDIA 自家的 Halos AI Systems Inspection Lab 通過 ANAB 認可為 ISO/IEC 17020 檢驗機構，登記類別是 Type C（second party），檢驗方式是審閱文件，效期到 2027 年 1 月 2 日；…`
- 改：`NVIDIA 自家的 Halos AI Systems Inspection Lab 通過 ANAB 認可為 ISO/IEC 17020 檢驗機構；ANAB 的證書開給 NVIDIA Corporation，登記類別是 Type C（second party），檢驗方式是審閱文件，效期到 2027 年 1 月 2 日；…`
- 來源：<https://search.anab.org/public/organization_files/NVIDIA-Corporation-Cert-and-Scope-File-06-06-2025_1749243349.pdf>
- 理由：第一輪判定「Type C 是印在開給 NVIDIA Corporation 的證書上，不是印在實驗室名下」，並據此改了正文第 9 段與 FAQ 第三題——但摘要沒改。摘要是讀者最先看到的五句，而且規格要求 `summary` ⊆ 正文；留著就等於文章自己前後兩套說法。

### 2. 表格第三列：同一個連動

- 原：`["機構獲得認可", "NVIDIA 自家的 Halos AI Systems Inspection Lab", "認可為 ISO/IEC 17020 檢驗機構，登記類別 Type C（second party）", "ANAB"]`
- 改：`["機構獲得認可", "NVIDIA 自家的 Halos AI Systems Inspection Lab（證書開給 NVIDIA Corporation）", "認可為 ISO/IEC 17020 檢驗機構，登記類別 Type C（second party）", "ANAB"]`
- 理由：與第一輪拆表格第一列的理由相同——表格是這篇的骨幹，最容易被整列抄走。「認定者」欄寫 ANAB，「涵蓋對象」欄就必須是 ANAB 檔案上認得出來的對象。

### 3. 正文第 8 段：補上第二組措辭落差（協調者裁定的那一條）

- 原（段末）：`…與 9 月 21 日說法不一致，這裡以「正在檢驗」版本為準。`
- 改（段末）：`…與 9 月 21 日說法不一致，這裡以「正在檢驗」版本為準；同一頁另稱 IGX 是「third-party assessed」（意為：經第三方查驗）的晶片，與部落格「設計上支援」的措辭同樣有落差。`
- **協調者裁定（本報告交付後）**：`third-party assessed` 一律意譯成「經第三方查驗」，正文不得出現「評估」兩個字；標題的三種強度（已認證、檢驗中、機構認可）維持不變。已照做——意譯前後同為兩個字，段落字數仍是 **2,996**，正文＋FAQ＋callout 的「評估」回到 **0 次**，`check_article.py` 重跑仍印 `OK … paragraphs 2996`。
- 來源：<https://www.nvidia.com/en-us/ai-trust-center/halos/robotics/> 的常見問題
  `Is the NVIDIA IGX SoC safety certified?` → `The NVIDIA IGX is a third-party assessed, safety-compliant System-on-a-Chip that includes built-in hardware safety mechanisms, such as a Functional Safety Island (FSI), to meet stringent industrial safety standards.`
  對照部落格 <https://blogs.nvidia.com/blog/physical-ai-halos-safety/>：`It's designed to support systems developed for standards including IEC 61508 and ISO 13849.`
- 為什麼值得花這 68 個字：文章第 5 段教讀者 IGX 用的是「支援」而非已取得認證，第 13 段又請讀者自己去看那一頁——不寫這一句，照做的讀者會在同一頁讀到相反的措辭，而文章沒有先提醒。研究紀錄 `must_not_write` 第 7 條要求兩個官方頁措辭不一致時兩邊都寫、以帶限定詞的版本為準；第一組（Halos OS 的 `safety-certified`）已經照做，第二組接在同一句後面最省字。

### 4. 正文第 12 段：刪掉第 6 段但書的重述（騰字數，其一）

- 原（段末）：`…還沒出貨——前面的「level 4-ready」車輛同樣是準備階段，非已載客上路的 4 級自駕車。`
- 改（段末）：`…還沒出貨。`
- **但書沒有被刪**：`level 4-ready` 的限定詞與「還不是已上路載客的 4 級自駕車」原文留在第 6 段，一個字都沒動；刪掉的是第 12 段回頭再講一次的那句。省 44 字。

### 5. 正文第 11 段：刪掉同一句裡重複的歸因（騰字數，其二）

- 原：`NVIDIA 自稱 Halos 是「the first and only full-stack safety system for physical AI」（意為：…），這是廠商自己的說法，本站沒有比較其他公司的方案。`
- 改：`NVIDIA 自稱 Halos 是「the first and only full-stack safety system for physical AI」（意為：…），本站沒有比較其他公司的方案。`
- **歸因沒有被刪**：「NVIDIA 自稱」留著，`must_not_write` 第 6 條要的界線句「本站沒有比較其他公司的方案」也留著；刪掉的是同一句裡把「自稱」再說一次的「這是廠商自己的說法」。省 10 字。

研究紀錄另外附加了 `factcheck.second_round`（`checked_by`／`checked_on`／`method`／`claims_checked`／`changes`／`open_questions`／`coordinator_rulings`／`verdict`），
兩個檔案都是文字插入（不是 `json.dump`）：LF、無 `\uXXXX` 跳脫、檔尾一個換行，`git diff` 各只有 5 行與一段純新增。

## 4. 覆核過而且正確的重點

- **四種強度沒有互相污染**：「已認證」只給自駕車端；「正在檢驗」保留 `is inspecting` 的進行式；「機構獲得認可」沒有被寫成產品認證；「設計上支援」保留 `designed to support` 與 `including`（舉例，非完整清單）。本輪新增的子句是在寫「兩個官方頁措辭有落差」，沒有把第四種強度升級。
- **限定詞全在**：`may require`、`level 4-ready`、`early access`、`will be`、`Emerging standards … are beginning to` 五個限定語在正文與 FAQ 裡都還在；本輪刪的兩處都不是限定詞。
- **歸因密度**（DELTA-4-7 §14）：開頭段 0 個歸因語，其餘每段最多 2 個（第 10 段 2 個），沒有一段超標。「本文」0 次。
- **兩個結尾連結**：第一個 text 與索引內容包的 zh-TW `title` 逐字相同（程式比對 True）；第二個與 DELTA-4-7 §7 的表逐字相同。本輪沒有動這兩個 block。
- **個資**：沒有請求部落格裡 Advantech 那個查詢字串夾帶個人 email 的 outlook safelinks 轉址網址；ANAB PDF 第 2 頁的聯絡人姓名與 email 沒有抄進任何檔案，這份報告與研究紀錄裡都沒有。Omdia 頁面抽出的文字裡有一個 `my@email.address`，那是該站表單的佔位字串，不是任何人的 email，也沒有被使用。

## 5. 留給協調者的事

1. ~~**正文現在有一次「評估」**（第 8 段 `third-party assessed` 的意譯）。~~ **已由協調者裁定結案**：意譯改成「經第三方查驗」，正文的「評估」回到 0 次。新標題〈已認證、檢驗中與機構認可是三件不同的事〉維持不動，而且仍然站得住：三種強度在正文與表格都指得出來，新增子句是在陳述廠商兩頁的措辭落差，不是第四種強度。
2. **`title_candidates[0]` 仍是含「評估」的舊標題**，第一輪與第二輪都沒動，留給協調者決定要不要同步。
3. **第一輪「四頁搜價格字串 0 筆」要修正**：兩個 nvidia.com 頁面各有 1 筆 `pricing`，在地區切換視窗那句 `Visit your regional NVIDIA website for local content, pricing, and where to buy partners…`，與「台灣 (Taiwan)」出現在同一塊版面。**文章的說法不受影響**（那是網站版面不是內容，文章講的是 NVIDIA 這篇文章沒有價格），不需要改字；但下一輪若再引用「0 筆」這個說法要重數。
4. **ABI 與 Omdia 的牆不是同一種**：Omdia 明寫 `A subscription is required to view this content.`；ABI 是登入牆，頁面把 `Full Reports` 列在 `Subscriber Content` 底下、頂上寫 `Log in now to access`。正文寫「兩份原始報告都要訂閱才讀得到」對得上，而且比寫死狀態碼耐放——這是活資料，之後再變還要再改。
5. **Digit 的型號落差維持第一輪的判斷**：部落格 `its Digit 5 humanoid`、機器人頁未來式那句只寫 `Digit, Agility's humanoid`。兩頁講同一台，正文寫「Digit 5」可接受，但嚴格說未來式那一句沒有印出型號。
6. **出圖**：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug（DELTA-4-7 §15 刻意保留給定稿後）。圖上四格與 `hero_label` 沒有任何數字，可以照現況畫。

## 6. 自檢輸出（原樣）

```
OK ai-news-nvidia-physical-ai-safety-20260921 zh-TW paragraphs 2996
```

```
ai-news-nvidia-physical-ai-safety-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-nvidia-physical-ai-safety-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-nvidia-physical-ai-safety-20260921/diagram-1.svg
1 entries checked
```

```
check_article.py exit=0
pack_cli lint exit=1
```

`image_missing` 與 `raw_internal_url` 是 FACTCHECK-47 明列、出圖與 relink 之前預期會有的兩種；除此之外沒有任何 FAIL。

## 7. 結論

**ok**。第一輪的 8 處編輯逐條回一手來源覆核後**全部成立**，新寫進去的 8 段字串也都撐得住。
第二輪自己找到的是**第一輪連動沒做完**（ANAB 持證者只改了正文與 FAQ，摘要與表格沒跟上）與**協調者點名的第二組措辭落差**，
三處都已修正，字數從兩處重複敘述騰出，2,996 ≤ 3,000，`check_article.py` 印 OK。
沒有留下需要站主裁定才能發的問題，§5 的六條都是可發之後再處理的選項或提醒。
