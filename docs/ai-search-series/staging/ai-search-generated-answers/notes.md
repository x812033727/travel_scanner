# 查證記錄：ai-search-generated-answers

查證日一律 2026-09-14。所有來源都是搜尋引擎或廠商自己的開發者文件、說明中心與官方部落格；
沒有引用任何代理商部落格作為事實依據，正文也沒有出現任何行銷來源的斷言。

讀取方式：本次全部網址都以 WebFetch 直接讀取成功（HTTP 200），沒有遇到 Cloudflare 403，
因此不需要 Wayback Machine 快照。唯一的例外是 OpenAI 的爬蟲文件，原網址
`https://platform.openai.com/docs/bots` 回 301，轉址到 `https://developers.openai.com/api/docs/bots`，
`sources` 記的是轉址後的官方網址（那是目前的正式位置，不是被擋之後的替代讀法）。

## 主張與來源

| 主張（正文寫法） | 來源網址 | 查證日 | 實際讀取方式 |
| --- | --- | --- | --- |
| AI 模式把問題拆成子題、同時對多個資料來源各自搜尋，再把結果合起來變成容易理解的回應 | https://support.google.com/websearch/answer/16011537 | 2026-09-14 | WebFetch 直接讀取；原句 "dividing your question into subtopics and searching for each one simultaneously across multiple data sources. It then brings those results together to provide an easy-to-understand response." |
| 官方用語是「查詢展開（query fan-out）」 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取；原句 "may use a 'query fan-out' technique — issuing multiple related searches across subtopics and data sources — to develop a response." |
| 生成回應的過程中，模型會找出更多支援的網頁，因此能顯示比傳統搜尋更廣的連結 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取；原句 "While responses are being generated, our advanced models identify more supporting web pages, allowing us to display a wider and more diverse set of helpful links associated with the response than with a classic web search." |
| 要出現在 AI 摘要或 AI 模式沒有額外要求，也不需要其他特別的最佳化 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取；原句 "There are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary." |
| 兩個功能可能使用不同的模型與技術，顯示的回應與連結會不一樣 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取；原句 "may use different models and techniques, so the set of responses and links they show will vary." |
| 支援連結的資格條件：已建立索引、有資格在搜尋中顯示摘要片段、符合技術需求 | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取；原句 "To be eligible to be shown as a supporting link in AI Overviews or AI Mode, a page must be indexed and eligible to be shown in Google Search with a snippet, fulfilling the Search technical requirements." |
| 搜尋中心列出的控制項只有 robots.txt、nosnippet、data-nosnippet、max-snippet、noindex 與 Google-Extended | https://developers.google.com/search/docs/appearance/ai-features | 2026-09-14 | WebFetch 直接讀取；原句 "To limit the information shown from your pages in Search, use nosnippet, data-nosnippet, max-snippet, or noindex controls." 與 "To limit AI training and grounding in some of Google's other systems, read more about Google-Extended."；該頁頁尾標示 Last updated 2025-12-10 UTC（正文未引用這個日期） |
| Gemini API 的 Grounding with Google Search 把流程寫成五步，引用把一段文字對應到一個來源網址 | https://ai.google.dev/gemini-api/docs/google-search | 2026-09-14 | WebFetch 直接讀取；五步原文依序為 "Your application sends a user's prompt…"、"The model analyzes the prompt and determines if a Google Search can improve the answer."、"If needed, the model automatically generates one or multiple search queries and executes them."、"The model processes the search results, synthesizes the information, and formulates a response."、"The API returns a final, user-friendly response that is grounded in the search results."；引用欄位原句 "Each url_citation annotation links a text segment (defined by start_index and end_index) to a source URL." 正文明寫這是開發者用的 API、不是 AI 摘要的內部實作 |
| nosnippet：不顯示文字摘要片段或影片預覽；適用所有形式的搜尋結果，並阻止內容成為 AI 摘要與 AI 模式的直接輸入 | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | 2026-09-14 | WebFetch 直接讀取；原句 "Do not show a text snippet or video preview in the search results for this page." 與 "This applies to all forms of search results (at Google: web search, Google Images, Discover, AI Overviews, AI Mode) and will also prevent the content from being used as a direct input for AI Overviews and AI Mode." |
| max-snippet：限制摘要片段字數，也限制可當成直接輸入的量；設 0 等同 nosnippet，設 -1 不限長度 | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | 2026-09-14 | WebFetch 直接讀取；原句 "Use a maximum of [number] characters as a textual snippet for this search result."、"0: No snippet is to be shown. Equivalent to nosnippet."、"-1: Google will choose the snippet length that it believes is most effective…"、"will also limit how much of the content may be used as a direct input for AI Overviews and AI Mode." |
| data-nosnippet：標在 span、div、section 上；該段 HTML 必須合法、標籤正確關閉 | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | 2026-09-14 | WebFetch 直接讀取；原句 "with the data-nosnippet HTML attribute on span, div, and section elements." 與 "To ensure machine-readability, the HTML section must be valid HTML and all appropriate tags must be closed accordingly." |
| data-nosnippet 那一段沒有寫到 AI 摘要與 AI 模式的直接輸入（正文據此明寫「文件沒寫，不替它補」） | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | 2026-09-14 | WebFetch 第二次針對 data-nosnippet 段落重讀，明確問「這一段有沒有寫到 AI 直接輸入」，回覆為沒有；該段只寫 "You can designate textual parts of an HTML page not to be used as a snippet."。這是「文件沒寫」的陳述，不是推測 |
| noindex：不在搜尋結果中顯示這個頁面、媒體或資源 | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | 2026-09-14 | WebFetch 直接讀取；原句 "Do not show this page, media, or resource in search results." |
| 要擋掉所有摘要片段（含精選摘要與一般摘要）就加上 nosnippet | https://developers.google.com/search/docs/appearance/featured-snippets | 2026-09-14 | WebFetch 直接讀取；原句 "To block all snippets (including featured snippets and regular snippets) from appearing for a given page, add the nosnippet rule to that page." |
| max-snippet 設低時精選摘要可能不出現，但官方寫明不保證 | https://developers.google.com/search/docs/appearance/featured-snippets | 2026-09-14 | WebFetch 直接讀取；原句 "Featured snippets will only appear if enough text can be shown to generate a useful featured snippet." 與 "Using a low max-snippet setting doesn't guarantee that Google will stop showing featured snippets for your page. If you need a guaranteed solution, use the nosnippet rule." |
| 被 data-nosnippet 標記的文字在精選摘要與一般摘要都不會出現 | https://developers.google.com/search/docs/appearance/featured-snippets | 2026-09-14 | WebFetch 直接讀取；原句 "Text marked by the data-nosnippet HTML attribute won't appear in featured snippets or regular snippets either." |
| 搜尋生成式 AI 控制：以資源為單位納入或排除；排除時內容不會被使用者看到、不會被連結、也不會協助接地 | https://support.google.com/webmasters/answer/16908024 | 2026-09-14 | WebFetch 直接讀取；排除選項原句 "Your site's content is prevented from being visible to users in Search generative AI features, including being linked to within these features and helping with grounding AI responses in these features." |
| 該控制適用的功能是 AI 摘要、AI 模式與 Discover 中的生成式 AI 功能 | https://support.google.com/webmasters/answer/16908024 | 2026-09-14 | WebFetch 直接讀取；頁面列出的三項為 AI Overviews、AI Mode、Generative AI features in Google Discover |
| 該控制不是排名或收錄訊號；改設定後一般要幾天才生效 | https://support.google.com/webmasters/answer/16908024 | 2026-09-14 | WebFetch 直接讀取；原句 "this control isn't used as a ranking or inclusion signal affecting other parts of Search" 與 "it generally takes a few days for your site's content to be excluded from the applicable Search generative AI features."；正文寫「幾天」而不寫確切數字，因為文件本身寫的是 a few days |
| Google-Extended 管的是訓練未來的 Gemini 模型與其他系統的接地，不影響搜尋收錄，也不是排名訊號 | https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers | 2026-09-14 | WebFetch 直接讀取；原句 "Google-Extended is a standalone product token that web publishers can use to manage whether content Google crawls from their sites may be used for training future generations of Gemini models" 與 "Google-Extended does not impact a site's inclusion in Google Search nor is it used as a ranking signal in Google Search."；適用產品列為 Gemini Apps、Vertex AI API for Gemini、Grounding in Gemini Apps、Grounding with Google Search on Vertex AI |
| 「AI 摘要」是 Google 搜尋的生成式功能，官方說明寫明回應可能出錯、要點連結查證（正文用來確立詞彙所指） | https://support.google.com/websearch/answer/14901683 | 2026-09-14 | WebFetch 直接讀取；原句 "You'll find AI Overviews in your Google Search results when our systems determine that generative AI can be especially helpful" 與 "AI Overviews can and will make mistakes." |
| 微軟在 2023 年 9 月 22 日公布 NOCACHE 與 NOARCHIVE：NOCACHE 的內容仍可能出現在 Bing Chat 答案中但只顯示網址、摘要片段與標題；NOARCHIVE 不會被納入答案也不會被連結；兩者的內容仍會出現在 Bing 搜尋結果 | https://blogs.bing.com/webmaster/september-2023/Announcing-new-options-for-webmasters-to-control-usage-of-their-content-in-Bing-Chat | 2026-09-14 | WebFetch 直接讀取微軟官方部落格；發布日期 2023-09-22；原句 "Content with the NOCACHE tag may be included in Bing Chat answers. We will only display URL/Snippet/Title in the answer."、"Content tagged NOARCHIVE will not be included in Bing Chat answers, not be linked to in the answers."、"content with the NOCACHE tag or NOARCHIVE tag will still appear in our search results" |
| Bing 在 2025 年 10 月 15 日宣布支援 data-nosnippet，並寫明它同時作用於搜尋摘要與 AI 生成的答案 | https://blogs.bing.com/webmaster/October-2025/Bing-Introduces-Support-for-the-data-nosnippet-HTML-Attribute | 2026-09-14 | WebFetch 直接讀取微軟官方部落格；發布日期 2025-10-15；原句 "gives webmasters, developers, and publishers precise control over what content appears in search results and AI-generated answers" 與 "You can apply the data-nosnippet attribute to any HTML element you want to exclude from Bing Search snippets or AI summaries." |
| OpenAI 用 robots.txt 區分用途：OAI-SearchBot 讓網站出現在 ChatGPT 的搜尋，GPTBot 對應訓練基礎模型的抓取；退出 OAI-SearchBot 的網站不會出現在 ChatGPT 搜尋的答案裡，但仍可能以導覽連結出現；文件沒有逐頁的摘要控制 | https://developers.openai.com/api/docs/bots | 2026-09-14 | WebFetch 讀取（原網址 platform.openai.com/docs/bots 回 301 轉址到此）；原句 "OAI-SearchBot is used to surface websites in search results in ChatGPT's search features."、"Sites that are opted out of OAI-SearchBot will not be shown in ChatGPT search answers, though can still appear as navigational links."、"GPTBot is used to crawl content that may be used in training our generative AI foundation models."；針對「有沒有等同 nosnippet 的逐頁控制」提問，回覆為文件未提及 |

## 查不到、因此改寫或不寫的項目

- **AI 摘要與 AI 模式的排序與挑選機制**：官方文件只寫到查詢展開與資格條件，沒有公布哪些訊號決定
  排序、也沒有公布支援連結怎麼挑。正文因此明寫「Google 沒公布 AI 摘要怎麼排序、怎麼挑連結」，
  並在圖解底部重申一次，全文沒有任何機制推測。
- **data-nosnippet 會不會阻擋 AI 的直接輸入**：Google 的 robots meta 文件在那一段沒有寫。
  正文與 callout 都寫成「文件沒寫，不替它補」，並把 Bing 有寫的那一版標明是微軟自己的部落格。
- **Search Console 生成式 AI 成效報表的欄位與定義**：
  `https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports` 只讀到封存清單的
  標題與月份，取不到內文，因此正文不引用該報表的任何細節，只把成效與報表的操作連到既有的
  `google-ai-overviews-for-site-owners`，並以官方文件為準。
- **Vertex AI 的 grounding 回應欄位（groundingChunks、groundingSupports）**：
  `cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview` 301 轉址後仍只取回導覽結構，
  拿不到欄位說明。正文因此改用 Gemini API 文件裡讀得到的五步流程與 url_citation 說法，
  不寫任何欄位名稱。
- **Bing 說明中心的 robots meta 支援清單**：`bing.com/webmasters/help/...` 只回頁面標題，
  取不到內文。正文因此只引用微軟官方部落格裡讀得到的 NOCACHE、NOARCHIVE 與 data-nosnippet，
  不列舉 Bing 支援的完整規則清單。
- **AI 摘要使用哪個模型版本**：官方產品說明沒有指名模型，正文也不寫模型名稱或版本號。

## 分級標記與不承諾成效

- 正文所有機制敘述都對應上表的一手來源，屬第一級（官方文件說明的機制）。
- 第二級（業界普遍做法但官方沒有說明）只出現在「怎麼判斷一句說法屬於哪一級」那一節，
  用來當判讀示範，並且明寫官方文件說沒有額外要求。
- 第三級（廠商或代理商的行銷主張）全文沒有被當成事實依據使用；該節寫明引用時要標明是誰說的。
- 全文沒有任何前後對照數字、成效百分比或案例，沒有一句話承諾排名、索引、引用或流量結果；
  示例段落明寫「本文沒做過實測，也不給成效數字」。
- 唯一以第一人稱出現的敘述是查證行為本身（讀了哪份文件），沒有聲稱測試過任何功能。

## 用語

- 系列統一用語：接地（grounding）、提示詞、代理、上下文視窗；台灣用語：網路、資料、影片、使用者、品質。
- 功能名稱照 Google 繁體中文說明中心：AI 摘要（AI Overviews）、AI 模式（AI Mode）、
  精選摘要（featured snippets）、摘要片段（snippet）。
- 控制項名稱一律保留英文原字串（nosnippet、max-snippet、data-nosnippet、noindex、Google-Extended），
  因為那是要寫進網頁的字面值。
