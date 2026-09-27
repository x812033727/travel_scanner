---
id: 2026-09-26-video-series-review-card-file
title: Video series W0: move the review card and the gate bodies into their own file
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T17:38:50Z
created_at: 2026-09-26T17:36:18Z
completed_at: 2026-09-26T17:39:12Z
branch: claude/video-series-w0
depends_on: []
scope:
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.tsx
---

# Video series W0: move the review card and the gate bodies into their own file

## Why

漫劇要有自己的分頁與作品頁（`2026-09-26-video-series-admin-tab`），也要顯示每一集的審核卡片；HANDS-OFF 的「可以上架」清單（`2026-09-26-video-hands-off-web`）同樣要改 `admin-video-reviews.tsx`。先把審核卡片、六個關卡的 body、共用型別與小工具抽成 `admin-video-review-card.tsx`，兩邊都在它之上做，衝突面就只剩接點。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [x] `admin-video-review-card.tsx` 匯出 `ReviewCard`、`JudgeLine`、型別（`Gate`、`Review`、`ProjectSummary`、`Project`…）、`REFRESH_MS`、`SLUG`、`control`、payload 讀取小工具、`fileUrl`、`useWhen`、`useRefresh`；`admin-video-reviews.tsx` 只剩列表、單集頁、單集表單與佇列、分頁，並 re-export `REFRESH_MS`、`fileUrl`。
- [x] 純搬移：既有測試不改就綠；lint、typecheck、check:i18n（新檔沒有中文）綠。

## Steps

- [x] 搬移與 re-export。
- [x] vitest、lint、tsc、check:i18n。

## How to verify

```bash
cd apps/web && npx vitest run components/admin-video-reviews && npm run lint && npm run typecheck && cd ../.. && git add -A && CI=1 npm run check:i18n
```

## Notes

2026-09-27（claude-fable-5-1-video-drama）：同一支 PR 帶進 `docs/videos/SERIES.md` 與這八張票。
