# 查核報告（第二輪）：`tech-news-cisa-kev-zyxel-gs1900-20260921`

- 查核代理：獨立查核代理（**第二輪**，與第一輪不同人、未參與撰稿），2026-09-23（台北）
- 內容包：`apps/api/app/guides/content/tech-news-cisa-kev-zyxel-gs1900-20260921.json`（zh-TW only、`display_order` 323、`news_date` 2026-09-21）
- 研究紀錄：`docs/tech-news-2026/research/tech-news-cisa-kev-zyxel-gs1900-20260921.json`
- 第一輪報告：`factcheck/tech-news-cisa-kev-zyxel-gs1900-20260921-round1.md`（106 條、改 6 處）
- 本輪覆核 **42 條**（第一輪改動的 6 條＋第一輪新寫的 6 條＋隨機抽出的 30 條），另以程式把研究紀錄 26 條 `verbatim_quote`、文章十個型號與二十個版本字串、四段逐字引文、兩個結尾連結全部重驗
- **改 14 處**（內容包 11 處、研究紀錄 3 處）；第一輪那 6 處改動與 6 句新寫的句子**全部覆核通過，沒有一處被推翻**
- 結論：**ok**

---

## 1. 來源自己重抓（2026-09-23，`curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥2 秒；UA／標頭／查詢字串沒有帶入任何人的姓名或 email）

| # | URL | 狀態 | bytes | 正規化後正文 | 與第一輪 |
| --- | --- | --- | --- | --- | --- |
| 1 | `…/alerts/2026/09/21/cisa-adds-one-known-exploited-vulnerability-catalog` | 200 | 53,145 | 4,412 字元 | 逐字相同 |
| 2 | `https://www.cisa.gov/known-exploited-vulnerabilities-catalog` | 200 | **284,157** | 37,058 字元 | 正文逐字相同 |
| 3 | Zyxel 英文公告 `…gs1900-series-switches-06-16-2026` | 200 | 103,799 | 8,740 字元 | 逐字相同 |
| 4 | Zyxel 繁中公告 `…gs1900-series-switches-06-16-2026` | 200 | 102,183 | 5,665 字元 | 逐字相同 |

**來源 2 的 bytes 差異要說清楚**：第一輪報告記 286,240 B、本輪量到 284,157 B（與撰稿當天的 `_raw/kev-catalog.html` 同一個數字）。差的 2,083 B 在頁面外圍的動態區塊；**去掉標籤、註解、`script`／`style` 之後的正文兩輪一模一樣（37,058 字元）**，`Showing 1 to 20 of 1717 results` 也相同，CVE-2026-7273 那一筆的每一個欄位值逐字相同。**不是內容改版**，四條 `checked_on` 一律維持 2026-09-23。

程式化驗證（腳本在 `_tools/tech-news-cisa-kev-zyxel-gs1900-20260921-r2/`）：

- `verify_quotes.py`：研究紀錄 26 條 `verbatim_quote` 對正規化後正文做**連續字串**比對（NFKC＋彎引號／破折號正規化）→ **26/26 命中，0 條需要換片段**，沒有把不同段落拼在一起的情形。
- `check_strings.py`：十個型號 × 英／繁兩版共 20 條「型號＋受影響版本＋修補版本」整列比對 → **20/20 命中**；英文表的型號順序與文章、FAQ 2 的列舉順序相同。四段逐字引文（繁中漏洞說明、市售產品限定句、求助管道含「Zyxel 官方 中文論壇」中間那個空格、修訂紀錄）逐字命中。`/global/en/` → `/tw/zh/` 的置換結果**與繁中版網址完全相等**。
- `check_neg.py`：四份來源（KEV 只取 CVE-2026-7273 那一段）全文搜尋 `CVSS`／`severity`／`嚴重`／`IoC`／`PoC`／`exploit code`／`download` → **全部 0 命中**；兩份原廠公告的正文段（摘要到修訂紀錄）`下載`／`download` 也是 **0**。
- KEV 目錄頁 `Date Added` 逐筆清點：**2026-09-18 恰好三筆、全部是「Linux | Kernel」；2026-09-21 恰好一筆**（就是本篇這一筆）。

---

## 2. 第一輪改動與新寫句子的覆核（12 條，全部通過）

| 第一輪 | 覆核對象 | 本輪判定 | 依據（今天讀到的原文） |
| --- | --- | --- | --- |
| 改動 (1) | 開場段「CISA 在這一筆的備註裡直接連到原廠公告」 | **成立** | KEV 條目 `Additional Notes` 的**第一個**連結就是 `https://www.zyxel.com/global/en/support/security-advisories/…06-16-2026`（即 `sources[]` 第 3 條），其後才是 BOD 26-04、Forensics Triage Requirements、NVD |
| 改動 (1) | 「公告上有型號與韌體版本的對照表」 | **成立** | 該頁 `Affected model / Affected version / Patch availability` 十列 |
| 改動 (2) | 「2026 年 9 月 18 日也用同一個機制加進三個 Linux 核心漏洞」 | **成立**（見第 4 節開放問題 2） | KEV 目錄頁 `Date Added: 2026-09-18` 恰好三筆 |
| 改動 (2) | 「那三筆的廠商／產品欄印的是『Linux \| Kernel』」 | **成立** | 三筆的欄位值逐字都是 `Linux | Kernel` |
| 改動 (2) | 「落不到任何一台具體的機器」 | **成立** | 三筆的 `Additional Notes` 都寫 `This vulnerability affects an open-source component, third-party library, protocol, or proprietary implementation that could be used by different products.` |
| 改動 (2) | 反面：原稿「一個廠牌或型號都沒有點名」 | **確認是錯的** | 09-18 那三筆的**廠商欄有值（Linux）**；沒有點名的是機型，不是廠牌 |
| 改動 (3) | summary 1「廠商／產品欄印的是『Zyxel \| GS1900 Series Switches』，點到的是一條硬體產品線」 | **成立** | 同頁欄位值；`check_article.py` 的 summary-number 規則今天仍過 |
| 改動 (4) | 「並符合 BOD 26-04 與 CISA『鑑識初篩要求』的規定」 | **成立** | `ensuring compliance with CISA's BOD 26-04 … guidance and CISA's "Forensics Triage Requirements"`——合規對象確實是兩份 |
| 改動 (4) | 「雲端服務照 BOD 26-04 適用的指引處理，沒有可用的緩解措施就停止使用該產品」 | **方向對、連接詞仍不準 → 本輪再改** | 原文是 `Follow applicable BOD 26-04 guidance for cloud services **or** discontinue use of the product if mitigations are unavailable.`；第一輪已把條件句移回正確的那一支，但用逗號並列會讀成「兩件都要做」。見第 3 節改動 2 |
| 改動 (5) | 「網址只把 /global/en/ 換成 /tw/zh/」 | **成立** | 英文版網址做這個置換後與繁中版網址完全相等（程式驗證） |
| 改動 (6) | 第二段「來源是 CISA 與 Zyxel 的四份官方頁面」 | **成立** | `sources[]` 四條＝CISA 2 條＋Zyxel 2 條；查核日 2026-09-23 仍在前兩段（`check_article.py` 有這條檢查） |
| 改動 (6) | 刪掉查證流水帳後，界線是否有缺口 | **沒有缺口** | 「不做購買、換機建議」仍在第二段、FAQ 4 與 callout；「沒有操作任何一台交換器」仍在 callout |

---

## 3. 本輪改掉的 14 處

### 內容包（11 處）

**1. 表格第 1 列「管到誰」——協調者裁定 1**

- 原文：`["2026 年 6 月 16 日", "原廠公告首次發布，列出修補版本", "所有 GS1900 使用者"]`
- 改成：`["2026 年 6 月 16 日", "原廠公告首次發布，列出修補版本", "表中型號的使用者"]`
- 為什麼：原廠只說**表上列出的十個型號**受影響，並明寫「未列於表中的市售產品皆不受此漏洞影響」；「所有 GS1900 使用者」把十個型號擴大成整個系列，正是研究紀錄 `must_not_write` 第 3 條點名的錯型。第一輪把它留給協調者，本輪照裁定改。
- 來源：`https://www.zyxel.com/global/en/support/security-advisories/…06-16-2026`

**2. 第五節第一段：KEV「Action」欄的 `or` 被寫成並列**

- 原文：`雲端服務照 BOD 26-04 適用的指引處理，沒有可用的緩解措施就停止使用該產品。`
- 改成：`雲端服務照 BOD 26-04 適用的指引處理，或在沒有可用的緩解措施時停止使用該產品。`
- 來源怎麼寫：`Follow applicable BOD 26-04 guidance for cloud services **or** discontinue use of the product if mitigations are unavailable.` 這是一個選擇句，`if mitigations are unavailable` 只掛在後面那一支。第一輪已經把條件句從句首搬回正確位置（那一步是對的），但改成逗號並列，中文會讀成「雲端服務照指引處理」**而且**「停止使用該產品」兩件都要做。補回「或」與「在……時」，兩個分支與條件的掛靠就與原文一致。
- 來源：`https://www.cisa.gov/known-exploited-vulnerabilities-catalog`

**3–11.「本站」從 13 次收到 2 次——協調者裁定 2、3**

第一輪與協調者都記成 14 次，本輪逐 block 清點是 **13 次**（正文 6、FAQ 5、表格 1、callout 1）。裁定是「只留在免責 callout 與查核日那一句（全篇 ≤3）」，改後剩 **2 次**：表格第 4 列的「本站查核來源的日子」與 callout 的「本站沒有操作或測試任何一台交換器」（裁定 3 明文保留）。**每一處都只是把「本站不會怎樣」改寫成直述事實，界線聲明的內容一句都沒有刪。**

| # | 位置 | 原文 | 改成 |
| --- | --- | --- | --- |
| 3 | 第三節 P1 | 這個規律是**本站**把對照表整理出來的結果 | 這個規律是把對照表並排整理出來的結果 |
| 4 | 第三節 P2 | ……的操作步驟，**本站也不自己補一個**。 | ……的操作步驟。 |
| 5 | 第四節 P2 | ……不是設定教學，**本站**不會列出……的步驟。 | ……不是設定教學，**底下也**不會列出……的步驟。 |
| 6 | 第五節 P1 | ……不是**本站對讀者**的建議。 | ……不是**給一般讀者**的建議。 |
| 7 | 第五節 P2 | ……沒有附上任何韌體下載連結，**本站也不自己補一個**。 | ……沒有附上任何韌體下載連結。 |
| 8 | 第五節 P3 | ……也沒有任何嚴重度分數；**本站不做任何購買或換機建議**。 | ……也沒有任何嚴重度分數。 |
| 9 | FAQ 2 | ……的操作步驟，**本站也不自己補一個**。 | ……的操作步驟。 |
| 10 | FAQ 4（三處） | ……嚴重度分級，**本站也不引用任何分數。本站**不做購買或換機建議；……不是**本站對讀者**的建議。 | ……嚴重度分級。**這裡**不做購買或換機建議；……不是**給一般讀者**的建議。 |
| 11 | FAQ 6 | ……中文論壇（Community）。**本站不會自己補一個下載網址。** | ……中文論壇（Community）。 |

界線是否還在：不做購買／換機建議 → 第二段、FAQ 4、callout 各一次；不自己補下載網址 → 事實句「公告本身沒有附上任何韌體下載連結」本身就把話說完了，而且全篇確實沒有出現任何下載網址或選單路徑（`must_not_write` 17）；「這個規律是本站對照出來的」→ 改寫後仍寫明是整理對照表的結果、不是原廠公告的句子、不能外推（`must_not_write` 10）。`本文` 仍然 **0 次**。

### 研究紀錄（3 處）

**12. `verified_facts` 第 3 條的 `fact` 還留著第一輪已判定為錯的那一句**

- 原文：`……「Zyxel GS1900 Series Switches Stack-Based Buffer Overflow Vulnerability」。這是這一系列公告第一次在編號旁直接印出具名廠商與產品線。`
- 改成：刪掉後面那一句（前半與 `verbatim_quote` 相符，保留）。
- 為什麼：那句話**超出自己的 `verbatim_quote`**（引文只有 CVE 編號與名稱），而且與同一份檔案裡第一輪寫下的 `coordinator_rulings`（「原稿的『第一次點名具名廠商』是錯的」）互相矛盾。研究紀錄對撰稿與查核都有拘束力，留著會被後續繪圖、審稿代理當成已查證的事實再寫回文章。
- 來源：`https://www.cisa.gov/known-exploited-vulnerabilities-catalog`（09-18 三筆同樣印出具名廠商欄）

**13. `verified_facts` 第 20 條的「網址只差 /tw/zh/」**

- 改成：`網址只把 /global/en/ 換成 /tw/zh/`，與第一輪對正文所做的更正一致（差的是換掉一段，不是多一段）。
- 來源：`https://www.zyxel.com/tw/zh/support/security-advisories/…06-16-2026`

**14. 研究紀錄 `summary` 仍寫著被推翻的對比**

- 原文：`這一筆與 2026-09-18 那三個 Linux 核心漏洞最大的不同是：CISA 這次點名了具體的廠商與產品——KEV 目錄的廠商／產品欄印的是「Zyxel | GS1900 Series Switches」。`
- 改成：`這一筆與 2026-09-18 那三個 Linux 核心漏洞的差別在粒度：那三筆的廠商／產品欄印的是「Linux | Kernel」，這一筆印的是「Zyxel | GS1900 Series Switches」，落得到一條硬體產品線。`
- 為什麼：同 12。`check_article.py` 不比對研究紀錄的 `summary`，改它不影響自檢。
- 來源：`https://www.cisa.gov/known-exploited-vulnerabilities-catalog`

另已在研究紀錄 `factcheck` 底下加上 `second_round`（`checked_by`／`checked_on`／`method`／`claims_checked`／`changes`(14)／`open_questions`(4)／`coordinator_rulings`(4)／`verdict: ok`），用文字插入、沒有動到其他欄位的排版。

---

## 4. 隨機抽查的 30 條（`sample.py`，seed 20260923，從 92 條 CONFIRMED 抽三分之一）

抽到 `[1, 4, 5, 8, 11, 32, 34, 36, 43, 49, 50, 54, 56, 57, 60, 62, 66, 76, 77, 80, 86, 88, 90, 94, 96, 97, 98, 100, 102, 104]`，**30 條全部維持 CONFIRMED**，逐條依據：

| # | 主張 | 依據 |
| --- | --- | --- |
| 1 | 標題：CISA 把 Zyxel GS1900 交換器漏洞列入已遭利用清單 | 公告標題＋KEV 條目 |
| 4 | description 點名 Zyxel GS1900 系列交換器 | KEV 廠商／產品欄 |
| 5 | description：整理原廠公告列出的受影響型號與修補版本 | 原廠十列對照表 |
| 8 | 2026 年 9 月 21 日 CISA 發布公告 | `Release Date September 21, 2026` |
| 11 | 點名的是 Zyxel 的 GS1900 系列交換器 | `CVE-2026-7273 Zyxel GS1900 Series Switches …` |
| 32 | 對其他組織 CISA 用的字是「鼓勵」 | `CISA encourages all organizations …` |
| 34 | 「Release Date」欄印 2026 年 9 月 21 日 | 同上 |
| 36 | 依據是「有實際遭到利用的證據」 | `based on evidence of active exploitation` |
| 43 | Due Date 2026 年 9 月 24 日 | `Date Added: 2026-09-21 Due Date: 2026-09-24` |
| 49 | Zyxel 2026 年 6 月 16 日首次發布公告 | `Revision history 2026-6-16: Initial release` |
| 50 | 十個型號字串與順序與原廠表相同 | 程式比對 20/20 命中，順序一致 |
| 54 | 原廠同一天也發布了繁體中文版 | 兩版修訂紀錄都只有 2026-6-16 一列 |
| 56 | 繁中版修訂紀錄同樣只有一列 | `修訂紀錄 2026-6-16：首次發布` |
| 57 | 繁中版公司名印為「兆勤科技 (Zyxel)」 | 繁中版摘要 |
| 60 | GS1900-8 受影響版本 2.90(AAHH.1)C0 及更早 | 對照表第一列 |
| 62 | 其他型號版本代碼不同、排法相同 | 十列逐列比對 |
| 66 | 兩份公告都沒有寫在管理介面查版本的步驟 | 兩版正文只有摘要／漏洞說明／對照表／求助管道／致謝／修訂紀錄六段，沒有任何操作步驟 |
| 76 | 繁中版求助管道整句逐字（含「Zyxel 官方 中文論壇 (Community)」的空格） | 逐字命中 |
| 77 | 公告本身沒有附任何韌體下載連結 | 兩份公告正文 `下載`／`download` 皆 0 |
| 80 | 沒有任何嚴重度分數 | 四份來源 `CVSS`／`severity`／`嚴重` 皆 0 |
| 86 | 「公告對象是所有組織，要求對象是美國聯邦機關」 | `While BOD 26-04 applies only to FCEB agencies, CISA encourages all organizations …` |
| 88 | 表格第 4 列 2026 年 9 月 23 日／查核日／無 | 四條 `checked_on` 一致 |
| 90 | 圖解 caption 與研究紀錄 `diagram.caption` 逐字相同 | 程式比對 True（`check_article.py` 也驗） |
| 94 | 四份來源都沒有 CVSS 或嚴重度分級 | 同 80 |
| 96 | 管道是當地服務代表或官方中文論壇 | 逐字命中 |
| 97 | 四份來源都是 CISA 與 Zyxel 官方頁面 | 今天四條全部 200 且讀到正文 |
| 98 | KEV 內容與勒索軟體欄可能變動，寫的是查核當下狀態 | `Known To Be Used in Ransomware Campaigns? Unknown`；`live_data_warnings` 4 |
| 100 | 文中不含攻擊手法、入侵指標或嚴重度分數 | 四份來源 `IoC`／`PoC`／`exploit code` 皆 0，文章技術粒度停在來源印的那幾個詞 |
| 102 | 第二個結尾連結 text 與目標包 zh-TW `title` 逐字相同 | `check_links.py` OK（第一個連結的索引包也 OK） |
| 104 | slug 後綴 `20260921` ＝ `news_date` ＝ 第一段日期 | 程式比對一致 |

---

## 5. 界線與讀者優先（改後重掃）

| 項目 | 結果 |
| --- | --- |
| 「本文」 | **0 次** |
| 「本站」 | **13 → 2 次**（表格查核日一格＋callout 免責），符合協調者裁定 2 的 ≤3 |
| 「官方」 | 全篇 5 次，其中 3 次是「官方中文論壇」這個專有名稱 |
| 歸因密度 | 第一段 1 個歸因片語；正文沒有任何「X 表示」「指出」；每段最多 2 個 |
| `description` | 158 字（120–200），句尾只帶「（2026 年 9 月查證）」，沒有流水帳、沒有清點數字 |
| 標題／描述／summary 的篩選數量字 | 無 |
| 只說表上列的型號受影響 | **過**（本輪把表格第 1 列的「所有 GS1900 使用者」改掉後，全篇再無擴大句） |
| 不重述 KEV／BOD 26-04 是什麼 | **過**（只寫 Due Date、只適用 FCEB、encourages 三件查得實的事，並導到第二個連結） |
| 不寫攻擊手法／入侵指標／嚴重度分數 | **過** |
| 不寫 Zyxel 是台灣廠商 | **過**（只用繁中版同日發布、公司名「兆勤科技 (Zyxel)」兩件事實） |
| 購買建議／推薦式比價／沒歸因的廠商宣稱 | **無**；廠商宣稱都掛在「原廠公告」上 |
| 一個 callout、無投資免責、不帶 finance 主題 | **過** |
| 但書與限定詞有沒有為了字數被刪 | **沒有**：「市售」「仍在漏洞支援期間內」兩個限定詞在正文與 FAQ 3 各一組完整版；本輪只刪了查證紀律句，正文 2,547 → **2,516 字**（1,800–3,000） |
| `summary` ⊆ 正文、FAQ 答案 ⊆ 正文、圖解數字在正文 | **過**（`check_article.py` 驗過） |

---

## 6. 留給協調者／站主的事

1. **「CISA『鑑識初篩要求』」是本篇自行翻譯的文件名**，來源印的是 `CISA's "Forensics Triage Requirements"`。讀者拿這個中文名到 CISA 網站查不到對應頁面。要不要補英文原名屬體例，本輪沒有動。
2. **「三個 Linux 核心漏洞」的「三」是清點來的**：KEV 目錄頁今天 `Date Added: 2026-09-18` 恰好三筆、全部是「Linux | Kernel」，但來源沒有印出「三」這個字。它與文末第二個連結那篇既有文章的標題（DELTA-4-7 第 7 條指定逐字照抄的「三個 Linux 核心漏洞列入『已遭利用』清單」）一致，所以沒有動；若站主認為清點數字一律不寫，這一句可改成「也用同一個機制加進 Linux 核心的漏洞」。
3. **live data**：Due Date 2026-09-24 上線時已過（查核日 09-23），全篇釘死日期、沒有相對時間；勒索軟體欄 Unknown 與鑑識初篩欄 Yes 都寫成「查核當天目錄印的是……」。上線前若再重抓 KEV，只要那一筆欄位值沒變就不必改稿。
4. **圖還沒畫**：`build_assets.py` 的 `_DRAWINGS` 沒有這個 slug，`--assets` 不能跑。本輪沒有動到任何型號、版本字串或日期，`diagram.nodes` 與 caption 不受影響。
5. **第一輪報告的 KEV 目錄 bytes（286,240）與本輪（284,157）不同**，但正規化後的正文兩輪逐字相同。若有人拿 bytes 當「頁面有沒有改版」的判準，請改用正文字元數與那一筆的欄位值。

---

## 7. 自檢輸出（原樣）

```
OK tech-news-cisa-kev-zyxel-gs1900-20260921 zh-TW paragraphs 2516
```
`check_article.py tech-news-cisa-kev-zyxel-gs1900-20260921` → **exit 0**（不帶 `--full`、不帶 `--assets`）

```
tech-news-cisa-kev-zyxel-gs1900-20260921
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-cisa-kev-zyxel-gs1900-20260921/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-cisa-kev-zyxel-gs1900-20260921/diagram-1.svg
1 entries checked
```
`pack_cli lint --kind life --slug tech-news-cisa-kev-zyxel-gs1900-20260921` → **exit 1**（只有出圖與 relink 前預期的兩類）

exit code 檔：`C:\Users\x8120\mokaair-work\news47\factcheck\tech-news-cisa-kev-zyxel-gs1900-20260921-round2.exitcodes.txt`

## 8. 結論

**ok。** 第一輪的 6 處改動與 6 句新寫的句子逐句回一手來源重驗，**沒有一處被推翻**；研究紀錄 26 條 `verbatim_quote` 全部命中；隨機抽查的 30 條全部維持 CONFIRMED。本輪的 14 處改動裡，只有一處是事實層面的（KEV「Action」欄的 `or` 被寫成並列），其餘是協調者的兩項裁定（表格第 1 列、「本站」收斂）與三處研究紀錄自身殘留的錯誤主張。文章沒有骨幹論述被改動，不需要第三輪。
