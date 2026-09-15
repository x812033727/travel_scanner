---
id: 2026-09-15-content-retopic-finance
title: 財經系列依批次掛上 finance 子主題（finance-basics／banking／credit／tax-insurance／investing）
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-15T13:57:26Z
completed_at:
branch:
depends_on:
  - 2026-09-15-guide-retopic-cli
scope:
  - apps/api/app/guides/content
---

# 財經系列依批次掛上 finance 子主題（finance-basics／banking／credit／tax-insurance／investing）

## Why

財經系列 120 篇的批次（`docs/life-finance-series.md` 批次 01–06）就是子主題的分界，但 slug 沒有統一前綴，retopic 只能靠關鍵字猜。由編輯依總表逐批指派最準。

## Definition of done

- [ ] 已落地的財經 pack 每篇掛一個 finance 子主題；`docs/life-finance-series.md` 各批次段落註明對應子主題。

## Steps

- [ ] 對照總表批次 → 子主題：01→finance-basics、02→banking/credit、03–04→tax-insurance、05–06→investing。
- [ ] 改 `topics`，跑 lint 與測試，部署後匯入。

## How to verify

```bash
cd apps/api && uv run python -m app.guides.pack_cli lint --kind life --catalogue docs/life-finance-series.md
```

## Notes

尚未落地的批次（03–06）在各自的批次任務裡直接帶子主題，不必回頭補。
