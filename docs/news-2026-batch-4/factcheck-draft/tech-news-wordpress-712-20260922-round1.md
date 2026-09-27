# 查核報告（第一輪）：tech-news-wordpress-712-20260922

- 查核者：獨立查核代理，第一輪（opus）；沒有參與撰稿。
- 查核日：2026-09-26（台北）。規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/tech/FACTCHECK.md`、DELTA-4-8（全文）、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF 十二條錯誤型態、tech.md。
- 改動檔案：內容包 `apps/api/app/guides/content/tech-news-wordpress-712-20260922.json`（11 處文字替換）、研究紀錄 `docs/tech-news-2026/research/tech-news-wordpress-712-20260922.json`（editorial_brief 1 處＋附加 `factcheck`）。腳本：`<WORK>\_tools\tech-news-wordpress-712-20260922\fc1-*.py|sh`。

## 摘要

- 主張 125 條：CONFIRMED 101、CHANGED 14、NOT FOUND 2（一句刪除、一句改寫）、OUT OF SCOPE 8。
- 第一輪事實修改：內容包 14 條主張層級的事實修改（11 次文字替換），另有 1 處讀者優先的歸因語刪減、研究紀錄 1 處更正。改了超過十處 → 結論 `needs_second_round`（本來就排了第二輪）。
- 撰稿者點名先查的三件事：
  1. 第一節兩句英文直接引文：兩句都與發布文逐字相同。第一句的中文譯文多了「官方評為」（原文沒有）→ 已刪；第二句譯文正確。
  2. 表格每個版本號：7.1.0–7.1.1／7.1.2、7.0.0–7.0.5／7.0.6、6.9.0–6.9.8／6.9.9、6.8.0–6.8.9／6.8.10，與 GHSA 的 Affected／Patched 兩欄逐列相符；正文、summary、FAQ 裡的 7.0.6、6.9.9、6.8.10、4.7.0–4.7.36 也都相符。
  3. FAQ 2：「佈景主題只是前提之一」有依據；但同一句的「伺服器環境的前提是否成立官方沒有點名細節」與 GHSA 原文相反（GHSA 寫了伺服器端前提的具體條件並點名伺服器環境），也和第一節自己的句子矛盾 → 改寫；「可靠的做法」是來源沒有做的評價 → 改成「要修補就是把版本更新到自己分支對應的修補版」（GHSA 的 Patched versions 與 backport 句撐得住）。
- 協調者裁定全部守住（逐條見文末）：事件是 9/22；KEV 四處都是「美國時間 9 月 25 日（台北時間 9 月 26 日凌晨）」，KEV 是什麼只一句；沒有攻擊鏈細節、沒有點名伺服器環境；Twenty Twelve／Fourteen 肯定句、第三方主題 such as；9/28 期限只約束美國聯邦民事行政機關（結論不變，歸因改準）。
- 自檢：`check_article.py` → `OK tech-news-wordpress-712-20260922 zh-TW paragraphs 2811`（exit 0）；`pack_cli lint` 只有 `raw_internal_url` 警告與兩條 `image_missing`（exit 1，皆為預期）。

## 重抓結果（2026-09-26 台北，UTC 14:26–14:33）

`curl -sSL --max-time 30 --compressed -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1.5 秒，請求不含任何人的姓名或 email。bytes 為落地檔案大小。原始檔：`<WORK>\_raw\tech-news-wordpress-712-20260922\round1\`。

| 來源 | HTTP | bytes | 正文？ | 與研究代理的檔案比對 |
| --- | --- | --- | --- | --- |
| WordPress 7.1.2 Release（sources 1） | 200 | 154,558 | 是，四段正文與三個小標 | 只差 CSS／JS 的 `?ver=` 快取參數；正文逐字相同；`article:published_time` 2026-09-22T14:01:20+00:00 |
| GHSA-7hp8-65ch-5whp（sources 2） | 200 | 205,297 | 是，標題、兩欄 25 組版本、Description、CVSS v4、CWE-98 | 多 5 bytes（每次請求不同的屬性）；空白正規化後文字完全相同；`relative-time` 2026-09-22T13:57:27Z |
| CISA Adds One KEV to Catalog（sources 3） | 200 | 53,409 | 是 | 位元組相同；Release Date September 25, 2026；`<time>` 12:00:00Z 為佔位值 |
| KEV JSON（sources 4） | 200 | 1,752,832 | 是 | 位元組相同；catalogVersion 2026.09.25、dateReleased 2026-09-25T18:58:16.5029Z；CVE-2026-87902 dateAdded 2026-09-25、dueDate 2026-09-28 |
| 佐證：wordpress.org/news/feed/ | 200 | 287,223 | 是 | 最新一筆仍是 7.1.2（Tue, 22 Sep 2026 14:01:20 +0000），沒有更新的安全版 |
| 佐證：cveawg.mitre.org CVE-2026-87902 | 200 | 2,798 | 是 | 位元組相同；CNA affected 為 version 0 lessThan 7.1.2 |
| 佐證：WordPress.org 說明文件〈Dashboard Updates Screen〉 | 200 | 165,637 | 是 | 研究代理沒有抓；從 `/documentation/` → `/documentation/category/dashboard/` 的連結取得，不是猜的。只用來查第三節的介面描述，不進 sources[]（上限四條） |

研究紀錄 4 條 source 引文、33 條 `verified_facts` 引文、內容包 9 個英文引號字串，全部是今天抓檔裡的連續字串（`fc1-verify-after.txt`，0 failures）。三份 HTML 以詞界比對 `Taiwan` 0 次；GHSA 的 `exploit*` 只出現在 CVSS 指標說明文字裡，發布文 0 次；KEV 條目不含 plugin。

## 改掉的地方（原文 → 改成什麼、來源原文、理由）

1. **description、第一段、summary 第 1 條**（同一個事實三處）
   「受影響範圍從最新的 7.1 分支（，一路）回溯到 4.7 分支」→「修補範圍從最新的 7.1 分支（，一路）回溯到 4.7 分支」。
   GHSA 的 Affected versions 欄只列拿到修補的分支、最舊 4.7.0；它沒說 4.7 以前不受影響（佐證的 CVE 紀錄寫 lessThan 7.1.2）。原句會被讀成「4.7 以前不受影響」，和第二節自己的但書衝突。發布文「As a courtesy, the security fix was backported to all branches eligible to receive security fixes (currently through 4.7).」、GHSA「the fix has been backported to all branches back to 4.7」撐得住「修補範圍」。
   研究紀錄 `editorial_brief` 的「受影響範圍從 4.7 到 7.1.1 各分支」同步更正，免得第二輪照紀錄改回去。
   URL：https://github.com/WordPress/wordpress-develop/security/advisories/GHSA-7hp8-65ch-5whp
2. **summary 第 4 條** 「各分支都有自己的修補版本」→「從 4.7 到 7.1 的各分支都有自己的修補版本」。單獨讀時對 4.7 以前的分支不成立（那些分支沒有修補版）。GHSA Patched versions 從 7.1.2 列到 4.7.37，25 個分支都在。URL：同上。
3. **第一節第一個引文的譯文** 「（這個安全版修補了一個官方評為嚴重等級的安全漏洞）」→「（這個安全版修補了一個嚴重等級的安全漏洞）」。原文「This security release features a fix for a critical severity security vulnerability.」沒有「官方評為」，括號裡是譯文，不能加字。URL：https://wordpress.org/news/2026/09/wordpress-7-1-2-release/
4. **第一節第二段** 刪「官方沒有公開觸發的實際做法，」。GHSA 的 Description 寫了兩個前提的具體條件（目錄條件、伺服器端可被利用的轉換方式與點名的伺服器環境）；「官方沒有公開」是超出來源的否定句。依裁定正文只寫「攻擊手法的細節不在這裡討論」。URL：GHSA。
5. **第一節第二段（讀者優先）** 同段有三個歸因語（發布文說明／官方寫的是／GHSA 說明），刪「官方寫的是」，改成直接陳述「可能導致（can lead to）遠端執行程式碼」。協調者核准的改寫類型，事實不變。
6. **第四節第二段** 「但 CISA 明寫，這個期限只約束美國聯邦民事行政機關（FCEB），對其他所有組織只是鼓勵…」→「但這個期限只約束美國聯邦民事行政機關（FCEB）：CISA 明寫相關指令只適用於這些機關，對其他所有組織只是鼓勵…」。CISA 原文「While BOD 26-04 applies only to FCEB agencies, CISA encourages all organizations to adopt risk-based vulnerability management…」講的是指令，不是「這個期限」；公告頁也沒有印 9/28（出自 KEV JSON 的 dueDate，該條目 requiredAction 要求依 BOD 26-04 處理）。結論照裁定不變。URL：https://www.cisa.gov/news-events/alerts/2026/09/25/cisa-adds-one-known-exploited-vulnerability-catalog
7. **第四節第三段** 「CISA 沒有公布受害數量、受害地區或攻擊者身分」→「CISA 的公告與 KEV 目錄條目沒有寫受害數量、受害地區或攻擊者身分」（否定句限縮到讀過的頁）。URL：KEV JSON 與 CISA 公告。
8. **第四節第三段** 「遭利用的判斷只出自 CISA」→「遭利用的判斷出自 CISA」（拿掉排他的「只」；CVE 紀錄另列第三方文章，不在 sources[]，不能說只有 CISA）。URL：CISA 公告。
9. **第五節第三段** 「官方沒有說多少網站已經透過自動背景更新完成更新」→「發布文沒有說…」。WordPress.org 另有版本統計頁，「官方沒有說」範圍太大；發布文確實沒寫。URL：發布文。
10. **FAQ 2** 「而且佈景主題只是前提之一，伺服器環境的前提是否成立官方沒有點名細節，不能用沒用這幾個主題來判斷安全與否，可靠的做法還是把版本更新到自己分支對應的修補版。」→「而且佈景主題只是兩個前提之一，另一個前提在伺服器環境，不能用沒用這幾個主題來判斷安全與否，要修補就是把版本更新到自己分支對應的修補版。」GHSA「The pre-conditions are:」下列兩條，第二條就是伺服器端並點名環境，所以「官方沒有點名細節」是錯的（NOT FOUND／與來源相反）；「可靠」是評價，來源只撐得住「修補在各分支的修補版裡」與「建議立即更新」。URL：GHSA。
11. **FAQ 4** 「CISA 明寫 2026 年 9 月 28 日的期限只約束美國聯邦民事行政機關，對其他所有組織只是鼓勵，不是法定期限；不過既然官方判斷這個漏洞已遭實際利用，愈早更新愈好。」→「2026 年 9 月 28 日的期限只約束美國聯邦民事行政機關：CISA 明寫相關指令只適用於這些機關，對其他所有組織只是鼓勵，不是法定期限；不過既然 CISA 判斷這個漏洞已遭實際利用，愈早更新愈好。」同第 6 點；另外這篇的「官方」一路指 WordPress，而 WordPress 兩份文件都沒提到遭利用，改成 CISA。URL：CISA 公告。

## 主張表

| # | 位置 | 主張 | 判定 | 依據／備註 |
| --- | --- | --- | --- | --- |
| 1 | title | 7.1.2 修補核心嚴重漏洞 | CONFIRMED | 發布文 critical severity；KEV product Core |
| 2 | description | 9/22 發布 7.1.2 安全版 | CONFIRMED | published_time 14:01:20Z＝台北 22:01 |
| 3 | description | 官方評為嚴重等級、核心漏洞 | CONFIRMED | 發布文；GHSA Critical |
| 4 | description | 受影響範圍 7.1→4.7 | CHANGED | 改「修補範圍」（第 1 點） |
| 5 | description | 美國時間 9/25（台北 9/26 凌晨） | CONFIRMED | Release Date；dateReleased 18:58Z |
| 6 | description | 依遭實際利用的證據列入 | CONFIRMED | 「based on evidence of active exploitation」 |
| 7 | description | 185 字、句尾（2026 年 9 月查證） | CONFIRMED | 讀者優先規則 |
| 8 | 第一段 | 9/22、7.1.2、嚴重等級、核心 | CONFIRMED | 同 2–3 |
| 9 | 第一段 | 受影響範圍 7.1→4.7 | CHANGED | 第 1 點 |
| 10 | 第一段 | 各分支都有對應修補版（上下文限 4.7–7.1） | CONFIRMED | GHSA Patched versions |
| 11 | 第一段 | 不需要登入就能觸發 | CONFIRMED | GHSA「An unauthenticated attacker can…」；CVSS PR:N |
| 12 | 第一段 | 兩邊前提都成立才可能 RCE | CONFIRMED | 發布文、GHSA 條件句 |
| 13 | 第一段 | CISA 中文全名、列入 KEV、日期 | CONFIRMED | CISA 公告 |
| 14 | 第一段 | 依遭實際利用的證據 | CONFIRMED | CISA 公告 |
| 15 | 第一段 | 值得回頭確認版本號 | OUT OF SCOPE | 編輯建議 |
| 16 | 第二段 | 2026-09-26 查核 | CONFIRMED | 與 checked_on、caption、sources 一致 |
| 17 | 第二段 | 讀的文件＝四條 sources | CONFIRMED | tech WRITER 第 2 條要求的段落 |
| 18 | 第二段 | 沒有實測、不提供購買建議 | OUT OF SCOPE | 規格固定句 |
| 19 | summary 1 | 9/22、嚴重等級、核心 | CONFIRMED | |
| 20 | summary 1 | 受影響範圍 7.1→4.7 | CHANGED | 第 1 點 |
| 21 | summary 2 | 不需登入；兩邊前提 | CONFIRMED | |
| 22 | summary 2 | GHSA 標示 CVSS 4.0 分數 9.2 | CONFIRMED | 「9.2 CVSS overall score」「CVSS v4 base metrics」 |
| 23 | summary 3 | KEV 日期兩個都寫 | CONFIRMED | 裁定 |
| 24 | summary 3 | 修補期限 2026-09-28 | CONFIRMED | KEV dueDate |
| 25 | summary 3 | 期限只約束美國聯邦民事行政機關 | CONFIRMED | 「BOD 26-04 applies only to FCEB agencies」＋條目 requiredAction 指向 BOD 26-04 |
| 26 | summary 4 | 各分支都有自己的修補版 | CHANGED | 限縮為 4.7 到 7.1（第 2 點） |
| 27 | summary 4 | 7.0→7.0.6、6.9→6.9.9 | CONFIRMED | GHSA |
| 28 | summary 4 | 對照自己分支，不是一律 7.1.2 | CONFIRMED | GHSA 逐分支表 |
| 29 | 第一節小標 | 條件式的核心漏洞 | CONFIRMED | GHSA 標題 conditional RCE |
| 30 | 第一節 P1 | 9/22 發布〈WordPress 7.1.2 Release〉 | CONFIRMED | |
| 31 | 第一節 P1 | 引文 1 逐字 | CONFIRMED | 發布文第一句 |
| 32 | 第一節 P1 | 引文 1 譯文 | CHANGED | 刪「官方評為」（第 3 點） |
| 33 | 第一節 P1 | 引文 2 逐字 | CONFIRMED | 發布文第二句 |
| 34 | 第一節 P1 | 引文 2 譯文「因為是安全版，建議立即更新網站」 | CONFIRMED | 忠實 |
| 35 | 第一節 P1 | 用的是建議，不是強制 | CONFIRMED | it is recommended |
| 36 | 第一節 P2 | 未經驗證攻擊者在特定條件下可能觸發 | CONFIRMED | 「under certain conditions」 |
| 37 | 第一節 P2 | 可能導致（can lead to）RCE，非必然 | CHANGED | 只刪第三個歸因語（第 5 點，讀者優先） |
| 38 | 第一節 P2 | GHSA：部分常見的伺服器預設環境已符合伺服器端前提 | CONFIRMED | 研究紀錄建議的轉述；裁定不點名 Docker／cPanel（見待決 6） |
| 39 | 第一節 P2 | 官方沒有公開觸發的實際做法 | NOT FOUND | 刪除（第 4 點） |
| 40 | 第一節 P2 | 攻擊細節不在這裡討論 | OUT OF SCOPE | 裁定 |
| 41 | 第一節 P3 | 兩個官方命名並列 | CONFIRMED | |
| 42 | 第一節 P3 | GHSA 標題逐字 | CONFIRMED | |
| 43 | 第一節 P3 | CISA 命名逐字 | CONFIRMED | 公告與 KEV vulnerabilityName |
| 44 | 第一節 P3 | 嚴重程度 Critical | CONFIRMED | |
| 45 | 第一節 P3 | CVSS 4.0 基本分數 9.2 | CONFIRMED | 只有 base metrics，overall＝CVSS-B |
| 46 | 第一節 P3 | GHSA 自己的評分、非共同分數 | CONFIRMED | CISA 兩頁沒有分數 |
| 47 | 第二節小標 | | CONFIRMED | |
| 48 | 第二節 P1 | 受影響欄 7.1.0–7.1.1 … 6.7、6.6 … 4.7.0–4.7.36 | CONFIRMED | GHSA |
| 49 | 第二節 P1 | 修補欄逐列對應 | CONFIRMED | 兩欄各 25 列、分支順序相同 |
| 50 | 第二節 P1 | 詳細版本號見下表 | OUT OF SCOPE | 表只列四個分支（待決 5） |
| 51 | 第二節 P1 | 對照自己分支 | CONFIRMED | |
| 52 | 第二節 P2 | 7.1.1 在受影響範圍，要再更新 | CONFIRMED | |
| 53 | 第二節 P2 | as a courtesy 回溯到可收安全修補的所有分支 | CONFIRMED | 發布文 Backports 段 |
| 54 | 第二節 P2 | 「currently through 4.7」逐字與譯文 | CONFIRMED | |
| 55 | 第二節 P3 | 只有最新版本受積極支援 | CONFIRMED | 發布文 |
| 56 | 第二節 P3 | 舊分支拿到修補≠仍受積極支援 | CONFIRMED | 由上句推得 |
| 57 | 第二節 P3 | 4.7 以前不在表內≠不受影響 | CONFIRMED | not_said |
| 58–61 | 表格 | 7.1／7.0／6.9／6.8 四列的受影響與修補版本 | CONFIRMED | GHSA 逐列 |
| 62 | 表格 | 6.7 至 4.7 各分支→詳見 GHSA | CONFIRMED | |
| 63 | 表格 | 4.7 以前→不在表內、修補只回溯到 4.7 | CONFIRMED | |
| 64 | 表格 caption | 出處與查核日 | CONFIRMED | 74 字 |
| 65 | 第三節小標 | 三個查核步驟 | CONFIRMED | 內部結構 |
| 66 | 第三節 P1 | 更新（Updates）頁面看得到目前版本 | CONFIRMED* | 四條 sources 沒寫；WordPress.org〈Dashboard Updates Screen〉撐得住，但 sources 已滿（待決 1） |
| 67 | 第三節 P1 | 對照上表或 GHSA | CONFIRMED | |
| 68 | 第三節 P1 | Dashboard → Updates → Update Now | CONFIRMED | 發布文 |
| 69 | 第三節 P1 | 可到 WordPress.org 下載 7.1.2 | CONFIRMED | 發布文 |
| 70 | 第三節 P2 | 自動背景更新引文逐字 | CONFIRMED | |
| 71 | 第三節 P2 | 譯文 | CONFIRMED | 「If you have sites…」譯成關係子句，意思相同 |
| 72 | 第三節 P2 | 會開始，不是已完成 | CONFIRMED | will begin |
| 73 | 第三節 P2 | 回頭看版本號、不只看通知 | OUT OF SCOPE | 編輯建議 |
| 74 | 第三節 P3 | 請維護者回報版本號，標明是編輯建議 | CONFIRMED | 兩份 WordPress 文件確實沒寫代管 |
| 75 | inline 連結 | 文字＝目標 zh-TW 標題、五語齊全 | CONFIRMED | website-maintenance-routine（en／ja／ko／zh-CN／zh-TW） |
| 76 | 圖解 caption | 9/22、7.1.2、查核日 9/26 | CONFIRMED | |
| 77 | 圖解 caption | 「四個步驟」 | OUT OF SCOPE | 與「三個查核步驟」不一致（待決 2） |
| 78 | 圖解 alt | 四格內容 | CONFIRMED | |
| 79 | 第四節小標 | | OUT OF SCOPE | |
| 80 | 第四節 P1 | KEV 是 CISA 依實際利用證據維護的清單（一句） | CONFIRMED | 「based on evidence of active exploitation」「must have … evidence of exploitation」 |
| 81 | 第四節 P1 | 美國時間 9/25（台北 9/26 凌晨）加入 | CONFIRMED | |
| 82 | 第四節 P1 | CISA 命名 | CONFIRMED | |
| 83 | 第四節 P2 | KEV 附 2026-09-28 期限 | CONFIRMED | dueDate |
| 84 | 第四節 P2 | CISA 明寫這個期限只約束 FCEB | CHANGED | 第 6 點 |
| 85 | 第四節 P2 | 鼓勵其他組織風險導向修補 | CONFIRMED | 「CISA encourages all organizations…」 |
| 86 | 第四節 P2 | 不是台灣站長的法定期限 | CONFIRMED | 推論，來源撐得住 |
| 87 | 第四節 P3 | CISA 沒有公布受害數量等 | CHANGED | 限縮到兩頁（第 7 點） |
| 88 | 第四節 P3 | 只寫依證據判斷 | CONFIRMED | |
| 89 | 第四節 P3 | 發布文與 GHSA 沒提遭利用 | CONFIRMED | 兩頁都沒有 |
| 90 | 第四節 P3 | 判斷只出自 CISA | CHANGED | 拿掉「只」（第 8 點） |
| 91 | 第四節 P3 | 不是 WordPress 核心第一次進 KEV | CONFIRMED | |
| 92 | 第四節 P3 | WordPress Core 另兩筆今年 7 月加入 | CONFIRMED | CVE-2026-60137、CVE-2026-63030，皆 2026-07-21；KEV 裡 product＝Core 的只有這三筆 |
| 93 | 第五節小標 | | OUT OF SCOPE | |
| 94 | 第五節 P1 | 四份文件沒提到台灣 | CONFIRMED | 詞界比對 0 次 |
| 95 | 第五節 P2 | GHSA 沒有暫時緩解做法 | CONFIRMED | 頁面沒有 Workarounds 段 |
| 96 | 第五節 P2 | 替代方案不是官方說法、官方只給更新 | CONFIRMED | 「官方」＝WordPress，兩份文件只給更新 |
| 97 | 第五節 P3 | 官方沒說多少網站已完成更新 | CHANGED | 改「發布文」（第 9 點） |
| 98 | 第五節 P3 | 核心漏洞、四份來源沒提外掛 | CONFIRMED | KEV 條目不含 plugin；發布文只在導覽列 |
| 99 | 第五節 P4 | 去新聞頁與 GHSA 看更新 | CONFIRMED | feed 今天最新仍是 7.1.2 |
| 100 | FAQ 1 | 會開始不是已完成 | CONFIRMED | |
| 101 | FAQ 1 | 7.1→7.1.2、7.0→7.0.6 | CONFIRMED | |
| 102 | FAQ 2 | Twenty Twelve、Twenty Fourteen（legacy）肯定句 | CONFIRMED | 「This affects the legacy Twenty Twelve and Twenty Fourteen themes」 |
| 103 | FAQ 2 | Neve、Hestia、Sydney 是舉例 | CONFIRMED | 「such as」 |
| 104 | FAQ 2 | 不是完整清單 | CONFIRMED | |
| 105 | FAQ 2 | 佈景主題只是前提之一 | CONFIRMED | 改成「兩個前提之一」，GHSA 列兩條 |
| 106 | FAQ 2 | 伺服器前提官方沒有點名細節 | NOT FOUND | 與 GHSA 相反，改寫（第 10 點） |
| 107 | FAQ 2 | 可靠的做法是更新到自己分支的修補版 | CHANGED | 第 10 點 |
| 108 | FAQ 3 | 不必跳到 7.1.2 | CONFIRMED | GHSA 逐分支修補版 |
| 109 | FAQ 3 | 6.9.9、6.8.10 | CONFIRMED | |
| 110 | FAQ 3 | 裝分支修補版即完成修補；只積極支援最新版；善意回溯 | CONFIRMED | |
| 111 | FAQ 4 | 非美國聯邦民事行政機關不受直接約束 | CONFIRMED | |
| 112 | FAQ 4 | CISA 明寫 9/28 期限只約束… | CHANGED | 第 11 點 |
| 113 | FAQ 4 | 官方判斷已遭利用 | CHANGED | 改 CISA（第 11 點） |
| 114 | FAQ 5 | 編輯建議；官方文件沒提代管；7.1.2 | CONFIRMED | |
| 115 | callout | 9/22 發布；會開始不是已完成 | CONFIRMED | |
| 116 | callout | 查核到 9/26 | CONFIRMED | |
| 117 | 結尾連結 1 | 索引標題逐字、網址 | CONFIRMED | tech-news-2026-index 五語 |
| 118 | 結尾連結 2 | CRA 那篇標題逐字、網址 | CONFIRMED | tech-news-eu-cra-reporting-20260911 五語 |
| 119–122 | sources | 四條 title、url、checked_on 2026-09-26 | CONFIRMED | 今天都 200、都是正文 |
| 123 | 研究紀錄 | hero_label「自動更新不等於已更新」、diagram.title | CONFIRMED | |
| 124 | 研究紀錄 | diagram 四格 | CONFIRMED | 第一格同待決 1 |
| 125 | 研究紀錄 | editorial_brief「受影響範圍從 4.7 到 7.1.1 各分支」 | CHANGED | 第 1 點，紀錄同步更正 |

（58–61、119–122 各算四條，總數 125。）

## 界線檢查

- 購買建議、推薦式比價：沒有。主機商與佈景主題都沒有推薦。
- 沒歸因的廠商宣稱：「嚴重等級」寫成「官方評為」；CVSS 9.2 寫成 GHSA 的評分；遭利用寫成 CISA 的判斷（FAQ 4 已從「官方」改成 CISA）。
- 攻擊細節：正文沒有 get_page_template、page- 目錄條件、pearcmd／PEAR、register_argc_argv、Docker、cPanel、PHP 版本；「page-」只出現在照原文並列的 GHSA 標題裡（正文與 sources 各一次）。
- 狀態：KEV 是後續發展；自動更新「會開始」不寫成已完成；沒有「首次」「唯一」。

## 讀者優先

- 「本文」0 次；「這篇」2 次、「這一篇」2 次（第二段、description、callout、inline 連結句）。
- 每段歸因語：改完後最多兩個（第一節 P1、P2 與第二節 P2 各兩個）。
- 「官方」全篇 30 次，偏多（DELTA-4-7 第 14 條的警告）；屬文風，沒改，交協調者。
- 第二段列出讀過的文件，是 tech WRITER 第 2 條要求的段落（只把「本文」換成「這一篇」），保留。

## 待協調者決定

1. 第三節「更新（Updates）頁面看得到目前版本」與 FAQ 1、callout、圖解第一格：四條 sources 沒寫這件事，WordPress.org〈Dashboard Updates Screen〉撐得住，但 sources[] 已滿四條。要換掉一條來源，或保留（第一輪保留並記在紀錄的 factcheck.method）。
2. 圖解 caption「四個步驟」對第三節「三個查核步驟」，第四格不是步驟。畫圖時決定是否改成「四件事」，caption 與研究紀錄 `diagram.caption` 要一起改。
3. 「4.7 以前」可能被讀成含 4.7：翻譯要寫成 before 4.7／早於 4.7；要改中文就表格、圖解、alt 一起改。
4. 兩個官方命名只有英文，沒有中文譯名（寫作規格要求引文附中文）。
5. 「詳細版本號見下表」比表格實際內容寬。
6. 「部分常見的伺服器預設環境」的「常見」是研究紀錄的轉述，GHSA 沒寫「常見」；依裁定不點名，保留。

## 協調者裁定的查核結果

- 事件是 9/22 的 7.1.2：slug、news_date、第一段一致；發布文與 feed 今天仍是 2026-09-22T14:01:20Z。守住。
- KEV「美國時間 9 月 25 日（台北時間 9 月 26 日凌晨）」：四處寫法一致；KEV 是什麼只用第四節第一段一句說明。守住。
- 沒有攻擊鏈細節、沒有點名伺服器環境：守住。刪掉的兩句（「官方沒有公開觸發的實際做法」「伺服器前提官方沒有點名細節」）是把「這裡不轉述」寫成了「官方沒有」，與 GHSA 原文相反。
- Twenty Twelve／Fourteen 肯定句、第三方主題 such as：FAQ 2 與 GHSA 原文相符。守住。
- 9/28 只約束美國聯邦民事行政機關：結論守住；第四節與 FAQ 4 改成 CISA 原文說的「相關指令只適用於這些機關」，不再寫 CISA「明寫這個期限」。

## 自檢輸出（原樣）

```
OK tech-news-wordpress-712-20260922 zh-TW paragraphs 2811
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

## 結論

`needs_second_round`：主張層級改了 14 處事實（超過十處）。沒有改到骨幹論述，但第二輪要逐句重查第一輪新寫的句子：第 1、2、6、10、11 點。
