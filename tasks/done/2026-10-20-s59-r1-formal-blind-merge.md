---
id: 2026-10-20-s59-r1-formal-blind-merge
title: S59 R1 formal blind narrative merge
status: done
priority: P2
area: docs
owner: codex-s59-author
claimed_at: 2026-10-20T23:42:58Z
created_at: 2026-10-20T23:42:56Z
completed_at: 2026-10-20T23:44:44Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s59/review/r1-merge
---

# S59 R1 formal blind narrative merge

## Why

S59 R1 已有兩位獨立盲讀者的 13 題原票。必須把原票對準同一組五檔 SHA，依工具的固定 OR 規則合併，執行官方 `narrative --answers`，留下可重查的 HOLD 紀錄，才開始 R2 修稿。

## Definition of done

- [x] 原票、結構化答案、OR 合併答案、官方輸出與官方紀錄完整封存，五檔前後 SHA 相同。
- [x] 正式判定標示 `payoffs`、`no_recap` 兩項必過 NO 與 HOLD。

## Steps

- [x] 從兩張原票抽取每題票和場景證據，保留原票 SHA。
- [x] 以固定 OR 生成答案，執行官方 CLI，記下退出碼、結果和 SHA。
- [x] 寫入 `docs/videos/curio-s59/review/r1-merge/summary.md`。

## How to verify

`node docs/videos/curio-s59/review/r1-merge/build-merge.mjs`；`node docs/videos/curio-s59/review/r1-merge/run-cli.mjs`。第二個 wrapper 自身退出 0，所封存的官方 CLI 預期退出 1（敘事 HOLD），詳見 `cli-status.json`。`node tools/tasks.mjs check`。

## Notes

原票 A/B 各 10/13 YES；固定 OR 後 11/13，必過 `payoffs` 與 `no_recap` 為 NO。個別讀者另指出 `no_toc`、`no_detour`，R2 一併修。未修改 R1 創作檔。
