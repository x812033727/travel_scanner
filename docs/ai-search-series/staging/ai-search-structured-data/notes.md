# 查證記錄：ai-search-structured-data

查證日一律 **2026-09-14**。格式：`主張｜來源網址｜查證日｜實際讀取方式`。
本篇沒有任何成效數字，也沒有任何實測；下表每一列都是「文件上寫了什麼」。

## 讀取方式說明（先講環境）

- `developers.google.com` 與 `schema.org` 在這個環境用 `curl -sSL` 直接讀得到（HTTP 200），
  `schema.org` 必須加 `--compressed`，否則拿到的是 gzip 位元組。
- `schema.org` 的頁面頂端帶有「You are viewing the development version of Schema.org」橫幅，
  型別定義內容與正式站一致，`sources` 仍寫 `https://schema.org/…` 正式網址。
- Google 的 FAQ 結構化資料說明文件網址已經**轉址**（HTTP 301）到
  `https://developers.google.com/search/updates#removing-faq-rich-result`，
  這本身就是「文件已被移除」的證據，FAQ 相關事實一律引自該更新紀錄。
- Wayback Machine 的 CDX API 在這個環境被 egress policy 擋住，因此沒有使用快照。
- `bing.com/webmasters/help/...` 是需要 JavaScript 的應用程式，`curl` 只拿得到空殼，
  所以微軟的說法改引 `blogs.bing.com` 的官方網誌文章（WebFetch 讀取）。
- repo 內的 `docs/seo.md` 與 `apps/web/lib/structured-data.ts`、
  `apps/web/components/guides/article-page.tsx`、`apps/web/app/[locale]/{guides,life,destinations}/page.tsx`
  只讀不改，用來描述本站現況。

## 官方文件說明的機制（第 1 級）

| 主張 | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| 結構化資料是「為網頁提供資訊並將網頁內容分類的標準化格式」（英文原文：a standardized format for providing information about a page and classifying the page content） | https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data | 2026-09-14 | curl 直接讀取，HTTP 200；頁尾 Last updated 2025-12-10 UTC |
| Google 支援 JSON-LD、微資料 (Microdata)、RDFa 三種格式，並建議優先使用 JSON-LD | 同上 | 2026-09-14 | curl 直接讀取；繁中版同頁 `?hl=zh-tw` 用詞為「微資料」 |
| 涉及 Google 搜尋的行為以 Google 搜尋中心文件為準，而不是 schema.org 的文件 | 同上 | 2026-09-14 | curl 直接讀取（"rely on the Google Search Central documentation as definitive for Google Search behavior"） |
| 官方建議的量測方式是自己挑一批頁面做前後對照（"run a before and after test on a few pages on your site"） | 同上 | 2026-09-14 | curl 直接讀取，"Measuring the effect of structured data" 一節 |
| 「使用結構化資料會『啟用』相關功能，但不『保證』該功能一定會顯示。」 | https://developers.google.com/search/docs/appearance/structured-data/sd-policies?hl=zh-tw | 2026-09-14 | curl 直接讀取繁中版，HTTP 200；頁尾 Last updated 2026-07-10 UTC |
| 「即使複合式搜尋結果測試顯示網頁已正確加上標記，Google 也不能保證您的結構化資料一定會出現在搜尋結果中。」 | 同上 | 2026-09-14 | curl 直接讀取繁中版 |
| 不顯示的常見原因包含：結構化資料無法代表網頁主要內容、所參照的內容已對使用者隱藏、不符合指南或搜尋基礎入門 | 同上 | 2026-09-14 | curl 直接讀取繁中版 |
| 「請勿為網頁讀者看不到的內容加上標記。」＋演出者的例子（JSON-LD 介紹某位演出者，內文就必須描述同一位） | 同上 | 2026-09-14 | curl 直接讀取繁中版；英文版原文 "Don't mark up content that is not visible to readers of the page." |
| 「請勿為不相關或容易誤導使用者的內容加上標記，例如造假評論或與網頁主題無關的內容。」 | 同上 | 2026-09-14 | curl 直接讀取繁中版 |
| 完整性規定：標記評論時使用者會預期搜尋結果看到的就是全部評論，只標一部分可能誤導 | 同上 | 2026-09-14 | curl 直接讀取繁中版 |
| 「不是由實際使用者給予的評論或評分，可能會導致人工判決處罰。」 | 同上 | 2026-09-14 | curl 直接讀取繁中版 |
| 人工判決處罰的範圍：「無法以複合式搜尋結果的形式呈現，但是這並不會影響網頁在 Google 網頁搜尋中的排名。」 | 同上 | 2026-09-14 | curl 直接讀取繁中版 |
| 自利評論：被評論的對象自己控制關於自己的評論時，該頁面不符合星級評論功能的資格 | https://developers.google.com/search/docs/appearance/structured-data/review-snippet | 2026-09-14 | curl 直接讀取，HTTP 200 |
| 垃圾內容的定義包含「操縱 Google 搜尋中的生成式 AI 回覆」；違反政策的網站「可能排名較低，或完全不出現在搜尋結果中」 | https://developers.google.com/search/docs/essentials/spam-policies | 2026-09-14 | curl 直接讀取，HTTP 200；頁尾 Last updated 2026-08-28 UTC |
| 「結構化資料不是生成式 AI 搜尋的必要條件，也沒有特別的 schema.org 標記需要加；但仍建議繼續使用，因為關係到複合式搜尋結果的資格」（"Overfocusing on structured data" 一節，屬於 "Mythbusting generative AI search: what you don't need to do"） | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | 2026-09-14 | curl 直接讀取，HTTP 200；頁尾 Last updated 2026-07-10 UTC |
| Article 標記的用途：幫助 Google 更理解網頁，並顯示更好的標題文字、圖片與日期資訊 | https://developers.google.com/search/docs/appearance/structured-data/article | 2026-09-14 | curl 直接讀取；頁尾 Last updated 2026-09-08 UTC |
| BreadcrumbList 表示網頁在網站層級中的位置；該功能在桌機版、所有有 Google 搜尋的地區與語言可用 | https://developers.google.com/search/docs/appearance/structured-data/breadcrumb | 2026-09-14 | curl 直接讀取；頁尾 Last updated 2026-09-08 UTC |
| ItemList 要搭配 Course list、Movie、Recipe、Restaurant 其中一種，才有資格取得同站輪轉（host carousel）；Top stories 這類跨站輪轉無法用標記控制 | https://developers.google.com/search/docs/appearance/structured-data/carousel | 2026-09-14 | curl 直接讀取；頁尾 Last updated 2026-09-08 UTC |
| FAQ 複合式搜尋結果：2026-05-08 加註淘汰、「This feature will no longer appear in Google Search starting May 7, 2026」；2026-06-15「Removed documentation for the FAQ rich result feature」 | https://developers.google.com/search/updates | 2026-09-14 | 由 faqpage 文件網址 301 轉址到此頁的 `#removing-faq-rich-result` 錨點，curl 讀取全文 |
| 網站連結搜尋框：2024-10-21 公告，2024-11-21 起移除；「This doesn't affect rankings」；留著標記不會造成問題（"Unsupported structured data like this won't cause issues in Search"） | https://developers.google.com/search/blog/2024/10/sitelinks-search-box | 2026-09-14 | curl 直接讀取，HTTP 200 |
| schema.org 是共用詞彙表，由 Google、Microsoft、Yahoo 與 Yandex 發起，以開放社群流程維護 | https://schema.org/ | 2026-09-14 | curl --compressed，HTTP 200；頁面帶 development version 橫幅 |
| 「Not every type of information in schema.org will be surfaced in search results — you can refer to each company's documentation to find specific uses.」 | https://schema.org/docs/faq.html | 2026-09-14 | WebFetch 讀取 |
| ItemList 型別定義（任何種類的項目清單，與 HTML 清單不同） | https://schema.org/ItemList | 2026-09-14 | curl --compressed |
| BreadcrumbList 型別定義（由連結網頁構成的 ItemList，用 position 重建順序） | https://schema.org/BreadcrumbList | 2026-09-14 | curl --compressed |
| 微軟：「Bing works hard to understand the content of a page and one of the clues that Bing uses is structured data.」 | https://blogs.bing.com/webmaster/august-2018/Introducing-JSON-LD-Support-in-Bing-Webmaster-Tools | 2026-09-14 | WebFetch 讀取；文章日期顯示 2018-07-30，網址路徑寫 august-2018，正文只引「線索之一」這句，不引日期 |

## 業界普遍做法，官方文件沒有說明（第 2 級）

| 主張 | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| 很多網站替文章加上 Article 與 BreadcrumbList，期待 AI 產品也讀得懂；官方文件沒有說明生成式 AI 功能如何使用這些標記 | https://developers.google.com/search/docs/fundamentals/ai-optimization-guide | 2026-09-14 | curl 直接讀取。該指南只寫「不是必要條件、沒有特別標記」，沒有說明 AI 功能如何使用標記，因此正文寫成慣例而非機制 |

## 廠商或代理商的行銷主張（第 3 級，句子裡已寫出是誰說的）

| 主張 | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| 美國數位行銷公司 Globe Runner 在 2026-07-02 的行銷文章寫「Both Google and Microsoft have confirmed that structured data helps their AI systems understand, verify, and cite content」，並稱「For AI systems, schema is a trust signal, not a display trigger」 | https://globerunner.com/structured-data-schema-markup-ai-2026/ | 2026-09-14 | curl + WebFetch。文內把兩個「確認」歸給 Search Engine Land 的報導；外部連結只有 searchengineland.com 與 searchenginejournal.com，沒有任何連向 Google 或 Microsoft 自己的文件 |

其他搜尋結果（Medium、多家代理商部落格）出現「3.2 倍」「36%」「44%」之類的引用率數字，
**一律不採用**：沒有可查的查詢集與方法，也不符合本系列「不寫成效數字」的規則。

## 本站現況（只讀 repo，沒有修改）

| 主張 | 來源檔案 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| 文章頁輸出 BreadcrumbList 加 Article（系列總覽頁為 CollectionPage），標題、描述、`datePublished`、`dateModified` 取自這一頁的內容，只有在有 hero 時才寫 `image` | apps/web/components/guides/article-page.tsx（第 256–277 行） | 2026-09-14 | 直接讀取檔案 |
| 目錄頁與目的地索引輸出 BreadcrumbList 加 ItemList；清單為空時 `itemList()` 回傳 null，整段標記不輸出 | apps/web/lib/structured-data.ts、apps/web/app/[locale]/life/page.tsx、guides/page.tsx、guides/[kind]/page.tsx、destinations/page.tsx | 2026-09-14 | 直接讀取檔案 |
| 首頁輸出 Organization 與 WebSite；SearchAction 只在搜尋可用時輸出，且文件寫明它不是在換取網站連結搜尋框 | apps/web/lib/structured-data.ts、docs/seo.md「Structured data and social metadata」一節 | 2026-09-14 | 直接讀取檔案 |
| 本站沒有評論、FAQ 與商品／Offer 標記；`docs/seo.md` 原文：「There is no invented review or FAQ markup.」「Purchases are not enabled; this work does not add Product/Offer markup…」 | docs/seo.md | 2026-09-14 | 直接讀取檔案 |
| 本站沒有量測過結構化資料對曝光的影響；`docs/seo.md` 開頭即寫明「it does not promise indexing, ranking, or a measured performance improvement」 | docs/seo.md | 2026-09-14 | 直接讀取檔案 |

## 沒有寫進正文的東西

- 沒有引用任何「AI 引用率提升」的數字。
- 沒有描述任何搜尋結果畫面或 AI 回答（本站沒有做過實測）。
- 微軟是否對「schema 幫助 Copilot 引用」有官方說法：在 blogs.bing.com 找到的
  2026-02-10「AI Performance」公告沒有提到結構化資料，因此正文不寫這件事，
  只寫「去廠商自己的說明中心找原文；找不到就以官方文件為準」。
- 本篇沒有寫 Search Console 報表的操作流程，那屬於既有文章
  `google-ai-overviews-for-site-owners` 與本系列的 `ai-search-measuring-citations`。

## 圖上的數字

`diagram-1.svg` 的文字節點只有一個數字：右下角的「© Mokaair 製圖 2026」。
正文多處出現「2026」（例如「2026 年 9 月 14 日查證」「2026 年 5 月 7 日」），符合圖上數字必須出現在正文的規定。
`hero.svg` 不含任何數字。
