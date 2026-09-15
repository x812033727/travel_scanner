# ai-search-eeat 查證記錄

查證日一律 2026-09-14。格式：`主張｜來源網址｜查證日｜實際讀取方式`。

## 讀取方式說明

- `guidelines.raterhub.com` 的 PDF 會 302 轉到 `static.googleusercontent.com`；WebFetch 不自動跟隨跨網域轉址，改抓轉址目標，回來是 8.6 MB 的 PDF 二進位檔，本地用 pypdf 抽出全文（182 頁）後逐節閱讀。`sources` 仍寫原始的 `guidelines.raterhub.com` 網址。
- `services.google.com/fh/files/misc/hsw-sqrg.pdf`（Google 自己出的《Search Quality Rater Guidelines: An Overview》）同樣以 WebFetch 取得 PDF 後本地抽文字。
- `developers.google.com/search/blog/2022/12/...` 的內文是前端渲染，WebFetch 只拿得到導覽與日期；Wayback Machine 在本環境被擋（WebFetch 與 curl 皆不可用），改以限定 `developers.google.com` 的 WebSearch 取摘要交叉比對，確認日期與該次改版內容。
- 其餘 `developers.google.com` 文件以 WebFetch 直接讀取，頁尾的 Last updated 日期一併記下。

## 一手來源（官方文件說明的機制）

- 指南現行版本封面日期為 September 11, 2025，頁尾標示 Copyright 2025，全文 182 頁｜https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf｜2026-09-14｜PDF 轉址後本地抽文字，第 1 頁與各頁頁尾
- E-E-A-T 定義在第 3.4 節「Experience, Expertise, Authoritativeness, and Trust (E-E-A-T)」，第 26 頁｜同上｜2026-09-14｜PDF 目錄與第 26 頁
- 「The most important member at the center of the E-E-A-T family is Trust.」「If a page is untrustworthy for any reason, it has low E-E-A-T.」金融詐騙的例子在同節｜同上｜2026-09-14｜PDF 第 26–27 頁
- 第 0.1 節：「No single rating can directly impact how a particular webpage, website, or result appears in Google Search, nor can it cause specific webpages, websites, or results to move up or down on the search results page.」「Using ratings to position results on the search results page would not be feasible, as humans could never individually rate each page on the open web.」「Instead, ratings are used to measure how effectively search engines are working... Ratings are also used to improve search engines by providing examples of helpful and unhelpful results」｜同上｜2026-09-14｜PDF 第 6 頁
- Page Quality 用滑桿給整體評分，等級為 Lowest / Low / Medium / High / Highest，另有 Lowest+、Low+、Medium+、High+ 半級；表上沒有任何 E-E-A-T 欄位｜同上｜2026-09-14｜PDF 第 19 頁（3.0 Overall Page Quality Rating）
- 第 5.6 節：「E-E-A-T assessments should be based on the MC itself, the information you find during reputation research, verifiable credentials, etc, not just website or content creator claims of "I'm an expert!".」自我介紹誇大或輕微誤導時用 Low｜同上｜2026-09-14｜PDF 第 63 頁
- 第 4.5.1 節：對需要高度信任的頁面，關於責任歸屬的資訊不足或造假是 Lowest 的理由｜同上｜2026-09-14｜PDF 第 35 頁
- 第 4.6.4 節 Site Reputation Abuse 定義：第三方內容主要因為宿主網站既有的排名訊號而被刊登｜同上｜2026-09-14｜PDF 第 41 頁
- 第 3.4 節的名聲調查是「What others say about the website or content creators: Look for independent reviews, references, news articles...」，方向是別人怎麼說這個網站｜同上｜2026-09-14｜PDF 第 27 頁
- 附錄二 Guideline Change Log 只涵蓋 September 2023 – September 2025（列出 September 2025、January 2025、February 2024、November 2023），2022 年那次改版不在表上｜同上｜2026-09-14｜PDF 第 182 頁
- 約 16,000 名外部評分者；任務分 Page Quality 與 Needs Met 兩種；「no single rating – or single rater – directly impacts how a given page or site ranks in Search」｜https://services.google.com/fh/files/misc/hsw-sqrg.pdf｜2026-09-14｜PDF 本地抽文字，第 15、16、17、18、34 頁；文件封面標示 November 2023
- 「While E-E-A-T itself isn't a specific ranking factor, using a mix of factors that can identify content with good E-E-A-T is useful.」「Search raters have no control over how pages rank. Rater data is not used directly in our ranking algorithms.」「Of these aspects, trust is most important.」頁面標示 Last updated 2025-12-10 UTC｜https://developers.google.com/search/docs/fundamentals/creating-helpful-content｜2026-09-14｜WebFetch 直接讀取
- Experience 是 2022 年 12 月 15 日那則公告所屬的改版加入的，標題為〈Our latest update to the quality rater guidelines: E-A-T gets an extra E for Experience〉｜https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t｜2026-09-14｜WebFetch 取得日期與標題（內文為前端渲染，未取得全文），再以限定 developers.google.com 的 WebSearch 交叉確認日期與內容
- 官方排名系統指南列出 BERT、MUM、RankBrain、link analysis systems and PageRank、neural matching、freshness systems 等，沒有任何名為 E-E-A-T 或 E-A-T 的系統；該頁自陳只列「some of our more notable ranking systems」。Last updated 2025-12-10 UTC｜https://developers.google.com/search/docs/appearance/ranking-systems-guide｜2026-09-14｜WebFetch 直接讀取
- 結構化資料功能總覽列出 Article、Breadcrumb、Product、Review snippet、Profile page 等型別，沒有任何一種對應 E-E-A-T、expertise、authority 或 trust。Last updated 2026-06-15 UTC｜https://developers.google.com/search/docs/appearance/structured-data/search-gallery｜2026-09-14｜WebFetch 直接讀取
- Article 結構化資料有 author 屬性（Person 或 Organization，建議含 author.name、author.url）；該頁寫明 Google 不保證使用結構化資料的功能一定會出現在搜尋結果裡。Last updated 2026-09-08 UTC｜https://developers.google.com/search/docs/appearance/structured-data/article｜2026-09-14｜WebFetch 直接讀取
- 連結濫發包含買賣連結、過度的連結交換、以自動程式建立連結、低品質目錄或書籤網站連結。Last updated 2026-08-28 UTC｜https://developers.google.com/search/docs/essentials/spam-policies｜2026-09-14｜WebFetch 直接讀取

## 行銷主張（第三級，正文已標明是誰說的）

- 恆遠數位科技（ForeverWebs，販售 SEO 服務）2026 年 4 月 6 日的文章，標題稱 E-E-A-T 為「2026 年 Google 最重視的排名因素」，內文卻寫「嚴格來說，E-E-A-T 不是像 PageSpeed 或反向連結那樣可以直接量測的排名因子」｜https://foreverwebs.com/blog/eeat-google-ranking-guide-2026｜2026-09-14｜WebFetch 直接讀取；僅作為「確實有人這樣用這個詞」的佐證，不作事實依據
- Whoops SEO（販售 SEO 成長代理服務）的文章寫「它不是一條獨立演算法，也不是一個可直接量測的分數」，接著主張「對排名的影響是間接、緩慢，但長期累積下來非常實質」｜https://seo.whoops.com.tw/what-is-eeat/｜2026-09-14｜WebFetch 直接讀取；同上，僅作用詞佐證

## 查不到而改寫的項目

- 指南是否有 2026 年的新版：以限定 google.com／developers.google.com 的 WebSearch 查詢，未見 2025 年 9 月之後的改版公告；線上 PDF 於查證日仍為 September 11, 2025 版。正文只寫「查證日取得的版本」，不宣稱那是最後一版。
- 2022 年 12 月那則公告的內文段落無法逐字取得（前端渲染、Wayback 被擋）。正文只引用公告的日期與標題這兩項可交叉確認的事實，不引述內文字句。
- Google 是否在內部使用與 E-E-A-T 相關的訊號：官方只寫「E-E-A-T 本身不是一個特定的排名因素」與「用一組能辨識出具備良好 E-E-A-T 的內容的因素是有用的」。正文照抄這兩句，並寫明排名系統清單能證明的是「官方沒有公布這樣一個系統」，其餘以官方文件為準，不推測。

## 圖上出現的數字

- `diagram-1.svg` 只有一個數字：版權行的 `2026`。正文有「2026 年 9 月 14 日」「2026 年 9 月」「2026 年 8 月 28 日」「2026 年 4 月 6 日」。
- `hero.svg` 不含任何數字。
