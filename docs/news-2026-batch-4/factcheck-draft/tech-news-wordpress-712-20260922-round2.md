# 查核報告（第二輪）：tech-news-wordpress-712-20260922

- 查核者：獨立查核代理，第二輪（opus）；沒有參與撰稿，也沒有參與第一輪。
- 查核日：2026-09-26（台北）。規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/tech/SECOND-ROUND.md`（連帶 `tech/FACTCHECK.md`）、DELTA-4-8 全文、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF 十二條錯誤型態；第一輪報告 `tech-news-wordpress-712-20260922-round1.md`。
- 改動檔案（只有這兩個）：內容包 `apps/api/app/guides/content/tech-news-wordpress-712-20260922.json`（42 次文字替換）、研究紀錄 `docs/tech-news-2026/research/tech-news-wordpress-712-20260922.json`（30 次文字替換＋五條 KEV 事實的區段替換＋附加 `factcheck.second_round`）。腳本：`<WORK>\_tools\tech-news-wordpress-712-20260922\fc2-*.py|sh`，都是逐字串替換、每個舊字串先斷言只出現一次，沒有 json.dump 整份檔。
- 規格差異照指派訊息處理：SECOND-ROUND.md 說「附加在同一份報告檔的最後」，指派訊息指定獨立的 round2 檔，照指派訊息寫在這裡。DELTA-4-8 第 4 條說 KEV「正文兩個日期都寫」，協調者裁定 1 較新，照裁定只寫美國時間，研究紀錄同步註明。

## 摘要

- 查核 137 條：第一輪改過或新寫的 12 處、協調者七項裁定改出來的 24 條、第一輪 CONFIRMED 101 條隨機抽 34 條（seed 20260926；第 92 條與 B7 同一句，只算一次）、但書回掃 18 條、程式比對引文 46 條、連結目標 3 條，加第二輪自己的讀者優先修改 1 條。
- 判定：CONFIRMED 且不必改 98；CHANGED 35（第一輪的句子 3、裁定改出來的 23、隨機抽查 8、第二輪讀者優先 1）；NOT FOUND 刪除 1（「7 月另有兩筆 WordPress Core 條目」，換掉 KEV JSON 後 sources[] 撐不住）；OUT OF SCOPE（只記錄）3。
- 最重的三處：
  1. **說明文件只撐得住一半的原句**。〈Dashboard Updates screen〉寫更新頁面能升級核心，並在「已經是最新版」時列出可重新安裝的版本號；有新版可升級時的範例沒有列出目前安裝的版本。原本第三節「點選更新（Updates）分頁，就能看到目前安裝的 WordPress 版本」與 FAQ 1、callout、圖解第一格都寫得比來源強。裁定的前提（「文件說更新頁面顯示已安裝版本」）只對最新版成立——來源優先，改成文件撐得住的說法，並把另一份能直接撐住「去哪看版本號」的說明文件列給協調者（待決 1）。
  2. **換掉 KEV JSON 連帶的三件事**：9 月 28 日期限（summary、第四節、FAQ 4 的題目與答案）、台北時間 9 月 26 日凌晨（description、第一段、summary、第四節）、「不是第一次列入 KEV，7 月另有兩筆」（第四節第三段），全部刪除；期限改成 CISA 公告撐得住的「相關指令要求美國聯邦民事行政機關（FCEB）優先快速修補高風險漏洞，而且只適用於這些機關」。
  3. **新來源讓兩個否定句失效**：說明文件出現「plugin」23 次，「四份來源都沒有提到外掛」改成「發布文、GHSA 與 CISA 的公告談這個漏洞時都沒有提到外掛」；GHSA 點名了兩種環境，「部分常見的伺服器預設環境」的「常見」GHSA 沒寫，照裁定 6 改寫。
- 自檢：`check_article.py` → `OK tech-news-wordpress-712-20260922 zh-TW paragraphs 2900`（exit 0，≤3,000）；`pack_cli lint` 只剩 `raw_internal_url` 警告與兩條 `image_missing`（exit 1，皆為預期）；引文比對 46 條 0 failures。
- 結論：`ok`。

## 重抓結果（2026-09-26 台北，UTC 14:45–14:49）

`curl -sSL --max-time 30 --compressed -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1.5 秒，請求不含任何人的姓名或 email。bytes 是落地檔案大小。原始檔與 `fetch-log.tsv` 在 `<WORK>\_raw\tech-news-wordpress-712-20260922\round2\`。

| 來源 | HTTP | bytes | 正文？ | 與第一輪比對 |
| --- | --- | --- | --- | --- |
| WordPress 7.1.2 Release（sources 1） | 200 | 154,558 | 是 | 抽出的文字壓空白後相同；`article:published_time` 2026-09-22T14:01:20+00:00 |
| GHSA-7hp8-65ch-5whp（sources 2） | 200 | 205,292 | 是 | 文字相同；兩欄 25 組版本、Description、CVSS v4 9.2、CWE-98 |
| CISA Adds One KEV to Catalog（sources 3） | 200 | 53,409 | 是 | 位元組相同；Release Date September 25, 2026 |
| **Dashboard Updates screen（新 sources 4）** | 200 | 165,637 | 是，h1「Dashboard Updates screen」 | 從 `https://wordpress.org/documentation/`（200、154,127）→ `/documentation/category/dashboard/`（200、149,487）的連結取得；文字與第一輪佐證抓檔相同；published 2019-01-22、頁尾 Last updated June 6, 2024 |
| KEV JSON（移出 sources[]） | 200 | 1,752,832 | 是 | 位元組相同；catalogVersion 2026.09.25；CVE-2026-87902 dueDate 2026-09-28；WordPress Core 另兩筆 CVE-2026-60137、CVE-2026-63030 dateAdded 2026-07-21 |
| 佐證：wordpress.org/news/feed/ | 200 | 287,223 | 是 | 最新一筆仍是 7.1.2（Tue, 22 Sep 2026 14:01:20 +0000），沒有更新的安全版 |
| 佐證：〈Dashboard screen〉說明文件 | 200 | 158,220 | 是 | 同一分類頁取得；At a Glance 小工具底部顯示正在執行的 WordPress 版本（不在 sources[]，只給協調者參考） |

說明文件的兩處行內標籤（「Dashboard Updates Screen」加粗、「You」的 Y 單獨加粗）會讓純去標籤的文字多出空白，所以引文比對用兩種抽法（`fc2-text.py` 去掉行內標籤不留空白），任一種對得上就算連續字串。四份 sources 以詞界比對 `Taiwan`、`台灣`、`臺灣` 都是 0 次；`plugin` 在發布文只出現在導覽列、GHSA 與 CISA 公告 0 次、說明文件 23 次；`exploit` 在發布文 0 次，GHSA 只出現在 CVSS 指標說明裡。

## 協調者裁定的落實

1. **來源互換**：內容包與紀錄的 sources[] 第 4 條換成〈Dashboard Updates screen〉（`https://wordpress.org/documentation/article/dashboard-updates-screen/`），紀錄 source 引文與四條新 verified_facts 都是連續字串：
   - 「The Dashboard Updates Screen provides the links necessary to install a ‘core’ WordPress upgrade automatically, or to download the file necessary to complete a manual upgrade.」
   - 「When visiting the Dashboard Updates Screen, if you are running the latest version of WordPress, you should see messages like this:」
   - 「If you need to re-install version x.x, you can do so here or download the package and re-install manually:」
   - 「When visiting the Dashboard Updates Screen, and there is an WordPress upgrade available, you should see messages like this:」（「an WordPress」是來源自己的錯，照抄）
   頁面**有**寫可以從這裡更新；「顯示已安裝版本」只在已是最新版時成立（見上面最重的第 1 處）。只有 KEV JSON 撐得住的都刪了：9 月 28 日、台北時間換算、7 月兩筆。KEV 日期四處都只寫「美國時間 9 月 25 日」；圖解 caption 本來就沒有 KEV 日期。紀錄的 event_date_basis、sourcing_notes、not_said、must_not_write、live_data_warnings、editorial_brief 同步改，五條 KEV 事實移到 unverified_or_excluded。
2. 圖解 caption「四個步驟」→「四件事」，並補「說明文件」為出處；內容包 caption 與 `diagram.caption` 逐字相同（check_article 驗過）。
3. 「4.7 以前」→「早於 4.7 的版本」：第二節第三段、表格最後一列、圖解 alt、node 4，紀錄的 not_said、must_not_write、editorial_brief、verified_facts 第 9、15 條；內容包剩 0 次（紀錄只剩 must_not_write 裡說明「不寫 4.7 以前」的那一次）。
4. 兩個正式名稱第一次出現時附譯名：「頁面範本解析中未經驗證的路徑穿越，導致有條件的遠端執行程式碼」「WordPress 核心遠端檔案引入漏洞」。譯名逐詞對過原文（leading to＝導致，conditional 保留成「有條件的」，沒有加「可能」）。must_not_write 加註譯名不是第三種名稱。
5. 「詳細版本號見下表」→「7.1、7.0、6.9、6.8 分支的版本號整理在下表，其餘分支請看 GHSA 的逐分支表」，與表格六列一致。
6. 「部分常見的伺服器預設環境」→「GHSA 另外點名了兩種伺服器環境，在官方映像或預設設定下（其中一種限特定 PHP 版本）就已經符合伺服器端的前提」。依據 GHSA「The official php image for Docker is affected, and the default cPanel configuration is affected when PHP prior to 8.5 is in use.」，這句在第二個前提（伺服器端）的條目下；沒有點名 Docker、cPanel 或 PHP 版本號。
7. 「官方」約 30 次 → 2 次：第一節第二段「官方映像」（official image 的直譯，不是歸因）、callout「請以官方頁面為準」。其餘改成點名或直接陳述，每一處都重查歸因對象：「自評為嚴重等級」（critical severity 出自 WordPress 發布文，GHSA 也是 WordPress 自己的儲存庫）、「開頭寫的是」（那句確實是發布文第一句）、「發布文寫的是」×3、「發布文同一段也提醒」（Backports 段）、「它稱為 legacy」（GHSA）、「WordPress 也提醒」、「不是 WordPress 文件寫的做法」×2、「文件沒寫的」、「如果 WordPress 後續發布」；「不是官方說 4.7 以前的版本不受影響」改成直接陳述「不代表這些版本不受影響」。

## 改掉的地方（原文 → 改成什麼、來源、理由）

裁定落實的逐條 before／after 見研究紀錄 `factcheck.second_round.changes`（23 筆）。下面只列第二輪自己的判斷：

1. **第三節第一段**「進入網站控制台（Dashboard），點選更新（Updates）分頁，就能看到目前安裝的 WordPress 版本；對照上表或 GHSA 頁面，找出所在分支對應的修補版本。」→「進入網站控制台（Dashboard）的更新（Updates）頁面，依 WordPress.org 的說明文件，已經是最新版本時，在這一頁會看到已是最新版的訊息與可重新安裝的版本號，有新版時則會看到升級的提示；再把目前的版本號對照上表或 GHSA 頁面，確認是不是所在分支的修補版本。」文件只在最新版的情況寫出版本號。URL：說明文件。
2. **FAQ 1、callout**「回到控制台的更新頁面，確認目前版本號……」→「回頭確認目前的版本號……」／「都建議親自確認版本號……」。同上：對停在舊分支、已裝修補版的網站，文件沒寫更新頁面會顯示什麼。URL：說明文件。
3. **研究紀錄 diagram node 1**「控制台的更新頁面」→「更新頁面會寫明是否最新」（正文第三節有同義句）。
4. **第五節第三段**「四份來源都沒有提到外掛」→「發布文、GHSA 與 CISA 的公告談這個漏洞時都沒有提到外掛」。新來源提到外掛 23 次（更新頁面也能更新外掛）。紀錄 not_said、must_not_write 同步。
5. **第五節第一段**「查到的四份官方文件都沒有提到台灣，只能說官方文件沒有提到台灣」→「這一篇引用的四份文件都沒有提到台灣，只能說文件沒寫」。換來源後重查，四份都是 0 次；否定句限縮到引用的文件。
6. **第四節第三段**「CISA 的公告與 KEV 目錄條目沒有寫……」→「CISA 的公告沒有寫……」；同段「這也不是 WordPress 核心元件第一次被列入 KEV 目錄……7 月加入的。」刪除（只有 KEV JSON 撐得住）。
7. **第四節第二段**改成公告原句撐得住的一般句：「CISA 的公告寫明，相關指令要求美國聯邦民事行政機關（FCEB）優先快速修補高風險漏洞，而且只適用於這些機關；對其他所有組織，CISA 只是鼓勵採取風險導向的漏洞管理、優先修補 KEV 目錄裡的漏洞，這對台灣站長沒有約束力。」原文「requires federal agencies to prioritize rapid remediation of high-risk vulnerabilities」「While BOD 26-04 applies only to FCEB agencies, CISA encourages all organizations to adopt risk-based vulnerability management and prioritize remediation of KEV Catalog vulnerabilities」。URL：CISA 公告。
8. **第一節第三段**「GHSA 另外標示嚴重程度 Critical，CVSS 4.0 基本分數 9.2，這是 GHSA 自己的評分」→「嚴重程度 Critical、CVSS 4.0 基本分數 9.2 是 GHSA 自己的評分」（同一分數兩個歸因併成一個，事實不變）。
9. **第五節第二段**三個歸因語（GHSA 頁面沒有列出／不是官方說法／官方只給了）→「GHSA 頁面沒有列出更新以外的暫時緩解做法；換佈景主題、刪目錄或改伺服器設定之類的替代方案都不是 WordPress 提出的做法，要修補就是更新。」（讀者優先，協調者核准的改寫類型）

## 主張表

### A. 第一輪改過或新寫的 12 處（逐句回原文）

| # | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| A1 | description、第一段、summary 1 | 修補範圍從最新的 7.1 分支回溯到 4.7 分支 | CONFIRMED | 發布文 Backports「currently through 4.7」；GHSA「backported to all branches back to 4.7」；Patched 7.1.2…4.7.37 |
| A2 | summary 4 | 從 4.7 到 7.1 的各分支都有自己的修補版 | CONFIRMED | GHSA Patched 25 組，分支連續 |
| A3 | 第一節 P1 | 引文 1 譯文拿掉「官方評為」 | CONFIRMED | 原文無此字 |
| A4 | 第一節 P2 | 刪「官方沒有公開觸發的實際做法」 | CONFIRMED | GHSA 寫了兩個前提的具體條件 |
| A5 | 第一節 P2 | 可能導致（can lead to），不是必然 | CONFIRMED | 發布文 |
| A6 | 第四節 P2 | 9/28 期限只約束 FCEB：CISA 明寫相關指令只適用於這些機關 | CHANGED | 後半 CONFIRMED；9/28 只出自 KEV JSON，裁定 1 刪除，改寫見改動 7 |
| A7 | 第四節 P3 | CISA 的公告與 KEV 目錄條目沒有寫受害數量… | CHANGED | KEV 條目移出 sources[]，限縮到公告（改動 6）；公告確實沒寫 |
| A8 | 第四節 P3 | 遭利用的判斷出自 CISA | CONFIRMED | 公告「based on evidence of active exploitation」；發布文、GHSA 沒提 |
| A9 | 第五節 P3 | 發布文沒有說多少網站已完成自動更新 | CONFIRMED | 發布文全文沒有數字 |
| A10 | FAQ 2 | 佈景主題只是兩個前提之一，另一個在伺服器環境；要修補就更新到分支修補版 | CONFIRMED | GHSA「The pre-conditions are:」兩條；Patched versions |
| A11 | FAQ 4 | 9/28 期限…；CISA 判斷已遭利用 | CHANGED | 9/28 刪除、題目改「CISA 的修補要求跟我有關嗎？」；「CISA 判斷已遭利用」CONFIRMED |
| A12 | 紀錄 editorial_brief | 修補範圍從 7.1 回溯到 4.7（4.7 以前是沒列） | CONFIRMED | 字面依裁定 3 改「早於 4.7 的版本」 |

### B. 裁定改出來的句子（每句當新主張查）

| # | 位置 | 主張（改後） | 判定 | 依據 |
| --- | --- | --- | --- | --- |
| B1 | sources[] 4（包＋紀錄） | Dashboard Updates screen | CHANGED | 裁定 1；從索引連過去取得；200、正文 |
| B2 | description | 美國時間 9 月 25 日，CISA 依遭實際利用的證據將它列入 | CHANGED | 公告 Release Date September 25, 2026；「based on evidence of active exploitation」 |
| B3 | 第一段 | 同上（CISA 中文全名） | CHANGED | 同上 |
| B4 | summary 3 | 美國時間 9/25 列入 KEV；相關指令只約束 FCEB，對其他組織只是鼓勵 | CHANGED | 公告；⊆ 第四節 P2 |
| B5 | 第四節 P1 | 美國時間 9/25 加進 KEV；KEV 是依實際遭利用證據維護的清單 | CHANGED | 公告「must have a CVE ID, evidence of exploitation…」 |
| B6 | 第四節 P2 | 相關指令要求 FCEB 優先快速修補高風險漏洞，只適用於這些機關；對其他組織只是鼓勵…；對台灣站長沒有約束力 | CHANGED | 公告兩句原文（改動 7）；最後一句是推論，來源撐得住 |
| B7 | 第四節 P3 | 不是第一次列入 KEV，7 月另有兩筆 | NOT FOUND | 只有 KEV JSON；刪除 |
| B8 | FAQ 4 | CISA 的這項要求不直接約束你：相關指令只適用於這些機關，對其他組織只是鼓勵 | CHANGED | 公告 |
| B9 | 第二段 | 讀的文件＝發布文、說明文件、GHSA、CISA 公告 | CHANGED | 與 sources[] 一致 |
| B10 | 第三節 P1 | 更新頁面：最新版時看到訊息與可重新安裝的版本號；有新版時看到升級提示 | CHANGED | 說明文件三句（改動 1） |
| B11 | FAQ 1 | 回頭確認目前版本號是否對到分支修補版（7.1.2、7.0.6） | CHANGED | 改動 2；版本號 GHSA |
| B12 | callout | 建議親自確認版本號；發布日 9/22；查核到 9/26 | CHANGED | 改動 2 |
| B13 | 第五節 P1 | 引用的四份文件都沒有提到台灣 | CHANGED | 詞界比對 0 次（改動 5） |
| B14 | 第五節 P3 | 發布文、GHSA、CISA 公告談這個漏洞時沒提外掛 | CHANGED | 改動 4 |
| B15 | 圖解 caption＋diagram.caption | 站長確認網站已修補要看的四件事，依發布文、說明文件與 GHSA 整理 | CHANGED | 裁定 2 |
| B16 | diagram node 1 | 先看版本號／更新頁面會寫明是否最新 | CHANGED | 說明文件（改動 3） |
| B17 | 第二節 P3、表格、alt、node 4 | 早於 4.7 的版本不在 GHSA 表內，修補只回溯到 4.7 | CHANGED | 裁定 3；發布文、GHSA |
| B18 | node 4 | 不在修補範圍（拿掉「官方」） | CHANGED | 發布文「currently through 4.7」 |
| B19 | 第一節 P3 | GHSA 名稱中文譯名 | CHANGED | 逐詞對原文 |
| B20 | 第一節 P3 | CISA 名稱中文譯名 | CHANGED | 逐詞對原文 |
| B21 | 第二節 P1 | 7.1、7.0、6.9、6.8 的版本號在下表，其餘看 GHSA | CHANGED | 與表格一致 |
| B22 | 第一節 P2 | GHSA 點名兩種環境，官方映像或預設設定下（一種限特定 PHP 版本）就符合伺服器端前提 | CHANGED | GHSA 原句 |
| B23 | 全文 | 「官方」→ 點名或直接陳述（約 28 處） | CHANGED | 每處歸因對象重查過（裁定 7） |
| B24 | 第一節 P3 | Critical、9.2 是 GHSA 自己的評分 | CHANGED | 改動 8；GHSA「9.2 CVSS overall score」「CVSS v4 base metrics」 |

### C. 第一輪 CONFIRMED 的隨機三分之一（34 條，編號沿用第一輪主張表）

| # | 位置 | 主張 | 判定 | 備註 |
| --- | --- | --- | --- | --- |
| 2 | description | 9/22 發布 7.1.2 | CONFIRMED | published_time 14:01:20Z＝台北 22:01 |
| 3 | description | 官方評為嚴重等級 | CHANGED | 事實對；「官方評為」→「自評為」（裁定 7） |
| 6 | description | 依遭實際利用的證據列入 | CONFIRMED | |
| 7 | description | 長度、句尾 | CONFIRMED | 167 字，句尾「（2026 年 9 月查證）」 |
| 8 | 第一段 | 9/22、7.1.2、嚴重、核心 | CHANGED | 事實對；「官方評為」→「自評為」 |
| 12 | 第一段 | 兩邊前提都成立才可能 RCE | CONFIRMED | |
| 19 | summary 1 | 同 8 | CHANGED | 同 3 |
| 21 | summary 2 | 不需登入；兩邊前提 | CONFIRMED | GHSA「An unauthenticated attacker can…」；PR:N |
| 22 | summary 2 | CVSS 4.0 9.2 | CONFIRMED | |
| 27 | summary 4 | 7.0.6、6.9.9 | CONFIRMED | |
| 30 | 第一節 P1 | 9/22 發布〈WordPress 7.1.2 Release〉 | CONFIRMED | |
| 31 | 第一節 P1 | 引文 1 逐字 | CONFIRMED | 程式比對 |
| 33 | 第一節 P1 | 引文 2 逐字 | CONFIRMED | 程式比對 |
| 36 | 第一節 P2 | 未經驗證者在特定條件下可能觸發 | CONFIRMED | 「under certain conditions」 |
| 38 | 第一節 P2 | 部分常見的伺服器預設環境 | CHANGED | 「常見」GHSA 沒寫；裁定 6 |
| 41 | 第一節 P3 | 兩個官方命名並列 | CONFIRMED | 字面改「正式名稱」 |
| 42 | 第一節 P3 | GHSA 標題逐字 | CONFIRMED | |
| 43 | 第一節 P3 | CISA 命名逐字 | CONFIRMED | 公告本身就有 |
| 51 | 第二節 P1 | 對照自己分支 | CONFIRMED | |
| 53 | 第二節 P2 | as a courtesy | CONFIRMED | |
| 55 | 第二節 P3 | 只有最新版受積極支援 | CONFIRMED | |
| 56 | 第二節 P3 | 舊分支拿到修補≠仍受支援 | CONFIRMED | |
| 59 | 表格 | 7.0：7.0.0–7.0.5／7.0.6 | CONFIRMED | |
| 64 | 表格 caption | 出處與查核日 | CHANGED | 拿掉「官方」 |
| 69 | 第三節 P1 | 可到 WordPress.org 下載 7.1.2 | CONFIRMED | |
| 76 | 圖解 caption | 9/22、7.1.2、9/26 | CHANGED | 「四個步驟」→「四件事」 |
| 78 | 圖解 alt | 四格內容 | CHANGED | 「4.7 以前的處理」→「早於 4.7 的版本」 |
| 82 | 第四節 P1 | CISA 命名 | CONFIRMED | |
| 85 | 第四節 P2 | 鼓勵其他組織風險導向修補 | CONFIRMED | 併入 B6 |
| 92 | 第四節 P3 | WordPress Core 另兩筆 7 月加入 | 見 B7 | 不重複計數 |
| 94 | 第五節 P1 | 沒提到台灣 | CONFIRMED | 換來源後重查，併入 B13 |
| 95 | 第五節 P2 | GHSA 沒有暫時緩解 | CONFIRMED | 沒有 Workarounds 段 |
| 98 | 第五節 P3 | 四份來源沒提外掛 | CHANGED | 見 B14 |
| 100 | FAQ 1 | 會開始不是已完成 | CONFIRMED | |

### D. 但書與限定詞回掃（18 條）

| # | 原文 | 正文 | 判定 |
| --- | --- | --- | --- |
| D1 | 發布文 under certain conditions／GHSA 無條件的「An unauthenticated attacker can…」 | 第一段「不需要登入就能觸發」；第一節 P2「在符合特定條件時可能觸發」 | CONFIRMED |
| D2 | can lead to | 可能導致（can lead to），不是必然 | CONFIRMED |
| D3 | If relevant pre-conditions for both… | 兩邊的前提都成立時 | CONFIRMED |
| D4 | it is recommended | 建議，不是強制 | CONFIRMED |
| D5 | If you have sites that support automatic background updates | 支援自動背景更新的網站 | CONFIRMED |
| D6 | will begin | 會開始，不是已完成 | CONFIRMED |
| D7 | currently through 4.7 | 目前回溯到 4.7 | CONFIRMED |
| D8 | only the most recent version… actively supported | 只有最新版本受到積極支援 | CONFIRMED |
| D9 | As a courtesy | 出於善意 | CONFIRMED |
| D10 | such as Neve, Hestia, and Sydney | 舉例，不是完整清單 | CONFIRMED |
| D11 | some **popular** third party themes | 「部分第三方佈景主題」 | OUT OF SCOPE（沒譯出 popular，不是限縮用的但書） |
| D12 | legacy Twenty Twelve and Twenty Fourteen（This affects，肯定句） | 它稱為 legacy 的…，不是「例如」 | CONFIRMED |
| D13 | based on evidence of active exploitation | 依遭實際利用的證據 | CONFIRMED |
| D14 | encourages all organizations | 只是鼓勵 | CONFIRMED |
| D15 | specifically those … on publicly exposed assets that grant total control… | 「高風險漏洞」 | OUT OF SCOPE（依裁定寫一般句，沒有說這個漏洞落在那個範圍） |
| D16 | you should see messages like this | 會看到 | OUT OF SCOPE（should 是「預期會看到」，寫「會看到」不強化事實） |
| D17 | 7.1.0 - 7.1.1 受影響 | 7.1.1 也要再更新 | CONFIRMED |
| D18 | 說明文件「Future security updates will be applied automatically.」 | 沒有寫進正文，也沒有寫「預設會自動更新」 | CONFIRMED（沒有超出） |

### E. 程式比對的引文（46 條，`fc2-verify-after.txt`）

研究紀錄 sources[] 4 條、verified_facts 33 條、內容包 9 個含英文的引號字串，對今天的抓檔做連續字串比對：46 OK、0 failures；verified_facts 的 url 全部在 sources[] 裡。第一次跑時有兩條被標 FAIL（發布文「actively supported.」與公告「Catalog, based on」），原因是我的去標籤法在 `<strong>`、`<a>` 前後插了空白，改用去行內標籤的抽法後對上，不是引文的錯。

### F. 連結目標（3 條）

| # | 連結 | 判定 |
| --- | --- | --- |
| F1 | 結尾 1：2026 年科技新聞總整理：硬體、平台、電信與法規的重點 → tech-news-2026-index | CONFIRMED，逐字相同，五語齊全 |
| F2 | 結尾 2：歐盟《網路韌性法》通報義務上路：9 月 11 日起，誰要多快通報 → tech-news-eu-cra-reporting-20260911 | CONFIRMED，逐字相同，五語齊全 |
| F3 | inline：網站維護要做什麼：備份、更新與故障回報的日常安排 → website-maintenance-routine | CONFIRMED，逐字相同，五語齊全 |

計數：A 12＋B 24＋C 33（第 92 條併入 B7）＋D 18＋E 46＋F 3＋第二輪自己的讀者優先修改 1（第五節 P2）＝137。CONFIRMED 且不必改 98（A 9、C 25、D 15、E 46、F 3；A12、C41 只有依裁定的字面微調，仍算 CONFIRMED）；CHANGED 35（A 3、B 23、C 8、第五節 P2 1）；NOT FOUND 1（B7）；OUT OF SCOPE 3（D11、D15、D16）。

## 界線檢查

- 購買建議、推薦式比價：沒有；主機商、佈景主題都沒推薦。
- 廠商宣稱：嚴重等級寫成 WordPress「自評為」；9.2 寫成 GHSA 自己的評分；遭利用寫成 CISA 的判斷。
- 攻擊細節：正文沒有 get_page_template、page- 目錄條件、pearcmd／PEAR、register_argc_argv、Docker、cPanel、PHP 版本號；GHSA 標題的中文譯名只是翻譯，沒有展開解釋。
- 狀態：KEV 是後續發展；自動更新「會開始」；沒有「首次」「唯一」；沒有推定台灣受影響或不受影響。
- 科技篇只有一個 callout、沒有免責 callout、topics 沒有 finance。

## 讀者優先

- 「本文」0 次；「這一篇」4 次、「這篇」2 次。
- 「官方」30 → 2（見裁定 7）。
- 開頭段只有一個歸因語（「自評為」）；正文每段最多兩個（第一節 P1、P2，第二節 P2，第四節 P2 各兩個；第五節 P2 從三個減到兩個）。第一節 P3 並列兩個名稱，把「誰命名」算成內容，不算歸因語。
- description 167 字，句尾「（2026 年 9 月查證）」；title、description、summary 沒有選文數字。
- summary 的數字都在正文（check_article 驗過）；FAQ 答案都在正文範圍內；圖解四格的數字（4.7）在正文。

## 待協調者決定

1. **更新頁面與版本號**：〈Dashboard Updates screen〉只在已是最新版時列出版本號。若要第三節直接告訴讀者「去哪裡看目前版本」，〈Dashboard screen〉（`https://wordpress.org/documentation/article/dashboard-screen/`，200、158,220 bytes，同一分類頁取得）寫 At a Glance 小工具底部會顯示正在執行的 WordPress 版本，可以改換成這一份（sources[] 已滿四條，要換掉一條）。現行寫法不需要換也正確。
2. 說明文件頁尾 Last updated June 6, 2024，範例按鈕是 Upgrade Automatically；正文的按鈕字樣照 7.1.2 發布文（Update Now），已寫進 live_data_warnings。
3. 「不是第一次列入 KEV」刪了；若要留，要有一條 sources[] 撐（上限四條）。
4. 翻譯代理請照研究紀錄：KEV 只寫美國時間 9 月 25 日、不寫期限日期、「早於 4.7 的版本」譯成 before 4.7／versions earlier than 4.7。

## 自檢輸出（原樣）

```
OK tech-news-wordpress-712-20260922 zh-TW paragraphs 2900
check rc=0
```

```
tech-news-wordpress-712-20260922
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-wordpress-712-20260922/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-wordpress-712-20260922/diagram-1.svg
1 entries checked
lint rc=1
```

```
checked 46, failures 0
```

## 結論

`ok`：七項裁定都落實並逐句回查；第二輪另外抓到說明文件只撐得住一半的原句（已改成文件撐得住的說法）與兩個被新來源推翻的否定句。沒有動到骨幹論述，zh-TW 段落 2,900 字。

## 第二輪補充：來源替換

協調者在第二輪之後要求的窄範圍補充（2026-09-26 台北，UTC 15:12），處理上面「待協調者決定」第 1 條：讀者最需要的動作是「先查自己網站跑的是哪個版本，再更新」，而〈Dashboard Updates screen〉只在已是最新版時寫出版本號。

### 前提檢查

1. **發布文有沒有寫怎麼更新**：重抓 `https://wordpress.org/news/2026/09/wordpress-7-1-2-release/` → 200、154,558 bytes，與第二輪抓檔位元組相同。正文第三段原句（逐字）：「You can download WordPress 7.1.2 from WordPress.org, or visit your WordPress Dashboard, click “Updates”, and then click “Update Now”.」→ 更新路徑有來源，條件成立，照要求換來源。
2. **〈Dashboard screen〉**：從 `https://wordpress.org/documentation/`（200、154,127）→ `/documentation/category/dashboard/`（200、149,487）的 href 取得 `https://wordpress.org/documentation/article/dashboard-screen/` → 200、158,220 bytes，與第二輪佐證抓檔位元組相同；h1「Dashboard screen」，article:published_time 2018-10-20T04:19:26+00:00、modified 2024-06-06T14:01:27+00:00，頁尾 First published October 20, 2018／Last updated June 6, 2024。逐字引文（全部在今天的抓檔裡是連續字串）：
   - 小標「Dashboard → Home」
   - 「By default, WordPress delivers five widgets on this page: At a Glance, Activity, Quick Draft, WordPress Events and News, and Welcome.」
   - 「A statement at the bottom of this widget tells you what WordPress version you’re running on, as well as the current theme that you have activated on your site.」（這句不限定網站是否最新版，舊分支的網站也適用）
   - 「The Screen Options panel allows you to choose which widgets are displayed or not displayed.」
   - 「Check the box to display a specific widget, or uncheck the box to hide that widget.」
   - 詞界比對 Taiwan／台灣／臺灣 0 次；提到 plugin 只在導覽列與「Plugin or theme developers can make new Dashboard widgets…」一句，第五節第三段的外掛否定句本來就限定在發布文、GHSA 與 CISA 公告，不受影響。

抓取：`curl -sSL --max-time 30 --compressed -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1.5 秒，請求不含任何人的姓名或 email；原始檔與 `fetch-log.tsv` 在 `<WORK>\_raw\tech-news-wordpress-712-20260922\round2b\`，腳本 `<WORK>\_tools\tech-news-wordpress-712-20260922\fc2b-*.py|sh`（逐字串替換，每個舊字串先斷言只出現一次，沒有 json.dump）。

### 改過的每一句與出處

內容包 `apps/api/app/guides/content/tech-news-wordpress-712-20260922.json`（4 處）：

| # | 位置 | 原文 → 改成 | 出處 |
| --- | --- | --- | --- |
| 1 | sources[] 第 4 條 | Dashboard Updates screen（…/dashboard-updates-screen/）→ Dashboard screen（WordPress.org 說明文件）`https://wordpress.org/documentation/article/dashboard-screen/`，checked_on 2026-09-26 | 說明文件 |
| 2 | 第二段 | 「…發布文與〈Dashboard Updates screen〉說明文件…」→「…發布文與〈Dashboard screen〉說明文件…」 | 與 sources[] 一致 |
| 3a | 第三節第一段（第一步），看版本號 | 「進入網站控制台（Dashboard）的更新（Updates）頁面，依 WordPress.org 的說明文件，已經是最新版本時，在這一頁會看到已是最新版的訊息與可重新安裝的版本號，有新版時則會看到升級的提示；再把目前的版本號對照上表或 GHSA 頁面，確認是不是所在分支的修補版本。」→「網站控制台（Dashboard）首頁預設會顯示 At a Glance 小工具，依 WordPress.org 的說明文件，小工具底部會寫出網站正在執行的 WordPress 版本（小工具被隱藏的話，可以在 Screen Options 面板勾選回來）；把這個版本號對照上表或 GHSA 頁面，確認是不是所在分支的修補版本。」 | 說明文件：Dashboard → Home（首頁）、By default … At a Glance（預設）、A statement at the bottom of this widget …（版本號）、Screen Options 兩句（括號）；對照修補版：GHSA Patched versions（原有） |
| 3b | 同段，更新 | 「手動更新的做法是進入控制台、點「Updates」、再點「Update Now」，也可以直接到 WordPress.org 下載 7.1.2 安裝。」→「還不是修補版的話，發布文寫的更新做法是進入控制台、點「Updates」、再點「Update Now」，也可以直接到 WordPress.org 下載 7.1.2 安裝。」 | 發布文（上面的原句） |
| 4 | FAQ 1 | 「建議還是回頭確認目前的版本號，是不是…」→「建議還是回控制台首頁的 At a Glance 小工具確認目前的版本號，是不是…」（第二輪因來源不足拿掉的「去哪裡看」，現在有來源，補回） | 說明文件 |

沒改、但重看過的：callout（「都建議親自確認版本號」，沒有描述介面，仍成立）、FAQ 5（請維護者回報版本號，編輯建議）、圖解 caption（「依 WordPress 發布文、說明文件與 GHSA 整理」，說明文件換成另一份仍成立，內容包 caption 與 `diagram.caption` 逐字相同，check_article 驗過）、圖解 alt、第五節第一段（四份文件都沒提台灣，新文件 0 次）。歸因語：第三節第一段兩個（「依 WordPress.org 的說明文件」「發布文寫的」），沒有超過。

研究紀錄 `docs/tech-news-2026/research/tech-news-wordpress-712-20260922.json`（文字插入，每處舊字串只出現一次；寫入前 `json.loads` 驗過）：

- `sources[3]` → Dashboard screen，fetched_at 2026-09-26T15:12:29Z、200、158,220 bytes，verbatim_quote 為 At a Glance 那一句。
- `verified_facts`：〈Dashboard Updates screen〉四條移除，換成〈Dashboard screen〉五條（上面五句引文）；發布文更新路徑那一條補註「第三節第一步的更新做法只以這一句為依據」。
- `unverified_or_excluded`：「更新頁面一定看得到目前版本」那條補上協調者決定換來源；新增一條收〈Dashboard Updates screen〉的四點與移出理由。
- `sourcing_notes` 末尾加第二輪補充段（抓取鏈、bytes、日期、round2b 目錄）；`not_said` 外掛那條改成新文件提到外掛的方式；`must_not_write` 介面字樣那條加「At a Glance、Screen Options 保留英文原名，不寫文件沒寫的畫面位置」；`live_data_warnings` 說明文件那條改成〈Dashboard screen〉（Last updated June 6, 2024，發布當天重看）；`editorial_brief` 第三節改成在 At a Glance 看版本、照發布文路徑更新。
- `diagram.nodes[0]`：`["先看版本號", "更新頁面會寫明是否最新"]` → `["先看版本號", "控制台首頁的 At a Glance"]`（細節 12.6 單位，上限 15）。
- `factcheck.second_round.source_swap_addendum`：checked_by、method、兩句逐字引文、8 筆 changes、paragraph_chars_after 2924。

### 自檢

```
OK tech-news-wordpress-712-20260922 zh-TW paragraphs 2924
check rc=0
```

```
tech-news-wordpress-712-20260922
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-wordpress-712-20260922/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-wordpress-712-20260922/diagram-1.svg
1 entries checked
lint rc=1
```

引文比對（`fc2b-verify.txt`）：sources 4 條、verified_facts 34 條、補充段兩句、內容包英文引號字串，全部是抓檔裡的連續字串；verified_facts 的 url 都在 sources[]；內容包、sources[]、verified_facts 都不再有 dashboard-updates-screen。`checked 50, failures 0`。

給翻譯代理：At a Glance、Screen Options 保留英文原名；按鈕字樣照發布文（Updates、Update Now）。圖解第 1 格已改，畫圖時照研究紀錄。

結論：`ok`，zh-TW 段落 2,924 字（≤3,000）。
