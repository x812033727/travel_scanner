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
（之後要讓 `TopicCreate/Update` 帶 `parent_slug` 與 `descriptions_json`）。

### Phase 1 — 分類架構（本 PR 落地）
| 任務 | 內容 |
| --- | --- |
| `guide-topic-hierarchy-api` | 0076：`parent_id`、`descriptions_json`、兩個新父主題與 23 個子主題種子；`?topic=` 含子主題；`?country=`；`GET /guides/destinations`；保留 slug |
| `guide-retopic-cli` | `pack_cli retopic`：依前綴與系列成員提案，`--apply` 只改 `topics`。已對 `ai-term-`、`claude-code-`、`codex-`、`gemini-`、`ai-news-`、`ai-search-`、`wordpress-`、`woocommerce-`、`chatgpt-` 共 430 篇套用 |
| `content-retopic-life-remaining-a-m` / `-n-z` / `content-retopic-finance` | 其餘無前綴文章由編輯審 dry-run 表後套用 |
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

### Phase 3 — 互連
`guide-aliases-seed-and-pack-field` → `pack-autolink-and-relink-cli` → `content-relink-autolink-life` / `-travel`；
`article-links-table-and-related-api`（0078 連結表、related、backlinks、`guides-links-check`）→ `term-link-popover-related-grid-web`。

### Phase 4 — SEO / AEO / GEO
`summary-and-faq-blocks-api` → `summary-faq-definedterm-jsonld-web`（**web 渲染器先部署，再發布含新區塊的內容**）；
`article-breadcrumb-visible-web`；`robots-ai-crawler-switch`；`content-summary-howto-and-life`（人工撰寫，不自動生成）。
既有 `2026-09-14-answer-first-howto-descriptions`（應改為明列 68 檔）與 `2026-09-14-heading-anchors-for-h3` 屬同一階段。

### Phase 5 — UI/UX
`guides-hub-redesign-web` → `life-hub-redesign-web`；`listing-toolbar-web`；`article-reading-polish-web`。

檔案先後序（避免 scope 衝突）：`service.py/router.py/schemas.py`：1.1 → registry → search → links → blocks；
`admin_service.py`：1.1 → crud → search → aliases → links；`content-blocks.tsx`：heading-anchors → term-link → jsonld；
`structured-data.ts/article-page.tsx`：aio(review) → term-link → jsonld → breadcrumb；`pack_ingest.py`：urlopen(review) → autolink → blocks。

## 分類詞彙（0076 種子；標籤在 `app/guides/taxonomy.py`，改種子即可）

**生活分享**：`software`、`gadgets`、`productivity`、`daily`、`misc` 維持單層；`tutorial` 保留於資料但不作導覽。

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
| `finance` 理財與金錢 | `finance-basics` / `banking` / `credit` / `tax-insurance` / `investing` | 財經批次 01／02／02／03–04／05–06 |

**旅遊**：主題不加子層；第二軸為國家 → 目的地（`DestinationProfile.country` → `japan`、`south-korea`、`taiwan`、`thailand`、`vietnam`、`singapore`、`hong-kong`）。

## 部署與驗證

- 部署順序：migrate（0076、0077）→ API → web；之後 `python -m app.cli guides-import --actor-email … --dry-run` 應列出 430 筆 `taxonomy: update`，再正式匯入。
- Phase 2 部署後**必須**跑一次 `python -m app.cli guides-search-reindex`（索引只在發布時建，不跑則搜尋是空的），
  再 `guides-aliases-seed --dry-run` → 正式跑；`SHOW lc_ctype;` 需為 UTF-8，`\di ix_guide_search_entries_search_text_trgm` 應存在。
  驗證：`curl '/api/v1/guides/search?locale=zh-TW&q=機器學習'`（`best_match` 為名詞解釋篇）、`q=ＡＩ`、`q=%25%25`（0 筆不 500）、`q=a`（422）；
  開 `/zh-TW/search/articles?q=Ollama`；桌機 header 輸入 `Codex`、⌘K；手機 icon；無 JS 時表單仍送出。
- 驗證：`GET /api/v1/guides/topics?locale=zh-TW&section=life`（父 `parent:null`、子帶 `parent`、`count/counts`）、
  `GET /api/v1/guides?locale=zh-TW&kind=howto&country=japan`、`GET /api/v1/guides/destinations?locale=zh-TW`、`GET /api/v1/guides/series?locale=zh-TW`；
  開 `/zh-TW/life/topics/ai-terms`、`/zh-TW/guides/topics/transport`、`/en/life/topics/ai-terms`（應 noindex），看 canonical、robots、JSON-LD；`/sitemap.xml` 含主題 hub 列。
- 風險：sitemap 已拆成 index（每專區×語系一個子檔，`pack_cli lint` 4,000 列預警）；
  CJK 搜尋用 pg_trgm 需 UTF-8 `lc_ctype`；新 block 的 web 渲染器先於內容；
  別名以（文章、語系、別名）唯一，同語系多篇共用的別名只加權、不置頂（系列 lesson 的 `aliases` 有 346 個重複，如 `cli`、`手機`）。
