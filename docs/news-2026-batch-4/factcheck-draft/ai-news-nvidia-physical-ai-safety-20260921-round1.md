# `ai-news-nvidia-physical-ai-safety-20260921` 查核報告（第一輪）

- 查核者：independent factcheck agent, round 1（沒有參與撰稿）
- 查核日：2026-09-23
- 垂直／順序：AI，`display_order` 176，事件日 2026-09-21
- 內容包：`apps/api/app/guides/content/ai-news-nvidia-physical-ai-safety-20260921.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-nvidia-physical-ai-safety-20260921.json`
- 結論：**needs_second_round**（DELTA-4-7 第 12 條第一輪一律再跑第二輪；本輪改了 12 條主張、8 處編輯，其中標題與表格第一列動到骨幹表述）

## 1. 來源重抓結果（2026-09-23 台北）

四條都用 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1.5 秒；
UA、標頭、查詢字串、表單一律沒有帶入任何人的姓名、email 或個人資料。HTML 先刪 `<!-- -->` 註解、再 `html.unescape`、`&nbsp;` 換空白；
PDF 用系統 `python` 的 pypdf 抽文字（`apps/api/.venv` 沒有 pypdf）。

| # | URL | HTTP | bytes | 抽出正文 | 是否讀到正文 |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://blogs.nvidia.com/blog/physical-ai-halos-safety/` | 200 | 121,824 | 9,866 字元 | 是（從 `Physical AI is moving rapidly…` 到 `…separates a prototype from a scalable solution`） |
| 2 | `https://www.nvidia.com/en-us/ai-trust-center/physical-ai/safety-certification/` | 200 | 665,291 | 23,803 字元 | 是（含 Certification Program 與 Frequently Asked Questions 全文） |
| 3 | `https://search.anab.org/public/organization_files/NVIDIA-Corporation-Cert-and-Scope-File-06-06-2025_1749243349.pdf` | 200 | 434,445 | 6 頁／8,526 字元 | 是（證書＋五頁認可範圍） |
| 4 | `https://www.nvidia.com/en-us/ai-trust-center/halos/robotics/` | 200 | 761,431 | 36,411 字元 | 是（非 SPA 殼） |

- **四條的 bytes 與研究紀錄寫的完全相同**，而且把撰稿／研究代理 00:39–00:46 存下的 `_raw/<slug>/*.txt` 與我今天的抽文字**壓縮空白後逐字比對，四份一模一樣**（9,775／23,176／35,265／8,173 字元）。這段期間來源沒有改動，所有「截至查核當天」的狀態句今天仍然成立。
- 內容包裡 17 段英文逐字引文、研究紀錄 4 條 `sources[].verbatim_quote` 與 38 條 `verified_facts[].verbatim_quote`，全部以壓縮空白後的**連續子字串**比對命中，**0 失敗**；`verified_facts` 的 `url` 全都在 `sources[]` 裡。
- 另外重抓兩條**被排除**的預測報告連結，只用來核對正文對「讀不到」的描述，沒有拿來撐任何事實：
  `https://my.abiresearch.com/research/15976/` 200／17,744 bytes（登入牆：`Log in now to access` / `Subscriber Content ✓ Full Reports`）；
  `https://omdia.tech.informa.com/om146251/robotics-hardware-market-forecast--2026` **200／221,965 bytes**（訂閱牆：`A subscription is required to view this content.`）。
  研究紀錄記的是 403——**這一條本輪變了**，見改動 4。
- 沒有請求部落格裡 Advantech 那個 outlook safelinks 轉址網址（查詢字串夾帶個人 email）；ANAB PDF 第 2 頁的聯絡人姓名與 email 沒有抄進任何檔案，這份報告裡也沒有。
- 事件日：頁面自印 `September 21, 2026`，`article:published_time` 2026-09-21T16:00:46+00:00、`article:modified_time` 2026-09-21T16:06:14+00:00，JSON-LD 相同。依 DELTA-4-7 第 10 條**不換算**，維持 2026-09-21。

## 2. 主張表（124 條）

判定：C＝CONFIRMED、CH＝CHANGED、NF＝NOT FOUND（已改寫）。

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| 1 | title | 「評估」是三種說法之一 | **NF** | 全篇只有標題出現「評估」二字；正文與表格的四種說法是已認證／還在檢驗中／機構獲得認可／設計上支援。來源裡確有一項評估（`TÜV Rheinland also performed an independent UNECE safety assessment of NVIDIA DRIVE AV`），但這篇從頭到尾沒寫它 |
| 2 | title | 「認證」與「檢驗中」是不同的事 | C | 部落格同一段同時用 `certified` 與 `is inspecting` |
| 3 | title | 長度 36 字（需 ≤60） | C | checker |
| 4 | desc | 事件日 2026 年 9 月 21 日 | C | 頁面自印 `September 21, 2026` |
| 5 | desc | NVIDIA 在官方部落格說明實體 AI（自駕車與機器人）的安全 | C | `AVs, humanoid robots, industrial robots and more` |
| 6 | desc | 為什麼要橫跨硬體、軟體、AI 行為與運作環境 | C | `safety across the hardware, software, AI, operating environment and deployment lifecycle` |
| 7 | desc | 整理哪些已完成第三方認證、哪些還在檢驗中 | C | 文章 `How Is NVIDIA Halos Independently Assessed?` 一節 |
| 8 | desc | ANAB 認可的檢驗實驗室屬於哪種類別、效期到何時 | C | ANAB PDF |
| 9 | desc | 結尾只帶「（2026 年 9 月查證）」、沒有查證流水帳 | C | DELTA-4-7 §14 |
| 10 | desc | 長度 152 字（需 120–200） | C | checker |
| 11 | desc | 沒有放 4,900 萬／6,000 萬 | C | 指派表 A6 |
| 12 | P1 | 事件日 = slug 尾碼 = `news_date` = 第一段 | C | 三處都是 2026-09-21 |
| 13 | P1 | 文章標題〈Why Deploying Physical AI at Scale Demands Safety at Every Layer〉 | C | 頁面 H1 逐字 |
| 14 | P1 | 主張安全不能只靠部署前檢查一次 | C | `not a one-time check before deployment` |
| 15 | P1 | 要橫跨硬體到部署後的每個環節 | C | 同 #6 |
| 16 | P1 | 這類機器愈來愈常出現在生活周遭 | C | `As these machines enter roads, factories, warehouses and other environments shared with people` |
| 17 | P1 | 不是產品發表，沒有價格、上市日 | C | 四頁全文搜 `price`／`pricing`／`$`／`available now`／`general availability` 皆 0 筆 |
| 18 | P1 | 四個官方來源都沒提到台灣 | C | 部落格 0 筆、ANAB PDF 0 筆；兩個 nvidia.com 各 2 筆，分別在地區切換視窗（`United States / 대한민국 / 中国大陆 / 台灣 (Taiwan) / 日本`）與表單國家下拉（`Syria / Taiwan / Tajikistan`） |
| 19 | P1 | 正文沒有寫出任何發布時刻 | C | DELTA-4-7 §10 |
| 20 | P2 | 查核日 2026-09-23 | C | 與研究紀錄、四條 source、表格 caption、圖解 caption 五處一致 |
| 21 | P2 | 依據 NVIDIA 官方部落格 | C | source 1 |
| 22 | P2 | 「AI Trust Center 的兩個 Halos 頁面」 | C | 兩頁都在 `/ai-trust-center/` 下；認證頁的瀏覽器標題就是 `Certification for Safer Physical AI | NVIDIA Halos` |
| 23 | P2 | ANAB 核發的 ISO/IEC 17020 認可證書與範圍檔案 | C | `CERTIFICATE OF ACCREDITATION` ＋ `SCOPE OF ACCREDITATION TO ISO/IEC 17020:2012` |
| 24 | P2 | 規格與宣稱一律標明是 NVIDIA 自己的說法 | C | 見 #46、#78、#89 |
| 25 | 摘要1 | 橫跨硬體、軟體、AI 行為、運作環境與部署生命週期 | C | 同 #6 |
| 26 | 摘要1 | 不是部署前檢查一次就結束 | C | 同 #14 |
| 27 | 摘要2 | TÜV SÜD 把 DriveOS 6.0 與「相關工程流程」認證到 ISO 26262 ASIL D | **CH** | 原文是 `Automotive Product Lifecycle software process and DriveOS 6.0 to ISO 26262 ASIL D`；車用工程流程對應的是 ISO/SAE 21434 |
| 28 | 摘要2 | TÜV Rheinland 還在檢驗 IGX Thor、Halos OS、Holoscan Sensor Bridge，尚未完成 | C | `TÜV Rheinland is inspecting … for functional-safety certification readiness` |
| 29 | 摘要3 | 通過 ANAB 認可為 ISO/IEC 17020 檢驗機構 | C | `ANAB has accredited the NVIDIA Halos AI Systems Inspection Lab as an ISO/IEC 17020 inspection body` |
| 30 | 摘要3 | 登記類別 Type C（second party） | C | `TYPE C (SECOND PARTY) BODY` |
| 31 | 摘要3 | 檢驗方式是審閱文件 | C | `Verification of conformity of inspected items by review of documentation` |
| 32 | 摘要3 | 效期到 2027 年 1 月 2 日 | C | `Certificate Expiry Date: 02 January 2027` |
| 33 | 摘要3 | 最終系統級認證仍要由獨立第三方完成 | C | `helps companies prepare for final certification by independent third-party bodies` |
| 34 | 摘要4 | 認可在 80 個國家受承認、包含中國（NVIDIA 說法） | C | `recognized in 80 countries, including China` |
| 35 | 摘要4 | 四個官方頁面都沒提到台灣，無法推論 | C | 同 #18；ANAB PDF 無國家清單 |
| 36 | 摘要5 | Halos Core for IGX 只開放已註冊開發者早期存取 | C | `available in early access for registered developers` |
| 37 | 摘要5 | Digit 5 安全系統整合進行中、尚未出貨 | C | 部落格 `Agility is integrating…`；機器人頁 `will be the first production robot shipping with NVIDIA Halos OS` |
| 38 | 摘要 | 五句都沒有 4,900 萬／6,000 萬 | C | 指派表 A6 |
| 39 | 摘要 | 每個數字都在正文出現 | C | checker |
| 40 | §1 P1 | 「the hardware, software, AI, operating environment and deployment lifecycle」逐字 | C | 連續子字串命中 |
| 41 | §1 P1 | 理由有四個 | C | `Four shifts define new safety standards` |
| 42 | §1 P1 | 環境動態，工廠倉庫無法只靠靜態分區控制 | C | `Roads, factories and warehouses cannot be fully controlled through static zones or physical barriers` |
| 43 | §1 P1 | AI 行為需要保證機制 | C | `AI behavior requires its own assurance` |
| 44 | §1 P1 | ISO/IEC TS 22440 才剛開始處理 AI 特有風險 | C | `Emerging standards such as ISO/IEC TS 22440 are beginning to address these AI-specific risks`（限定語氣有保留） |
| 45 | §1 P1 | 「may require additional safety testing」（可能，非必然） | C | 逐字命中，括號註解正確 |
| 46 | §1 P1 | 情境複雜度高，測試要搭配模擬與合成資料 | C | `requires real-world testing to be combined with simulation, synthetic data generation and scenario reconstruction` |
| 47 | §1 P2 | 「市場研究機構」ABI Research | **NF** | 四條來源都沒有描述這兩家是什麼機構；已刪 |
| 48 | §1 P2 | 到「2035 年前」L3–L5 裝機量 4,900 萬台 | **CH** | 原文 `By 2035`；改為「到 2035 年」 |
| 49 | §1 P2 | Omdia：2026–2035 年「全球」約 6,000 萬台工業機器人 | **NF** | 原文 `roughly 60 million industrial robots will be deployed between 2026 and 2035`，沒有地理範圍；「全球」已刪 |
| 50 | §1 P2 | 這兩個數字是外部機構的預測，不是 NVIDIA 的承諾 | C | 部落格明白寫 `ABI Research projects` / `Omdia estimates` |
| 51 | §1 P2 | ABI 原始報告要付費訂閱 | C | 今日重抓 200／17,744 bytes 登入牆 |
| 52 | §1 P2 | 「Omdia 報告連結被拒絕存取」 | **CH** | 今日重抓回 **200／221,965 bytes**，頁面寫 `A subscription is required to view this content.`；改寫成「兩份原始報告都要訂閱才讀得到」 |
| 53 | §1 P2 | 引用的是 NVIDIA 部落格轉述的說法 | C | 研究紀錄 `unverified_or_excluded` 要求的框架 |
| 54 | §2 P1 | 「the platforms, standards and evidence remain specific to each domain」逐字 | C | 命中 |
| 55 | §2 P1 | Halos OS 建立在 ASIL-D 認證的 DriveOS 上 | C | `Halos OS provides a unified software foundation built on ASIL-D certified DriveOS` |
| 56 | §2 P1 | IGX Thor 帶專用功能安全島 | C | `with a dedicated Functional Safety Island` |
| 57 | §2 P1 | 「designed to support systems developed for standards including IEC 61508 and ISO 13849」逐字 | C | 命中 |
| 58 | §2 P1 | 用的是「支援」，非已取得認證 | C | must_not_write 的界線，文章有寫出來 |
| 59 | §2 P2 | Geely、Isuzu、Nissan 與 Einride 在 Hyperion 上打造 level 4-ready 車輛 | C | 逐字；文章沒寫成已上路的 L4 |
| 60 | §2 P2 | 「level 4-ready」還不是已上路載客的 4 級自駕車 | C | must_not_write |
| 61 | §2 P2 | Advantech 與 NexCOBOT 打造安全設計的 IGX 系統 | C | `Advantech and NexCOBOT build safety-designed NVIDIA IGX systems`；**沒有**寫成台灣公司（四頁都沒寫國籍） |
| 62 | §2 P2 | Agility 正整合 IGX Thor 與 Halos Core 進 Digit 5 | C | `Agility is integrating NVIDIA IGX Thor and Halos Core into the safety system for its Digit 5 humanoid` |
| 63 | 表格 r1 c2 | 「自駕車：DriveOS 6.0 與相關工程流程」 | **NF** | 與 #27 同源，已改寫 |
| 64 | 表格 r1 c3 | 「通過 ISO 26262 ASIL D、ISO/SAE 21434」 | **NF** | 等於說 DriveOS 6.0 也通過 ISO/SAE 21434；來源沒這樣寫，已拆開 |
| 65 | 表格 r1 c4 | 認定者 TÜV SÜD | C | 逐字 |
| 66 | 表格 r2 | 機器人：IGX Thor、Halos OS、Holoscan Sensor Bridge／檢驗認證準備度尚未完成／TÜV Rheinland | C | 逐字 |
| 67 | 表格 r3 | Halos AI Systems Inspection Lab／ISO/IEC 17020、Type C（second party）／ANAB | C | 部落格＋ANAB PDF |
| 68 | 表格 r4 | IGX Thor／支援 IEC 61508、ISO 13849 等標準，非已取得認證／NVIDIA 自述 | C | `including` 舉例式，文章有寫「等標準」 |
| 69 | 表格 | caption 100 字（≤200）、四列、四欄 | C | checker |
| 70 | §3 P1 | 「TÜV SÜD certified NVIDIA’s Automotive Product Lifecycle software process and DriveOS 6.0 to ISO 26262 ASIL D」逐字 | C | 命中 |
| 71 | §3 P1 | 也把車用工程流程認證到 ISO/SAE 21434 | C | `as well as NVIDIA’s automotive engineering processes to ISO/SAE 21434` |
| 72 | §3 P2 | 「TÜV Rheinland is inspecting NVIDIA IGX Thor, Halos OS and Holoscan Sensor Bridge for functional-safety certification readiness」逐字 | C | 命中 |
| 73 | §3 P2 | 機器人頁把 Halos OS 說成「safety-certified operating system foundation」 | C | 機器人頁逐字命中 |
| 74 | §3 P2 | 兩個官方頁措辭不一致，以「正在檢驗」為準 | C | must_not_write 要求兩邊都寫、以帶限定詞的為準——文章照做 |
| 75 | §3 P3 | ANAB 認可的不是任何一輛車或機器人，而是實驗室 | C | `ANAB has accredited the NVIDIA Halos AI Systems Inspection Lab as an ISO/IEC 17020 inspection body` |
| 76 | §3 P3 | 「讓它符合 ISO/IEC 17020、登記類別 TYPE C」 | **NF** | ANAB 的證書與範圍檔案從頭到尾沒有出現 `Halos AI Systems Inspection Lab`，持證者印的是 `NVIDIA Corporation`；已補上這一步 |
| 77 | §3 P3 | 「review of documentation」（審閱文件） | C | 逐字命中 |
| 78 | §3 P3 | 效期到 2027 年 1 月 2 日 | C | `Expiry Date: 02 January 2027`（證書頁與範圍頁各印一次） |
| 79 | §3 P3 | 實驗室補充既有認證工作，最終系統級認證由獨立第三方完成 | C | 認證頁 `complements existing certification efforts…`＋部落格 `independent third-party bodies` |
| 80 | 圖解 | caption 與研究紀錄 `diagram.caption` 逐字相同 | C | 程式比對 True |
| 81 | 圖解 | 四格：硬體層／軟體層／驗證層／檢驗報告 | C | 部落格分層與 `Simulation and validation` 一節 |
| 82 | 圖解 | 「檢驗報告不等於最終系統認證」 | C | 同 #79 |
| 83 | 圖解 | alt 與四格一致 | C | 逐字比對 |
| 84 | 圖解 | 圖上沒有任何數字 | C | 研究紀錄 `diagram`＋`hero_label` 掃描 0 個數字 |
| 85 | 研究紀錄 | `hero_label`「每一層都要留下證據」 | C | 部落格 `safety across … every layer`／`need evidence` |
| 86 | §4 P1 | 製造商、主管機關、保險業者與職場安全團隊都需要證據 | C | `manufacturers, regulators, insurers and workplace safety teams need evidence` |
| 87 | §4 P1 | 證明能在無人介入時安全運作 | C | `can work together safely without human intervention` |
| 88 | §4 P1 | 「recognized in 80 countries, including China」逐字 | C | 認證頁命中 |
| 89 | §4 P1 | 沒列完整名單，四頁也沒有台灣敘述，不可推論 | C | 同 #18、#35 |
| 90 | §4 P1 | 頁面偶爾出現的「台灣 (Taiwan)」是網站地區選單 | C | 認證頁第 88 行、機器人頁第 88 行同一塊地區切換視窗 |
| 91 | §4 P2 | 四個來源都沒有事故、召回或主管機關調查 | C | 部落格與認證頁 `accident/crash/recall/investigat/incident` 0 筆；機器人頁 1 筆是安全概念說明（`prevent incidents from occurring`），不是事故報導 |
| 92 | §4 P2 | 「the first and only full-stack safety system for physical AI」是 NVIDIA 自己的說法 | C | 逐字命中，文章寫「NVIDIA 自稱」 |
| 93 | §4 P2 | 本站沒有比較其他公司的方案 | C | 編輯聲明 |
| 94 | §5 P1 | 「early access for registered developers」逐字 | C | 機器人頁命中 |
| 95 | §5 P1 | 不是公開上市產品 | C | 同上，早期存取＋需註冊 |
| 96 | §5 P1 | 「will be the first production robot shipping with NVIDIA Halos OS」逐字、未來式 | C | 機器人頁命中 |
| 97 | §5 P1 | 前面的 level 4-ready 車輛同樣是準備階段 | C | 同 #60 |
| 98 | §5 P2 | 可到 AI Trust Center 的 Halos 頁面查目前元件 | C | 認證頁 Certification Program 一節、機器人頁元件清單 |
| 99 | §5 P2 | 從常見問題連到 ANAB 的證書與範圍檔案 | C | 認證頁 `Frequently Asked Questions` 裡 `Read the complete ANAB accreditation scope here.` |
| 100 | §5 P2 | 看得到版本號與效期 | C | `version 002, was last updated on: 06 June 2025`／`Expiry Date: 02 January 2027` |
| 101 | §5 P2 | 四種強度值得記住 | C | 與表格四列一致 |
| 102 | FAQ1 | 自駕車端已認證、機器人端還在檢驗 | C | 同 #70、#72 |
| 103 | FAQ1 | 也把車用工程流程認證到 ISO/SAE 21434 | C | 同 #71 |
| 104 | FAQ1 | 官方用的字是「正在檢驗」不是「已經認證」 | C | `is inspecting` |
| 105 | FAQ2 | ANAB 認可的是實驗室本身，不是替車、晶片或機器人核發認證 | C | 同 #75 |
| 106 | FAQ2 | 最終系統級認證仍要由獨立第三方完成 | C | 同 #33 |
| 107 | FAQ3 | 「依 ANAB 的證書檔案，這間實驗室登記的類別是 Type C」 | **NF** | 同 #76，已改寫成「證書與認可範圍檔案開給的是 NVIDIA Corporation」 |
| 108 | FAQ3 | Type C（second party）不是完全獨立的第三方 | C | 讀 ANAB 自己印的類別標籤，沒有自行解釋 Type A/B/C 的定義（研究紀錄禁止） |
| 109 | FAQ3 | 不代表檢驗結果不可信 | C | 沒有價值判斷，符合 must_not_write |
| 110 | FAQ4 | 兩個數字來自 ABI Research 與 Omdia，不是 NVIDIA 的承諾或出貨目標 | C | 同 #50 |
| 111 | FAQ4 | 「市場研究機構」「到 2035 年前」 | **NF／CH** | 同 #47、#48，已改 |
| 112 | FAQ4 | 「一份要付費訂閱、另一份的連結被拒絕存取」 | **CH** | 同 #52，已改 |
| 113 | FAQ5 | Halos Core for IGX 只開放已註冊開發者早期存取，支援 Linux 與 Linux 加 QNX | C | `in Linux and Linux plus QNX configurations` |
| 114 | FAQ5 | Digit 5 官方寫的是「將會是」 | C | 同 #96（機器人頁那句只寫 `Digit`，見待決事項 2） |
| 115 | FAQ5 | 完全沒有提到價格、上市日或台灣供貨時程 | C | 同 #17、#18 |
| 116 | FAQ6 | 四個官方頁面都沒有提到台灣；80 國沒有列出名單 | C | 同 #18、#35 |
| 117 | FAQ6 | 「台灣 (Taiwan)」是網站自己的地區選單 | C | 同 #90 |
| 118 | callout | 不是產品發表，沒有價格、上市日或台灣供貨時程 | C | 同 #17 |
| 119 | callout | 規模預測是 ABI Research 與 Omdia 兩家外部機構的說法 | C | 同 #50 |
| 120 | callout | 「原始報告查核當下都讀不到」 | C | 今天仍成立（兩份都在牆後） |
| 121 | callout | 四種強度用詞 | C | 與表格一致 |
| 122 | 結尾連結 | 第一個 text 與 `ai-news-2026-january-september-index` 的 zh-TW title 逐字相同 | C | 程式比對 True，且與 DELTA-4-7 §6 逐字一致 |
| 123 | 結尾連結 | 第二個 text 與 `ai-news-frontier-governance-20260528` 的 zh-TW title 逐字相同 | C | 程式比對 True，且與 DELTA-4-7 §7 逐字一致 |
| 124 | 研究紀錄 | `title` 與內容包 title 一致、`corrections_applied` 為 `[]`、`display_order` 176 | **CH** | title 已同步改新標題；其餘不動 |

**統計：124 條 → CONFIRMED 112、CHANGED 5、NOT FOUND（已改寫）7；沒有整句刪除的主張。**

## 3. 改了什麼（8 處編輯）

### 1. 標題：拿掉文章沒有交代的「評估」

- 原：`NVIDIA 談實體 AI 安全：認證、評估與檢驗中是三件不同的事`
- 改：`NVIDIA 談實體 AI 安全：已認證、檢驗中與機構認可是三件不同的事`
- 理由：全篇（正文、表格、FAQ、callout）只有標題出現「評估」兩個字，讀者在文章裡找不到它對應什麼。文章自己教的是四種強度——已認證／還在檢驗中／機構獲得認可／設計上支援——新標題取其中三種，每一種在正文都指得出來。來源裡確實有一項評估（`TÜV Rheinland also performed an independent UNECE safety assessment of NVIDIA DRIVE AV`，<https://blogs.nvidia.com/blog/physical-ai-halos-safety/>），但這篇沒有寫它，不能靠它撐標題。
- 連動：研究紀錄 `title` 已同步（`check_article.py` 會比對）。`title_candidates[0]` 仍是研究代理原本提的舊標題，**沒有動**，留給協調者決定。

### 2. 摘要第二句：ASIL D 的對象

- 原：`TÜV SÜD 已把 NVIDIA 的 DriveOS 6.0 與相關工程流程認證到 ISO 26262 ASIL D`
- 改：`TÜV SÜD 已把 NVIDIA 的 DriveOS 6.0 與車用產品生命週期軟體流程認證到 ISO 26262 ASIL D`
- 來源：`TÜV SÜD certified NVIDIA’s Automotive Product Lifecycle software process and DriveOS 6.0 to ISO 26262 ASIL D, as well as NVIDIA’s automotive engineering processes to ISO/SAE 21434.`（<https://blogs.nvidia.com/blog/physical-ai-halos-safety/>）
- 理由：ASIL D 的對象是「車用產品生命週期**軟體**流程」與 DriveOS 6.0；「車用工程流程」對應的是 ISO/SAE 21434。正文第 7 段本來就寫對，摘要與表格沒有跟上。

### 3. 表格第一列：兩個標準各自掛回自己的對象

- 原：`["已完成認證", "自駕車：DriveOS 6.0 與相關工程流程", "通過 ISO 26262 ASIL D、ISO/SAE 21434", "TÜV SÜD"]`
- 改：`["已完成認證", "自駕車：DriveOS 6.0、車用產品生命週期軟體流程與車用工程流程", "DriveOS 6.0 與產品生命週期軟體流程通過 ISO 26262 ASIL D；車用工程流程通過 ISO/SAE 21434", "TÜV SÜD"]`
- 理由：原本的寫法等於說 DriveOS 6.0 也通過了 ISO/SAE 21434，來源沒有這樣寫。表格是這篇的骨幹，這一列最容易被讀者當成結論抄走。

### 4. 兩個預測數字那一段：刪掉來源沒有的描述，並改掉已經不成立的取得狀態

- 原：`市場研究機構 ABI Research 預測，到 2035 年前 L3 至 L5 自駕車裝機量將達 4,900 萬台；Omdia 估計，2026 到 2035 年間全球約部署 6,000 萬台工業機器人。這兩個數字是外部機構的預測，不是 NVIDIA 的承諾；查核當下，ABI Research 原始報告要付費訂閱、Omdia 報告連結被拒絕存取，這裡引用的是 NVIDIA 部落格轉述的說法。`
- 改：`ABI Research 預測，到 2035 年 L3 至 L5 自駕車裝機量將達 4,900 萬台；Omdia 估計，2026 到 2035 年間約部署 6,000 萬台工業機器人。這兩個數字是外部機構的預測，不是 NVIDIA 的承諾；查核當下兩份原始報告都要訂閱才讀得到，這裡引用的是 NVIDIA 部落格轉述的說法。`
- 三件事：
  1. 「市場研究機構」四條來源都沒有寫，刪掉（原文只有 `ABI Research projects` / `Omdia estimates`）。
  2. 「全球」不在 Omdia 那句話裡：`roughly 60 million industrial robots will be deployed between 2026 and 2035`，沒有地理範圍。
  3. 「到 2035 年前」→「到 2035 年」，對齊 `By 2035`。
  4. **「Omdia 報告連結被拒絕存取」已不成立**：<https://omdia.tech.informa.com/om146251/robotics-hardware-market-forecast--2026> 今天回 200／221,965 bytes，頁面寫 `A subscription is required to view this content.`（研究紀錄當時是 403）。ABI 仍是登入牆。改成「兩份原始報告都要訂閱才讀得到」，既正確也比寫死狀態碼耐放。
- 歸因與年份都保留（指派表 A6、研究紀錄 `unverified_or_excluded` 的要求），標題與摘要仍然沒有這兩個數字。

### 5. FAQ 第四題：與第 4 處同一組問題

- 原：`…分別來自市場研究機構 ABI Research（預測到 2035 年前有 4,900 萬台…）…查核當下，兩份原始報告都讀不到，一份要付費訂閱、另一份的連結被拒絕存取…`
- 改：`…分別來自 ABI Research（預測到 2035 年有 4,900 萬台…）…查核當下兩份原始報告都要訂閱才讀得到…`

### 6. 正文第 9 段：ANAB 的證書開給誰

- 原：`…而是 NVIDIA 自家的檢驗實驗室 Halos AI Systems Inspection Lab，讓它符合 ISO/IEC 17020、登記類別「TYPE C (SECOND PARTY) BODY」…`
- 改：`…而是 NVIDIA 自家的檢驗實驗室 Halos AI Systems Inspection Lab；ANAB 的證書開給 NVIDIA Corporation，符合 ISO/IEC 17020，登記類別是「TYPE C (SECOND PARTY) BODY」…`
- 來源：ANAB 的證書與認可範圍檔案（<https://search.anab.org/public/organization_files/NVIDIA-Corporation-Cert-and-Scope-File-06-06-2025_1749243349.pdf>）六頁全文**沒有出現** `Halos AI Systems Inspection Lab` 這個名字，持證者印的是 `NVIDIA Corporation`（`The ANSI National Accreditation Board Hereby attests that NVIDIA Corporation … Fulfills the requirements of ISO/IEC 17020:2012`）。「實驗室被認可」是 NVIDIA 部落格的說法，「Type C（second party）」是 ANAB 檔案上的登記——把這一步補起來，這篇最重要的界線才站得住，而且更有力：認可掛在 NVIDIA 公司自己身上。

### 7. FAQ 第三題：同一件事

- 原：`依 ANAB 的證書檔案，這間實驗室登記的類別是 Type C（second party）…`
- 改：`ANAB 的證書與認可範圍檔案開給的是 NVIDIA Corporation，登記的檢驗機構類別是 Type C（second party）…`

### 8. 研究紀錄

- `title` 同步成新標題。
- 附加 `factcheck` 物件（`checked_by`／`checked_on`／`method`／`claims_checked`／`changes`／`open_questions`／`coordinator_rulings`）。
- 兩個檔案都是文字插入（不是 `json.dump`），LF、無 `\uXXXX` 跳脫、檔尾一個換行。

## 4. 查過而且正確的重點

- **不換算時刻**：`article:published_time` 2026-09-21T16:00:46+00:00 是整點排程佔位，文章第一段寫 2026 年 9 月 21 日、沒有出現任何時刻，slug 尾碼與 `news_date` 一致——DELTA-4-7 第 10 條照做。
- **四種強度沒有互相污染**：「已認證」只給自駕車端、「正在檢驗」保留 `is inspecting` 的進行式、「機構獲得認可」沒有寫成產品認證、「設計上支援」保留 `designed to support` 與 `including`（舉例，非完整清單）。
- **兩頁矛盾兩邊都寫**：機器人頁的 `safety-certified operating system foundation` 與部落格的「還在檢驗認證準備度」都寫進正文，並以帶限定詞的版本為準。
- **台灣的位置照實寫**：四頁都沒有台灣敘述，「台灣 (Taiwan)」只在地區切換視窗與表單國家下拉；文章沒有從「包含中國」往任何方向推論，也沒有把 Advantech、NexCOBOT 寫成台灣公司（四頁都沒寫國籍）。
- **沒有購買建議、沒有推薦式比價、沒有價格**：四頁搜不到價格字串，文章也沒有「值得買／該升級」這類句子；廠商宣稱（first and only、80 國、safety-certified）都有歸因。
- **狀態詞沒有被強化**：`level 4-ready`、`early access`、`will be`、`may require` 四個限定詞全部保留在正文與 FAQ 裡。
- **AI 垂直只有一個 callout**，沒有投資免責段落。
- **兩個結尾連結**的 text 與目標內容包的 zh-TW `title` 逐字相同（程式比對 True），也與 DELTA-4-7 §6／§7 的表逐字相同；本輪沒有動這兩個 block。
- **個資**：沒有請求部落格裡 Advantech 那個夾帶個人 email 的 safelinks 轉址網址；ANAB PDF 第 2 頁的聯絡人姓名與 email 沒有進任何檔案。

## 5. 讀者優先檢查（DELTA-4-7 §14）

- 「本文」出現 **0 次**；指涉自己用「這一篇」。
- 歸因密度：開頭段 1 個歸因語（`NVIDIA 在官方部落格發表`），其餘每段最多 2 個，**沒有一段超標**。第 4 段的 `ABI Research 預測`／`Omdia 估計` 是研究紀錄與指派表強制要求的歸因，不是贅語。
- `description` 沒有查證流水帳，句尾只帶「（2026 年 9 月查證）」；標題、`description`、摘要都沒有挑選筆數。
- 第一段就交代了跟讀者的關係：不是產品發表、沒有價格與上市日、四個官方來源都沒提到台灣。
- 「官方」全篇（正文＋FAQ＋callout）出現 **16 次**。歸因密度規則是過的，但若協調者要再壓低重複，那是文字調整、不是事實問題——本輪沒有動。

## 6. 留給協調者的事

1. **`title_candidates[0]` 沒有跟著改**，仍是含「評估」的舊標題。要不要同步由協調者決定。若不想要「認證／認可」這種形近詞，研究紀錄第三個候選「NVIDIA Halos 的安全分層：誰檢驗、檢驗到哪裡、哪些還沒完成」也完全撐得住。
2. **Digit 的型號**：部落格寫 `its Digit 5 humanoid`，機器人頁那句未來式寫的是 `Digit, Agility's humanoid`（沒有 5）。正文與 FAQ 把未來式那句掛在「Digit 5」上，是兩頁合併的結果。兩頁講的是同一台機器人，但嚴格說機器人頁沒有印出型號。
3. **第二組措辭落差**：機器人頁還有一句 `The NVIDIA IGX is a third-party assessed, safety-compliant System-on-a-Chip`，與部落格的 `designed to support … IEC 61508 and ISO 13849` 是另一組不一致（第一組是 Halos OS 的 `safety-certified`）。本輪沒有寫進正文；若第二輪覺得該補，字數要從別處挪（現在 2,982／3,000）。
4. **預測報告的取得狀態是活資料**：ABI 是登入牆、Omdia 這一輪已從 403 變成 200＋訂閱牆。正文現在寫「都要訂閱才讀得到」，比寫死狀態碼耐放，但若之後再變也要再改。
5. **出圖**：`build_assets.py` 的 `_DRAWINGS` 還沒有這個 slug（DELTA-4-7 §15 刻意保留給定稿後）。圖上四格與 `hero_label` 沒有任何數字，可以照現況畫。

## 7. 自檢輸出（原樣）

```
OK ai-news-nvidia-physical-ai-safety-20260921 zh-TW paragraphs 2982
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

## 8. 結論

**needs_second_round**。DELTA-4-7 第 12 條規定第一輪之後一律再跑第二輪；此外本輪改了 12 條主張（8 處編輯），其中標題、表格第一列與 ANAB 持證者三處動到骨幹表述，第二輪要逐句回一手來源重驗這些新寫進去的句子。
