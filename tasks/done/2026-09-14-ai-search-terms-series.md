---
id: 2026-09-14-ai-search-terms-series
title: GEO、AEO、AIO 搜尋最佳化名詞系列（10 篇＋總索引）
status: done
priority: P2
area: docs
owner: claude-opus-5
claimed_at: 2026-09-14T13:23:19Z
created_at: 2026-09-14T13:23:14Z
completed_at: 2026-09-16T06:12:05Z
branch: claude/relaxed-hawking-2y2r3f
depends_on: []
scope:
  - docs/ai-search-series
  - apps/api/app/guides/content/ai-search-seo.json
  - apps/web/public/guides/ai-search-seo
  - apps/api/app/guides/content/ai-search-geo.json
  - apps/web/public/guides/ai-search-geo
  - apps/api/app/guides/content/ai-search-aeo.json
  - apps/web/public/guides/ai-search-aeo
  - apps/api/app/guides/content/ai-search-aio.json
  - apps/web/public/guides/ai-search-aio
  - apps/api/app/guides/content/ai-search-llmo.json
  - apps/web/public/guides/ai-search-llmo
  - apps/api/app/guides/content/ai-search-eeat.json
  - apps/web/public/guides/ai-search-eeat
  - apps/api/app/guides/content/ai-search-structured-data.json
  - apps/web/public/guides/ai-search-structured-data
  - apps/api/app/guides/content/ai-search-llms-txt.json
  - apps/web/public/guides/ai-search-llms-txt
  - apps/api/app/guides/content/ai-search-generated-answers.json
  - apps/web/public/guides/ai-search-generated-answers
  - apps/api/app/guides/content/ai-search-measuring-citations.json
  - apps/web/public/guides/ai-search-measuring-citations
  - apps/api/app/guides/content/ai-search-terms-index.json
  - apps/web/public/guides/ai-search-terms-index
---

# GEO、AEO、AIO 搜尋最佳化名詞系列（10 篇＋總索引）

## Why

站上完全沒有解釋 GEO、AEO、AIO 這組名詞的文章。搜遍 `docs/`、`tasks/`、程式碼與 398 個內容包，
`AEO`、`AIO`、「answer engine」、「generative engine」零命中，`GEO` 全是座標的誤命中。

這組詞的中文搜尋結果幾乎全是行銷公司的內容農場，彼此定義互相矛盾：GEO 是 SEO 的上位還是改名、
GEO 與 AEO 是不是同一件事、AIO 到底指 Google 的 AI Overviews 功能還是一門服務、
LLMO 能不能影響訓練資料、llms.txt 有沒有引擎真的在讀——每一題都有兩種以上的現行說法。

所以這系列的價值不是「再給一個定義」，而是把**各家定義的分歧點**講清楚，並且分清楚
哪些是官方文件說明的機制、哪些是業界慣例、哪些只是廠商的行銷主張。

站上已有三篇相鄰文章，角度都是「讀者怎麼用」或「站長照著做」，不是名詞解釋：
`google-ai-overviews-for-site-owners`、`google-ai-mode-search`、`chatgpt-search-vs-google`。
本系列與它們互連，不重寫它們的操作步驟。

規格與撰稿指令在 [`docs/ai-search-series/`](../../docs/ai-search-series/brief.md)。

## Definition of done

- [x] `docs/ai-search-series/` 的 `brief.md`、`ARTICLES.md`、`catalogue.json` 寫定，11 個 slug 與標題不再變動。
- [x] 11 個內容包落在 `apps/api/app/guides/content/ai-search-*.json`，各自的
      `apps/web/public/guides/<slug>/` 有 `hero.svg`、`hero.jpg`、`diagram-1.svg`。
- [x] `pack_cli lint --warnings` 對這 11 個 slug 零 error 零 warning。
- [x] 每篇正文 1,800–3,000 中文字（按 `_body_length` 的算法），≥5 個 level-2 heading。
- [x] 每篇 ≥2 個獨立一手來源，`sources[]` 每筆帶**實際查證日**的 `checked_on`。
- [x] 22 張 SVG（11 hero ＋ 11 圖解）逐張目視過，全尺寸與縮到約 400 px 各看一次。
- [x] 所有站內連結的目標 slug 都真的存在。
- [x] `cd apps/api && uv run pytest tests/test_guides_content_pack.py` 通過。
- [x] `npm run check:tasks` 通過，`tasks/BOARD.md` 沒有被 commit。
- [ ] 總索引 `ai-search-terms-index` **最後**發布。（部署時才發生，見 ARTICLES.md「發布」）

## Steps

- [x] 寫 `docs/ai-search-series/brief.md`（撰稿指令，沿用 `docs/life-ai-series-brief.md` 再加本題守則）。
- [x] 寫 `docs/ai-search-series/ARTICLES.md` 與 `catalogue.json`，把 11 篇的 slug、標題、主軸、
      必涵蓋點與**確切的連結目標**定死，再開始撰稿。
- [x] 一篇一個撰稿代理，每波 ≤7 個，只寫自己的 `docs/ai-search-series/staging/<slug>/`。
- [x] 每篇交件就 `pack_cli ingest --from docs/ai-search-series/staging --slug <slug>`。
- [x] 10 篇正文齊了才寫總索引。
- [x] `pack_cli lint --render-dir` 產出 PNG，逐張目視。
- [x] 跑完驗證指令，commit、push。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life \
  --slug ai-search-seo --slug ai-search-geo --slug ai-search-aeo --slug ai-search-aio \
  --slug ai-search-llmo --slug ai-search-eeat --slug ai-search-structured-data \
  --slug ai-search-llms-txt --slug ai-search-generated-answers \
  --slug ai-search-measuring-citations --slug ai-search-terms-index \
  --render-dir ../../docs/ai-search-series/renders --warnings

cd apps/api && uv run python -m app.guides.pack_cli lint --kind life   # 回歸：其他 life 文章沒被影響
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guides_pack_ingest.py -q
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
npm run check:tasks
```

部署後在主機發布，先 dry-run，10 篇正文先上、確認後總索引最後上：

```bash
python -m app.cli guides-import --actor-email <admin> --dry-run --slug ai-search-seo ...
python -m app.cli guides-import --actor-email <admin> --publish --slug ai-search-seo ...
python -m app.cli guides-import --actor-email <admin> --publish --slug ai-search-terms-index
```

## Notes

- **slug 前綴用 `ai-search-`**，不用 `geo-` 或 `seo-term-`。這系列存在的目的就是拆解
  「哪個縮寫才是上位概念」這個爭議；用其中一個縮寫當前綴等於在 11 個永久網址裡先替一方站隊。
- **`lint --catalogue` 這個旗標現在不能用。** 它會把不在指定總表裡的 life 文章全報成缺漏，
  既有 82 篇 `ai-term-*` 就已經在噴了（票：`2026-09-14-guides-pack-lint-catalogue-life`）。
  改用 `--slug` 逐篇指定。**不要**為了消音把這 11 篇加進 `docs/life-ai-series.md`——那是
  另一個系列的總表；本系列的紀錄是 `docs/ai-search-series/ARTICLES.md`。
- **`display_order` 用 100**（不是撰稿指令寫的 10）。既有的 `ai-terms-index.json` 就是 100，
  而且 `/life` 公開列表是 `published_at` 由新到舊排（`apps/api/app/guides/service.py:216`），
  所以總索引靠**最後發布**落到列表最上方。
- **本票不動任何工程檔。** `apps/web/app/robots.ts`、`apps/web/lib/structured-data.ts`、
  `apps/web/app/sitemap.ts`、`docs/seo.md` 刻意不在 scope 裡：文章**描述**它們的既有做法，
  不修改它們。
- **日後改 `apps/web/app/robots.ts` 或 `apps/web/lib/structured-data.ts`，要回頭複查
  `ai-search-llms-txt` 與 `ai-search-structured-data` 兩篇**——它們引述站方目前的做法並標了查證日。
- `ARTICLES.md` 把 `ai-search-llms-txt`、`ai-search-generated-answers`、
  `ai-search-measuring-citations` 標為「易變」：llms.txt 的採用狀況、AI 模式的開放地區、
  Search Console 生成式 AI 報表都還在變。life 內容包不走到期邏輯，`valid_until` 維持 null。
- **未量測搜尋引擎實際收錄或引用結果。** 本系列不宣稱任何成效。
- sitemap 額度：目前 498 個（文章, 語系）列，警告門檻 800，加 11 篇到 509。
