---
id: 2026-09-11-planner-overlay-close-guard-race
title: 規劃彈層的關閉鈕在重開後會靜默失效
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T10:24:18Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/planner-overlay.tsx
  - apps/web/lib/modal-sheet.ts
  - apps/web/components/planner-overlay.test.tsx
---
# 規劃彈層的關閉鈕在重開後會靜默失效

## Why

`PlannerOverlay` 的關閉鈕只有在自己是最上層彈層時才會真的關閉：

```ts
// apps/web/components/planner-overlay.tsx
const closeOverlay = useCallback(() => {
  if (panelRef.current && isTopModalLayer(panelRef.current)) onCloseRef.current();
}, []);
```

`isTopModalLayer` 讀的是 `apps/web/lib/modal-sheet.ts` 裡 module-level 的 `layers` 陣列，登記與登出都發生在 React 的 effect／cleanup。當前一個彈層的 unregister 還沒收乾淨就重新開啟，新面板不是 `layers.at(-1)`，於是**按下關閉鈕什麼都不會發生**——沒有錯誤、沒有回饋，彈層就停在畫面上。使用者只剩 Escape 或點背景可以脫身。

這不是理論問題，它已經讓 CI 紅過兩次：`apps/web/components/trip-editor.test.tsx` 連續「開啟安排編輯器 → 關閉 → 再開 → 關閉」，第二次關閉會逾時。`999dbc5`（2026-09-11）試過在點擊後補 `waitFor`，沒有修好——失效的是那個**點擊本身**，不是等待的時間不夠。之後在 PR #393 又重現一次。

證據與分析：https://github.com/x812033727/travel_scanner/pull/393#issuecomment-5632942149

## Definition of done

- [ ] 重開後的彈層，關閉鈕一定能關（或在無法關閉時有明確行為，而不是靜默無效）。
- [ ] 有一支測試涵蓋「關閉 → 重開 → 關閉」的登記／登出交錯，會在修好前失敗。
- [ ] `trip-editor.test.tsx` 不需要靠 `waitFor` 掩蓋這個競態。

## Steps

- [ ] 釐清 `layers` 的登記與登出順序，確認新面板何時不是 `at(-1)`。
- [ ] 修正守衛（例如改以「面板仍掛載且沒有更上層的彈層包住它」判定，而非嚴格相等），不要放寬成任何彈層都能關掉別人。
- [ ] 檢查同樣讀 `isTopModalLayer` 的其他呼叫點（`components/community/ui.tsx`、`components/discovery/detail-drawer.tsx`）是否有相同暴露。

## How to verify

```sh
cd apps/web && npx vitest run components/planner-overlay.test.tsx components/trip-editor.test.tsx
npm run lint:web && npm run typecheck:web && npm run test:web
```

手動：在行程規劃器連續開關同一個安排編輯器數次，關閉鈕每次都要有效。

## Notes

- scope 先只列 `planner-overlay.tsx`、`modal-sheet.ts` 與 `planner-overlay.test.tsx`。`trip-editor.test.tsx` 目前被
  `2026-09-11-pr388-seo-review` 與 `2026-09-10-seoul-day2-transport-ux` 押著，要動得先協調。
- 由 #393 的 CI 調查順帶發現，非該 PR 造成；#393 未修此問題，只留下分析。
