# ai-search-aeo 查證記錄

查證日一律 **2026-09-14**。格式：`主張｜來源網址｜查證日｜實際讀取方式`。
本篇沒有用到任何代理商部落格當事實依據；三筆行銷內容（Ahrefs、HubSpot、Kalicube）
只用來佐證「確實有人這樣用這個詞」，正文每一處都寫明了是誰說的、是行銷內容。

## Google 官方文件（第一級：官方文件說明的機制）

- 精選摘要的定義「把一般搜尋結果的格式反過來，先顯示描述片段」，且可出現在相關問題群組裡｜https://developers.google.com/search/docs/appearance/featured-snippets｜2026-09-14｜curl 直接取得 HTTP 200，頁面標示 Last updated 2025-12-10 UTC
- 「How can I mark my page as a featured snippet?」官方回答是「You can't.」，由 Google 系統自行判斷｜https://developers.google.com/search/docs/appearance/featured-snippets｜2026-09-14｜同上
- 退出方式：nosnippet 擋掉所有摘要；data-nosnippet 擋特定文字；max-snippet 調短會降低出現機會，但官方明寫「doesn't guarantee」，也不提供確切的最短長度｜https://developers.google.com/search/docs/appearance/featured-snippets｜2026-09-14｜同上
- 點擊精選摘要會自動捲到頁面上出現在摘要裡的那一段；瀏覽器不支援或系統無法確定位置時才帶到頁面最上方｜https://developers.google.com/search/docs/appearance/featured-snippets｜2026-09-14｜同上
- 精選摘要出現的三個位置（搜尋結果最上方、「其他人也問」、知識圖譜資訊旁），以及「在你用手機或對裝置說話時特別有用」｜https://support.google.com/websearch/answer/9351707｜2026-09-14｜curl 直接取得 HTTP 200
- 相關問題群組（People Also Ask）的官方定義，以及「使用者展開問題時，看到的就是精選摘要」｜https://developers.google.com/search/docs/appearance/visual-elements-gallery｜2026-09-14｜curl 直接取得 HTTP 200，頁面標示 Last updated 2026-02-04 UTC
- speakable：Google 助理用它在智慧音箱回答主題新聞查詢，唸出段落時標示出處並把完整文章網址送到手機；文件標示 beta；只適用美國、英文內容與 Google Home｜https://developers.google.com/search/docs/appearance/structured-data/speakable｜2026-09-14｜curl 直接取得 HTTP 200，頁面標示 Last updated 2026-09-08 UTC，beta 字樣仍在
- AI 概覽／AI 模式沒有額外的出現條件、不需要特殊標記或機器可讀檔案；可能使用查詢展開（query fan-out）；兩者可能使用不同模型與技術；nosnippet、data-nosnippet、max-snippet、noindex 是可用的控制項｜https://developers.google.com/search/docs/appearance/ai-features｜2026-09-14｜curl 直接取得 HTTP 200，頁面標示 Last updated 2025-12-10 UTC
- 官方直接處理 AEO 與 GEO 兩個縮寫：「"AEO" stands for "answer engine optimization" and "GEO" for "generative engine optimization" ... From Google Search's perspective, optimizing for generative AI search is optimizing for the search experience, and thus still SEO.」並提醒評估第三方 AEO／GEO 建議與服務時對照官方指引｜https://developers.google.com/search/docs/fundamentals/ai-optimization-guide｜2026-09-14｜curl 直接取得 HTTP 200，頁面標示 Last updated 2026-07-10 UTC
- 同一份指南的「你不需要做的事」：llms.txt 等特殊檔案與標記、把內容切碎（chunking）、為了 AI 重寫內容、製造不真實的品牌提及、過度聚焦結構化資料；並寫明「There's no ideal page length」｜https://developers.google.com/search/docs/fundamentals/ai-optimization-guide｜2026-09-14｜同上
- 正面建議只到「用段落、章節與標題整理內容」，理由寫的是讀者好讀（"People generally appreciate it when web pages are organized by paragraphs and sections, along with headings"）｜https://developers.google.com/search/docs/fundamentals/ai-optimization-guide｜2026-09-14｜同上
- 精選摘要 2014 年 1 月推出（"When we introduced featured snippets in January 2014"），文章由 Danny Sullivan 於 2018 年 1 月 30 日發表｜https://blog.google/products-and-platforms/products/search/reintroduction-googles-featured-snippets/｜2026-09-14｜WebFetch 取得全文
- Search Console 的曝光、點擊、位置定義；停留在 Google 平台內部的點擊不計為點擊；精選摘要通常佔第 1 個位置｜https://support.google.com/webmasters/answer/7042828｜2026-09-14｜WebFetch 取得全文

## 流量相關：兩邊的說法都標了出處與範圍

- Google 自己說「featured snippets do indeed drive traffic」（2018-01-30 那篇）｜https://blog.google/products-and-platforms/products/search/reintroduction-googles-featured-snippets/｜2026-09-14｜WebFetch 取得全文
- 2025 年 8 月 6 日 Liz Reid（VP, Head of Google Search）：整體自然點擊量年對年大致持平、點擊品質提升；Google 未公開底層數據，屬內部資料｜https://blog.google/products-and-platforms/products/search/ai-search-driving-more-queries-higher-quality-clicks/｜2026-09-14｜WebFetch 取得全文並確認作者與日期
- 皮尤研究中心（2025-07-22）：出現 AI 摘要的造訪點擊一般搜尋結果 8%、未出現時 15%、點擊摘要內連結 1%；樣本 900 位美國成人、68,879 次 Google 搜尋，瀏覽資料 2025-03-01 至 03-31、搜尋結果擷取 2025-04-07 至 04-17；研究自述只涵蓋 Google｜https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/｜2026-09-14｜WebFetch 取得全文
- 正文沒有把任何一邊的數字推廣成「你的網站也會如何」，並在 callout 明寫本站沒有做過實測、不提供成效保證。

## 論文（一手）

- GEO: Generative Engine Optimization，Aggarwal、Murahari、Rajpurohit、Kalyan、Narasimhan、Deshpande；2023-11-16 投稿，v3 為 2024-06-28；提出 GEO-bench｜https://arxiv.org/abs/2311.09735｜2026-09-14｜WebFetch 取得摘要頁。本篇只寫「這個詞出自一篇論文」，論文的查詢集、指標與百分比數字留給 ai-search-geo 那一篇，不在本篇引用。

## 行銷內容（第三級：只證明有人這樣用，正文都寫明是誰說的）

- Ahrefs（SEO 工具商）行銷部落格，Ryan Law，2025-04-07：「GEO is 'generative engine optimization', LLMO is 'large language model optimization', AEO is 'answer engine optimization'. Three names for the same idea.」｜https://ahrefs.com/blog/geo-is-just-seo/｜2026-09-14｜WebFetch 取得全文並確認作者與日期
- HubSpot（行銷軟體商）部落格，Zoe Ashbridge，更新於 2026-07-31：「Some experts differentiate and use AEO when discussing for direct search results answers, like featured snippets. They'll use GEO when referring to AI chatbot citations.」、「Why isn't there a general consensus...」、「At HubSpot, we use AEO as a term that captures all initiatives to improve visibility in answer engines.」｜https://blog.hubspot.com/marketing/aeo-vs-geo｜2026-09-14｜WebFetch 取得全文
- Kalicube（行銷公司）自家網站主張「Answer Engine Optimization coined by Jason Barnard in 2017」，同一頁的圖又寫「Created by Jason Barnard, 2018」；同頁把 Featured Snippets、People Also Ask、Voice Results 列為 AEO 的目標介面｜https://kalicube.com/entity/answer-engine-optimization/｜2026-09-14｜WebFetch 取得全文
- 微軟新聞稿 2009-05-28：「Microsoft Corp. today unveiled Bing, a new Decision Engine and consumer brand, providing customers with a first step in moving beyond search」｜https://news.microsoft.com/source/2009/05/28/microsofts-new-search-at-bing-com-helps-people-make-better-decisions/｜2026-09-14｜curl 直接取得 HTTP 200

## 查不到、因此沒有寫死的項目

- **AEO 這個詞確切的提出年份**：只找得到 Kalicube 自家頁面的主張，而且同一頁 2017 與 2018 並存，沒有任何一手的中立記錄可以裁定。正文因此寫「同一頁一處寫 2017 年、另一處的圖寫 2018 年，自己就對不起來」，不採用任何一個年份當事實。
- **「結論先寫、用問答格式、一問一答版面」會不會讓頁面被選為答案**：Google 官方文件沒有任何一句支持這個因果，反而明寫不需要為了 AI 重寫內容、沒有理想頁長。正文把這些做法標成「業界普遍做法但沒有官方確認」，沒有承諾任何結果。
- **精選摘要所需的最短文字長度**：官方明寫不提供確切數字（受資訊、語言、平台影響），因此正文只寫「max-snippet 設太短就不會出現」，不給任何字數。
- 本次查證所有官網都以 curl 或 WebFetch 直接取得 HTTP 200，沒有需要改用 Wayback Machine 快照的情形。
