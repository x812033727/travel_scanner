# 文章架構：分類、搜尋、互連與 SEO/AEO/GEO

站主 2026-09-15 核准的文章系統重整計畫。`docs/travel-guides.md` 仍是文章系統的規格本體；
這份文件記錄目標架構、分階段的任務、分類詞彙與已做的決策，讓後續每張任務有同一份地圖可看。

## 為什麼

- 943 篇內容包（life 818、howto 106、intel 19）用的是為幾十篇設計的架構。生活分享只有 8 個扁平主題，
  `tutorial` 掛在 659 篇、`ai` 529 篇，主題 chip 對讀者已無導覽意義；旅遊 33 個目的地沒有「國家」這層。
- 沒有公開搜尋：只有 kind／section／destination／topic 篩選。
- 互連分裂：`ArticleInline`（167 篇）與原始 `https://mokaair.com/...` 連結（743 篇）並存；「相關文章」只有
  系列目錄與自動規則；81 篇名詞解說與 `docs/ai-terms-series/aliases.json` 沒有任何自動連結。
- SEO 基礎有（canonical、hreflang、JSON-LD、llms.txt），但沒有可見麵包屑、沒有 answer-first 摘要，
  robots 連會引用來源的 AI 搜尋爬蟲也擋掉。

## 已確認的決策

| 決策 | 選擇 |
| --- | --- |
| AI 爬蟲 | 放行會引用來源的搜尋型爬蟲（PerplexityBot、ClaudeBot、OAI-SearchBot），續封純訓練用（GPTBot、CCBot、Google-Extended、Bytespider…）；任務 `robots-ai-crawler-switch` |
| 名詞自動連結 | 寫入內容包（authoring-time 工具產生可審閱 diff），不做渲染時比對 |
| 搜尋 | 伺服器端 Postgres：索引表 + pg_trgm；SQLite 測試以同一 `LIKE` 對等；不用 tsvector（無法切中日韓詞） |
| 主題層級 | 兩層。`tutorial` 降為橫向標籤，不當父主題；新父主題 `website`、`marketing` |
| URL | 全部既有 URL 不變，只新增頁面（主題 hub、搜尋結果頁） |

## 目標架構

```
旅遊攻略 /guides                          生活分享 /life
├─ 主題 hub /guides/topics/{topic}        ├─ 主題 hub /life/topics/{topic}      ← 可索引、有導言、子主題 chips
├─ 國家 → 目的地 分組（DestinationProfile.country）│   └─ 兩層主題（guide_topics.parent_id）
├─ 系列 hub（既有 series 機制）            ├─ 系列／教學中心 列（series_registry.json）
└─ 文章頁                                 └─ 文章頁
    ├─ 可見麵包屑（專區 › 主題 › 文章）＋ BreadcrumbList
    ├─ 重點摘要（summary block，answer-first）→ JSON-LD abstract + speakable
    ├─ 內文名詞連結（ArticleInline + 定義卡 popover）
    ├─ 延伸閱讀（編輯 related → 自動：子主題 › 主題 › 目的地 › 系列）＋ 引用本文的文章
    └─ 既有：ToC、系列導覽、TravelCrosslinks、來源

搜尋：header 搜尋框（桌機欄位＋⌘K；手機 icon → sheet）→ typeahead（BFF /api/travel/guides/search）
      → 結果頁 /{locale}/search/articles?q=&section=（noindex, follow；純 GET form，無 JS 也可用）
```

分類軸：`kind`（URL）× `destination`（旅遊；國家分組不需新欄位）× `topic`（兩層）× `series`（檔案制＋登錄檔）。

## 分階段與任務

任務都在 `tasks/open/`，`npm run tasks -- list` 可看；id 前綴 `2026-09-15-`。scope 刻意窄，內容批次用前綴或明列檔案。

### Phase 0 — 前置（既有任務）
`2026-09-14-pack-ingest-urlopen-scheme`（review，持有 `pack_ingest.py`）→ `2026-09-14-guide-listing-curated-order`
→ `2026-09-14-sitemap-split-before-1000-rows`（P1；吸收 `2026-09-14-guide-sitemap-capacity`）→ `2026-09-12-guide-topic-admin-crud`
（2026-09-16 落地：`POST/PUT /admin/guides/topics`，`TopicCreate/Update` 帶 `parent_slug` 與 `descriptions`；後台「新增主題」表單）。

### Phase 1 — 分類架構（本 PR 落地）
| 任務 | 內容 |
| --- | --- |
| `guide-topic-hierarchy-api` | 0076：`parent_id`、`descriptions_json`、兩個新父主題與 23 個子主題種子；`?topic=` 含子主題；`?country=`；`GET /guides/destinations`；保留 slug |
| `guide-retopic-cli` | `pack_cli retopic`：依前綴與系列成員提案，`--apply` 只改 `topics`。已對 `ai-term-`、`claude-code-`、`codex-`、`gemini-`、`ai-news-`、`ai-search-`、`wordpress-`、`woocommerce-`、`chatgpt-` 共 430 篇套用 |
| `content-retopic-life-remaining-a-m` / `-n-z` / `content-retopic-finance` | 2026-09-16 已審 367 筆提案並套用；21 篇留在單層父主題（productivity／daily／software） |
| `series-registry` | `series_registry.json` + `GET /guides/series` |
| `topic-hub-pages-web` | 主題 hub 頁、chips 改連 hub、`?topic=` canonical、sitemap 主題列、`docs/seo.md` |
| `guides-hub-destinations-by-country-web` | 旅遊 hub「依目的地瀏覽」 |
| `llms-txt-topic-hubs-and-series` | llms.txt 列父主題與系列（等 aio 任務合併） |

### Phase 2 — 搜尋（已落地，同一分支）
| 任務 | 內容 |
| --- | --- |
| `guide-search-api` | 0077：`guide_search_entries`（發布寫入、撤下刪除，同一交易）與 `guide_article_aliases`；`GET /guides/search`（LIKE 子字串 AND、命中位置加權、別名／標題精確命中置頂 `best_match`）；PostgreSQL 建 pg_trgm GIN；`guides-search-reindex`、`guides-aliases-seed` CLI；限流 fail-open 120/60s |
| `article-search-results-page-web` | `/search/articles?q=&section=&offset=`：純 GET 表單、noindex/follow、`<mark>` 標示、專區 chips、offset 分頁、422／故障分開文案、空結果列主題與系列 |
| `site-search-header-web` | 桌機 header combobox typeahead（≤6 筆＋查看全部）、⌘K／Ctrl+K 與手機 icon 開同一個 sheet、頁尾連結 |

細節見 `docs/travel-guides.md`「Search」。別名種子這次一併做了（`app/guides/aliases.py`）；
`guide-aliases-seed-and-pack-field` 剩內容包欄位、後台欄位與 `docs/ai-suffix-keywords.md` 來源。

### Phase 3 — 互連（已落地，同一分支；內容第一批已套）
| 任務 | 內容 |
| --- | --- |
| `guide-aliases-seed-and-pack-field` | `ArticlePack.aliases`（≤12／語系）走 taxonomy 匯入、後台可編；`guides-aliases-seed` 加 `docs/ai-suffix-keywords.md`（`keyword`）來源。同語系別名多篇共用不 409（Phase 2 決策） |
| `pack-autolink-and-relink-cli` | `app/guides/autolink.py`；`pack_cli relink`（原始站內 URL → article inline）與 `autolink`（名詞第一次出現連到詞條，每目標一次、≤8／篇、ASCII 詞界、重跑 no-op）；lint `raw_internal_url` |
| `article-links-table-and-related-api` | 0078 `guide_article_links`（inline 列發布時寫、撤下時刪；related 列編輯指定）；`PublicArticle += related／backlinks／aliases`、`ArticleReference.description`；`guides-links-rebuild`、`guides-links-check` |
| `term-link-popover-related-grid-web` | `<TermLink>` 定義卡、`<RelatedGrid>`／`<Backlinks>`、後台別名與 related 欄位；順手做掉 `heading-anchors-for-h3`（`section-N-M`） |
| `content-relink-autolink-life` | 第一批 `ai-term-`／`ai-search-` 89 篇：317 條 URL 轉換、220 條名詞連結；其餘前綴分批 |

細節見 `docs/travel-guides.md`「Links」。全庫 `relink --dry-run`：742 篇、4,027 條可轉、552 條保留（551 條非文章 URL、1 條自連）。

### Phase 4 — SEO / AEO / GEO（機制已落地，同一分支；內容由編輯另寫）
| 任務 | 內容 |
| --- | --- |
| `summary-and-faq-blocks-api` | `SummaryBlock`（2–5 句、至多一個、在第一個標題前）與 `FaqBlock`（2–10 題、至多一個）；lint `no_summary`；索引納入；`PublicArticle.term_set` |
| `summary-faq-definedterm-jsonld-web` | 摘要卡 `#article-summary`、FAQ `<details>`；JSON-LD `abstract`＋`speakable`、`FAQPage`（只從 faq 區塊）、`DefinedTerm`；後台可加兩種區塊 |
| `article-breadcrumb-visible-web` | 每篇文章可見麵包屑：專區 › 父主題 › 子主題 › (系列) › 標題，與 `BreadcrumbList` 同一條 trail |
| `robots-ai-crawler-switch` | `AI_CRAWLER_POLICY=block\|allow-search\|allow`（預設 allow-search，每次請求讀取）；`docs/seo.md` 記錄 |
| `heading-anchors-for-h3` | 已在 Phase 3 做掉（`section-N-M`） |

**上線順序**：web 先部署（渲染器與 guard），之後才發布含 summary／faq 的內容；
`content-summary-howto-and-life`（編輯撰寫摘要與 FAQ）與 `2026-09-14-answer-first-howto-descriptions` 留給內容階段。

### Phase 5 — UI/UX（2026-09-16 落地）
| 任務 | 內容 |
| --- | --- |
| `guide-listing-curated-order` | `GET /guides?sort=latest\|curated`；`/life`、hub 精選攻略、`/guides/howto` 用 curated；舊 cursor 被拒導回第一頁 |
| `guides-hub-redesign-web` | `HubHero`（搜尋）→ `TopicTiles` → 精選攻略（首張 featured 卡）→ 最新情報 → 依目的地 |
| `life-hub-redesign-web` | 同構；三段手寫 aside 由登錄檔列取代；**開頭先列「最新新聞」（`ai-news`，最新在前，站主 2026-09-16 要求）** |
| `listing-toolbar-web` | `ListingToolbar`（chips、`?sort=`）與 `ListingEmpty`（附搜尋）；md 以上 sticky |
| `article-reading-polish-web` | `GuideCard` `compact`／`featured`；`.app-term-link`／`.app-term-card`／`.app-summary-card` 以 token 寫；延伸閱讀格距；系列上下篇雙欄 |
| `llms-txt-topic-hubs-and-series` | `/llms.txt` 多 `### Topics`（父主題、篇數最多的語系）與 `### Series` |
| 篇數與課序（2026-09-16） | 讀者看得到的地方一律不顯示目錄大小與課程序號：站主的理由是「會一直增加」，顯示出來就一直是錯的。`TopicOption.count`／`counts`、`SeriesEntry.number`、`GuideSearchResult.total`、`DestinationFacet.count`、`SitemapSummary.counts` 全部留在 wire 上，因為可見性、`noindex`、hreflang、sitemap、排序、上下篇與分頁都靠它們 —— 拿掉的只有畫面 |
| 新聞日期與新聞清單（2026-09-16） | `guide_articles.news_date`（migration `0079_guide_news_date`）＋`GET /guides?sort=news`（新聞日期由新到舊、無日期排最後）。生活分享首頁「最新新聞」改為依新聞日期最新 20 條、一條一行（日期＋標題）、不顯示主題描述；`/life/topics/ai-news` 同樣一條一行、沒有排序切換。顯示的是新聞發生的日期，不是發布或更新時間 —— 新聞分批匯入，同批發布時間幾乎一樣 |
| 系列搬進主題（2026-09-16） | `SeriesRow` 從兩個 hub 移到 `renderTopicHub`：每個系列在 `series_registry.json` 都指定一個（子）主題，子主題頁顯示自己的，父主題頁蒐集底下所有子主題的 |
| sitemap 上限 | 每專區×語系超過 5,000 列自動編號子檔，API `offset`；lint 不再預警 |

檔案先後序（避免 scope 衝突）：`service.py/router.py/schemas.py`：1.1 → registry → search → links → blocks；
`admin_service.py`：1.1 → crud → search → aliases → links；`content-blocks.tsx`：heading-anchors → term-link → jsonld；
`structured-data.ts/article-page.tsx`：aio(review) → term-link → jsonld → breadcrumb；`pack_ingest.py`：urlopen(review) → autolink → blocks。

## 分類詞彙（0076 種子；標籤在 `app/guides/taxonomy.py`，改種子即可）

**生活分享**：`software`、`gadgets`、`productivity`、`daily`、`misc` 維持單層；`tutorial` 保留於資料但不作導覽。

0079 又加了兩個新聞垂直：`crypto` 掛在 `finance` 底下（同一個 YMYL 主題、同一條免責規則），`tech-news` 掛在新父主題 `tech` 底下。`tech` 沒有拿 `gadgets` 或 `software` 改造：前者是 3C 裝置、後者是 App，而晶片、電信與平台法規兩邊都不是，上面那句「維持單層」也因此仍然成立。

| 父主題 | 子主題 | 吸收（`retopic` 規則摘要） |
| --- | --- | --- |
| `ai` AI 工具 | `ai-terms` AI 名詞解釋 | `ai-term-*`、詞彙表 hub、`*-explained` 概念篇 |
| | `ai-news` AI 新聞與趨勢 | `ai-news-*` |
| | `ai-search` AI 搜尋與 GEO | `ai-search-*`、`google-ai-overviews-*`、`zero-click-*` |
| | `ai-chat` 對話助理 | `chatgpt-*`、非 Code 的 `claude-*`、非 CLI/API 的 `gemini-*`、`deepseek-*`、`notebooklm-*`… |
| | `claude-code` / `codex` / `gemini-dev` | 各系列前綴與目錄成員 |
| | `ai-coding` AI 寫程式與本機模型 | `ai-coding-*`、`ollama-*`、`local-*`、`gguf-*`、`whisper-*`… |
| | `ai-create` AI 圖片、影片與聲音 | `ai-image-*`、`ai-video-*`、`midjourney-*`、`suno-*`… |
| | `ai-work` AI 工作應用 | `ai-for-*`、`ai-meeting-*`、`n8n-*`、`zapier-*`… |
| | `ai-safety` AI 安全、隱私與法規 | `ai-privacy-*`、`ai-scams-*`、`ai-regulation-*`… |
| | `ai-plans` AI 方案與費用 | `ai-free-vs-paid-*`、`ai-api-pricing-*`、`openrouter-*`… |
| `website` 架站與電商（新） | `wordpress` / `woocommerce` / `web-basics` | `wordpress-*` 與主題、主機前綴；`woocommerce-*`；`domain-*`、`dns-*`、`website-*`、`css-*`… |
| `marketing` 行銷與 SEO（新） | `seo` / `ads` / `content-marketing` | `seo-*`、SEO 工具、技術 SEO；`google-ads-*`、`adsense-*`、`affiliate-*`；`content-marketing-*`、`brand-*`、`marketing-*`… |
| `finance` 理財與金錢 | `finance-basics` / `banking` / `credit` / `tax-insurance` / `investing` / `crypto`（0079） | 財經批次 01／02／02／03–04／05–06；`crypto-news-*`、`bitcoin-*`、`stablecoin-*` |
| `tech` 科技與產業（0079 新增） | `tech-news` | `tech-news-*` |

**旅遊**：主題不加子層；第二軸為國家 → 目的地（`DestinationProfile.country` → `japan`、`south-korea`、`taiwan`、`thailand`、`vietnam`、`singapore`、`hong-kong`）。

## 部署與驗證

- 部署順序：migrate（0076、0077）→ API → web；之後 `python -m app.cli guides-import --actor-email … --dry-run` 應列出 430 筆 `taxonomy: update`，再正式匯入。
- Phase 4 部署後：`curl https://mokaair.com/robots.txt` 應只擋訓練用爬蟲（`AI_CRAWLER_POLICY` 未設即 allow-search）；
  文章頁看麵包屑；含 summary／faq 的文章把 JSON-LD 貼到 validator.schema.org（Article.abstract／speakable、FAQPage、DefinedTerm）。
- Phase 3 部署後：migrate 0078 → `python -m app.cli guides-links-rebuild`（連結表只在發布時寫，不跑則「引用本文的文章」全空）→
  `guides-aliases-seed --dry-run`（現在含 keyword 來源）→ 正式跑 → `guides-import --slug …`（第一批 89 篇，`--publish`）→
  `guides-links-check --locale zh-TW`（列出指向未發布目標的連結；已知 25 條在暫緩發布的批次上）。
  驗證：`GET /guides/life/ai-term-machine-learning?locale=zh-TW` 看 `related`／`backlinks`／`aliases`；
  文章頁 hover 名詞看定義卡、Tab 到連結按 Esc；手機首次點開卡；文末「同主題延伸閱讀」。
- Phase 2 部署後**必須**跑一次 `python -m app.cli guides-search-reindex`（索引只在發布時建，不跑則搜尋是空的），
  再 `guides-aliases-seed --dry-run` → 正式跑；`SHOW lc_ctype;` 需為 UTF-8，`\di ix_guide_search_entries_search_text_trgm` 應存在。
  驗證：`curl '/api/v1/guides/search?locale=zh-TW&q=機器學習'`（`best_match` 為名詞解釋篇）、`q=ＡＩ`、`q=%25%25`（0 筆不 500）、`q=a`（422）；
  開 `/zh-TW/search/articles?q=Ollama`；桌機 header 輸入 `Codex`、⌘K；手機 icon；無 JS 時表單仍送出。
- 驗證：`GET /api/v1/guides/topics?locale=zh-TW&section=life`（父 `parent:null`、子帶 `parent`、`count/counts`）、
  `GET /api/v1/guides?locale=zh-TW&kind=howto&country=japan`、`GET /api/v1/guides/destinations?locale=zh-TW`、`GET /api/v1/guides/series?locale=zh-TW`；
  開 `/zh-TW/life/topics/ai-terms`、`/zh-TW/guides/topics/transport`、`/en/life/topics/ai-terms`（應 noindex），看 canonical、robots、JSON-LD；`/sitemap.xml` 含主題 hub 列。
- 風險：sitemap 已拆成 index（每專區×語系一個子檔，超過 5,000 列自動編號成 `-2`、`-3`… 子檔，沒有上限；lint 不再預警）；
  CJK 搜尋用 pg_trgm 需 UTF-8 `lc_ctype`；新 block 的 web 渲染器先於內容；
  別名以（文章、語系、別名）唯一，同語系多篇共用的別名只加權、不置頂（系列 lesson 的 `aliases` 有 346 個重複，如 `cli`、`手機`）。
