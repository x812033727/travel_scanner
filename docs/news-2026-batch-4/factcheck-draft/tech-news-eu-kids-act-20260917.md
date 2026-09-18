# 獨立查核：tech-news-eu-kids-act-20260917

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 本來就是 2026-09-18，四處一致，**沒有改**）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 今天重抓並讀 body，
新聞稿 PDF 用**系統 Python + pypdf** 抽文字（3 頁、7,545 字元），
研究紀錄每一條 `verbatim_quote` 都用**字面子字串搜尋**回原文比對。
除了為了反駁而開的兩個官方端點（factsheet 列印端點、執委會的 KIDS Act 政策總覽頁）以外，
**沒有用任何 `sources[]` 以外的網址替文章補事實**，也沒有猜任何識別碼或網址。

檢查的主張：**124 條**（正文 37 句、summary 4 句、FAQ 6 題的 15 個答句、表格 16 格＋表頭＋caption、
callout、圖解 caption、title、description、兩個 link text、研究紀錄的 28 條逐字引文與 diagram 六個欄位）。
**改了 16 處**，另有 4 件留給站主。`hero.alt` 依規格未查未改。

## 重抓結果（四條 sources 今天都拿到正文，bytes 與撰稿者紀錄完全相同）

| source | HTTP | bytes | body 是正文嗎 | 驗到的東西 |
| --- | --- | --- | --- | --- |
| digital-strategy `/en/news/eu-kids-act-...-children-eu` | 200 | 49,928 | 是，伺服器端算好的 HTML | 開頭兩段、`PRESS RELEASE / Publication 17 September 2026`、`Last update 17 September 2026`、von der Leyen 引文。**這一頁沒有四大支柱的內容**，只有導言與「Read the full press release and factsheet」 |
| presscorner `.../print/en/ip_26_1890/IP_26_1890_EN.pdf` | 200 | 87,640 | 是，`application/pdf`，pypdf 抽出 3 頁 7,545 字元 | `Strasbourg, 17 September 2026`、`IP/26/1890`、四大支柱全文、Next steps、Background、兩則具名引文（皆 `- 17/09/2026`） |
| digital-strategy `/en/faqs/kids-act-explained` | 200 | 68,346 | 是 | 年齡階梯、既有帳號六個月條款、零知識證明、4,500 萬門檻、6%、30／90 天、監督分工 |
| digital-strategy `/en/library/proposal-eu-kids-act-...` | 200 | 53,786 | 是 | 提案正式全名、`Publication 17 September 2026`、提案本體／Communication／SWD 三個下載 |

**逐字引文**：研究紀錄 28 條（含我新增的 3 條）今天全部是原文的連續字串，只有 1 條原本不是（見改動第 16 項）。

**factsheet 今天重測仍是 404**：`.../print/en/fs_26_1891/FS_26_1891_EN.pdf` 回 HTTP 404、300 bytes 的 JSON
（`Document with Reference fs_26_1891 and langague en not found`，`langague` 是對方頁面自己的錯字，照抄）。
撰稿者沒有重測、直接沿用前期紀錄的結論，這次測過了，結論成立。

## 改掉的 16 處

1. **年齡邊界寫反了（最重的一處）。「13 歲以下」→「未滿 13 歲」**，共 6 處（title、description、第一段、
   summary 第 1 句、第 2 節第 1 段、FAQ 第 2 題）。來源是 `children under the age of 13`／`Under 13: no account.`，
   而 13、14 歲**有**監護人開設的迷你帳號——中文「13 歲以下」含 13 歲，等於把 13 歲說成禁止，
   和文章自己的表格（`13 歲至未滿 15 歲`）互相矛盾。同一型態在另一端：
   **「18 歲以下」→「未滿 18 歲」**（第 3 節第 1 段、summary 第 3 句、圖解格）——原文是 `users below the age of 18`。
2. **表格「15 歲以上」列的「官方寫明的限制」寫成「官方頁面未再另列限制」**，是被來源推翻的否定句：
   安全設計義務的適用對象是 `below the age of 18`，15 到未滿 18 歲的服務仍在義務範圍內。
   已改成「服務仍須符合未滿 18 歲的安全設計義務」。
3. **罰則多了一個來源沒有的限定詞。「全球前一年總營業額的 6%」→「全球年總營業額的 6%」**（第 5 節第 2 段、FAQ 第 5 題）。
   問答頁印的是 `Fines can reach 6% of total worldwide annual turnover.`；
   `preceding` 在四份 body 裡 **0 次**——「前一年」是《數位服務法》的寫法，被帶進來了。
4. **年齡規定的適用範圍被放大。** 草稿把年齡階梯寫成適用於社群媒體全體；問答頁自己劃了範圍：
   `The age rules apply to social networking and video-sharing services with proven risky features`
   （提案摘要頁的說法一致：`certain online social networking services and video-sharing platforms`）。
   已在第 2 節第 1 段與 FAQ 第 2 題補上「適用的是帶有經證實風險功能的社群網路與影音分享服務」。
5. **情態詞被強化。「規則要求監護人開設迷你帳號」→「提案要求平台提供家長管控，讓監護人開設迷你帳號」。**
   新聞稿是 `the proposal calls for parental control, enabling guardians to set up mini accounts`，
   問答頁是 `a guardian can set up a limited account`——義務在平台，不在監護人。
6. **把單一產品的性質推廣到全部方案。** summary 第 3 句原本寫「年齡驗證方案不留存身分證件與生物特徵資料」，
   但新聞稿只對**歐盟年齡驗證應用程式**這麼寫（`the EU age verification app, which does not retain identity documents or biometric data`）。
   已改成指名該應用程式。同句另補回 `without stopping points`（「沒有停頓點的無限捲動」）與「未滿 18 歲」。
7. **summary 第 4 句掉了「歐盟境內」**：原文是 `45 million or more active monthly users in the EU`，門檻是歐盟境內的月活躍使用者。已補。
8. **禁止清單三個詞被放寬**（第 3 節第 2 段）：`profiling-based recommender feeds`→「演算法推薦」改為「依側寫推薦的訊息流」；
   `reward tricks`→「獎勵機制」改為「獎勵花招」；`unsolicited contact from strangers`→「陌生人主動搭訕」改為「陌生人未經邀請的接觸」。
   清單本身的「新聞稿列了好幾種」（`These include` / `It also includes`）沒有被寫成全清單，這點原本就對。
9. **第三支柱名稱**：`Privacy-preserving age assurance` 被譯成「隱私保護的年齡驗證」，
   但同一份新聞稿把 `age assurance`（工具）與 `age verification`（開新帳號時執行的動作）分開用，
   文章兩段後正是靠這個分別。已改成「隱私保護的年齡查核」。
10. **被刪掉的條件補回**：第 2 節補 `when it is passed on to children`（「在裝置交給兒童使用時」）；
    第 4 節第 3 段補 `Before coming into contact with children under the new rules`，
    並把「提交合規計畫」還原成問答頁的 `a detailed plan showing how they intend to meet every obligation of the law`；
    第 3 節第 3 段把 `Online services` 還原成「線上服務」、把 `safe recommender systems` 的「安全」補回。
11. **工具敘事從正文移出。** 第 5 節最後一段原本告訴讀者「提案本體的 PDF 本文沒有下載」「factsheet 連結回應 HTTP 404」——
    這是 BRIEF 型態 5 明文排除的容器／工具敘事。已改寫成「本文依據的是執委會自己的新聞稿與問答摘要，不是提案的法條全文」，
    404 這件事留在研究紀錄與本報告裡（而且我今天重測過，仍是 404）。
12. **自己清點出來的數字。** 同一段寫「這是本站……第三篇處理同一個服務、歐盟另有一套規則的報導」——
    同批另有一篇歐盟題（`tech-news-apple-att-eu-20260916`），這個「第三」一上線就可能是錯的。已刪掉計數。
13. **否定句收窄**：「官方文件也沒有提到台灣或歐盟以外的地區」與 FAQ 第 6 題的「也沒有提到歐盟以外的任何國家或地區」
    收成「沒有提到台灣」（`Taiwan` 在四份 body 各 0 次，這一條站得住）；
    「官方沒有給時間表」→「官方頁面沒有寫出時間表」。
14. **FAQ 第 6 題的管轄推論。** 「提案規範的是在歐盟境內提供的服務」不是任何一頁寫的；
    改成來源真的寫的「這是一部歐盟的法規提案，訂的是歐盟共通的年齡與設計規則」。
15. **一批小的**：「案號 IP/26/1890」→「編號」（那是新聞稿編號，不是案號，兩處）；
    `children and young people's protection online`→「兒童與青少年的網路保護」（原本掉了青少年）；
    `will be called to perform age verification`→「將被要求執行」；
    `National authorities designated by Member States`→「會員國指定的主管機關」；
    「規則要求採用零知識證明技術」→「提案要求」（提案語氣）；
    第 3 節結尾原本斷言「官方自己認為（設計義務）比年齡關卡更核心」，改用問答頁自己的
    `more importantly that they are safe in their design`；
    第 5 節第 1 段的「證明服務符合兒童安全與設計的要求」還原成 `age-appropriate and safe by design`。
    另**補了一段來源有、草稿沒寫**的內容：未滿 13 歲那一段實際長什麼樣（孩子本身沒有帳號、
    個人化推薦與搜尋關閉、家長可隨時中止、滿 13 歲結束）。
16. **研究紀錄**：`verified_facts` 第 15 條的 `verbatim_quote` 用刪節號把兩句接起來，而且跨過一個連結邊界——
    PDF 與 HTML 抽出來的文字都是 `Child Safety Online , Dr Maria Melchior`（逗號前有一個空格），
    整串在兩份 body 裡都搜尋不到。已拆成兩條各自搜尋得到的短引文，並寫明那個空格是怎麼來的。
    同時：title 與圖解兩格跟著年齡用字改；新增 2 條問答頁的事實（適用範圍、未滿 13 歲的安排）；
    加上 `factcheck` 欄位與一條 `live_data_warnings`（四頁的 `Last update` 是頁面狀態，不是事實，沒寫進文章）。

## 查過而且正確的部分（沒有動）

- **「提案」語氣全篇成立。** `in force`、`entry into force`、`apply from`、`2027`、`2028` 在四份 body 全部 **0 次**；
  唯一的狀態句是 `The legislative proposal has been submitted to the European Parliament and Council`。
  文章沒有任何一句把 KIDS Act 寫成已生效、已上路，callout、summary 末句與 FAQ 第 1 題三處各自講了一次。
- **沒有自算日期。** 六個月、30 天、90 天三個期間一律寫成公式（「規則適用後 6 個月內」），
  沒有換算成任何日曆日期，也沒有出現生效年份。
- **哪個數字出自哪一頁，分得對。** `6%`、`45 million`、`30 days` 三個字串只出現在問答頁，其餘三份各 0 次；
  文章「罰則數字只出現在常見問答頁面，新聞稿本文沒有寫」成立。
  （`90 days` 新聞稿也有一次，但文章沒有反過來說新聞稿沒有，所以不算錯。）
- **協調者點名要重查的條件句沒有被簡化。** 既有帳號那條的但書
  `Where a platform can already tell with high confidence that a user is an adult, no new check is needed`
  在第 5 節與 FAQ 第 3 題兩處都完整保留。4,500 萬門檻那條的「詳細計畫＋獨立稽核＋
  `This audit needs to be paid by platforms, not taxpayers`」也逐項對上。
- **HTML 新聞稿與 PDF 沒有互相矛盾。** 兩頁重疊的部分（導言段、von der Leyen 引文）逐字相同；
  四大支柱只存在於 PDF，新聞稿 HTML 那一頁確實沒有，文章引用支柱時都寫「新聞稿」並指向 PDF。
- 四大支柱名稱、五類服務、AI 陪伴預設關閉、預設隱私設定、應用程式商店三項義務、
  執委會／數位服務協調官／市場監督機關／會員國指定主管機關的四段分工、
  `builds on the structures already in place`（沒有寫成修改或取代 DSA／AI Act）——逐條對上。
- 專家小組背景：Maria Melchior 博士、Jorg M Fegert 教授、超過 60 位專家、2026 年 3 月首次召開、
  開會三次、2026 年 7 月交報告——全部逐字在新聞稿裡。92% 那條歸因給執委會引用民調，
  並寫明本文沒查民調本身，符合規格。
- **科技垂直界線**：沒有購買建議、沒有推薦式比價、沒有未歸因的廠商宣稱、沒有免責 callout、
  沒有任何規避年齡驗證的作法、沒有點名任何公司或服務、沒有斷言台灣的規定。
- `checked_on` 2026-09-18 在內容包四條 source、研究紀錄、第二段、表格 caption、圖解 caption 五處一致，未改。
- 兩個結尾連結：第一個逐字等於 DELTA-4-5 指定的科技索引標題；
  第二個逐字等於 `tech-news-eu-cra-reporting-20260911` 的 zh-TW title（32 字，逐字元比對相同）。

## 留給站主的事

1. **factsheet FS/26/1891 到今天仍讀不到**（列印端點 404）。新聞稿頁面掛著它的連結，
   如果之後補上，可能帶有文章目前沒有的數字；文章沒有任何一句依賴它。
2. **提案本體、隨附 Communication 與 SWD 三份文件都可以從提案摘要頁下載，本次沒有讀。**
   條號、法律依據與每項義務的確切文字只在那裡面；文章因此一個條號都沒有引用。
3. **有第五個官方頁 `digital-strategy.ec.europa.eu/en/policies/kids-act`（200、54,563 bytes）**，
   它多寫了兩件四條 sources 都沒有的事：適用對象還包含**應用程式商店與作業系統**，
   以及**部分服務擬予豁免**（百科、教育平台、數位新聞）。它的支柱名稱也不同
   （`Age assurance and parental responsibility`、`Strong enforcement`），30 天在那裡指的是
   合規計畫的審查時限、不是初步認定。`sources[]` 已經是四條上限，所以我沒有動它；
   要不要換掉其中一條、把豁免清單寫進文章，是編輯決定。
4. **四頁的 `Last update` 都還是 2026-09-17。** 發布前如果官方改版，數字要重讀一次。

## 自檢

```
OK tech-news-eu-kids-act-20260917 zh-TW paragraphs 2962
```

沒有留下任何 FAIL（索引與第二個連結都已存在，DELTA-4-5 第 3、4 項的例外用不到）。
正文 2,962 字，上限 3,000；改動過程中沒有為了字數刪掉任何但書或限定詞，
反而是先把工具敘事與自算計數拿掉、才騰出空間補回上面那幾個條件。

## 結論

`needs_owner` — 事實層面已經全部修到位（16 處），文章可以往翻譯走；
留給站主的四件事都是「要不要再擴充」的編輯決定，不是錯誤。
骨幹論述（這是提案、年齡是階梯、設計義務才是主體）沒有被推翻，所以不需要第二輪。

## 第二輪

第二輪代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-09-18**（`checked_on` 仍是 2026-09-18，六處一致，**沒有改**）。
四條來源自己用 `curl -sL -A "Mokaair-editorial"` 重抓：**200／49,928**、**200／87,640**（`application/pdf`，系統 Python ＋ pypdf 6.16.2，3 頁 7,545 字元）、
**200／68,346**、**200／53,786**，四條 body 都是正文，位元組數與前期紀錄、第一輪紀錄完全相同。
另外只為了反駁而開了兩個端點：factsheet 列印端點今天仍是 **HTTP 404、300 bytes** 的 JSON（`langague` 是對方的錯字），
第五個官方頁 `/en/policies/kids-act` **200／54,563**——兩者都沒有拿來替文章補任何事實，`sources[]` 一條都沒有動。

覆核了 **120 條**主張（第一輪改過的每一段、新寫的每一句、28 條逐字引文、表格 21 格與 caption、summary、FAQ、callout、圖解四格與 `hero_label`、title、description），
另跑 12 項程式字串清點。**又改了 5 處**，其中 2 處在研究紀錄、3 處在內容包。

### 又改的 5 處

1. **逐字引文兩條其實對不上（最重的一處）。** 用「只收合空白、不做任何其他正規化」的連續字串比對重跑 28 條，
   第 18 條與第 23 條失敗：問答頁印的是 `‘zero knowledge proof'`（`‘` 是 U+2018），紀錄寫成直引號；
   `The largest platforms – those with 45 million … in the EU – cannot`（`–` 是 U+2013 破折號），紀錄寫成連字號。
   紀錄的 `sourcing_notes` 原本聲明「沒有清掉任何非 ASCII 標點」，對這兩條並不成立。已把來源的原字元還原，
   現在 28 條**全部**是各自來源 body 的連續子字串。
2. **表格沒有帶年齡規定的適用範圍。** 第一輪把問答頁的 `The age rules apply to social networking and video-sharing services with proven risky features`
   補進第 2 節與 FAQ 第 2 題，但表格整張只寫年齡階梯，單看表格會讀成適用於所有服務。
   已把同一句措辭加進表格 caption（「表中的年齡規定適用的是帶有經證實風險功能的社群網路與影音分享服務」），
   正文、表格、FAQ 三處現在逐字相同。圖解 caption 沒有動，仍與研究紀錄 `diagram.caption` 相等。
3. **圖解第四格掉了「年總」。** `最高罰全球營業額 6%` 與正文的「全球年總營業額的 6%」不一致，
   等於在圖上把 `total worldwide annual turnover` 的限定詞拿掉。已改成 `最高罰全球年總營業額 6%`（11.65 單位，上限 15）。
4. **兩句否定句的範圍仍是無界的。** 第 5 節最後一段與 callout 都寫「官方文件（也）沒有提到台灣」——
   「官方文件」不是本文引用的那幾頁。已收成「這四份頁面也沒有提到台灣」與「本文查到的四份官方頁面沒有提到台灣」。
5. **第 4 節的時間表否定句**：「歐盟數位身分皮夾則會在未來加入，官方頁面沒有寫出時間表」收成「常見問答頁面沒有寫出時間表」——
   `and, in time, the European Digital Identity Wallet` 只出現在問答頁，其他三份沒有講這件事。

### 協調者點名的八項，逐項結果

- **(a) 年齡邊界**：全域掃過內容包每一個含「歲」的字串，**沒有任何一處**還寫「13 歲以下」或「18 歲以下」；
  第一輪改的 9 處（title、description、第一段、summary 第 1 與第 3 句、第 2 節、第 3 節、FAQ 第 2 題、圖解格）
  全部是「未滿」，對得上 `children under the age of 13` 與 `users below the age of 18`。方向兩端都對：
  表格的「15 歲以上」是對的（`From 15: young people can open their own account`），
  13／14 歲有迷你帳號的三處（第一段、第 2 節、表格第 2 列、FAQ 第 2 題）與「未滿 13 歲禁帳號」互不矛盾。
- **(b) 適用範圍**：見上面第 2 項，已補成三處一致。
- **(c) 6%**：`preceding` 在四份 body **0 次**；`6%` 只在問答頁出現 1 次，
  新聞稿、新聞頁、摘要頁各 0 次，文章「罰則數字只出現在常見問答頁面」成立。兩處都寫「全球年總營業額」。
- **(d) 提案語氣**：`in force` 0、`entry into force` 0、`apply from` 0、`2027` 0、`2028` 0（四份 body）。
  逐句讀過全篇，沒有任何一句把它寫成已生效；三個期間（六個月、30 天、90 天）一律只寫公式，全篇沒有任何換算出來的日曆日期。
  （注意：`enter into force` 在**第五個頁面**出現 1 次——那一頁不是來源，文章也沒有靠它。）
- **(e) 工具敘事**：正文、summary、FAQ、callout 都搜不到 PDF 沒下載／404 的敘述；第 5 節現在只寫「依據的是新聞稿與問答摘要，不是法條全文」。
- **(f) 第五個官方頁**：它多寫的「也適用應用程式商店與作業系統」「部分服務擬豁免（百科、教育平台、數位新聞）」
  與文章**不矛盾**：文章沒有「只適用／僅適用」這類全稱句（程式掃過 `只適用`、`僅適用`、`只有社群` 皆 0），
  第 4 節本來就寫了應用程式商店的三項義務，而且沒有任何一句否認豁免存在。沒有用它補事實，`sources[]` 維持四條。
- **(g) 逐字引文**：見第 1 項。28 條沒有任何一條含 `...`、`…` 或 `|`；第 15 條已是拆開的兩條短引文，兩條都比對成功。
- **(h) 台灣**：`Taiwan` 在四份 body **0 次**；文章只寫「這四份頁面沒有提到台灣」，不推測、不比較、不預告。

### 另外重驗而且正確的部分

- **但書沒有為字數被刪**：`up to one hour per day`（至多）、`targeted within 90 days`（目標是）、
  `such as`／`These include`（舉的例子／列了好幾種）、`e.g. account creation date, credit card details`（這是舉例，不是完整清單）、
  既有帳號那條的「已能高度確信是成年人就不必重查」——五個都還在。
- `summary` 每句都在正文找得到；FAQ 六題的答句都在正文找得到；圖上四個數字（13、15、18、6）都出現在正文。
- 界線：`topics` 只有 `tech`／`tech-news`（不帶 finance）、只有一個 callout、沒有投資免責段落、沒有購買或升級建議、
  沒有推薦式比價、沒有未歸因的廠商宣稱（92% 仍歸因給執委會引用民調）、沒有規避年齡驗證的作法、沒有點名任何公司。
- 兩個結尾連結**沒有動**：第一個逐字等於科技索引標題，第二個逐字等於既有文章 `tech-news-eu-cra-reporting-20260911` 的 zh-TW title；
  callout 裡「《網路韌性法》通報義務 2026 年 9 月 11 日起適用」與那篇既有文章的第一段一致，沒有改寫它、也沒有與它矛盾。
- `checked_on` 2026-09-18 在內容包四條 source、研究紀錄、第二段、表格 caption、圖解 caption 仍然一致。

### 第二輪自檢

```
OK tech-news-eu-kids-act-20260917 zh-TW paragraphs 2965
```

一個 FAIL 都沒有留下（DELTA-4-5 第 3、4 項允許的那兩條例外用不到）。正文 2,965 字，上限 3,000；
四處改動只增加 3 個字（表格 caption 與 callout 不計入段落字數），沒有為了字數刪掉任何但書或限定詞。

### 第二輪結論

`needs_owner` — 沒有留下任何站不住的事實；這一輪的 5 處是引文忠實度、適用範圍、限定詞與否定句範圍的精修，
骨幹論述（提案、階梯、設計義務為主體）再次成立。留給站主的仍是第一輪那四件擴充與否的編輯決定，
其中第五個官方頁的豁免清單最值得站主決定要不要換來源。
