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

## 內容包格式

檔案 `apps/api/app/guides/content/<slug>.json`。

slug 一律 `<vertical>-news-<topic>-<YYYYMMDD>`，日期是**事件日**，不是發布日
（批次 3 把 `...-20260709` 改名為 `...-20260708` 就是因為官方發布日是 7/8）。

`topics`：AI 用 `["ai", <橫向主題>, "ai-news"]`；科技用 `["tech", "tech-news"]`
（可再加 `gadgets`／`software`）；幣圈用 `["finance", "crypto"]`。
`destination_id` 一律 `null`。`kind` 一律 `life`。

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
