# 查證記錄：ai-search-seo

查證日一律 2026-09-14。全部來源都是搜尋引擎自己的開發者文件、說明中心、規範原文或
提案本身的網站；沒有引用任何代理商部落格作為事實依據。

讀取方式說明：下表的「實際讀取方式」欄寫的是這一次真正讀到內容的管道。
本次所有網址都以 WebFetch 直接讀取成功，沒有遇到 Cloudflare 403，因此不需要
Wayback Machine 快照或限定官方網域的 WebSearch 交叉比對。

## 主張與來源

| 主張（正文寫法） | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| Google 搜尋分成檢索、建立索引、提供搜尋結果三個階段 | https://developers.google.com/search/docs/fundamentals/how-search-works | 2026-09-14 | WebFetch 直接讀取，HTTP 200 |
| 「即使頁面符合 Google Search Essentials，Google 也不保證會檢索、建立索引或提供該頁面」 | https://developers.google.com/search/docs/fundamentals/how-search-works | 2026-09-14 | WebFetch 直接讀取，原句為 "Google doesn't guarantee that it will crawl, index, or serve your page, even if your page follows the Google Search Essentials." |
| 技術需求三項：Googlebot 沒有被擋、頁面回傳 HTTP 200 成功狀態碼、頁面有可索引的內容 | https://developers.google.com/search/docs/essentials/technical | 2026-09-14 | WebFetch 直接讀取；文件寫的是符合這三項才「eligible」被建立索引，正文照此譯成「有資格」 |
| 「已檢索，目前尚未建立索引」的官方描述：將來可能建立索引也可能不會，不需要重新提交 | https://support.google.com/webmasters/answer/7440203 | 2026-09-14 | WebFetch 直接讀取，原句為 "The page was crawled by Google but not indexed. It may or may not be indexed in the future; no need to resubmit this URL for crawling." |
| 網頁已建立索引不保證會出現在搜尋結果中，結果隨使用者搜尋紀錄、位置等變數而不同 | https://support.google.com/webmasters/answer/7440203 | 2026-09-14 | WebFetch 直接讀取，原句為 "Just because a page is indexed doesn't guarantee that it will show up in your search results." |
| RFC 9309 標題為 Robots Exclusion Protocol，2022 年 9 月發布，Standards Track | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-09-14 | WebFetch 直接讀取 RFC Editor 原文 |
| RFC 9309 作者：Martijn Koster、Gary Illyes、Henner Zeller、Lizzi Sassman（後三位署名 Google LLC），正文寫成「Martijn Koster 與 Google 的三位工程師」 | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-09-14 | WebFetch 直接讀取原文作者欄 |
| robots.txt 的規則不是一種存取授權，也不能代替內容安全措施 | https://www.rfc-editor.org/rfc/rfc9309.html | 2026-09-14 | WebFetch 直接讀取，原句為 "These rules are not a form of access authorization." 與 "The Robots Exclusion Protocol is not a substitute for valid content security measures." |
| robots.txt 主要用途是避免網站被大量請求壓垮，不是讓網頁不出現在 Google 的機制 | https://developers.google.com/search/docs/crawling-indexing/robots/intro | 2026-09-14 | WebFetch 直接讀取，原句為 "used mainly to avoid overloading your site with requests; it is not a mechanism for keeping a web page out of Google." |
| 被 robots.txt 擋住的網址若有其他網站連過來，仍可能被建立索引，只是結果沒有說明文字 | https://developers.google.com/search/docs/crawling-indexing/robots/intro | 2026-09-14 | WebFetch 直接讀取，原句為 "A page that's disallowed in robots.txt can still be indexed if linked to from other sites." |
| 要讓 noindex 生效，該網頁不能被 robots.txt 擋住，否則爬蟲永遠看不到那條規則 | https://developers.google.com/search/docs/crawling-indexing/block-indexing | 2026-09-14 | WebFetch 直接讀取，原句為 "If the page is blocked by a robots.txt file or the crawler can't access the page, the crawler will never see the noindex rule." |
| 指出標準網址的偏好是「提示，不是規則」；Google 可能選擇不同的網址 | https://developers.google.com/search/docs/crawling-indexing/canonicalization | 2026-09-14 | WebFetch 直接讀取，原句為 "indicating a canonical preference is a hint, not a rule." |
| canonical 訊號強度：轉址最強、連結註解次之、寫在網站地圖裡是弱訊號 | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls | 2026-09-14 | WebFetch 直接讀取；文件把 redirects 標為 strongest signal、rel=canonical 為 strong signal、sitemap 為 weak signal |
| 官方文件沒有要求每一頁都放自我指向的 canonical（正文標為「業界普遍做法，官方文件沒有要求」） | https://developers.google.com/search/docs/crawling-indexing/canonicalization | 2026-09-14 | WebFetch 直接讀取；該頁只說明可以指出偏好、不指出網站也能運作，通篇未出現「每頁必須自我指向」的要求。這是「文件沒有寫」的陳述，正文因此標為業界慣例而非官方機制 |
| hreflang：兩個網頁若沒有互相指向對方，標記會被忽略 | https://developers.google.com/search/docs/specialty/international/localized-versions | 2026-09-14 | WebFetch 直接讀取，原句為 "If two pages don't both point to each other, the tags will be ignored." |
| Sitemap 協定為 0.9 版，只有 loc 必填；changefreq 是提示不是命令；priority 不太可能影響結果頁位置 | https://www.sitemaps.org/protocol.html | 2026-09-14 | WebFetch 直接讀取提案本身的網站；原句為 "the value of this tag is considered a hint and not a command." 與 "the priority you assign to a page is not likely to influence the position of your URLs in a search engine's result pages." |
| Google 忽略 priority 與 changefreq；只在 lastmod 一致且可驗證時才採用 | https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap | 2026-09-14 | WebFetch 直接讀取，原句為 "Google ignores <priority> and <changefreq> values." 與 "Google uses the <lastmod> value if it's consistently and verifiably accurate."（正文不寫角括號，因為內容包禁止 HTML 樣式的字串） |
| 網站地圖不保證裡面的每個項目都會被檢索與建立索引 | https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview | 2026-09-14 | WebFetch 直接讀取，原句為 "it doesn't guarantee that all the items in your sitemap will be crawled and indexed." |
| 要出現在 AI 摘要或 AI 模式「沒有額外要求，也不需要其他特別的最佳化」 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取，原句為 "There are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary." |
| 網頁必須已建立索引、符合技術需求、有資格顯示摘要片段，才可能出現在 AI 功能裡 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取，原句為 "a page must be indexed and eligible to be shown in Google Search with a snippet, fulfilling the Search technical requirements." |
| 站長可用的控制項：nosnippet、data-nosnippet、max-snippet、noindex、robots.txt 對 Googlebot 的規則；AI 訓練用途為 Google-Extended | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取該頁的控制項清單 |
| Google 描述 AI 功能採用「查詢展開」（query fan-out），會同時發出多個相關搜尋 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取，原文用語為 "query fan-out"；該頁未公布挑選引用的排序規則，正文因此只寫「沒有公布排序規則」 |
| Bing：在 AI 驅動的搜尋裡，讓網站可被檢索、保持更新、完整建立索引比以往更重要（2025 年 7 月） | https://blogs.bing.com/webmaster/July-2025/Keeping-Content-Discoverable-with-Sitemaps-in-AI-Powered-Search | 2026-09-14 | WebFetch 直接讀取 Bing 官方部落格；文章日期 2025-07-31，原句為 "keeping your website crawlable, fresh, and fully indexed is more important than ever" |

## 分級標記的依據

正文把每個說法標成三級，對應如下：

- **官方文件說明的機制**：上表所有帶原句引用的條目。正文在句子裡寫出是哪一份官方文件說的。
- **業界普遍做法，官方文件沒有確認**：正文表格裡只有「每一頁都放自我指向的 canonical」
  這一條。依據是官方標準化說明頁通篇沒有這個要求，表格因此寫成「官方文件沒有要求」，
  不寫成「官方不建議」，也不寫成「官方建議」。
- **廠商或代理商的行銷主張**：正文只用「這類標題在行銷內容裡很常見」這種描述句，
  **沒有引用任何一家代理商的說法當事實依據**，也沒有把任何無主詞的斷言寫進正文。
  對照的一手依據是 Google AI 功能說明頁「沒有額外要求」那一句。

## 刻意沒有寫進正文的東西

- **沒有任何成效數字。** 搜尋「SEO 已死」得到的結果幾乎全是代理商部落格，
  其中流傳的比例數字（無點擊搜尋佔比、市佔率等）都沒有一手來源可查，全部略去。
- **沒有寫「業界普遍認為 AI 引用會增加」這類句子。** 系列規則禁止承諾成效。
- **沒有引用 Bing Webmaster Guidelines 頁面。** 該頁（bing.com/webmasters/help/...）
  以 WebFetch 讀取只回傳標題、沒有正文，無法取得可引用的原句，因此不列入 sources；
  改用 Bing 官方部落格那一篇（正文與 sources 都用它）。
- **「約 500 頁以下的網站可以不用網站地圖」** 這個數字雖在 Google 網站地圖總覽讀到，
  但與本篇主軸無關，且會讓圖解與正文多一個需要對齊的數字，故不寫進正文。

## 圖解的數字檢查

`diagram-1.svg` 上只出現一個數字：右下角的「© Mokaair 製圖 2026」。
正文多處出現 2026（查證日 2026 年 9 月 14 日、表格圖說）。
其餘層級標號一律用中文數字一、二、三、四，避免多餘的數字對齊問題。
`hero.svg` 完全沒有數字，只有一行九個字的標題文字（字級 52）。
