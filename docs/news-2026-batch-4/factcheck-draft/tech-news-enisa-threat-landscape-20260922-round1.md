# 查核報告：tech-news-enisa-threat-landscape-20260922（第一輪）

- 查核者：第一輪獨立查核代理（Claude Opus 5, 1M context），沒有參與撰稿
- 查核日：2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-enisa-threat-landscape-20260922.json`
- 研究紀錄：`docs/tech-news-2026/research/tech-news-enisa-threat-landscape-20260922.json`
- 主張數 98：**CONFIRMED 73、CHANGED 14、NOT FOUND 0、OUT OF SCOPE 11**
- 結論：**needs_second_round**（事實改動 14 處，其中一處推翻了研究紀錄的前提）

---

## 1. 來源重抓（2026-09-23 01:31 台北）

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機之間間隔 2 秒。
**任何請求的 UA、標頭、查詢字串與表單都沒有帶入任何人的姓名、email 或其他個人資料。**

| # | 來源 | HTTP | bytes | 轉址 | 是否讀到正文 | 與撰稿代理 `_raw` 副本比對 |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | ENISA 新聞稿 | 200 | 62,053 | 0 | 是（Press Release／Sep 22,2026／Lepassaar 引述／五個小標／Analysis by threat categories 五條全在） | md5 相同 |
| S2 | ENISA 出版品頁 | 200 | 52,427 | 0 | 是（Publication date: September 22, 2026、PDF 下載連結、Language 只有 EN） | md5 相同 |
| S3 | 報告全文 PDF | 200 | 8,377,315 | 0 | 是（`%PDF-1.7`、pypdf 抽出 101 頁、250,702 字元） | md5 相同，抽出的文字逐位元組相同 |

三條都讀得到正文，沒有換版（`live_data_warnings` 第 2 條提醒的 bytes 比對通過）。
PDF 用**系統 python 的 pypdf**重抽（venv 沒有 pypdf），沒有沿用撰稿代理的 `etl2026.txt` 當作判準，而是拿自己抽的那一份做全文檢索，再與它比對確認一致。

---

## 2. 主張逐條核對

判準：CONFIRMED＝在今天自己抓到的原文裡找得到支撐句；CHANGED＝已修；NOT FOUND＝找不到支撐（改寫或刪除）；OUT OF SCOPE＝編輯判斷／寫作風格，非事實。
「報告 p.N」指 PDF 第 N 頁（本報告的頁碼＝PDF 頁序＝報告自印頁碼）。

### 標題與 description

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 1 | 標題「ENISA 公布 2026 威脅全景報告：統計的是 2025 一整年的事件」 | 名稱 ETL 2026、期間 2025-01-01～12-31（S2、報告 p.9） | CONFIRMED |
| 2 | 2026 年 9 月 22 日 ENISA 發布《ENISA Threat Landscape 2026》報告 | S2「Publication date: September 22, 2026」、S1「Sep 22,2026」 | CONFIRMED |
| 3 | 統計的是 2025 年 1 月至 12 月 | S1／S2「observed from 1 January to 31 December 2025」 | CONFIRMED |
| 4 | 範圍在歐盟的 8,257 起事件 | 報告 p.9「collected and analysed 8 257 incidents」 | CONFIRMED |
| 5 | 「60.4% 利用漏洞」分母只有 5.2% —— **原文寫成「新聞稿」的數字** | 報告 p.12 寫 5.2%／60.4%；S1 寫的是 5%／60% | **CHANGED（C1）** |
| 6 | description 以「（2026 年 9 月查證）」收尾、無挑選數量 | DELTA-4-7 第 14 條 | CONFIRMED |

### summary 四句

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 7 | 2026-09-22 同日發布報告與新聞稿 | S1、S2 | CONFIRMED |
| 8 | 範圍是歐盟會員國與設在歐盟的組織 | 報告 p.10「snapshot of threats faced by EU MSs and EU-based organisations」 | CONFIRMED |
| 9 | 報告名稱寫 2026、統計 2025 全年 8,257 起 | 報告 p.9 | CONFIRMED |
| 10 | 新聞稿寫「60% 是利用漏洞」 | S1 逐字 | CONFIRMED |
| 11 | 分母是能判定入侵途徑的未授權存取事件、報告寫 5.2%、其中 60.4% | 報告 p.12 逐字 | CONFIRMED |
| 12 | 以件數看 DDoS 最常見、51.3% | 報告 p.11「DDoS remain the primary incident type (51.3%)」 | CONFIRMED |
| 13 | 金錢動機活動 29.3%、特別是勒索軟體、短期衝擊最大 | 報告 p.7 | CONFIRMED |
| 14 | 2025 年攻擊者主要用消費級 AI 工具增強既有技能，非突破性能力 | 報告 p.15 | CONFIRMED |
| 15 | 對 2026 年是「可能」等級的前瞻評估、不是已發生 | 報告 p.8／p.96、Appendix B（p.100） | CONFIRMED |

### 正文第一節（P01–P06）

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 16 | 2026-09-22 同一天發布新聞稿與報告 | S1、S2 | CONFIRMED |
| 17 | 報告 101 頁 | 自己抓的 PDF，pypdf 計 101 頁 | CONFIRMED |
| 18 | 範圍是歐盟會員國與設在歐盟的組織 | 報告 p.10 | CONFIRMED |
| 19 | 查核日 2026 年 9 月 23 日 | 本輪重抓日與研究紀錄 `checked_on` 一致，未更動 | CONFIRMED |
| 20 | 讀的是新聞稿、出版品頁與報告全文 PDF | 與 `sources[]` 三條一致 | CONFIRMED（但見第 5 節的讀者優先意見） |
| 21 | 本站沒有做任何測試、不做資安產品或服務推薦 | 編輯聲明 | OUT OF SCOPE |
| 22 | **三條來源都沒有提到台灣、台灣的機關或台灣的企業** | 報告 p.78 出現 Taiwan 兩次 | **CHANGED（C2）** |
| 23 | 報告名稱 2026、分析期間 2025-01-01～12-31 | 報告 p.9 | CONFIRMED |
| 24 | **「新聞稿與報告本文用的是同一句話交代」** | 該句只在 S1 與 S2，報告全文 0 次 | **CHANGED（C3）** |
| 25 | 說成「2026 年的威脅」「今年的攻擊」是誤讀 | 依 23 推得的編輯判斷 | OUT OF SCOPE |
| 26 | 觀察期改成曆年制 | 報告 p.9 | CONFIRMED |
| 27 | 與上一版有六個月重疊 | 報告 p.9「an overlap of six months with the previous ETL」 | CONFIRMED |
| 28 | 擴大追蹤的網路犯罪活動範圍，新增資料外洩與詐騙 | 報告 p.9 | CONFIRMED |
| 29 | **這些改變都會影響報告裡的數字（漏了報告自己的但書）** | 報告 p.9 同句還有「did not substantially change the trends and rankings」 | **CHANGED（C4）** |
| 30 | 這一篇不寫「比去年增加／減少」 | 編輯判斷，與 `must_not_write` 第 6 條一致 | OUT OF SCOPE |
| 31 | **唯一的年增數字是「全球」新發布的 CVE 成長 22%** | 報告 p.90 沒有印地理範圍（同章寫 DDoS 才有「At a global level」） | **CHANGED（C5）** |
| 32 | 這一版共分析 8,257 起事件 | 報告 p.9 | CONFIRMED |
| 33 | 資料來自三個管道：公開來源、會員國匿名分享、Cyber Partnership Programme | S1 逐字（報告 p.9 版本多一個「mainly」） | CONFIRMED |
| 34 | 這個總數只印在報告方法論，新聞稿沒有寫 | 報告 p.9「Methodology」章；S1 全文檢索 8 257／8257／8,257 皆 0 次 | CONFIRMED |
| 35 | 公開來源與自願分享的資訊不構成完整圖像 | 報告 p.9 逐字 | CONFIRMED |
| 36 | 應被當成主流趨勢的概觀、一張快照 | 報告 p.10 逐字 | CONFIRMED |
| 37 | 新聞稿主張：相依關係擴大攻擊面、需要新一層級的警覺 | S1 逐字 | CONFIRMED |
| 38 | **這句話寫在新聞稿的「標題」** | HTML 裡是 `div.quote-wrapper` 的前言段；標題是「Exploring the evolution…」 | **CHANGED（C6）** |
| 39 | 這是 ENISA 對整份報告下的總結 | S1 前言段的位置與語氣 | CONFIRMED |
| 40 | 「下面先說明兩個統計陷阱」的導引 | 結構語 | OUT OF SCOPE |

### 正文第二節（P07–P09）與表格

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 41 | DDoS 是件數最多的事件類型、51.3% | 報告 p.11、p.12、p.7；S1 寫 51% | CONFIRMED |
| 42 | DDoS 主要由地緣政治情勢與政治聲明之類的特定事件帶動 | S1 逐字 | CONFIRMED |
| 43 | 件數其次是未授權存取、39.5% | 報告 p.11「followed by unauthorised access (39.5%)」 | CONFIRMED |
| 44 | 金錢動機活動占所有紀錄事件 29.3%、特別是勒索軟體、短期衝擊最大 | 報告 p.7 逐字 | CONFIRMED |
| 45 | 新聞稿：勒索軟體仍是短期衝擊最大的事件類型 | S1 逐字（該句在報告全文 0 次，本篇已標明出自新聞稿） | CONFIRMED |
| 46 | 被鎖定最多的部門是公共行政、31.8% | 報告 p.13、p.18、p.20 | CONFIRMED |
| 47 | 該部門 81.8% 的紀錄事件是意識形態驅動的 DDoS | 報告 p.20 | CONFIRMED |
| 48 | 「也就是網站被灌爆，不是被入侵」 | 報告 p.20「Public-facing websites and portals … repeatedly targeted」 | CONFIRMED |
| 49 | 表格列 1：DDoS／51.3%／件數最多、多屬短時間灌爆、衝擊通常有限 | 報告 p.12「low-impact DDoS attacks」；S1「low-impact」 | CONFIRMED |
| 50 | 表格列 2：未授權存取／39.5%／件數第二多 | 報告 p.11 | CONFIRMED |
| 51 | **表格列 3：金錢動機（含勒索軟體）／29.3%／與前兩列並列成同一軸的「事件類型」** | 29.3% 是「assessed objectives」動機軸（報告 p.7、p.13），與事件類型軸重疊 | **CHANGED（C7）** |
| 52 | 表格 caption：依報告執行摘要整理、查核日 2026-09-23 | 51.3%／39.5%／29.3% 三個數字都在報告 p.7 執行摘要 | CONFIRMED |

### 正文第三節（P10–P12）與圖解

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 53 | 新聞稿最容易被誤讀的一句是「60% 是利用漏洞」 | S1 逐字 | CONFIRMED |
| 54 | 分母是 ENISA 能判定入侵途徑的那一小部分未授權存取事件 | 報告 p.12、S1 | CONFIRMED |
| 55 | 新聞稿寫 5%／60% | S1 逐字 | CONFIRMED |
| 56 | 報告寫 5.2%／60.4% | 報告 p.12 逐字 | CONFIRMED |
| 57 | **「母數本身就只有整體的 5.2%」** | 來源只寫 `(5.2%)`，沒有寫這 5.2% 的基數是什麼 | **CHANGED（C8）** |
| 58 | 不能讀成「六成入侵都是漏洞造成」 | 依 54–56 推得 | CONFIRMED |
| 59 | 國家關聯入侵行動只有 20% 判定得出最初入侵途徑 | 報告 p.60 逐字 | CONFIRMED |
| 60 | 那 20% 的子集合裡 70% 是利用漏洞 | 報告 p.60 逐字 | CONFIRMED |
| 61 | 「比例很高不代表母數很大」的讀法 | 編輯歸納 | OUT OF SCOPE |
| 62 | **報告「在附錄裡」承認蒐報粒度、時序、部門歸類的偏誤** | 這三項在 p.9「Methodology」章；Appendix B（p.100）是可能性用語表 | **CHANGED（C9）** |
| 63 | 偏誤及於「公開來源與自願分享的資訊」 | 報告 p.9 寫的是「inherent to open-source reporting」 | **CHANGED（同 C9）** |
| 64 | 圖解 alt：2025 全年、8,257 起、60.4% 分母只有 5.2%、公共行政 31.8% | 報告 p.9／p.12／p.20 | CONFIRMED |
| 65 | 圖解 caption 與研究紀錄 `diagram.caption` 逐字相同 | `check_article.py` 通過 | CONFIRMED |

### 正文第四節（P13–P15）

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 66 | 2025 年新公布並取得 CVE 編號的漏洞超過 4.8 萬個 | 報告 p.90 逐字；S1 同 | CONFIRMED |
| 67 | 比前一年增加 22% | 報告 p.90、S1 | CONFIRMED |
| 68 | **這是「全球的 CVE 發布量」** | 報告 p.90 沒有印地理範圍 | **CHANGED（同 C5）** |
| 69 | 71% 的已記載漏洞把攻擊向量標為 Network | 報告 p.91 逐字 | CONFIRMED |
| 70 | 也就是有可能被遠端利用 | 報告 p.91「potential risk of remote exploitation」 | CONFIRMED |
| 71 | 對直接連上網際網路的服務與裝置風險最高 | 報告 p.91「especially for internet-facing systems」 | CONFIRMED |
| 72 | 「先檢查暴露在網路上的東西」的歸納 | 編輯歸納，正文已標明 | OUT OF SCOPE |
| 73 | 讀者做法清單是編輯整理、不是 ENISA 列出的待辦 | 正文自陳，且報告確實沒有這種清單 | CONFIRMED |
| 74 | 美國 CISA 把三個 Linux 核心漏洞列進「已遭利用」清單 | 第二個連結目標文章（已發布）與 `overlaps_existing_article` | CONFIRMED |
| 75 | 正文不含 CVE 編號與設備品牌型號 | 內容包全文檢索：`CVE-\d{4}-\d+` 0 筆；Zyxel／D-Link／Huawei／Netgear／Realtek／DASAN 皆 0 | CONFIRMED |

### 正文第五節（P16–P19）

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 76 | 針對供應鏈與第三方的攻擊持續被觀察到、期間有多起大規模或高衝擊例子 | 報告 p.12 逐字 | CONFIRMED |
| 77 | 熱門函式庫與 npm 套件遭入侵的情況增加 | 報告 p.12 逐字 | CONFIRMED |
| 78 | 報告舉 Shai-Hulud 行動為例 | 報告 p.12 | CONFIRMED |
| 79 | ENISA 於 2026 年 3 月發布套件管理器安全使用的技術建議 | 報告 p.12 逐字 | CONFIRMED |
| 80 | 報告只提到有這份建議、沒有說明內容 | 報告 p.12 僅一句＋腳註（腳註網址在抽文字時被截斷，本輪未抓） | CONFIRMED |
| 81 | 威脅類別之間的界線持續模糊 | S1 逐字 | CONFIRMED |
| 82 | 類似技術／基礎設施／存取機制重複出現在三類通報 | S1 逐字 | CONFIRMED |
| 83 | **「這也呼應報告開頭的主張：相依關係擴大攻擊面……」** | 該句在報告全文 0 次（「expand the attack surface」「new level of vigilance」各 0 次），只在 S1 | **CHANGED（C10）** |
| 84 | 2025 年攻擊者主要用消費級 AI 工具增強既有技能、調整攻擊向量 | 報告 p.15 逐字 | CONFIRMED |
| 85 | 報告揭露只在有限範圍內用 AI 支援資料蒐集與處理 | 報告 p.4 DISCLAIMER 逐字 | CONFIRMED |
| 86 | 所有產出經人員審閱驗證、報告內沒有 AI 生成內容 | 報告 p.4「reviewed and validated by subject-matter experts」 | CONFIRMED |
| 87 | **「對 2026 年，ENISA 的評估轉趨謹慎」** | 同一段 p.8 另寫 AI「will **highly likely** increasingly support malicious operations」，沒有轉趨謹慎這回事 | **CHANGED（C11）** |
| 88 | likely 在報告定義為 60%–90% 的信心水準 | Appendix B（p.100）「LIKELY Moderate to high confidence. 60 - 90%」 | CONFIRMED |
| 89 | 2026 年可能看到攻擊鏈更多階段直接由 AI 驅動 | 報告 p.8／p.96 逐字 | CONFIRMED |
| 90 | 可能出現人不在迴路內的概念驗證實驗 | 報告 p.8「possible experimentation of Human-out-of-the loop proof of concepts」 | CONFIRMED |

### FAQ、callout、來源與結尾連結

| # | 主張 | 判準來源 | 判定 |
| --- | --- | --- | --- |
| 91 | FAQ1：報告講的不是 2026 年的事、是 2025 全年 8,257 起 | 報告 p.9 | CONFIRMED |
| 92 | **FAQ2：報告與新聞稿都沒有提到台灣** | 報告 p.78 兩次 Taiwan | **CHANGED（同 C2）** |
| 93 | FAQ2：這份報告沒有替任何人新增法律義務 | 全文沒有義務性條文，S1／S2 亦無；與 `not_said` 第 2 條一致 | CONFIRMED |
| 94 | FAQ3：60%／5% 的分母說明 | 同 53–56 | CONFIRMED |
| 95 | FAQ4：不是法規、不是指引，NIS2 的義務來自指令本身 | 報告 p.18 只引 NIS2 作比較 | CONFIRMED |
| 96 | FAQ5：DDoS 51.3% 件數最多但衝擊有限；29.3% 金錢動機才是短期衝擊最大 | 報告 p.7、p.12；S1 | CONFIRMED |
| 97 | **FAQ7：CC BY 4.0「代表可以自由公開流通與再利用」／「每一個數字都可以翻到報告裡核對」** | 報告 p.2 的授權有「provided appropriate credit is given and any changes are indicated」，p.3 封面圖版權屬第三方；本篇的 5%／60% 只在新聞稿 | **CHANGED（C12）** |
| 98 | callout 六句（三份來源、2025 資料年、22% 例外、台灣、不含 CVE／型號、新聞稿與報告數字對不上一律採報告） | 各句對應上列；台灣句與「全球」句同 C2／C5 | **CHANGED（C13、C14）**，其餘 CONFIRMED |

另外逐字核對（不計入 98 條，因為是機械比對）：

- `sources[]` 三條的 `url`、順序與研究紀錄一致，`checked_on` 三條都是 `2026-09-23`，與研究紀錄相同——本輪重抓日就是同一天，依規格**沒有更動**。
- 第一個結尾連結 text 與 `tech-news-2026-index.json` 的 zh-TW `title` 逐字相同。
- 第二個結尾連結 text 與 `tech-news-cisa-kev-linux-kernel-20260918.json` 的 zh-TW `title` 逐字相同（程式比對 `==` 為 True），網址與 DELTA-4-7 第 7 條相同。
- 事件日一致性：slug 尾碼 `20260922`＝`news_date` `2026-09-22`＝第一段「2026 年 9 月 22 日」。
- `hero.alt` 依規格未查、未改。

---

## 3. 改掉的 14 處（before → after）

**C1 — description 把報告的數字說成新聞稿的**
- before：`新聞稿「60.4% 利用漏洞」的分母其實只有 5.2%`
- after：`報告「60.4% 利用漏洞」的分母其實只有 5.2%`
- 來源：報告 p.12「…(5.2%), 60.4% were seen leveraging a vulnerability…」；新聞稿印的是 5%／60%。
  <https://www.enisa.europa.eu/sites/default/files/2026-09/ENISA%20Threat%20Landscape%202026_Final.pdf>
- 為什麼：這篇文章的主軸就是「哪個數字出自哪裡」，descripton 自己把出處寫反，是最不能留的一種錯。

**C2 — 台灣：報告其實提到了（正文第二段、FAQ2、callout 三處）**
- before（正文）：`以 2026 年 9 月 23 日查核，這份報告與新聞稿都沒有提到台灣、台灣的機關或台灣的企業。`
- after（正文）：`報告統計的是歐盟會員國與設在歐盟的組織，沒有任何台灣機關或企業的事件；新聞稿與出版品頁沒有提到台灣，報告全文只有一處寫到台灣——在直接取材自歐盟對外事務部（EEAS）資訊操弄報告的那一章，台灣與香港、新疆、西藏被列為中國相關敘事經常出現的題目。`
- 來源：報告 p.78（第 5 章 FIMI，ENISA 自陳整章「directly drawn from the EEAS 4th report on Foreign Information Manipulation and Interference, published in March 2026」）：
  「The so-called big four topics (Taiwan, Hong Kong, Xinjiang and Tibet) featured heavily…」與
  「Hong Kong, Taiwan and the situation in the South China Sea were used in conjunction with promoting China's concepts and views on sovereignty and territorial claims.」
  <https://www.enisa.europa.eu/sites/default/files/2026-09/ENISA%20Threat%20Landscape%202026_Final.pdf>
- 為什麼：研究紀錄 `not_said` 第 1 條與 `must_not_write` 第 15 條都寫「三條來源都沒提到台灣」，並據此規定正文只能寫「未見任何關於台灣的內容」。本輪對 101 頁全文做大小寫不敏感檢索，`Taiwan` 出現 2 次（`Taipei` 0 次），兩次都在 p.78。對台灣讀者來說，這正好是整份報告裡唯一直接寫到台灣的地方，寫成「沒有提到」既不準確、也剛好漏掉最相關的一段。改寫照原文中性轉述「被列為敘事題目」，不做任何實質判斷，也沒有引用該章的其他統計。同一段落的 FAQ2 與 callout 同步改。

**C3 — 「同一句話交代」的出處**
- before：`新聞稿與報告本文用的是同一句話交代`
- after：`新聞稿與出版品頁用的是同一句話交代`
- 來源：`To shape our understanding of the cyber threat landscape…observed from 1 January to 31 December 2025…` 在新聞稿與出版品頁各 1 次，在報告 PDF **0 次**（報告 p.9 用的是另一句「The reporting period of the ETL has been updated to the calendar year…」）。
  <https://www.enisa.europa.eu/publications/enisa-threat-landscape-2026>
- 附帶：這一改也把正文裡唯一的「本文」兩字消掉了（DELTA-4-7 第 14 條）。

**C4 — 補回報告自己的但書**
- before：`這些改變都會影響報告裡的數字。`
- after：`這些改變都會影響報告裡的數字（報告同時寫明，這並沒有實質改變趨勢與排名）。`
- 來源：報告 p.9「While this was observed to have an impact on the numbers presented in this report, **it did not substantially change the trends and rankings observed in the previous iteration.**」
- 為什麼：原句只取前半、把來源往「所以數字不可信」的方向加強了一格。不比較年增減的理由仍然成立（六個月重疊），但限定詞要還回去。

**C5 — CVE 22% 的「全球」（正文兩處＋callout 一處）**
- before：`是全球新發布的 CVE 數量成長 22%，那是全球的漏洞公告量，不是歐盟的事件數` ／ `因為它算的是全球的 CVE 發布量` ／ `除了全球 CVE 發布量的年增 22%`
- after：`是 2025 年新發布並取得 CVE 編號的漏洞成長 22%，那是漏洞公告的數量，不是 ENISA 蒐集的歐盟事件數` ／ `因為它算的是 CVE 編號的公布量` ／ `除了 CVE 公布量的年增 22%`
- 來源：報告 p.90 第 7 章「Overall, more than 48 thousand new vulnerabilities were published in 2025…a 22% increase from the previous year.」——沒有寫地理範圍；同一章講 DDoS 時倒是明寫「At a global level」（p.89）。
- 為什麼：文章是靠「這個數字不是歐盟事件數」來正當化唯一的年增比較，這個對比來源撐得住；「全球」這個範圍詞來源沒印，而這一篇通篇在教人看分母與範圍，自己不能多加一個。

**C6 — 新聞稿那句話的位置**
- before：`新聞稿在標題主張：2026 年版威脅全景報告確認，`
- after：`新聞稿開頭第一句就主張：2026 年版威脅全景報告確認，`
- 來源：新聞稿 HTML 裡該句在 `<div class="quote-wrapper"><p>`，標題（`<h1>`／麵包屑）是「Exploring the evolution of the cyber threat landscape: How dependencies weaken our digital resilience」。
  <https://www.enisa.europa.eu/news/exploring-the-evolution-of-the-cyber-threat-landscape-how-dependencies-weaken-our-digital-resilience>

**C7 — 表格第三列不是同一個分類軸**
- before：`["金錢動機（含勒索軟體）", "29.3%", "件數不是最多，卻是短期衝擊最大的類型"]`
- after：`["金錢動機的活動（含勒索軟體）", "29.3%", "依動機分類，與上兩列不同軸、會互相重疊；件數不是最多，卻是短期衝擊最大"]`
- 來源：報告 p.13「Based on **assessed objectives** … ideology-driven (57.3%), financially motivated (29.2%)…」；p.13 另寫未授權存取那 39.5% 裡有 63.9% 是金錢動機——兩軸明確重疊。
- 為什麼：51.3%＋39.5%＋29.3%＝120.1%，同一欄「以件數看的占比」下並列會讓讀者以為三者互斥。這一篇的主題就是分母，表格不能自己犯這個錯。

**C8 — 5.2% 的基數來源沒有寫**
- before：`母數本身就只有整體的 5.2%`
- after：`母數本身只有 5.2%`
- 來源：報告 p.12 只寫 `(5.2%)`，沒說是「占全部事件」還是「占未授權存取事件」；同一份報告 p.60 的對照例子反而寫得出來（「in only 20% of the recorded incidents」）。
- 為什麼：原句把括號裡的比例指定成「整體的」，是自己補的基數。同段也順手把三個歸因短語收成兩個（FACTCHECK-47 的歸因密度規定）。

**C9 — 偏誤那段在方法論，不在附錄；限定詞範圍也不同**
- before：`報告自己在附錄裡也承認，公開來源與自願分享的資訊本來就有蒐報粒度、時序與部門歸類上的偏誤。`
- after：`報告在方法論那一節也寫明，公開來源的通報本來就有蒐報粒度、時序與部門歸類上的偏誤。`
- 來源：報告 p.9 標題就是「Methodology」，該段寫「multiple caveats are inherent to **open-source reporting**. Those notably include reporting granularity and temporality… Another caveat concerns proper sectoral categorisation」；報告的 Appendix A 是執法行動、Appendix B 是可能性用語表（p.97、p.100），都沒有這段。

**C10 — 「相依關係擴大攻擊面」是新聞稿的話，不是報告開頭的話**
- before：`這也呼應報告開頭的主張：數位相依關係擴大了攻擊面`
- after：`這也呼應新聞稿開頭的主張：數位相依關係擴大了攻擊面`
- 來源：`expand the attack surface` 與 `new level of vigilance` 在報告 101 頁全文各 0 次，只在新聞稿。同一篇文章的第六段已經正確地把它歸給新聞稿，這裡自相矛盾。

**C11 — ENISA 對 2026 年不是「轉趨謹慎」**
- before：`對 2026 年，ENISA 的評估轉趨謹慎：報告寫「可能」`
- after：`對 2026 年，報告給的是一句有保留的預測：寫「可能」`
- 來源：報告 p.8 同一段先寫「ENISA assess artificial intelligence will **highly likely**（>90%）increasingly support malicious operations」，再用 likely（60–90%）寫攻擊鏈那一句。措辭有保留是事實，「評估轉趨謹慎」是替 ENISA 加上的態度。

**C12 — CC BY 4.0 的條件與「每一個數字」**
- before：`報告採 CC BY 4.0 授權、標記 TLP:CLEAR，代表可以自由公開流通與再利用；……這一篇引用的每一個數字都可以自己翻到報告裡核對。`
- after：`報告標記 TLP:CLEAR、採 CC BY 4.0 授權，代表可以自由公開流通，再利用時要標示來源並註明有沒有改動（封面圖除外，版權屬第三方）；……這一篇引用的數字都可以自己翻到報告或新聞稿裡核對。`
- 來源：報告 p.2「reuse is allowed, **provided appropriate credit is given and any changes are indicated**」、p.3「Copyright for the image on the cover © Shutterstock」。另外本篇引用的 5%／60% 只印在新聞稿，翻報告找不到。

**C13／C14 — callout 的台灣句與「全球」句**：與 C2、C5 相同的兩處，已同步改；callout 其餘句子（三份來源、2025 資料年、不含 CVE 編號與型號、新聞稿數字對不上一律採報告）逐條核對後保留。

### 一併更正的研究紀錄（同一輪，見記錄的 `factcheck` 欄位）

1. `not_said` 第 1 條與 `must_not_write` 第 15 條的「三條來源都沒提到台灣」——更正並標明報告 p.78。**這一條如果不改，第二輪很可能會把正文改回錯的那句。**
2. `not_said` 第 6 條「沒有點名任何一個廠牌的產品有漏洞，也沒有給任何 CVE 編號」——報告 p.90 點名 D-Link、Zyxel、DASAN、Huawei、Realtek、Netgear 的未修補老舊 IoT／邊緣裝置，全文含 **38 組** CVE 編號。報告沒有的是「待修清單」那種形式。本篇按分工仍然不寫任何 CVE 編號與機型，但研究紀錄的事實敘述要對。
3. `not_said` 第 4 條與 `verified_facts` 第 35 條的「全球 CVE 的量」——同 C5。
4. `summary` 末句「全文沒有提到台灣」——同 C2。

---

## 4. 界線檢查（`tech.md`）

- 購買建議／推薦式比價：**沒有**。第四節那段讀者做法只講「把對外服務排進固定檢查清單」，沒有提任何產品、廠牌或價格，而且自陳是編輯整理。
- 沒有歸因的廠商宣稱：**沒有**。ENISA 的每個比例在正文都帶著「報告寫」「ENISA 統計」之類的來源；本輪反而是把過多的歸因收掉（C8 那段）。
- 缺「預告／草案／分批開放」狀態的句子：**沒有**。文章明寫這是情勢分析、不是法規、不新增義務（FAQ4、callout），也沒有把 2026 年的 likely 評估寫成已發生（C11 改後更清楚）。
- 可操作的攻擊細節、入侵指標、CVE 編號、設備型號：**沒有**（機械檢查：`CVE-\d{4}-\d+` 0 筆、六個廠牌名 0 筆）。
- 免責 callout：科技篇只有一個 info callout，沒有多出投資免責段落。
- 最高級（「首次」「史上最多」）：**沒有**。

## 5. 讀者優先（DELTA-4-7 第 14 條）的意見

- **「本文」**：改前有 1 次（`新聞稿與報告本文`），C3 一併消掉，現在 0 次。
- **歸因密度**：改前第十段有 3 個歸因短語（超過「一段最多兩個」），C8 收成 2 個。開頭兩段各 0 個，其餘每段 ≤2。
- **description**：191 字，沒有挑選數量，以「（2026 年 9 月查證）」收尾，沒有查證流水帳。
- **仍留給協調者判斷的一處**：第二段前半「讀的是這則新聞稿、報告的出版品頁與報告全文 PDF；本站沒有做任何測試，也不做任何資安產品或服務的推薦」是查證流水帳，DELTA-4-7 第 14 條說這不是內容。第一輪沒有動它，因為 `check_article.py` 要求查核日出現在前兩段，整段重寫屬於改寫不是改事實。建議審稿階段收成一句。
- **第一段就講清楚跟讀者的關係**：第一段給了機關、日期、範圍；「跟台灣的關係」在第二段，C2 之後那一段反而變得更具體（統計不含台灣，但 FIMI 章把台灣列為敘事題目）。

## 6. 留給站主／協調者的事

1. **台灣那一句要寫到什麼程度**（最重要）。第一輪的處理是中性轉述報告 p.78 的原文，不做實質判斷、不引用該章其他統計。若站主認為政治敏感度過高、寧可只講統計範圍，可以改寫；但**不可以回到「報告沒有提到台灣」**——那與全文檢索的結果相反。
2. **表格第三列**若協調者希望只留同一軸的兩列，`summary` 第三句與 FAQ 第五題也用了 29.3%，要一起改。
3. **5.2% 的基數**在來源是個括號，ENISA 若之後出 Booklet 或勘誤把分母寫明，這句要回來重寫（`live_data_warnings` 已提醒 PDF 是固定檔名、可能換版）。
4. 新聞稿「Additional resources」那一條的連結仍是 ENISA 貼錯的本機檔案路徑（含個人資料夾名稱）。本輪照研究紀錄的規定沒有引用、沒有抄錄該字串到任何檔案。
5. 研究紀錄 `verified_facts` 第 3 條寫「每頁頁首印 TLP:CLEAR」，實際是 101 頁中的 100 頁（封底沒有）。內容包沒有用到這個說法，本輪只記錄、未改。

## 7. 自檢輸出（原樣）

```
OK tech-news-enisa-threat-landscape-20260922 zh-TW paragraphs 2700
EXIT:0
```

```
tech-news-enisa-threat-landscape-20260922
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-enisa-threat-landscape-20260922/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-enisa-threat-landscape-20260922/diagram-1.svg
1 entries checked
EXIT:1
```

`pack_cli lint` 只剩 `image_missing` 與 `raw_internal_url` 兩種，與 FACTCHECK-47 預期的一致（出圖與 relink 之前本來就會有）。

## 8. 結論

**needs_second_round**（DELTA-4-7 第 12 條本來就要求兩輪）。事實改動 **14 處**，其中 C2 推翻了研究紀錄的一條前提、C5 與 C9 動到了論述骨幹的限定詞。
第二輪請特別逐句回到一手來源複查：C2 改寫後那三段關於台灣的新句子（正文第二段、FAQ2、callout）、C4 新補的但書、C7 新寫的表格備註、C12 新寫的授權條件——這四處是第一輪自己寫進去、還沒有別人查過的句子。
