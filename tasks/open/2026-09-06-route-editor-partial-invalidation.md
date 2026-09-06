---
id: 2026-09-06-route-editor-partial-invalidation
title: 行程編輯後不清整天路段、缺的段用距離估計、按鈕不再預設 refresh
status: review
priority: P1
area: web
owner: claude-fable-5.1
claimed_at: 2026-09-06T03:00:03Z
created_at: 2026-09-06T02:45:24Z
completed_at:
branch: claude/route-editor-partial-invalidation
depends_on: []
scope:
  - apps/web/lib/trip-types.ts
  - apps/web/lib/trip-types.test.ts
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/route-timeline-link.tsx
  - apps/web/components/route-timeline-link.test.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 行程編輯後不清整天路段、缺的段用距離估計、按鈕不再預設 refresh

## Why

`trip-editor.tsx` 目前：

- 每個會觸發 `compute-day` 的按鈕都送 `refresh=true`——查路（有路線時，:1521）、當日交通方式
  radio、緩衝 select（:1523）、stale 橫幅（:1525）——連 Redis 快取都跳過，改緩衝也整天重打。
- 改順序丟掉整天的路段（`move`，:709）、拖曳丟掉整趟（`drop`，:723）；但後端只作廢真的不再
  相鄰的段。
- 一天被標 stale 之後，`projectChainedStarts` 收到空陣列（:1452-1456），所有段退回
  「上一站結束 + 緩衝」的 0 分鐘估計，連沒被碰到的段也一起變「約」。
- 橫幅寫「行程內容已變更，舊路線不再使用」，實際上只有 2 段缺。

配合後端 `2026-09-06-route-recompute-reuses-saved-segments`（重算只補缺的段、編輯後不再自動查），
前端要做到：缺的段顯示距離估計、其餘段維持原路線、按查路只查缺的那幾段。

## Definition of done

- [x] 改一站地點後，只有碰到那一站的兩段變成「約 X 分」，其餘段仍顯示「預計」與原路線。
- [x] 「約 X 分」用兩站座標的距離估（步行 4.5 km/h；汽車 5 分 + 30 km/h；大眾運輸 10 分 +
      20 km/h；取 5 分整），缺座標才退回只加緩衝。
- [x] 改順序／拖曳只丟不再相鄰的段。
- [x] 查路、改當日交通方式、改緩衝、橫幅都送 `refresh:false`；只有「重新查詢可用路線」（:1556）
      與當天是今天時送 `refresh:true`。
- [x] 橫幅改為「有 N 段移動尚未查路」+ 查路；N = 0 不顯示。文案走 `messages/*/trips.json`
      五語系（`check:i18n` 會擋新的硬編碼中文）。
- [x] `npm run lint:web && CI=1 npm run check:i18n && npm run typecheck:web && npm run test:web` 通過。

## Steps

- [x] `lib/trip-types.ts`：`estimateLegMinutes(from, to, mode)`、`adjacentPairKeys(rows)`；
      `projectChainedStarts` 多收 `mode`，缺 segment 時用估計值。
- [x] `components/trip-editor.tsx`：`computeRoutes` 的 refresh 預設 false 並逐一改呼叫點；
      `projectChainedStarts` 改傳完整 `routes`；`move`/`drop` 只丟不再相鄰的段；橫幅計數與文案。
- [x] `components/route-timeline-link.tsx`：`stale` 語意改為「沒有 segment 或
      segment.status === "stale"」，確認缺段時的樣式。
- [x] 測試：`lib/trip-types.test.ts`、`components/trip-editor.test.tsx`、
      `components/route-timeline-link.test.tsx`。

## How to verify

```bash
npm run lint:web && CI=1 npm run check:i18n && npm run typecheck:web && cd apps/web && npx vitest run lib/trip-types.test.ts components/trip-editor.test.tsx components/route-timeline-link.test.tsx
```

手動：開一趟有 3 站以上的行程 → 改第 2 站地點 → 只有 1→2、2→3 變「約」；按查路 →
Network 裡 `compute-day` 的 body 是 `refresh:false`；改緩衝 → 同樣 `refresh:false`。

## Notes

- `RouteModePanel` 不動：它已經是點哪種交通方式才查哪種。
- `staleDays` 仍可保留當「有東西改過」的旗標，但不要再拿它把整天路段清掉。
- `route-timeline-link.tsx` 本身不用改：缺 segment 時本來就顯示「選擇這段交通方式」，
  只是 editor 不再把整天的 `stale` 旗標傳進去（改成 `segment?.status === "stale"`）。
- `staleDays` 保留為「這一天改過東西」的旗標，只拿來決定橫幅要不要出現（且缺段 > 0）；
  它有 14 個寫入點，這次不拆。
- 測試裡路段分鐘數避開 0/5/10/15/30：緩衝下拉的選項文字也是「30 分」，`getByText` 會撞到。
- 再確認時發現：留下來的路段若直接拿存在上面的 `ready_time` 定錨，上游一段改成估計值後
  下游會顯示舊的絕對時間。`projectChainedStarts` 改成跟後端一樣用 duration + buffer 接著算，
  `ready_time` 只在沒有上一站可接時才用。路段卡片上的「09:00 → 09:20」仍是存的時間，按查路後才更新。
