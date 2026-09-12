---
id: 2026-09-11-admin-shell-modal-layer
title: admin-shell 命令面板改用 modal-sheet 的分層堆疊
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-11T20:07:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-shell.tsx
  - apps/web/components/admin-shell.test.tsx
---

# admin-shell 命令面板改用 modal-sheet 的分層堆疊

## Why

`2026-09-11-dialog-primitives-and-a11y-cleanup` 把十二個 dialog 裡的十一個改成用
`lib/modal-sheet.ts` 的 `useModalSheet`，只剩 `admin-shell.tsx` 沒動——它在
`2026-09-09-site-experience-settings`（`codex-site-experience`，`blocked`，claim 09-09 10:58
已過 24 小時）的 scope 裡，為了一個檔去接手整張別人的任務不划算，所以獨立成這張。

它不是壞的：`admin-shell.tsx:72-86` 的命令面板已經有 document 層級的 Escape、Tab 陷阱、
捲動鎖與焦點還原，只少了 `registerModalLayer` 的分層堆疊。今天沒有東西會疊在命令面板上，
所以這是一致性而不是缺陷——優先度 P3。

同檔 `:92` 的帳號選單另有一個 `Escape` handler，那是 popover 不是 dialog，不在範圍內。

## Definition of done

- [ ] `admin-shell.tsx` 的命令面板改用 `useModalSheet`，手刻的 effect 移除。
- [ ] 既有測試（若有）仍綠；Escape 從 `document` 發也要能關。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web -- admin-shell
```

## Notes

- 開始之前先確認 `2026-09-09-site-experience-settings` 是否仍持有 `admin-shell.tsx`；
  若已合併或釋出，正常 claim 即可。
