# 獨立查核：crypto-news-sec-regulation-crypto-assets-20260821

查核代理：未參與撰稿。查核日 **2026-09-17**（文章的 `checked_on` 本來就是 2026-09-17，五處一致，不改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，GovInfo PDF 用系統 `python`
的 pypdf 6.16.2 抽文字。**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，也沒有猜任何識別碼。

檢查的主張：**108 條**（正文 17 段的每一句、摘要 4 句、FAQ 8 題的答句、兩個 callout、表格 9 格與表頭與 caption、
圖解 caption 與研究紀錄 `diagram` 四格與 `hero_label`、title、description）。
**另加研究紀錄 76 條 `verbatim_quote` 的逐條機械比對**（見下一節）。
改了 **20 處**，研究紀錄另改 5 處，4 件留給站主。

## 撰稿者沒做完的那一步：76 條引文的逐條驗證

撰稿代理在「逐條驗證 `verbatim_quote`」之前因 API 錯誤中斷，所以這一步由本輪補做。
自寫 `verify_quotes.py`：把 `verified_facts[]` 每一條的 `verbatim_quote` 與它 `url` 對應的今日全文
都做 `re.sub(r"\s+", " ", …)` 之後做子字串比對，並同時檢查每條 `url` 是否在 `sources[]` 裡。

```
---- 76 facts checked, 0 MISS, 0 url-not-in-sources, 0 no-body ----
```

**76／76 全部命中，0 MISS，沒有任何一條 `url` 不在 `sources[]`。** 這是本批次目前唯一一篇引文欄位零瑕疵的紀錄。

為了證明這個結果不是程式太鬆，跑了負向控制：把 `corrections-crypto.md` must_fix 4 指出的那條錯誤引文
（`… not a general market conception of decentralization`）餵進去，回報 **MISS**；改成原文
（`… of what constitutes decentralization`）回報 **HIT**；把 `ACTION: Proposed rule.` 改成
`Proposed rules.` 也回報 MISS。程式抓得到錯。

**附帶抓到一個方法論陷阱，值得寫進後續批次**：聯邦公報 `.txt` 是約 72 欄硬換行，
**以「行」為單位的 grep 會漏掉被切開的字串**。佔位字串 `[INSERT EFFECTIVE DATE OF FINAL RULE, IF ADOPTED]`
就有一處被切在 `[INSERT` 與 `EFFECTIVE` 之間——逐行 grep 只找到 2 處，正規化空白後才是 3 處。
研究紀錄原本寫的「兩處」就是這樣少算的。本輪所有條號、金額、否定句都改用正規化空白比對重查。

## 重抓結果（四條 sources 都還在，body 都是正文）

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| 聯邦公報全文 `.txt` | 200 | 795,262 | 是。`<html><head><title>Federal Register, Volume 91 Issue 161 (Friday, August 21, 2026)</title></head><body><pre>` 包起來的公報全文，首個資料行是報頭 `[Federal Register Volume 91, Number 161 …]`，末行 `[FR Doc. 2026-17183 Filed 8-20-26 8:45 am]` |
| GovInfo 官方 PDF | 200 | 5,538,351 | 是。`application/pdf`，pypdf 讀出 **146 頁**，第 1 頁抽出文字首行為第 54510 頁頁首，SUMMARY 與 DATES 與 `.txt` 逐字相符 |
| 聯邦公報 API JSON | 200 | 70,689 | 是。compact JSON，`type`／`action`／`page_length`／`effective_on` 都在 |
| SEC 新聞稿 RSS | 200 | 18,402 | 是。`application/rss+xml`，**25 個 `<item>`**，最新 `pubDate` 為 `Wed, 16 Sep 2026 10:00:00 -0400` |

**協調者問的第 5 點：2026-76 還在 feed 裡。** 25 筆的視窗今天是 2026-89 至 2026-65，2026-76 在其中；
它的 `<title>` 是 `SEC Proposes New Regulation Crypto Assets`、`<link>` slug 帶 2026-76、
`<pubDate>` 是 `Tue, 18 Aug 2026 13:15:48 -0400`。**所以 `sources[]` 維持 4 條**，
依賴它的三句（新聞稿編號、標題、美東時間戳記）都可以留。`sec.gov` 的網頁對 `curl` 回 403，
但這個 RSS 端點今天可讀，與紀錄一致。

聯邦公報的正規網頁版（`/documents/2026/08/21/2026-17183/regulation-crypto-assets`）本輪沒有重抓，
因為它本來就沒有列進 `sources[]`（紀錄已說明它回 `Request Access` 攔截頁）。

## 改掉的 20 處

**射程與限定詞（協調者第 2、8 點）**

1. **Rule 306 停止的是「募資豁免」，不是「某項豁免」**（第 4 節第 3 段＋摘要第 3 句）。這是本輪最重要的一處。
   條文寫的是 `temporarily suspending an exemption under this subpart`，而 **Sec. 228.306 位於 Subpart C
   （Fundraising Exemption）**——`.txt` 的子部結構是 Subpart A 一般規定（228.100–104）、
   Subpart B 新創豁免（228.200）、Subpart C 募資豁免（228.300–307）、Subpart D 安全港（228.400）、
   Subpart E 合格買方（228.500）。所以它**不及於新創豁免，也不及於安全港**；條文提到的 offering statement
   與 Sec. 228.305 報告也都是募資豁免那一套機制（新創豁免走的是 Form NOR 與 Form TR）。
   原文「豁免也可以被停止」接在安全港那兩段之後，讀者會以為安全港可以被停止。
   已改成「募資豁免也可以被停止」；摘要第 3 句同步改成「募資豁免本身也可以被委員會暫時停止」。
2. **Rule 306 少了「有理由相信」**。條文是 `if it has reason to believe that:`，原文寫成「基於六種事由作成命令」，
   把一個門檻寫成了既定事由。已補回。
3. **Rule 306「沒有人請求時」少了第二個要件**。條文是
   `If no hearing is requested **and none is ordered by the Commission**`，原文只寫「沒有人請求時」。
   已改成「沒有人請求、委員會也沒有另行指定時」。同句的「成為永久」補上條文緊接著的
   `and shall remain in effect unless or until it is modified or vacated by the Commission`
   （改為「並持續到委員會修改或撤銷為止」），否則「永久」比來源絕對。另補回請求聽證須「以書面」。
4. **Rule 101(d) 被寫成無條件規則**。原文是「Rule 101(d) 規定輕微偏離不會使豁免失效」。
   條文 (d)(1) 是**附三項舉證要件**、而且只及於「對特定個人或實體的該次要約或出售」：
   須由主張豁免之人證明 (i) 該違反與直接保護該特定對象的條件無關、(ii) 就整個募集而言輕微、
   (iii) 已善意且合理地嘗試遵循全部條件。已照條文改寫。
5. **Rule 101(d) 後半句少了前提**。條文 (d)(2) 是
   `**Where an exemption is established only through reliance upon paragraph (1)**, the failure to comply is
   nonetheless actionable by the Commission under section 20`。原文寫成「這種失誤仍可由委員會依第 20 條追究」，
   漏了「豁免只靠這一款成立時」。已補回。
6. **SUMMARY 欄三個限定詞被刪**（第 2 節第 3 段）：`certain` principles-based narrative disclosures、
   make available `to their investors`、antifraud and antimanipulation provisions `of the Federal securities laws`。
   已補成「向投資人提供某些原則導向的敘述性揭露」與「聯邦證券法反詐欺與反操縱條款」。
7. **PWG 報告的三項建議被寫成全清單**（第 5 節第 1 段）。原文是
   `Some of those recommendations were directed at the Commission, **including** that the Commission should …`，
   下面才是三個 bullet。原文寫成「報告建議委員會建立 A、B 與 C」。已改成「對委員會的建議包括……」。
   同句另補回兩個限定詞：空投安全港是 `safe harbor for **certain** airdrops`（已改「針對特定空投的安全港」）、
   第 5 條豁免是 `exemption from **registration**`（已補「註冊」）。
8. **Rule 103(a) 的一致性要求被併類又放大範圍**（第 3 節第 1 段）。原文寫「與發行人在官網、官方社群帳號
   與白皮書等既有公開管道上的說法一致」。條文分成**兩類**——
   `established public communication channels (such as its website or official social media accounts)`
   與 `promotional materials (such as whitepapers)`——白皮書是宣傳資料，不是公開管道；
   而且該要求限於 `relating to **material aspects** of the issuer, the subject crypto asset, and the
   associated crypto network or associated crypto application`，原文把範圍寫成全部說法。
   已分開兩類並補回「關於重要面向的」。另把「還要……一致」改為「也應……一致」，對應條文的 `should`。
9. **FAQ 8「所有意見都會公開」少了緊接的但書**。ADDRESSES 欄在
   `The Commission will post all submitted comments on its website` 之後緊接著寫
   `The Commission may redact in part or withhold entirely from publication submitted material that is obscene
   or subject to copyright protection.` 已補上。
10. **安全港效果的賓語不完整**。條文是 `will be deemed **not to constitute or represent or to be subject to**
    that investment contract`，FAQ 4 只寫「不受該投資契約拘束」，已補成「不構成、不代表也不受」。
    第 4 節第 2 段最後一句的 `asserting that a crypto asset **is subject to an investment contract** (or is
    otherwise a security)` 原本只寫「屬於證券」，已補回「受投資契約拘束或」。
11. **covered investment contract 的定義少了兩個字**。條文是 `a **contract, transaction, or scheme**
    involving a crypto asset`，原文只寫「安排」。已補成「契約、交易或安排」。

**清點數字（協調者第 2 點：來源自己有沒有印或編號）**

12. **「三個界線」沒有來源編號，已改掉**（第 4 節第 2 段＋FAQ 4）。釋義那三句分別以
    `As with any safe harbor, however`、`Finally, even if`、`Moreover, while` 起頭，**文件沒有印「三個」**。
    已改為不帶計數的寫法。
    — 相對地，**這四個清點數字是條文自己印的編號，予以保留**：covered investment contract 的
    **三項要件**（條文印 `(1)`／`(2)`／`(3)`）、Rule 103(b) 的**十類**（條文印 `(1)` 至 `(10)`，
    釋義的節級標題也以 `i.` 至 `x.`、`Paragraph (b)(1)` 至 `(b)(10)` 對應）、
    Rule 306(a) 的**六種**情形（條文印 `(1)` 至 `(6)`）、Rule 400 的**兩項**條件（條文印 `(a)`／`(b)`）。
    前兩處另在正文加註「條文編號的」，讓讀者知道計數是文件自己的。
13. **刪掉「這是草案在文字上與美國穩定幣法接上的一處」**（第 2 節第 1 段）。「一處」是計數式斷言
    （該法全名在全文確實只出現 1 次，但那仍是查核者數的），而且整句是評論性補述，刪掉不損事實。
    註 122 的實質內容（定義相同、Public Law 119-27）保留——`corrections-crypto.md` must_fix 1 要的就是這一句。

**「沒有生效日」與待填字串（協調者第 4 點）**

14. **佔位字串不只在失格條款那一處**（第 1 節第 2 段＋摘要第 4 句）。以正規化空白比對，
    `[INSERT EFFECTIVE DATE OF FINAL RULE, IF ADOPTED]` 在全文出現 **3 次、跨兩個條文**：
    Sec. 228.104(a)（失格事由的但書）、Sec. 228.104(b)（舊「bad actor」事由的揭露義務）、
    以及 **Sec. 228.300(b)(4)**（募資豁免的發行人資格，交易法第 12(j) 條命令的排除但書）。
    原文寫「在失格條款那一處」。已改成「在失格條款與募資豁免的發行人資格條款處」；
    摘要改成「規則原文該寫生效日的地方」，不印查核者自己數的次數。
    — DATES 欄本身**確認只寫兩件事**、沒有生效日也沒有遵循期限（見下一節）。
    — API 的 `effective_on` 今天仍是 **2026-08-21**，與 `publication_date` 同日；文章說它不能替代 DATES 欄，成立。
15. **callout 那句「未見延長意見期的公告」改掛得到的來源**。原句是
    「以聯邦公報查核到 2026 年 9 月 17 日，未見延長意見期的公告」——那要靠聯邦公報**搜尋 API** 才成立，
    而那個網址不在 `sources[]`（研究紀錄自己也把它列進 `unverified_or_excluded`）。
    已改成「以聯邦公報的文件紀錄查核到 2026 年 9 月 17 日，type 欄仍是 Proposed Rule、
    意見截止日仍是 2026 年 10 月 20 日」——這兩個值今天都直接讀自 `sources[2]`。

**Project Crypto 的日期（協調者第 1 點）：查了，**沒有**錯，沒有改**

16. 見下一節。這一點是本輪唯一「BRIEF 點名過、但這一篇沒有犯」的項目，只在同段補了兩個限定詞（見第 7 處）。

**條號與定義（協調者第 3 點）**

17. **Rule 500 是「新增」定義，不是「重新定義」**（FAQ 6）。釋義寫的是
    `Subpart E would **define** ``qualified purchaser'' for purposes of section 18(b)(3)` 與
    `would set forth **a definition** of ``qualified purchaser'' in Rule 500`，
    `corrections-crypto.md` must_add 10 也寫「擬**新增**」。沒有既有定義被改寫。
    已改成「新增一個就證券法第 18(b)(3) 條適用的『合格買方』定義」。
    同題結尾「也就是它會失效」改成「也就是這一層優先排除不是永久的」，並把釋義那一句改成引號直引。
18. **FAQ 3 的「必須寫在該溝通的表面上」不是來源的用語，已刪**。
    `on its face` 與 `face of the communication` 在全文以正規化空白比對**都是 0 次**；
    Rule 304(b) 寫的是 `The communications must: (1) State that no money or other consideration is being
    solicited …; (2) State that no offer to buy … can be accepted …; (3) State that a person's indication of
    interest involves no obligation or commitment of any kind`。
    已改成條文實際要求該溝通載明的那三件事，並補回 Rule 304(a) 的「或其授權之人」。
    （這個「表面上」是從 `corrections-crypto.md` must_add 3 的措辭一路抄進研究紀錄再抄進文章的，
    修正清單本身在這裡也不精確——研究紀錄已加註說明。）
19. **FAQ 7 第 49／50 題的歸屬寫錯了**。原文把「限於實體」與「在美國設立或登記」兩件事一起掛在第 49、50 兩題上，
    其實**兩件都在第 49 題**（`Should we include an issuer eligibility requirement that would limit use of
    Rule 200 only to entities (i.e., excluding natural persons)? If so, should we require that such entity be
    formed or incorporated in the United States?`）；**第 50 題**問的是要不要比照募資豁免加上美國連結條件
    （多數高階主管或董事為美國公民或居民、逾 50% 資產在美國、業務主要在美國管理）。已分開寫。

**否定句的範圍（BRIEF 型態 2、6）**

20. 三處概括否定與一處無來源斷言：
    - 「**也沒有規定購買人的國籍或居住地**」（第 5 節第 3 段＋FAQ 7）是對 146 頁文件下的概括否定。
      以正規化空白比對，`nationality` 與 `domicile` 全文 **0 次**，`citizens or residents` 的 7 處**全部**
      掛在發行人的高階主管或董事——所以實質為真，但依 BRIEF 型態 2 仍不寫成概括否定。
      已改成正面陳述：「被要求要有美國連結的是募資豁免下的發行人，不是買方，
      購買人那一側的條件是合格投資人身分與 10% 上限」。
    - FAQ 5 的「**文件沒有寫任何關於可以拿到多少的內容**」同理，已改成
      「這一款處理的不是分配的數量；本文也不寫任何可以拿到多少的內容」。
    - 「**聯邦公報上每份文件都有 type 欄與 action 欄**」（第 5 節第 2 段）是從一份文件推及全體，
      已改成只講這一份的 type 欄與 action 欄。
    - 「安全性那一類**常被讀成**『草案要求公開原始碼』」是關於外界怎麼解讀的無來源斷言，
      已改成直接說條文不是那樣寫的。條文的實質（`to the extent the issuer has made it publicly available`、
      該款沒有 `free of charge`）不動。

**表格（協調者第 6 點）**

21. **4 欄改 3 欄**（制度｜募集上限｜財報要求），每格縮短：
    | 草案裡的制度 | 募集上限 | 財報要求 |
    | --- | --- | --- |
    | 新創豁免（Rule 200） | 四年期間 500 萬美元 | 不要求財報 |
    | 募資豁免 Tier 1 | 12 個月 2,000 萬美元 | 須附財報，無查核要求 |
    | 募資豁免 Tier 2 | 12 個月 7,500 萬美元 | 須附財報並經查核 |

    依協調者授權移除「申報表格」整欄與關係人出售上限（600 萬／2,250 萬美元）。
    `caption` 未動，仍帶查核日與「這是草案的內容，不是現行制度」與「是發行人端的募集上限，不是任何人的投資額度」。
    **表中六個數字逐一對回條文**：500 萬＝Rule 200(b)(4) 的 `$5,000,000`；
    2,000 萬＝Rule 300(a)(1) 的 `$20,000,000`；7,500 萬＝Rule 300(a)(2) 的 `$75,000,000`。
    **一個要記下來的細節**：「12 個月」**不在** Rule 300(a)(1)／(a)(2) 的條文裡，
    條文只寫金額；`in a 12-month period` 出自釋義（`Under Tier 1 … up to $20 million … in a 12-month period`、
    Tier 2 同句式），SUMMARY 欄也寫 `during each 12-month period`。表格印 12 個月是掛釋義，不是掛條文，
    研究紀錄已加註。三格財報要求分別對回
    `For Tier 1 offerings, there is no financial statement assurance requirement.`、
    Tier 2 的 `must be audited in accordance with either U.S. GAAS or PCAOB standards`、
    以及釋義的括號句 `(but would not be required to do so under the startup exemption)`。

字數：原稿 2,950／3,000，上述補回的限定詞把它推到 3,127。依 FACTCHECK.md
「不可以刪但書或限定詞來湊字數」，改為精簡**純敘述**：SEC 英文全名改括號縮寫、
刪「三個日期不能混用」（小節標題已寫同一件事）、刪「也就是本文開頭那一天」、
刪「委員個別聲明的內容與公眾意見件數不在本文範圍」、刪第 3 節第 3 段與段首重複的「既沒有要求公開原始碼」。
**定稿 2,988 字，沒有刪掉任何但書或限定詞。**

## 查過而且正確的部分（沒有動）

- **Project Crypto 的日期站得住，這一篇沒有犯 BRIEF 型態 11 那個錯。**
  這份 8 月提案的**本文自己**以自己的語氣寫
  `On July 31, 2025, following publication of the President's Working Group Report, Commission Chairman
  Paul S. Atkins announced the launch of ``Project Crypto''`，註 49 引的是**同一天**（July 31, 2025）的那場演講
  `American Leadership in the Digital Finance Revolution`。
  也就是說**日期是本文寫的，不是從註腳裡一場演講的日期推出來的**，而文章的「宣布啟動」
  正對應 `announced the launch`。前期研究把註腳日期當啟動日那個問題，在這一份 8 月文件上不成立，
  所以這句**不改**。同段另兩句也逐字對回本文：
  2025-01-23 的行政命令設立 President's Working Group（`issued an executive order … on January 23, 2025`、
  `established the President's Working Group on Digital Asset Markets`）、
  2025-07-30 的 PWG 報告（`On July 30, 2025, the President's Working Group issued a report`）。
  兩句只需補 `including` 與 `certain` 兩個限定詞（已於第 7 處處理）。
- **DATES 欄逐字確認只有兩件事**：`DATES: This release was published in the Federal Register on August 21,
  2026. Comments should be received on or before October 20, 2026.`——沒有生效日、沒有遵循期限。
  API 的 `dates` 欄位是同一句。
- **三個日期都對**：署名區 `By the Commission. Dated: August 18, 2026.`、
  末行 `[FR Doc. 2026-17183 Filed 8-20-26 8:45 am]`、
  報頭 `[Federal Register Volume 91, Number 161 (Friday, August 21, 2026)]`。
  送存註記沒有寫時區，文章也只寫送存日、不寫時刻，正確。
- **API 今天的值**：`type=Proposed Rule`、`action=Proposed rule.`、`publication_date=2026-08-21`、
  `comments_close_on=2026-10-20`、`effective_on=2026-08-21`、`citation=91 FR 54510`、
  `start_page=54510`、`end_page=54655`、`page_length=146`、`agencies` **只有一個**
  `SECURITIES AND EXCHANGE COMMISSION`。文章「機關欄只有 SEC 一個機關」成立
  （`must_not_write` 的「不可寫成 SEC 與 CFTC 聯名」沒踩到）。
- **金額與期間逐一對回條文**：四年 500 萬（Rule 200(b)(4) 與 SUMMARY 的 `up to $5 million during a
  four-year period`）；12 個月 7,500 萬（Rule 300(a)(2) 與 SUMMARY 的 `up to $75 million during each
  12-month period`）；Tier 1 的 2,000 萬與 600 萬、Tier 2 的 2,250 萬（條文以 `including not more than`
  寫成級距內的子上限，文章沒有寫成兩個獨立額度）；
  非合格投資人 **10%** 上限（Rule 300(c)(2)(i)(C)：`10 percent of the greater of that purchaser's:
  (1) Annual income or net worth **if a natural person**…; or (2) Revenue or net assets … **if a non-natural
  person**`——文章的「年收入或淨資產（法人為營收或淨資產）兩者較高者」對）；
  **48 小時**（實為 Rule 300(c)(2)(i)(B)，對象是「還沒有負 Sec. 228.305(a) 申報義務」的發行人，文章寫對了）；
  Rule 306 的 **30 個日曆日**。四年期間的起訖（Rule 200(b)(1)：自提交依賴通知後起算，
  至「提交後滿四年」與「提交過渡報告之日」兩者**較早**者）亦確認。
  這些全部是**發行人端的門檻**，文章沒有一處寫成投資額度或機會。
- **條號逐一確認**：Rule 101(d)、102、103、103(b)、104、200、300、304、305、306、307、400、500；
  Form NOR（239.605）、TR（239.604）、1-CRYPTO、1-KC（239.601）、1-SC（239.602）、1-UC；
  證券法第 5 條、第 2(a)(1) 條、第 18(b)(3) 條、第 20 條；交易法第 3(a)(10) 條；
  註 122 與 Public Law 119-27（139 Stat. 419，2025 年 7 月 18 日）；17 CFR 200.30-1(n)(1)。
  **Rule 104 的「任何豁免」是對的**：條文為 `No exemption under Regulation Crypto Assets is available`，
  而 228.104 在 Subpart A——這正是它與只及於 Subpart C 的 Rule 306 的差別。
  **Rule 101(d) 寫「豁免」不限於募資豁免也是對的**：它在 Subpart A，射程是
  `any exemption under this Regulation Crypto Assets`。
- **Rule 103(b)(2)(v) 與 (b)(6) 的分工正確**（`corrections-crypto.md` must_fix 5 已正確套用）：
  `publicly accessible, free of charge` 掛的是發行人自己編製並散布的白皮書與其他募集資料的網址；
  原始碼那一款只在 `to the extent the issuer has made it publicly available` 的範圍內要求列出網址，
  而且該款**沒有**出現 `free of charge`。
- **安全港的界線三句逐字對回釋義**，而且 `may` 都保留了：
  `the Commission would not be precluded from challenging whether an issuer did, in fact, satisfy those
  conditions`（文章：「委員會可以主張」）、
  `even if an issuer has not satisfied the investment contract safe harbor, a crypto asset **may** nonetheless
  not be subject to an investment contract under the Howey test`（文章：「仍可能」）、
  `it would not prevent other parties from asserting …`。
- **州法優先排除**：Rule 500 的 (a)(b) 兩支與 (b)(2) 的持續要件，以及釋義的
  `would preempt State securities law registration and qualification requirements for covered investment
  contracts that were initially sold by the issuer either pursuant to an exemption in Regulation Crypto Assets
  or another exemption under the Federal securities laws.` 與
  `Such secondary market preemption would continue for the period during which the issuer continues to
  satisfy …`。
- **意見提交方式與個資提醒**：ADDRESSES 欄的三種方式、`Please include File Number S7-2026-27 on the
  subject line.`、紙本寄 `Vanessa A. Countryman, Secretary`、
  `Do not include personal identifiable information in submissions`。
- **GovInfo PDF 端到端重讀**：146 頁，第 1 頁抽出文字首行
  `54510 Federal Register / Vol. 91, No. 161 / Friday, August 21, 2026 / Proposed Rules`。
  PDF 版案號用 en dash（`33–11434`）、`.txt` 用 ASCII 連字號（`33-11434`），
  文章沒有印會因版本而異的破折號形式，正確。
- **界線檢查（協調者第 7 點）全部通過**：
  - **沒有任何行情數字**——幣價、市值、交易量、資金流、報酬、殖利率、質押報酬、空投獎勵一個都沒有。
  - **由 CoinMarketCap 推導的市場數字一個都沒有進文章**：9,746 個掛牌加密資產、
    2024 年推出 3,165 個專案、由它推導的 475 家，以及 CoinLaw 的 ICO 統計，全部沒有出現。
    經濟分析裡屬於 SEC 申報件數的 130／99／31 與 636／581／14／41 也沒有寫（字數所限，留在研究紀錄）。
  - **沒有點名任何代幣或平台**。草案本身提到 Bitcoin 的兩處都是 2008 年的歷史背景
    （`Since the advent of Bitcoin in 2008`、註 5 的白皮書引註），文章沒有引用；
    Coinbase 的 25 處都在判決引註裡，文章也沒有引用。
  - **airdrops 那一題沒有任何會被讀成「可以領到什麼」的句子**。FAQ 5 只講 `covered transaction` 的定義
    與「要不要走豁免與揭露的程序」，並明寫不寫分配數量。
  - **「合法化」只出現在第 5 節那個標明是編輯設計的反例裡**，一次，而且句子的結論是
    「照這份文件能得到的結論只有『SEC 提出了一套募集與揭露的草案』」。
  - **每個操作性句子都帶「草案／提案／打算」**：逐句掃過 17 段、8 題 FAQ 與兩個 callout，
    沒有一句把提案寫成現行義務；「草案」「提案」「擬議」「打算」等字樣分布在每一節。
    第 2 段那句總括聲明（「下面每一個操作性句子講的都是『草案打算怎麼做』」）**沒有被當成替代品**。
  - **免責 callout 與 `crypto.md` 樣板逐字相同**（以程式比對 `title` 與 `text` 全等），
    含「不是投資建議」六個字，查核日 2026-09-17。文章另有一個本文提醒 callout，共兩個，符合幣圈規定。
- **`checked_on` 五處一致**：內容包 4 條 source、研究紀錄頂層、第 2 段、表格 caption、免責 callout
  都是 2026-09-17。**沒有因為本輪重查而改動它。**
- **摘要沒有多說**：四句的每一個數字都在正文或表格出現過；FAQ 八題答案都是純文字、沒有網址；
  全文沒有簡體字（`check_article.py` 的 `SIMPLIFIED` 檢查通過）。
- **`sources[]` 之外的事實沒有外溢**（改掉第 15 處之後）：`statements.rss` 的委員聲明、
  `2026-05635.json` 的 3 月釋令生效狀態、聯邦公報搜尋 API 的 count、regulations.gov 的意見件數，
  一句都沒有進文章。研究紀錄的 `unverified_or_excluded` 13 條理由本輪逐條複核，都站得住。

## 研究紀錄另改的 5 處

1. `event_date_basis` 與 `not_said[0]`：佔位字串的位置從「Sec. 228.104(a) 與 Sec. 228.300(b)(4) 兩處」
   改為 228.104(a)、228.104(b) 與 228.300(b)(4)，並寫下 3 次這個計數是查核者自己數的、
   以及逐行 grep 為何會少算（硬換行）。
2. Rule 306 那條事實：補上 `an exemption under this subpart` 與 Subpart C 的射程說明。
3. Rule 304 那條事實：刪掉「於其表面上載明」，改為條文 (b)(1)–(4) 實際要求載明的事項，
   並註明 `on its face` 全文 0 次、這個措辭來自 `corrections-crypto.md` must_add 3。
4. Tier 1 那條事實：註明「12 個月」出自釋義而非 Rule 300(a)(1) 條文，並把「關係企業」改為「關係人」
   （`affiliates` 包含自然人）。
5. 新增 `factcheck` 欄位（`method`／`verdict`／`edits_to_the_pack` 20 條／`checked_and_correct` 16 條／
   `left_for_the_owner` 5 條）。

## 留給站主的 4 件事

1. **「委員會核准這份提案是 2026 年 8 月 18 日」的「核准」是解讀，不是來源的字。**
   文件印的是 `By the Commission. Dated: August 18, 2026.`，全文沒有 `approve`／`approval`。
   本批次的 `corrections-crypto.md` 與任務指派都用「核准」，文章也把逐字引文放在同一句旁邊讓讀者自己看，
   所以本輪**沒有改**。若要更嚴格，可把三處（第 1 節第 1 段、callout 標題與內文）改為「作成」。
2. **Tier 2 財報的查核準則（U.S. GAAS 或 PCAOB）為控字數移出表格，正文也沒有寫。**
   事實已核實（`must be audited in accordance with either U.S. GAAS or PCAOB standards by an auditor that is
   independent under 17 CFR 210.2-01`）並留在研究紀錄。要加回約需 20 字，目前字數 2,988／3,000 只剩 12 字，
   得從別處刪等量純敘述——這是編輯取捨，查核代理不代決定。
3. **關係人出售上限（Tier 1 的 600 萬、Tier 2 的 2,250 萬美元）依協調者授權自表格移除，正文也沒有寫。**
   兩個數字都已核實，要加回只需一句，同樣受字數限制。
   另有三條已核實但未進正文：Rule 300(a)(3) 第一年次級出售不得超過募集總價 30%、
   Rule 300(c)(3)(ii) 不允許 `at the market offerings`、Rule 307(b) 九個月未取得核准得宣告放棄。
4. **`sources[3]` 是 25 筆的滾動視窗。** 今天 2026-76 還在（視窗為 2026-89 至 2026-65，它排第 14），
   但翻譯與上線若拖過數週要再抓一次。被擠掉時，新聞稿編號、標題與美東時間戳記那三句要刪、
   或改掛其他讀得到的官方管道；依協調者授權，`sources[]` 降到 3 條是允許的（下限 2）。

## 自檢

```
OK crypto-news-sec-regulation-crypto-assets-20260821 zh-TW paragraphs 2988
```

## 結論

`needs_second_round`。

四條來源今天全部重抓可讀、body 都是正文；撰稿者沒做完的 76 條引文驗證本輪補做，**76／76 全數命中、0 MISS**，
`verified_facts` 的引文欄位是本批次目前最乾淨的一份。協調者點名的八項全部查了：
Project Crypto 的日期**沒有錯**（本文自己寫的，不是註腳推出來的），
金額、期間與條號全部對到條文，界線檢查全部通過。

選 `needs_second_round` 的理由是 FACTCHECK.md 第 3 節的門檻：**改了 20 處，超過十處**，
而且其中第 1 處（Rule 306 只能停止募資豁免、不及於新創豁免與安全港）**動到第 4 節的骨幹論述**——
那一節整個就是在論「豁免不等於免責」，射程改了之後論述的邊界也跟著變。
第 4、5 處（Rule 101(d) 從無條件改為附三項舉證要件）同樣改寫了一段規範性敘述。
第二輪要看的是**本輪這 20 處改寫本身**，不是重做來源比對——來源那一層已經逐條做完並留下可重現的配方。

---

# 第二輪查核

查核代理：**未參與撰稿，也未參與第一輪查核**。查核日 2026-09-17（`checked_on` 本來就正確且一致，未動）。

依指派，**不重做來源比對**（第一輪已把 76 條 `verbatim_quote` 對今日全文逐條命中，配方可重現）。
本輪做四件事：覆核第一輪 20 處改寫、逐段檢查精簡過的敘述有沒有吃掉但書、新表格六個數字對回條文、
以及協調者點名的「核准」動詞與新聞稿 RSS 滾動視窗。

比對方式一律先把來源與待查字串都做 `re.sub(r"\s+", " ", …)` 再找子字串（.txt 是約 72 欄硬換行）。
**但本輪不只搜關鍵字**：把相關條文整節列印後逐句對讀——`Sec. 228.306` 全節、`Sec. 228.101(d)` 全條、
Subpart D 的 `Sec. 228.400` 與 Subpart E 的 `Sec. 228.500` 規則本文、`Sec. 228.103(a)` 與 `(b)` 全段、
`Sec. 228.304` 全條、第 49／50 題全文、PWG 報告三個 bullet 全文。
User-Agent 一律 `Mokaair-editorial`，未帶任何 email 或個人資料。

## 重抓結果（位元組數與第一輪完全相同）

| source | HTTP | bytes | body 是正文嗎 |
| --- | --- | --- | --- |
| 聯邦公報全文 `.txt` | 200 | 795,262 | 是，`text/plain`，公報全文，末行 `[FR Doc. 2026-17183 Filed 8-20-26 8:45 am]` |
| GovInfo 官方 PDF | 200 | 5,538,351 | 是，`application/pdf` |
| 聯邦公報 API JSON | 200 | 70,689 | 是，compact JSON，今日值見下 |
| ~~SEC 新聞稿 RSS~~ | 200 | 18,402 | 是，`application/rss+xml`，25 個 `<item>`——**但本輪已將它自 `sources[]` 刪除**，理由見下一節 |

API 今日值：`type=Proposed Rule`、`action=Proposed rule.`、`publication_date=2026-08-21`、
`comments_close_on=2026-10-20`、`effective_on=2026-08-21`、`citation=91 FR 54510`、
`start_page=54510`、`end_page=54655`、`page_length=146`、`agencies` 只有一個
`SECURITIES AND EXCHANGE COMMISSION`。`dates` 欄與文件 DATES 欄同一句。

## 第一輪 20 處改寫的方向全部站得住，沒有一處需要反轉

骨幹那兩處特別確認過：

- **Rule 306 只及於募資豁免，第一輪改對了。** `Sec. 228.306` 印在 `Subpart C--Fundraising Exemption`
  之下（同層另有 `Subpart B--Startup Exemption`、`Subpart D--Investment Contract Safe Harbor`、
  ``Subpart E--Definition of ``Qualified Purchaser.'' ``），條文寫的是
  `temporarily suspending an exemption under this subpart`，1 次命中。不及於新創豁免與安全港。
  其餘元素逐一命中：`if it has reason to believe that`、`(1)` 至 `(6)` 六款、`written request`、
  `30 calendar days`、`hearing`、`shall remain in effect unless or until it is modified or vacated by the
  Commission`。
- **Rule 101(d) 確實附三項舉證要件。** `(d)(1)` 的射程是
  `for any offer or sale to a particular individual or entity`，要件為 `(i)`／`(ii)`／`(iii)`；
  `(d)(2)` 的前提確實是 `Where an exemption is established only through reliance upon paragraph (1)`。
  （但套進正文時掉了三個限定詞，見下一節第 4 處。）
- **Rule 400 的兩項條件是條文自己印的 `(a)`／`(b)`**；三個界線的三句
  （`As with any safe harbor, however`／`Finally, even if`／`Moreover, while`）各 1 次命中，
  文件確實**沒有印「三個」**，第一輪刪掉計數是對的，而**敘述本身三句都在、完整**。
- **第 4 節第 1 段只寫「被視為不受該投資契約拘束」不算收窄。** 文件自己的 SUMMARY 欄就是這樣寫的
  （`would be deemed not to be subject to an investment contract`），完整賓語
  （`not to constitute or represent or to be subject to`）留在 FAQ 4，兩處各有來源。

## 本輪改掉的 9 件事（16 處）

**第一件：協調者第 4 點——「核准」不是來源的字（4 處）**

1. 全文以詞界比對只有三處 `approv*`，**全部無關**：職員聲明的
   `the Commission has neither approved nor disapproved its content`、Form ID 由 SEC 幕僚核可、
   以及法定標示 `does not pass upon the merits of or give its approval to any securities offered`。
   **沒有一處是「委員會核准這份提案」**；文件印的只有 `By the Commission. Dated: August 18, 2026.`。
   已把四處改為「作成」：小節標題「核准、送存、刊登是三個日期」→「**作成**、送存、刊登是三個日期」、
   第 1 節第 1 段「委員會核准這份提案是…」→「委員會**作成**這份提案的日期是…」、
   提醒 callout 標題「提案、核准、刊登、生效是四件不同的事」→「**作成、送存**、刊登、生效是四件不同的事」
   （順帶讓標題與內文實際列的四件事對齊）、callout 內文同步改。
   **title、description、摘要四句、表格、圖解 caption、hero_label 本來就沒有用這個意思**
   （title 與 description 用的是「提出」），已逐一確認。
   文章其他 7 處「核准」指的是 `qualification of the offering statement`（FAQ 3、FAQ 6）與
   `granting of applications`（第 3 節第 3 段），是另一個意思，**不動**。

**第二件：協調者第 7 點——RSS 降到 3 條（1 處，連帶刪 3 句）**

2. 今天重抓確認 2026-76 **還在**視窗內（25 個 `<item>`，視窗 2026-89 至 2026-65，它排第 14），
   但**再 11 則就會被擠出去**。以視窗自己的發稿速率推算：
   全視窗 24 則／70 天＝每日 0.343 則；2026-76 之後 13 則／29 天＝每日 0.448 則。
   11 則需要 **25 至 32 天，也就是 2026-10-12 至 2026-10-19 前後**——
   **落在本文自己在講的意見截止日 2026-10-20 之前或同時**。
   一個在文章的新聞窗口內就會失效的網址不值得占一個 `sources` 位子，**已整條刪除**。
   只靠它的三句一併刪掉：第 1 節第 3 段「SEC 官方新聞稿 RSS 上有一則編號 2026-76 的項目，
   標題是…，時間戳記為美東時間 2026 年 8 月 18 日」整句刪除；第 2 段讀過的文件清單刪掉
   「以及 SEC 官方新聞稿 RSS」。
   **不損失任何事實**：08-18 由文件署名區支撐，同時見於 `.txt` 與 GovInfo PDF 兩條 sources。
   第 1 節第 3 段改以 FR API 的 type 欄收尾（今天重抓為 `Proposed Rule`），段落數維持 3 段。
   副作用：**本文現在沒有任何一句依賴活資料。**

**第三到第七件：第一輪改寫後仍位移或收窄的限定詞（協調者第 1 點）**

3. **Rule 306 的 30 日起算點位移。** 原文「收到通知者得於 30 個日曆日內以書面請求聽證」讀起來像
   從收到通知起算；條文 `(b)(2)` 是
   `upon receipt of a written request within 30 calendar days **after the entry of the order**`。
   已改為「得於**命令作成後** 30 個日曆日內」，同句後段的「該命令於第 30 個日曆日成為永久」
   也因此有了起算點（條文為 `shall become permanent on the 30th calendar day after its entry`）。
4. **Rule 101(d) 掉了三個限定詞**——第一輪報告描述正確，但套進正文時沒套滿：
   - 主體「**發行人**若能證明」→「**主張豁免之人**若能證明」。條文是
     `if the person relying on the exemption establishes`，**不限於發行人**（出售證券持有人也可能是）。
   - 要件 (i)「該違反與**保護**該特定對象無關」→「該違反與**直接保護**該特定對象的**條件**無關」。
     條文是 `a term, condition, or requirement **directly** intended to protect that particular
     individual or entity`；漏掉 `directly` 與「條件」會換掉這個要件的意思。
   - 要件 (iii)「已善意合理地嘗試遵循」→「已善意合理地嘗試遵循**全部條件**」。條文是
     `comply with **all applicable** terms, conditions, and requirements`。
5. **安全港界線那一段的舉例掉了一個限定詞、又把一個清單收窄。** 條文是
   `if an issuer files a Form TR and misrepresents, **either intentionally or otherwise**, that it has
   satisfied the conditions in **Rule 400(a)**`，後果是
   `the reporting, registration, **and other requirements** of the Federal securities laws continue to apply`。
   原文漏了「不論故意與否」（中文的「不實陳述」偏向故意，漏掉會讓讀者以為過失不算）、
   把 Rule 400(a) 寫成籠統的「條件」、也把 `and other requirements` 寫成只有兩項。
   已改成「不實陳述已滿足**第一項**條件（**條文寫的是不論故意與否**）……申報與註冊**等**要求仍然適用」。
6. **FAQ 3 把 Rule 304(b) 的四款寫成封閉的三件事。** 條文是
   `The communications must: (1)…(2)…(3)…(4) After the public filing of the offering statement:`
   （(4) 另有 (i) 至 (iii)）。原文用「以及」把四款寫成三款的全清單，
   已改為「必須載明的事項**包括**：…」。同題另補回兩處條文文字：
   (1) 的對象是 `no money **or other consideration** is being solicited`（原文只寫「金錢」）、
   (2) 的第三個分句 `any such offer **may** be withdrawn or revoked … at any time before notice of its
   acceptance`（原文整句漏掉，已補「而且該要約在收到接受通知之前得隨時撤回」）。
7. **購買人條件被寫成「與」而條文是「或」。** Rule 300(c)(2)(i)(C) 是
   `Unless the purchaser is **either** an accredited investor … **or** the aggregate purchase price … is
   no more than 10 percent of the greater of…`——**兩者擇一，不是兩者都要**。
   第 5 節第 3 段與 FAQ 7 原本都寫「條件是合格投資人身分**與** 10% 上限」，「與」會被讀成兩個都要滿足。
   已各改為「條件是合格投資人身分，**不是的話**有 10% 上限」。FAQ 2 本來就寫對，不動。

**第八件：第一輪修正沒有套滿的一處**

8. **FAQ 1 還留著第一輪已在正文改掉的錯。** 正文第 1 節第 2 段已改成
   「在失格條款**與募資豁免的發行人資格條款**處」，但 FAQ 1 仍寫「在失格條款**那一處**」。
   佔位字串正規化空白後全文 **3 次**、跨 `Sec. 228.104(a)`、`228.104(b)` 與 `Sec. 228.300(b)(4)`
   兩個條文，「那一處」不成立。已同步改成與正文一致的寫法。

**第九件：協調者第 3 點——表格的出處分層**

9. 六個數字逐格覆核：500 萬＝Rule 200(b)(4) 的 `$5,000,000`（SUMMARY 另寫
   `up to $5 million during a four-year period`，所以「四年期間」有條文之外的第二個出處）；
   2,000 萬＝Rule 300(a)(1) 的 `$20,000,000`；7,500 萬＝Rule 300(a)(2) 的 `$75,000,000`
   （SUMMARY 另寫 `up to $75 million during each 12-month period`）。
   三格財報要求分別對回 `For Tier 1 offerings, there is no financial statement assurance requirement.`、
   `For Tier 2 offerings, the financial statements … must be audited in accordance with either U.S. GAAS or
   PCAOB standards by an auditor that is independent under 17 CFR 210.2-01`、
   以及 `an issuer would be required to provide financial statements under the fundraising exemption (but
   would not be required to do so under the startup exemption)`。
   **第一輪指出的問題確認成立**：Tier 1 的「12 個月」**不在** Rule 300(a)(1) 條文裡（條文只寫金額），
   出自釋義 `Under Tier 1 … up to $20 million … in a 12-month period`；Tier 2 的 12 個月則同時有釋義與
   SUMMARY。原 caption 寫「依提案規則原文整理」容易被讀成全部出自規則本文，
   已改為「依提案文件整理；**金額出自規則本文，「12 個月」這個期間出自文件的釋義**」。
   表格其餘部分（欄名、三列、儲存格長度、查核日與兩句界線）不動，儲存格仍是最長 10 字。

## 查過而且正確的部分（沒有動）

- **協調者第 2 點：第一輪為控字數精簡的約 140 字都是純敘述，沒有動到但書或限定詞。** 逐一核對被刪的五處：
  SEC 英文全名改括號縮寫（縮寫在正文與 description 都用得一致）、刪「三個日期不能混用」（小節標題已寫同一件事）、
  刪「也就是本文開頭那一天」（查核日在第 2 段已寫）、刪「委員個別聲明的內容與公眾意見件數不在本文範圍」
  （研究紀錄 `unverified_or_excluded` 有記，刪掉不產生任何新主張）、
  刪第 3 節第 3 段與段首重複的「既沒有要求公開原始碼」（同段開頭已承載同一個否定）。
  **五處都不是條文裡的條件。**
- **協調者第 2 點：17 段正文、8 題 FAQ、兩個 callout 逐句掃過「草案／提案／擬議／打算」的定位，
  沒有一句把提案寫成現行義務。** 三處值得記下來的判斷：第 2 節第 2 段「被管到的不是所有加密資產」
  沒有帶「草案」，但小節標題就是「草案管到誰：…」，且同段兩次寫「條文」指的是擬議條文；
  第 3 節第 2 段「Rule 103(b) 把必須揭露的資訊編成十類」同理；
  第 5 節第 2 段「要確認一份美國聯邦規則的狀態…」是給讀者的一般方法，不是提案的操作性內容。
- **第一輪其餘 11 處改寫逐一回條文覆核，全部正確**：SUMMARY 欄三個限定詞；
  PWG 報告的 `including` 清單（三個 bullet 分別是 `fit-for-purpose exemption from registration under
  section 5`、`time-limited safe harbor or exemption`、`safe harbor for certain airdrops`，
  文章的「包括」「有期限」「針對特定空投」「註冊」都對）；
  Rule 103(a) 分兩類（`established public communication channels (such as its website or official social
  media accounts)` 與 `promotional materials (such as whitepapers)`）並限於
  `relating to material aspects of…`；FAQ 8 的遮蔽但書；安全港效果的完整賓語與「受投資契約拘束或屬於證券」；
  covered investment contract 的「契約、交易或安排」；Rule 500 是「新增」定義；
  FAQ 3 刪掉「表面上」（`on its face` 與 `face of the communication` 正規化後皆 **0 次**）；
  FAQ 7 第 49／50 題的歸屬（第 49 題含「限於實體」與「在美國設立或登記」兩問，
  第 50 題才是比照募資豁免的美國連結三要件——已讀兩題全文確認）；
  三處概括否定改成正面陳述；callout 的延長意見期那句改掛 FR API。
  - **附帶記一筆**：Rule 103(a) 的一致性要求，**前言那一段寫的是 `would be required to be consistent`，
    規則本文寫的是 `should be consistent`**。文章掛的是 Rule 103，用「應」對應規則本文，是較保守的選擇。
- **條文自己印的計數全部確認無誤**：covered investment contract 的三項要件印 `(1)(2)(3)`；
  Rule 103(b) 的頂層編號逐一列印確認是 `(1)` 至 `(10)`，**剛好十類**；
  Rule 306(a) 印 `(1)` 至 `(6)`；Rule 400 印 `(a)(b)`。
  - **更正第一輪報告的一句自述**：它說「前兩處另在正文加註『條文編號的』」，
    實際上**只有**第 2 節第 2 段的三項要件加了，第 3 節第 2 段仍是「編成十類」。
    這**不必改**——「編成」已經把分類歸給條文本身，計數也確實是條文印的。
- **「這份草案沒有提到台灣」保留。** 這不是 BRIEF 型態 2 禁止的那種概括否定：
  它是對一份**已刊登定本**做全文窮盡比對的結果（`Taiwan` 與 `Taipei` 以詞界比對皆 **0 次**），
  不是從「這一頁沒寫」推到「官方沒有」。同理 `nationality` 與 `domicile` 皆 0 次，
  但 FAQ 7 那句仍收在 `Rule 300(c)(2)` 這一款的範圍內寫，不對整份文件下否定。
- **協調者第 5 點：摘要四句、FAQ 八題、兩個 callout、description、title、圖解 caption、
  研究紀錄 `diagram` 四格與 `hero_label` 全部重讀。** 摘要與圖上的數字逐一確認出現在正文或表格：
  2026-08-21、500 萬、7,500 萬、四年、12 個月、第 5 條、1933、2026-10-20 都在；
  圖上的 500 萬與 7,500 萬在第 2 節第 3 段與表格，「十類」在第 3 節第 2 段。
  title 與研究紀錄 `title` 相同、圖解 caption 與 `diagram.caption` 相同。
  description 172 字（120–200）、title 52 字（≤60）。
- **協調者第 6 點：界線全部通過。** 沒有任何幣價、市值、交易量、資金流、報酬、殖利率、質押報酬或空投獎勵數字；
  **沒有由 CoinMarketCap 推導的專案數或家數**（9,746、3,165、475 一個都沒有），
  也沒有 SEC 申報件數（130／99／31、636／581／14／41 留在研究紀錄）；
  **沒有點名任何代幣或平台**。
  **FAQ 5（空投）沒有任何會被讀成「可以領到什麼」的句子**——只講 `covered transaction` 定義的範圍與
  「要不要走豁免與揭露的程序」，並明寫「處理的不是分配的數量；本文也不寫任何可以拿到多少的內容」；
  段落裡出現的「獎勵」是條文自己的分類用語（`as a reward or incentive for conducting activities primarily
  related to operating, governing, or securing…`），不帶任何數量或條件。
  「合法化」仍只出現在第 5 節那個標明是編輯設計的反例裡，一次。
- **免責 callout 與 `crypto.md` 樣板逐字相同**（以程式比對 `title` 與 `text` 全等），
  含「不是投資建議」六個字，查核日 2026-09-17。共兩個 callout，符合幣圈規定。
- **`checked_on` 未動**，刪掉第 4 條 source 之後仍五處一致（內容包 3 條 source、研究紀錄頂層、第 2 段、
  表格 caption、免責 callout）。**`hero.alt` 未查未改。**

## 留給站主的 4 件事

1. **`hero.alt` 還寫著「一條由核准、送存、刊登三個節點連起來的橫線」。** 依指派本輪不動 alt，
   但主圖重繪時那三個節點的用語要跟正文一起改成「**作成**、送存、刊登」——
   這是全篇唯一還留著「核准」舊用語的地方。
2. **第一輪留下的三件編輯取捨本輪沒有代決定**，都仍成立：Tier 2 財報的查核準則（U.S. GAAS 或 PCAOB）
   不在表格也不在正文；關係人出售上限（Tier 1 的 600 萬、Tier 2 的 2,250 萬美元）同樣不在；
   Rule 300(a)(3)、Rule 300(c)(3)(ii)、Rule 307(b) 三條已核實但不在正文。
   **字數現在是 2,941，離 3,000 還有 59 字**（第一輪當時只剩 12 字），要加回其中一項有空間了。
3. **`sources` 現為 3 條（下限 2），三條都是固定文件**，翻譯與上線前不需要再回頭確認任何 feed。
   若想恢復一條 SEC 自家管道，新聞稿的固定網址是
   `https://www.sec.gov/newsroom/press-releases/2026-76-sec-proposes-new-regulation-crypto-assets`
   （RSS 的 `<link>` 指向它），但 **`sec.gov` 的網頁對 `curl` 回 403，本批次兩輪都沒有讀到它的正文**，
   依 FACTCHECK.md 不可列進 `sources`；要列必須有人真的讀到 body。
4. **「作成」這個譯法是本輪依來源選的。** 批次的 `corrections-crypto.md` 與任務指派仍寫「核准」，
   同批其他篇用的是「作成／署名／通過」。這一篇已經統一為「作成」；要改成「署名」也同樣有來源支撐。

## 自檢

```
OK crypto-news-sec-regulation-crypto-assets-20260821 zh-TW paragraphs 2941
```

## 結論

`needs_owner`。

**第一輪 20 處改寫的方向全部站得住，沒有一處需要反轉**，兩處骨幹（Rule 306 的 subpart 射程、
Rule 101(d) 的三項舉證要件）逐句對回條文後確認正確。本輪改的 9 件事（16 處）**沒有一件動到論述骨幹**：
七件是限定詞的補回或位移修正、一件是第一輪沒套滿的同一個錯（FAQ 1 的「那一處」）、
一件是表格 caption 的出處分層。其中 Rule 101(d) 的三個限定詞與 FAQ 1 那一處，
是**第一輪報告已經寫對、但套進內容包時沒套滿**的——值得回饋給批次：
改寫清單與實際套用要逐條對讀一次。

**不需要第三輪。** 唯一還沒閉合的是 `hero.alt`（協調者重繪主圖時處理），
以及三件字數／來源下限的編輯取捨——那些依規定不由查核代理決定。
