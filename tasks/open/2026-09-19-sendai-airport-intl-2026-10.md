---
id: 2026-09-19-sendai-airport-intl-2026-10
title: sendai-airport-access-loople-bus-guide 2026-10-31 前重查仙台機場國際線冬季班期（長榮、星宇、台灣虎航）
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-19T06:47:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/sendai-airport-access-loople-bus-guide.json
---

# sendai-airport-access-loople-bus-guide 2026-10-31 前重查仙台機場國際線冬季班期（長榮、星宇、台灣虎航）

## Why

`sendai-airport-access-loople-bus-guide` H2-5 的表格列了長榮、星宇、台灣虎航飛仙台的每週班期，冬季班表換季後會變。規格 `docs/travel-guides-batch-7/sendai-airport-access-loople-bus-guide.md`「上線後與交叉檢查」要求上線 PR 同時開票，2026-10-31 以前重讀。

## Definition of done

- [ ] 2026-10-31 以前重讀仙台機場官網國際線月間時刻，三家的每週班期核對完；班期變了就改 H2-5 表格與表後那兩句。
- [ ] 更新 `checked_on`，lint 通過。

## Steps

- [ ] **2026-10-31 以前**（冬季班表換季後）：重讀 https://www.sendai-airport.co.jp/flight/intl-monthly.html 與其 API，核對長榮、星宇、台灣虎航的每週班期。
- [ ] 有變就改 H2-5 表格與表後那兩句；跑 lint 與內容包測試，部署後 `guides-import --dry-run` 再 `--publish`。

## How to verify

```bash
cd apps/api
uv run python -m app.guides.pack_cli lint --slug sendai-airport-access-loople-bus-guide
uv run pytest tests/test_guides_content_pack.py -q
```

部署後 `guides-import --dry-run` 列出 `sendai-airport-access-loople-bus-guide` 為 `update`，再 `--publish`；打開 `/zh-TW/guides/howto/sendai-airport-access-loople-bus-guide` 看 H2-5。

## Notes

- 來源：`docs/travel-guides-batch-7/sendai-airport-access-loople-bus-guide.md`「上線後與交叉檢查」，由 `2026-09-16-launch-articles-batch-7` 開出。
- 空港線票價與首末班（2027-03-20 後）、るーぷる與地鐵票券（2027-04-01 前）在 `2026-09-19-sendai-four-spring-2027`，因為那些數字與其他三篇仙台文共用。
- 反向連結（`japan-ic-card-suica-icoca-guide`、`japan-shinkansen-ticket-guide` blocks[6] 之後新增區塊，第 9、10 篇擇一）在票 `2026-09-19-batch-7-backlinks-existing-guides`（既有文章補連第七批）。
- `tasks/BOARD.md` 不要提交。
