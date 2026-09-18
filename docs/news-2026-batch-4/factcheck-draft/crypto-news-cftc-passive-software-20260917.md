# 獨立查核：crypto-news-cftc-passive-software-20260917

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 本來就是 2026-09-18，且五處一致，沒有更動）。

查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；兩份 PDF 用**系統 `python`**
的 pypdf 6.16.2 同時以預設與 `extraction_mode="layout"` 兩種模式抽字，layout 模式保留欄位縮排，
用來逐項比對編號 1–10 的條件與五段 Covered Activities 項目符號。新聞稿 HTML 去標籤後逐句比對。
第 5 節那句 2026-03-23 聯名解釋令不在本篇 `sources[]` 內，改以既有文章
`crypto-news-sec-crypto-interpretation-20260323` 的來源鏈路交叉核對，並另讀 Federal Register API 的
`2026-05635.json` 反駁查證（**沒有寫進 `sources[]`**）。沒有用 `sources[]` 以外的網址替文章補任何事實。

檢查的主張：約 **95** 條（正文 12 段每一句、摘要 4 句、FAQ 7 題的問與答、兩個 callout、表格 5 列與 caption、
圖解 caption 與四格、`hero_label`、title、description）。改了 **20 處**，另有 5 件留給站主。
`hero.alt` 依規格不查也不改。

## 重抓結果（三條 sources 都還在、位元組數與研究紀錄逐一相同）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| cftc.gov/PressRoom/PressReleases/9300-26 | 200 | 34,508 | 是（text/html，最終網址未轉址） | `Release Number 9300-26`；日期欄 `September 17, 2026`；兩段內文與研究紀錄三條引文逐字相符（含 `Commission’s` 的 U+2019） |
| cftc.gov/csl/26-25/download | 200 | 232,223 | 是（application/pdf，7 頁 19,527 字元） | 報頭、Re: 行、Background、Division No-Action Position、條件 1–10、Covered Activities 五段、結尾效力三句、註腳 6／12／14／24、副本收受者 |
| cftc.gov/csl/26-09/download | 200 | 312,032 | 是（application/pdf，7 頁 19,293 字元） | 報頭 `March 17, 2026`；`your letter on behalf of Phantom Technologies, Inc. (“Phantom”), dated March 13, 2026`；TSV Letter Requirements (1)–(6)；同樣的「不拘束委員會」段 |

字元數的算法：7 頁 `extract_text()` 直接相接（不加分隔字元），與研究紀錄的 19,527／19,293 完全吻合，
代表抽取路徑可重現。三個位元組數與前期研究紀錄相同，是穩定文件、不是活頁面。

## 改掉的 20 處

**兩處是實質錯誤**

1. **「十項條件之外，提供者還要另外遞交一份同意遵守這些條件、接受委員會管轄的通知」**（第 4 節第 2 段）。
   那就是**條件 10** 本身：`10. The PSP files a notice with the Division agreeing to satisfy these
   conditions and consenting to the Commission’s jurisdiction to investigate and take enforcement action…`。
   寫成「十項之外」會讓讀者以為手續有十一道。已改成「第十項條件則是向部門遞交一份通知……」。
2. **「這個立場建立在申請人向部門陳述的事實與情況上」**（第 5 節第 1 段）。原文是
   `are based upon the facts and circumstances presented to the Division staff`，沒有主詞；
   而且 Letter 26-25 是普遍性的函，**根本沒有申請人**（有申請人的是 26-09）。已改成「向部門職員陳述」。

**限定詞被刪或範圍被改（BRIEF 型態 1、3）**

3. **「相同條件」→「實質相同條件」**（第 1 節第 2 段）。原文 `on substantially the same terms`，
   `substantially` 是 BRIEF 第 3 節明列不得刪的限定詞之一。同段另刪掉「會有這次擴大，是因為 3 月那封信只保護一家公司」
   這句自撰因果，改為照原文分述「MPD 收到其他處境類似提供者與其律師詢問」與「部門認為給予所有 PSP 是有理由的」兩件事。
4. **「那些解釋函建立在六項前提上」**（第 2 節第 2 段與 FAQ 第 7 題）。兩封信的原文都是
   `relied on representations from the TSV that required, **among other things**: (1)…(6)
   (requirements (1) through (6) collectively, the “TSV Letter Requirements”)`——
   六項是**被合稱的那六項**，不是全部的前提。已改成「建立在該供應商所作的一組陳述上，信中把其中六項合稱『TSV 函前提』」。
5. **「每位使用者」→「每位客戶」**（同兩處）。TSV Letter Requirements 第 (1) 項原文是 `each customer`，
   而 `User` 在這兩封信裡是**另有定義**的用語（DCM 參與者或 FCM／IB 客戶）。混用會換掉主體。
6. **「有一部分不符合這些前提——登記業者與使用者不需要有既有關係——」**（同兩處）。原文是
   `(e.g., the Registrant and User did not need to have a pre-existing relationship)`，
   `e.g.` 是舉例，不是唯一原因。已改成「有一部分落在這些前提之外（信中舉的例子是……）」。
7. **風險揭露條件漏掉三件事**（第 4 節第 1 段）。條件 3 原文有規則編號 `Commission Regulation 1.55(b)`、
   範圍限定 `to the extent relevant to the trading activity facilitated by the PSP`，以及整條的例外：
   `This condition shall not be applicable if a Registrant is registered with the Commission and obligated
   to provide a risk disclosure statement to the User consistent with Commission Regulation 1.55.`
   草稿三者都沒有，等於把一條有例外的義務寫成無條件義務。已全部補回。
8. **「提供者的對外溝通與行銷要比照已登記介紹經紀商的規則辦理」**（第 4 節第 2 段）。條件 5 的義務客體是政策與程序：
   `adopts and enforces policies and procedures reasonably designed to ensure compliance with applicable
   Commission and National Futures Association (“NFA”) rules…`。已改寫並補上條件 1（法定失格事由）、
   條件 7 的「承諾書送交部門」、條件 8 的規則編號 1.31 與「受管制業務」範圍。
9. **「軟體介面必須清楚區分」→「清楚而顯著地區分」**（第 3 節第 1 段、FAQ 第 2 題）。原文 `clearly and conspicuously`。
   同處補回 `either as a standalone product or`（獨立產品或內嵌功能），原本只寫了內嵌那一半。
10. **分潤與收費的 `may` 被寫成直述**（第 3 節第 1 段）。原文兩處都是 `may also agree to share a specified
    portion of their relevant revenues` 與 `this agreement may provide for the PSP to charge a
    transaction-based fee`。已改成「業者可以同意分給提供者一定比例的相關收入」「也可以透過使用條款直接收取」。
    同段「特定商品」補成「特定衍生性商品契約」（`particular derivatives contracts`）。
11. **摘要第 3 句的「買賣訊號」補回「明示的」**（`express “buy” or “sell” signals`）。正文本來就有，摘要掉了。

**結構限制寫反、連接詞寫窄**

12. **「以該會員的期貨佣金商、介紹經紀商客戶身分間接交易」主從寫反了**（第 3 節第 2 段）。原文是
    `as a customer of an FCM or IB **that is a member of the DCM**`——是那家 FCM／IB 為 DCM 會員，
    不是「該會員的 FCM」。已改成「以身為該市場會員的期貨佣金商、介紹經紀商之客戶身分」。
13. **同句「資金」補回 `or other property`，「或」改回 `and/or`**：原文
    `maintain the funds or other property securing its derivatives positions in custody with the DCM’s
    derivatives clearing organization (“DCO”) **and/or** an FCM that is a member of such DCO`。
    保管對象也寫清楚是**該 DCO 的**會員 FCM。

**自己算出來的數字、寫太滿的否定句（BRIEF 型態 6、9）**

14. **標題「十項條件劃出四條線」→「十項條件劃出的界線」**。「四」不在任何來源；信中那句禁止規定列的是三件事
    （持有／控制／保管資產、產生明示買賣訊號、對路由或執行行使裁量），正文也從來沒出現過「四條線」。
    研究紀錄 `title` 與圖解第四格（原為「不得下單訊號」）同步改。**「十項」保留**——條件在信中是 1 到 10 編號的。
15. **「只包含信中列出的五項」→「只包含信中條列的這些」**（第 3 節第 1 段）。
    原文 `includes only the following activities:` 之後是**無編號**的項目符號，「五」是編輯數出來的。
16. **FAQ 第 4 題刪掉「以 2026 年 9 月 18 日查核，尚未見到這樣的法規制定或指引」**。
    本篇三條 sources 撐不起這個否定句——沒有做過聯邦公報或 CFTC 全站檢索。改成「信中沒有說委員會何時會著手，
    本文也不推測」，並補上「部門保留依其裁量提早終止」。
17. **FAQ 第 6 題「兩封信全文都未見『台灣』一詞」→「未見 Taiwan 一詞」**。信是英文，用中文詞描述檢索結果會誤導。
    實際查法：兩份抽取全文不分大小寫檢索 `taiwan`，26-25 與 26-09 各 **0** 次（`china`、`asia` 同樣 0 次）。
18. **「隨時修改或終止」四處改成「依其裁量」**（摘要第 4 句、第 5 節第 1 段、本文提醒 callout、FAQ 第 1 題）。
    原文是 `the Division retains the authority to condition further, modify, suspend, terminate, or
    otherwise restrict the terms of the position taken herein, **in its discretion**`——沒有「隨時」。
    第 5 節同時補回 `as with all staff letters`（如同所有職員函）。

**用語與來源標示**

19. **「僅對單一申請人生效」「一封只對一家公司生效的信」→「只有一家公司能援用」**
    （第一段、第 1 節標題、description）。註腳 6 講的是 `only the Beneficiary of a no-action letter may
    rely on it and, thus, no PSP other than Phantom may rely on Letter 26-09`——是**援用資格**，不是生效與否。
    同步：第一段補回原文的 `solely as a result of them engaging in the Covered Activities`
    （「僅因為……從事信中定義的『適用活動』卻未登記」）；第 3 節第 1 段補回
    `The PSP’s involvement in order submission will be limited to providing software on the User’s device…
    will not have any affirmative involvement with any particular orders`——這句原本**只出現在圖解格子上，正文沒有**。
20. **表格「取得方式」欄「MPD 主動擴大」→「符合條件者遞交通知」**；
    **`sources[1]` 的 title** 改成貼近該函 Re: 行的寫法（含 `Section 4d(g)` 與 `Section 4k(1)`），
    原寫法把兩個條號都省掉了；受 schema 的 200 字元上限所限，IB／AP 沿用該函自己的縮寫。
    第 5 節第 2 段「處理加密資產在什麼情況下受投資契約規範的證券法問題」改成
    「處理聯邦證券法如何適用於特定類型的加密資產與相關交易」，貼近該解釋令的正式標題。

## 查過而且正確的部分（沒有動）

- **事件日與所有日期**：26-25 報頭 `CFTC Letter No. 26-25   No-Action   September 17, 2026`、
  新聞稿日期欄 `September 17, 2026`、編號 9300-26；slug 尾碼／`news_date`／第一段三者一致。
  26-09 的 **2026-03-17**（報頭）與申請書的 **2026-03-13**（`dated March 13, 2026`）在文章裡分開寫，沒有混用。
- **具名人**：26-25 是 DJ Hennes, Director, Market Participants Division；26-09 是 Thomas J. Smith, Acting Director。
- **新聞稿三條引文逐字相符**，包括 `The position is similar to that provided in Staff Letter 26-09 and now is
  broadly available to such providers.`
- **條號全部正確**：4d(g)、4k(1)、3.12(a)、17 CFR 140.99 與 140.99(a)(2)、1.55(b)、1.31、3.1、
  NFA Compliance Rule 2-29；註腳 14 `For the avoidance of doubt, PSPs are not limited to providers of
  crypto asset related software.` 逐字無誤。
- **禁止事項三句與原文一字不差**：`At no point would the PSP hold, control, or take into custody User assets,
  generate express “buy” or “sell” signals, or exercise discretion with respect to the routing or execution
  of User orders.`
- **效力界線寫成條件不是日期**，沒有把 `until the effective date of a Commission rulemaking or guidance…`
  換算成任何日曆日（BRIEF 型態 9 的常見陷阱，這篇沒有踩）。
- **2026-03-23 聯名解釋令那句成立**：Federal Register API `2026-05635.json` 的
  `publication_date` 與 `effective_on` 同為 `2026-03-23`、`agencies` 是 CFTC 與 SEC、`citation` 是 91 FR 13714、
  `corrections` 是空的；既有文章另以署名欄 `By the Commissions. Dated: March 17, 2026.` 佐證是委員會層級。
  「委員會層級的聯名文件、刊登當天就生效」與「26-25 是部門層級、性質與拘束力不同」的對比可以寫。
- **兩個 link**：第一個 text 與幣圈索引 zh-TW title 逐字相同；第二個 text 與
  `crypto-news-sec-crypto-interpretation-20260323` 的 zh-TW title 逐字相同。`check_article.py` 對兩者都沒有 FAIL。
- **免責 callout** 的 title 與 text 與 `crypto.md` 樣板**逐字相同**（程式比對 `True`），含「不是投資建議」六個字，
  查核日 2026-09-18；`checked_on` 在三條 source、研究紀錄、第二段、表格 caption 與兩個 callout 一致，本次沒有更動。
- **界線**：全文沒有幣價、漲跌幅、市值、交易量、資金流、殖利率或任何報酬數字；事件契約與永續契約只以
  「信中列為可送單的商品類型」出現；Phantom 只以 Letter 26-09 申請人與其自述業務出現，沒有評價它的產品；
  沒有費率比較、沒有推薦語氣、沒有「本站實測」。本篇不是草案文件，無「缺草案字樣」的問題。
- **摘要**的每個數字（2026-09-17、2026-03-17、十項）都在正文出現；FAQ 答案都是純文字沒有網址；全文沒有簡體字。

## 留給站主的事

1. **申請人是誰提的**：26-09 原文是 `your letter **on behalf of** Phantom Technologies, Inc., dated March 13,
   2026 … **as supplemented by additional correspondence with Division staff** (together, the “Request”)`——
   申請由律師代提，且 Request 還包含後續補充往來。文章目前寫「Phantom 在 2026 年 3 月 13 日提出的申請」，
   日期正確但顆粒度較粗。要不要寫細請站主決定。
2. **來源自己的兩處不一致，本代理沒有代為訂正**：26-25 註腳 2 把公司名印成 `Phantom Technologies, Inc`
   （`Inc` 後沒有句點），26-09 內文是 `Phantom Technologies, Inc.`；26-09 的 Re: 行把條號印成 `Section 4(k)`，
   內文與 26-25 都是 `Section 4k(1)`。文章一律採內文寫法，也沒有在文中說明。
3. **字數只剩 6 個字**：zh-TW 段落 2,994／3,000。翻譯與逐語審稿若要補任何一句，必須同時從別處刪掉等量的字，
   **不可以刪但書或限定詞來湊**。
4. **圖解第四格改過**：`["不得下單訊號", "不得產生買賣訊號或裁量執行"]` →
   `["不得給買賣訊號", "不得產生明示訊號或行使裁量"]`，內容包 image caption 與研究紀錄 `diagram.caption`
   的「下達買賣訊號」也改成「產生明示的買賣訊號」。畫圖時請用新版。
5. **沒有查也沒有寫**（沿用撰稿階段的排除理由，本次未改變）：TSV 系列解釋函 06-29／08-07／08-12 本文、
   NFA Compliance Rule 2-29 與 Interpretive Notice 9003（`nfa.futures.org` 不在 `crypto.md` 白名單）、
   Phantom 申請書原文（未公開）。

## 結論

`needs_second_round`。骨幹（誰發的、什麼時候、是什麼層級的文件、十項條件、三條禁止規定、不拘束委員會）
全部回得到兩封信原文，沒有一句需要推翻；但共改了 20 處，其中兩處是實質錯誤（條件 10 被寫成十項之外、
26-25 被安上一個不存在的申請人），另有多處限定詞（`substantially`、`among other things`、`e.g.`、
`clearly and conspicuously`、`may`、`and/or`、條件 3 的整條例外）遭刪。依規格「改超過十處事實」的門檻，
交第二輪覆核；覆核建議集中在**第 3 節第 1 段與第 4 節兩段**（改動最密集的三段）以及**摘要與 FAQ 的同步**。

自檢輸出：

```
OK crypto-news-cftc-passive-software-20260917 zh-TW paragraphs 2993
```

## 第二輪

第二輪查核代理：未參與撰稿，也未參與第一輪。查核日 **2026-09-18**（`checked_on` 本來就一致，沒有更動）。

查核方式：三條 `sources[]` 於 2026-09-18 再以 `curl -sL -A "Mokaair-editorial"` 重抓一次並讀 body，
位元組數與第一輪逐一相同；兩份 PDF 用**系統 `python`** 的 pypdf 6.16.2 以預設與 `layout` 兩種模式重抽，
`layout` 模式用來逐項核對編號 1–10 的條件與 Covered Activities 的五段項目符號。
範圍不是整篇重做：第一輪改動過的每一段與新寫進去的每一句、研究紀錄每一條 `verbatim_quote`、
`summary`／FAQ／callout／表格／圖解與正文的同步、界線與否定句，以及指派訊息點名的九個疑點。
約 **60** 條主張，再改 **13 處**。第 5 節那句 2026-03-23 聯名解釋令仍不在本篇 `sources[]` 內，
改以既有文章 `crypto-news-sec-crypto-interpretation-20260323` 的內容包交叉核對；沒有新增任何
`sources[]` 以外的網址當作文章依據。

### 重抓結果（與第一輪逐一相同，三條都是正文）

| source | HTTP | bytes | body | 複驗到的東西 |
| --- | --- | --- | --- | --- |
| PressReleases/9300-26 | 200 | 34,508 | 是（text/html，未轉址） | `Release Number 9300-26`、`September 17, 2026`、三條引文逐字 |
| csl/26-25/download | 200 | 232,223 | 是（PDF，7 頁） | 條件 1–10、Covered Activities 五段、結尾效力四句、註腳 2／6／14／22／24 |
| csl/26-09/download | 200 | 312,032 | 是（PDF，7 頁） | 報頭 `March 17, 2026`、`on behalf of Phantom … dated March 13, 2026`、同樣的不拘束委員會段 |

**抽字字元數的算法要更正一次**：七頁 `extract_text()` **直接相接**是 19,521／19,287，
`"\n".join` 才是研究紀錄記的 19,527／19,293（差的 6 就是六個接縫）。第一輪報告寫成「直接相接得 19,527」
是算法寫錯，**文件本身沒有變**，三個位元組數也完全相同。

### 第一輪那 20 處：全部複驗成立，沒有一處需要推翻

兩處實質錯誤的訂正都對：條件 10 的原文確實是第十項本身（`10. The PSP files a notice with the Division
agreeing to satisfy these conditions and consenting to the Commission’s jurisdiction…`）；
26-25 結尾確實是 `are based upon the facts and circumstances presented to the Division staff`，沒有主詞，
而 26-25 也確實沒有申請人（有申請人的是 26-09，抬頭 `Dear Mr. Jacobs:`）。
指派訊息點名的疑點逐條複驗：條件 3 的 `1.55(b)`、`to the extent relevant to the trading activity
facilitated by the PSP` 與整條例外都在；條件 5 的 `adopts and enforces policies and procedures reasonably
designed…` 在；條件 1、7 的承諾書與通知送交部門在；條件 8 的 `1.31` 在。
「六項前提」的 `among other things`、`each customer`、`e.g.` 三處寫法都對。
五處被還原的限定詞（`substantially`、`clearly and conspicuously`、`may`、`and/or`、`or other property`）今天再查一次都在。
`in its discretion`（依其裁量）**五處**（摘要第 4 句、第 5 節第 1 段、本文提醒 callout、FAQ 第 1 與第 4 題），
`as with all staff letters` 在第 5 節；全文「隨時」0 次。
免責 callout 與 `crypto.md` 程式比對逐字相同，本次沒有動。
研究紀錄 14 條非空 `verbatim_quote` 全部是今天重抽正文裡 **raw 即命中**的連續字串，沒有一條是拼接的。
FAQ 第 6 題的否定句以**詞界**（不是子字串）複驗：`taiwan` 在兩封信各 0 次，`china`／`asia`／`japan`／`korea` 同樣各 0 次。

### 第二輪再改的 13 處

**第一輪的訂正沒有同步到摘要與 FAQ（三處，指派訊息點名的 (a)）**

1. **`summary` 第 1 句仍寫著「僅對單一申請人生效的 Letter 26-09」**。第一輪把第一段、第 1 節標題與
   `description` 從「生效」改成「援用」（依據是註腳 6 的 `only the Beneficiary of a no-action letter may
   rely on it`），唯獨摘要沒跟著改，文章因此自己跟自己矛盾。已改成「僅有單一申請人能援用的」。
2. **`summary` 第 2 句掉了 `solely` 的「僅」**。原文 `solely as a result of them engaging in the Covered
   Activities`，正文第一段本來就有「僅」。摘要寫成「不會建議委員會因為這些提供者未登記……而對他們採取執法行動」，
   會被讀成未登記一概不究。已改成「不會僅因為……就建議委員會對他們採取執法行動」。
3. **FAQ 第 2 題的分潤仍是直述**：「由業者同意把相關收入的特定比例分給它」。原文是
   `which may also agree to share a specified portion of their relevant revenues`，第一輪已在正文補回
   `may`，FAQ 沒補。已改成「業者可以同意把……」。

**限定詞與但書（兩處）**

4. **條件 1 的但書 `absent a waiver by the Division` 從頭到尾沒寫進正文**（全文「豁免」0 次）。
   原文是 `The PSP, its principals …, and any individual engaged in soliciting Users as part of the Covered
   Activities are not subject to statutory disqualification, **absent a waiver by the Division**.`
   草稿與第一輪都把它寫成絕對禁止；研究紀錄的條件摘要本來就有這一句。已在第 4 節第 2 段補回「除非部門豁免」。
5. **圖解第一格說明「不介入個別委託」少了 `affirmative`**。原文
   `The PSP will not have any affirmative involvement with any particular orders`，正文寫的是「不積極介入」。
   圖上少一個詞就成了更強的主張。已改成「前端軟體，不積極介入個別委託」（14 字，仍在 15 字上限內）。

**日期混用（一處，指派訊息點名的 (f)）**

6. **第 5 節第 2 段「2026 年 3 月 23 日，……聯名發布過一份解釋令」**。那份文件是 2026-03-17 由兩個委員會作成、
   2026-03-20 送存、**2026-03-23 刊登兼生效**——既有文章 `crypto-news-sec-crypto-interpretation-20260323`
   第一段就把三個日期分開寫。把 3 月 23 日寫成「發布」是 BRIEF 型態 11 的混用，也和被連結的那篇不一致。
   已改成「聯名的解釋令刊登在聯邦公報」，同句後半的「刊登當天就生效」保留。

**圖解與正文不一致（三處，指派訊息點名的 (i)）**

7. **圖解 caption 把適用活動掛到十項條件上**。原文寫的是「依 CFTC Letter No. 26-25 的十項條件可以做與不能做的事」，
   但圖上四格（開發下單介面、收費與分潤、不得保管資產、不得給買賣訊號）全部出自信中**第 6 頁的
   `Covered Activities` 定義**，不是第 4–5 頁編號 1–10 的條件；圖又掛在講適用活動的第 3 節末尾。
   已改成「依 CFTC Letter No. 26-25 定義的『適用活動』」，內容包 image caption 與研究紀錄 `diagram.caption` 同步。
8. **圖解第二、三格寫「用戶」**，正文、摘要與 FAQ 一律「使用者」。已改成「向使用者收費、與業者分潤」
   「不得持有或保管使用者資產」（各 12 字）。第四格維持第一輪的版本。

**主體被換掉（兩處）**

9. **條件 4 的「不透過這個軟體」**（第 4 節第 1 段與 FAQ 第 3 題同一句）。原文是
   `they continue to have the ability to access the respective Registrant **independently of the PSP**`，
   以及適用活動那段的 `without the PSP’s involvement`——限制的對象是**提供者**，不是它的軟體。
   寫成軟體會把這條收窄（換個軟體就算數）。已改成「不透過提供者」。第 3 節第 1 段本來就寫對，沒有動。
10. **FAQ 第 7 題「促成這次無異議函的申請活動裡」**。落在 TSV 函前提之外的是 **26-09 申請人**所提的活動
    （`In relation to Letter 26-09 … As certain of these activities fell outside of the TSV Letter
    Requirements`），不是 26-25 本身。已改成「Letter 26-09 申請人所提的活動裡」，與正文第 2 節第 2 段一致。
11. **FAQ 第 7 題補回「在適當情形下」**（`Commission staff has, **under appropriate circumstances**,
    determined that certain TSVs need not register`）。正文有，FAQ 掉了。

**用語與研究紀錄（兩處）**

12. **第 1 節第 2 段「不能引用該函」的「引用」改成「援用」**：`rely on` 全篇其餘七處都寫「援用」。
13. **研究紀錄第 13 條 `verbatim_quote` 砍掉抽取瑕疵**：原本是
    `Each document or notice required to be submitted under these conditions  to the Division`，
    `conditions` 後面那兩個空白是 pypdf 的字距瑕疵（26-09 同一句抽出來只有一個空白），
    而這份紀錄自己的 `sourcing_notes` 寫明「只取沒有斷字瑕疵的連續字串」。已縮短到
    `Each document or notice required to be submitted under these conditions`。

**字數**：上面兩處加字（條件 1 的但書 +7、第 5 節的刊登 +3）依規格等量刪減，刪的是重複敘述不是限定詞——
第 3 節第 1 段「用封閉式定義畫出……只包含」改成「把……定義成只包含」（「封閉式」的意思由「只包含」承擔）、
第 4 節第 2 段刪掉「那種」與「則是……一份」。zh-TW 段落 **2,993 → 2,992**，餘裕從 7 字變成 8 字。
（附帶更正：第一輪報告與研究紀錄寫的 2,994 與自檢當時印的 2,993 對不上，2,993 才是對的，研究紀錄已改。）

### 第二輪查過而且正確、沒有動的部分

- **骨幹**：誰發的、什麼時候、什麼層級的文件、十項條件、三條禁止規定、不拘束委員會、效力界線是條件不是日期——
  全部回得到兩封信原文。
- **表格**五列與 caption 成立，包含「兩封信皆為 MPD 依 17 CFR 140.99 發出、對委員會皆無拘束力」：
  26-09 第 7 頁與 26-25 第 7 頁各有一段幾乎相同的 `not binding on the Commission`。
- **兩個結尾連結**：第一個 text 與幣圈索引 zh-TW title 逐字相同，第二個與
  `crypto-news-sec-crypto-interpretation-20260323` 的 zh-TW title 逐字相同，`check_article.py` 對兩者都沒有 FAIL
  （依 `DELTA-4-5.md` 第 3、4 條，本批不應再有那兩條 FAIL，實測也沒有）。
- **界線**：沒有幣價、漲跌幅、市值、交易量、資金流、報酬或費率比較；事件契約與永續契約只以「信中列舉的可送單商品類型」出現；
  Phantom 只以 26-09 的受益人與其自述業務出現；沒有推薦語氣、沒有「本站實測」。`hero.alt` 依規格沒查也沒改。

### 留給站主的事

1. **第一輪留下的五件事全部維持**，本輪沒有代為決定（律師代提與 Request 含補充往來的顆粒度、
   26-25 註腳 2 的 `Inc` 少一個句點、26-09 Re: 行印成 `Section 4(k)`、字數餘裕、沒有查也沒有寫的那三類文件）。
2. **第 5 節第 2 段那一句的依據不在本篇 `sources[]` 內**。本篇三條來源都是 CFTC 的新聞稿與兩封信，
   聯名解釋令的事實是以站上既有文章為準寫的。第二輪已把說法改到與那篇一致；
   若站主希望每一句都由本篇自己的來源撐住，就要把聯邦公報那條加進 `sources[]`（會變四條，仍在 2–4 上限內）。
3. **圖解要用新版重畫**：第一格「前端軟體，不積極介入個別委託」、第二格「向使用者收費、與業者分潤」、
   第三格「不得持有或保管使用者資產」，caption 改成「依 CFTC Letter No. 26-25 定義的『適用活動』」。

### 結論

`ok`。第一輪的 20 處改動全部複驗成立；第二輪再改 13 處，其中三處是第一輪的訂正沒有同步到摘要與 FAQ、
一處是條件 1 的但書從頭到尾沒進正文、一處是 2026-03-23 的日期混用。沒有任何一句需要推翻，也沒有動骨幹。

自檢輸出：

```
OK crypto-news-cftc-passive-software-20260917 zh-TW paragraphs 2992
```
