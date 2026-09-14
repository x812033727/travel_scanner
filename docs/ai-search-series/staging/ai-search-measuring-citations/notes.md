# 查證記錄：ai-search-measuring-citations

查證日一律 **2026-09-14**。格式：`主張｜來源網址｜查證日｜實際讀取方式`。
本環境對部分官網回 403 或只回 SPA 外殼，實際讀法逐條記在最後一欄；`sources` 一律寫原始網址。

## referrer 規範

- 預設 referrer policy 是 `strict-origin-when-cross-origin`（規範原文：「The default referrer
  policy is "strict-origin-when-cross-origin".」）｜https://w3c.github.io/webappsec-referrer-policy/
  ｜2026-09-14｜curl 取原始 HTML 後抽文字；文件自標 Editor's Draft, 20 March 2026
- `no-referrer` 時 `Referer` 標頭整個省略（「The header Referer will be omitted entirely.」）
  ｜同上｜2026-09-14｜同上
- 跨站請求只送來源 origin；來源是 potentially trustworthy URL 而目的地不是時不送 Referer
  ｜同上｜2026-09-14｜同上（第 3.7 節）
- **版本差異（正文未寫，留給校閱）**：w3.org/TR 的快照是 2017-01-26 的 Candidate Recommendation，
  該版寫的預設值是 `no-referrer-when-downgrade`。正文採用現行編輯草案的值，兩個網址都放進 `sources`
  ｜https://www.w3.org/TR/referrer-policy/｜2026-09-14｜curl 取原始 HTML，確認標頭日期與 CR 狀態

## Google：搜尋結果送出的 referrer

- Google 用 referrer meta 標籤簡化搜尋結果送出的來源網址，網站會看到 Google 的裸主機名
  （原文：「You may start to see origin referrers—Google's home pages…」「detecting bare Google
  host names using SSL」）｜https://developers.google.com/search/blog/2012/03/upcoming-changes-in-googles-http
  ｜2026-09-14｜curl 取原始 HTML 後抽文字；文章日期 Monday, March 19, 2012（正文寫 2012 年 3 月 19 日）

## Google：生成式 AI 成效報表

- 發布日 Wednesday, June 3, 2026；文中加註「As of August 31, 2026, we've rolled out these insights
  to all websites worldwide.」（正文寫 2026 年 6 月 3 日、2026 年 8 月 31 日）
  ｜https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports｜2026-09-14
  ｜curl 取原始 HTML 後抽文字
- 報表列出的資訊是 Impressions、Pages、Countries、Devices、Dates（正文寫「曝光，可依頁面、國家、裝置分組」）
  ｜同上，並與說明中心交叉比對｜2026-09-14｜同上。同一篇寫「adding additional metrics over time」，
  所以正文不寫報表有點擊或排名指標
- 報表涵蓋 AI Overviews 與 AI Mode；「Search Console doesn't include data from experiments in
  Search Labs」；「the usual data limitations (1,000 row limitation, time period, etc)…also apply」；
  最新資料可能是 preliminary；資料多半歸到 canonical URL；曝光定義是「how many times links to your
  site were shown to a user in a generative AI feature on Google Search」
  ｜https://support.google.com/webmasters/answer/16984139｜2026-09-14｜curl（去掉 `?hl=en` 追蹤參數後仍可讀）
- 匿名化查詢：「Anonymized queries are those that aren't issued by more than a few dozen users over a
  two-to-three month period.」表格不列、圖表總數會算，所以各列加總不等於總數；介面匯出上限 1,000 列，
  Search Analytics API 上限每天每站每種搜尋類型 50,000 列（**正文最後只保留 1,000，50,000 因字數刪掉，
  `sources` 仍保留這筆**）｜https://developers.google.com/search/blog/2022/10/performance-data-deep-dive
  ｜2026-09-14｜curl 取原始 HTML 後抽文字；文章日期 Wednesday, October 19, 2022
- 「Position value is the average position for all searches. For your specific search your position
  might be different than the average because of many variables, such as your search history,
  location, and so on.」（正文「自己搜尋看到的位置可能因搜尋紀錄、所在地而與報表平均值不同」）
  ｜https://support.google.com/webmasters/answer/7042828｜2026-09-14｜curl
- 「You must verify ownership of your property before you can see any data for it」
  ｜https://support.google.com/webmasters/answer/9008080｜2026-09-14｜WebSearch 限定 support.google.com
  取摘要（該頁 curl 回 SPA 外殼）。正文只用「要先驗證網站所有權才看得到」這一句，沒有延伸

## Google：AI 摘要與 AI 模式本身

- 「AI Mode and AI Overviews may use different models and techniques, so the set of responses and
  links they show will vary.」；同頁另寫「Indexing and serving isn't guaranteed.」
  ｜https://developers.google.com/search/docs/appearance/ai-features｜2026-09-14｜WebFetch
- AI 模式的 Personal Intelligence「references previous searches and activity saved in your Search
  Services History」（正文：個人化功能會參考先前的搜尋與搜尋服務紀錄裡的活動）
  ｜https://support.google.com/websearch/answer/16011537｜2026-09-14｜curl（桌面版分頁）

## OpenAI

- OAI-SearchBot「used to surface websites in search results in ChatGPT's search features」；
  GPTBot「used to crawl content that may be used in training our generative AI foundation models」；
  ChatGPT-User「used for certain user actions in ChatGPT and Custom GPTs…Because these actions are
  initiated by a user, robots.txt rules may not apply」
  ｜https://developers.openai.com/api/docs/bots｜2026-09-14｜WebFetch；舊網址
  platform.openai.com/docs/bots 回 301 轉到這個網址
- 「ChatGPT automatically includes the UTM parameter utm_source=chatgpt.com in referral URLs」，
  並說允許 OAI-SearchBot 的發布者可用 Google Analytics 這類工具追蹤。**這是 UTM 查詢參數，不是
  `Referer` 標頭**，正文特別把兩者分開｜https://help.openai.com/en/articles/12627856-publishers-and-developers-faq
  ｜2026-09-14｜WebFetch，網址後加 `.json` 才讀得到全文
- seed 參數：「repeated requests with the same seed and parameters should return the same result.
  Determinism is not guaranteed」｜https://developers.openai.com/api/docs/api-reference/chat/create
  ｜2026-09-14｜WebFetch

## Perplexity

- PerplexityBot「designed to surface and link websites in search results on Perplexity…It is not
  used to crawl content for AI foundation models」；Perplexity-User「supports user actions within
  Perplexity…Since a user requested the fetch, this fetcher generally ignores robots.txt rules」
  ｜https://docs.perplexity.ai/docs/resources/perplexity-crawlers｜2026-09-14｜WebFetch
- 該頁**沒有**說明使用者從 Perplexity 點出去時會不會送 referrer。正文因此寫「其他助理是否送出
  referrer，查證時沒找到同等級的官方說明，以官方文件為準」

## Bing / Microsoft

- AI Performance 公開預覽公告，日期 February 10, 2026（正文只寫「2026 年 2 月」）；涵蓋「Microsoft
  Copilot, AI-generated summaries in Bing, and select partner integrations」；Total Citations
  「without indicating placement or presentation within a specific answer」；Average Cited Pages
  「does not indicate ranking, authority, or the role of any page within an individual answer」；
  Page-level citation activity「reflects how often pages are cited, not page importance, ranking,
  or placement」；Grounding queries「The data shown represents a sample of overall citation activity.」
  ｜https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
  ｜2026-09-14｜curl 取原始 HTML 後抽文字
- `https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c` 是 JS 單頁應用，curl 只拿得到外殼，
  WebFetch 也只回標題。**正文因此只採用官方部落格那一篇的字句**，沒有引用 help 頁的任何說法
- 另有 Microsoft Advertising 的部落格帶著轉換率百分比。那是廣告產品的行銷內容，**沒有採用、
  沒有寫進正文、沒有放進 `sources`**

## 沒有採用的東西

- 任何「約有 X% 的 AI 流量無法歸因」類型的數字：查不到一手來源，一個都沒寫
- 任何代理商或 AI 能見度工具廠商的部落格：沒有當事實依據，也沒有當佐證引用。
  正文第六節只講方法論（樣本、可稽核、可重現），不點名任何公司，唯一提到廠商的那句寫成
  「廠商的行銷資料怎麼說是一回事」，主詞明確且標明是行銷內容
- 各家 AI 助理的 referrer 行為（除了 OpenAI 那條 UTM 參數的官方說明）：查不到官方文件，
  正文寫「以官方文件為準」

## 主張分級檢查

- **官方文件說明的機制**：referrer 預設政策與省略條件、Google 2012 的 referrer 簡化、
  生成式 AI 成效報表的涵蓋範圍與限制、匿名化查詢、爬蟲與使用者觸發抓取的區分、
  utm_source=chatgpt.com、seed 不保證決定性、AI 模式個人化、Bing 引用次數的但書。
  正文句子都帶「官方文件／說明中心／規範寫明」。
- **業界普遍做法但無官方確認**：只有一條——在自己散布的連結上另外加追蹤參數，
  正文寫「業界普遍會另外加自己的追蹤參數，官方文件沒說明它在 AI 介面的效果」。
- **廠商行銷主張**：只有第六節那一句，主詞是「廠商的行銷資料」，並明說本文不評論任何公司。
- 全文沒有任何一句承諾排名、索引、引用或流量結果；導言第二段明寫本站沒做過實測。

## 圖上的數字

`diagram-1.svg` 的文字節點只出現一個數字：右下角署名的 `2026`。正文多處有 2026（查證日、
報表日期），`missing_diagram_numbers` 回傳空清單。`hero.svg` 沒有任何數字。
