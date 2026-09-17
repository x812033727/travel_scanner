# 獨立查核：tech-news-eu-cra-reporting-20260911

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，六處一致，不改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body。
第四條在查核中段整段時間讀不到（見下），期間改用執委會自己的三份實施文件反駁條文相關敘述——
它們只寫進本報告與研究紀錄，**沒有進 `sources[]`，文章也沒有引用它們獨有的內容**；
出版局恢復後，所有條文敘述又以《歐盟公報》全文逐條複驗了一次。
任何請求都沒有放入 email、姓名或任何個人資料，也沒有猜任何識別碼：
CELEX 32024R2847、cellar UUID、download-handler 網址全部取自已讀到的頁面上的 `href`／`data-uri`。

檢查的主張：**96 條**（正文 17 段、summary 4 句、FAQ 6 題答句、表格 4 列與 caption、
圖解 caption 與四格、callout、title、description；`hero.alt` 依規格不查不改）。
內容包改了 **16 處**，研究紀錄改了 6 處，另有 4 件留給站主。

## 重抓結果：第四條中途整個出版局倒了，後來恢復

| source | HTTP | bytes | body 是不是正文 |
| --- | --- | --- | --- |
| 執委會 cra-reporting | 200 | 52,986 | 是。`Last update 11 September 2026`，與紀錄相同 |
| ENISA 啟用新聞稿 | 200 | 49,879 | 是。`Sep 11,2026`、`initial operating capability` |
| ENISA 常見問答 | 200 | 79,220 | 是。31 題，`Updated: 17 September 2026`（**第 9 題標示 `[UPDATED]`，內容已改**） |
| CELLAR `celex/32024R2847` | **500／502 → 200** | 237／122 → **710,696** | 中斷時是 `Unable to acquire JDBC Connection` 的 Hibernate 例外；恢復後是《歐盟公報》全文 |

第四條連續試 **八次**，全部 500 或 502，帶不帶 `Accept-Language: eng` 都一樣。
不是這一條壞掉，是整個出版局中斷了一段時間：

- `op.europa.eu` 的 `download-handler`（`format=xhtml|pdfa2a`、`language=en`，網址取自紀錄頁的 `data-uri`）回 **204／0 bytes**；
- `law-tracker.europa.eu` 回 **503**；
- `eur-lex.europa.eu` 用真實瀏覽器開啟，直接轉到 `TodayOJ` 並印出
  **「EUR-Lex is temporarily not fully available.」**（對 `curl` 則照舊是 202／0 bytes 的 WAF）。

唯一還活著的出版局端點是紀錄頁 `op.europa.eu/…/21b7d4eb-a6e2-11ef-85f0-01aa75ed71a1`
（200、552,233 bytes），但它只有中繼資料，沒有條文。

中斷期間改讀執委會自己託管在 `ec.europa.eu`、不受影響的三份文件：
CRA 實施常見問答（PDF，66 頁、169,657 字）、實施指引 C(2026) 5252 附件（PDF，84 頁、251,378 字）、
以及 `cra-summary` 頁（200、123,150 bytes）。

**後來出版局恢復，第四條回到 HTTP 200、710,696 bytes——與撰稿者記錄的位元組數完全相同**，
`sourcing_notes` 的取得配方（`Accept-Language: eng`）也重現無誤。
我因此把所有條文敘述回到《歐盟公報》全文逐條複驗：
第 2(1)、3(42)、13(8)–(9)、14(1)–(8)、15、16(1)–(2)、17(4)–(6)、24(3)、64(1)–(2) 與 (10)、69(2)–(3)、71(1)–(2)，全部命中。
`checked_on` 沒有改。

## 改掉的 16 處

1. **「次要代表只能看到自己送出的通報，主要代表能看到該製造商全部通報」被今天的來源推翻**（第 5 節第 3 段）。
   ENISA 常見問答第 9 題今天標著 `[UPDATED]`，寫的是
   「Primary and Secondary ARs associated with the same manufacturer can access, view, and update
   notifications associated with that manufacturer, regardless of with AR originally submitted them.」
   （`with` 是來源自己的錯字，應為 `which`，照印）
   下面接「The only exception concerns draft notifications. Drafts are stored locally in the individual
   AR's account…」。已改成「主要與次要代表都看得到該製造商的通報，不分原本是誰送出，只有尚未送出的草稿留在各自帳號裡」。
   **這是全篇唯一被推翻的事實，而且是查核當天才被改掉的**——研究紀錄原本寫「內容沒有變動，只是頁面被重新發布」，該句已更正。

2. **「第 16 條依文義要到 2027 年 12 月 11 日才輪到」這個推論刪掉**（第 3 節第 3 段）。
   這是撰稿者自己點名要重查的第 2 點，判斷是：**不該寫**。
   第 71 條第 2 項只提前第 14 條與第四章，這一點沒錯；但執委會的通報頁寫著
   「Pursuant to Article 16 of the CRA…ENISA has established the CRA SRP, operational as of 11 September 2026.」，
   ENISA 常見問答第 2 題更直接寫「The legal basis for the operation of the SRP is the CRA, which states in Art. 16(1)」。
   文章拿「不在清單裡」推出「尚未適用」，等於和兩個官方頁對立。
   已改成只寫可驗證的兩件事：清單裡沒有第 16 條；執委會與 ENISA 都寫明平台依第 16 條建立並自 9 月 11 日起運作。

3. **同一個推論從罰則段與 FAQ 第 6 題刪掉**（第 4 節第 3 段、FAQ 6）。這是撰稿者點名的第 1 點。
   回原文核對的結果分成兩半：
   - 「第 64 條不在第 71 條第 2 項列出的提前適用條文裡」**成立**——全文恢復後確認第 64 條在
     `CHAPTER VII CONFIDENTIALITY AND PENALTIES`（自第 63 條起），不是被提前的第四章；
     執委會 `cra-summary` 的章節表也放在第七章（`Confidentiality and penalties (Articles 63-63)`，
     `63-63` 是該頁自己的錯字）。第 71 條第 2 項的原文是
     「This Regulation shall apply from 11 December 2027. However, Article 14 shall apply from
     11 September 2026 and Chapter IV (Articles 35 to 51) shall apply from 11 June 2026.」
   - 「依文義要到 2027 年 12 月 11 日才適用」**不成立，已刪**。執委會實施指引第 210 段寫
     「In accordance with **Article 69(3) and 71(2), second sentence**, the obligation to comply with
     Article 14 applies from 11 September 2026 to all products…」——**第 69 條第 3 項同樣不在提前清單裡，
     執委會卻正在用它**。所以「不在清單＝還沒適用」不是安全的推論，而文章自己第 4 節第 1 段就靠這一條。
   - 「官方沒說明會不會被罰」**成立但範圍要限縮**：三條來源以 `penalt`／`fine`／`sanction`／金額字串搜尋
     **全部 0 次**，已改寫成「本文查到的三個官方頁面都沒有提到罰鍰，也沒有說明…」。
   同段另補回罰鍰的條件：第 64 條第 2 項原文是
   「administrative fines of up to EUR 15 000 000 or, **if the offender is an undertaking**,
   up to 2,5 % of **the its** total worldwide annual turnover for the preceding financial year,
   whichever is higher.」（`of the its` 是《歐盟公報》自己的錯字，照抄不訂正）——
   正文漏了「違規企業」這個條件（FAQ 有，正文沒有），已補齊。

4. **第 13 條兩個數字的但書補回**（FAQ 5）。原文寫「訂出至少 5 年的維護支援期，安全更新至少要保留 10 年」，
   兩個數字都掉了條文自己的條件：
   - 第 13 條第 8 項第三款：「the support period shall be at least five years. **Where the product with
     digital elements is expected to be in use for less than five years, the support period shall
     correspond to the expected use time.**」（執委會實施指引第 126 段與實施常見問答 4.5.2 也各寫一次）
   - 第 13 條第 9 項：安全更新「**remains available after it has been issued for a minimum of 10 years
     or for the remainder of the support period, whichever is longer**」。
   已補成「至少 5 年，但預期使用時間不到 5 年時支援期等於預期使用時間」與
   「至少保留 10 年，或保留到支援期結束為止，取其長」。
   （中間曾因 `sources[3]` 不可讀、且兩份執委會文件以詞界搜尋 `10 years`／`ten years` 各 0 次而一度刪掉 10 年，
   出版局恢復後在第 13 條第 9 項找到原文，已還原並補上但書。）

5. **開源軟體維護者在 FAQ 5 的義務補上範圍限制**，與下面第 8 點同一個問題。

6. **第 14 條第 2 項的「不得無故延遲」補回**（第 2 節第 2 段）。
   ENISA 常見問答第 7 題印的是「Without undue delay and in any case within 24 hours」，
   第 26 題又特別重申「the requirement to report upon becoming aware, without undue delay」。
   只寫「24 小時內」會讓人以為撐到 23 小時 59 分都沒事。

7. **「遇到漏洞或事故」改成「遇到遭積極利用的漏洞或重大資安事故」**（第 4 節第 1 段）。
   第 14 條只涵蓋這兩種，全篇其他地方都寫對了，只有這一句放大了範圍。

8. **開源軟體維護者的義務補上範圍限制**（第 1 節第 2 段、FAQ 5）。
   ENISA 新聞稿是「to the extent that they are involved in the development of products with digital
   elements」，文章寫成「同一種義務」「相同的通報義務」，已補「以其涉入產品開發的範圍為限」。

9. **「第 14 條第 7 項第 3 款」降成「第 14 條第 7 項」**（第 3 節第 2 段）。
   全文恢復後核對：那四項確實在第 14 條第 7 項的**第三款（third subparagraph）**裡，條文自己也寫
   「In relation to the third subparagraph, point (d)」——所以撰稿者沒有寫錯。
   但四項本身編號是 `(a)`–`(d)`，中文寫「第 7 項第 3 款」很容易被讀成 `(c)`，
   而常見問答第 18 題只寫 `Art. 14(7)`，因此仍採較不歧義的寫法。
   同段替經銷商補回「供貨其最多產品的」——條文是
   「the distributor **making available on the market the highest number of products**」，
   授權代表與進口商都寫了「最多產品」，只有經銷商漏掉。

10. **FAQ 第 1 題的「第 14 條第 7 項只處理『製造商沒有在歐盟設主要營業地』的情形」是錯的**。
    第 14 條第 7 項處理的是通報送到哪一國的窗口，有沒有歐盟主要營業地都在裡面
    （常見問答第 18 題兩種情形並列）。已改寫。

11. **第 1 節標題把「生效」與「適用」混用**：原標題「今天只有一個生效」與同節第 3 段
    「『生效』跟『條文要求你做什麼』是兩件事」自相矛盾（規則 2024 年就生效了）。
    已改成「第 71 條的三個日期，9 月 11 日只輪到第 14 條」。

12. **兩處「今天」改成日期**（第 1 節標題與第 2 段）。文章查核日是 9 月 17 日、刊出更晚，
    「今天（2026 年 9 月 11 日）」讀起來像是 9 月 11 日寫的。

13. **72 小時計時器的瑕疵補上 ENISA 的對沖詞**（第 5 節第 2 段）。原文是
    「As a result, **in some cases**, a notification may be displayed as overdue」，
    文章寫成一定會顯示逾期。已改成「因此有些通報會在知悉未滿 72 小時就顯示逾期」。

14. **「通報只能透過介面手動送出」改成「通報須透過平台介面送出」**（第 5 節第 1 段）。
    常見問答第 15 題沒有「手動」兩個字，同一題反而明說
    「Organisations may automate their internal reporting workflows」。

15. **三個無範圍的否定句限縮**：summary 第 4 句「官方沒有公布」、第 4 節第 2 段兩處「官方頁面沒有／沒講」、
    FAQ 第 3 題「官方目前沒有承諾」，全部改成「本文查到的官方頁面…」。

16. **研究紀錄**：`sourcing_notes` 更正「ENISA 常見問答內容沒有變動」的結論並補上中斷配方；
    第 30 題的 `verbatim_quote` 從殘句 `"might be marked as"` 換成頁面上的完整句子
    `Your submission might be marked as ‘invalid’ in the SRP.`；
    另補 `live_data_warnings` 兩條與 `factcheck` 欄位。

## 撰稿者三個自報疑點的裁決

1. **第 64 條那一段**——「不在提前清單裡」對，「依文義要到 2027 才適用」不對，「官方沒說明」要限縮。見上面第 3 點。
2. **第 16 條的雙重表述**——不該用。已改成「清單裡沒有」＋「官方說平台依它建立並在運作」。見第 2 點。
3. **用 ENISA 常見問答第 12 題取代直接引第 69 條第 3 項**——**這個改寫是對的，而且比撰稿者想的更站得住腳**。
   執委會實施指引第 210 段用完全同一個意思寫出「Article 69(3) and 71(2), second sentence」，
   兩份官方文件互相印證，文章也沒有自己主張第 69 條第 3 項「已生效」。

另外三個取捨：
- **CELLAR 要 `Accept-Language: eng`**：屬實，配方重現無誤（恢復後 200、710,696 bytes，
  與撰稿者記錄的位元組數完全相同），已寫進研究紀錄。
- **不照 `source_list_fix` 換掉 CELLAR**：理由（罰鍰金額只在法規原文）**成立**——
  我重抓 `cra-summary` 確認該頁只寫第七章訂罰則，**不印 1500 萬歐元與 2.5%**。
  但今天的中斷讓這條來源的可用性變成站主的決定，見下。
- **`must_fix 1` 只寫生效公式、不寫 2024-12-10**：**認可**。BRIEF 第 9 條就寫「生效日一律寫公式，不寫日期」，
  而 BRIEF 優先於修正清單。附帶收穫：文章寫的公告日 **2024-11-20** 今天在出版局紀錄頁的
  `Published: 2024-11-20` 欄位獨立核對無誤（研究紀錄原本那條事實的引文是「Done at Strasbourg, 23 October 2024」，撐不住公告日）。
- **`must_fix 4` 因來源名額沒寫授權法案細節**：**認可**。文章只寫「2025 年 12 月 11 日通過授權法案」，
  這句逐字在 `sources[0]`（`on 11 December 2025, the Commission adopted a delegated act`）與常見問答第 21 題。

## 查過而且正確的部分（沒有動）

- **四個時限與起算點**：24 小時、72 小時、漏洞「修補措施備妥後 14 天」、事故「72 小時通報後 1 個月」，
  在執委會頁與常見問答第 7 題兩處逐字相符；14 天只掛漏洞、1 個月只掛事故，表格四列與正文一致。
- **三個適用日**：2027-12-11／2026-09-11／2026-06-11 在四處一致（執委會頁、ENISA 新聞稿、常見問答第 4 與第 29 題）。
  第四章＝第 35 至 51 條、第 64 條屬第七章，另在 `cra-summary` 的章節表獨立確認。
- **窗口判斷**：主要營業地（決策地→員工最多）與四種備位身分的順序，逐項與常見問答第 18 題相同；
  「選錯窗口**可能**被判定無效」的「可能」有留。
- **上線狀態四條逐字無誤**：只有英文（第 24 題）、沒有 API（第 15 題）、自願通報未開放（第 4／27 題）、
  計時器瑕疵（第 26 題）；「初始運作量能」出自 ENISA 新聞稿本人。
- **條號逐條回全文核對無誤**：第 2 條第 1 項的範圍、第 3 條第 42 項的定義（另在執委會實施常見問答
  獨立確認為 `Article 3(42)`）、第 14 條第 2 項與第 4 項的 (a)(b)(c)（表格四列的依據欄完全正確）、
  第 14 條第 6 項的中間報告、第 14 條第 8 項的使用者通知、第 16 條第 1 項與第 2 項、
  第 17 條第 5 項（前提是「After a security update or another form of corrective or mitigating
  measure is available」，文章寫的「須修補或緩解措施備妥、且製造商同意」對）、
  第 24 條第 3 項、第 69 條第 2 項與第 3 項、第 71 條第 1 項與第 2 項。
- **界線**：全文沒有購買或升級建議、沒有推薦式比價、沒有攻擊手法或惡意程式名稱、沒有入侵指標；
  廠商與機關的說法都有歸因（ENISA 說明／表示、執委會說明）；**只有一個 callout，沒有投資免責段落**；
  沒有任何通報件數、註冊家數或會員國 CSIRT 數量；沒有簡體字。
- **日期沒有混用**：簽署日 2024-10-23、公告日 2024-11-20、適用日 2026-09-11／2026-06-11／2027-12-11
  在文章裡分開寫；`news_date`、slug 尾碼與事件日一致。
- **`checked_on` 2026-09-17** 在四條 source、研究紀錄、第二段、表格 caption、圖解 caption 共六處一致，未改。
- **字數**：段落合計 **2,971／3,000**（改前 2,877），沒有為了湊字數刪掉任何但書。

## 留給站主的 4 件事

1. **`sources[3]` 的可用性，不是它的內容。** 條文敘述已在出版局恢復後全部複驗無誤，
   但這條端點今天曾有數十分鐘整段 500／502，而且平時對瀏覽器供應的是約 2 MB 的 RDF 檔、不是法規——
   讀者點進去看不到法條。出刊當天要重測；若不可讀或仍是 RDF，可換成執委會 `cra-reporting` 頁
   自己掛的那個連結 `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R2847`。
   **我沒有代為替換**——EUR-Lex 今天自己也在維護，對 `curl` 又是 202／0 bytes，
   換成一個我讀不到正文的網址會違反「`sources[]` 只放你自己讀到正文的網址」。
2. **換成 `cra-summary` 不是純粹換連結。** 該頁不印 1500 萬歐元與 2.5%，也沒有第 3 條第 42 項定義
   與第 14 條的分項編號。真要換，第 4 節罰則段與 FAQ 第 6 題得整段重寫。
3. **第 64 條第 10 項仍刻意沒寫**（微型與小型企業不因逾 24 小時早期警訊受罰、開源軟體維護者不受罰）。
   `cra-summary` 也寫了同一件事，對讀者其實有用；但段落只剩 **29 字**的空間（2,971／3,000），
   要補就得從別處等量刪字，這是編輯取捨，查核代理不代決定。
4. **ENISA 常見問答是上線第一週的活文件。** 查核當天第 9 題就被改寫，並直接推翻文章一句話。
   出刊當天與每次改版都要逐題重讀，**不能沿用任何一輪（包含這一輪）的比對結論**。

## 自檢

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
 - zh-TW link text must be the title of tech-news-apple-eu-business-terms-20260818
```

只剩規格允許的兩條：索引內容包還不存在，第二條相關文章的內容包在查核期間被別的代理建立了，
`text` 要由協調者換成它的正式 title。兩個結尾連結依規格沒有動。

## 結論

`needs_owner`：96 條主張逐條核對後，1 條被今天的來源推翻、16 處已改，文章本身可刊；
所有條文敘述都回《歐盟公報》全文複驗無誤，沒有任何一條事實失去依據。
擋住的是 `sources[3]` 這條端點的可用性——查核當天曾整段時間 500／502，平時對瀏覽器也只供應 RDF——
換不換連結是站主的決定，而且換了會牽動罰則段。

---

## 第二輪

第一輪改了 16 處，超過十處，因此做第二輪。查核日仍是 **2026-09-17**（`checked_on` 六處一致，沒有因為重查而更動）。

第二輪不是整篇重做，範圍是協調者指定的五件事：覆核第一輪**改動過的每一個段落與新寫進去的每一句**、
回掃有沒有為了字數刪掉但書、`summary` 與 FAQ 答句是否都在正文找得到同樣條件的說法、
每一個日期與時限連著「起算點／對誰／哪一類事件」回條文原文、以及執行 `sources[3]` 換網址。

重新核對 **61 條**主張（第一輪改動段落裡的每一句 25 條、`summary` 4 句、FAQ 6 題答句、
四個時限 × 起算點／對象／事件類型 12 條、三個適用日與生效公式 4 條、罰鍰否定句的範圍、
ELI 同一份文件，以及界線與 `checked_on`／字數／簡體字等 8 項複查），
另以程式化搜尋把研究紀錄 **36 條 `verbatim_quote`** 逐條比對原文。
改了 **14 處**：換網址 1 處（同時動內容包與研究紀錄）、其他內容包 8 處、只動研究紀錄的 5 處。
**第二輪沒有推翻任何事實**——14 處全部是限定詞、歸因與範圍的收緊，加上換網址。

### 四條來源今天的狀態（第二輪重抓）

| source | HTTP | bytes | body 是不是正文 |
| --- | --- | --- | --- |
| 執委會 cra-reporting | 200 | 52,986 | 是。與第一輪同 bytes，`Last update 11 September 2026` |
| ENISA 啟用新聞稿 | 200 | 49,879 | 是。與第一輪同 bytes |
| ENISA 常見問答 | 200 | 79,220 | 是。31 題逐題重讀，內容與第一輪相同；第 9 題仍掛 `[UPDATED]` |
| 《歐盟公報》全文（CELLAR，`Accept-Language: eng`） | 200 | 710,696 | 是。與第一輪、與撰稿者記錄同 bytes |
| **`sources[3]` 的新網址**（EUR-Lex ELI） | **202** | **0** | **否，讀不到正文**（見下） |

### `sources[3]` 換網址：已執行

協調者已用真實瀏覽器（語言偏好 zh-TW）確認舊網址 `https://publications.europa.eu/resource/celex/32024R2847`
回的是純文字錯誤 `None of the requests returned successfully a redirection … Not found work … language(s) [zho]`，
也就是本站繁中／簡中／日／韓四個語系的讀者點下去全部是錯誤頁。已依指示換成
**`https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng`**，內容包與研究紀錄同步，
`title` 改成「EUR-Lex：《歐盟公報》刊登的 Regulation (EU) 2024/2847（網路韌性法）全文」，
研究紀錄的 `publisher` 改成 `EUR-Lex, Publications Office of the European Union`，
`verified_facts` 裡 **21 條**指向舊端點的 `url` 一併改掉（改完 36 條引文全部仍在來源找得到、全部指得到 `sources[]`）。

**(a) 兩個網址是同一份文件的一手依據——公報自己印的 ELI 字串。**
在 CELLAR 讀到的 710,696 bytes 全文裡，公報自己印出這個永久識別碼三次，逐字如下：

- 附件六（EU declaration of conformity）的註腳：
  `OJ L, 2024/2847, 20.11.2024, ELI: http://data.europa.eu/eli/reg/2024/2847/oj .`
- 全文最末的版權行：
  `ELI: http://data.europa.eu/eli/reg/2024/2847/oj`
- 卷首另印出處：`Official Journal of the European Union` / `EN` / `L series` / `2024/2847` / `20.11.2024`

`http://data.europa.eu/eli/reg/2024/2847/oj` 就是 EUR-Lex 那個 ELI 網址指向的同一份文件。
這一行已逐字記進研究紀錄的 `sourcing_notes`，並取代公告日那條事實原本的引文（見下面第 10 點）。

**(b) 條文內容的複驗。** 條文是 **2026-09-17 經 CELLAR（`Accept-Language: eng`，CELEX 32024R2847）讀到全文複驗**的：
第二輪重抓仍為 200、710,696 bytes，第 2(1)、3(42)、13(8)–(9)、14(1)–(8)、15、16(1)–(3)、17(5)、
24(3)、64(1)–(2) 與 (10)、69(2)–(3)、71(1)–(2) 條全部逐字重新命中。
**EUR-Lex 當天部分停擺**（站上掛著 `EUR-Lex is temporarily not fully available.`、ELI 網址被導到 TodayOJ），
所以當天讀不到 EUR-Lex 供應的正文是預期中的事；**出刊當天要重開確認**。

**(c) 收工前再抓一次（照實記）。** `2026-09-17 16:18Z`，`curl -A "Mokaair-editorial"`：

```
plain    http=202 size=0 redirects=0 final=https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng
+AccLang http=202 size=0 redirects=0 final=https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng
```

**HTTP 202、0 bytes、沒有轉址、沒有讀到正文。** 這是本容器對整個 `eur-lex.europa.eu` 的一貫結果
（第一輪也記了同樣的 202／0 bytes），加上 EUR-Lex 當天自己在維護。抓不到不算失敗，但也表示
**沒有人在今天親眼確認過讀者點下去會看到什麼**——這是留給站主的第一件事。
所有請求的 UA、標頭與查詢字串都沒有放入任何 email、姓名或個人資料。

### 改掉的其餘 13 處（換網址是第 1 處，已在上一節說明）

1. **第五節第一段：ENISA 的「未來階段」被寫成同一種承諾。** 原文「ENISA 說會在「未來階段」陸續補上」
   把三件不同語氣的事併成一句。常見問答的原文是三種：
   自願通報是承諾（第 4 題 `Voluntary reporting under Art. 15 will be introduced in a future phase of the platform.`、
   第 27 題 `The platform will be enhanced at a later stage to support voluntary reporting under Art.15.`）；
   應用程式介面只是「可能考慮」（第 15 題 `API functionality may be considered in a future phase of the SRP.`）；
   其他語言只是「會評估」（第 24 題 `This availability of additional language versions of the platform itself
   will be reviewed in the next phase of the project.`）。
   已改成「ENISA 說自願通報會在「未來階段」開放，應用程式介面與其他語言版本則只說會在下一階段評估，都沒有給時間表」。
   **這是第二輪最重的一處：把機關對未來的三種不同承諾強度還原。**

2. **第四節第二段與 FAQ 第 3 題：第 14 條第 8 項掉了通知的主要標的與「必要時」。**
   條文是「the manufacturer shall inform the impacted users …, and where appropriate all users,
   **of that vulnerability or incident** and, **where necessary**, of any risk mitigation and corrective
   measures that the users can deploy」——要通知的主要標的是**漏洞或事故本身**，緩解與更正措施是「必要時」才加的。
   兩處原本都只寫「通知風險緩解與更正措施」，把主標的與 `where necessary` 一起寫掉了。
   已改成「把漏洞或事故告知受影響使用者，必要時一併說明風險緩解與更正措施」。

3. **FAQ 第 3 題：「條文沒有訂通知要多快送出」超出條文範圍。**
   第 14 條第 8 項後段其實寫了「Where the manufacturer fails to inform the users of the product with
   digital elements **in a timely manner**, the notified CSIRTs designated as coordinators may provide
   such information to the users」——條文並非完全不談時間，只是沒有訂出期限。
   已限縮成「條文只寫製造商未「及時」告知時，CSIRT 可以代為通知使用者，沒有訂出通知要多快送出，也沒規定語言或管道」。

4. **FAQ 第 1 題（第一輪新寫的句子）把判準掛錯條。** 第一輪寫的是
   「第 14 條第 7 項處理的是通報要送到哪一國的窗口（…），**判斷的仍然是產品有沒有在歐盟市場上架**，而不是使用者人在哪裡」。
   第 14 條第 7 項判的是**通報送到哪一國的窗口**（主要營業地→四種備位身分），
   產品在不在歐盟市場是**第 2 條第 1 項**的範圍問題，兩件事被縫成一句。
   已改成「第 14 條第 7 項處理的**只是**通報要送到哪一國的窗口（…），跟使用者人在哪裡無關；
   決定規則管不管得到的，仍然是上面第 2 條的市場範圍」。

5. **第三節第二段：進口商的判準抄成「進口最多」。** 條文第 14 條第 7 項第三款 (b) 是
   「the Member State in which the importer **placing on the market** the highest number of products
   with digital elements of that manufacturer is established」——判準是**投放市場**的數量，不是進口量；
   ENISA 常見問答第 18 題也寫 `the importer places the highest number of your products … on the market`。
   授權代表（代理其最多產品）與經銷商（供貨其最多產品，第一輪補的）都對，只有進口商這一項還是舊寫法。
   已改成「在市場上投放其最多產品的進口商所在國」。

6. **第三節第一段：特別例外情形被掛在第 14 條第 7 項底下。** 原文
   「第 14 條第 7 項規定，製造商要用…送出，並同步讓 ENISA 看到**——除非有特別例外情形**」。
   但第 14 條第 7 項的原文只有「shall be **simultaneously accessible to ENISA**」，**沒有任何例外**；
   例外在第 16 條第 2 項（特別例外情形下 ENISA 先只拿到部分資訊）。
   執委會頁面確實把兩件事寫成一句（`…and, unless particularly exceptional circumstances apply,
   the information is made available simultaneously to ENISA.`），但文章點名了條號，讀者去查第 14 條第 7 項會找不到。
   已改成「並同步讓 ENISA 看到；**執委會說明**，特別例外情形下不在此限」，並在研究紀錄新增這條執委會引文。

7. **第四節第三段補上「並通知執委會」，讓 FAQ 第 6 題 ⊆ 正文。**
   FAQ 第 6 題寫「實際罰則規則由各會員國自訂**並通知歐盟執委會**」，正文只有「由會員國自訂」——
   FAQ 帶了一個正文沒有的事實。該事實本身正確（第 64 條第 1 項
   `Member States shall, without delay, notify the Commission of those rules and measures`），
   所以選擇補進正文而不是從 FAQ 刪掉。

8. **第二節第三段刪掉三度重複的時限清單（這是為了騰字數，刪的是重複、不是但書）。**
   原文「歐盟執委會把時限濃縮成一句話：24 小時內送早期警訊、72 小時內送完整通報，漏洞在修補措施備妥後
   14 天內送最終報告，事故則是 72 小時通報後 1 個月內送最終報告」——這四個時限在同節第二段講過一次、
   表格四列再列一次，這裡是第三次。已改成「歐盟執委會的通報頁面把上面這四個時限濃縮成同樣一句話」，
   執委會作為第二個獨立來源的意義保留，重複的清單去掉。
   **騰出來的字全部用在上面第 1、2、5、6、7 點補回來的限定詞上**；段落合計仍是 **2,971／3,000**，與第一輪相同。

9. **研究紀錄：第 71 條第 1 項的引文多了一個句號，是 36 條裡唯一搜尋不到的一條。**
   公報把《歐盟公報》刊名排成斜體，句號前有一個空格，頁面上實際是
   `… in the Official Journal of the European Union .`，
   所以紀錄裡的 `… European Union.` 不是頁面上的連續字串。已改成到 `Union` 為止。
   （第一輪的紀錄寫「verbatim_quote 全部是今天重新抓取後、用程式化搜尋在正規化文字裡找到的連續字串」——
   這一條是例外，本輪補做了全部 36 條的程式化比對。）

10. **研究紀錄：公告日那條事實的引文撐不住它自己。** `fact` 寫「2024 年 10 月 23 日簽署，
    同年 **11 月 20 日刊登於《歐盟公報》**」，引文卻只有 `Done at Strasbourg, 23 October 2024.`——
    只撐得住簽署日。第一輪發現了這個問題但沒有改引文，改用出版局紀錄頁的 `Published` 欄位佐證。
    第二輪直接用公報自己印的出處行取代：`OJ L, 2024/2847, 20.11.2024, ELI: http://data.europa.eu/eli/reg/2024/2847/oj`——
    **一行同時撐起 L 系列編號、公告日與 ELI**，而且出自 `sources[3]` 本身。

11. **研究紀錄：三條引文延長到撐得住各自的 `fact`。**
    第 14 條第 7 項四種備位身分的引文原本只有 (a) 款，延長到 (b) 款（進口商那一款，見上面第 5 點）；
    第 64 條第 1 項的引文延長到印出通知執委會義務的地方（見第 7 點）；
    第 14 條第 8 項的引文延長到 `and, where necessary, …` 那一段（見第 2 點）。三條都重新確認是連續字串。

12. **研究紀錄：常見問答第 24 題那條事實補記語氣。** 原本只記「上線時只支援英文介面」，
    補上同題第二句（其他語言「will be reviewed in the next phase」）與第 15 題的 API「may be considered」，
    作為上面第 1 點改寫的依據。

13. **研究紀錄：`sourcing_notes`、`live_data_warnings`、`corrections_applied`、`unverified_or_excluded`
    四處關於 `sources[3]` 的敘述全部改寫**，第一輪的出版局中斷紀錄標明「保留備查」而不是刪掉；
    `corrections_applied` 裡「source swap 未套用」那一條改成「第二輪以另一種方式套用」並說明為什麼不是換成 `cra-summary`。
    另加 `factcheck.second_round`（日期、範圍、61 條、14 處、方法、結論、留給站主四件事）。

### 回掃：第一輪有沒有為了字數刪掉但書

**沒有。** 逐段比對第一輪改動前後的敘述，第一輪是**補**但書（第 13 條的 5 年與 10 年、
第 14 條第 2 項的「不得無故延遲」、開源軟體維護者的範圍限制、`in some cases`、「可能」被判定無效），
沒有任何一處是把限定詞換成字數。段落從 2,877 增到 2,971 也符合這個方向。
第二輪自己要補字時，字是從上面第 8 點那句三度重複的時限清單騰出來的，**沒有動任何但書**，
段落總數維持 2,971／3,000。

### `summary` ⊆ 正文、FAQ ⊆ 正文

- **`summary` 四句全部通過。** 第 1 句（9 月 11 日、第 14 條、平台、24／72 小時）在第一節與第二節；
  第 2 句（開源軟體維護者、2027-12-11）在第一節第二段；第 3 句（初始運作量能、英文介面、無 API、
  自願通報未開放）在第五節第一段；第 4 句（沒有公布件數、不提供升級建議）在第五節第三段與第二段／callout。
  **沒有任何數字只出現在 summary。**
- **FAQ 六題**：第 2、4、5 題與正文條件完全一致；第 1、3、6 題的落差已在本輪改掉（上面第 4、3、7 點）。

### 日期與時限：連著起算點、對誰、哪一類事件重核

全部回公報原文，全部正確，**沒有改動**：

- **24 小時**（早期警訊）：第 14 條第 2 項 (a) 與第 4 項 (a)，都是
  `without undue delay and in any event within 24 hours of the manufacturer becoming aware of it`——
  起算點是**製造商知悉**，對象是**製造商**，漏洞與事故**兩類都適用**。
- **72 小時**（完整通報）：第 2 項 (b) 與第 4 項 (b)，同樣是 `of the manufacturer becoming aware`，兩類都適用。
- **14 天**（最終報告）：**只掛漏洞**。第 2 項 (c)`a final report, no later than 14 days after a corrective
  or mitigating measure is available`——起算點是**措施備妥**，不是知悉。
- **1 個月**（最終報告）：**只掛事故**。第 4 項 (c)`a final report, within one month after the submission
  of the incident notification under point (b)`——起算點是**72 小時通報送出**，不是知悉，也不套用 14 天。
- **三個適用日**：第 71 條第 2 項 `This Regulation shall apply from 11 December 2027.` ＋
  `However, Article 14 shall apply from 11 September 2026 and Chapter IV (Articles 35 to 51) shall
  apply from 11 June 2026.`
- **生效日**：第 71 條第 1 項只印公式 `on the twentieth day following that of its publication`，
  文章也只寫公式、不寫換算後的日期，符合 BRIEF 第 9 條。
- 表格四列的期限、起算點與依據欄（第 14 條第 2 項 (a)(b)(c)、第 4 項 (a)(b)(c)）逐格重核無誤。

### 其他複查過、沒有改的部分

- **第一輪最重的那處改寫今天仍然成立**：ENISA 常見問答第 9 題仍掛 `[UPDATED]`，仍寫
  `Primary and Secondary ARs associated with the same manufacturer can access, view, and update
  notifications associated with that manufacturer, regardless of with AR originally submitted them.`
  （`with` 是來源自己的錯字）與 `The only exception concerns draft notifications. Drafts are stored
  locally in the individual AR's account…`，文章第五節第三段與之相符。31 題逐題重讀，全頁沒有再變。
- **第一輪換掉「第 16 條／第 64 條依文義要到 2027」之後寫上的句子**逐句回一手來源：
  第 71 條第 2 項的提前清單確實只有第 14 條與第四章；執委會寫
  `Pursuant to Article 16 of the CRA … ENISA has established the CRA SRP, operational as of 11 September 2026.`；
  ENISA 分兩題寫同一件事（第 2 題的法律依據 `Art. 16(1)`、第 4 題
  `The platform has become operational on 11 September 2026`）。「執委會與 ENISA 都寫明」兩邊都站得住。
- **限定範圍的否定句今天重新實測**：`cra-reporting`、ENISA 新聞稿、ENISA 常見問答三頁以
  `penalt`／`fine`／`sanction`／`15 000 000`／`15 million`／`2,5`／`2.5 %` 逐一搜尋，**全部 0 次**。
  「本文查到的三個官方頁面都沒有提到罰鍰」範圍剛好——查了三頁，就寫三頁，沒有寫成「官方沒有」。
- **執委會指引 C(2026) 5252 第 210 段沒有進 `sources[]`，文章正文也沒有點名它。**
  逐字確認正文、`summary`、FAQ、callout、表格與圖解都沒有出現「C(2026) 5252」「第 210 段」
  「Section 9.1」「Section 5」等字樣，它只留在研究紀錄與查核報告裡，符合規格。
- **第 64 條屬第七章**這次直接在公報全文的章節標題上確認（`CHAPTER VII` / `CONFIDENTIALITY AND PENALTIES`，
  自第 63 條起，第 65 條之後才是 `CHAPTER VIII`），不必再靠 `cra-summary` 那個印錯成 `63-63` 的章節表。
- **第 13 條兩個但書**回全文重驗，第一輪補的字沒有寫過頭：第 8 項第三款
  `Without prejudice to the second subparagraph, the support period shall be at least five years.
  Where the product with digital elements is expected to be in use for less than five years, the
  support period shall correspond to the expected use time.`；第 9 項
  `remains available after it has been issued for a minimum of 10 years or for the remainder of the
  support period, whichever is longer`。
- **一個來源自己的用字出入，文章選對了邊**：ENISA 常見問答第 5 題把開源軟體維護者的範圍寫成
  `involved in the **deployment** of products`，但第 24 條第 3 項原文與 ENISA 自己的新聞稿都是
  `involved in the **development** of the products`。文章寫「涉入產品**開發**」，跟著法規與新聞稿走，正確。
- **界線**：沒有購買或升級建議、沒有推薦式比價、沒有攻擊手法或惡意程式名稱；
  ENISA 與執委會的說法都有歸因；只有一個 callout、沒有投資免責段落；
  沒有任何通報件數或註冊家數；沒有簡體字；`checked_on` 2026-09-17 六處仍一致。

### 留給站主的 4 件事（取代第一輪那 4 件）

1. **出刊當天必須重開 `sources[3]` 的新網址 `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng`，
   確認讀者看得到法規正文。** 今天 EUR-Lex 自己掛著維護訊息、ELI 網址被導到 TodayOJ，
   對 `curl` 是 202／0 bytes，**沒有人在今天親眼確認過讀者會看到什麼**。
   條文內容不受影響（同日經 CELLAR 讀到全文逐條複驗無誤）。
   若出刊當天 EUR-Lex 仍不可用，備案是執委會 `cra-reporting` 頁自己掛的
   `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R2847`——但那也是 EUR-Lex，同一個站倒了會一起倒。
2. **ENISA 常見問答仍然是活文件。** 第二輪重讀 31 題，內容與第一輪相同、沒有再變，
   但第 9 題仍掛著 `[UPDATED]`，代表這一頁還在改。出刊當天要再逐題重讀，
   **不能沿用第一輪或第二輪的比對結論**。
3. **第 64 條第 10 項仍刻意沒寫。** 第二輪已在全文確認原文是 `By way of derogation from paragraphs 3 to 9`，
   而第 13、14 條的罰鍰上限訂在**第 2 項**、不在第 3 到 9 項之內——這個對不上是條文本身的用字瑕疵，
   寫進文章需要做法律判斷，查核代理不代決定。段落只剩 **29 字**，要補得從別處等量刪字。
4. **常見問答第 13 題有一件對讀者有用、文章沒寫的事**：製造商在 2026-09-11 之前就已知悉的積極利用漏洞
   **不必回溯通報**，該日之後才知悉的才要（依執委會 FAQ 5.1 與 5.3）。
   文章沒有寫錯（第四節只講「遇到」新的漏洞或事故），補不補是編輯取捨。

### 自檢（第二輪改完）

```
FAIL
 - zh-TW link target tech-news-2026-index.json does not exist yet
 - zh-TW link text must be the title of tech-news-apple-eu-business-terms-20260818
```

只剩規格允許的兩條，兩個結尾連結依規格沒有動。

### 第二輪結論

`needs_owner`：61 條複核、36 條引文逐條比對之後，**沒有任何一條事實被推翻**，
14 處改動全部是限定詞、歸因與範圍的收緊，加上協調者決定的換網址。文章本身可刊。
`sources[3]` 已換成 EUR-Lex 的 ELI 網址，而且有公報自己印的 ELI 字串證明是同一份文件、
條文也在同日經 CELLAR 全文複驗無誤；**唯一沒能在今天確認的，是讀者點下去會看到什麼**——
EUR-Lex 當天部分停擺，對 `curl` 是 202／0 bytes，出刊當天必須重測。
