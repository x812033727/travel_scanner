---
id: 2026-09-11-admin-shell-modal-layer
title: admin-shell 命令面板改用 modal-sheet 的分層堆疊
status: done
priority: P3
area: web
owner: codex-b10e-modal
claimed_at: 2026-09-30T10:54:00Z
created_at: 2026-09-11T20:07:47Z
completed_at: 2026-09-30T11:16:14Z
branch: codex/remaining-tickets-20260930
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

- [x] `admin-shell.tsx` 的命令面板改用 `useModalSheet`，手刻的 effect 移除。
- [x] 既有測試（若有）仍綠；Escape 從 `document` 發也要能關。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web -- admin-shell
```

## Notes

- 開始之前先確認 `2026-09-09-site-experience-settings` 是否仍持有 `admin-shell.tsx`；
  若已合併或釋出，正常 claim 即可。

### 2026-09-30 local implementation (codex-b10e-modal)

- Checked main `422b3f68`, open PR files, remote heads, local branches and worktree
  changes before claiming normally. The earlier site-experience claim now owns
  acceptance files only; historical admin shell changes are from merged #377/#380.
  No other active implementation touches these two files. Missing old worktrees and
  incomplete P: article-only checkouts were recorded rather than modified.
- Replaced the hand-written Escape/Tab/overflow effect with `useModalSheet`.
  A following layout effect focuses the command input only when opening, preserving
  immediate typing without interfering with the hook's opener capture. The account
  popover and Ctrl/Meta+K shortcut behavior are unchanged.
- Added five behavioral regressions: document Escape and two-way Tab wrapping,
  keyboard-opener focus return, handled/IME Escape, top-layer keyboard handling,
  and scroll locking when the lower shell unmounts before the upper sheet.
  Against the old component: 4 failed / 1 passed. With the fix: the command shell,
  admin navigation and modal hook suites passed 27 tests across 3 files.
- Independent diff review found no blocking issue. Full web checks and the final
  PR receipt are recorded at the final delivery; this is not production acceptance.
- Final local verification: TypeScript, scoped ESLint, five-locale i18n and task
  validation passed. Full local lint was interrupted under sustained memory
  pressure; the full web suite had not started and is delegated to PR CI.
  Rebased onto `d7787f51` (only upstream video operations changed), with identical
  web contents. A fresh 26-PR/worktree collision review found no active overlap.
- Draft PR #1044: all eight CI checks passed on `8b7f609b`, including the full
  web checks and required API/container/smoke jobs. After main advanced to
  `3b3c1eb3`, the four source/test files remained byte-identical; 45 focused
  tests passed again and the local task check passed. Preserved the concurrent
  GitHub main merge and PR promotion, then added this archive on top. Full CI
  must be assessed again on the new pushed head.
- The owner asked to continue clearing unfinished tickets after the concrete
  two-ticket archive request. Verified the completed record and matching body,
  removed only its leftover open copy, and retained this completion record.
  This closes the local implementation ticket; PR merge and deployment remain
  separate and have not been performed.
