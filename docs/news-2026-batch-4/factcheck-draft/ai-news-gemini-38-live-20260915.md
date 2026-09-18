# 獨立查核：ai-news-gemini-38-live-20260915

查核代理：未參與撰稿。查核日 **2026-09-18**（文章的 `checked_on` 本來就是 2026-09-18，
今天重抓四條來源都讀到正文，所以不改）。
查核方式：`sources[]` 四條全部以 `curl -sL -A "Mokaair-editorial"` 重抓並讀 body，
28 條 `verbatim_quote` 用程式做連續字串比對（正規化彎引號與各種連字號後），
三份 Google 頁面的地區用語用**詞界**掃描而非子字串。
**沒有使用任何 `sources[]` 以外的新網址替文章補事實**，請求裡沒有任何 email、姓名或個人資料。

檢查的主張：96 條（title、description、18 段正文、summary 4 句、FAQ 6 題的答句、
表格 5 列與 caption、圖解 caption 與研究紀錄 `diagram` 四格、`hero_label`、callout；
`hero.alt` 依規格不查不改）。**內容包改了 29 處**（下面歸成 12 類），研究紀錄改了 11 處，
另有 4 件留給站主。

## 重抓結果（四條 sources 今天都可讀、零轉址、body 是正文）

| source | HTTP | bytes | 驗到的東西 |
| --- | --- | --- | --- |
| 模型發表文 blog.google/…/gemini-3-8-live-gemini-3-8-live-extended-thinking/ | 200 | 429,811 | `article:published_time` 2026-09-15、署名 `Sep 15, 2026`、正文首段的 `Updated September 17, 2026`、兩個定位句、`97 supported languages`、`rolling out starting today` 兩張可用性清單、三段影片圖說、四個評測數字、SynthID 段 |
| 開發者文 blog.google/…/build-real-time-voice-applications-gemini-audio/ | 200 | 391,560 | 同樣的 published_time／署名、`Key capabilities include` 五條、`97+ languages`、`Competitively priced at $0.005/min…$0.018/min` 與註腳 `Estimate based on $3/1M tokens…`、`a more streamlined alternative to cascaded architectures` |
| DeepMind 模型卡 deepmind.google/models/model-cards/gemini-3-8-audio/ | 200 | 148,728 | `Published 15 September 2026`、基於 Gemini 3 Pro、`up to 128K`／`64K token output`、兩份 Distribution 通路清單、`knowledge cutoff date is January 2025`、Frontier Safety 那段、Known Limitations |
| Gemini API 定價頁 ai.google.dev/gemini-api/docs/pricing | 200 | 243,411 | 三個代號同一價格區塊、$0.75／$4.50／$3.00／$12.00／$1.00 與 `or $0.005/min` 等每分鐘值、免費層級與 `Used to improve our products` Yes/No、grounding 的 5,000 與 $14、頁尾 `Last updated 2026-09-16 UTC.` |

定價頁今天是 243,411 bytes（研究紀錄寫 243,407）——活文件的 4 byte 漂移，內容相同。
28 條 `verbatim_quote` 只有一條原本搜尋不到（下面第 10 點），已修。

## 改掉的 29 處（歸成 12 類）

1. **把「發表文與模型卡互相矛盾」改成只在真正不一致的兩點上並陳**（第 2 節第 2、3 段、FAQ 第 3 題）。
   草稿寫「發表文的消費端說法是 3.8 Live 只到 Search Live、Extended Thinking **只到** Gemini Live；
   但模型卡把 Gemini App 與 Vertex AI 列成兩款共同通路」。**發表文自己就不是這樣寫的**：
   同一篇的第三段影片圖說是
   `Manage your day with Gemini 3.8 Live Extended Thinking in the Gemini app — ask for your Daily Brief…`，
   內文 `They also make speaking with Gemini across the Gemini app, Google Workspace, and Search more fluid…`
   與小節標題 `Across Google Workspace, Search, and the Gemini app, our Live models deliver…` 又各寫一次。
   Extended Thinking 在 Gemini app 這件事**兩份文件並不衝突**，寫成矛盾等於製造一個來源裡沒有的矛盾。
   真正只有模型卡寫的是「3.8 Live 也在 Gemini App」與「兩款都上 Google Cloud / Vertex AI」，
   現在正文與 FAQ 就只並陳這兩項，並保留「不替 Google 認定哪一份才準」。
2. **補上發表文自己的修訂戳**（第 2 節第 3 段）。頁面正文第一段是 Google 的斜體
   `<i>Updated September 17, 2026</i>`，而署名與兩個 `published_time` 仍是 2026-09-15。
   2026-09-16 的批次查核記下的小節標題沒有 `and the Gemini app`——這一頁在兩次查核之間被改過。
   文章寫「發表文頂端另標示曾於 9 月 17 日更新」，事件日仍用 9/15，`event_date_basis` 明寫排除這個戳記。
3. **地區的否定句超出範圍**（第 3 節第 1 段、FAQ 第 1 題、callout）。草稿寫
   「三份文件全文檢索，沒有找到任何國家、地區或市場的**名稱**」。
   blog.google 的頁尾國別選單印著約三十個國家名，**包含「台灣 (中文)」**，這句話在字串層級是錯的。
   詞界掃描真正為 0 的是 region／country／countries／market／worldwide／globally／United States／Taiwan，
   `global` 的四個命中全是版面字樣（`Global network`、`Global (English)`、`Reach global audiences`）。
   已改成「說明可用性時只點名產品與訂閱身分，沒有一句寫出開放的國家、地區或市場」。
   （順帶：批次修正清單說「唯一的 `market` 命中在 `marketing toolkits` 裡」，那是子字串造成的，
   詞界比對下 `market` 是 0 次。）
4. **訂閱門檻與狀態逐項核對，兩處收緊**（表格）。四格「即日開放」改成「即日起推出」——
   Google 寫的是 `rolling out starting today`，而本文第 3 節整節就在講「開始不等於完成」，
   表格原本自己拆了自己的台。Workspace 列的「Gmail 與 Keep **全訂閱者**」語意含糊，
   原文是 `all Google AI subscribers in Gmail and Keep`，已改成「限 Google AI 訂閱者」；
   「文件」那一側原文是 `Google AI Pro and Ultra subscribers in Workspace in Docs`，維持不合併。
   一般使用者（Extended Thinking）列補上 Gemini App，依第 1 點的圖說。
5. **語言數字的框架**（第 3 節第 3 段、FAQ 第 6 題）。草稿把 97 與 97+ 寫成「也有類似狀況」
   （跟地區未說明並列）並說「不擅自挑一個當成唯一答案」，讀起來像兩份官方文件互相打架。
   97（模型發表文，講 3.8 Live 對話中自動切換）與 97+（開發者文的能力條列）**並不互相否定**。
   已改成照原樣並列、寫明各自出處與各自講的東西，並在 FAQ 補上「這是模型聽得懂、說得出的語言，
   不等於各介面的介面語言或開放地區」。FAQ 的「Google 沒有公布清單」也收成
   「本文查核的四份文件都沒有列出語言名稱」。
6. **刪掉文章自己推測的成本機制**（第 4 節第 1 段、FAQ 第 2 題）。草稿寫 3.8 Live「為規模與成本效率打造」
   「**指的應是**它平常用掉的推理 token 較少」，FAQ 寫「差別是 Extended Thinking 的推理過程
   **通常會用掉更多 token**」。**Google 沒有印這個比較。** 定價頁只寫輸出價格
   `Output price (including thinking tokens)`。兩處都改成定價頁真正印的事。
   同段的「**前一代** gemini-3.1-flash-live-preview」改成「較早的」，並補上定價頁沒有寫取代或停用
   （研究紀錄 `not_said` 第 10 條原本就記對了，文章卻自己加了世代關係）。
7. **評測數字補回主詞與比較對象**（第 5 節第 1 段）。草稿把四個數字寫成沒有主詞的「排行榜名次」。
   原文 82.6／68.6%／35.1%／97.7% 全部是 **Extended Thinking** 的成績，
   `second place in the Speech Agent Arena` 才是 3.8 Live；
   Speech to Speech Quality Index 是 **Artificial Analysis** 的、τ-Voice-banking 是 **Sierra** 的。
   已逐一補回，`「Google 表示」` 的歸因與「9 月 15 日的快照」保留。
8. **3.7 Flash 不是這兩款的「上一代」**（第 5 節第 2 段）。模型卡只寫
   `We evaluated Gemini 3.7 Flash … based on Gemini 3.7 Flash results`，
   沒有說它是這兩款的前一代（站上另有 `ai-news-gemini-38-flash-20260902`，而定價頁上較早的 live 模型
   是 3.1 Flash Live Preview）。已改成「Google 依前沿安全框架評估的對象是 Gemini 3.7 Flash」，
   結論仍寫成推論、不是「通過」。
9. **三處把來源的範圍寫寬或寫窄**：
   （a）首段「兩款模型…**分別**以模型發表文與開發者文說明」——兩篇都在寫兩款模型，已改成「兩篇公告」。
   （b）第 1 節第 2 段「開發者文稱**這**是『比串接式架構更精簡的替代方案』」——原文主詞是
   `These models`（兩款），已改成「把兩款模型合稱為」。
   （c）第 1 節第 3 段「另外**列出五項**能力」——原文是 `Key capabilities include`，
   已改成「條列主要能力，用的是『包括』」，不把非窮舉清單寫成全清單、也不把自己數的 5 當成事實。
   同段 SynthID 從無歸因的事實改成 `發表文說 Google AI 產品生成的語音都會加上…`
   （原文是 `All audio generated by our AI products`）。
10. **研究紀錄第 9 條的 `verbatim_quote` 是拼裝品**。原本寫
    `Gemini 3.8 Live is distributed in the following channels; respective documentation shared in line: Gemini API, Gemini App, …`，
    但頁面上那句話在 `<p>` 裡就結束了，五個通路名是五個 `<li>` 連結。
    已截到真正搜尋得到的 `…shared in line:`，通路清單改寫進 `fact`。
    另外第 6 條刪掉 `everyone else gets it **only** in Search Live` 的 only、
    第 12 條的 `is_vendor_claim` 由 false 改 true（同一句帶著 `Competitively priced` 與
    `industry-leading performance` 兩個廠商修辭）。
11. **兩個小的規格對齊**：第 2 節標題「**五**種身分」與圖解／圖說／`editorial_brief` 的「四種身分」打架，
    已改成四種（表格 5 列是因為一般使用者拆成兩款模型各一列）；
    第 4 節「輸出音訊與文字，**上限** 64K token」——模型卡只在情境窗那一側寫 `up to`，
    輸出那側是 `with 64K token output`，已拿掉「上限」。
    第 3 節第 1 段的「**Workspace 兩個場景**」也不對：`coming soon` 的兩項是
    Customer Experience（兩款都有）與 Workspace 企業用戶端（只有 Extended Thinking），已改寫。
12. **description 與字數**。description 把知識截止日寫成「Google 至今沒有說明的…限制」，
    但知識截止日是模型卡明寫的，已改。所有改動後 zh-TW 段落 **2,984 字**（上限 3,000），
    為了容納上面的但書，從第 3 節第 2 段與第 5 節第 3 段的重複敘述各精簡了一些，
    **沒有刪掉任何一個限定詞或但書**。

## 查過而且正確的部分（沒有動）

- **`sources[]` 可以出刊**：四條全部 HTTP 200、零轉址、body 是正文，
  文章每一條事實都追得到這四條之一，沒有任何事實掛在新聞媒體、整合站或搜尋摘要上。
  `checked_on` 2026-09-18 在內容包每條 source、研究紀錄、第二段、表格 caption、圖解 caption 五處一致。
- **事件日沒有混用**：`article:published_time=2026-09-15`、`published_time=2026-09-15T17:00:00+00:00`、
  可見署名 `Sep 15, 2026`、模型卡 `Published 15 September 2026`；slug 尾碼與 `news_date` 都是 2026-09-15。
  定價頁頁尾的 `Last updated 2026-09-16 UTC` 與發表文的 9/17 更新戳都沒有被當成事件日。
- **可用性清單逐字重現**：`For developers` / `For enterprises`（private preview + coming soon）/
  `For everyone`，兩款各一組；文件與 Gmail／Keep 的訂閱門檻沒有被合併。
- **價格逐格重對**：0.75／4.50／3.00／12.00／1.00 美元（每百萬 token）、每分鐘 0.005／0.018／0.002、
  免費層級的 `Free of charge` 與 `Used to improve our products` 的 Yes/No 分野、
  grounding 的 5,000 次與每 1,000 次 14 美元，以及「一次請求**可能**觸發不只一次查詢」的 may。
  兩個模型代號逐字印在定價頁上。
- **模型卡規格**：以 Gemini 3 Pro 為基礎、輸入 audio/images/video/text、`up to 128K`、
  `knowledge cutoff date is January 2025`、已知限制的 `may` 與 `occasional` 都保留。
- **界線**：全文沒有購買或升級建議、沒有推薦式比價、沒有「值得買／該升級」式結論；
  能力、名次與價格都有歸因，沒有本站實測的暗示；分批開放與私人預覽的狀態每一處都寫了。
  **沒有任何一句讓讀者以為台灣帳號或繁體中文介面已經支援**，反而在正文、FAQ 與 callout 三處
  寫明官方未說明開放地區。AI 篇只有一個 callout，沒有投資免責段落。
- **三份刻意排除的文件沒有殘留**：全文搜不到 `pass@1`、`gemini-3.8-live-preview`、`tau-cubed`、
  `thinking_level`、`NON_BLOCKING`、`interaction_status`、`85+` 或 `2026-08-26`，
  也完全沒有提到 Gemini 3.5 Transcribe。撰稿者的排除決定與 `unverified_or_excluded` 一致。
- **兩篇只有單向連結**（開發者文 → 模型發表文 1 次，反向 0 次），
  文章沒有拿互相連結當合併成一篇的理由，合乎修正清單 must_fix 1。
- **倉庫面**：`display_order` 159 與 `check_article.py` 的 `RELATED` 順序一致、批次內無重號；
  topics `ai`/`software`/`ai-news` 合法；表格 4 欄 5 列、每節 2–4 段、summary 在第一個 heading 前、
  FAQ 6 題純文字無連結；`hero_label`「新語音模型，先看能不能用」12 字。

## 留給站主的 4 件事

1. **`check_article.py` 仍是 FAIL，只剩兩條連結文字，兩條都在規格允許範圍。**
   索引 `ai-news-2026-january-september-index` 的 zh-TW title 目前還是
   「2026 年 AI 新聞總整理：1 月 1 日至 9 月 14 日的重點與生活應用」，本文的連結文字寫的是改名後的
   「1 月至 9 月」；第二個連結指向同批的 `ai-news-gpt-live-1-api-20260910`，那篇現在的 title 是
   「GPT-Live 1 開放 API：電話客服能不能接、聲音是誰的、會不會錄音」，與本文的連結文字不同。
   依規格兩個結尾連結未動，等索引改名與 `align_links.py` 一起處理。
2. **模型發表文是活文件，而且已經被 Google 改過一次**（正文自帶 `Updated September 17, 2026`，
   小節標題在 09-16→09-18 之間多了 `and the Gemini app`）。
   出刊前建議再抓一次那一頁，確認第 2 節第 2、3 段引用的三種寫法還在；
   若 Google 把可用性清單本身也改掉，那兩段要跟著改。
3. **圖解 SVG 尚未繪製。** 研究紀錄的四格已改成「API 與 AI Studio 當天推出」與「文件限 Pro 與 Ultra」，
   畫的時候照這個版本，不要沿用舊的「當天開放」。圖上沒有任何數字。
4. **τ 這個希臘字母要保持原樣。** Google 自己在部落格寫 `τ-Voice-banking`、
   在評測 PDF 寫 `tau-cubed-Bench`，五語譯文與圖像都不要替 Google 統一名稱。

## 結論

`needs_second_round`：29 處已改，其中第 1 點動到了整篇的骨幹論述
（兩份文件到底哪裡不一致），第 3、6、7 點各推翻一條寫進正文的事實。
文章本身現在每一句都指得到四條來源之一，界線與歸因也都過了，
但依規格「改到骨幹論述」要再送一輪，請對第 2 節第 2、3 段與 FAQ 第 3 題逐句再查一次。

## 第二輪

第二輪查核代理：沒有參與撰稿，也沒有參與第一輪。查核日 **2026-09-18**（`checked_on`
本來就是 2026-09-18，四條來源今天仍讀得到正文，依規格不改）。

四條 `sources[]` 今天重抓一次（`curl -sL -A "Mokaair-editorial"`，請求的 UA、標頭、
查詢字串、表單裡沒有任何 email、姓名或個人資料）。**三份 HTML 與第一輪抓到的檔案逐位元組相同**
（`cmp`），定價頁抽出的純文字也相同——也就是說第一輪引用的每一句今天都還在頁面上，
可以就地覆核而不是拿舊快照比對。

| source | HTTP | bytes | 轉址 | body |
| --- | --- | --- | --- | --- |
| 模型發表文 blog.google/…/gemini-3-8-live-… | 200 | 429,811 | 0 | 正文（與第一輪 byte-identical） |
| 開發者文 blog.google/…/build-real-time-voice-applications-gemini-audio/ | 200 | 391,560 | 0 | 正文（byte-identical） |
| DeepMind 模型卡 deepmind.google/models/model-cards/gemini-3-8-audio/ | 200 | 148,728 | 0 | 正文（byte-identical） |
| Gemini API 定價頁 ai.google.dev/gemini-api/docs/pricing | 200 | 243,407 | 0 | 正文（純文字與第一輪相同；第一輪報告寫的 243,411 與研究紀錄寫的 243,407 差 4 byte，今天讀到 243,407） |

覆核 66 條主張（第一輪改動過的 29 處與新寫進去的每一句、18 段正文、summary 4 句、
FAQ 6 題答句、表格 5 列與 caption、callout、圖解四格與 title／caption、`hero_label`、
title、description；`hero.alt` 依規格不查不改），**30 條 `verbatim_quote` 用程式做連續字串比對**
（NFKC＋彎引號／連字號／空白正規化後）——**30/30 命中**，沒有一條是拼裝品，
也沒有含 `...`／`|` 的跨段落引文（第 30 條是 href 裡的 slug，那條事實本身就寫明是對 HTML 做的 grep）。
**內容包改 9 處、研究紀錄改 9 處**，另有 2 件留給站主。

### 改掉的 9 處（內容包）

1. **FAQ 第 3 題「這兩項只有模型卡寫」是錯的否定句（指派疑點 1）。**
   第一輪把矛盾收斂到「『3.8 Live 也在 Gemini App』與『兩款都上 Vertex AI』這兩項只有模型卡寫」。
   逐句回原文的結果：**第一項站不住**。發表文自己的小節標題是
   `Across Google Workspace, Search, and the Gemini app, our Live models deliver more intuitive, collaborative experiences`，
   第二段內文是 `They also make speaking with Gemini across the Gemini app, Google Workspace, and Search more fluid`——
   `our Live models` 與 `They` 都指兩款模型，**沒有把 3.8 Live 排除在 Gemini app 之外**。
   換句話說，第一輪為了不製造假矛盾而收斂，卻在收斂時寫出另一個過寬的否定句。
   已改成限定版本：發表文**那張可用性清單**沒有把 Gemini App 算給 3.8 Live。
   第二項（Vertex AI）覆核無誤：詞界掃描下 `Vertex AI` 在兩篇部落格的可讀內文 0 次、
   開發者文 HTML 0 次，模型發表文 HTML 只出現 2 次且都在同一個 href
   （`https://console.cloud.google.com/vertex-ai/studio/multimodal-live`，「Gemini Enterprise」那個連結）。
   模型卡原句也逐字確認：`Gemini 3.8 Live is distributed in the following channels; respective documentation shared in line:`
   後面五個 `<li>` 是 Gemini API、Gemini App、Google AI Studio、Google Cloud / Vertex AI、Google Search Live；
   Extended Thinking 那組是 Gemini App、Gemini API、Google AI Studio、Google Cloud / Vertex AI、
   Google Workspace (Gmail, Docs, and Keep)。
2. **第 2 節第 2 段補一句，讓 FAQ 有正文可依。** 因為「FAQ 答案 ⊆ 正文」，
   上面那個限定說法必須在正文出現過，已在圖說那一句後面加「內文與小節標題也把兩款模型合稱寫進去」。
3. **第 2 節第 3 段「模型卡列的通路更寬」不成立。** 「更寬」在字面上主張模型卡涵蓋發表文，
   但**模型卡的 Distribution 沒有 Gemini Enterprise**，而發表文的可用性清單有
   （`For enterprises: In private preview in Gemini Enterprise…`）。兩份清單互有出入、誰也沒涵蓋誰。
   已改成「模型卡的通路清單不同」。（反向缺口因字數已滿沒有寫進正文，記在研究紀錄與 must_not_write。）
4. **callout 的地區否定句範圍過寬（指派疑點 3）。** 第一輪把「三份文件沒有任何國家名稱」收窄成
   「說明可用性時沒有一句寫出開放地區」，這個修法在正文與 FAQ 第 1 題是對的（兩處都寫「三份文件」），
   但 **callout 寫的是「四份文件」，而第一輪只掃了三份**。補掃第四份（定價頁）的結果：
   `country`／`countries`／`market`／`worldwide`／`globally`／`global`／`United States`／`Taiwan` 皆 0，
   但 `regions` 有兩次——導覽連結 `Available regions`，以及
   `Google AI Studio usage is free of charge in all available regions. See Billing FAQs for details.`。
   定價頁確實沒有點名任何地區，所以否定句仍成立，但它**不是對地區隻字未提**。
   callout 已改成「四份文件在說明可用性時，都沒有寫出開放的國家、地區或市場」，
   並把定價頁那句「在所有可用地區」寫進括號裡，讓讀者看得到這個否定句的邊界在哪。
5. **summary 第 2 句比正文強。** 原本寫「開發者**即日起可以**透過 Gemini API 與 Google AI Studio
   **使用**兩款模型」，但正文與 Google 寫的都是 `rolling out starting today`（即日起開始推出），
   而第 3 節整節就在講「開始不等於完成」——摘要自己先把結論推翻了。
   已改成照 Google 的措辭：「Google 對兩款模型都寫『即日起開始推出』，開發者這一側的通路是…」。
6. **grounding 的 5,000 次額度接錯層級（第 4 節第 3 段、FAQ 第 5 題）。**
   定價頁上 `Grounding with Google Search *` 那一列，**免費層級那一格只寫 `Supported`**，
   `5,000 free search requests per month (shared across all Gemini 3.x models), then $14 per 1,000 requests.`
   印在**付費層級**那一格。原文兩處都把這個額度接在「定價頁還有免費層級…」之後，讀起來像免費層級的權益。
   兩處都補上層級，FAQ 另外寫明免費層級那一欄只寫「支援」。
7. **第 3 節第 1 段結尾「也就是說，官方未說明開放地區」是同段前一句的覆述**，
   前一句已經寫了「沒有一句寫出開放的國家、地區或市場」。為了騰出上面兩處但書的字數，
   改成「本文因此無法判斷台灣帳號是否已在可用範圍」——**刪的是重複敘述，不是限定詞**。
8. **第 3 節第 2 段「使用者無法從官方文件判斷」縮成「使用者無從判斷」**（同段前面已經說明是官方文件沒寫）。
9. **FAQ 第 5 題補上免費層級那一欄的實際字樣**（見第 6 點）。

### 研究紀錄改的 9 處

`verified_facts` 第 9 條（改掉「Gemini App for 3.8 Live 只有模型卡寫」的敘述，改記成限定版本並補上
Gemini Enterprise 的反向缺口）、第 22 條（`fact` 原本寫 `outputs are audio and text up to 64K tokens`，
模型卡原句是 `Audio and text, with 64K token output`，`up to` 只印在情境窗那一側——第一輪已經改對正文，
但紀錄自己還留著這個 `up to`）；`not_said` 第 1 條（補上定價頁的補掃結果與那句
`free of charge in all available regions`，並寫明否定句只能寫成「沒有點名地區」而不是「隻字未提」）；
`must_not_write` 第 6 條（把「只有模型卡寫」這個寫法列為禁止，並加上「不可寫成模型卡列的通路更寬」）；
`diagram` 的 title 與兩格（見下）；`left_for_the_owner` 第 3 條（改寫成新版圖解規格）；
`factcheck.second_round`（新增）。

**圖解（指派疑點 4）**：三處與正文／表格對不上，已改，SVG 尚未繪製所以現在改不影響任何產出。
- title `3.8 Live 的四道門` → `兩款模型的四道門`。四道門講的是兩款模型，掛在其中一款名下是錯的。
- 開發者格 `API 與 AI Studio 當天推出` → `API 與 AI Studio 即日起推出`，與正文引號、表格四列的狀態詞一致。
- 企業格 `私人預覽，另有 Vertex AI` → `Gemini Enterprise 私人預覽`。模型卡把 Vertex AI 列給**兩款模型**、
  沒有對應到任何身分；放進「企業」那一格等於憑發表文那個 href 把它寫成企業專屬的路，
  而研究紀錄自己就寫過「那是網址不是它點名的通路」。Vertex AI 仍由正文、表格 caption 與 FAQ 承接。

### 覆核過而且正確（沒有動）

- **四個成績的主詞全部是 Extended Thinking（指派疑點 2）**，第一輪修對了。原句：
  `Gemini 3.8 Live Extended Thinking … capturing the #1 overall spot on Artificial Analysis' Speech to Speech Quality Index (82.6),
  and leads in agentic task completion with 68.6% on τ-Voice and 35.1% on Sierra's τ-Voice-banking benchmark.
  It also provides strong reasoning capabilities, scoring 97.7% on Big Bench Audio…`；
  `securing a second place in the Speech Agent Arena` 才是 3.8 Live。
  指數屬 Artificial Analysis、banking 基準屬 Sierra，文章都寫對；`τ-Voice` 這個基準原文沒有註明擁有者，
  文章也沒有替它加。**這五個數字與兩個名次只出現在第 5 節第 1 段一處**——表格、摘要、FAQ、圖解都沒有，
  不可能不一致。HTML 裡是 `<i>τ</i>-Voice` 與 `<i>τ</i>-Voice-banking`，文章照原樣；`tau-cubed` 不在這四份來源上。
- **地區（指派疑點 3 的另一半）**：三份 Google 頁面詞界掃描 `region`／`regions`／`country`／`countries`／
  `market`／`markets`／`worldwide`／`globally`／`United States`／`Taiwan` 全部 0；`global` 的命中是
  `Global network`、`Global (English)` 與開發者文的 `Reach global audiences`。頁尾國別選單 30 個項目、
  含「台灣 (中文)」——所以第一輪把「沒有任何國家名稱」改掉是對的。**全文沒有一句讓讀者以為台灣或繁體中文已支援**：
  「台灣」三次都在「無法判斷／無法代替 Google 確認」的句子裡，「繁體」「中文」在內容包 0 次，
  FAQ 第 6 題還特別寫明 97／97+ 講的是模型聽說的語言、不等於介面語言或開放地區。
- **方案門檻與狀態詞四處一致（指派疑點 4）**：`Google AI Pro and Ultra subscribers in Workspace in Docs,
  and all Google AI subscribers in Gmail and Keep` 在正文、表格、FAQ 第 2 題三處都沒有被合併；
  `rolling out starting today` 在正文引號、表格四列、圖解開發者格一致寫成即日起（開始）推出，不是「開放」；
  private preview 與兩處 `coming soon`（Customer Experience 兩款都有、Google Workspace business customers
  只有 Extended Thinking）在正文與表格一致，都寫明沒有時間表。
- **發表文的更新標記（指派疑點 5）**：今天（2026-09-18）讀到的仍是正文第一段的斜體
  `Updated September 17, 2026`，署名仍是 `Sep 15, 2026`，兩個 `published_time` 仍是 `2026-09-15`；
  整份 HTML 與第一輪抓到的版本**逐位元組相同**，兩份可用性清單、三段圖說、小節標題、四個評測數字
  都沒有再被改過。文章寫的「發表文頂端另標示曾於 9 月 17 日更新」因此**不需要改**。
  定價頁頁尾今天仍是 `Last updated 2026-09-16 UTC.`。
- **價格逐格再對**：3.8 Live 區塊付費層級 `$0.75 (text)`／`$3.00 or $0.005/min (audio)`／
  `$1.00 or $0.002/min (image/video)`，輸出（`including thinking tokens`）`$4.50 (text)`／
  `$12.00 or $0.018/min (audio)`；免費層級輸入輸出都是 `Free of charge`；
  `Used to improve our products` 的 Yes/No；`may result in one or more queries` 的 may 保留。
  **這個區塊沒有頁面上其他區塊那種「到 2026-12-31 前 X、2027-01-01 起 Y」的分期價**
  （例如 Batch 那一列就有），文章寫成單一組價格是對的；也確認這個區塊沒有 Live Translate／
  Transcribe Live 那種每分鐘換算的星號註腳，只有開發者文的註腳說是估計值。
- **模型卡**：`Gemini 3.8 Audio is based on Gemini 3 Pro`、`token context window of up to 128K`、
  `Audio and text, with 64K token output`、`knowledge cutoff date is January 2025`、
  前沿安全是對 `Gemini 3.7 Flash` 做的且結論是 `not likely to reach any T/CCLs`、
  已知限制的 `may` 與 `occasional` 都在，文章的「推論不是評估」寫法與原文一致
  （原文自己寫 `based on Gemini 3.7 Flash results, we are confident that…`）。
- **界線**：沒有購買、升級或投資建議（「建議」兩次都在「不構成使用或購買建議」），沒有推薦式比價，
  沒有「值得買／划算／便宜」，沒有本站實測的暗示；不帶 `finance` 主題、只有一個一般 callout、
  沒有投資免責段落；沒有提到 3.5 Transcribe、3.8 Flash 或站上既有 Gemini 文章的內容，不重寫也不矛盾。
- **但書沒有被字數擠掉**：`up to` 只留在情境窗那一側、`Key capabilities include` 沒有寫成全清單、
  每分鐘價格仍標示為換算估計值、前沿安全仍寫成推論、3.1 Flash Live Preview 仍只寫「較早的」
  且註明定價頁沒有寫取代或停用。第二輪的改動全部是把話說窄或補上出處，**沒有刪任何一個限定詞**；
  zh-TW 段落 2,984 → **2,992**（上限 3,000）。

### 留給站主的 2 件事（第一輪的 4 件，其中 2 件已由本輪處理）

1. **`check_article.py` 仍是 FAIL，只剩兩條連結文字，兩條都在規格允許範圍**，
   等索引改名與 `align_links.py` 一起處理（與第一輪相同，兩個結尾連結未動）。
2. **τ 這個希臘字母在五語譯文與圖像裡要保持原樣**；Google 自己在部落格寫 `τ-Voice-banking`、
   在評測 PDF 寫 `tau-cubed-Bench`，不要替 Google 統一名稱。
   （第一輪的第 2 件「出刊前再抓一次發表文」：本輪已抓，頁面與第一輪逐位元組相同，暫時不必再抓；
   第 3 件「圖解照研究紀錄的版本畫」：本輪又改了三處，請以研究紀錄現在的四格與 title 為準。）

### 結論

`ok`。第一輪動到的骨幹論述（兩份文件到底哪裡不一致）已逐句回原文覆核：
方向是對的，但收斂時寫出了一個過寬的否定句（第 1 點）與一個站不住的「更寬」（第 3 點），
兩處都已改成來源撐得住的限定說法，並在正文補了依據。
文章現在每一句都指得到四條來源之一，否定句都有查法與範圍，界線與歸因也都過了。
