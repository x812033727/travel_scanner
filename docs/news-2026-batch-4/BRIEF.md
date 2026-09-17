# 撰稿規格：2026 年新聞批次 4（AI、科技、幣圈）

給研究／撰稿、查核與翻譯代理的**共同**規則。三個垂直各有一份補充規格，**都要讀**：

- 幣圈：[`crypto.md`](crypto.md) ← 法遵限制最多，不讀會寫出不能刊的東西
- 科技（非 AI）：[`tech.md`](tech.md)
- AI：[`ai.md`](ai.md)

前三批的工作區是 `docs/ai-news-2026-09`、`docs/ai-news-2026-ytd`、`docs/ai-news-2026-09-mid`。
這份規格以 [`docs/ai-news-2026-09-mid/BRIEF.md`](../ai-news-2026-09-mid/BRIEF.md) 為底本，
**下面標「批次 4 新增」的才是這次才有的規則**，其餘沿用。

格式範本：`apps/api/app/guides/content/ai-news-siri-ai-ios-27-20260914.json`。

## 查證規則（最重要）

- **只用一手來源**：廠商官網公告、官方部落格、說明中心／支援頁、API 文件、
  主管機關公告與法規原文、標準組織規格、當事人本人發表的原文。
  新聞媒體與整合站可以拿來找線索與交叉確認日期，但文章的 `sources`
  **只放一手來源**（至少 2 條、最多 4 條）。
- 每一個日期、價格、百分比、方案名、地區、語言、機型、條號，
  都要能指到一條 source 的原文。查不到的寫「官方未說明」或不寫。
- 廠商宣稱的能力、評測數字一律寫成「OpenAI 表示／Apple 說明／金管會指出」，不寫成事實；
  本站沒有實測，不可寫「我們試用」。
- 分批開放、beta、預覽、地區限制、方案限制分開寫，不把美國首發推定成台灣帳號都能用。
- 生活情境要標明是編輯設計的例子。
- 查核日 `checked_on` 一律寫**實際查證當天**，並寫進 `sources[].checked_on` 與研究紀錄。

### 撰稿模型的知識截止日早於這段期間

**這是批次 4 最大的風險，不是形式問題。** 這批涵蓋 2026-01-01 至今，
其中幣圈與非 AI 科技完全在訓練資料之外。**每一個事實都要現查**，
不准憑印象寫下任何日期、法條號、版本號、產品名或機構名。

實例：本規格撰寫時，查證者為了確認台灣《虛擬資產服務法》而**自行猜測**了
全國法規資料庫的 `pcode=G0380347`，結果是一個不存在的頁面。
猜識別碼、猜網址、猜條號都屬於捏造，即使猜對也一樣。
**先搜尋，拿到官方頁的真實網址，再抓那一頁。**

研究紀錄的 `unverified_or_excluded` 是這件事的防線：它逼撰稿者寫下
「我看到但查不到一手來源、所以沒寫」的東西。**`unverified_or_excluded` 空白的文章要當成可疑，不是乾淨。**

### 網路請求

- **不得在任何請求（包含 User-Agent、查詢字串、表單）放入使用者的 email 或任何個人資料。**
- 需要自訂 User-Agent 時一律用 `Mokaair-editorial`。
- 被 403／451 擋時（實測 `openai.com`、`sec.gov` 會擋），換同一官方站的其他頁、
  官方 RSS、或各國 newsroom（如 `apple.com/<國家>/newsroom`）。**不要改用整合站充數。**
  查到的事實如果只存在於被擋的頁面後面，那就不寫。

### 先找官方 feed，再抓網頁

廠商的官方 RSS/Atom **比抓網頁可靠**，而且日期是官方給的，不必從版面猜。
2026-09-16 實測：`openai.com` 的網頁對 `curl` 與 WebFetch 都回 **403**，
但 **`https://openai.com/news/rss.xml` 回 200**，裡面 1,193 筆帶 `pubDate` 的項目。

可用的 feed 與格式差異整理在
[`candidates-tech-and-ai.md`](candidates-tech-and-ai.md) 開頭那張表
（注意 Apple Newsroom 是 **Atom**：`<entry>`／`<updated>`，不是 `<item>`／`<pubDate>`；
Anthropic 兩個常見位址都 404，沒有 feed）。
沒有 feed 的主管機關，找它的結構化管道：美國的 Federal Register 有公開 API，
是 `sec.gov` 被 403 擋掉時的官方刊登管道。

**feed 給的是日期與標題，不是內容。** 開稿時仍要讀該篇原文，
`sources` 放的是文章頁的網址，不是 feed 的網址。

**兩個實測踩到的陷阱，抓 feed 時一定要檢查：**

1. **HTTP 200 不代表拿到 feed。** `https://news.samsung.com/global/feed` 回 200，
   但 body 是 Akamai 的 `<TITLE>Access Denied</TITLE>`。只看狀態碼會把一頁拒絕當成資料。
2. **feed 可能是死的。** `https://www.usb.org/rss.xml` 回 200、格式正確、有 10 筆 item，
   但最新一筆是 **2018-07-31**。拿它當「這家沒有新消息」的依據會錯。

所以判斷「拿到 feed 了嗎」要看兩件事：**`<item>`／`<entry>` 的數量**，
以及**最新一筆的日期**。兩者都合理才算拿到，否則要當成取得失敗、換管道。

3. **官方標題裡有看不見的字元。** Apple Developer 的
   `Update: New domain for Sign in with Apple` 實際上是
   `Sign\xa0in\xa0with\xa0Apple`（不斷行空格）；OpenAI 的
   `Build more natural voice experiences with GPT‑Live‑1 in the API` 用的是
   非 ASCII 的連字號 `‑`（U+2011）。**用純 ASCII 的字串去比對會查無此項**，
   而 `check_article.py` 要求 link 的 `text` 等於目標文章的 title，
   所以抄標題時要連這些字元一起抄，不要自己打一遍。

## 內容包格式

檔案 `apps/api/app/guides/content/<slug>.json`。

slug 一律 `<vertical>-news-<topic>-<YYYYMMDD>`，日期是**事件日**，不是發布日
（批次 3 把 `...-20260709` 改名為 `...-20260708` 就是因為官方發布日是 7/8）。

`topics`：AI 用 `["ai", <橫向主題>, "ai-news"]`；科技用 `["tech", "tech-news"]`
（可再加 `gadgets`／`software`）；幣圈用 `["finance", "crypto"]`。
`destination_id` 一律 `null`。`kind` 一律 `life`。

**`news_date` 必填（2026-09-16 新增，PR #537）。** 內容包多了一個頂層欄位：

```json
"news_date": "2026-09-14"
```

值就是**事件日**，和 slug 尾巴的日期一致。它不是發布日、也不是更新日。
`/life` 首頁的「最新新聞」與新聞主題頁用 `sort=news` 依這個欄位由新到舊排，
**沒有 `news_date` 的文章會被排到最後、而且不會出現在首頁那 20 條裡**。
既有 38 篇 `ai-news-*-YYYYMMDD` 已經由 #537 補齊，測試會擋住之後忘記帶的包——
所以漏了會直接 CI 紅，不是只是排序不好看。

### blocks 的順序（批次 4 新增了兩個區塊）

1. `paragraph`：事件是什麼（第一句寫出事件日期，例如「2026 年 6 月 30 日」）。
2. `paragraph`：寫「本文於 YYYY 年 M 月 D 日查核」，說明開放狀態／本文不做實測的界線。
3. **`summary`（批次 4 新增，必帶）** — 見下一節。
4. 五個 `{"type":"heading","level":2,"text":"…"}` 小節，每節 2–4 個 paragraph。
5. 第 2 節結尾放 `table`：3–4 欄、3–6 列、**最多 4 欄**、儲存格短（手機會擠），
   `caption` 寫查核日。
6. 第 3 節結尾放 `image` 圖解：`/guides/<slug>/diagram-1.svg`。
7. **`faq`（批次 4 新增，必帶）** — 見下一節。
8. `callout`：本文的提醒。**幣圈另外還要一個免責 callout，見 `crypto.md`。**
9. 兩個 link：第一個是本垂直的索引，第二個是一則相關新聞。

**`summary` 必須在第一個 `heading` 之前**，這是 schema 的硬性驗證
（`GuideDocument.one_summary_one_faq`），放錯位置整份文件會被拒絕。

### 篇幅與用語

- 所有 paragraph 的 text 串起來（含標點）**1,800–3,000 字**；title ≤ 60 字；description 120–200 字。
- 台灣繁體中文與台灣用語（「使用者」「帳號」「影片」「軟體」），**不可出現簡體字**。
- 不要列表、不要 Markdown、不要 emoji。
- 語氣平實、具體、不聳動，不下投資或醫療建議。
- **不要重寫既有文章講過的事。** 動筆前先讀本垂直的索引與既有篇目。

## 批次 4 新增：`summary` 與 `faq`（SEO／AEO／GEO）

站上 845 篇 life 內容包裡只有 5 篇有 `summary`、1 篇有 `faq`。
**這批是第一批全面帶這兩個區塊的內容**，規格見 `docs/seo.md` 與
`docs/article-architecture.md` 的 Phase 4。

### `summary`

```json
{"type":"summary","items":["第一句是答案：發生了什麼、改變了什麼。","第二、三句是條件與限制。","最後一句是一個但書。"]}
```

- 2–5 句，每句 ≤ 300 字，放在第一個 heading 之前，**一篇只能有一個**。
- 渲染成頁面上的摘要卡 `#article-summary`，並餵給 JSON-LD 的 `abstract` 與 `speakable`。
- **只能重述正文已經寫過、而且有來源的內容。** 數字逐字照正文，不得出現正文沒有的數字——
  答案引擎最不該從這裡引用到一個文章本身沒說的數字。
- 不要寫「本文介紹…」這種後設句，也不要只把 `description` 抄一遍。

### `faq`

```json
{"type":"faq","items":[{"question":"…","answer":"…"}]}
```

- 2–10 組，question ≤ 200 字、answer ≤ 1000 字，**一篇只能有一個**。
- 渲染成 `<details>`，並餵給 `FAQPage` 結構化資料。
- **只放讀者真的會問、而且這篇真的答得出來的問題。** 答案是純文字，不能有連結。
- 不要把小節標題改寫成問句充數。

### 字數影響

`_body_length` 會把 `summary` 與 `faq` 的字一起算進 `TEXT_RANGE`（1,500–6,000）。
批次 3 的英文譯文本來就有 7,700–10,100 字元、會觸發 `text_length` **warning**，
加了這兩個區塊之後更確定會觸發。**那是 warning，前兩批同樣如此，
不要為了消掉它刪掉任何一條查證過的條件或限制。**

## 站內連結

- 兩個 link 都用絕對網址 `https://mokaair.com/zh-TW/life/<slug>`，
  link 的 `text` 必須**等於目標文章該語言的正式 title**。
- 內容定稿後跑 `pack_cli relink` 與 `pack_cli autolink`，產生可審閱的 diff 再套用。
  不要自己手寫 `rich_paragraph` 的 `article` inline。

## 研究紀錄

檔案 `docs/<工作區>/research/<slug>.json`，格式沿用批次 3：

```json
{"slug":"…","event_date":"YYYY-MM-DD","title":"（同 zh-TW title）",
 "sources":[同內容包 sources],"checked_on":"YYYY-MM-DD",
 "verified_facts":["每條一個可查的事實，句尾括號寫出處 URL"],
 "unverified_or_excluded":["看到但查不到一手來源、因此沒寫進文章的說法，以及原因"],
 "editorial_brief":"原創情境與這篇刻意不談的範圍",
 "hero_label":"主圖下方標語，繁中 ≤ 12 字",
 "diagram":{"title":"圖解標題 ≤ 20 字","caption":"（同內容包 diagram caption）",
            "nodes":[["小標 ≤ 8 字","說明 ≤ 14 字"],[…],[…],[…]]}}
```

圖解是 2×2 四格卡片（左上→右上→左下→右下），`nodes` 剛好 4 組。
**圖上任何數字都必須出現在文章正文。**

## 圖像

- hero 是點陣圖 1600×900 JPEG，**≤ 200 KB**（硬上限 300 KB）。
- 圖解是自繪 SVG，`viewBox="0 0 1600 900"`，要有 `<title>` 與 `<desc>`，
  不得有 `<script>`／`<foreignObject>`／`<image>`／`<use>`、外部網址、`@import`，
  字級不得小於 15 px。
- **一律不畫任何商標、字標、圖示、吉祥物或介面截圖**——商標不是我們的，
  而且畫面一改就過時。產品用純文字寫出名字。
- 五語各一張 hero 與一張圖解（`hero-<locale>.jpg`、`diagram-1-<locale>.svg`）。
- 代理看不到自己畫出來的版面：contact sheet 一定要有人逐張看過。

## 流程

一篇一個撰稿代理 → **交給另一個代理獨立查核** → 翻譯 → 逐語系審稿 → 圖像 → 索引 → 驗證。

**獨立查核不能省。** 批次 3 的紀錄：7 篇每篇 56–102 條主張，每篇都改了 15–38 處，
一篇需要第二輪。撰稿者不得查核自己的文章。

每個撰稿代理**只寫自己那兩個檔案**（內容包 + 研究紀錄），不動其他檔案、不 git commit。
審稿代理**只交修正清單**，由 `apply_corrections.py` 統一套用，避免多代理寫同一個檔。

## 自檢

```bash
cd apps/api
uv run python ../../docs/<工作區>/check_article.py <slug> --full --assets   # 要 OK
uv run python -m app.guides.pack_cli lint --kind life                        # 0 error
```

輸出 `OK` 才算完成；有 `FAIL` 就修到過。

## 翻譯（第二階段才做）

四個 locale 加進同一個內容包，順序 `zh-TW, en, ja, ko, zh-CN`：

- blocks 型別與順序、table 的欄列數、`summary` 的句數、`faq` 的題數、
  sources（title 可譯，url 與 `checked_on` 不變）完全對應。
- hero.src → `/guides/<slug>/hero-<en|ja|ko|zh-cn>.jpg`，diagram 同理，alt／caption 翻譯。
- 兩個 link 的 url 換成 `https://mokaair.com/<locale>/life/<slug>`，
  text 用目標內容包該 locale 的正式 title。
- 日期寫法照目標語言習慣，但年月日數字不變；價格幣別不變。
- 介面名稱對照各語言的官方說明頁，不要自己翻。
- **幣圈的免責 callout 用該語言自己的標記字串，不是中文那句的翻譯**——見 `crypto.md`。

## 查核回饋：36 篇查出來的錯誤型態（批次 4 新增）

36 篇研究紀錄各配一份獨立查核，**36 篇全部 `needs_fixes`**：103 條事實被推翻、204 條查不到依據。
撰稿代理不能重讀來源，紀錄裡留下的錯就是刊出去的錯。以下依「刊出去的傷害」排序，
每一條都在兩個以上的垂直出現過。標**收緊**的是本規格已經有、但這次沒擋住的規則。

### 1. `verbatim_quote` 不是逐字

NVIDIA 併購 Hugging Face 那篇用刪節號把兩句接起來，而原文順序是**相反的**
（原文先「NVIDIA is the largest contributor of open models and data to Hugging Face…」，
下一段才是「NVIDIA has released more than 500 models…」）。
CUDA-Q 文件頁原文印的是 “fault-tolerant fault-tolerant”（NVIDIA 自己重複了一次），紀錄悄悄清成一個；
SEC 解釋令報頭原文是 `[Release Nos. 33-11412; 34-105020; File No. S7-2026-09]li`，
那個 `li` 在聯邦公報 .txt、XML 與 GPO PDF 三處都在，是**已刊登的文本**，紀錄把它修掉了。
FDIC 用 ` / ` 把報頭裡相隔 39 行的兩串接成一句，iPhone Duo 也有四條是這樣把兩個頁面元素拼起來的；
Apple M6 七條把 Apple 的破折號重打成 ASCII 連字號。
科技垂直 13 篇裡有 9 篇的引文欄位靠不住。

**規則**：`verbatim_quote` 只能是在來源頁**原樣搜尋得到的連續字串**——錯字、重複字、不斷行空格、
U+2011 連字號、註腳標記一律照抄，來源自己有錯就寫明是來源的錯。
要清理、要接、要省略，就不要叫 `verbatim_quote`，標成「讀到的值」或改寫成敘述。
**收緊**：前面「官方標題裡有看不見的字元」原本只講 link 的 `text`，這批在引文欄位又踩一次，
該規則適用於所有要照抄的字串。

### 2. 把「來源沒說」寫成「來源說沒有」

iPhone Duo 紀錄寫「內螢幕不是用超瓷晶盾 2」——Apple 只說明超瓷晶盾 2 用於正面／外螢幕，
從來沒有說內螢幕不是；同篇「Apple 沒提到 NCC」被它自己列為來源的台灣規格頁
（「如需台灣 NCC 認證產品的進一步詳細資訊…」）推翻。
Windows Zenith 紀錄寫「Intel grep 0 次」，實際出現 2 次，藏在 intelligence／Intelligent 裡；
Apple M6 紀錄寫「三篇都沒有 foundry」，Mac Studio 稿出現兩次 Foundry（那是特效軟體公司）；
NVIDIA Vera Rubin 紀錄用「Taiwan 與 TSMC 各 0 次」反過來禁止撰稿者提台灣，
但同一批公告寫著 DSX 是在 GTC Taipei 發表的——那條禁令會擋掉一個來源真的有寫的事實。

**規則**：否定句一律限縮到「這一頁沒有寫」並寫出查法，句型是「以 X 查核到 2026-09-16 未見」。
不可以寫「官方沒有」「從未」「第一份」「唯一」「恰好」「全部」。
子字串 grep 的零次不算零次（要用詞界比對），而且同義詞要各查一次。

### 3. 收窄或放大來源說的範圍

OpenAI 募資稿原文是 “growing revenue four times faster than the companies who defined the
Internet and mobile eras, **including** Alphabet and Meta”，紀錄寫成「比 Alphabet 與 Meta 快四倍」，
把舉例變成對打；同篇另外兩條把 “including …” 起頭的機構名單與銀行團寫成「參與機構為……」。
CUDA-Q 紀錄寫「恰好六家在用」，原文是 “already being used by QPU makers and labs **including** …”。
Hugging Face 事件那篇刪掉一個 `wrongly`（原文 “nor **wrongly** processes HDF5 external references”），
把修好一個瑕疵講成拿掉一個功能；前沿治理那篇刪掉 `where appropriate`，
以及 `if the model is amongst their respective most capable models`。

**規則**：`including`／`such as`／「例如」起頭的清單**永遠不是全清單**，不可以寫成「共 N 家」「名單為」，
也不可以拿某一語系的名單當全名單。`where appropriate`、`may`、`if`、`up to`、`substantially`、`wrongly`
這類限定詞刪掉一個就是換了一個主張，一律原樣留著。

### 4. 活文件的快照被當成常數

ESMA 的 MiCA 臨時名冊在**查核當天** 15:58 UTC 被換掉：頁面的 “Last update” 從 9 September 2026
變成 16 September 2026，CASPS.csv 從 346 列／342 個 LEI 變成 352 列／349 個，
NCASP.csv 從 167 列變成 174 列、通報主管機關從 3 國變成 5 國，德國從 89 變成 94。
而且舊快照本身就算錯了——三個 LEI 各重複一次的話，346 列只可能是 343 個 LEI。
AI 垂直十一篇研究紀錄都記了 `openai.com/news/rss.xml` 的 item 數，同一天記出 1,193／1,194／1,195 三種，
查核者再抓又是 1,196；本規格上面自己寫的「1,193 筆」同樣已經過期。
主權 AI 語料庫更亂：同日新聞稿寫 22 億 tokens（截至 8 月底）、簡報寫 21 億、
taic 端點回 2,200,397,354、資料集 6,417 筆與 318.59 GB，遠高於簡報的 5,000 與 200 GB。

**規則**：名冊列數、feed 筆數、儀表板與 API 的計數、「Last update」字串、PDF 的 `ModDate`
都是當下的值，不是事實。要寫就標出處與時點，並在定稿當天重抓一次；
不同來源的計數不可以出現在同一句話裡，更不可以相加相減。
**收緊**：上面叫你數 `<item>` 是為了判斷「這個 feed 到底拿到了沒有」，
那個數字是取得成敗的判準，**不是可以寫進文章或研究紀錄的事實**。

### 5. 放棄的路徑被寫成環境限制

SEC 解釋令那篇寫「本容器無法抽 PDF 文字（pdftotext 與 pdftoppm 都不在）」，
但 pypdf 與 pdfminer 都裝著，查核者把 20 頁、161,882 字整份抽了出來——
代價是 `sources` 第一條是一份**從未讀過**、只靠 md5 比對的文件。
台灣 VASP 那篇寫「金管會站內搜尋外包給 Google CSE、列表分頁靠 JS」，
實際上一個純表單 POST（`mcustomize=news_list.jsp` 加 keyword）就回 HTTP 200、129,023 bytes
與伺服器端算好的三列結果；因為寫掉了這條路，兩則直接相關的金管會新聞稿
（2025-03-25 預告草案、2025-02-13 座談會）從頭到尾沒讀。
OCC 那篇寫「occ.gov 對所有路徑回 302」，實際是回 200 但送回首頁；
馬祖海纜那篇寫「中華電信訊息列表前端渲染、等於取不到」，而 robots.txt 就寫著 sitemap，
裡面有 6,826 個網址、含每一則 2026 年公告。

**規則**：「我抓不到」不等於「拿不到」。宣告環境限制之前先換一條路徑：
sitemap、robots.txt、純表單 POST、開放資料檔、govinfo 這類官方鏡像。
容器行為與工具敘事不進文章；寫進研究紀錄時要寫成能重現的配方——
歐盟 CELEX 那條配方漏寫了 `Accept-Language: eng`，照抄的人三種 Accept 全拿到 HTTP 400。

### 6. 引用一個從來沒有落地的網址

Astral 那篇寫「OpenAI 的 Codex 開發者文件首頁 astral／ruff／uv 各出現 0 次」，掛在
`developers.openai.com/codex/`。那個網址 308 轉到 `/codex`、再 308 轉到 `learn.chatgpt.com/docs`，
回來的是一個 12,413 字的導覽殼——裡面連 `python` 也是 0 次。
零次是殼造成的，不是關於 Codex 文件的證據。

**規則**：記網址之前先確認**最後落地的是哪一個 URL**、body 是不是正文。
轉址後的頁、軟性 404、擋阻頁都不能拿來當「某個字沒出現」的依據——
負面證據對頁面的要求比正面證據更高，換不到能承載它的頁面就不寫那句話。
**收緊**：上面「HTTP 200 不代表拿到 feed」不只適用於 feed。本批實測到的擋阻頁包括
聯邦公報的 `Request Access`（10,596 bytes）、MOPS 的 800 bytes 安全頁、EUR-Lex 的 202 加 0 bytes、
NVIDIA 新聞室標題為 `News Archive` 的軟性 404。**先看 body，再記 `checked_on`。**

### 7. `sources[]` 裡放了讀不到的網址，還附查核日

OCC 那篇的 `sources[0]` 是聯邦公報的正規頁，實際回 302 到 `unblock.federalregister.gov`，
body 是 10,596 bytes 的 “Request Access”，紀錄卻掛著 `checked_on: 2026-09-16`，
`sourcing_notes` 一個字都沒提被擋。AI 垂直有三篇（`chatgpt-financial-services`、
`chatgpt-storage-scale`、`openai-funding`）的 `sources[0]` 是 `openai.com/index/*` 的 403 頁，
而正文實際上整篇來自 `web.archive.org` 的封存。

**規則**：`sources[]` 只放**你自己讀到正文**的網址，`checked_on` 是你讀到它那一天。
被擋就換官方的其他管道（RSS、govinfo、各國 newsroom）或不寫；
要用封存就把封存網址本身放進 `sources[]` 並在正文說明依據，
**不可以一邊引封存、一邊宣稱讀的是官方頁**。
**收緊**：「每個數字都要指得到一條 source 的原文」這條，36 篇裡有 31 篇沒做到
（`gpt-live-1-api` 67 條裡 33 條掛在 12 個未列網址、NCUA 90 條裡 75 條、馬祖海纜 43 條裡 21 條）。
做法要倒過來：**先定四條 `sources`，再把文章收到那四條真的涵蓋的範圍**，不要指望事後補來源。
另外，推導出來的網址一樣是猜的（拿掉 WordPress 尺寸後綴、用 cellar id 拼、
從別的語系路徑類推、`?page=3`），本規格說猜對也算捏造。

### 8. 不同語系的官方頁互相矛盾，而在地化版本掉了對沖詞

iPhone Duo 台灣新聞稿把英文的 `up to` 拿掉：EN “up to 20 percent faster” 變成「快了 20%」、
“up to 40 percent higher stiffness” 變成「高出 40%」。更糟的是
EN “up to 40 percent faster and more power efficient” 的 40% 只掛在速度上，
台灣版寫成「速度和能源效率都提升了 40%」。同一篇台灣版把 MagSafe／Qi2 配到 20 分鐘那一邊，
英文版與台灣規格頁都是 20 分鐘有線、30 分鐘無線。
上市地區數台灣版寫「超過 63 個國家和地區」，en／uk／jp／au／sg 都寫 70 以上。
日本 FSA 同一頁的英文版寫 “March 17, 2023 (Updated July 23, 2026)”，
日文版寫「令和４年11月４日」（2022-11-04）加上令和８年７月23日更新，只有更新日對得起來。

**規則**：兩個語系都是官方，不可以挑一個當唯一數字，也不可以混用；
繁中稿以英文版的對沖詞為準，並註明兩版差異與各自出處。
數字要連著**它自己的條件**一起抄——iPhone 18 Pro 的 30 小時不在「eSIM 專用機型」那個限定語裡面，
NVIDIA 的 40%／35% 是工廠層級、不是機櫃層級。

### 9. 研究者自己算出來的數字

Apple 的註腳只列語言名稱，紀錄寫「支援 16 種語言」——16 這個數字來源沒有印。
NVIDIA 只說「1,000 個邏輯量子位元……150,000 個實體量子位元」，紀錄寫成「每個邏輯量子位元 150 個實體」。
Pixel Drop 紀錄寫「五項功能」，Google 正文的小標只有四個（第五個是圖片的列數）。
台灣 4G 三組頻段「合計 280 MHz」是把表格相加出來的；ENISA 頁面上的「27 個會員國」是自己數的。
NCUA 那份 634,750 bytes 的全文裡「2027」出現 **0 次**，寫「2027 年 1 月 18 日生效」就是文章自己的算術。

**規則**：加總、相除、清點、換算出來的數字，來源沒印就不是事實。
要嘛照來源的說法寫（「官方列出的語言包含繁體中文」「制定日起 18 個月或最終規則後 120 天，取其早」），
要嘛明寫是編輯換算。**生效日一律寫公式，不寫日期。**

### 10. 廠商宣稱被寫成事實，而 `is_vendor_claim` 旗標擋不住

OpenAI 與 Broadcom 那篇有八個事實標成 `is_vendor_claim=false`，包括「超過 8 億週活躍使用者」
這種公司自報數、「從零開始設計這顆晶片」這種自述功勞，以及發行人自己在前瞻性陳述裡免責的部署時程。
iPhone Duo 的 20 分鐘充電、「零快門延遲」、「首次」、「超過 500 家電信業者」都標成 false，
但它們和同篇標成 true 的電池數字掛的是同一個「Apple 於 2026 年 7 月以預量產機測試」註腳。
馬祖海纜「殘骸移動」是中華電信的**初步推估**，也標成 false。反方向也有：
OCC 那篇把主管機關的分析假設標成 true。

**規則**：旗標不可信，自己判斷。**外部無法觀察、公司或機關自報、關於未來、關於自己的功勞或流程**——
一律是宣稱，寫成「Apple 表示／NVIDIA 表示／中華電信初步推估／金管會指出」。

### 11. 日期混用

主權 AI 語料庫的「逾 15 億 tokens」被寫成「截至 2026-07-24」，官方只寫「自上線以來」，
7/24 是發布日；同篇客語語料的「近日上架」被寫成 7/24 上架。
NVIDIA 一月稿的 “will also offer” HGX Rubin NVL8 被寫成現在式的已供貨。
SEC 的 Project Crypto「2025-07-31 啟動」其實是註腳 18 那場演講的日期。
幣圈四篇都有這個張力：FDIC 理事會 04-07 對刊登 04-10、SEC 解釋令作成 03-17 對刊登兼生效 03-23、
SEC 八月案核准 08-18 對刊登 08-21、NCUA 署名 05-14 對刊登 05-18。
AI 垂直另有時區問題：22:00 GMT 在台北已經是隔天早上，
而 OpenAI feed 有 338 筆 `pubDate` 是 `00:00:00 GMT` 的佔位值，日期可用、時刻不可用。

**規則**：發布日、作成日、核准日、刊登日、生效日、供貨日、頁面更新日是**不同的日期**，
紀錄與文章都要分開寫，slug 尾碼與 `news_date` 用事件日並在文章裡把兩個日期都寫出來。
沒有截止時點的累計數字不要自己補一個。要寫進繁中正文的時刻先換算成台北時間。

### 12. 研究紀錄被截斷的那一段，沒有人查核過

`apple-september-hardware` 有 91 條事實，交到查核者手上的檔案在第 34 條中間就斷了，
Series 12／Ultra 4／AirPods 5 之後全部未經查核；`taiwan-sovereign-ai-corpus` 斷在第 40 條；
JFSA 審議會那篇斷在第 25 條；馬祖海纜的 `not_said` 最後一項斷在句子中間。

**規則**：那些區段不是「通過查核」，是「沒有人看過」。
撰稿用到截斷點之後的內容，先送第二輪查核；不要因為同一份檔案前面都對就整份照抄。

### 逐篇的修正清單

以上是型態，個案在這三份：[`corrections-crypto.md`](corrections-crypto.md)（11 篇）、
[`corrections-tech.md`](corrections-tech.md)（13 篇）、[`corrections-ai.md`](corrections-ai.md)（12 篇）。
每篇分 `must_fix`／`must_add`／`live_data_warnings`／`source_list_fix`。
開稿前先讀本篇 slug 的那一段，再讀研究紀錄：兩者衝突時以修正清單為準，
修正清單與本規格衝突時以本規格為準，並把衝突記進 `tasks/`。
