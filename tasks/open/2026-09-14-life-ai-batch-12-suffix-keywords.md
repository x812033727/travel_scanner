---
id: 2026-09-14-life-ai-batch-12-suffix-keywords
title: 生活分享 AI 系列批次 12：字尾關鍵字補位（11 篇）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-14T23:07:00Z
completed_at:
branch:
depends_on:
  - 2026-09-14-ai-suffix-keywords-catalogue
scope:
  - apps/api/app/guides/content/ai-tools-by-search-term.json
  - apps/web/public/guides/ai-tools-by-search-term
  - apps/api/app/guides/content/ai-image-to-text-ocr.json
  - apps/web/public/guides/ai-image-to-text-ocr
  - apps/api/app/guides/content/ai-taiwanese-hokkien-hakka-tools.json
  - apps/web/public/guides/ai-taiwanese-hokkien-hakka-tools
  - apps/api/app/guides/content/ai-line-sticker-creation.json
  - apps/web/public/guides/ai-line-sticker-creation
  - apps/api/app/guides/content/ai-interior-design-visualization.json
  - apps/web/public/guides/ai-interior-design-visualization
  - apps/api/app/guides/content/ai-id-photo-rules-taiwan.json
  - apps/web/public/guides/ai-id-photo-rules-taiwan
  - apps/api/app/guides/content/ai-naming-brainstorm-checks.json
  - apps/web/public/guides/ai-naming-brainstorm-checks
  - apps/api/app/guides/content/ai-fortune-telling-apps-caution.json
  - apps/web/public/guides/ai-fortune-telling-apps-caution
  - apps/api/app/guides/content/ai-stock-research-boundaries.json
  - apps/web/public/guides/ai-stock-research-boundaries
  - apps/api/app/guides/content/ai-legal-questions-boundaries.json
  - apps/web/public/guides/ai-legal-questions-boundaries
  - apps/api/app/guides/content/ai-health-questions-boundaries.json
  - apps/web/public/guides/ai-health-questions-boundaries
---

# 生活分享 AI 系列批次 12：字尾關鍵字補位（11 篇）

## Why

`docs/ai-suffix-keywords.md` 對照「〇〇 AI」字尾型搜尋詞之後，有一組詞在站上哪裡都對不到文章（圖片轉文字、台語、
LINE 貼圖、裝潢、證件照、取名），再加一篇把讀者會搜的字對到文章的索引 hub，排成 `docs/life-ai-series.md` 的批次 12。
四篇敏感／YMYL 題（算命、投資、法律、健康）先列著等站主拍板。這批只有 11 篇，不是 20。

開工前先讀 `docs/life-ai-series.md` 的「經驗記錄」、`docs/ai-suffix-keywords.md` 的「寫法規則」與批次 06 票的做法。

## Definition of done

- [ ] 十一個（或拍板後剩下的）`apps/api/app/guides/content/<slug>.json`（zh-TW），每篇：標題以字尾詞開頭、description 第一句與導言各含字尾詞一次、hero（自繪或 Commons）、至少一張自繪 `diagram-1.svg`、≥3 個 h2、一表、一 callout、sources 每筆有 `checked_on`、至少一個站內 `link`。
- [ ] hub `ai-tools-by-search-term`：`featured: false`、`display_order: 100`，每一組字尾詞一段加對應文章的 `link`，只連已經寫好的篇；批次 08／09／11 的落點等該批寫完再回頭補連結。
- [ ] 沒有 logo、字標、圖示、截圖；照片只來自 Commons 的 CC0／PD／CC BY／CC BY-SA。
- [ ] `guides-pack lint --kind life` 沒有 error；每張圖渲染成 PNG 後人工看過；`test_guides_content_pack.py` 全綠。
- [ ] 收尾：`ai-tools-choose-by-task` 導言後補一個連到 hub 的 `link`（那篇在補強票的 scope，補強票 done 後再改）。

## Steps

這十一篇（slug · 標題 · 關鍵字 · topics · 圖）：

1. `ai-tools-by-search-term` · 〇〇 AI 怎麼找：從你會搜的字找到對的工具與教學 · 翻譯 AI、簡報 AI… · ai, misc · 圖：插 · 易變
2. `ai-image-to-text-ocr` · 圖片轉文字 AI：截圖、掃描件與手寫筆記變成可編輯文字 · 圖片轉文字 AI · ai, tutorial · 圖：插 · 易變
3. `ai-taiwanese-hokkien-hakka-tools` · 台語 AI 與客語 AI：語音辨識、合成與翻譯工具有哪些、準不準 · 台語 AI · ai, daily · 圖：照 · 易變
4. `ai-line-sticker-creation` · 貼圖 AI：用 AI 做 LINE 貼圖的生成、去背、審核規則與版權 · 貼圖 AI · ai, daily · 圖：插 · 易變
5. `ai-interior-design-visualization` · 裝潢 AI：把房間照片變成設計提案，哪些不能靠 AI · 裝潢 AI · ai, daily · 圖：照 · 易變
6. `ai-id-photo-rules-taiwan` · 證件照 AI：AI 修圖或生成的證件照能不能用，護照與身分證規定 · 證件照 AI · ai, daily · 圖：插 · 易變
7. `ai-naming-brainstorm-checks` · 取名 AI：品牌、公司與商品名的提示詞，以及預查與商標檢索 · 取名 AI · ai, daily · 圖：插
8. `ai-fortune-telling-apps-caution` · 算命 AI 在做什麼：生成式回答的原理、個資流向與付費陷阱 · 算命 AI · ai, daily · 圖：插 · **待拍板**
9. `ai-stock-research-boundaries` · 投資 AI 能幫什麼：整理財報與新聞、不能預測漲跌、金管會怎麼管 · 投資 AI · ai, daily · 圖：插 · 易變 · **待拍板**
10. `ai-legal-questions-boundaries` · 法律 AI：法律問題問 AI 能整理什麼、什麼要找律師 · 法律 AI · ai, daily · 圖：插 · **待拍板**
11. `ai-health-questions-boundaries` · 健康 AI：症狀整理、看診前準備與它不能取代的事 · 健康 AI · ai, daily · 圖：插 · **待拍板**

- [ ] 先問站主 8–11 寫不寫；不寫的從 `docs/life-ai-series.md` 與 `docs/ai-suffix-keywords.md` 刪掉，並把 scope 裡對應的路徑拿掉。
- [ ] 一篇一個撰稿代理、每波最多七個，代理照 `docs/life-ai-series-brief.md`（含第 4 節的字尾詞規則）產出工作區；指派只准連已寫的 slug。
- [ ] 每篇落地就 `guides-pack ingest`；被拒的退回修。
- [ ] `guides-pack lint --render-dir` 逐張看圖；跑測試；更新這張票；commit。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --render-dir /tmp/renders --catalogue ../../docs/life-ai-series.md
cd apps/api && uv run pytest tests/test_guides_content_pack.py tests/test_guide_partner_links.py -q
npm run check:tasks
```

部署後在主機：`python -m app.cli guides-import --actor-email <admin> --slug … --dry-run`，再 `--publish`。

## Notes

- 8–11 四篇寫的時候依 `seo-trust-sensitive-topics` 的作者、來源與界線要求；金管會、衛福部、司法院等官方頁為主要來源。
- sitemap 現在 886 列，這批加 11 列；批次 10、11 落地時會超過 1,000，見 `2026-09-14-sitemap-split-before-1000-rows`。
