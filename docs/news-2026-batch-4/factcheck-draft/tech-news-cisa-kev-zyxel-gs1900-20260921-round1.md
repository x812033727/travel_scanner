# 查核報告（第一輪）：`tech-news-cisa-kev-zyxel-gs1900-20260921`

- 查核代理：獨立查核代理（第一輪），2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-cisa-kev-zyxel-gs1900-20260921.json`（zh-TW only、`display_order` 323、`news_date` 2026-09-21）
- 研究紀錄：`docs/tech-news-2026/research/tech-news-cisa-kev-zyxel-gs1900-20260921.json`（`sourcing_verdict: full`、`checked_on` 2026-09-23）
- 主張數 **106**；**CONFIRMED 99／CHANGED 6／NOT FOUND 0／OUT OF SCOPE 1**
- 結論：**needs_second_round**（第一輪本來就一定要跑第二輪；本輪改了 6 處事實，其中 3 處動到骨幹論述）

---

## 1. 來源重抓結果（2026-09-23，`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥2 秒；UA／標頭／查詢字串沒有帶入任何人的姓名或 email）

| # | URL | 狀態 | bytes | 正規化後正文 | 讀到正文？ |
| --- | --- | --- | --- | --- | --- |
| 1 | `https://www.cisa.gov/news-events/alerts/2026/09/21/cisa-adds-one-known-exploited-vulnerability-catalog` | 200 | 53,145 | 4,412 字元 | 是（`Release Date September 21, 2026`、CVE 一行、BOD 段落齊全） |
| 2 | `https://www.cisa.gov/known-exploited-vulnerabilities-catalog` | 200 | 286,240 | 37,058 字元 | 是（CVE-2026-7273 完整條目：Date Added／Due Date／Action／Notes／CWE-121／Unknown／Yes） |
| 3 | `https://www.zyxel.com/global/en/support/security-advisories/…-gs1900-series-switches-06-16-2026` | 200 | 103,799 | 8,740 字元 | 是（十列對照表、限定句、`Revision history 2026-6-16: Initial release`） |
| 4 | `https://www.zyxel.com/tw/zh/support/security-advisories/…-gs1900-series-switches-06-16-2026` | 200 | 102,183 | 5,665 字元 | 是（同一張表、`2026-6-16：首次發布`） |

來源 2 的 bytes 比研究紀錄當時多了 2,083（284,157 → 286,240），頁面仍印 `Showing 1 to 20 of 1717 results`、CVE-2026-7273 的每一個欄位值逐字相同，屬於動態頁的正常變動，**不是內容改版**，四條 `checked_on` 一律維持 2026-09-23（今天就是重抓日，沒有改的理由）。

**只作為反證、刻意不進 `sources[]` 的三份**（依科技查核規格「不准用 `sources[]` 以外的新網址替文章補事實」）：

| URL | 狀態 | bytes | 用途 |
| --- | --- | --- | --- |
| `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` | 200 | 1,737,207 | `catalogVersion 2026.09.21`、`count 1717`；確認 `dateAdded=2026-09-21` 全庫只有這一筆，`dateAdded=2026-09-18` 的三筆 `vendorProject` 都是 `Linux`、`product` 都是 `Kernel` |
| `https://www.cisa.gov/news-events/alerts/2026/09/18/cisa-adds-two-known-exploited-vulnerabilities-catalog` | 200 | 53,411 | 公告正文印的是 `CVE-2025-39964 Linux Kernel Race Condition Vulnerability`、`CVE-2026-53266 Linux Kernel Out-of-Bounds Write Vulnerability` |
| `https://www.cisa.gov/news-events/alerts/2026/09/18/cisa-adds-one-known-exploited-vulnerability-catalog` | 200 | 53,224 | 公告正文印的是 `CVE-2025-39682 Linux Kernel Improper Check for Unusual or Exceptional Conditions Vulnerability` |

---

## 2. 改掉的 6 處

### (1) 開場段：「這系列公告第一次在編號旁直接寫出具名的廠商與產品線」——**錯的**

- 原文：`——KEV 目錄的廠商／產品欄印的是「Zyxel | GS1900 Series Switches」，這是這系列公告第一次在編號旁直接寫出具名的廠商與產品線。`
- 改成：`——KEV 目錄的廠商／產品欄是「Zyxel | GS1900 Series Switches」，而 CISA 在這一筆的備註裡直接連到原廠公告，公告上有型號與韌體版本的對照表。`
- 來源怎麼寫：`sources[]` 第 2 條（KEV 目錄頁）今天同一頁就印著三筆 `Linux | Kernel`（Date Added 2026-09-18）；2026-09-18 兩則公告的正文在編號旁印的就是 `Linux Kernel Race Condition Vulnerability` 等名稱。KEV 的 `vulnerabilityName` 本來就以廠商＋產品開頭，這不是這一筆的特例。
- 為什麼：這是科技查核規格第 6 條點名的錯型（「第一份／唯一」這種超出「這一頁沒有寫」範圍的句子）。替代句改成兩件今天在來源上讀得到的事：這一筆的備註第一個連結就是原廠公告（研究紀錄 `verified_facts` 第 26 條），而那份公告有型號與韌體版本對照表。
- 來源：`https://www.cisa.gov/known-exploited-vulnerabilities-catalog`

### (2) 第一節：「2026 年 9 月 18 日那一次一個廠牌或型號都沒有點名」——**錯的**

- 原文：`CISA 在 2026 年 9 月 18 日也發布過同機制的公告，但那一次一個廠牌或型號都沒有點名。`
- 改成：`CISA 在 2026 年 9 月 18 日也用同一個機制加進三個 Linux 核心漏洞，KEV 目錄那三筆的廠商／產品欄印的是「Linux | Kernel」，落不到任何一台具體的機器；這一次點到的是一條硬體產品線，對得到自己手上那一台。`
- 來源怎麼寫：KEV 目錄頁今天同頁可見 `Linux | Kernel` × 3（`CVE-2025-39682`／`CVE-2026-53266`／`CVE-2025-39964`，Date Added 都是 2026-09-18）。**廠牌有點名（Linux），沒有點名的是機型。**
- 為什麼：這是全篇的角度（「這一次不一樣在哪裡」）所依附的那一句，錯了整節就站不住。改寫後角度保留，但依據換成查得實的那一個：那三筆對不到具體機器，這一筆是一條硬體產品線。
- 來源：`https://www.cisa.gov/known-exploited-vulnerabilities-catalog`

### (3) summary 第一條：跟著 (1)(2) 的對比說法走

- 原文：`，這次在編號旁直接寫出受影響廠牌與產品線：Zyxel GS1900 系列交換器。`
- 改成：`，廠商／產品欄印的是「Zyxel | GS1900 Series Switches」，點到的是一條硬體產品線。`
- 為什麼：`這次` 是相對於「上次沒有」的比較級，前提已被推翻；改成直述目錄欄位值。summary 的數字（1900 等）在正文都找得到，`check_article.py` 的 summary-number 規則仍過。
- 來源：`https://www.cisa.gov/known-exploited-vulnerabilities-catalog`

### (4) 第五節：KEV「Action」欄的條件被前移

- 原文：`依照廠商指示採取緩解措施，並符合 BOD 26-04 的規定；沒有可用的緩解措施時，就依 BOD 26-04 對雲端服務的規定處理，或停止使用該產品。`
- 改成：`依照廠商指示採取緩解措施，並符合 BOD 26-04 與 CISA「鑑識初篩要求」的規定；雲端服務照 BOD 26-04 適用的指引處理，沒有可用的緩解措施就停止使用該產品。`
- 來源怎麼寫：`Follow applicable BOD 26-04 guidance for cloud services **or discontinue use of the product if mitigations are unavailable.**` 條件句掛在「停止使用該產品」那一支，不是掛在整句前面；原文把它前移，等於把「雲端服務照指引處理」也寫成有條件。順手補回被省掉的 `and CISA's "Forensics Triage Requirements"`（合規對象是兩份，不是一份）。
- 來源：`https://www.cisa.gov/known-exploited-vulnerabilities-catalog`

### (5) 第二節：兩份公告的網址差異

- 原文：`網址只差 /tw/zh/，`
- 改成：`網址只把 /global/en/ 換成 /tw/zh/，`
- 為什麼：英文版是 `…/global/en/support/…`、繁中版是 `…/tw/zh/support/…`，差的不是「多一段」而是「換一段」；讀者照原句去拼網址會拼錯。
- 來源：`https://www.zyxel.com/tw/zh/support/security-advisories/…-gs1900-series-switches-06-16-2026`

### (6) 第二段：查證流水帳（研究紀錄 `must_not_write` 第 20 條）

- 原文：`這一篇的資料在 2026 年 9 月 23 日查核，讀的是 CISA 這則公告全文、KEV 目錄頁對這一筆的完整條目，以及 Zyxel 原廠公告的英文版與繁體中文版。本站沒有登入或操作任何一台交換器，也不做任何品牌或型號的購買、換機建議；下文整理官方公告寫了什麼、沒寫什麼，以及讀者可以自己核對的兩件事：型號與韌體版本。`
- 改成：`這一篇的資料在 2026 年 9 月 23 日查核，來源是 CISA 與 Zyxel 的四份官方頁面。下文整理公告寫了什麼、沒寫什麼，以及讀者可以自己核對的兩件事：型號與韌體版本；這裡不做任何品牌或型號的購買、換機建議。`
- 為什麼：`must_not_write` 第 20 條與 DELTA-4-7 第 14 條都禁止把「我們讀了哪幾頁」「本站沒有操作機器」寫進正文。查核日（`check_article.py` 要求出現在前兩段）與不做購買建議的界線都保留。事實沒有變動，只是把流水帳拿掉。
- 來源：無（規格層面的修正）

---

## 3. 逐條主張表（106 條）

判定：C＝CONFIRMED、CH＝CHANGED、NF＝NOT FOUND、OS＝OUT OF SCOPE。「來源」欄的 1／2／3／4 對應第 1 節那張表的四條 `sources[]`。

| # | 位置 | 主張 | 判定 | 來源 |
| --- | --- | --- | --- | --- |
| 1 | title | CISA 把 Zyxel GS1900 交換器漏洞列入已遭利用清單 | C | 1,2 |
| 2 | description | 事件日 2026 年 9 月 21 日 | C | 1,2 |
| 3 | description | CISA 把 CVE-2026-7273 列入「已遭利用漏洞」目錄 | C | 1,2 |
| 4 | description | 點名 Zyxel GS1900 系列交換器 | C | 1,2 |
| 5 | description | 整理原廠公告列出的受影響型號與修補版本 | C | 3,4 |
| 6 | description | 2026 年 9 月 24 日的期限實際管到誰 | C | 1,2 |
| 7 | description | 說明不涉及攻擊手法；句尾只帶「（2026 年 9 月查證）」 | C | — |
| 8 | 第一段 | 2026 年 9 月 21 日 CISA 發布公告 | C | 1 |
| 9 | 第一段 | 依「有實際遭到利用的證據」 | C | 1 |
| 10 | 第一段 | 把 CVE-2026-7273 加進 KEV 目錄 | C | 1 |
| 11 | 第一段 | 點名的是 Zyxel 的 GS1900 系列交換器 | C | 1,2 |
| 12 | 第一段 | 繁體中文官網印為「兆勤科技」 | C | 4 |
| 13 | 第一段 | 廠商／產品欄是「Zyxel \| GS1900 Series Switches」 | C | 2 |
| 14 | 第一段 | 「這系列公告第一次在編號旁直接寫出具名的廠商與產品線」 | **CH** | 2 |
| 15 | 第一段 | （新）CISA 在這一筆的備註裡直接連到原廠公告 | C | 2 |
| 16 | 第一段 | （新）那份公告上有型號與韌體版本的對照表 | C | 3,4 |
| 17 | 第二段 | 查核日 2026 年 9 月 23 日 | C | 1–4 |
| 18 | 第二段 | 「讀的是…」「本站沒有登入或操作任何一台交換器」 | **CH** | — |
| 19 | 第二段 | （新）來源是 CISA 與 Zyxel 的四份官方頁面 | C | 1–4 |
| 20 | 第二段 | 不做任何品牌或型號的購買、換機建議（界線聲明） | C | — |
| 21 | summary 1 | 2026-09-21／依證據／CVE-2026-7273／KEV | C | 1 |
| 22 | summary 1 | 「這次在編號旁直接寫出受影響廠牌與產品線」 | **CH** | 2 |
| 23 | summary 1 | （新）廠商／產品欄印的是「Zyxel \| GS1900 Series Switches」 | C | 2 |
| 24 | summary 2 | 原廠公告列出受影響型號的韌體版本與修補版本對照表 | C | 3,4 |
| 25 | summary 2 | 寫明未列於表中的市售產品不受此漏洞影響 | C | 3,4 |
| 26 | summary 2 | 公告首次發布於 2026 年 6 月 16 日 | C | 3 |
| 27 | summary 2 | 繁體中文版同一天發布 | C | 4 |
| 28 | summary 3 | 漏洞出在 GS1900 系列交換器韌體的 CGI 程式 | C | 2,3,4 |
| 29 | summary 3 | 未經身分驗證的 LAN 攻擊者、特製 HTTP 請求、可能執行 OS 指令 | C | 2,3,4 |
| 30 | summary 4 | KEV 對這一筆印的到期日是 2026 年 9 月 24 日 | C | 2 |
| 31 | summary 4 | BOD 26-04 只適用於 FCEB 機關 | C | 1 |
| 32 | summary 4 | 對其他組織 CISA 用的字是「鼓勵」 | C | 1 |
| 33 | 第一節 P1 | 公告標題「CISA Adds One Known Exploited Vulnerability to Catalog」 | C | 1 |
| 34 | 第一節 P1 | 「Release Date」欄印 2026 年 9 月 21 日 | C | 1 |
| 35 | 第一節 P1 | CVE 名稱「Zyxel GS1900 Series Switches Stack-Based Buffer Overflow Vulnerability」 | C | 1,2 |
| 36 | 第一節 P1 | 依據是「有實際遭到利用的證據」 | C | 1 |
| 37 | 第一節 P1 | 沒有附上證據、案例或受害者（限於這則公告） | C | 1 |
| 38 | 第一節 P2 | CISA 2026 年 9 月 18 日也用同一個機制加進條目 | C | 2 |
| 39 | 第一節 P2 | 「那一次一個廠牌或型號都沒有點名」 | **CH** | 2 |
| 40 | 第一節 P2 | （新）09-18 加進的是三個 Linux 核心漏洞 | C | 2 |
| 41 | 第一節 P2 | （新）那三筆的廠商／產品欄印「Linux \| Kernel」 | C | 2 |
| 42 | 第一節 P2 | KEV 是什麼、BOD 期限分級不重講（編輯聲明，符合 `must_not_write` 2） | OS | — |
| 43 | 第一節 P3 | Due Date 2026 年 9 月 24 日 | C | 2 |
| 44 | 第一節 P3 | 公告寫明 BOD 26-04 只適用 FCEB 機關 | C | 1 |
| 45 | 第一節 P3 | 對其他所有組織用的是 encourages | C | 1 |
| 46 | 第一節 P3 | 這個日期拘束美國聯邦機關，不是台灣的機關、公司或個人 | C | 1 |
| 47 | 第二節 P1 | KEV 目錄寫的是整個系列的名稱 | C | 2 |
| 48 | 第二節 P1 | KEV 目錄沒有列出實際型號 | C | 2 |
| 49 | 第二節 P1 | Zyxel 2026 年 6 月 16 日首次發布公告 | C | 3,4 |
| 50 | 第二節 P1 | 十個型號字串（GS1900-8／-8HP／-10HP／-16／-24／-24E／-24EP／-24HPv2／-48／-48HPv2）與原廠表逐字相同、順序相同 | C | 3,4 |
| 51 | 第二節 P2 | 「未列於表中的市售產品皆不受此漏洞影響」逐字 | C | 4 |
| 52 | 第二節 P2 | 修補程式只釋出給「仍在漏洞支援期間內」的型號 | C | 3,4 |
| 53 | 第二節 P2 | 已下市或超出漏洞支援期間的機種原廠沒有另外交代 | C | 3,4 |
| 54 | 第二節 P3 | 原廠同一天也發布了繁體中文版 | C | 3,4 |
| 55 | 第二節 P3 | 「網址只差 /tw/zh/」 | **CH** | 3,4 |
| 56 | 第二節 P3 | 修訂紀錄同樣只有一列「2026-6-16：首次發布」 | C | 4 |
| 57 | 第二節 P3 | 繁中版公司名印為「兆勤科技 (Zyxel)」 | C | 4 |
| 58 | 第二節 P3 | 型號、版本字串與限定詞與英文版逐字對應 | C | 3,4 |
| 59 | 第二節 P3 | 兩版沒有互相矛盾 | C | 3,4 |
| 60 | 第三節 P1 | GS1900-8 受影響版本 2.90(AAHH.1)C0 及更早 | C | 3,4 |
| 61 | 第三節 P1 | GS1900-8 修補版本 2.90(AAHH.2)C0 | C | 3,4 |
| 62 | 第三節 P1 | 其他型號版本代碼不同、排法相同 | C | 3,4 |
| 63 | 第三節 P1 | 每一列受影響版本是 .1)C0 及更早、修補版本是 .2)C0 | C | 3,4 |
| 64 | 第三節 P1 | 明寫這是本站對照的結果、不可外推（`must_not_write` 10） | C | — |
| 65 | 第三節 P2 | 讀者可核對的兩個動作：型號、韌體版本 | C | 3,4 |
| 66 | 第三節 P2 | 兩份公告都沒有寫在管理介面查版本的操作步驟 | C | 3,4 |
| 67 | 第三節 P3 | 型號對上但版本沒更新仍在受影響範圍內 | C | 3,4 |
| 68 | 第三節 P3 | 型號不在名單才適用「市售產品不受影響」，且要在售、在支援期間內 | C | 3,4 |
| 69 | 第四節 P1 | 繁中版漏洞說明整段逐字引用 | C | 4 |
| 70 | 第四節 P1 | CISA 的英文說明是同一件事 | C | 2,3 |
| 71 | 第四節 P1 | 不解釋觸發、不寫入侵指標（編輯聲明，符合 `must_not_write` 1） | OS→C | — |
| 72 | 第四節 P2 | 明寫是編輯設計的例子、不是設定教學 | C | — |
| 73 | 第五節 P1 | Action 欄：依照廠商指示採取緩解措施 | C | 2 |
| 74 | 第五節 P1 | 「沒有可用的緩解措施時，就依…雲端服務的規定處理，或停止使用該產品」（條件前移） | **CH** | 2 |
| 75 | 第五節 P1 | 這是 CISA 對美國聯邦機關的要求，不是本站建議 | C | 2 |
| 76 | 第五節 P2 | 繁中版求助管道整句逐字（含「Zyxel 官方 中文論壇 (Community)」的空格） | C | 4 |
| 77 | 第五節 P2 | 公告本身沒有附任何韌體下載連結 | C | 3,4 |
| 78 | 第五節 P3 | 四份來源都沒有寫漏洞實際怎麼被觸發 | C | 1–4 |
| 79 | 第五節 P3 | 沒有入侵指標 | C | 1–4 |
| 80 | 第五節 P3 | 沒有任何嚴重度分數 | C | 1–4 |
| 81 | 第五節 P3 | 原廠六月就釋出修補、九月才列入 CISA 目錄 | C | 1,3 |
| 82 | 第五節 P3 | 兩份公告都沒有解釋這段時間差（不代為猜測） | C | 1,3,4 |
| 83 | 表格列 1 | 2026 年 6 月 16 日／原廠公告首次發布，列出修補版本 | C | 3,4 |
| 84 | 表格列 1 | 「管到誰：所有 GS1900 使用者」 | C（見第 4 節保留意見） | 3,4 |
| 85 | 表格列 2 | 2026 年 9 月 21 日／CISA 列入 KEV 目錄 | C | 1,2 |
| 86 | 表格列 2 | 「公告對象是所有組織，要求對象是美國聯邦機關」 | C | 1 |
| 87 | 表格列 3 | 2026 年 9 月 24 日／KEV 印的 Due Date／FCEB 機關 | C | 1,2 |
| 88 | 表格列 4 | 2026 年 9 月 23 日／本站查核來源的日子／無 | C | — |
| 89 | 表格 caption | 四個容易混在一起的日期整理，查核日 2026 年 9 月 23 日（34 字，≤200） | C | — |
| 90 | 圖解 caption | 與研究紀錄 `diagram.caption` 逐字相同（`check_article.py` 有這條檢查） | C | — |
| 91 | FAQ 1 | 9/24 前不需要完成任何更新；期限只拘束 FCEB 機關 | C | 1,2 |
| 92 | FAQ 2 | 十個型號再列一次，字串與原廠表一致；先型號後版本 | C | 3,4 |
| 93 | FAQ 3 | 不在名單≠安全：兩個限定詞（市售、仍在漏洞支援期間內）都保留 | C | 3,4 |
| 94 | FAQ 4 | 四份來源都沒有 CVSS 或嚴重度分級；不做購買或換機建議 | C | 1–4 |
| 95 | FAQ 5 | 勒索軟體欄查核當天印的是 Unknown，不是「否」 | C | 2 |
| 96 | FAQ 6 | 沒有下載連結；管道是當地服務代表或官方中文論壇 | C | 3,4 |
| 97 | callout | 四份來源都是 CISA 與 Zyxel 官方頁面、查核日 2026-09-23 | C | 1–4 |
| 98 | callout | KEV 內容與勒索軟體欄可能隨時間變動，寫的是查核當下狀態 | C | 2 |
| 99 | callout | 9/24 期限拘束 FCEB 機關，不是台灣讀者 | C | 1 |
| 100 | callout | 文中不含攻擊手法、入侵指標或嚴重度分數 | C | — |
| 101 | 結尾連結 1 | `2026 年科技新聞總整理：硬體、平台、電信與法規的重點` 與索引包 zh-TW `title` 逐字相同 | C | — |
| 102 | 結尾連結 2 | `CISA 同一天兩則公告：三個 Linux 核心漏洞列入「已遭利用」清單` 與 `tech-news-cisa-kev-linux-kernel-20260918` 的 zh-TW `title` 逐字相同 | C | — |
| 103 | sources 1–4 | 四條 URL、標題與 `checked_on`（2026-09-23）今天全部重抓並讀到正文 | C | 1–4 |
| 104 | 日期一致性 | slug 後綴 `20260921` ＝ `news_date` 2026-09-21 ＝ 第一段的 2026 年 9 月 21 日 | C | — |
| 105 | 中繼資料 | 研究紀錄 `title` 與 zh-TW `title` 相同；`display_order` 323；`topics` = tech／tech-news | C | — |
| 106 | `hero.alt` | 依科技查核規格不查、不改（主圖由協調者繪製後改寫） | OS | — |

---

## 4. 界線檢查（`tech.md` 與指派訊息的六條）

| 界線 | 結果 |
| --- | --- |
| 不重述 KEV／BOD 26-04 是什麼、期限怎麼分級 | **過**。全篇只寫三件查得實的事（Due Date、只適用 FCEB、encourages），並在第一節就把讀者導去第二個連結那篇。改寫 (2) 只多加了 09-18 那三筆的欄位值，沒有解釋機制。 |
| 不把 Zyxel 稱為台灣廠商 | **過**。全文沒有「台灣廠商／本土品牌／總部／新竹」。台灣角度只用查得實的兩件事：繁中版公告同日發布、公司名印為「兆勤科技 (Zyxel)」。 |
| FCEB 期限不得寫成讀者的建議 | **過**。第一節、表格第 3 列、FAQ 1、callout 四處都把 9/24 釘死在 FCEB 機關上；沒有「還有一天」「即將到期」這類相對時間。 |
| 只說表上列的型號受影響／已修補 | **過**。十個型號逐一列出、沒有清點數字、沒有「GS1900 全系列」；兩個限定詞（市售、仍在漏洞支援期間內）在正文、FAQ 3 各出現一次完整版。改寫 (1)(2) 用的是「一條硬體產品線」，指的是 CISA 欄位的粒度，不是「全系列有漏洞」。 |
| 不寫攻擊手法／入侵指標 | **過**。技術粒度停在來源印的那幾個詞；第四節第二段明寫是編輯設計的例子、不是設定教學。 |
| 沒有購買建議、推薦式比價、沒歸因的廠商宣稱、缺狀態的句子 | **過**。沒有價格或比較；廠商宣稱（修補程式、不受影響、對照表）都掛在「原廠公告」上；沒有把預告寫成已上市這類問題。 |
| 只有一個 callout、沒有投資免責段 | **過**（`check_article.py` 也驗過）。 |

## 5. 讀者優先檢查

- **「本文」0 次**（DELTA-4-7 第 14 條）；指涉自己用「這一篇」。
- **`description`** 158 字（120–200），句尾只帶「（2026 年 9 月查證）」，沒有查證流水帳，也沒有清點數字。
- **標題／描述／summary 沒有任何篩選數量字**。
- **歸因密度**：改寫後第一段只剩一個歸因片語（依「有實際遭到利用的證據」），其餘是直述欄位值；正文每一段最多兩個（P6、P8、P9、P18 各 2）。全篇「官方」只出現 5 次（其中 3 次是「官方中文論壇」這個專有名稱）。
- **仍偏高的一項**：正文＋callout 共 14 次「本站」。第二段最嚴重的一處已改（見改動 6），其餘是界線聲明（「本站不自己補一個下載網址」「不是本站對讀者的建議」），屬於改寫範圍，留給審稿決定，見下一節。

## 6. 留給協調者／站主的事

1. **表格第 1 列「管到誰：所有 GS1900 使用者」**：`editorial_brief` 指定這樣寫，但 `must_not_write` 第 3 條禁止把十個型號擴大成整個系列。查核判斷這一格講的是「誰該去對這張表」而不是「誰有漏洞」，所以**沒有動**；若覺得容易誤讀，可改成「表上列出的型號使用者」（改了不影響任何數字與自檢）。
2. **callout 仍留著「本站沒有操作或測試任何一台交換器」**，與第二段刪掉的那句同一類流水帳。沒有動，因為它是全篇唯一一個 callout，動它會牽到界線聲明的完整性。
3. **「本站」14 次**：見第 5 節。要收斂是改寫，不是改事實，第一輪刻意不做。
4. **live data**：Due Date 2026-09-24 在上線時已過（查核日 09-23），全篇都是釘死日期的寫法，沒有相對時間；勒索軟體欄 Unknown 與鑑識初篩欄 Yes 都寫成「查核當天目錄印的是……」。上線前若再重抓，只要 KEV 那一筆的欄位值沒變就不用改稿。
5. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 沒有這個 slug，`--assets` 還不能跑；圖上的四格要照研究紀錄 `diagram.nodes` 與定稿數字畫（本輪沒有動到任何版本字串與日期）。

## 7. 自檢輸出（原樣）

```
OK tech-news-cisa-kev-zyxel-gs1900-20260921 zh-TW paragraphs 2547
```
`check_article.py tech-news-cisa-kev-zyxel-gs1900-20260921` → exit 0（不帶 `--full`、不帶 `--assets`）

```
tech-news-cisa-kev-zyxel-gs1900-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-cisa-kev-zyxel-gs1900-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-cisa-kev-zyxel-gs1900-20260921/diagram-1.svg
1 entries checked
```
`pack_cli lint --kind life --slug tech-news-cisa-kev-zyxel-gs1900-20260921` → exit 1（只有出圖與 relink 前預期的兩類）

exit code 檔：`C:\Users\x8120\mokaair-work\news47\factcheck\tech-news-cisa-kev-zyxel-gs1900-20260921-round1.exitcodes.txt`

## 8. 結論

**needs_second_round。** 依 DELTA-4-7 第 12 條，第一輪一律要跑第二輪；本輪改了 **6 處事實**，其中開場段、第一節第二段與 summary 第一條這 3 處動到骨幹論述（文章「這一次不一樣在哪裡」的依據被整個換掉），第二輪必須逐句回一手來源重驗這三處新寫的句子，尤其是：

- 「CISA 在這一筆的備註裡直接連到原廠公告」（KEV 目錄 Additional Notes 第一個連結）
- 「09-18 那三筆的廠商／產品欄印的是『Linux | Kernel』」（KEV 目錄同頁）
- 「雲端服務照 BOD 26-04 適用的指引處理，沒有可用的緩解措施就停止使用該產品」（Action 欄條件句的掛靠位置）
