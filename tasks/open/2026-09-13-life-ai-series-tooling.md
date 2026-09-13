---
id: 2026-09-13-life-ai-series-tooling
title: 生活分享 AI 系列：內容包產製與檢查工具 guides-pack、撰稿 brief
status: in-progress
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-13T11:57:46Z
created_at: 2026-09-13T11:55:58Z
completed_at:
branch: claude/festive-brown-6nsxfm
depends_on: []
scope:
  - apps/api/app/guides/pack_ingest.py
  - apps/api/app/guides/pack_cli.py
  - apps/api/tests/test_guides_pack_ingest.py
  - apps/api/tests/test_guides_content_pack.py
  - docs/life-ai-series-brief.md
  - docs/travel-guides.md
---

# 生活分享 AI 系列：內容包產製與檢查工具 guides-pack、撰稿 brief

## Why

前三批旅遊文章（PR #443、#446、#454）都靠一支只活在 session scratchpad 的 `ingest_pack.py`：驗證內容包、
複製 SVG、從 Commons API 抓照片與授權、寫尺寸與 credit。它沒進 repo，每批都重寫一次，而且沒有測試。
生活分享的 AI 系列有 220 篇（`docs/life-ai-series.md`），要分十一批、由不同 session 產出，工具必須是
repo 裡可重複執行、有測試、進 CI 的東西。AI 文章多了一件旅遊文章沒有的事：軟體沒有照片可拍，hero 要
用自繪插圖，而 `HERO_SRC_PATTERN` 只收點陣圖，所以工具要把 `hero.svg` 渲染成 `hero.jpg`。

## Definition of done

- [ ] `cd apps/api && uv run python -m app.guides.pack_cli ingest --from <workdir> --slug <slug>` 把撰稿代理的工作區
      （`pack.json`、`diagram-N.svg`、`hero.svg` 或 `images.json`、`notes.md`）變成一個通過 `ArticlePack` 與
      `_validate_document` 的內容包加 `apps/web/public/guides/<slug>/` 的圖檔：hero ≤200 KB、photo ≤150 KB、
      credit 與尺寸由工具寫，Commons 授權白名單 CC0／PD／CC BY／CC BY-SA。
- [ ] `guides-pack lint [--kind life] [--render-dir …] [--catalogue …]` 對內容包跑系列規則（≥3 個 h2、一表一 callout、
      partner_link ≤3、每個 source 有 checked_on、SVG viewBox／title／desc／無外部參照／字級 ≥15、圖上數字都在正文），
      能把每張 SVG 渲染成 PNG 給人看，能比對總表與內容包的缺口。
- [ ] `tests/test_guides_content_pack.py` 多一個測試讓所有 life 內容包必須通過 lint（只算 error）。
- [ ] `docs/life-ai-series-brief.md` 是每批撰稿代理原文重用的指令；`docs/travel-guides.md` 補 hero 政策與工具指引。
- [ ] ruff、mypy、pytest 全綠。

## Steps

- [ ] `app/guides/pack_ingest.py`：`lint_document`、`check_svg`、`missing_diagram_numbers`、`commons_file_info`、
      `fit_bytes`、`render_svg`、`ingest`、`lint_all`；I/O 可注入，測試不打網路、不開瀏覽器。
- [ ] `app/guides/pack_cli.py`（`python -m app.guides.pack_cli ingest|lint`；`app/cli.py` 的 scope 被 2026-09-12-food-merchant-enrichment 持有，等它收掉再加一行別名）。
- [ ] `tests/test_guides_pack_ingest.py`；`tests/test_guides_content_pack.py` 加 life lint 測試。
- [ ] brief 與 travel-guides.md。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app
cd apps/api && uv run pytest tests/test_guides_pack_ingest.py tests/test_guides_content_pack.py -q
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue ../../docs/life-ai-series.md
```

## Notes

- 渲染用 `/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell`（`CHROMIUM_BIN` 可覆寫）；
  主機只有 WenQuanYi 字型，所以自繪 hero 少字或無字，標籤留在 SVG 圖解上由讀者端字型渲染。
