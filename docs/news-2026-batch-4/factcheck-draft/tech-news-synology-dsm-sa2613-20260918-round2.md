# 查核報告（第二輪）：tech-news-synology-dsm-sa2613-20260918

- 查核者：獨立查核代理，第二輪（opus）；沒有參與撰稿，也沒有參與第一輪。
- 查核日：2026-09-26（台北）。規格：`FACTCHECK-48.md`、`docs/news-2026-batch-4/agents/tech/SECOND-ROUND.md`（第一輪規則 `agents/tech/FACTCHECK.md` 全部適用）、DELTA-4-8 全文、DELTA-4-7 第 3、4、10、11、14、16 條、BRIEF 十二條錯誤型態。
- 交付位置：`SECOND-ROUND.md` 寫「附加在同一份報告檔」，`FACTCHECK-48.md` 與指派訊息指定 `<WORK>\factcheck\<slug>-round2.md`；照後者，第一輪報告沒有動。
- 改動檔案：內容包 `apps/api/app/guides/content/tech-news-synology-dsm-sa2613-20260918.json`（6 次逐字替換）、研究紀錄 `docs/tech-news-2026/research/tech-news-synology-dsm-sa2613-20260918.json`（5 次逐字替換、1 次錯字修正、附加 `factcheck.second_round`）。腳本：`<WORK>\_tools\tech-news-synology-dsm-sa2613-20260918\fc2-*.py|sh`；改前備份 `fc2-pack-before.json`、`fc2-record-before.json`。沒有 json.dump，沒有跑 git。

## 摘要

- 主張 91 條：CONFIRMED 80、CHANGED 11（內容包 6 處、研究紀錄 5 處）、NOT FOUND 0、OUT OF SCOPE 0。範圍：第一輪改動或新寫的 35 處（27 個 CH／NF 位置、4 處讀者優先改寫、4 處研究紀錄更正）全部逐句回原文；第一輪 111 條 CONFIRMED 用固定種子（20260926）隨機抽 37 條；限定詞回掃 14 條；研究紀錄另 5 條。
- **第一輪的 19 點改動全部成立**，沒有一處要改回去。第一輪新寫的句子（「四個修補版本的更新都會重新啟動裝置」「7.4-90075 的說明另寫」「7.4-90075 寫的安全性修補是」「兩筆 CVE 紀錄標示為 unknown」「CISA 在 CVE 紀錄裡沒有另外給分數」「那個時點的評估」等）逐句都對得上今天抓到的原文。
- 這一輪改的三件事：
  1. **協調者裁定 2**：FAQ 5「官方都沒有說明原因，這裡只並列兩份來源各自的日期，不推論是延後公布或刻意等待」→「以公告與 DSM 版本說明查核到 2026 年 9 月 26 日，兩者都沒有說明原因。」
  2. **掉了「四份裡的三份」**：第三節第一段與 FAQ 1 寫「DSM 版本說明寫，NAS 可能…不會通知」，但這段只在 7.3.2、7.2.2、7.2.1 三個 Update 版本的說明裡，7.4-90075 的說明沒有（它寫的是自動更新沒執行時到控制台手動更新，以及列出的舊機型收不到通知）。兩處都改成「DSM 7.3.2、7.2.2、7.2.1 三個 Update 版本的說明寫」。第一輪只改了 callout，這兩處留作 open question。
  3. **掉了「以上」**：公告寫「Upgrade to … or above」，第一段、FAQ 3、callout 寫成「把 DSM 升到…修補版本」。對已經在更新版本的人（例如 7.4.1-90080），這讀起來像要升到一個比自己舊的版本。三處補「至少」。summary 與表格本來就有「以上」。
- 研究紀錄改了 5 處（見下），讓它與第一輪改過的正文一致，免得翻譯或第三輪照紀錄改回去。
- 字數：zh-TW 段落 2,877 → 2,908（≤3,000）。增加的字都是補回的限定詞，沒有刪任何限定詞。
- 自檢：`check_article.py` → `OK tech-news-synology-dsm-sa2613-20260918 zh-TW paragraphs 2908`（exit 0）；`pack_cli lint` 只有 `raw_internal_url` 警告與兩條 `image_missing`（exit 1，都是預期中的）。
- 結論：**ok**。

## 重抓結果（2026-09-26 台北 23:15 起，UTC 15:15）

`curl -sSL --max-time 30 --compressed -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔至少 1.5 秒，請求不含任何人的姓名或 email（`fc2-fetch.sh`）。原始檔：`<WORK>\_raw\tech-news-synology-dsm-sa2613-20260918\round2\`，逐筆紀錄在 `fetch-log.tsv`。

| 來源 | HTTP | 落地 bytes | 正文？ | 與第一輪比對 |
| --- | --- | --- | --- | --- |
| Synology-SA-26:13 DSM（sources 1） | 200 | 125,185 | 是（`<article>`：Publish Time／Last Updated 2026-09-18 16:17:35 UTC+8、Severity、Status、Abstract、Affected Products、Mitigation None、Detail 八條、Revision 只有 1） | 位元組相同 |
| CVE-2026-13684（sources 2） | 200 | 2,505 | 是（dateUpdated 2026-09-18T19:14:16.588Z） | 位元組相同 |
| CVE-2026-13639（sources 3） | 200 | 2,474 | 是（dateUpdated 2026-09-18T19:13:24.287Z） | 位元組相同 |
| DSM 版本說明資料（sources 4） | 200 | 746,801 | 是（JSON；`all_versions` 356 筆，第一筆 7.4.1-90080／2026-07-23） | 位元組相同 |
| 佐證：DSM 版本說明頁外殼 | 200 | 121,415 | Vue 外殼 | 位元組相同 |

研究紀錄 4 條 source 引文與 46 條 verified_facts 引文，用研究代理的比對規則對今天的檔案做連續字串比對（`fc2-verify.py`，前後兩次都是 0 failures）。沒有任何引文含 `...`、`…` 或 `|`。第 40–46 條（版本說明）同一句在整份資料裡出現多次，我逐條確認它們出現在紀錄指名的那個版本（`fc2-text.py rn` 的解碼全文）。

四份來源的字串計數（`fc2-ctx.py`，以詞界比對）：公告與兩筆 CVE 紀錄 `Taiwan`、`QuickConnect`、`firewall`、`PoC`、`exploit`、`KEV` 都是 0 次；版本說明 `SA-26:13`、`SA_26_13`、八個 CVE 編號 0 次，`SA-26:06` 3 次（就是三個 Update 版本）。

## 改掉的地方（原文 → 改成什麼、來源原文、理由）

### 內容包（6 處，3 件事）

1. **FAQ 5 答句（協調者裁定 2）**
   「…確實早於 9 月 18 日的公告發布日；以這兩份來源查核到 2026 年 9 月 26 日，官方都沒有說明原因，這裡只並列兩份來源各自的日期，不推論是延後公布或刻意等待。」→「…確實早於 9 月 18 日的公告發布日；以公告與 DSM 版本說明查核到 2026 年 9 月 26 日，兩者都沒有說明原因。」
   理由：原句在否定句裡點名了 must_not_write 禁止的推論，也多一個「官方」。改後只說兩份文件都沒有說明原因，與第二節第二段一致（FAQ ⊆ 正文）。URL：https://www.synology.com/api/releaseNote/findChangeLog?identify=DSM&lang=en-global&model=&dsm_major= 與 https://www.synology.com/en-global/security/advisory/Synology_SA_26_13
2. **第三節第一段**「DSM 版本說明寫，NAS 可能因為更新還沒推到某個地區，」→「DSM 7.3.2、7.2.2、7.2.1 三個 Update 版本的說明寫，NAS 可能因為更新還沒推到某個地區，」
   來源：三個 Update 版本的 Important notes 都寫「Your Synology NAS may not notify you of this DSM update because of the following reasons. … The update is not available in your region yet. … Your DSM is working fine without having to update.」。7.4-90075 的 Important Note 沒有這段，它寫的是「If auto update does not run, perform a manual update in Control Panel.」，以及列出的舊機型「won't receive notifications for this update on your DSM」。原句把四份裡三份的內容寫成版本說明整體的說法，用 DSM 7.4 的讀者會以為這段也適用他的版本（BRIEF 第 3 型：放大範圍）。URL：版本說明資料。
3. **FAQ 1**「不一定。DSM 版本說明寫，NAS 可能因為更新還沒推到你所在的地區，」→「不一定。DSM 7.3.2、7.2.2、7.2.1 三個 Update 版本的說明寫，NAS 可能因為更新還沒推到你所在的地區，」。理由同第 2 點。
4. **第一段**「處理方式是把 DSM 升到各版本線各自的修補版本。」→「處理方式是把 DSM 至少升到各版本線各自的修補版本。」
5. **FAQ 3**「處理方式就是把 DSM 升到公告列出的修補版本。」→「處理方式就是把 DSM 至少升到公告列出的修補版本。」
6. **callout**「處理方式是把 DSM 升到公告列出的修補版本；」→「處理方式是把 DSM 至少升到公告列出的修補版本；」
   第 4–6 點的來源：Affected Products 四列都是「Upgrade to 7.4-90075 or above.」這類寫法。三處掉了「or above」；已經在 7.4.1-90080（版本說明 2026-07-23，在「7.4-90075 or above」範圍內）的人照字面讀，會以為要「升到」一個比較舊的版本。URL：公告。

### 研究紀錄（5 處，對來源是錯的或與改過的正文不一致）

7. **verified_fact（7.4-90075 不能降級）**「這只針對 7.4 版本線的大版本更新，不要套到 7.3.2、7.2.2、7.2.1 的 Update 版本。」→「四個修補版本裡只有 7.4-90075 的說明寫這句；三個 Update 版本的說明對降級沒有寫，所以不要套到它們，也不要反過來寫成『只有 7.4 不能降級』（同一份資料裡 7.3.2-86009、7.2.2-72806、7.2.1-69057 這些大版本的說明也有同一句；第二輪查核更正）。」第一輪第 5 點從正文刪掉「這只針對 7.4 這個大版本更新」（NOT FOUND），紀錄卻還這樣寫；而且全文掃描顯示同一句也出現在 7.3.2-86009、7.3.1-86003、7.3-81180、7.2.2-72806、7.2.1-69057、7.2-64570 的說明，所以「只針對 7.4 版本線」本身就不對。
8. **editorial_brief**「版本說明寫 NAS『可能不會通知』有這些更新、而且分地區推出」→「三個 Update 版本的說明寫 NAS『可能不會通知』有這個更新、而且分地區推出…（第二輪查核更正：7.4-90075 的說明沒有這段）」。第 2 點的錯就是從這句來的。
9. **not_said**「版本說明只說 NAS『可能不會通知』與『分地區推出』。」→「三個 Update 版本的說明只說…，7.4-90075 的說明寫自動更新沒有執行時到控制台手動更新（第二輪查核更正）。」
10. **title_candidates 第 4 條**「DSM 7.2.1 以前公告沒有答案」→「早於 DSM 7.2.1 的版本公告沒有答案」（協調者裁定 1）。
11. **must_not_write 第 4 條**「不寫『7.2.1 以前的版本不受影響／很安全』」→「不寫『早於 7.2.1 的版本不受影響／很安全』…；範圍寫『早於 7.2.1』，不寫『7.2.1 以前』（DSM 7.2.1 本身在 7.2.1-69057-12 以前是 affected；第二輪查核更正）」（協調者裁定 1）。

第 10、11 點的來源：兩筆 CVE 紀錄都是 `{"lessThan":"7.2.1","status":"unknown","version":"0","versionType":"semver"}` 加上 `{"lessThan":"7.2.1-69057-12","status":"affected","version":"7.2.1",…}`。URL：https://cveawg.mitre.org/api/cve/CVE-2026-13684、https://cveawg.mitre.org/api/cve/CVE-2026-13639

另外修了我自己在 `second_round.open_questions` 寫錯的位置（「第一段第三節」→「第一節第三段」，`fc2-fix.py`）。

## 協調者裁定的落實

1. **早於 7.2.1**：正文七處（summary 4、第二節第一段、表格第五列、第三節第二段、FAQ 2、callout、圖片 alt）與研究紀錄 diagram 第四格都是「早於（DSM）7.2.1」，逐一核對過。研究紀錄 verified_facts 第 22、26 條、not_said 第 4 條、editorial_brief 兩處也已經是「早於」。還留著「7.2.1 以前」的兩處（title_candidates、must_not_write）這一輪已改。第一輪 factcheck 物件裡的 `before` 是歷史紀錄，沒有動。
2. **FAQ 5**：已改（第 1 點）。
3. **defaultStatus**：正文、verified_facts、not_said、must_not_write、editorial_brief 沒有任何一句以 `defaultStatus` 為依據。FAQ 2「不是『不受影響』，也不是『受影響』」依據的是 `lessThan 7.2.1` 那一列的 `unknown`。第一輪 `factcheck.open_questions` 第 1 條提到這一欄，屬於第一輪的歷史紀錄，沒有動；翻譯不要從它推論。
4. **KEV、替代做法、操作路徑**：KEV、「已遭利用」、QuickConnect、防火牆在內容包都是 0 次。唯一的操作位置是 7.4-90075 說明原句裡的「到控制台（Control Panel）手動更新」。我掃了整份版本說明的 `Info Center`、`Update & Restore`、`Control Panel >`：`Update & Restore` 只出現在 5.1、5.2、6.0、6.1 的說明；`Info Center` 出現在 5.1、7.0（服務分頁），以及 7.4-90075 的「Added display for GPU information in Info Center.」。三者都不是查看版本號的路徑，所以「查看版本號的畫面路徑，四份來源都沒有寫」成立。

## 主張表

C＝CONFIRMED、CH＝CHANGED。「R1#」是第一輪主張表的編號。

### A. 第一輪改動或新寫的句子（35 條，全部重查）

| # | R1# | 位置 | 主張（第一輪改後） | 判定 | 依據 |
| --- | --- | --- | --- | --- | --- |
| A1 | 4 | description | 下午 4 點 17 分（台北時間） | C | 「Publish Time: 2026-09-18 16:17:35 UTC+8」 |
| A2 | 28 | summary 4 | 早於 DSM 7.2.1 的版本，CVE 紀錄標示為 unknown（未知） | C | 兩筆紀錄都是 version 0／lessThan 7.2.1／unknown |
| A3 | 45 | 第一節第三段 | 向量都有 AV:N、AC:L、PR:N、UI:N | C | 兩條都是 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| A4 | 55 | 第二節第一段 | CVE 紀錄對早於 7.2.1 的版本標 unknown，不是「不受影響」 | C | 同 A2 |
| A5 | 60 | 第二節第二段 | 7.4-90075 寫的安全性修補是 Ghostscript CVE-2023-43115 與「多個安全性弱點」 | C | Fixed Issues 17 條，第 16、17 條是「Fixed security vulnerabilities regarding Ghostscript (CVE-2023-43115).」「Fixed multiple security vulnerabilities.」 |
| A6 | 63 | 表格 | 欄名「版本說明上的寫法與日期（末列為 CVE 紀錄）」 | C | 第五列出自 CVE 紀錄 |
| A7 | 68 | 表格第五列 | 早於 DSM 7.2.1 的版本 | C | 同 A2 |
| A8 | 70 | 表格第五列 | 兩筆 CVE 紀錄標示為 unknown（未知） | C | 13684、13639 都有這一列 |
| A9 | 71 | caption | 依公告、DSM 版本說明與兩筆 CVE 紀錄整理 | C | 三種來源各撐一部分表格 |
| A10 | 74 | 第三節第一段 | 對照上表 | C | 表格在第二節末，位在這段之前 |
| A11 | 78 | 第三節第二段 | 四個修補版本的更新都會重新啟動裝置 | C | 三個 Update 版本「This update will restart the device.」；7.4-90075「This update will restart your Synology NAS.」 |
| A12 | 81 | 第三節第二段 | 刪掉「這只針對 7.4 這個大版本更新」 | C | 刪得對：三個 Update 版本的說明對降級沒有寫；而且同一句也出現在 7.3.2-86009 等大版本（紀錄第 7 點同步） |
| A13 | 82 | 第三節第二段 | 早於 DSM 7.2.1：公告沒列、CVE 紀錄 unknown、公告沒有給答案 | C | Affected Products 只有四列 |
| A14 | 84 | 第三節第三段 | 公告沒有提供更新以外的做法，緩解措施欄寫 None（以公告頁查核到 9/26） | C | 「Mitigation None」；列舉已刪，符合 must_not_write 第 5 條 |
| A15 | 86 | 圖片 alt | 「…手動更新、早於 7.2.1」 | C | 與 diagram nodes 一致 |
| A16 | 88 | 紀錄 diagram | 第四格「早於 7.2.1／CVE 紀錄標 unknown」 | C | 同 A2 |
| A17 | 94 | 第四節第一段 | CISA 在 CVE 紀錄裡沒有另外給分數 | C | `adp` 只有 `ssvc`，沒有 `cvssV3_1` |
| A18 | 108 | 第五節第一段 | 查不到答案：公告沒有寫出是否已有公開攻擊程式或概念驗證 | C | 公告 PoC／exploit／proof of concept 0 次 |
| A19 | 112 | 第五節第二段 | 看 SSVC 評估的三個值有沒有改變 | C | 三個 options 並列 |
| A20 | 117 | FAQ 2 | 兩筆 CVE 紀錄對早於 7.2.1 標 unknown，不是不受影響、也不是受影響 | C | 依據是 unknown 那一列，不是 defaultStatus |
| A21 | 120 | FAQ 3 | 列舉刪除，只說公告沒有提供更新以外的做法 | C | 同 A14 |
| A22 | 126 | FAQ 4 | 這是那個時點的評估 | C | SSVC timestamp 2026-09-18T19:14:05Z／19:13:10Z |
| A23 | 127 | FAQ 5 問句 | 「比公告日期還早？」 | C | 6/16–7/29 早於 9/18，問句不帶自己算的間隔 |
| A24 | 135 | callout | 沒有提供其他暫時做法 | C | Mitigation None；must_not_write 允許的寫法 |
| A25 | 136 | callout | 三個 Update 版本的說明寫，NAS 可能不會主動通知、分地區推出 | C | 三個 Update 版本原文；「分地區推出」是研究紀錄允許的寫法 |
| A26 | 139 | callout | 那個時點的評估，不是保證 | C | 同 A22 |
| A27 | 140 | callout | 早於 DSM 7.2.1 的版本 CVE 紀錄標 unknown | C | 同 A2 |
| A28 | 13 | 第一段 | 這則公告的整體嚴重程度是 Critical、狀態是 Resolved | C | 「Severity Critical Status Resolved」 |
| A29 | 15 | 第一段 | 屬於不需要登入的遠端攻擊者可利用的一組 | C | Abstract 第一句「remote attackers」，對照第二、三句的「remote authenticated users」；PR:N |
| A30 | 58 | 第二節第二段 | 以兩份來源查核到 9/26，官方沒有說明原因，這裡不推論 | C | 公告與版本說明都沒有說明；限縮到兩份來源 |
| A31 | 62 | 第二節第二段 | 要求升到這些版本的是公告 | C | Affected Products |
| A32 | — | 紀錄 fact 41、not_said 5 | 「到控制台手動更新」在四個修補版本的說明裡是唯一提到操作位置的句子；舊版另有舊介面路徑 | C | `fc2-ctx.out`：Update & Restore 在 5.1、5.2、6.0、6.1。7.4-90075 的 What's New 另有「Info Center」顯示 GPU，是功能描述不是操作，不影響 |
| A33 | — | 紀錄 fact 22／26、not_said 4、editorial_brief | 「早於 7.2.1」 | C | 同 A2 |
| A34 | — | 紀錄 fact 46 | 7.4-90075 Fixed Issues 十七條，最後兩條寫明 security vulnerabilities | C | 同 A5 |
| A35 | — | 紀錄 fact 40（第一輪新增） | 7.4-90075「This update will restart your Synology NAS.」 | C | 在 7.4-90075 的 Important Note 第二句 |

### B. 第一輪 CONFIRMED 隨機抽三分之一（37 條；`random.seed(20260926)`、`random.sample(111 條, 37)`）

| # | R1# | 位置 | 主張 | 判定 | 依據 |
| --- | --- | --- | --- | --- | --- |
| B1 | 2 | title | 兩個免登入、9.8 分 | C | 13684、13639 都是 9.8、PR:N |
| B2 | 5 | description | Synology 發布 SA-26:13 | C | 公告 |
| B3 | 7 | description | 兩個 Critical、CVSS 3.1 9.8 | C | Detail |
| B4 | 8 | description | 不需要登入就可能被利用 | C | PR:N、「remote attackers」；「可能」有保留 |
| B5 | 9 | description | 緩解措施欄 None | C | 「Mitigation None」 |
| B6 | 12 | 第一段 | DSM＝DiskStation Manager、Synology NAS 的作業系統 | C | 公告「Synology DiskStation Manager (DSM)」；版本說明「DSM operating system」「restart your Synology NAS」 |
| B7 | 17 | 第二段 | 2026-09-26 查核 | C | sources checked_on、caption、紀錄一致 |
| B8 | 18 | 第二段 | 讀的是公告、兩筆 CVE 紀錄（含 CISA 評估）、版本說明 | C | sources[] 四條 |
| B9 | 20 | summary 1 | 9/18、SA-26:13、八個 CVE 編號 | C | Detail 八條 |
| B10 | 24 | summary 3 | 緩解措施 None | C | |
| B11 | 27 | summary 4 | 到 9/26 沒有更新 | C | dateUpdated 未變，今天位元組相同 |
| B12 | 29 | 第一節標題 | 9 月 18 日的公告寫了什麼 | C | |
| B13 | 30 | 第一節第一段 | 正式名稱 Synology-SA-26:13 DSM | C | |
| B14 | 33 | 第一節第一段 | Revision 只有第 1 版、9/18 | C | 「Revision Date Description 1 2026-09-18」 |
| B15 | 34 | 第一節第一段 | 查核到 9/26 沒有改版 | C | Last Updated＝Publish Time |
| B16 | 36 | 第一節第二段 | 八個分三組 | C | Abstract 三句 |
| B17 | 37 | 第一節第二段 | 13684、13639、13635 遠端攻擊者、不需登入 | C | |
| B18 | 38 | 第一節第二段 | 後果依個別 CVE 不同，可能是讀寫任意檔案、阻斷服務或非敏感資訊 | C | 原文用「or」；「依個別 CVE 不同」與 Detail 相符 |
| B19 | 46 | 第一節第三段 | 即不需權限、不需互動、經網路 | C | PR:N、UI:N、AV:N |
| B20 | 48 | 第一節第三段 | 緩解措施欄 None | C | |
| B21 | 50 | 第二節第一段 | Affected Products 四條版本線 | C | 7.4、7.3、7.2.2、7.2.1 |
| B22 | 51 | 第二節第一段 | 都寫 or above | C | 四列都有 |
| B23 | 54 | 第二節第一段 | 沒有列 DSM 7.1、7.0、6.2 | C | |
| B24 | 61 | 第二節第二段 | 版本說明都沒有點名 SA-26:13 | C | 全份 0 次 |
| B25 | 67 | 表格 | DSM 7.2.1／7.2.1-69057-12 以上／Update 12，2026 年 6 月 30 日 | C | 公告；`{"version":"7.2.1-69057 Update 12","publish_date":"2026-06-30"`；下載連結 7.2.1-69057-12 |
| B26 | 79 | 第三節第二段 | 7.4-90075：自動更新沒執行時到控制台手動更新 | C | 「If auto update does not run, perform a manual update in Control Panel.」 |
| B27 | 80 | 第三節第二段 | 7.4-90075：裝了之後沒辦法降級 | C | 「After installing this update, you will not be able to downgrade to a previous DSM version.」 |
| B28 | 87 | 圖片 caption | 四個步驟、三種來源、查核日 | C | 與紀錄 diagram.caption 逐字相同 |
| B29 | 91 | 第四節標題 | 「沒有已知利用」 | C | Exploitation none；紀錄的註解 |
| B30 | 97 | 第四節第一段 | 13635 Moderate 5.3 Auth API 不需登入、非敏感資訊 | C | PR:N、C:L；「obtain non-sensitive information」 |
| B31 | 98 | 第四節第一段 | 13623 Moderate 4.8 Theme API 需管理員權限 | C | PR:H；「with administrator privileges」 |
| B32 | 99 | 第四節第一段 | 13666 Low 3.5 Sharing API 需登入且受害者點分享網址 | C | PR:L、UI:R；「when a victim clicks a sharing URL」 |
| B33 | 101 | 第四節第二段 | CISA 以 ADP 身分在兩筆紀錄各補一次 SSVC | C | 各一個 adp 區塊、一個 ssvc |
| B34 | 103 | 第四節第二段 | 13684 台北 3 點 14 分、13639 3 點 13 分 | C | 19:14:05Z、19:13:10Z，加 8 小時 |
| B35 | 116 | FAQ 2 | 表上沒有 7.1、7.0、6.2 | C | |
| B36 | 118 | FAQ 2 | 查核到 9/26 都沒有給出答案 | C | |
| B37 | 130 | FAQ 6 | 13684 在 SCGI、13639 在登入邏輯 | C | 「in SCGI」「in login logic」 |

### C. 限定詞回掃（14 條）

| # | 位置 | 主張 | 判定 | 依據／處理 |
| --- | --- | --- | --- | --- |
| C1 | 第三節第一段 | 「DSM 版本說明寫，NAS 可能…不會通知」 | CH | 改第 2 點（四份裡的三份） |
| C2 | FAQ 1 | 同上 | CH | 改第 3 點 |
| C3 | 第一段 | 升到修補版本 | CH | 補「至少」（第 4 點） |
| C4 | FAQ 3 | 同上 | CH | 第 5 點 |
| C5 | callout | 同上 | CH | 第 6 點 |
| C6 | FAQ 5 答句 | 不推論是延後公布或刻意等待 | CH | 協調者裁定 2（第 1 點） |
| C7 | summary 3、表格 | 四個修補版本都帶「以上」 | C | 與 Affected Products 逐字相符 |
| C8 | description、第一節第二段、第三節第一段、FAQ 1、callout、FAQ 6 | 「可能」都還在 | C | 原文 may／allows；沒有被強化 |
| C9 | 七處 unknown | 都帶「（未知）」，沒有寫成不受影響或受影響 | C | CVE 紀錄 |
| C10 | callout | 「分地區推出」 | C | 「not available in your region yet … may vary slightly」；已限縮在三個 Update 版本 |
| C11 | 第二節第二段、FAQ 5 | 6 月 16 日到 7 月 29 日之間、早於 9/18 | C | 6/16、7/29、6/30、6/30；沒有自己算的間隔 |
| C12 | 第三節第一段 | 查看版本號的畫面路徑，四份來源都沒有寫 | C | 全份掃描，見「協調者裁定的落實」第 4 點 |
| C13 | 第三節第三段 | 公告與兩筆 CVE 紀錄沒有裝置數量、地區分布、台灣資訊 | C | Taiwan 0 次，沒有數量 |
| C14 | 兩個結尾連結 | 文字與目標 zh-TW title 逐字相同、目標五語齊全 | C | tech-news-2026-index、tech-news-eu-cra-reporting-20260911 都是 en／ja／ko／zh-CN／zh-TW |

### D. 研究紀錄（5 條，全部 CH，見「改掉的地方」第 7–11 點）

| # | 位置 | 判定 |
| --- | --- | --- |
| D1 | verified_fact「7.4-90075 不能降級」的「只針對 7.4 版本線」 | CH |
| D2 | editorial_brief「版本說明寫…有這些更新」 | CH |
| D3 | not_said「版本說明只說…」 | CH |
| D4 | title_candidates 第 4 條「7.2.1 以前」 | CH |
| D5 | must_not_write 第 4 條「7.2.1 以前」 | CH |

合計：91 條，C 80、CH 11（C1–C6 這 6 條對應內容包的 6 處替換：C1、C2 各一處，C3–C5 各一處，C6 一處；D1–D5 是研究紀錄）。

## 讀者優先與界線

- 「本文」0 次；「最近」「本週」「日前」「剛剛」0 次；KEV、「已遭利用」0 次；「官方」3 → 2 次（第二節第二段的限縮否定句，以及 sources 4 的標題）。
- 第一段歸因語：「由 Synology 評為」1 個。改過的兩段：第三節第一段是「四份來源都沒有寫」「三個 Update 版本的說明寫」兩個；FAQ 5 沒有歸因語。
- description 188 字，以「（2026 年 9 月查證）」結尾；title／description／summary 沒有選題數字。
- 界線（SECOND-ROUND 第 5 條）：topics 是 tech、tech-news、software，沒有 finance；沒有投資免責 callout；只有一個 callout；沒有購買或換機建議（「至少升到修補版本」是公告自己的要求，不是升級建議）；沒有推定台灣可用；沒有替代做法。
- summary ⊆ 正文、FAQ ⊆ 正文：FAQ 1、FAQ 5 改後與第三節第一段、第二節第二段一致；diagram 的數字（7.2.1）在正文。

## 留給協調者

1. 第一輪報告寫版本說明資料「391 筆」：實際上是 `all_versions` 356 筆，加上 `versions.DSM.7.4` 的 2 筆與 `6.2` 的 33 筆。正文與研究紀錄都沒有用這個數字，不影響文章。
2. FAQ 6「向量都是不需要權限、不需要使用者互動，就能經網路利用」是在描述向量的性質，不是列出完整向量（第一節第三段已寫「向量都有 AV:N、AC:L、PR:N、UI:N」）。沒有改；翻譯時不要譯成「the vectors are AV:N/PR:N/UI:N」。
3. 第五節第一段「查不到答案：公告沒有寫出…概念驗證」只限縮到公告。依 CISA 自己的定義，SSVC 的 Exploitation none 也涵蓋「沒有公開 PoC」，但那份定義不在 sources[]，正文不解釋，沿用第一輪的處理。
4. 翻譯提醒：第 2、3 點的「DSM 7.3.2、7.2.2、7.2.1 三個 Update 版本的說明」與第 4–6 點的「至少」（at least／or above）都是限定詞，四語要保留。

## 自檢輸出（原樣）

```
OK tech-news-synology-dsm-sa2613-20260918 zh-TW paragraphs 2908
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

```
46 facts checked, 0 failures   (fc2-verify.py，改後)
```

結論：**ok**。第一輪的改動全部成立；這一輪改了 11 處（內容包 6、研究紀錄 5），都是限定詞、範圍與協調者裁定，沒有動到骨幹論述。
