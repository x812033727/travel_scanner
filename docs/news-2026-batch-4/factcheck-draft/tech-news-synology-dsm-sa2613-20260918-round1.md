# 查核報告（第一輪）：tech-news-synology-dsm-sa2613-20260918

- 查核者：獨立查核代理，第一輪（opus）；沒有參與撰稿。
- 查核日：2026-09-26（台北）。規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/tech/FACTCHECK.md`、DELTA-4-8（全文）、DELTA-4-7 第 3、4、10、11、14、16 條、DELTA-4-5、BRIEF 十二條錯誤型態。
- 改動檔案：內容包 `apps/api/app/guides/content/tech-news-synology-dsm-sa2613-20260918.json`（22 次逐字替換）、研究紀錄 `docs/tech-news-2026/research/tech-news-synology-dsm-sa2613-20260918.json`（10 次逐字替換＋附加 `factcheck`）。腳本：`<WORK>\_tools\tech-news-synology-dsm-sa2613-20260918\fc1-*.py|sh`；改前備份 `fc1-pack-before.json`、`fc1-record-before.json`。

## 摘要

- 主張 146 條：CONFIRMED 111、CHANGED 26、NOT FOUND 1（刪除）、OUT OF SCOPE 8。
- 第一輪事實修改：**16 個不同的事實**，落在 27 個主張位置（同一個「早於 7.2.1」的範圍錯誤就佔 8 處）；另有 2 處讀者優先的改寫（第一段歸因語、第二節第二段查證紀律敘述）與研究紀錄 3 處更正、1 條補充。超過十處 → `needs_second_round`（本來就排了第二輪）。
- 協調者點名先查的五件事：
  1. **補寫件日期**：事件日 2026-09-18 16:17（UTC+8）寫成事件日，全文「最近／本週／日前／剛剛」0 次；CISA SSVC 時間戳 19:14:05Z／19:13:10Z＝台北 9/19 03:14／03:13、美國 9/18，與公告日分開寫。守住。FAQ 4 與 callout 的「這是查核當下的評估」把評估時點說成查核日 → 改「那個時點的評估」。
  2. **嚴重程度**：Critical 2（13684、13639，CVSS 3.1 9.8，PR:N）、Important 2（13673 8.8、6205 8.1）、Moderate 2（13635 5.3、13623 4.8）、Low 2（13666 3.5、13683 2.7），逐條與公告 Detail 相符；標題「兩個免登入的 9.8 分漏洞」成立（9.8 恰好兩個、兩個都是 PR:N 且在「remote attackers」組；13635 也免登入但 5.3，正文已分開）。
  3. **遭利用**：三個 SSVC 值（none／yes／total）在第四節、summary、FAQ 4、callout 都並列；第五節「看 SSVC 評估是不是還維持在 none」只挑 none → 改「三個值有沒有改變」。KEV 全文 0 次。
  4. **版本**：四個修補版本與公告逐字相同、都帶「以上」。**「7.2.1 以前」與來源不合**：CVE 紀錄是 `version 0, lessThan 7.2.1 → unknown`，DSM 7.2.1 本身在 7.2.1-69057-12 以前是 `affected`，而且公告有列 DSM 7.2.1；「以前」可包含 7.2.1 本身，「DSM 7.2.1 以前的版本，公告沒有列」照字面是錯的 → 八處全改「早於 7.2.1」。協調者訊息寫的「7.2.1 and earlier are unknown」同樣與來源不合，**來源為準**。表格第五列：欄名改成「版本說明上的寫法與日期（末列為 CVE 紀錄）」、儲存格改「兩筆 CVE 紀錄標示為 unknown（未知）」、caption 補「兩筆 CVE 紀錄」。版本說明日期 6/16、6/30、6/30、7/29 只並列、不解釋落差；三個 Update 版本的 Fixed Issues 只有「Fixed security vulnerabilities (Synology-SA-26:06).」一條，7.4-90075 有十七條、最後兩條才是安全性修補 → 「7.4-90075 寫的是…」改「7.4-90075 寫的安全性修補是…」。
  5. **緩解**：None 照寫並歸給公告；callout「沒有其他暫時做法」是絕對否定 → 「沒有提供其他暫時做法」。第三節第三段與 FAQ 3 列舉「關閉 QuickConnect、連接埠轉發、防火牆設定或停用特定服務這類替代做法」違反研究紀錄 must_not_write 第 5 條（只准寫「公告沒有提供其他暫時做法」），兩處刪掉列舉。沒有畫面點選路徑；「到控制台（Control Panel）手動更新」是 7.4-90075 說明的原句，研究紀錄允許。自動更新不是保證：「不會通知／分地區推出」只有三個 Update 版本的說明有，callout 原本寫「這些更新」→ 改「三個 Update 版本的說明寫」。
- 字數：正文 2,991 → 2,877。騰出的空間來自刪掉的列舉與重複的查證紀律敘述，**沒有刪任何限定詞**。
- 自檢：`check_article.py` → `OK tech-news-synology-dsm-sa2613-20260918 zh-TW paragraphs 2877`（exit 0）；`pack_cli lint` 只有 `raw_internal_url` 警告與兩條 `image_missing`（exit 1，皆為預期）。

## 重抓結果（2026-09-26 台北 22:52 起，UTC 14:52）

`curl -sSL --max-time 30 --compressed -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥1.5 秒，請求不含任何人的姓名或 email。bytes 為落地檔案大小。原始檔：`<WORK>\_raw\tech-news-synology-dsm-sa2613-20260918\round1\`，逐筆紀錄在同目錄 `fetch-log.tsv`。

| 來源 | HTTP | bytes | 正文？ | 與研究代理的檔案比對 |
| --- | --- | --- | --- | --- |
| Synology-SA-26:13 DSM（sources 1） | 200 | 125,185 | 是，伺服器端算繪：Publish Time／Last Updated、Severity、Status、Abstract、Affected Products、Mitigation、Detail 八條、Revision | 位元組相同；Last Updated 仍 2026-09-18 16:17:35 UTC+8，Revision 仍只有 1 |
| CVE-2026-13684（sources 2） | 200 | 2,505 | 是 | 位元組相同；dateUpdated 2026-09-18T19:14:16.588Z 未變 |
| CVE-2026-13639（sources 3） | 200 | 2,474 | 是 | 位元組相同；dateUpdated 2026-09-18T19:13:24.287Z 未變 |
| DSM 版本說明資料（sources 4） | 200 | 746,801 | 是，JSON，391 筆，最新 7.3.2-86009 Update 4（2026-07-29） | 位元組相同 |
| 佐證：DSM 版本說明頁外殼 | 200 | 121,415 | Vue 外殼；`<title>Release Notes for DSM`、頁內 `$.ajax({url:"/api/releaseNote/findChangeLog"…identify="DSM"` | 位元組相同；證明 sources 4 是頁面自己載入的資料、標題正確 |
| 佐證：公告列表 | 200 | 144,090 | 是 | 位元組相同 |
| 佐證：CISA SSVC 頁 | 200 | 59,460（轉址到 /resources-tools/resources/…） | 是 | 研究代理沒有抓；網址來自 CISA BOD 26-04 頁的連結，不是猜的 |
| 佐證：《CISA SSVC Guide》PDF | 200 | 1,010,291 | 是，10 頁，pypdf 抽出 25,057 字 | 同上。Table 2：None＝「no evidence of active exploitation and no public proof of concept (PoC)」；答案要標時間點 |

研究紀錄 4 條 source 引文與 46 條 `verified_facts` 引文（含本輪補的一條）全部是今天抓檔裡的連續字串（`fc1-verify-after.txt`，0 failures）。四條來源以詞界比對 `Taiwan` 0 次；公告與兩筆 CVE 紀錄 `QuickConnect`、`firewall`、`PoC`、`exploit`、`KEV` 0 次。版本說明全份字串比對：`SA-26:13`、`SA_26_13`、八個 CVE 編號 0 次；`SA-26:06` 3 次（正是三個 Update 版本）。

## 改掉的地方（原文 → 改成什麼、來源原文、理由）

1. **「7.2.1 以前」→「早於 7.2.1」**（summary 4、第二節第一段、表格第五列、第三節第二段、FAQ 2、callout、圖片 alt、研究紀錄 diagram 第四格；八處）。CVE 紀錄 `{"lessThan":"7.2.1","status":"unknown","version":"0"}` 與 `{"lessThan":"7.2.1-69057-12","status":"affected","version":"7.2.1"}`；公告 Affected Products 有「DSM 7.2.1 … Upgrade to 7.2.1-69057-12 or above.」。「以前」在中文可以包含 7.2.1 本身，第三節「DSM 7.2.1 以前的版本，公告沒有列」照字面就是錯的；對 7.2.1 用戶也會被讀成「我的版本是未知」。研究紀錄 verified_facts 兩條、not_said 一條、editorial_brief 兩處同步更正。URL：https://cveawg.mitre.org/api/cve/CVE-2026-13684
2. **表格第五列與第三欄**：欄名「版本說明上的寫法與日期」→「版本說明上的寫法與日期（末列為 CVE 紀錄）」；第五列「7.2.1 以前版本／公告未列／CVE 紀錄標示為 unknown（未知）」→「早於 DSM 7.2.1 的版本／公告未列／兩筆 CVE 紀錄標示為 unknown（未知）」。原本 CVE 紀錄的狀態放在「版本說明」欄下，讀起來像版本說明的資料；改後每一格都說得出出自哪一頁。URL：同上與 https://cveawg.mitre.org/api/cve/CVE-2026-13639
3. **表格 caption**「依 Synology 資安公告 Synology-SA-26:13 與 DSM 版本說明整理」→「依 Synology 資安公告 Synology-SA-26:13、DSM 版本說明與兩筆 CVE 紀錄整理」。第五列出自 CVE 紀錄。
4. **第三節第二段：重新啟動**「三個 Update 版本會讓裝置重新啟動；7.4-90075 的版本說明寫，」→「四個修補版本的更新都會重新啟動裝置。7.4-90075 的說明另寫，」。7.4-90075 的說明也寫「This update will restart your Synology NAS.」；原句用分號對照，暗示 7.4-90075 不會重開。研究紀錄補一條 verified_fact。URL：https://www.synology.com/api/releaseNote/findChangeLog?identify=DSM&lang=en-global&model=&dsm_major=
5. **第三節第二段：「——這只針對 7.4 這個大版本更新」刪除（NOT FOUND）**。不能降級那句只出現在 7.4-90075 的說明（7.4.1-90080 也有），三個 Update 版本的說明對降級一個字都沒提；「只針對 7.4」把「沒寫」寫成「沒有這個限制」（BRIEF 第 2 型）。前面的「7.4-90075 的說明另寫」已把範圍講清楚。URL：同 4。
6. **第二節第二段：7.4-90075 的 Fixed Issues**「7.4-90075 寫的是 Ghostscript 的 CVE-2023-43115 與「多個安全性弱點」」→「7.4-90075 寫的安全性修補是…」。7.4-90075 的 Fixed Issues 是 17 條 `<li>`，前 15 條是 SSO、NFS、Link Aggregation、IPv6 等問題，最後兩條才是「Fixed security vulnerabilities regarding Ghostscript (CVE-2023-43115). Fixed multiple security vulnerabilities.」。三個 Update 版本的 Fixed Issues 確實只有「Fixed security vulnerabilities ( Synology-SA-26:06 ).」一條，照留。URL：同 4。
7. **第三節第三段、FAQ 3：刪掉替代做法的列舉**「以公告頁查核到 2026 年 9 月 26 日，沒有提到關閉 QuickConnect、連接埠轉發、防火牆設定或停用特定服務這類替代做法」→「（以公告頁查核到 2026 年 9 月 26 日）」。公告頁確實沒有這些字，但研究紀錄 must_not_write 第 5 條明寫「不寫關 QuickConnect、關連接埠轉發、關外網、改防火牆、停用服務、改密碼……有必要時只能寫『公告沒有提供其他暫時做法』」；「這類替代做法」等於把它們介紹成可行的替代做法（協調者：no workaround advice）。URL：https://www.synology.com/en-global/security/advisory/Synology_SA_26_13
8. **callout：緩解**「公告的緩解措施欄寫 None，沒有其他暫時做法。」→「…沒有提供其他暫時做法。」原句是超出公告頁的絕對否定；改成公告的說法（Mitigation None）。URL：公告。
9. **callout：通知與分地區**「DSM 版本說明寫，NAS 可能不會主動通知這些更新，而且採取分地區推出」→「三個 Update 版本的說明寫，…」。「may not notify you…not available in your region yet」只在 7.3.2／7.2.2／7.2.1 三個 Update 版本的說明裡；7.4-90075 的說明沒有這段（它寫的是自動更新沒執行時到控制台手動更新，以及列出的舊機型不會收到通知）。「這些更新」把範圍放大到四個版本。URL：同 4。
10. **FAQ 4、callout：評估時點**「這是查核當下的評估」→「這是那個時點的評估」。SSVC 時間戳是 2026-09-18T19:14:05Z／19:13:10Z，不是查核日；CISA SSVC Guide 也說答案反映的是分析當時的資訊、要標時間點（BRIEF 第 11 型）。URL：https://cveawg.mitre.org/api/cve/CVE-2026-13684
11. **FAQ 5 問句**「比公告日期早了兩三個月？」→「比公告日期還早？」。自己算的時間差（BRIEF 第 9 型），而且 7.3.2-86009 Update 4（2026-07-29）到 9/18 只有 51 天，「兩三個月」不成立。URL：同 4。
12. **第五節第一段：PoC 否定句**「還有幾件事，四份來源都沒有答案：公告與 CVE 紀錄都沒有寫出漏洞是否已有公開的攻擊程式或概念驗證；」→「還有幾件事查不到答案：公告沒有寫出漏洞是否已有公開的攻擊程式或概念驗證；」。CVE 紀錄的 SSVC Exploitation 值本身就是對 PoC 的判斷（CISA SSVC Guide Table 2：None＝沒有積極利用的證據、也沒有公開 PoC）；研究紀錄 not_said 第 1 條也只說「公告沒有提到」，並把 SSVC 評估列為「唯一的相關資料」。否定句限縮回公告。URL：公告。
13. **第五節第二段**「看 SSVC 評估是不是還維持在 none」→「看 SSVC 評估的三個值有沒有改變」。協調者：遭利用只透過三個值一起寫；原句也把「評估」等同於 Exploitation 一欄。URL：CVE 紀錄。
14. **第四節第一段**「CISA 沒有另外給分數」→「CISA 在 CVE 紀錄裡沒有另外給分數」。否定句限縮到讀過的頁（CISA-ADP 區塊只有 SSVC，沒有 CVSS）。URL：CVE-2026-13684。
15. **第一節第三段**「向量都是 AV:N、AC:L、PR:N、UI:N」→「向量都有…」。完整向量是 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`，四個指標是其中一部分。URL：公告。
16. **第三節第一段**「對照下表」→「對照上表」。表格在第二節末，位在這段之前。
17. **description** 補「（台北時間）」：時刻沒有時區，翻成四語時會變成沒有時區的 4:17 pm；第一段本來就寫了。188 字。
18. **第一段（讀者優先，協調者核准的改寫）**：原本有三個歸因語（「公告把…標為」「由 Synology 評為」「公告把它們歸在」），改成「這則公告的整體嚴重程度是 Critical、狀態是 Resolved；……屬於不需要登入的遠端攻擊者可利用的一組」，只留研究紀錄要求的「由 Synology 評為」。事實不變。
19. **第二節第二段（讀者優先）**：刪查證紀律的敘述「這裡只並列兩份來源各自的日期，不推論原因」→「這裡不推論」、「這裡只能寫『公告要求升到這些版本』，不能寫成版本說明修補了 SA-26:13」→「要求升到這些版本的是公告」（DELTA-4-7 第 14 條：查證紀律不寫進正文）。事實不變。

### 研究紀錄的更正（對來源是錯的，否則第二輪會照紀錄改回去）

- verified_fact（7.4-90075「到控制台手動更新」）與 not_said 第 5 條寫「這是來源裡唯一提到操作位置的句子」「四條來源裡提到操作位置的只有…」：sources 4 是全部 DSM 版本的說明，DSM 5.1（2014）與 6.1（2017）的說明寫「Control Panel > Update & Restore」、7.0 寫「Control Panel > Info Center」。改成「在四個修補版本的說明裡是唯一的」並註明舊版路徑不適用。正文「查看版本號的畫面路徑，四份來源都沒有寫」仍成立（那些路徑是更新或服務設定，不是看版本號），照留。
- 13684、13639 兩條 unknown 事實與 not_said、editorial_brief、diagram：「7.2.1 以前」→「早於 7.2.1」（見第 1 點）。
- 7.4-90075 Fixed Issues 那條：註明十七條裡只有最後兩條寫明 security vulnerabilities。
- 補一條 verified_fact：7.4-90075「This update will restart your Synology NAS.」。

## 主張表

C＝CONFIRMED、CH＝CHANGED、NF＝NOT FOUND、OOS＝OUT OF SCOPE。

| # | 位置 | 主張 | 判定 | 依據／備註 |
| --- | --- | --- | --- | --- |
| 1 | title | SA-26:13 是 Synology 對 DSM 的公告 | C | 「Synology-SA-26:13 DSM」 |
| 2 | title | 兩個免登入、9.8 分 | C | 9.8 恰好兩個，都是 PR:N、都在「remote attackers」組 |
| 3 | title | 先對版本號再更新 | OOS | 編輯建議 |
| 4 | description | 9/18 下午 4 點 17 分 | CH | 補（台北時間）（第 17 點） |
| 5 | description | Synology 發布 SA-26:13 | C | 公告 |
| 6 | description | 八個 CVE 編號 | C | Detail 八條；研究紀錄允許「公告列出的八個」 |
| 7 | description | 兩個 Critical、CVSS 3.1 9.8 | C | Detail |
| 8 | description | 不需要登入就可能被利用 | C | PR:N、「remote attackers」 |
| 9 | description | 緩解措施欄 None | C | 「Mitigation None」 |
| 10 | description | 188 字、句尾（2026 年 9 月查證） | C | 讀者優先規則 |
| 11 | 第一段 | 9/18 16:17 台北、Synology 發布 SA-26:13 DSM | C | Publish Time UTC+8 |
| 12 | 第一段 | DSM＝DiskStation Manager、Synology NAS 的作業系統 | C | 公告「Synology DiskStation Manager (DSM)」；版本說明「DSM operating system」「restart your Synology NAS」 |
| 13 | 第一段 | 整體 Critical、狀態 Resolved | C | 「Severity Critical Status Resolved」；歸因語改寫（第 18 點） |
| 14 | 第一段 | 八個裡兩個由 Synology 評為 Critical、9.8 | C | Detail |
| 15 | 第一段 | 屬於不需登入的遠端攻擊者可利用的一組 | C | Abstract 第一組；歸因語改寫 |
| 16 | 第一段 | 處理方式是升到各版本線的修補版本 | C | Affected Products |
| 17 | 第二段 | 2026-09-26 查核 | C | checked_on、sources、caption 一致 |
| 18 | 第二段 | 讀的是公告、兩筆 CVE 紀錄（含 CISA 評估）、版本說明 | C | sources[] 四條 |
| 19 | 第二段 | 沒有實測、不提供替代做法 | OOS | 固定句 |
| 20 | summary 1 | 9/18、SA-26:13、八個 CVE 編號 | C | |
| 21 | summary 1 | 13684、13639 Critical 9.8、不需登入 | C | |
| 22 | summary 2 | 其餘依序 Important 2、Moderate 2、Low 2 | C | Detail 順序 13673 I、6205 I、13635 M、13623 M、13666 L、13683 L；正文第四節逐條列出 |
| 23 | summary 2 | 多數需要已登入 | C | 五／六（PR:L×3、PR:H×2） |
| 24 | summary 3 | 緩解措施 None | C | |
| 25 | summary 3 | 四個修補版本與「以上」 | C | 與 Affected Products 逐字 |
| 26 | summary 4 | CISA 評估（台北 9/19 凌晨）三個值 | C | ADP ssvc |
| 27 | summary 4 | 到 9/26 沒有更新 | C | dateUpdated 未變、今天位元組相同 |
| 28 | summary 4 | DSM 7.2.1 以前 unknown | CH | 第 1 點 |
| 29 | 第一節 | 標題 | C | |
| 30 | 第一節 | 正式名稱 Synology-SA-26:13 DSM | C | |
| 31 | 第一節 | 發布 9/18 16:17（台北、UTC+8） | C | |
| 32 | 第一節 | 最後更新時間相同 | C | Last Updated 同值 |
| 33 | 第一節 | Revision 只有第 1 版、9/18 | C | 「Revision Date Description 1 2026-09-18」 |
| 34 | 第一節 | 查核到 9/26 沒有改版 | C | 今天位元組相同 |
| 35 | 第一節 | 讀者可回頁看 Last Updated 與 Revision | OOS | 讀者指引（兩個欄位確實在頁上） |
| 36 | 第一節 | 八個分三組 | C | Abstract 三句 |
| 37 | 第一節 | 13684、13639、13635 遠端攻擊者、不需登入 | C | |
| 38 | 第一節 | 後果依 CVE 不同：讀寫任意檔、阻斷服務、非敏感資訊 | C | |
| 39 | 第一節 | 13673、6205、13666 需已登入 | C | |
| 40 | 第一節 | 其中一種要受害者點分享網址 | C | 「when a victim clicks a sharing URL」 |
| 41 | 第一節 | 13623、13683 需管理員；有限檔案或非敏感資訊 | C | |
| 42 | 第一節 | Critical 9.8 只有兩個 | C | |
| 43 | 第一節 | 13684 在 SCGI | C | |
| 44 | 第一節 | 13639 在登入邏輯 | C | 「login logic」 |
| 45 | 第一節 | 向量都是 AV:N、AC:L、PR:N、UI:N | CH | 「都有」（第 15 點） |
| 46 | 第一節 | 即不需權限、不需互動、經網路 | C | PR:N、UI:N、AV:N |
| 47 | 第一節 | 13635 也不需登入，只是 Moderate、非敏感資訊 | C | |
| 48 | 第一節 | 緩解措施欄 None | C | |
| 49 | 第二節 | 標題 | C | |
| 50 | 第二節 | Affected Products 四條版本線 | C | |
| 51 | 第二節 | 都寫 or above | C | |
| 52 | 第二節 | 每列 Severity 都是 Critical | C | |
| 53 | 第二節 | 那是整列等級，不代表八個都是 Critical | C | Detail 等級各異 |
| 54 | 第二節 | 沒有列 DSM 7.1、7.0、6.2 | C | |
| 55 | 第二節 | CVE 紀錄對 7.2.1 以前標 unknown | CH | 第 1 點 |
| 56 | 第二節 | 版本說明日期 6/16～7/29 | C | 6/16、7/29、6/30、6/30 |
| 57 | 第二節 | 都早於 9/18 | C | |
| 58 | 第二節 | 以兩份來源查核到 9/26 沒有說明原因 | C | 限縮後的否定句；敘述精簡（第 19 點） |
| 59 | 第二節 | 三個 Update 版本 Fixed Issues 寫 SA-26:06 | C | 三筆都只有這一條 |
| 60 | 第二節 | 7.4-90075 寫的是 Ghostscript 與多個安全性弱點 | CH | 第 6 點 |
| 61 | 第二節 | 都沒有點名 SA-26:13 | C | 全份 0 次 |
| 62 | 第二節 | 要求升到這些版本的是公告 | C | 讀者優先改寫（第 19 點） |
| 63 | 表格 | 第三欄欄名 | CH | 第 2 點 |
| 64 | 表格 | DSM 7.4／7.4-90075 以上／7.4-90075，6/16 | C | |
| 65 | 表格 | DSM 7.3／7.3.2-86009-4 以上／Update 4，7/29 | C | 下載連結 7.3.2-86009-4 |
| 66 | 表格 | DSM 7.2.2／7.2.2-72806-9 以上／Update 9，6/30 | C | 下載連結 -9 |
| 67 | 表格 | DSM 7.2.1／7.2.1-69057-12 以上／Update 12，6/30 | C | 下載連結 -12 |
| 68 | 表格 | 第五列「7.2.1 以前版本」 | CH | 第 1 點 |
| 69 | 表格 | 第五列公告未列 | C | |
| 70 | 表格 | 第五列第三格 | CH | 第 2 點 |
| 71 | 表格 | caption 的來源 | CH | 第 3 點 |
| 72 | 表格 | caption：日期都早於 9/18 | C | |
| 73 | 第三節 | 標題 | OOS | |
| 74 | 第三節 | 對照「下表」 | CH | 第 16 點 |
| 75 | 第三節 | 看版本號的畫面路徑四份來源都沒寫 | C | 全份比對：只有舊版的更新／服務路徑與 7.4-90075「Info Center 顯示 GPU」，沒有看版本號的路徑 |
| 76 | 第三節 | 版本說明：未推到地區、系統評估不需更新而不通知 | C | 三個 Update 版本原文 |
| 77 | 第三節 | 沒通知不代表已是修補版 | C | 研究紀錄允許的推論 |
| 78 | 第三節 | 三個 Update 版本會重新啟動 | CH | 第 4 點 |
| 79 | 第三節 | 7.4-90075：自動更新沒執行時到控制台手動更新 | C | 「If auto update does not run, perform a manual update in Control Panel.」 |
| 80 | 第三節 | 7.4-90075：裝了不能降級 | C | 「you will not be able to downgrade」 |
| 81 | 第三節 | 這只針對 7.4 | NF | 刪除（第 5 點） |
| 82 | 第三節 | 7.2.1 以前公告沒列、unknown、沒有答案 | CH | 第 1 點 |
| 83 | 第三節 | 公告沒有更新以外的做法、None | C | |
| 84 | 第三節 | 沒提 QuickConnect、連接埠轉發、防火牆、停用服務 | CH | 刪列舉（第 7 點） |
| 85 | 第三節 | 公告與 CVE 紀錄沒有台數、地區、台灣 | C | Taiwan 0 次、沒有數量 |
| 86 | 圖片 | alt「7.2.1 以前」 | CH | 第 1 點 |
| 87 | 圖片 | caption：四個步驟、三種來源、查核日 | C | 與研究紀錄 diagram.caption 相同 |
| 88 | 研究紀錄 | diagram 第四格「7.2.1 以前」 | CH | 第 1 點 |
| 89 | 研究紀錄 | diagram 標題與前三格 | C | 「NAS 不一定會通知」出自三個 Update 版本 |
| 90 | 研究紀錄 | hero_label | OOS | |
| 91 | 第四節 | 標題「沒有已知利用」 | C | 研究紀錄的註解；CISA SSVC Guide Table 2 一致 |
| 92 | 第四節 | 9.8 是 Synology 的 CVSS 3.1 | C | CNA metrics |
| 93 | 第四節 | CNA 是 Synology | C | assignerShortName synology |
| 94 | 第四節 | CISA 沒有另外給分數 | CH | 第 14 點 |
| 95 | 第四節 | 13673 Important 8.8 LDAP API 需登入 | C | PR:L |
| 96 | 第四節 | 6205 Important 8.1 Upload API 需登入 | C | PR:L |
| 97 | 第四節 | 13635 Moderate 5.3 Auth API 不需登入、非敏感資訊 | C | PR:N |
| 98 | 第四節 | 13623 Moderate 4.8 Theme API 需管理員 | C | PR:H |
| 99 | 第四節 | 13666 Low 3.5 Sharing API 需登入且受害者點網址 | C | PR:L、UI:R |
| 100 | 第四節 | 13683 Low 2.7 EventScheduler API 需管理員 | C | PR:H |
| 101 | 第四節 | CISA 以 ADP 身分各補一次 SSVC | C | adp 各一個 ssvc 區塊 |
| 102 | 第四節 | 台北 9/19 凌晨、美國仍 9/18 | C | 19:14Z／19:13Z |
| 103 | 第四節 | 03:14 與 03:13 | C | |
| 104 | 第四節 | 三個欄位相同 none／yes／total | C | |
| 105 | 第四節 | 查核到 9/26 沒更新 | C | |
| 106 | 第四節 | 三個值要一起看 | OOS | 研究紀錄的編輯要求 |
| 107 | 第五節 | 標題 | OOS | |
| 108 | 第五節 | 四份來源都沒答案、公告與 CVE 紀錄都沒寫 PoC | CH | 第 12 點 |
| 109 | 第五節 | Affected Products 沒列機型、只列版本線 | C | |
| 110 | 第五節 | 公告沒說明為什麼晚於修補版本 | C | |
| 111 | 第五節 | 可回頁看 Last Updated、Revision | C | |
| 112 | 第五節 | 看 SSVC 是否還是 none | CH | 第 13 點 |
| 113 | 第五節 | 9/26 的狀態之後可能改變 | OOS | |
| 114 | FAQ 1 | 版本說明：未推到地區或系統評估而不通知 | C | |
| 115 | FAQ 1 | 對照四個修補版本 | C | |
| 116 | FAQ 2 | 表上沒有 7.1、7.0、6.2 | C | |
| 117 | FAQ 2 | CVE 紀錄對 7.2.1 以前 unknown | CH | 第 1 點 |
| 118 | FAQ 2 | 查核到 9/26 沒有答案 | C | |
| 119 | FAQ 3 | None＝公告沒有提供更新以外的做法 | C | |
| 120 | FAQ 3 | 列舉 QuickConnect 等 | CH | 第 7 點 |
| 121 | FAQ 3 | 處理方式是升級 | C | |
| 122 | FAQ 4 | 各一次評估、台北 9/19 凌晨（美國 9/18）、Exploitation none | C | |
| 123 | FAQ 4 | Exploitation＝是否已知遭利用 | C | SSVC Guide「Evidence of Active Exploitation of a Vulnerability」 |
| 124 | FAQ 4 | 到 9/26 沒更新 | C | |
| 125 | FAQ 4 | Automatable yes、Technical Impact total | C | |
| 126 | FAQ 4 | 查核當下的評估 | CH | 第 10 點 |
| 127 | FAQ 5 | 問句「早了兩三個月」 | CH | 第 11 點 |
| 128 | FAQ 5 | 6/16～7/29、早於 9/18 | C | |
| 129 | FAQ 5 | 兩份來源都沒說明原因 | C | 限縮到兩份來源 |
| 130 | FAQ 6 | 13684 SCGI、13639 登入邏輯 | C | |
| 131 | FAQ 6 | 9.8、不需權限、不需互動、經網路 | C | |
| 132 | FAQ 6 | 可能讓遠端攻擊者讀寫任意檔案並阻斷服務 | C | 「allows remote attackers to read or write arbitrary files and conduct denial-of-service attacks」 |
| 133 | FAQ 6 | 公告沒有進一步說明攻擊手法 | C | 只有 CWE 類別與一句描述 |
| 134 | callout | 9/18 公告、處理方式是升級 | C | |
| 135 | callout | 沒有其他暫時做法 | CH | 第 8 點 |
| 136 | callout | 版本說明：不會通知這些更新、分地區推出 | CH | 第 9 點 |
| 137 | callout | 沒通知不代表已修補、直接比對版本號 | C | |
| 138 | callout | CISA 三個值、台北 9/19 凌晨、到 9/26 沒更新 | C | |
| 139 | callout | 查核當下的評估 | CH | 第 10 點 |
| 140 | callout | 7.2.1 以前 unknown | CH | 第 1 點 |
| 141 | 連結 1 | 「2026 年科技新聞總整理：硬體、平台、電信與法規的重點」 | C | 與 tech-news-2026-index 的 zh-TW title 逐字相同；五語齊全 |
| 142 | 連結 2 | 「歐盟《網路韌性法》通報義務上路：9 月 11 日起，誰要多快通報」 | C | 與 tech-news-eu-cra-reporting-20260911 逐字相同；五語齊全 |
| 143 | sources 1 | 標題、網址、checked_on | C | 200、125,185 |
| 144 | sources 2 | 同上 | C | 200、2,505 |
| 145 | sources 3 | 同上 | C | 200、2,474 |
| 146 | sources 4 | 「Release Notes for DSM（DSM 版本說明頁載入的官方資料，en-global）」 | C | 外殼頁 `<title>` 與 `$.ajax` 呼叫 |

合計：C 111、CH 26、NF 1、OOS 8。

## 讀者優先檢查

- 「本文」0 次；「最近」「本週」「日前」「剛剛」0 次；KEV 與「已遭利用」0 次；簡體字 0（checker）。
- 第一段歸因語 3 → 1（第 18 點）。其餘段落：我把「X 表示／說明／寫／官方…」這類掛來源的動詞算成歸因語，描述文件本身的句子（例如「Severity 欄都寫 Critical」「修補版本都寫 or above」——這一節寫的就是那張表）不算；第三節第二段改寫後剩兩個，第二節第二段剩「以這兩份來源查核…官方沒有說明原因」與「Fixed Issues 欄位…寫的是」兩個。
- 「官方」剩 3 次：第二節第二段與 FAQ 5 各一次，都在「以這兩份來源查核到 2026 年 9 月 26 日」限縮的否定句裡；另一次是 sources 4 的標題。
- description 以「（2026 年 9 月查證）」結尾；title／description／summary 沒有選題數字（「八個 CVE 編號」是公告列出的數量，研究紀錄允許的寫法）。
- 正文的查證紀律敘述（「這裡只能寫…不能寫成…」）已刪；第二段的查核日句照 DELTA-4-7 第 14 條保留。

## 留給協調者

1. 兩筆 CVE 紀錄 CNA 區塊的 `defaultStatus` 是 `affected`：沒落在任何範圍的版本（例如各修補版本以上）在機器可讀欄位預設為 affected，與公告「or above」不一致，看起來是 CNA 的資料寫法。正文沒碰、不建議寫；提醒第二輪與翻譯不要從這欄推論。
2. 協調者訊息的「7.2.1 and earlier are unknown」與來源不合（見第 1 點）；翻譯指示若沿用這句，請改成「earlier than 7.2.1」。
3. CISA《SSVC Guide》的 None 定義（沒有積極利用證據、也沒有公開 PoC）與第四節標題、FAQ 4 的註解一致；這份指南不在 sources[]（上限四條），正文沒有引用它，也沒有替 Automatable／Technical Impact 下定義。
4. 第三節第一段與 FAQ 1 的「DSM 版本說明寫，NAS 可能…不會通知」只有三個 Update 版本的說明有這段；兩處沒說「這些更新」，照原文留著（對版本說明整體是真的）；callout 已限縮。第二輪可再判斷要不要也寫成「三個 Update 版本的說明」。
5. FAQ 5 的「不推論是延後公布或刻意等待」在否定句裡點名了 must_not_write 禁止的推論；事實沒錯，照留，要收緊可改「不推論原因」。
6. 研究紀錄 diagram 第四格已改「早於 7.2.1」，圖片 alt 同步；`build_assets.py` 畫圖時照新字。hero.alt 沒動。

## 自檢輸出（原樣）

```
OK tech-news-synology-dsm-sa2613-20260918 zh-TW paragraphs 2877
exit=0
```

```
tech-news-synology-dsm-sa2613-20260918
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/tech-news-synology-dsm-sa2613-20260918/hero.jpg
  error: image_missing: zh-TW: /guides/tech-news-synology-dsm-sa2613-20260918/diagram-1.svg
1 entries checked
exit=1
```

結論：`needs_second_round`（16 個事實修改，本來就排第二輪）。第二輪請優先重查第 1–19 點改動與新寫的句子：第三節第二段整段、第二節第二段、第五節第一段、表格第五列與欄名、callout 三處。
