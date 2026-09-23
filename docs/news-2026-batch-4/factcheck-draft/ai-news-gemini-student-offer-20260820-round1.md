# 查核報告：ai-news-gemini-student-offer-20260820（第一輪）

- 查核代理：獨立查核代理（第一輪），未參與撰稿
- 查核日：2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-gemini-student-offer-20260820.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-gemini-student-offer-20260820.json`（已附 `factcheck`）
- 結論：**needs_second_round**（第一輪改了 14 處，其中 9 處是事實，且動到第二節與第四節的骨幹論述）

---

## 1. 重抓結果

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥ 2 秒。
任何請求的 UA、標頭、查詢字串都沒有帶入任何人的姓名、email 或個人資料。

| # | 來源 | 今天的狀態 | bytes | 抽出的正文 | 是不是正文 |
| --- | --- | --- | --- | --- | --- |
| 1 | `blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/` | 200 | 384,141（與研究紀錄相同） | 13,069 字元，含九條註腳 | 是 |
| 2 | `one.google.com/offer/studentoffer8` | 200 | 1,043,224（研究紀錄 1,043,180） | 3,376 字元條文 | 是 |
| 3 | `support.google.com/googleone/answer/16548195?hl=zh-TW` | 200（302 到 `?hl=zh-Hant`） | 1,708,111 | 3,377 字元，含 168 筆國家清單 | 是 |
| 4 | `gemini.google/tw/students/?hl=zh-TW` | 200 | 180,799（與研究紀錄相同） | 5,156 字元，含頁尾但書與常見問題 | 是 |
| 對照 | `support.google.com/googleone/answer/16548195?hl=en` | 200 | 1,700,071 | 6,327 字元，168 筆、Taiwan 第 145 | 是（只做對照，不入 sources） |

公告頁 JSON-LD 今天仍印 `"datePublished": "2026-08-19T19:00:00+00:00"` 與 `"dateModified": "2026-08-21T21:29:45.413039+00:00"`；
條款頁仍自印 `Last updated: August 19, 2026`，研究紀錄「條款若改日期整段重核」的觸發條件沒有發生。
四份來源的 `checked_on` 都是 2026-09-23，與內容包第二段、表格 caption、研究紀錄一致，未改。

清單逐筆清點（`<li>` 計數，中英兩版各跑一次）：

| 項目 | zh-TW 版 | en 版 |
| --- | --- | --- |
| 清單長度 | 168 | 168 |
| 台灣／Taiwan | 第 145，前後為瑞士／塔吉克 | 第 145，前後為 Switzerland／Tajikistan |
| 香港／Hong Kong | 第 64 | 第 64 |
| 澳門／Macau | 第 86 | 第 86 |
| 美國／United States | 第 159 | 第 159 |

內容包寫的「168 筆、台灣第 145 筆、前後瑞士與塔吉克」今天完全復現，`live_data_warnings` 第 1 條不需動。

---

## 2. 主張表

77 條。`C` = CONFIRMED、`X` = CHANGED、`N` = NOT FOUND、`S` = 風格／不在事實範圍。

### 標題、描述、開場

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 1 | title「一年免費的 Google AI 學生方案」 | C | `1. Sign up for your 12-month student plan, free of charge.` |
| 2 | title「台灣在供應名單內」 | C | 說明頁供應清單第 145 筆＝台灣；寫的是「供應名單」不是「資格名單」，與四份頁面說得出口的範圍一致 |
| 3 | title「期滿自動續扣」 | C | 條款 Recurring billing 段 |
| 4 | title 與研究紀錄 `title` 逐字相同、長度 36 | C | 自檢 |
| 5 | description 事件日與「官方頁面自印 8 月 19 日」 | C | 頁面印 `Aug 19, 2026` |
| 6 | description 以「（2026 年 9 月查證）」結尾、長度 151 | C | 規格 |
| 7 | 第一段事件日 2026-08-20＝slug 後綴＝`news_date` | C | DELTA-4-4 第 3 條 |
| 8 | 第一段「公告頁面自己印出的日期是**美國時間** 8 月 19 日」 | **X** | 頁面沒有標任何時區 |
| 9 | 第一段四項功能「同一天另外**開放**……給所有使用者」 | **X** | 原文是 `are rolling out today` |
| 10 | 「這一則在發布當時沒有排進本站的頭條批次，這一篇補上」 | S | `must_not_write` 只准這一句，逐字相符 |
| 11 | 公告與條款列出的排除地區都沒有台灣 | C | 註腳 3 七個地區、條款六個地區，兩份都沒有台灣 |
| 12 | 說明頁清單上有台灣 | C | 第 145 筆 |
| 13 | 最終資格由 Google 在兌換流程自行認定 | C | `Google reserves the right to determine eligibility in its sole discretion.` |
| 14 | 「公告本身沒有任何一句寫『台灣可以』」 | C | 五份抓下來的頁面全文搜尋，沒有任何一句寫台灣學生合格 |
| 15 | 第二段：四份官方文件、2026-09-23 查核 | C | 今天四條全部 200 且讀到正文 |
| 16 | 第二段「**文中**的功能說明」 | **X** | DELTA-4-7 第 14 條的自我指涉 |
| 17 | 第二段與結尾 callout 逐字重複 | **X** | 同上 |

### summary 五句

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 18 | 第 1 句：日期、兩套方案、同日四項功能 | C | 公告正文與註腳 1、3 |
| 19 | 第 2 句：排除地區都沒有台灣；168 筆、第 145 筆 | C | 今天清點復現 |
| 20 | 第 3 句：五個資格條件 | C | 條款 Requirements & eligibility 五條逐條相符 |
| 21 | 第 4 句：12 個月、12-31 兌換期限、期滿續扣、不適用 Workspace for Education | C | 條款 The Offer／Recurring billing／General |
| 22 | 第 5 句：$165 無幣別；常見問題寫「美國大學生」、**搜尋摘要文字**寫 Google AI Pro | **X**（用語） | 那串字只在 `<meta name="description">` |

### 第一節：免費一年的兩條路徑

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 23 | 美國合格大學生免費一年 Google AI Pro | C | `For eligible college students in the U.S., we're offering one year of Google AI Pro for free` |
| 24 | 美國以外「Google AI Plus 有供應的 140 多個市場」免費一年 AI Plus | C | 註腳 3 `in over 140 markets where Google AI Plus is available` |
| 25 | 該段的歸因語有三個 | **X** | 上限兩個 |
| 26 | 四項功能當天開始鋪開給所有 Gemini app 使用者、不限學生 | C | `The student hub, study notebooks, interactive visualizations, and Deep Research in Gemini Live are rolling out today to all Gemini app users.`（註腳 6、7 另有縮限，見待決事項 1） |
| 27 | 定價、Notebook 用量倍率、完整排除清單「另一則開學公告注腳已整段寫過」 | C | 開檔核對目標內容包：19.99／4.99 各 2 次以上、「4 倍」2 次、七個排除地區全在 |
| 28 | 那一則是「**同一週**發布」 | **X** | 目標是 2026-09-17／18 的公告，距本篇公告一個月 |

### 第二節：台灣算不算

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 29 | 公告註腳七個排除地區（含順序：美、玻、阿、加、澳門、香港、突） | C | 註腳 3 逐字相符，順序也相同 |
| 30 | 條款六個排除地區（玻、阿、加、香港、澳門、突），沒有美國 | C | `(except for Bolivia, Albania, Canada, Hong Kong, Macau, and Tunisia).` |
| 31 | 「沒有美國，**因為**美國學生走的是另一套 AI Pro 資格」 | **X** | 沒有一頁說明排除清單的理由，且與同節後面「兩份文件都沒有說明原因」自相矛盾 |
| 32 | 說明頁判準被寫成引句「所在國家或地區有沒有這個方案可以訂閱」 | **X** | 頁面原文是「您目前居住的國家/地區，必須支援 Google AI Plus 會員方案：」 |
| 33 | 168 筆、台灣第 145、前後瑞士與塔吉克 | C | 今天中英兩版都復現 |
| 34 | 「Google 頁面本身沒有印出總數」 | C | 頁面只有清單，沒有任何總數 |
| 35 | 香港、澳門、美國都在供應清單上 | C | 第 64、86、159 筆 |
| 36 | 「**這三個地區**被學生優惠排除」 | **X** | 美國只被排除在 AI Plus 那一條路徑之外，條款的六地清單根本沒有美國 |
| 37 | 條款保留 Google 自行認定資格的權利 | C | 條款 Requirements & eligibility 末句 |
| 38 | 「任何一頁都沒有寫『台灣學生符合資格』」 | C | 五份頁面全文搜尋 |
| 39 | 表格列 1 的引句「美國以外 140 多個市場」 | **X** | 兩句被縫成一個引句：「美國以外」在正文、「140 多個市場」在註腳 3 |
| 40 | 表格列 2、3、4 | C | 條款六地／說明頁 168 筆第 145／學生頁頁尾與常見問題 |
| 41 | 表格 caption（34 字） | C | — |

### 第三節：Offer Terms 的關卡

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 42 | 五個資格條件（18 歲、機構所在地、SheerID、個人帳戶、註冊時已有付款方式） | C | 條款五條逐條相符；SheerID 出自條款，不是註腳 5 |
| 43 | 五種不符資格身分（家庭群組、企業採購、Pixel 組合、第三方／Google Fi、受監護帳戶） | C | 條款逐字相符 |
| 44 | 「不適用學校配發的 Workspace for Education 帳戶」出自條款一般條款段 | C | `This offer is not available on your school-issued Workspace for Education account.`（註腳 5 的 `Not available on school-issued accounts` 是 YouTube Premium 組合那一條，本篇沒有引用） |
| 45 | 優惠期是從兌換當天起算的 12 個月 | C | `for the duration of the promoted 12 month period from the day you redeem the Offer` |
| 46 | 2026-12-31 是兌換期限、不是免費期滿的日子 | C | `Offer expires and must be redeemed by December 31, 2026.` |
| 47 | 自動續扣（**缺法規但書**） | **X** | 條款寫 `except where consent is required under applicable laws` |
| 48 | 期間內取消「可能」維持到期滿 | C | 原文用 `may`，內容包也保留了「可能」二字 |
| 49 | 連到 `ai-free-vs-paid-plans-2026` 的敘述「已經寫過概略」 | C | 開檔核對：該篇「學生與團隊方案」段確有台灣在名單內、SheerID、兌換期限 |
| 50 | 圖說 caption 與研究紀錄 `diagram.caption` 逐字相同（104 字） | C | 自檢 |
| 51 | 本篇沒有寫「最長 4 年」「僅限個人使用」 | C | 那兩句只在註腳 5，草稿沒有誤植 |
| 52 | 本篇沒有寫「用學校信箱驗證」 | C | 只在 FAQ 裡當否定句出現 |

### 第四節：台灣學生頁

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 53 | Google 有一個中文台灣學生頁 | C | 200／180,799 bytes、`lang="zh-TW"` |
| 54 | 「**主標**直接寫『免付費使用 Google AI Plus 學生方案 1 年，立即申請』」 | **X** | 第一個 `h1` 是「Google Gemini：免付費使用學生方案 1 年」，沒有方案名；帶 AI Plus 的那句在第三個 `h1`「準備好提升學習成效了嗎？」底下，且句末有驚嘆號 |
| 55 | 頁尾但書逐字（兌換期限、付款方式、每月 $165、隨時取消） | C | 逐字相符（頁面另在句首有「僅限符合資格的學生。須遵守優惠條款。」，內容包從「兌換期限」起引，不影響語意） |
| 56 | 「頁面只印『$165』，未標幣別，也沒有『新台幣』三個字」 | C | 頁面確實只印 `$165`；全篇「新台幣」只出現在否定句與 FAQ 題目裡 |
| 57 | 常見問題「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案……每年都必須驗證資格」 | C | 逐字相符 |
| 58 | 與英文公告的分流互相矛盾、以查核日限縮 | C | 註腳 1／3 的分流 |
| 59 | meta description「立即訂閱 Google AI Pro 方案，享有更多 Gemini 功能」 | C | `<meta name="description">`／`og:description`／`twitter:description` 三個都有，句末有驚嘆號 |
| 60 | 「主標題推 Plus、**常見問題講 Pro**、搜尋摘要文字又寫 Pro」 | **X** | 常見問題寫的是 **Plus**，不是 Pro；寫 Pro 的只有 meta description |
| 61 | 「這不代表 Google 承認翻譯出錯」 | C | 五份頁面都沒有這種說法，守住 `must_not_write` |

### 第五節、FAQ、callout、連結、sources

| # | 主張 | 判定 | 依據 |
| --- | --- | --- | --- |
| 62 | 四份文件沒有定義「高等教育機構」 | C | 條款只寫 `higher education institution`，沒有定義 |
| 63 | 沒有寫 SheerID 要送什麼、審核多久 | C | 兩頁都只寫「以 SheerID 驗證」 |
| 64 | 沒有列出 140 多個市場的完整名單 | C | 註腳 3 沒有連出清單 |
| 65 | 沒有寫台灣的標準月費 | C | 條款只寫 `the standard monthly subscription price ... for your country` |
| 66 | 領取入口需登入、本站沒有登入 | C | 沿用研究紀錄 `unverified_or_excluded`；本輪同樣沒有登入 |
| 67 | 168／145 是查核當天結果、清單會變 | C | 今天復現，`live_data_warnings` 照寫 |
| 68 | FAQ 1：只能說台灣不在排除名單、在供應清單上，最終由 Google 認定 | C | 守住 `must_not_write` 第 2 條 |
| 69 | FAQ 2：12 個月從兌換日起算、12-31 是兌換期限 | C | 條款 |
| 70 | FAQ 3：只寫 SheerID，沒有學校信箱 | C | 條款 |
| 71 | FAQ 4：$165 無幣別；公告寫「4.99 美元或當地等值金額」 | C | 註腳 3 |
| 72 | FAQ 5：「把**這幾個地區**另外排除在外」 | **X** | 同 #36，把美國掃進港澳同一句 |
| 73 | callout：四份文件、沒有登入、不構成建議、最終由 Google 認定 | C | 與條款一致；AI 垂直只有這一個 callout，沒有多加免責段 |
| 74 | 第一個結尾連結文字「2026 年 AI 新聞總整理：1 月至 9 月的重點與生活應用」 | C | 逐字等於 `ai-news-2026-january-september-index` 的 zh-TW `title` |
| 75 | 第二個結尾連結文字「Gemini Notebook 開學工具上線：公司、學校與個人帳號各有各的條件」 | C | 逐字等於目標內容包 zh-TW `title`，且與 `check_article.py` 的 `RELATED` 第 167 行一致 |
| 76 | 兩個內文 `article` 連結的文字 | C | 逐字等於兩個目標的 zh-TW `title` |
| 77 | 四條 `sources` 的標題、網址、`checked_on` | C | 今天全部 200、讀到正文；`checked_on` 未改 |

---

## 3. 改掉的 14 處

事實 9 處（#8、#9、#28、#31、#32、#36、#47、#54、#60），連帶修正 3 處（#22／#39／#72 的相同用語與同一個分別），讀者優先 2 處（#16＋#17、#25）。

1. **#8 頁面自印日期的時區** — `（台北時間；Google 公告頁面自己印出的日期是美國時間 8 月 19 日）` → `（台北時間；公告頁面自己印出的日期是 8 月 19 日）`
   來源：<https://blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/>（頁面只印 `Aug 19, 2026`，沒有標時區）。
   跨日的兩個日期都還在，description 與 summary 本來就寫「官方頁面自印 8 月 19 日」，改後三處一致。

2. **#9 四項功能的開放狀態** — `同一天另外開放……四項功能，給所有 Gemini 應用程式使用者。` → `同一天起也向所有 Gemini 應用程式使用者鋪開……四項功能。`
   來源：同上（`are rolling out today`）。

3. **#16／#17 第二段** — 刪掉與結尾 callout 逐字重複的「不構成使用或購買建議」與「這項優惠」，「文中」改「這裡」，「Google 提供的台灣學生頁面」縮成「台灣學生頁」。
   依據：DELTA-4-7 第 14 條。查核日 2026-09-23 保留（`check_article.py` 要求它出現在開頭兩段）。

4. **#25 第三段歸因密度** — `Google 官方公告把免費方案分成兩條路徑：` → `免費方案分成兩條路徑：`（該段原有三個歸因語，上限兩個）。

5. **#28 第二個連結那篇的時間** — `Google 在同一週發布的另一則開學公告注腳已經整段寫過` → `Google 九月另一則開學公告的注腳已經整段寫過`
   依據：`apps/api/app/guides/content/ai-news-gemini-notebook-study-tools-20260918.json` 的 `news_date` 是 2026-09-18，其 sources 是 9/17–18 的 Workspace 公告與 9/15 消費端原文，距本篇公告一個月。

6. **#31 條款排除清單沒有美國的理由** — `——沒有美國，因為美國學生走的是另一套 Google AI Pro 資格` → `——沒有美國，美國的合格學生走的是另一套 Google AI Pro 資格`
   來源：<https://one.google.com/offer/studentoffer8>、註腳 1。沒有一頁說明排除清單的理由；原句也與同節後面「兩份文件都沒有說明原因」打架。

7. **#32 說明頁判準的假引句** — `用來判斷「所在國家或地區有沒有這個方案可以訂閱」` → `用來判斷居住的國家或地區有沒有這個方案可以訂閱`
   來源：<https://support.google.com/googleone/answer/16548195?hl=zh-TW>（「您目前居住的國家/地區，必須支援 Google AI Plus 會員方案：」）。改成「居住的」同時把說明頁的**居住地**判準與條款的**機構所在地**判準分開。

8. **#36 美國被寫成「被學生優惠排除」** — `換句話說，這三個地區被學生優惠排除……兩份文件都沒有說明原因。` → `換句話說，香港與澳門被這項學生優惠排除……兩份文件都沒有說明原因；美國不同，美國的合格學生另有 Google AI Pro 那一套。`
   來源：註腳 1（美國合格學生一年 Google AI Pro）＋條款六地排除清單（沒有美國）。這正是公告註腳與 Offer Terms 兩份清單不一致的地方，不能壓平。

9. **#39 表格對註腳的縫合引句** — `只寫「美國以外 140 多個市場」與 7 個排除地區` → `只寫「Google AI Plus 有供應的 140 多個市場」與 7 個排除地區`
   來源：註腳 3（`Eligible students in over 140 markets where Google AI Plus is available`）。

10. **#47 自動續扣掉了法規但書** — `期滿如果沒有提前取消，系統會自動……` → `期滿如果沒有提前取消，除非適用法律要求另行取得同意，系統會自動……`
    來源：<https://one.google.com/offer/studentoffer8>（`except where consent is required under applicable laws`）。研究紀錄明寫這個限定詞要保留。

11. **#54 台灣學生頁的「主標」** — `主標直接寫「……立即申請」。` → `頁面下半的申請區塊寫「……立即申請！」，最上方的大標則只寫「免付費使用學生方案 1 年」，沒有點出方案名稱。`
    來源：<https://gemini.google/tw/students/?hl=zh-TW>。頁面第一個 `h1` 是「Google Gemini：免付費使用學生方案 1 年」；帶 Google AI Plus 的那句在第三個 `h1` 底下的行動呼籲區塊，句末有驚嘆號。**研究紀錄原本也把它寫成「主標」，同樣不準**（`verified_facts` 那一條的引句本身在頁面上找得到，錯的是位置）。

12. **#60 三處不一致的內容** — `主標題推 Plus、常見問題講 Pro、搜尋摘要文字又寫 Pro` → `申請區塊推 Google AI Plus、常見問題把 Plus 說成美國大學生專屬、網頁描述又改推 Google AI Pro`
    來源：同上。常見問題寫的是 **Google AI Plus**（「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案」），只有 meta description 寫 Pro。草稿把兩端都標錯，整段論證因此站不住。

13. **#22 用語：搜尋摘要文字 → 網頁描述**（正文、表格列 4、summary 第 5 句共三處）
    來源：同上。那串字只存在於 `<meta name="description">`／`og:description`／`twitter:description`；Google 搜尋實際顯示什麼本站沒有查。

14. **#72 FAQ 第五題** — `把這幾個地區另外排除在外；` → `把香港與澳門另外排除在外（美國是改走 Google AI Pro 那一套）；`（同 #36）。

---

## 4. 查過而且正確的部分

- **台灣的分寸全篇守住**：四份頁面沒有任何一句寫台灣學生合格，內容包也沒有一句這樣寫；能寫的兩件事（不在排除名單、在供應清單上）都有出處，並且每次都帶上「最終由 Google 自行認定」。title 用的是「供應名單」而不是「資格名單」。
- **12 個月與 12 月 31 日沒有混用**：第三節、summary 第 4 句、FAQ 第 2 題三處都寫「從兌換當天起算 12 個月」「12 月 31 日是兌換期限」。
- **$165 全篇沒有變成新台幣**：三處提到金額都標明頁面沒有印幣別，`must_not_write` 第 7 條守住。
- **SheerID 與學校配發帳戶的出處正確**：兩條都歸給 Offer Terms，不是註腳 5；註腳 5 獨有的「最長 4 年」「僅限個人使用」全篇 0 次。
- **19.99 美元沒有被寫成美國學生要付的錢**：本篇根本沒有引用這個數字，改為連到已發布的那一篇。
- **兩篇既有文章是連過去、不是重寫**：Notebook 那篇只用一句帶過定價、用量倍率與完整排除清單；`ai-free-vs-paid-plans-2026` 只用一句帶過台灣在名單內、SheerID、兌換期限。兩處連結文字都與目標的 zh-TW `title` 逐字相同。
- **沒有購買建議、沒有推薦式比價**：callout 明寫不構成使用或購買建議，正文沒有「值得／划算／該不該辦」的語氣，也沒有跨廠商學生方案比較。
- **沒有「最近」「本週」「日前」「本文」「首次」「唯一」「從未」**；否定句一律限縮成「這幾頁沒有寫」並帶查核日。
- **沒有 AI 生成摘要的句子**：公告頁 `Read AI-generated summary` 區塊的每一句都不在內容包裡。
- **沒有描述任何商標圖示或介面截圖**；hero 與圖解的 alt 都寫成不含商標的抽象構圖。

---

## 5. 留給協調者／站主的事

1. **公告註腳 6、7 縮限了正文那句「給所有使用者」**：兩條都寫 `Available on mobile and web to all signed in consumer accounts in all Gemini app languages. Rolling out to school-issued Google accounts and users who meet minimum age requirements in the coming weeks.`。研究紀錄沒有收這兩條，本篇也沒寫。段落字數目前 **2,958／3,000**，要補得先挪出約 30 字。建議補在第一節第一段末尾並註明是註腳 6、7——請協調者決定補或不補。
2. **居住地判準 vs 機構所在地判準**：說明頁寫「您目前居住的國家/地區」，條款寫「你就讀的合格高等教育機構所在的國家或地區」，兩者不是同一件事。第二節用供應清單推台灣、第三節才寫機構條件，中間沒有把落差點破。本輪只把第二節的動詞改成「居住的」；要不要加一句明講，請協調者決定（同樣受字數限制）。
3. **第二段仍與結尾 callout 重複約一半**：本輪只刪逐字重複的部分。若要再精簡，第二段還可省約 60 字，正好給前兩件事騰空間。
4. **`description` 裡的「查核過程」**：DELTA-4-7 第 14 條說 description 不寫查證流水帳。現行句是「……台灣是否列在供應名單上的查核過程……（2026 年 9 月查證）」，結尾合規、中間偏流水帳。長度 151，可換成「台灣列在哪一份官方名單上」而不破 120–200。本輪未動。
5. **引句的排版空格**：台灣學生頁原文是「2026年12月31日」（數字與中文之間沒有空格），內容包依站上排版慣例寫成「2026 年 12 月 31 日」。全批一致，本輪未動。
6. **領取入口需登入**：`one.google.com/ai-student` 本輪同樣沒有登入、沒有重抓，正文相關敘述維持研究紀錄的寫法。
7. **研究紀錄的一個小錯已記在 `factcheck` 裡**：`verified_facts` 把台灣學生頁的行動呼籲寫成「主標」。引句本身在頁面上找得到，錯的是位置；`verified_facts` 原文本輪未改，只在 `factcheck.changes` 說明。第二輪若要，可一併訂正。

---

## 6. 自檢

```
$ ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py ai-news-gemini-student-offer-20260820
OK ai-news-gemini-student-offer-20260820 zh-TW paragraphs 2958
exit=0

$ ./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life --slug ai-news-gemini-student-offer-20260820
ai-news-gemini-student-offer-20260820
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` so they become article inlines that follow the target's publication
  error: image_missing: zh-TW: /guides/ai-news-gemini-student-offer-20260820/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-gemini-student-offer-20260820/diagram-1.svg
1 entries checked
exit=1
```

兩個 lint 類別都是出圖與 relink 之前的預期狀態。退出碼另寫在
`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-gemini-student-offer-20260820-r1\exit-codes.txt`。

## 7. 結論

**needs_second_round**。第一輪改了 14 處，其中 9 處是事實；第四節的骨幹論證（台灣學生頁三處寫法不一致）被重寫，
第二節對美國的歸類也重寫過，這兩段的每一句都要第二輪逐句回一手來源重查。
第二輪另請覆核本輪新寫進去的五句：第一段「同一天起也向所有 Gemini 應用程式使用者鋪開」、
第二節「美國不同，美國的合格學生另有 Google AI Pro 那一套」、第三節「除非適用法律要求另行取得同意」、
第四節「最上方的大標則只寫『免付費使用學生方案 1 年』，沒有點出方案名稱」與
「常見問題把 Plus 說成美國大學生專屬」。
