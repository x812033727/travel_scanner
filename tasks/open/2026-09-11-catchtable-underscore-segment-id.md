---
id: 2026-09-11-catchtable-underscore-segment-id
title: CatchTable 店家 id 有底線分段時存不了訂位連結
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-11T19:26:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/platform_links.py
  - apps/api/tests/test_food_platform_links.py
  - apps/web/lib/reservation-platforms.ts
  - apps/web/lib/reservation-platforms.test.ts
---

# CatchTable 店家 id 有底線分段時存不了訂位連結

## Why

PR #397 讓 CatchTable 的店家 id 可以含點號（例如 `yosukgung.kr`），規則是每個點分段都要以英數開頭（`_CATCHTABLE_SLUG`，`apps/api/app/foods/platform_links.py:65`）。

但實際資料裡有 id 是 `hani._.noodle`（首爾 하니칼국수），中間那段只有一個底線，所以
`https://www.catchtable.net/shop/hani._.noodle` 被判為不是精準店家頁，存不進訂位平台欄位。
這一頁在 2026-09-12 的查核中，由兩個獨立代理分別確認過就是該店（퇴계로 411-15、02-3298-6909）
且頁面可以訂位，純粹卡在網址規則。

## Definition of done

- [ ] `hani._.noodle` 這類 id 能通過前後端驗證，且沒有放寬到會接受搜尋頁、目錄頁或路徑穿越。
- [ ] Python 與 TypeScript 兩邊判斷一致，各自有測試。
- [ ] 首爾 하니칼국수 的訂位連結可以改回 verified 並公開。

## Steps

- [ ] 放寬 `_CATCHTABLE_SLUG`：分段可以用底線開頭，但仍禁止空分段，整體仍要以英數開頭。
- [ ] 同步改 `apps/web/lib/reservation-platforms.ts` 的對應規則。
- [ ] 補測試：`hani._.noodle` 會過；`a..b`、`.abc`、`abc.`、`shop/search` 仍被拒。

## How to verify

- `cd apps/api && pytest tests/test_food_platform_links.py`
- `cd apps/web && npx vitest run lib/reservation-platforms.test.ts`

## Notes

- 查核證據在 `apps/api/app/foods/data/platform_reviews/2026-09-11-public-merchants.json` 裡
  `seoul-hanikalgugsu` 那筆，狀態是 `ambiguous`，網址放在 `evidence` 的
  `unstorable_candidate` 角色下。改完規則後把它改成 `verified` 再跑一次匯入指令即可。
- 相關任務：`2026-09-11-food-reservation-link-backfill`。
