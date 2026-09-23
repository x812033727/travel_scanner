# 查核報告：ai-news-gemini-student-offer-20260820（第二輪）

- 查核代理：獨立查核代理（第二輪），未參與撰稿、未參與第一輪
- 查核日：2026-09-23
- 內容包：`apps/api/app/guides/content/ai-news-gemini-student-offer-20260820.json`
- 研究紀錄：`docs/ai-news-2026-09-late/research/ai-news-gemini-student-offer-20260820.json`（已附 `factcheck.second_round`）
- 第一輪報告：`C:\Users\x8120\mokaair-work\news44\factcheck\ai-news-gemini-student-offer-20260820-round1.md`
- 結論：**ok**（第二輪改 7 處內容包／2 處研究紀錄，其中 4 處是協調者裁示、3 處是本輪自己查出來的事實或引句問題）

---

## 1. 本輪自己重抓的來源

指令一律 `curl -sSL -A 'Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)'`，同一主機間隔 ≥ 2 秒。
任何請求的 UA、標頭、查詢字串都沒有帶入任何人的姓名、email 或個人資料。

| # | 來源 | 今天狀態 | bytes | 抽出的正文 |
| --- | --- | --- | --- | --- |
| 1 | `blog.google/.../student-offer-google-ai/` | 200 | 384,141 | 13,069 字元，含九條註腳 |
| 2 | `one.google.com/offer/studentoffer8` | 200 | 1,043,553 | 3,376 字元條文 |
| 3 | `support.google.com/googleone/answer/16548195?hl=zh-TW` | 200（302 到 `?hl=zh-Hant`） | 1,704,053 | 3,378 字元，含 168 筆清單 |
| 4 | `gemini.google/tw/students/?hl=zh-TW` | 200 | 180,799 | 5,156 字元，含頁尾但書與常見問題 |
| 對照 | `support.google.com/googleone/answer/16548195?hl=en` | 200 | 1,696,860 | 6,327 字元，168 筆、Taiwan 第 145 |

公告頁 JSON-LD 今天仍印 `"datePublished": "2026-08-19T19:00:00+00:00"`、`"dateModified": "2026-08-21T21:29:45.413039+00:00"`；
條款頁仍自印 `Last updated: August 19, 2026`（研究紀錄「條款改日期就整段重核」的觸發條件沒有發生）。
清單以 `<li>` 中英兩版各清點一次：**都是 168 筆，台灣第 145，前後為瑞士／塔吉克（Switzerland／Tajikistan）**，
香港第 64、澳門第 86、美國第 159，與第一輪數字完全一致。說明頁本身沒有印出總數（頁面上的「共 2 項」是輪播指示器）。

研究紀錄 50 條 `verbatim_quote` 以 NFKC 正規化（彎引號、U+2011、去空白）做**連續字串**比對：
47 條命中抽出的正文，3 條（JSON-LD 的兩個日期、台灣學生頁的 meta description）在 HTML head／原始碼而不在正文，已另以原始碼確認，不是拼接。
沒有一條是把不同段落縫起來的引文。

---

## 2. 第一輪那 14 處，逐一回一手來源重查

`C` = 維持、`X` = 本輪再改。

| # | 第一輪改的東西 | 本輪判定 | 今天讀到的依據 |
| --- | --- | --- | --- |
| R1-1 | 刪掉「美國時間」 | C | 公告頁只印 `Aug 19, 2026`（第 215 行），全頁沒有任何時區標示 |
| R1-2 | 「開放」→「鋪開」 | **X（連帶）** | 原文 `are rolling out today`，改得對；但 summary 第 1 句仍留著「另開放」，本輪一併改掉 |
| R1-3 | 第二段刪自我指涉與重複 | **X（協調者裁示一）** | 仍與結尾 callout 重複一半，本輪砍到本批最低限度 |
| R1-4 | 第三段刪一個歸因語 | C | 該段現為兩個（「官方寫成」「同一篇公告」），符合上限 |
| R1-5 | 「同一週」→「九月另一則開學公告」 | C | 開檔核對 `ai-news-gemini-notebook-study-tools-20260918`：`news_date` 2026-09-18，四條 sources 是 9/17–18 Workspace 與 9/15 消費端原文；該篇正文確實逐項寫過 19.99／4.99、4 倍／2 倍與七個排除地區，並自稱出自「註腳」 |
| R1-6 | 「因為」→「美國的合格學生走的是另一套」 | C | 五份頁面沒有任何一句解釋排除清單的理由；註腳 1 給美國合格學生一年 Google AI Pro |
| R1-7 | 假引句改成「居住的國家或地區」 | C | 說明頁原文「您目前居住的國家/地區，必須支援 Google AI Plus 會員方案：」逐字命中 |
| R1-8 | 把美國從「被學生優惠排除」拆出來 | C | 條款六地清單 `(except for Bolivia, Albania, Canada, Hong Kong, Macau, and Tunisia).` 沒有美國；公告註腳 3 的七地清單才有 |
| R1-9 | 表格引句改「Google AI Plus 有供應的 140 多個市場」 | C | 註腳 3 `Eligible students in over 140 markets where Google AI Plus is available` 逐字命中 |
| R1-10 | 自動續扣補回法規但書 | C | 條款 `On the date your Offer Period ends, except where consent is required under applicable laws, ...` 逐字命中 |
| R1-11 | 「主標」→「頁面下半的申請區塊」 | **X（引句不完整）** | 第三個 `h1`「準備好提升學習成效了嗎？」底下確實是「免付費使用 Google AI Plus 學生方案 1 年，立即申請！」；但第一個 `h1` 頁面印的是「Google Gemini：免付費使用學生方案 1 年」，草稿寫成「只寫『免付費使用學生方案 1 年』」少了前綴 |
| R1-12 | 三處不一致改成「申請區塊／常見問題／網頁描述」 | C | 常見問題確為 Plus（第 93 行），`<meta name="description">`／`og:`／`twitter:` 三個都寫 Pro |
| R1-13 | 「搜尋摘要文字」→「網頁描述」 | C | 那串字只在 head 的三個 meta，正文沒有 |
| R1-14 | FAQ 5 拆開港澳與美國 | C | 同 R1-8 |

## 3. 第一輪新寫進去的五句，逐句回一手來源

| 新句 | 判定 | 依據 |
| --- | --- | --- |
| 「同一天起也向所有 Gemini 應用程式使用者鋪開……四項功能」 | C（但**不完整**，見裁示一） | `The student hub, study notebooks, interactive visualizations, and Deep Research in Gemini Live are rolling out today to all Gemini app users.` |
| 「美國不同，美國的合格學生另有 Google AI Pro 那一套」 | C | 註腳 1「Eligible students in the U.S. only.」＋正文 `For eligible college students in the U.S., we're offering one year of Google AI Pro for free` |
| 「除非適用法律要求另行取得同意」 | C | 條款 `except where consent is required under applicable laws` |
| 「最上方的大標則只寫『免付費使用學生方案 1 年』」 | **X** | 頁面第一個 `h1` 是「Google Gemini：免付費使用學生方案 1 年」，引句漏了前綴 |
| 「常見問題把 Plus 說成美國大學生專屬」 | C | 「18 歲以上符合資格的美國大學生，可免付費使用 Google AI Plus 學生方案。……每年都必須驗證資格，才能繼續使用。」逐字命中 |

## 4. 抽查第一輪判定 CONFIRMED 的三分之一

61 條 CONFIRMED，以 `random.Random(20260923).sample` 抽 20 條（#2、3、4、6、19、21、26、33、34、38、44、46、51、56、57、64、66、68、69、76）。
**19 條維持 CONFIRMED，1 條（#26）改為「正確但不完整」並依裁示補上註腳。** 逐條依據：

- **#2 title「台灣在供應名單內」／#38「任何一頁都沒有寫台灣學生符合資格」** — 五份頁面全文搜尋：`terms` 0 次提到 Taiwan，`blog` 只在語系選單出現兩次「台灣 (中文)」，說明頁只有清單那一筆，學生頁只在語系選單。title 用「供應名單」不是「資格名單」，守得住。
- **#3 期滿自動續扣／#46 12-31 是兌換期限** — 條款 `Offer expires and must be redeemed by December 31, 2026.` 與 `for the duration of the promoted 12 month period from the day you redeem the Offer` 並存，兩件事沒有混用。
- **#4 title 逐字等於研究紀錄、36 字／#6 description 以「（2026 年 9 月查證）」結尾** — 程式比對通過（description 本輪重寫，見裁示三）。
- **#19 summary 第 2 句、#33／#34 清單數字** — 中英兩版各清點一次都是 168／第 145／瑞士＋塔吉克；頁面沒有印總數。
- **#21 summary 第 4 句** — 12 個月、12-31、自動改收標準月費、不適用 Workspace for Education，四項都在條款上。
- **#44 學校配發帳戶出自條款 General 段** — `This offer is not available on your school-issued Workspace for Education account.`，不是註腳 5。
- **#51 本篇沒有誤植註腳 5 獨有的條件** — 全檔 grep：「最長 4 年」0 次、「僅限個人使用」0 次、「19.99」0 次。
- **#56「$165」無幣別、無「新台幣」** — 學生頁全文搜尋「新台幣」0 次；內容包出現 3 次都在否定句或 FAQ 題目裡。
- **#57 常見問題引句／#68 FAQ 1 的分寸** — 逐字命中；FAQ 1 只寫「不在排除名單」「在供應清單上」並帶「最終由 Google 認定」。
- **#64「140 多個市場」沒有完整名單／#69 FAQ 2** — 註腳 3 沒有連出清單；FAQ 2 的算法與條款一致。
- **#66 領取入口需登入** — 本輪同樣沒有登入、沒有重抓 `one.google.com/ai-student`，沿用研究紀錄 `unverified_or_excluded`。
- **#76 兩個內文 `article` 連結文字** — 今天再開檔比對：「Gemini Notebook 開學工具上線：公司、學校與個人帳號各有各的條件」與「免費版夠不夠用：ChatGPT、Claude、Gemini 付費方案比較（2026）」逐字相符；兩個結尾連結（#74、#75）一併比對，也逐字相符。

---

## 5. 本輪改的 7 處（內容包）＋2 處（研究紀錄）

### 協調者裁示

**裁示一：「給所有使用者」那句要帶上註腳 6、7 的縮限；把第二段砍到本批最低限度騰字。**

- 第一節第一段：`……並不限定使用者是不是學生。` → `……並不限定使用者是不是學生；但註腳 6、7 把前兩項限縮成行動版與網頁版上已登入的一般消費者帳戶，學校配發的 Google 帳戶與符合最低年齡要求的使用者要再等幾週，而且有用量上限。`
  來源：<https://blog.google/innovation-and-ai/products/gemini-app/student-offer-google-ai/>
  註腳 6（學生專區）與註腳 7（學習筆記本）是同一段話：`Available on mobile and web to all signed in consumer accounts in all Gemini app languages. Rolling out to school-issued Google accounts and users who meet minimum age requirements in the coming weeks. Usage limits apply.`
  第一輪的開放問題漏抄了句末的 `Usage limits apply.`，本輪補上。註腳 8（互動式視覺化）不同，一開始就含學校配發帳戶；註腳 9 只寫相容性、供應狀況與年齡限制各有不同——所以只縮限「前兩項」。
- 第二段：`以下內容於 2026 年 9 月 23 日查核 Google 官方公告、Google One 的《Google AI Plan Membership Student Offer Terms》優惠條款、支援頁的訂閱地區清單與台灣學生頁共四份官方文件；本站沒有登入任何 Google 帳戶，也沒有實際申請，這裡的功能說明與資格條件都是 Google 的說法。`
  → `以下內容於 2026 年 9 月 23 日查核 Google 官方公告、Google One 優惠條款、支援頁的訂閱地區清單與台灣學生頁四份官方文件。這一則在發布當時沒有排進本站的頭條批次，這一篇補上。`
  DELTA-4-4 第 2 條那一句因此從第一段搬到第二段（第一段同步刪去）。第二段 177 → 101 字；被刪的「沒有登入」「不構成建議」在結尾 callout 一字未動地保留著，沒有資訊流失。

**裁示二：明講兩個判準不同。** 第二節第二段末尾加一句：
`這份清單的判準是居住地，優惠條款的判準則是就讀的高等教育機構所在的國家或地區，兩者不是同一件事。`
來源：說明頁「您目前居住的國家/地區，必須支援 Google AI Plus 會員方案：」＋條款 `The subscription plan included in your Offer depends on the country or region of your eligible higher education institution.`（研究紀錄 `verified_facts` 第 20、23、37 條）。
只寫紀錄撐得住的範圍：沒有推論兩者不一致時怎麼算——四份頁面都沒有寫。

**裁示三：`description` 重寫。**
- 舊（151 字）：`……Google 宣布讓合格大專學生免費使用一年 Google AI 方案。這裡整理 Google One 優惠條款的資格與扣款規則、台灣是否列在供應名單上的查核過程，以及台灣學生頁自己前後矛盾的說法（2026 年 9 月查證）。`
- 新（186 字，在 120–200 內）：`2026 年 8 月 20 日（台北時間；官方頁面自印 8 月 19 日），Google 宣布合格大專學生可免費使用一年 Google AI 方案，美國拿 Google AI Pro、美國以外拿 Google AI Plus。台灣不在公告與優惠條款的排除地區內，也列在 Google One 說明頁的供應清單上，最終資格由 Google 認定（2026 年 9 月查證）。`
  沒有查證流水帳、沒有選件數；台灣仍寫成「不在排除名單、在供應清單上、最終由 Google 認定」，守住 `must_not_write` 第 2 條。

**裁示四：段落字數低於 3,000。** 2,958 → **2,994**（刪 102、加 141）。

### 本輪自己查出來的

6. **summary 第 1 句與改過的正文不一致** — `同日另開放四項 Gemini 學習功能。` → `同日起四項 Gemini 學習功能也開始鋪開。`
   來源：同上（`are rolling out today`）。第一輪把正文的「開放」判為過頭並改成「鋪開」，但 summary 這一句沒跟著改，`summary ⊆ 正文` 因此破了一個口。

7. **台灣學生頁最上方大標的引句漏字** — `最上方的大標則只寫「免付費使用學生方案 1 年」，沒有點出方案名稱。`
   → `最上方的大標則是「Google Gemini：免付費使用學生方案 1 年」，沒有點出方案名稱。`
   來源：<https://gemini.google/tw/students/?hl=zh-TW>（第一個 `h1` 逐字為「Google Gemini：免付費使用學生方案 1 年」）。「只寫『X』」配上不完整的引句，等於宣稱大標就是那幾個字。結論（沒有點出方案名稱）不變，因為 Google Gemini 是產品名不是方案名。

8. **研究紀錄 `verified_facts` 第 46 條的「主標」**（第一輪只記在報告裡、沒有訂正）— 改成「頁面下半的申請區塊（第三個 `h1`「準備好提升學習成效了嗎？」底下）寫……；頁面最上方的 `h1` 是「Google Gemini：免付費使用學生方案 1 年」」，`verbatim_quote` 未動（本來就逐字命中）。

9. **研究紀錄新增一條 `verified_facts`**：公告註腳 6、7 的原文與它對「所有 Gemini 應用程式使用者」的縮限，並註明註腳 8、9 條件不同。正文現在引用了這一條，紀錄必須撐得住它。`sources` 未增（`blog.google` 本來就在）。

---

## 6. 邊界再掃一次

- `topics` 是 `["ai","software","ai-news"]`，**沒有 `finance`**；全篇**只有一個** `info` callout，沒有投資免責段。
- 沒有訂閱、購買、升級或投資建議；沒有「值得／划算／該不該辦」；沒有跨廠商學生方案比較。
- 沒有推定台灣可用：能寫的兩件事（不在排除名單、在供應清單上）每次都帶「最終由 Google 自行認定」。
- 廠商宣稱都有歸因；否定句一律限縮成「這幾頁沒有寫」＋查核日。
- 不重寫站上既有 AI 文章：Notebook 那篇與 `ai-free-vs-paid-plans-2026` 各一句帶過並連過去，兩處連結文字逐字等於目標的 zh-TW `title`。
- 讀者優先：全篇「本文」0 次、「最近」「本週」「首次」「唯一」「從未」各 0 次（`日前` 的 1 次是「12 月 31 日前兌換」的字串重疊，不是時間副詞）。
- 歸因密度：開頭段 1 個歸因語（「Google 宣布」），其餘各段 ≤ 2。本輪新加的句子沒有引入新的歸因語（「註腳 6、7」接在同一段已經有的「同一篇公告」之後）。
- `summary` 的每個數字都逐字出現在正文；圖解 nodes 的 18／12／31 與 `hero_label` 也都在正文；FAQ 答案無網址。
- `checked_on` 2026-09-23 四處（四條 sources、研究紀錄、第二段、表格 caption）一致，本輪未動。

---

## 7. 留給協調者／站主的事

1. **字數只剩 6 字餘裕（2,994／3,000）。** 之後若要再補但書，最無損的騰字處是第五節第二段（領取入口需登入那三句）與結尾 callout 的重複，本輪沒有動。
2. **「美國走 Google AI Pro 那一套」在相鄰兩段各寫一次、FAQ 第五題再寫一次**，三處同義且都正確；要騰字時這是第二個無損處。
3. **台灣學生頁頁尾但書原文寫「2026年12月31日」（無空格）**，內容包依站上排版慣例加了空格；兩輪都未動。
4. **`one.google.com/ai-student` 需登入**，本輪同樣沒有登入、沒有重抓。
5. **說明頁 `?hl=zh-TW` 今天仍 302 到 `?hl=zh-Hant`**；`sources` 保留 `?hl=zh-TW`（讀者點進去拿到同一頁），兩輪一致。

---

## 8. 自檢

```
$ ./.venv/Scripts/python.exe ../../docs/news-2026-batch-4/check_article.py ai-news-gemini-student-offer-20260820
OK ai-news-gemini-student-offer-20260820 zh-TW paragraphs 2994
exit=0

$ ./.venv/Scripts/python.exe -m app.guides.pack_cli lint --kind life --slug ai-news-gemini-student-offer-20260820
  warning: raw_internal_url: zh-TW: 2 article link(s) as raw URLs; run `pack_cli relink` ...
  error: image_missing: zh-TW: /guides/ai-news-gemini-student-offer-20260820/hero.jpg
  error: image_missing: zh-TW: /guides/ai-news-gemini-student-offer-20260820/diagram-1.svg
exit=1
```

兩個 lint 類別都是出圖與 relink 之前的預期狀態。退出碼另寫在
`C:\Users\x8120\mokaair-work\news44\_tools\ai-news-gemini-student-offer-20260820-r2\exit-codes.txt`，
輔助腳本（重抓、抽正文、清單清點、引句比對、字數與密度稽核、套用改動）同一個目錄。

## 9. 結論

**ok**。第一輪的 9 處事實修正今天全部回一手來源復現，只有台灣學生頁大標那一句的引句要再修；
另外抓到第一輪漏掉的連帶項（summary 第 1 句）。四條協調者裁示全部照辦，段落字數 2,994、`description` 186 字，
自檢 `check_article.py` 為 OK。不需要第三輪。
