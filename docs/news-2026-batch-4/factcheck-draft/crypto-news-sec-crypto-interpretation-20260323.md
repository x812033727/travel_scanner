# 獨立查核：crypto-news-sec-crypto-interpretation-20260323

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，五處一致，**沒有改**）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body；
聯邦公報 `.txt` 端點先剝 HTML tag 與 `[[Page NNNNN]]` 標記再正規化空白，
govinfo PDF 以**系統 Python 3.14.6 的 pypdf 6.16.2** 抽 20 頁全文，兩份文本互相比對；
CFTC 新聞稿剝 tag 後全文比對；FR API 的 metadata 逐欄讀。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，沒有猜任何識別碼，
任何請求都沒有帶入 email、姓名或個人資料。

檢查的主張：**107 條**（正文 41 句、摘要 4 句、FAQ 7 題答句共 27 句、兩個 callout 共 6 句、
表格 12 格與 caption、圖解 caption 與 4 段節點字串、title、description 2 句、`sources[]` 4 條）。
**改了 6 處事實、3 處編務**，另有 5 件留給站主。

## 重抓結果（四條 sources 都還在、都是真文件、位元組數與紀錄一致）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| FR 全文 `.txt`（2026-05635） | 200 | 170,238 | 是（20 頁釋令全文） | 報頭含多出來的 `li`、AGENCY／ACTION／SUMMARY／`DATES: Effective Date: March 23, 2026.`、五類分類段、第四至七節、第八節 Other Matters、署名欄、`[FR Doc. 2026-05635 Filed 3-20-26; 8:45 am]` |
| govinfo 已刊登 PDF | 200 | 353,096 | 是（pypdf 抽出 20 頁、165,092 字元） | md5 `e5613cb395282b5c52a3a694605d779a`；註 7／81／89／127／142 與 CFTC Voting Summary；與 `.txt` 互相吻合，含 `li` |
| CFTC 新聞稿 9198-26 | 200 | 37,594 | 是 | Release Number 9198-26、March 17, 2026、「joined the SEC **today**」、四點摘要、「will be published on CFTC.gov and in the Federal Register」、頁尾 `91 FR 13714` 與 Fact Sheet |
| FR API `2026-05635.json` | 200 | 3,468 | 是（metadata） | `type` = Rule、`comments_close_on` = null、`corrections` = []、`correction_of` = null、`signing_date` = null、`effective_on` = `publication_date` = 2026-03-23、pages 13714–13733、agencies = [CFTC, SEC] |

PDF 的 `/CreationDate` 今天仍是 `D:20260321130445Z`、`/ModDate` 是 `D:20260321090452-04'00'`——
**都是 3 月 21 日**，紀錄已經照修正清單 must_fix 1 不用它佐證 3 月 20 日送存，本次複驗結論相同。
`pypdf` 抽出的 165,092 字元可重現（19 個換頁以 `\n` 相接）；`page_views.count`（今天 5,600）與回應位元組數是活資料，兩個檔案都沒有把它們寫進文章。

**定稿日重跑（修正清單 must_add 7 與 live_data_warnings 要求）**：FR API 對本文件仍回
`corrections: []`、`correction_of: null`、`comments_close_on: null`。文章那兩句（「更正清單是空的」「沒有印截止日」）成立。

## 改掉的 6 處事實

1. **「它在每一類底下都列了具名例子」不成立**（第 3 節第 2 段）。
   釋令的具名例子**只出現在三類**：數位商品（`Examples of digital commodities include …`）、
   數位收藏品、數位工具；**穩定幣與數位證券兩節沒有任何具名資產**
   （以 `include`／`such as`／`example` 在該兩節內查核，2026-09-17 未見，兩節各 5,171／2,760 字元全讀過）。
   已改成「它**只在**數位商品、數位收藏品與數位工具三類底下列了具名例子」。
   同段的「清單以 include 起頭」與「結論基於委員會在作成日的理解」三類都成立，照舊。
2. **挖礦「兩種」、質押「四種」是清點出來的，來源沒有印**（第 4 節第 3 段與 FAQ 第 4 題）。
   釋令寫的是 `Only Protocol Mining Activities undertaken in connection with the following types … are addressed in this release:`
   後面接 `Self (or Solo) Mining`、`Mining Pool`；質押那一段同句式，接
   `Self (or Solo) Staking`、`Self-Custodial Staking Directly with a Third Party`、`Custodial Arrangement`、`Liquid Staking`。
   清單是關起來的（`Only`），但**全文沒有印出數量**——這正是 BRIEF 型態 9。
   已改成逐項指名、刪掉兩個數字；「只有」保留（它承載 `Only`）。
   研究紀錄的三條相關事實（挖礦、質押、附隨服務）也一併改成指名並註明來源沒有印數量。
3. **Protocol Mining／Staking 掉了網路的限定詞**（第 4 節第 3 段）。
   原文是 `on public, permissionless crypto networks that use proof-of-work`（質押同），
   前一版只寫「在工作量證明網路上」，會把結論擴張到許可制網路。
   已補成「在**公開、無需許可的**工作量證明網路上」，質押那半句補「**同類的**」。
4. **「明示」被刪掉**（第 4 節第 1 段，撰稿者自己點名的高風險句）。
   原文是 `it would be reasonable for a purchaser to expect profits based on the **explicit** representations or promises to engage in essential managerial efforts made by or on behalf of the issuer and conveyed to purchasers`。
   已改成「發行人所為或代其所為、並傳達給購買人的**明示陳述或承諾**算數」。
   **同一句的 `unless` 與註 89 的串通例外原本就都在，逐字複驗無誤**（見下一節）。
5. **註 123／125 的「how much」被寫成「以多少比例」，註 124／126 的「otherwise set」整個掉了**（第 5 節第 2 段）。
   原文是 `whether, when, or how much of a Depositor's digital commodities to stake` 與
   `guarantee or **otherwise set** the amount of rewards owed to the Depositors`。
   漏掉 `otherwise set` 會把「被排除在範圍外」的情形寫窄，方向上剛好偏向「所以現在可以做」。
   已改成「自行決定是否、何時、**質押多少**，或**保證、另行訂定**獎勵金額的安排」；FAQ 的「保證或固定」同步改成「保證或另行訂定」。
6. **FAQ 迷因幣例子的條件被放寬**。原文三個條件一個都不能省：
   `has **no** functionality within an associated functional crypto system`（沒有功能，**不是「功能有限」**）、
   `(and no related representations or promises to create such functionality or crypto system)`、
   `derives its value from the asset's artistic, entertainment, social, or cultural significance`。
   前一版寫成「功能有限」又刪掉整個括號，例子會被讀得比釋令寬。三個條件已全部補回，`may` 仍寫成「可能」。
   （這個例子**確實是釋令自己舉的**，在數位收藏品那一節的 `Some digital collectibles have limited or no functionality` 之後。）

## 改掉的 3 處編務

1. **title 改成「美國 SEC 與 CFTC 聯名解釋令：五類加密資產，刊登當天生效」**（33 字），研究紀錄的 `title` 同步、兩者逐字相同。
   同意協調者的理由：正文與 description 用的是「美國證券交易委員會（SEC）」與「商品期貨交易委員會（CFTC）」，
   標題的「證管會」與正文不一致；而且「證管會」在台灣是本地機關的舊稱，
   同批 JFSA 那篇的 `must_fix 1` 就是機關名混寫（把日本金融庁寫成金管會）。
   **改名安全**：`apps/api/app/guides/content/` 目前只有本篇自己帶這個標題字串，沒有別的內容包連到本篇。
2. **第 5 節第 3 段刪掉與下方 callout 逐字重複的識別碼串**，只留「聯邦公報引註 91 FR 13714」。
   文件編號與意見檔號在 callout 裡完整保留（FAQ 第 5 題也有意見檔號），資訊沒有損失；
   騰出的字數用來補上面那些限定詞。
3. **第 5 節第 1 段的分號改句號並改寫歸屬**。原句「另有註腳寫明，……其行為也在範圍之外；「不在範圍內」的意思是沒有處理，不是……」
   以分號相接，可能被讀成註腳自己這樣寫；釋令只寫 `activities are outside the scope of this release`，那個推論界線是本文的閱讀。
   已改成「範圍之外就是沒有處理的意思，**本文因此**不把它讀成「所以是證券」，也不讀成「所以現在可以做」。」

## 撰稿者自己點名的三句，逐句判定

1. **第 4 節第一段的第三人條款**：中譯**沒有**收窄或放大原文。
   `unless the representations or promises are authorized by the issuer and conveyed to purchasers` 的 `unless` 在（「除非那些陳述或承諾經發行人授權並傳達給購買人」），
   註 89 的例外也在（「但第三人與發行人串通傳達時，購買人依那些明示陳述期待獲利就是合理的」），
   `such as unaffiliated proponents … or holders …` 用括號「例如」保留了舉例性質。
   唯一的缺口是發行人那半句掉了 `explicit`，已補（上面第 4 點）。
2. **第 3 節第三段的穩定幣**：公式與用語都是**解釋令自己印的**，不是換算。
   註 80 逐字是 `The GENIUS Act will become effective on the earlier of 18 months after its date of enactment (July 18, 2025) or the date that is 120 days after the date on which the primary Federal payment stablecoin regulators issue any final regulations implementing the GENIUS Act.`——
   兩個分支、「取其早」、制定日 2025-07-18 全部在原文裡，文章沒有推算出任何日曆日期。
   「在該法生效之後才依法當然發生」對應 `These crypto assets categorically will not be securities by operation of statute **after the effective date** of the GENIUS Act.`；
   釋令並自己寫 `Given that the GENIUS Act is not yet effective`。
   **文章沒有任何一句會被讀成「穩定幣現在已經不是證券」**：第 3 節第三段與 FAQ 第 6 題都明寫現階段的依據是委員會對 Covered Stablecoins 適用 Howey 判準的解釋、不是法條本身；
   摘要與第 3 節第一段寫的是「是不是證券要看特徵而定」，對應釋令自己的
   `Stablecoins … are a broad category of crypto assets that may or may not be securities depending on their characteristics.`。
3. **第 5 節的「不在範圍內」與編輯設計的例子**：**沒有**被讀成「平台已受監理」，也沒有變相背書。
   第二段明標「以下是編輯設計的例子，不是實測」，問句的答案是「照文件讀不能這樣推」，
   沒有點名任何平台、沒有任何獎勵數字，並把註 123–126 的排除情形寫出來（第 5 點已把那兩處補精確）。
   第一段的歸屬問題已按上面編務第 3 點改寫。

## 查過而且正確的部分（沒有動）

- **三個日期沒有混寫**：署名欄 `By the Commissions. Dated: March 17, 2026.` 在兩位秘書長姓名之上
  （文章寫「作成、秘書長認證」，不是「秘書長簽署」，符合修正清單 must_fix 7）；
  17 CFR 第 231／241 兩份表格的 Release No. 33-11412 與 34-105020 日期欄都填 `March 17, 2026`；
  `[FR Doc. 2026-05635 Filed 3-20-26; 8:45 am]`；`DATES: Effective Date: March 23, 2026.` 只有一行。
  CFTC 新聞稿是 03-17、寫「今天」與 SEC 一起作成、並寫文件「將」刊登——三個日期與刊登狀態都對得上。
- **`does not itself create any new legal obligations` 與「沒有取代 Howey」逐字無誤**：
  `The interpretation does not itself create any new legal obligations for issuers of, and investors in, digital securities and crypto asset-related securities`（第九節）、
  `The interpretation in this release does not supersede or replace the Howey test, which is binding legal precedent.`（第一節）。
  FAQ 第 1 題把前一句的受詞完整寫出來，沒有擴張。
- **OMB／CRA 那一段照來源的話寫、沒有補因果**（修正清單 must_fix 5 的重點）：
  `Pursuant to the Congressional Review Act, the Office of Management and Budget ("OMB") has designated the interpretation in this release as a "major rule," as defined by 5 U.S.C. 804(2). Notwithstanding such designation, the interpretation in this release may take effect immediately pursuant to 5 U.S.C. 808(2) because it is an interpretive rule and thus exempt from the Administrative Procedure Act's notice and comment requirements.`
  `may` 寫成「可」、`Notwithstanding` 寫成「但」，並緊接一句「文件沒有說明 DATES 欄為什麼填 3 月 23 日」——
  該段（第八節 Other Matters）確實沒有解釋 DATES 欄。
- **五個類別的英文原名與限定詞**：`we classify crypto assets into five categories based on their characteristics, uses, and functions: (i) digital commodities; (ii) digital collectibles; (iii) digital tools; (iv) stablecoins; and (v) digital securities.`
  （`five` 是釋令自己印的，不是清點）。三句法律定位逐句對得上：
  `Digital commodities, digital collectibles, and digital tools, each as further described below, are not themselves securities.`、
  `Stablecoins, as further described below, are a broad category of crypto assets that may or may not be securities depending on their characteristics.`、
  `Digital securities, as further described below, are securities.`
  五個中文譯名與原文相符。分類非窮盡的但書（不屬任一類、混合特徵）也在。
- **註 81 的兩個 `generally` 都保留**：
  `payment stablecoins issued by a "foreign permitted stablecoin issuer" … registered with the Comptroller of the Currency will **generally** not meet the definition of "security," as such payment stablecoins will **generally** be considered "Covered Stablecoins."`
  FAQ 第 6 題寫「一般不會」「一般會被認為」。
- **註 127 與註 142 逐字無誤、位置正確**：
  `To the extent that Service Providers provide services not discussed below, their activities are outside the scope of this release.`（第 5 節第一段）、
  `The interpretation does not apply to or otherwise affect existing Commission or staff positions regarding employee compensation and benefit arrangements involving the issuance or award of securities.`（FAQ 包裝與空投那一題）。
- **包裝與空投的條件都對**：包裝是存入 Custodian 或 cross-chain bridge、一對一生成 Redeemable Wrapped Tokens、
  `without directly or indirectly offering any return, yield, profit opportunity, or additional good or service`、鎖住不得移轉出借質押再抵押、一對一贖回並銷毀；
  空投只處理未提供金錢、商品、服務或其他對價的受領人，`such as where the recipient performs a service` 即不適用，
  服務例子（追蹤社群帳號、轉發、撰文、推薦他人、修正程式瑕疵）是釋令自己舉的，文章用「包括」保留舉例性質。
- **分離與過去責任**：`any of the following non-exclusive indicia of separation` 的 `non-exclusive` 有保留（文章寫「非窮盡」）；
  第二個徵象的條件 `if a purchaser would not reasonably expect the issuer to be able to fulfill or to continue to engage in …` 寫對了；
  未登記又不符豁免 `the issuer will violate the Securities Act`、反詐欺責任 `even if the non-security crypto asset subsequently separates … and that investment contract ceases to exist` 都在。
  「兩個」這裡是釋令自己的小節編號（`1. Fulfillment …`／`2. Failure To Satisfy …`），不是清點，予以保留。
- **意見徵詢**：`we are soliciting public comment on the views set forth in the interpretation`、
  `the Commission **may** refine, revise, or expand upon the interpretation`——`may` 寫成「可能」；
  DATES 欄沒有截止日、FR API `comments_close_on` 為 null，文章與 FAQ 都沒有暗示任何截止日。
- **台灣那句的否定範圍正確**：`Taiwan`／`Taipei`／`China` 在 `.txt`、PDF 與 CFTC 新聞稿三處都是 **0 次**（詞界比對），
  文章寫成「以本文使用的……查核到 2026 年 9 月 17 日，未見」，沒有寫成「官方沒有」「從未」「第一份」。
- **界線（`crypto.md`）**：全文沒有幣價、漲跌幅、市值、交易量、ETF 資金流、殖利率、質押獎勵率、空投數量或任何獎勵金額；
  沒有比較或推薦任何交易所、錢包、託管業者或流動性質押提供者；
  釋令在三類底下列的具名資產**一個都沒有轉錄**，第 3 節第 2 段並寫明為什麼不轉錄；
  註 70 的 `coindesk.com` 沒有被引用或連結；CFTC 新聞稿裡 Atkins 主席
  「most crypto assets are not themselves securities」那句沒有進文章（只在研究紀錄的 `unverified_or_excluded`）。
- **沒有「缺草案字樣」的問題**：本篇是這批唯一已生效的文件，而且文章把它的定性寫清楚了——
  ACTION 欄與 FR API 的 `type` 都照抄（`Final rule; interpretation; guidance`／`Rule`），
  同時寫「它自己寫明不創設新義務」「這不是新法，而是主管機關把自己怎麼看既有法律寫成文字」，
  每一個操作性句子都是「解釋令說／釋令寫明」。
- **免責 callout 與 `crypto.md` 的樣板逐字相同**（tone、title、text 全等），含「不是投資建議」六個字，查核日 2026-09-17；
  本文提醒 callout 另計，共兩個。`checked_on` 在內容包四條 source、研究紀錄、第二段、表格 caption 與免責 callout **五處一致**，都是 2026-09-17，**本次沒有改動它**。
- **機械面**：摘要四句的每一個數字（2026／3／17／23／五）都在正文出現過；
  圖解 caption 與研究紀錄逐字相同、四段節點與正文一致、圖上沒有正文沒有的數字；
  FAQ 七題答案都是純文字、沒有網址；全文沒有簡體字、列表、Markdown 或 emoji；
  沒有任何一句寫容器或工具行為（修正清單 must_fix 2 與跨篇型態 10）。
- **`sources[]` 可追溯性**：四條全部承載事實、全部讀到正文，沒有任何事實掛在 `sources[]` 以外的網址；
  聯邦公報正規文件頁照舊排除（`curl -L` 落在 `unblock.federalregister.gov`、10,596 bytes 的 Request Access）；
  sec.gov 一句都沒有依賴。修正清單 `source_list_fix` 建議加的 FR API 已是第 4 條，
  「型別 Rule」「agencies 兩個機關」「更正清單是空的」三句都追溯得到。

## 留給站主的 5 件事

1. **五類的英文原名沒有印在文章裡**，只有中文譯名（五個譯名都與原文相符）。
   讀者要回頭搜原文會少一組關鍵詞。段落字數現在是 **2,948／3,000**，全部補上約需 80 字，補不進去；
   要補就得再砍別處的敘述，這是編輯取捨，查核代理沒有代決定。
2. **註 7 仍只在研究紀錄裡**（委員會明文推翻自己 2004 年 `In re Barkate` 的立場、認定依 Barkate 之後的判決
   Howey 的共同事業要件必須滿足）。修正清單 `must_add 1` 把它列為整份釋令法律動作最大的一步；受同一個字數上限限制。
3. **索引還沒列到本篇**。`check_article.py` 今天已經通過（索引內容包存在、第一條 link 的 text 對得上索引的 title）；
   但等索引列進本篇時，連到本篇的 link text 必須逐字用**改過後的新 title**
   「美國 SEC 與 CFTC 聯名解釋令：五類加密資產，刊登當天生效」，否則會在索引那一篇報錯。索引是另一個檔案，本代理沒有動。
4. **「截至 2026-09-17 沒有更正」是快照**：出刊當天要再抓一次
   `https://www.federalregister.gov/api/v1/documents/2026-05635.json` 確認 `corrections` 仍是 `[]`、`correction_of` 仍是 `null`。
5. **slug 尾碼與 `news_date` 都取刊登兼生效日 2026-03-23**（不是作成日 2026-03-17），與 C4 一致；
   修正清單說「選哪一個都行，但兩篇要一致」。若站主改採作成日，本篇與 C4 要一起改；
   文章內文已把 03-17、03-20、03-23 三個日期都明寫，不必改寫敘述。

## 自檢

```
OK crypto-news-sec-crypto-interpretation-20260323 zh-TW paragraphs 2948
```

## 結論

`ok`：107 條主張逐條回到四條一手來源核對，改了 6 處事實與 3 處編務。
骨幹論述——兩機關聯名、三個日期、五個類別與各自的法律定位、投資契約的開始與結束、
以及它自己寫明沒有處理的事——**逐條成立，沒有動到**。
改的都是限定詞（`explicit`、`public, permissionless`、`otherwise set`、`no functionality` 與那個括號）、
一個超出來源的全稱句，以及兩個來源沒有印的清點數字。
留給站主的 5 件事都是編輯取捨或出刊當天的例行複查，沒有一件擋住出刊。
