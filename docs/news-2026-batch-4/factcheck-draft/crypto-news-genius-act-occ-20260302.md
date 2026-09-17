# 獨立查核：crypto-news-genius-act-occ-20260302

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，
且六處一致，依 FACTCHECK.md「不要因為你今天重查就改它」維持不動）。

查核方式：`sources[]` 三條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
擬議條文本身逐條讀過（不只讀前言），`Question` 編號以正規式逐一比對，
59 條 `verified_facts` 的 `verbatim_quote` 以程式確認都是所掛網址上可搜尋到的連續字串。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，也沒有猜任何識別碼。
所有請求都沒有帶 email、姓名或任何個人資料。

檢查的主張：**98 條**（正文 51 個子句、摘要 4 句、五個小節標題、FAQ 6 題的問與答、
兩個 callout、表格 15 格與 caption、圖說、title、description、研究紀錄的四格與 `hero_label`）。
**改了 12 處**，另有 5 件留給站主。骨幹論述（這是草案不是生效規則、一比一準備金、
兩個營業日贖回上限）沒有被推翻。

## 重抓結果（三條 sources 都讀到正文，沒有一條是擋阻頁）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| FR 全文 `.txt`（2026-04089） | 200 | 800,323 | 是（GPO 全文） | 報頭、`AGENCY`／`ACTION`／`DATES`、Docket ID、RIN、`12 CFR Parts 3, 6, 8, 15, and 19`、註 12、註 53、註 93、擬議 15.1／15.10／15.11／15.12／15.14／15.15／15.16／15.30／15.31／15.32／15.41／15.42 條文本身、修正的 3.22(i)／6.2／8.2／8.6(c)／8.10／8.11／8.12、PART 15 兩種標題、Question 1–211 |
| FR API JSON（2026-04089） | 200 | 6,982 | 是（結構化欄位） | `citation` `91 FR 10202`、`page_length` 102、`publication_date` 2026-03-02、`type` Proposed Rule、`action`、`effective_on` `null`、`signing_date` `null`、`comments_close_on` 2026-05-01 |
| govinfo 公法 119-27 | 200 | 185,846 | 是（開頭 `[119th Congress Public Law 27]`） | `SEC. 20. ... EFFECTIVE DATE`（只有公式、沒有日曆日期）、`Approved July 18, 2025.` |

全文 `.txt` 的 4 個 NUL 位元組仍在（去掉後 800,319 bytes），`grep` 會把它當 binary，
研究紀錄記的配方今天照樣可重現。bytes 與紀錄一字不差，內容沒有改版。

## 改掉的 12 處

1. **「另外幾類都建立在這些資產之上」是假的**（第 3 節第 1 段）。擬議 15.11(b) 第 **(7)** 類是
   `(7) Any other similarly liquid Federal Government-issued asset approved by the OCC, in consultation
   with the State payment stablecoin regulator, if applicable`——它是留給 OCC 認可的**其他**聯邦政府發行資產，
   完全不建立在 (1) 到 (3) 之上。真正建立在其他類之上的是 (4) 附買回、(5) 附賣回、
   (6) 只投資於 (b)(1)–(5) 的政府型貨幣市場基金與 (8) 代幣化形式。
   已改成「其餘幾類多是這些資產的衍生形式，例如不超過隔夜的附買回與附賣回，
   另有一類是 OCC 認可的其他同等流動聯邦政府發行資產」。
   「八類」本身**沒有問題**：條文自己編號 (1) 到 (8)，引導語是 `must comprise exclusively:`，
   是封閉清單，所以既沒寫窄也沒寫寬。
2. **「四層申報」「四個週期」沒有來源**（title、第 4 節標題、第 4 節第 2 段、圖說、研究紀錄 diagram）。
   全文沒有把這四項編成一組，也沒有印過「四」。反過來說，草案自己的文書減量法一節把頻率印成
   `Frequency: Weekly, monthly, quarterly, annually, event-generated, and on occasion`（**六項**），
   而擬議 15.14 另有 (l) 的年度查核財報、(m) 的變更控制權申報，擬議 15.11(f) 還有每月具結——
   所以「四」不只沒有依據，而且比文件自己的清單窄。
   已全部改成不帶數字：title 與小節標題用「定期申報」，正文用
   「申報則不只一個週期，草案至少要求以下幾項」，圖說與研究紀錄 `diagram.title`／`caption`
   去掉「四道關卡」（`diagram.title` 改為「OCC 草案設下的關卡」）。
3. **修正篇目的清單不完整**（第 1 段）。原句「並修正既有的 part 3、part 6 與 part 8」寫成完整清單，
   但報頭印的是 `12 CFR Parts 3, 6, 8, 15, and 19`，而且草案確實要改 `19.1`、`19.3`、`19.180`
   （把 GENIUS Act 第 6 條下的停止命令、除職禁止、罰鍰與正式調查納入 part 19 的程序）。
   已改成「part 3、part 6、part 8 與 part 19」，但不寫 part 19 的內容。
4. **擬議 15.31(a)(3) 的但書被刪掉**（第 2 節第 2 段）。條文是
   `holds reserves in United States financial institutions sufficient to meet demands of United States
   customers, unless otherwise permitted under a reciprocal arrangement created and implemented by the
   Secretary of the Treasury under section 18(d)`。原句只寫「在美國金融機構持有足夠準備」，
   把要件寫死了。已補「（互惠安排另有許可者除外）」。
5. **擬議 15.11(g)(2)(i) 的例外被刪掉**（第 3 節第 2 段）。條文是
   `prohibited from issuing any new payment stablecoins immediately except as necessary to facilitate a
   transfer of payment stablecoins from one distributed ledger to another and provided that the net
   outstanding issuance value does not increase`。原句寫成無條件的「立即停止新發行」。
   已補「（跨帳本移轉且淨額不增加者除外）」。同一個例外句也在擬議 15.41(c)(2)。
6. **「銀行端要透過子公司」把範圍放大**（第 2 節第 2 段）。擬議 15.30(a)(1) 只對
   **受保**國民銀行、聯邦儲貸機構與**受保**聯邦分行課子公司路徑；未受保的國民銀行與未受保聯邦分行
   走 (a)(2) 的聯邦合格發行人路徑，可以自己發行。同段上一句引的註 93 也只寫「受保」。
   已改成「受保銀行端要透過子公司」。
7. **FAQ 第 3 題少寫了一個分支**。擬議 15.12(c)(3) 提前贖回的條件有兩個：
   `if the OCC determines that the issuer has the ability to redeem sooner in an orderly fashion and
   through a fair and transparent process` **or** `the OCC otherwise provides notice ... that the extended
   redemption period no longer applies`。已補「或 OCC 另行通知延長期間不再適用」。
8. **「聯邦準備理事會」不是原文的字**（第 4 節第 1 段）。擬議 15.12(b)(1)(ii) 印的是
   `by the OCC, Federal Reserve, or the State payment stablecoin regulator`，不是 Board of Governors。
   已改成「聯準會」；同時把「裁量性限制」掛回它的條次，寫成「同款 (ii) 的裁量性限制」。
9. **摘要第 3 句是沒帶草案字樣的操作性句子**。原句「贖回的時限訂為不超過兩個營業日……」
   違反 `must_not_write` 第五條（每一個操作性句子都要帶草案或擬議）。已改成「草案把贖回的時限訂為……」。
   第 3 節標題同理，從「準備金：按面額一比一……」改成「草案的準備金：按面額一比一……」。
10. **註 12 只寫了兩句中的兩句，第三句沒寫**（第 1 節第 2 段）。註 12 共三句，第三句是
    `The prohibitions that apply to a digital asset service provider would apply to an issuer to the
    extent that the issuer is a digital asset service provider.`
    已在句末補「而發行人若本身也是數位資產服務提供者，這些禁令同樣適用於它」。
    **前兩句本身查證無誤**：`must_fix 1` 確實套用了——(b)(1) 的 `begins on July 18, 2028` 與
    (b)(2) 的 `as of the effective date of the GENIUS Act` 拘束的都是數位資產服務提供者，
    文章沒有寫成「境外發行行為在生效日變成違法」。這是協調者點名的第一個高風險句，通過。
11. **第 5 節第 2 段依指示從 313 字壓成 153 字**。只留下「費用的金額還沒有訂、實際比率逐年在
    OCC 的年度費用公告發布」與「銀行端要把發行子公司解除合併」兩個重點；
    擬議 8.11、8.12、3.22(i) 的扣除正保留盈餘與排除投資／應收款兩項、以及 35%（最高 55%）的數字都不寫。
    同時刪掉第 5 節第 1 段開頭與第 3 節重複的「除了 Option A 與 Option B 二選一」。
12. **第 5 節新增一段給台灣讀者**（2–4 段的限制仍守住，第 5 節現在 3 段）。內容全部出自 `sources[0]`：
    擬議 15.1(b) 拘束的是那幾類美國機構而不是台灣讀者；擬議 15.12(d)(1) 要發行人用淺白文字公開
    自己的名稱、由誰負兌換義務、每月準備金組成報告的連結與購買及贖回的**所有**費用；
    擬議 15.10(c)(3) 禁止發行人直接或暗示表示穩定幣有美國全額信用擔保、受美國政府保證，
    或受聯邦存款保險或股金保險保障。三條都新增進 `verified_facts`，沒有金額、沒有推薦或比較語氣。

## 協調者點名的三個高風險句子

1. **註 12 的兩個時點**——通過（見上第 10 點），另補了第三句。
2. **擬議 8.11 的費用**——對**條文**成立：`8.11(a)` 的門檻是
   `50 percent or more of their interest and non-interest income`，`(a)(1) Minimum fee` 是一筆單純的最低費、
   金額由年度費用公告訂，`(a)(2) Additional amount for certain assets in excess of $1 billion` 才是加收。
   原句寫法正確。**但文件自己前後不一致**：8.11 的前言寫最低費是
   `a minimum fee associated with the first $1 billion of assets`，把它綁在前 10 億美元上。
   `must_fix 9` 的判斷對條文成立、對前言不成立。另外 8.11 只適用於擬議 8.10 底下的機構
   （非銀行聯邦合格發行人、受 OCC 管轄的境外發行人、受 12 U.S.C. 5903(d) 拘束的州級合格發行人），
   不適用於國民銀行——原句沒有寫出這個限制。依協調者指示整段已不寫，差異記進研究紀錄。
3. **八類準備資產**——「八類」與 `exclusively` 都正確，錯的是「都建立在這些資產之上」那半句（見上第 1 點）。

## 查過而且正確的部分（沒有動）

- **數字逐一對回擬議條文，全部成立**：93 天（15.11(b)(3)）；連續 15 個營業日（15.11(g)(3)，
  含「OCC 得自行決定延長」）；兩個營業日（15.12(b)(1)(i)，OCC 自稱 `outer limit`）；
  24 小時內 10% → 七個日曆日與 24 小時內通報（15.12(c)(1)、(c)(4)）；30 天完備通知（15.30(b)(3)(ii)）；
  第 120 天視為核准（15.30(b)(5)，起算日由 (b)(3)(iv) 定為 OCC 收到補足資料之日，
  文章「自 OCC 收到使其完備的資料當日起算」正確）；**超過** 100 億美元（15.15(b)(1) `more than $10 billion`）；
  250 億美元以上、0.5%、上限 5 億美元（15.11(d)）；500 萬美元與 12 個月總費用
  （15.41(a)(1)(i)(B)、(b)(1)）；180 天與其後每年（15.14(k)）；Question 1–211；篇幅 102 頁。
- **「Option A 與 Option B 數字相同」成立**。Option A 的安全港是 (c)(2)(i)–(v)，Option B 是 (c)(1)–(5)，
  五個數字（10%／30%／40%／50%／20 天）一一對應；Option B (4) 指向 (c)(1)，
  一如 Option A (iv) 指向 (c)(2)(i)，連「前述 10% 那一塊」的指向都一樣。
  「定案規則只會選一個」逐字是 `only one of which would be selected in the final rule`。
- **表格五列全對**：15.30(b)(3) 收件後 30 天內通知、15.30(b)(5) 完備後第 120 天、
  15.32(b)(4) 收件後第 30 天、15.30(e)(1) 收到通知後 30 天內（條文標題是 `Appeal`，用字是 `may request`）、
  15.14(k) 核准後 180 天內之後每年。
- **清點數字有三個站得住**：「六類」是 15.1(b)(1)–(6)、「四項要件」是 15.31(a)(1)–(4)
  （引導語 `all of the following requirements`）、「七種示例情形」是 15.42(a)(1)–(7)
  （引導語 `For example`，文章也照寫「示例」並保留「得」）。三者都是**條文自己的編號**，不是撰稿者清點。
  只有「四個週期／四層申報」沒有依據。
- **「OCC，隸屬美國財政部」**對得上報頭的 `DEPARTMENT OF THE TREASURY` / `Office of the Comptroller of
  the Currency` 與 `AGENCY: Office of the Comptroller of the Currency, Treasury.`。
  **註 93** 逐字是 `the OCC would not approve an insured national bank or a Federal savings association to
  issue a payment stablecoin directly (as opposed to through a subsidiary)`，文章寫法正確。
- **PART 15 兩種標題都在**：修正指示是 `12. Add part 15 to read as follows:` + `PART 15--PAYMENT STABLECOINS`，
  授權引註清單之後是 `PART 15--STABLECOIN`。FAQ 照來源並列、不擇一訂正，符合 BRIEF 跨篇型態第 4 條。
- **生效日只寫公式**。公法 `SEC. 20` 只有 `the earlier of (1) ... 18 months after the date of enactment` 與
  `(2) ... 120 days after ... any final regulations`，沒有印任何日曆日期；草案前言寫同一個公式。
  全文 **2027 出現 0 次**，沒有引用同批 FDIC 文件印的 `January 18, 2027`。
  註 12 的 2028 年 7 月 18 日是來源自己印的，且掛在數位資產服務提供者的禁令上，不是本法生效日。
- **界線乾淨**。OCC 經濟分析的 5,000 億／3,750 億／1,250 億美元、註 140 附近的私部門預測、
  Section IV 開頭「主要效果是支付型穩定幣總市值增加」那句、1,190 萬美元與
  `$11,929,204 million` 的排版錯誤、24／29 家假設、997 家與約 609 家小型實體、
  regulations.gov 的 257,601 則意見——**一個都沒有出現**。文中所有金額都是法定或擬議門檻。
  沒有任何一句把穩定幣、發行商、交易所或錢包寫成可以持有或選擇的對象，也沒有點名任何公司。
- **FAQ 第 4 題的算術示例沒有問題**。標明了「以下是編輯設計的例子」，講的是面額對公允價值
  （15.11(a)(1)(iii) 加上 15.2 的 `total consolidated par value` 定義），
  「而不是看它在市場上換到多少」只是排除次級市場價格，不是行情敘述，沒有任何會被讀成價格或報酬的說法。
- **免責 callout** 的 title 與 text 與 `crypto.md` 樣板**逐字相同**（含「不是投資建議」六個字），查核日 2026-09-17。
- **`checked_on` 沒有動**。2026-09-17 本來就是撰稿者讀到來源那一天，也是本輪重抓的同一天；
  內容包三條 source、研究紀錄、第 2 段查核句、表格 caption、圖說、免責 callout 六處一致。
- **59 條 `verified_facts` 的網址全部在 `sources[]` 之內**，`verbatim_quote` 全部是可搜尋到的連續字串
  （新增的三條刻意選單行片段，因為全文 `.txt` 會換行）。
- 摘要每個數字都在正文出現；FAQ 答案都是純文字、沒有網址；全文沒有簡體字；
  圖上與 `hero_label` 的數字（120、93）都在正文。
- 本篇沒有擴寫成 GENIUS Act 總覽，也沒有描述 FDIC／NCUA／FinCEN 與 OFAC 三案的內容。

## 留給站主的 5 件事

1. **`hero.alt` 還寫著「由每週到每年堆成四層的申報格線」。** 依任務書查核代理不動 `alt`
   （主圖由協調者繪製、`alt` 由協調者依實際畫面改寫），但「四層」已經從 title、小節標題、
   正文與圖說移除，改寫 `alt` 時請一併去掉；主圖構圖若已照「四層申報」畫好，也要一起調整。
   本 slug 目前還沒有任何已產出的圖檔（`apps/web/public/guides/<slug>/` 不存在）。
2. **title 從「……與四層申報」改成「……與定期申報」。** 目前 `apps/api/app/guides/content` 裡
   沒有別的內容包用舊 title 當 link text（已 grep），但日後 `pack_cli relink`／`autolink`
   與四篇 GENIUS Act 互連時要用新 title，四語系譯文也以新 title 為準。
3. **文件自身有一處不一致沒有寫進文章**：擬議 8.11 前言的「前 10 億美元」對條文的
   `(a)(1) Minimum fee`。已記進研究紀錄，**不要「訂正」任一處**。
4. **第 5 節壓縮後不再寫的內容**（目前 zh-TW 段落 2,982／3,000，補回需要等量刪字）：
   35%（最高 55%）的減除比率、擬議 8.11 與 8.12、3.22(i) 的扣除正保留盈餘與排除投資／應收款兩項、
   擬議 15.41(c)(3) 的「不得收取贖回費用」與「此後不得再發行」。依據都在 `verified_facts` 裡，刪的是篇幅。
   同理，擬議 15.11(b)(2) 的「受 FDIC 與 NCUA 依第 4(a)(1)(A)(ii) 條所定限制」這個但書
   也因為第 3 節用「核心是」做部分列舉而沒寫，若放寬字數應補回。
5. **`occ.gov` 今天沒有再測**（本篇不引用它的任何內容）；`uscode.house.gov` 的 12 U.S.C. 5901 頁面
   （修正清單 `must_add 6`）本輪同樣沒有納入 `sources[]`。兩者狀態下次仍要重測。

## 自檢

```
OK crypto-news-genius-act-occ-20260302 zh-TW paragraphs 2982
```

## 結論

**needs_owner。** 文章本身可刊：12 處都已改進內容包與研究紀錄，`sources[]` 三條今天都讀到正文，
界線沒有踩到，骨幹論述沒有被推翻。擋住「ok」的是第 1 與第 2 件——`hero.alt` 的「四層」與
title 改動要往主圖、索引與 `autolink` 傳，這兩件都在查核代理可動的三個檔案之外。

## 翻譯階段回頭抓到的三處（協調者更正，2026-09-17）

翻譯代理回報了三處繁中原稿的鬆動，協調者重抓 91 FR 10202 全文對回擬議 15.12 後改了 zh-TW
（四個譯文當初就是照正文與來源寫的，不必跟著改）：

1. 摘要第三句「單日贖回需求超過流通面額一成」→「單一 24 小時期間的贖回需求超過流通發行面額 10%」。
   條文是 `in excess of 10 percent of its outstanding issuance value in a single 24-hour period`；
   「單日」與「流通面額」都比條文鬆，而且中文數字「一成」會躲過 `check_article.py` 的摘要數字比對。
2. 第一節與 FAQ 第一題的「意見徵詢在 2026 年 5 月 1 日結束」→「文件印的意見截止日是 2026 年 5 月 1 日」。
   本文的來源只印了截止日，沒有任何一條能承載「已經結束、沒有展延」。
3. 第四節「裁量性限制只能由 OCC 課加，州級合格發行人的情形則是…」讀起來自相矛盾，
   改成「只能由主管機關課加：一般是 OCC，州級合格發行人則視情形是 OCC、聯準會或該州支付穩定幣主管機關」。
   條文是 `can only be imposed by the OCC or, in the case of a State qualified payment stablecoin issuer,
   by the OCC, Federal Reserve, or the State payment stablecoin regulator, as applicable`。

段落字數 2,982 → 2,992，`check_article.py --full` OK。
