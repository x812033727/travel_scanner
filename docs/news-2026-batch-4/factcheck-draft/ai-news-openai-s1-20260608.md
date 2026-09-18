# 獨立查核：ai-news-openai-s1-20260608（OpenAI 保密送件 S-1）

查核日 2026-09-18。查核代理沒有參與撰稿。核對 108 條主張（正文 17 段、summary 4 句、
FAQ 7 題、表格 4 列與 caption、圖解 caption 與研究紀錄 `diagram` 四格、`hero_label`、
`title`、`description`），改了 19 處，結論 `needs_owner`。

所有網路請求一律 `curl -sL -A "Mokaair-editorial"`，沒有任何請求（UA、標頭、查詢字串、表單）
帶入任何人的 email、姓名或個人資料。

## 一、`sources[]` 今天重抓的結果

| # | 網址 | HTTP | bytes | body 是不是正文 |
|---|---|---|---|---|
| 1 | `openai.com/index/openai-submits-confidential-s-1/` | 200 | 346,593 | 是。最終網址即帶斜線的原網址，`x-nextjs-prerender: 1`、`x-powered-by: Next.js`，回應標頭沒有 `cf-mitigated` 或任何挑戰標頭；`<title>` 為 `Confidential submission of draft S-1 to the SEC \| OpenAI`，正文兩小段可讀 |
| 2 | `efts.sec.gov/LATEST/search-index?q=&entityName=OpenAI` | 200 | 32,682 | 是。`hits.total.value = 46`，`hits.hits` 一次回傳全部 46 筆、未分頁 |
| 3 | `govinfo.gov/.../USCODE-2023-title15-...-sec77f.htm` | 200 | 24,007 | 是。§77f 全文，`(e) Emerging growth companies` 兩項俱在 |
| 4 | `federalregister.gov/documents/full_text/text/2026/05/21/2026-10222.txt` | 200 | 657,682 | 是。91 FR 30086 全文，頁首與委員會署名區塊俱在 |

**撰稿者「今天讀得到 OpenAI 公告全文」的說法成立**——第 1 條前期為 403（Cloudflare 挑戰頁），
本代理今天獨立重抓確認是公告正文，不是拒絕頁或軟性 404。

**引文比對**：22 條 `verified_facts`（原 19 條，本代理新增 3 條）的 `verbatim_quote`
全部以程式做連續字串比對，**22/22 在今天抓下來的來源檔裡原樣命中**，且 22 條的 `url`
**全部落在 `sources[]` 之內**——這在本垂直極少見（`corrections-ai.md` 跨篇通則第 4 條
說 12 篇裡有 10 篇做不到）。含 U+2019 撇號的那一段（`we’re`、`it’s`）逐字元核對通過。

**EDGAR 三個數字全部獨立重數，不讀聚合**：`file_type` 分組得 40 筆 `D` ＋ 6 筆 `D/A`；
逐筆展開 `display_names` 得 41 個不同申報人（2024-03-22 一筆掛
`MAV OpenAI Fund I` 與 `QP-MAV OpenAI Fund I` 兩個共同申報人）；
`form_filter` 單一 bucket `D:46`、`sum_other_doc_count = 0`；
`entity_filter` 30 個 bucket ＋ `sum_other_doc_count = 11` = 41。
**與撰稿者的清點完全一致**，`corrections-ai.md` must_fix 1 與 must_fix 3 確認沒有留在正文。

## 二、改掉的 19 處

### 1. 四條來源沒有一條定義 Form D，草稿卻寫了 Form D 的用途

- 原文：「Form D 是私募發行的通知文件，用途是創投基金或特殊目的公司通報自己完成了一輪私募，
  不是公司申請公開發行要用的表格」
- 來源怎麼寫：**沒有寫**。程式核對四條來源全文，`Form D`／`Regulation D`／
  `private placement`／`exempt offering` 在 91 FR 30086 與 USCODE §77f 都是 **0 次**；
  EDGAR 回應只回欄位值，不回定義。
- 改成：整句刪掉。該段改為只描述查詢實際回傳的東西。

### 2. 「這 41 個申報人清一色是投資 OpenAI 的創投基金與特殊目的公司」

- 來源怎麼寫：**沒有寫**。EDGAR 回應每筆 `_source` 只有
  `ciks`／`display_names`／`form`／`file_type`／`root_forms`／`file_date`／
  `biz_states`／`inc_states`／`items`；`invest` 與 `venture` 兩個字串在整份回應是 **0 次**。
  「投資 OpenAI」是從名稱推出來的，而名單裡的 `OpenAI Startup Fund` 系列依其名稱是
  **對外投資**的基金，把它說成「投資 OpenAI」風險更高。
- 改成：「這 41 個申報人的名稱看得出來是各種基金與特殊目的公司……要注意的是，
  這次查詢回傳的欄位只有申報人名稱、表單別、申報日與登記州別，沒有說明這些基金實際投資什麼，
  本文也不替它們推斷。」

### 3.（最重要）保密的法定保護只及於新興成長公司，草稿寫成適用所有人

- 原文：「保密遞件並不是新興成長公司獨有的做法。……幕僚自 2017 年起就已經接受所有發行人
  遞交草稿做非公開審查」，**下一段緊接**「法條同時規定，SEC 不得被強制揭露透過保密遞件
  收到的資訊；就資訊自由法而言，這屬於法定豁免。」
- 來源怎麼寫：91 FR 30086 在同一段接著寫
  `the Commission lacks the authority to extend this confidentiality to non-EGC companies and therefore only statutory EGCs will remain eligible for this accommodation.`
  而且 §77f(e)(2) 的豁免只及於「依**本項**取得的資訊」，本項標題就是
  `(e) Emerging growth companies`。
- 為什麼要改：兩段接在一起，讀者會以為「對所有發行人開放的非公開審查」也帶著法定保密，
  那正好是來源明文否定的一件事。
- 改成：「兩條路徑的保密程度並不一樣。第 6(e)(2) 條規定 SEC 不得被強制揭露依該項取得的資訊……
  但同一份提案規則接著寫明，委員會沒有權限把這層保密延伸到非新興成長公司，
  因此只有法定的新興成長公司仍然適用這項優惠。」

### 4.「SEC 對是否遞交過保密文件一貫不確認也不否認」——四處，全部無來源

- 來源怎麼寫：**沒有寫**。`neither confirm`／`confirm nor deny` 在 OpenAI 公告頁、
  USCODE §77f、91 FR 30086 **三份都是 0 次**。§77f(e)(2) 只寫「不得被**強制**揭露」，
  那是 FOIA 上的豁免，推不出 SEC 對外詢問的應答慣例。
- 出現在：正文一處、FAQ 第 3 題、FAQ 第 4 題、`callout` 一處。
- 改成：正文改為「本文查核的四條來源，都沒有說 SEC 會不會回應外界詢問某家公司是否遞交過草稿」；
  另外三處刪除。同段的「保密遞件不會出現在**任何**公開資料庫」一併刪掉（全稱、無來源）。

### 5.「公告沒有出現任何數字」——字面就不成立

- 公告正文本身有 `S-1`、`Rule 135`、`1933`，頁面上還有 `June 8, 2026`。
- 改成：「公告沒有寫任何和發行規模有關的數字」。

### 6.「S-1 是……**最常用**的註冊說明書表格」（正文＋FAQ 3）

- 來源怎麼寫：`most commonly` 在 91 FR 30086 為 **0 次**，四條來源都沒有任何使用頻率的比較。
- 改成：「註冊說明書表格之一」，並改掛文件裡實際印出的
  `registration statement on Form S-1 (Sec.  239.11 of this chapter)`。

### 7. 公告四句話的轉述掉了三個限定詞、多了一個（正文＋FAQ 2）

- 原文 `things we want to do that are **likely** easier as a private company`
  → 草稿「因為有些事以私人公司身分做起來比較容易」（掉了 `likely`，也掉了「想做的」）。
- 原文 `if that ends up being **best**` → 草稿「如果情況合適」（弱化）。
- 原文 `We expect it to leak` → 草稿「預期這件事**遲早**會外流」（原文沒有時間副詞）。
- 改成：「因為公司有些想做的事，以私人公司的身分做起來**多半**比較容易」「**萬一那樣做最好**、
  可以提早公開發行的選擇權」「預期這件事會外流」。

### 8. FAQ 5 把 15 天路演規定當成對 OpenAI 的把關

- 原文：「法條本身有把關：初次保密遞件與之後所有修正本，最晚要在公司進行路演前 15 天
  全部改為公開申報……目前**沒有證據顯示** OpenAI 的草稿已經到了必須公開申報的階段。」
- 違反研究紀錄 `must_not_write`：「不得斷定 OpenAI 是不是新興成長公司，
  **也不得把 15 天路演規定的適用對象替它下結論**」。該條規定在 §6(e)(1)，
  對象是新興成長公司，而文章別處明講不替 OpenAI 歸類——前後自相矛盾。
  後半句的「沒有證據顯示」也是無界限的否定。
- 改成：先寫明第 6(e)(1) 條的對象是新興成長公司，再說「本文也不替它歸類，
  因此不判斷這條 15 天規定對它適不適用」。

### 9. FAQ 4 兩句無來源的全稱否定

- 「過程中沒有『核准』或『受理』這種對外程序」「依法只有走到公開申報之後，
  資料才會出現在 EDGAR 上」——四條來源沒有一條這樣寫
  （`approv` 在 91 FR 30086 出現 29 次、`EDGAR` 出現 8 次，都是別的脈絡）。
- 改成限縮句：「條文把保密遞件寫成『在公開申報之前由 SEC 幕僚做保密的非公開審查』，
  本文查核的四條來源都沒有提到這個階段有對外的核准或受理程序。」

### 10.「這句話本身就是 OpenAI 目前**唯一**公開表態的立場」

- `BRIEF.md` 明文禁止「唯一」。撐這句的只有對 OpenAI 官方 RSS 的關鍵字掃描，
  而 RSS 不在 `sources[]`，依規則不能當文章的依據。
- 改成：「本文查核的四條來源裡沒有其他說法。」同段「保密遞件之後可能發生的事包括……
  官方沒有排除任何一種」也改成「公告沒有寫接下來會怎麼走」的限縮句。

### 11. `description` 與圖解第三格把「沒有註冊說明書」寫成「沒有公開申報」

- EDGAR 上**確實有** 46 筆以 OpenAI 為名的公開申報（Form D）；缺的是註冊說明書。
- `description` 改為「查不到以 OpenAI 為申報人名稱的公開註冊說明書」；
  研究紀錄 `diagram` 第三格由「全文檢索查無公開申報」改為「全文檢索查無註冊說明書」。

### 12. 表格四列補上適用範圍

- 6(e)(1) 列加「新興成長公司」；6(e)(2) 列加「提案規則指僅新興成長公司適用」；
  2017 年幕僚實務列加「該文件未提議入法」（來源：`We are not proposing to codify this process`）；
  門檻列補「**已完成**」會計年度。

### 13. summary 兩句

- 第 2 句補上適用對象與「沒有提議入法」；第 3 句「全部是投資機構的 Form D 或其修正」
  改為「表單別全部是 Form D 或 Form D/A」；第 4 句「官方沒有公布」改為「公告沒有寫出」，
  與正文一致。

### 14. 研究紀錄

- EGC 門檻那一條原本掛的引文是 `$1.235 billion **or more**`，那是「**喪失** EGC 資格」的條件，
  不是取得資格的門檻，與 fact 敘述不符。改引同一段的
  `Currently, a company qualifies as an EGC if it has total gross revenues of less than $1.235 billion during its most recently completed fiscal year`。
- 新增三條 `verified_facts`（EGC-only 保密、未提議入法、Form S-1 條次）與七條
  `unverified_or_excluded`，並補上 `factcheck` 欄位。
- `live_data_warnings` 與 `corrections_applied` 裡仍留著 OpenAI RSS 的確切筆數（1,207），
  `corrections-ai.md` must_fix 4 要求紀錄本身也要改寫成區間——已改為「逾 1,100 筆」。

## 三、查過而且正確的部分

- **公告頁的四個頁面事實**：可見日期 `June 8, 2026`、分類連結文字 `Company`
  （`href="/news/company-announcements/"`）、`data-testid="author-list"` 區塊的具名作者 `OpenAI`、
  `meta description` 一句，全部逐字核對無誤。公告正文第一段確為四句話（圖解「四句聲明」成立）。
- **JOBS Act／FAST Act 的命名確實掛得住 91 FR 30086**（must_fix 6 的改法正確）：
  註腳 7 與註腳 93 印出 `Jumpstart Our Business Startups Act, Public Law 112-106, 126 Stat. 306 (2012)`；
  正文印出 `Fixing America's Surface Transportation (``FAST'') Act`，緊接的註腳 95 印出
  `Public Law 114-94, 129 Stat. 1312 (2015)`。§77f 頁今天仍然 `JOBS`／`FAST`／`Jumpstart`／
  `Fixing America` **各 0 次**，那兩個簡稱不能掛回 §77f 頁這件事今天依然成立。
- **21 天改 15 天**：`Subsec. (e)(1). Pub. L. 114-94 substituted "15 days" for "21 days"`
  與 `Subsec. (e). Pub. L. 112-106 added subsec. (e).` 逐字命中。
- **91 FR 30086 的日期分離正確**：頁首 `[Federal Register Volume 91, Number 98 (Thursday, May 21, 2026)]`、
  `[Pages 30086-30190]`、`[FR Doc No: 2026-10222]`（文件自己印出的編號）；
  文末 `By the Commission. Dated: May 19, 2026.`。文章把刊登日與通過日分開寫，符合 must_add。
- **Rule 135 那一段**：引文逐字（含 U+2019）比對通過，中文轉述沒有超出原文，
  且照研究紀錄的決定不代為解讀 Rule 135——四條來源確實都沒有定義 Rule 135。
- **`checked_on` 四處一致**（內容包每條 source、研究紀錄、正文第二段、表格 caption 都是
  2026-09-18），而且今天確實在這一天讀到四條來源，**未更動**。
- **活資料處理正確**：46 筆與 41 個申報人在正文、FAQ 7 與追蹤段三處都綁了查核日並說明是快照；
  沒有任何 feed 筆數、sitemap `<url>` 數進入內容包。
- **`must_not_write` 逐條合規**：`§77f(e)(1)` 句尾那句排版異常的
  `emerging market growth company` 但書今天仍在來源頁上，文章照規定沒有引用。
- **界線檢查（本篇不可寫成投資題材）**：全篇沒有估值、募資金額、發行股數、承銷商、交易所、
  股票代號、上市時程預測，也沒有「值得期待」式語氣；沒有購買建議、沒有推薦式比價；
  公告內容一律歸因（「公告」「OpenAI 的原句」），沒有未歸因的廠商宣稱；
  沒有把預告或草案寫成已完成——通篇就是在說「送件 ≠ 公開申報 ≠ 核准 ≠ 一定會上市」。
  `topics` 為 `["ai","ai-news"]` 不含 `finance`；只有一個 `callout`，
  沒有投資免責 callout，而該 callout 明講本文不是投資建議。

## 四、留給站主的事

1. **四條 `sources[]` 已達上限，所以文章現在完全不解釋 Form D 是什麼**，讀者只知道
   「表單別是 D，不是 S-1」。要寫出 Form D 的用途就得換掉一條來源（例如 17 CFR 239.500
   的官方條文，或 `data.sec.gov` 上某一筆 Form D 本身）。這是編輯裁量，本輪沒有動 `sources[]`。
2. **第二個結尾連結的標題含有「1,220 億美元募資」這個金額。** 依規格結尾兩個連結由協調者處理，
   本代理沒有動；若站主認為本篇不該在任何位置出現募資金額，需要協調者換一篇相關文章。
3. **`www.sec.gov` 今天未實測**（研究紀錄記錄前一輪為 403）。文章因此只描述「以申報人名稱查詢」
   的概念、不給讀者可點的網址。若日後可讀，可以補一個讀者能直接點的查詢頁。

## 五、自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
```

僅剩規格允許保留的那一條（索引標題由協調者事後原地更新）。
段落總字數 2,563（1,800–3,000），`description` 189 字（120–200），
每節 2–4 段，兩個結尾連結未動。

## 六、結論

`needs_owner`——**改了 19 處，其中第 1、2、3、4 項動到骨幹論述**
（Form D 的說明、41 個申報人的性質、保密保護的適用範圍），
不是潤飾。骨幹改動後的每一句都已回到四條來源逐句重查，
新寫進去的句子沒有一句掛在 `sources[]` 以外的網址。
剩下的是站主裁量：要不要為了解釋 Form D 換一條來源（第四節第 1 點）。

## 第二輪

查核日 2026-09-18。第二輪代理沒有參與撰稿，也沒有參與第一輪。範圍是第一輪改動過的
每一段與**新寫進去的每一句**，逐句回四條來源原文；共覆核 71 條主張，**又改了 9 處**
（內容包 6 處、研究紀錄 3 處），結論 `ok`。

所有網路請求一律 `curl -sL -A "Mokaair-editorial"`，沒有任何請求（UA、標頭、查詢字串、
表單）帶入任何人的 email、姓名或個人資料。

### 一、四條來源今天獨立重抓

| # | 網址 | HTTP | bytes | body 是不是正文 |
|---|---|---|---|---|
| 1 | `openai.com/index/openai-submits-confidential-s-1/` | 200 | 346,590 | 是。`x-nextjs-prerender: 1`、`x-powered-by: Next.js`，回應標頭沒有 `cf-mitigated` 或任何挑戰標頭；兩小段正文可讀 |
| 2 | `efts.sec.gov/LATEST/search-index?q=&entityName=OpenAI` | 200 | 32,681 | 是。46 筆 `hits.hits` 一次回傳、未分頁 |
| 3 | `govinfo.gov/.../sec77f.htm` | 200 | 24,007 | 是。§77f 全文，`(e) Emerging growth companies` 兩項俱在 |
| 4 | `federalregister.gov/.../2026-10222.txt` | 200 | 657,682 | 是。91 FR 30086 全文 |

**引文比對**：`verified_facts` 24 條（第一輪 22 條，本輪新增 3 條、改寫 1 條的引文）
全部以程式做**連續字串**比對，**24/24 原樣命中**，`url` 全部落在 `sources[]` 之內。
含 U+2019 的兩條逐字元核對通過；唯一含 `|` 的那一條（`<title>… | OpenAI</title>`）
確認 `|` 是頁面標題本身的分隔符，不是把不同段落拼接起來的痕跡。

**EDGAR 自己重抓重數**（不讀第一輪的結論）：`hits.total.value=46`、`hits.hits` 46 筆、
展開 `display_names` 得 41 個不同申報人（2024-03-22 一筆掛 `MAV OpenAI Fund I` 與
`QP-MAV OpenAI Fund I` 兩個共同申報人）、`file_type` 分組得 40 筆 `D` ＋ 6 筆 `D/A`、
`form_filter` 單一 bucket `D:46` 且 `sum_other_doc_count=0`、`entity_filter` 30 bucket
＋ 11 = 41。**四個數字與第一輪完全一致**。

### 二、又改的 9 處

#### 1.（最重）第一輪重寫保密段時，漏掉了同一段的但書

- 第一輪停在「委員會沒有權限把這層保密延伸到非新興成長公司，因此只有法定的新興成長公司
  仍然適用這項優惠」。
- 來源怎麼寫：91 FR 30086 **在同一段緊接著**寫
  `Non-EGC registrants would continue to be able to use the Commission's confidential treatment procedures regarding FOIA requests pursuant to 17 CFR 200.83 (``Rule 83''), when submitting draft registration statements for nonpublic review.`
- 為什麼要改：只寫前半句，讀者會得到「非新興成長公司的草稿完全沒有保密可言」的印象，
  而來源明講還有 Rule 83 這條途徑（只是委員會的裁量程序，不是法定豁免）。
  第一輪為了修正「把非公開審查與法定保密混為一談」而重寫，卻在另一個方向上過頭了。
- 改成：補一句「同一段也接著說明，非新興成長公司遞交草稿做非公開審查時，仍然可以使用
  委員會既有的保密處理程序來因應資訊自由法的請求。」並新增對應的 `verified_facts`。

#### 2.「這次查詢回傳的欄位**只有**……」——「只有」不成立

- 第一輪新寫的句子：「這次查詢回傳的欄位只有申報人名稱、表單別、申報日與登記州別」。
- 來源怎麼寫：逐筆檢查 46 筆 `_source`，欄位另有 `biz_locations`／`biz_states`（營業地）、
  `adsh`、`file_num`、`film_num`、`items`、`sics`、`period_ending`、`file_description`。
  這是一個被來源直接否證的全稱句。
- 改成：「這次查詢回傳的是申報人名稱、表單別、申報日、登記州別與營業地這類申報欄位，
  **沒有一個欄位**說明這些基金實際投資什麼」——保留第一輪要表達的重點，但把否定句
  限縮成逐欄位可驗證的形式。

#### 3. Form D 整句刪掉之後，文章對讀者沒有交代

- 第一輪把「Form D 是私募發行的通知文件……」整句刪掉是對的：本輪重新確認
  `Form D`／`Regulation D`／`private placement`／`exempt offering` 在**四條來源全部 0 次**。
- 但刪完之後，文章從頭到尾出現 10 次 Form D 卻不解釋，讀者會卡住。
- 改成：在 EDGAR 那一段補一句誠實寫法——「本文引用的四條來源都沒有解釋 Form D 這份表單的
  用途，所以這裡只照查詢回傳的表單別寫，不代為說明它是做什麼用的。」**沒有自己補定義。**

#### 4.「委員會沒有提議把這套做法入法」漏掉同一句的轉折

- 來源全句是 `We are not proposing to codify this process **but we request comment on whether doing so would provide additional clarity and certainty.**`
- 只寫前半句，會把一件仍在徵詢意見的事寫得像已經定案。
- 改成：「……沒有提議把這套做法入法，只就是否入法徵詢外界意見。」引文同步補完整。

#### 5. FAQ 第 7 題：DRS 的說法不精確，且活資料沒帶日期

- 原文「而 S-1、DRS 這類才是註冊說明書」——DRS 依 91 FR 30086 自己的定義
  （`a draft registration statement (``DRS'')`）是註冊說明書**草稿**，不是註冊說明書。
- 「查核日看到的 46 筆」只說「查核日」而沒有印出日期。
- 改成：「2026 年 9 月 18 日查核時看到的 46 筆全部是 Form D 或 Form D/A，而註冊說明書要看的是
  S-1 這種表格，或是提案規則裡簡稱 DRS 的註冊說明書草稿。」並新增 DRS 定義的 `verified_facts`
  （第一輪用了這個說法卻沒有對應的 fact）。

#### 6. `description` 語句不通且沒有時點

- 原文「並以全文檢索系統**查核到查不到**以 OpenAI 為申報人名稱的公開註冊說明書」。
- 改成「並以全文檢索系統確認，**截至查核當天**查不到……」（195 字，仍在 120–200）。

#### 7–9. 研究紀錄三處

- **`not_said` 裡仍留著第一輪已經從文章刪掉的說法**：「SEC 依制度設計不確認也不否認一件
  保密遞件的存在」與「SEC 沒有公開任何與這次遞件有關的文件」。第一輪把這句從正文、FAQ 3、
  FAQ 4、callout 四處刪除，卻沒有回頭改這份紀錄——等於把無來源的說法留在原地給後續批次抄。
  已改寫成限縮在查詢範圍內的敘述並註明原因。
- **第一輪的舉證有一條是錯的**：`unverified_or_excluded` 寫「`invest` 與 `venture` 兩個字串
  在整份回應是 0 次」。重抓實測 **`invest` 8 次、`venture` 5 次**，全部落在申報人名稱裡
  （`MAV Alternate Investments`、`DiversiFi Ventures`、`Venelite Venture Funds`、
  `InvestX Capital`、`OurCrowd (Investment in G-new OpenAI)`、`GatePass Ventures`）。
  **結論不變**（回應確實沒有任何欄位說明這些基金投資什麼），但舉證方式改為列舉 `_source`
  欄位本身，不再用關鍵字計數。
- 新增三條 `verified_facts`（Rule 83、完整的「未提議入法」句、DRS 定義），並加上
  `factcheck.second_round`。

### 三、指派訊息點名的七個疑點

1. **保密遞件段逐句回原文**：文章沒有替 OpenAI 歸類是不是 EGC（正文、FAQ 3、FAQ 5
   三處都明講不歸類），沒有把條文寫成對 OpenAI 的適用結論，也沒有把「非公開審閱」與
   「法定保密」混為一談——「兩條路徑的保密程度並不一樣」這句正是來源的分野。
   §77f(e)(2) 的豁免文字確為 `pursuant to this subsection`，而該 subsection 標題就是
   `(e) Emerging growth companies`；FOIA 的連結由 91 FR 30086 註腳 224 明確指向
   `15 U.S.C. 77f(e)(2)`，不是文章自己接上去的。**唯一的缺口是第二節第 1 點的但書，已補。**
2. **Form D 自洽**：五處提及全部只寫表單代號 D／D/A、筆數與日期，沒有任何一處替讀者
   補定義；已加上「本文引用的來源沒有解釋這份表單」的誠實寫法（第二節第 3 點）。
3. **EDGAR 數字一致且都帶查核日**：46／41／40＋6 在正文、summary、表格、FAQ、圖解 nodes
   每一處一致；正文四處、summary 一處、FAQ 三處都印出 2026 年 9 月 18 日（全篇共 12 次），
   圖解 nodes 由 caption 帶日期。RSS 筆數只在 `live_data_warnings` 以「逾 1,100 筆」的
   **區間**記錄，沒有進入內容包。
4. **「不確認也不否認」刪除後沒有斷句**：正文改成限縮在四條來源的敘述，FAQ 3、FAQ 4、
   callout 三處都是完整且有界限的句子，沒有失去歸因的推論。**但研究紀錄漏改**，見第二節第 7 點。
5. **FAQ 5 沒有暗示上市時程**：先寫明第 6(e)(1) 條的適用對象是新興成長公司，再明講不替
   OpenAI 歸類、不判斷 15 天規定對它適不適用；「一旦走到那一步，草稿就會變成公開文件」
   是條文的條件句，不是對 OpenAI 的預測。
6. **公告原文的動詞與時態**：原句是 `We recently submitted a confidential S-1`
   （過去式＋`recently`，**沒有**寫出日期，也**沒有**出現
   `confidentially submitted a draft registration statement on Form S-1` 這樣的措辭）；
   `draft S-1` 只出現在頁面 `<h1>` 與 `<title>`。文章寫「已……保密遞交一份 S-1 註冊說明書
   草稿」並在兩處明講公告沒有寫遞件的實際日期、2026-06-08 只是公開確認日，與原文相符。
   2026-06-08 的依據是 hero meta 區塊的 `<p class="text-meta text-primary-100">June 8, 2026</p>`，
   緊鄰分類連結 `Company` 與 `<h1>`，確認是這篇文章自己的日期。
   **Rule 135 沒有任何制式語句**：`shares`、`price range`、`market conditions`、`subject to`、
   `road show`、`underwrit`、`IPO`、`NASDAQ`、`NYSE`、`valuation` 在公告頁**全部 0 次**，
   文章也沒有替它補上「股數與價格未定」「視市場狀況」「SEC 審閱完成後」這類句子。
   全文沒有「已申請上市」「即將上市」「預計某月掛牌」——title、description、summary、
   `hero_label`、hero alt、圖解 alt 與 caption 全部掃過；「申請上市」只出現在 FAQ 第 1 題的
   **問句**，答案第一個字就是「沒有」。
7. **界線**：沒有估值、上市時程預測、購買或投資建議；正文與 summary 出現的金額只有
   12.35 億美元這個 EGC 門檻（來源印出的數字），「1,220 億美元募資」**只**出現在第二個
   結尾連結的標題文字，正文任何位置都沒有。`topics` 為 `["ai","ai-news"]` 不含 `finance`；
   只有一個 callout，且是本篇自己的提醒（明講不是投資建議），沒有另加投資免責 callout。

### 四、留給站主的事

1. 四條 `sources[]` 已達上限，文章仍然不解釋 Form D 是什麼，只是現在會**誠實告訴讀者**
   「本文引用的來源沒有解釋這份表單」。要真的寫出用途就得換掉一條來源
   （17 CFR 239.500，或 `data.sec.gov` 上某一筆 Form D 本身）。本輪維持不動 `sources[]`。
2. 第二個結尾連結的標題含「1,220 億美元募資」。兩個結尾連結依規格由協調者處理，本輪未動。
3. `www.sec.gov` 本輪同樣沒有實測（沿用前兩輪的 403 紀錄），文章只描述查詢概念、
   不給可點的網址——這個保守作法在 `www.sec.gov` 可讀之前都成立。

### 五、自檢

```
FAIL
 - zh-TW link text must be the title of ai-news-2026-january-september-index
```

僅剩規格允許保留的那一條。段落總字數 2,888（1,800–3,000），`description` 195 字
（120–200），`title` 33 字，每節 2–4 段，兩個結尾連結未動。
兩個 JSON 檔重新驗證：可解析、2 格縮排、不跳脫非 ASCII、LF、檔尾一個換行。

### 六、結論

`ok`——第一輪的 19 處改動**方向全部正確**，骨幹論述經得起逐句回源。本輪又改的 9 處裡，
最重的是第一輪重寫保密段時漏掉的 Rule 83 但書（修正一個過頭的方向）、一個被來源直接
否證的「只有」全稱句，以及第一輪自己留在研究紀錄裡沒刪乾淨的「不確認也不否認」。
三者都不改變文章的立場，只是把它拉回來源真正寫的範圍。`verified_facts` 24/24 連續字串
命中、EDGAR 四個數字獨立重數一致，界線與 `must_not_write` 逐條合規。
沒有動 `sources[]`、沒有動兩個結尾連結、沒有 git add／commit，repo 裡沒有留暫存檔。
