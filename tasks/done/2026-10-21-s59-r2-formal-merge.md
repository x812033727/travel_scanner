---
id: 2026-10-21-s59-r2-formal-merge
title: S59 R2 formal blind merge and HOLD archive
status: done
priority: P2
area: docs
owner: codex-s59-author
claimed_at: 2026-10-21T00:10:46Z
created_at: 2026-10-21T00:10:43Z
completed_at: 2026-10-21T00:12:29Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s59/review/r2-merge
---

# S59 R2 formal blind merge and HOLD archive

## Why

S59 R2 已有兩位新讀者原票和獨立來源／畫面回條。必須在原創作五檔 SHA 不變時，按官方 13 題固定 OR 規則正式合併雙票，用 `narrative --answers` 留下可重查的 HOLD，才可開始 R3 修稿。

## Definition of done

- [x] 原票、逐項答案、OR 合併答案、官方輸出與紀錄完整封存，創作五檔前後 SHA 相同。
- [x] 正式判定記錄必過 `no_recap` 為 NO 及整體 HOLD，兩位讀者各自的重複證據清楚留存。

## Steps

- [x] 抽取 A/B 兩張 13 題原票與場景證據，核原票 SHA。
- [x] 用官方固定 OR 生成答案、執行隔離 CLI、存退出碼和 SHA。
- [x] 寫入 `docs/videos/curio-s59/review/r2-merge/summary.md`。

## How to verify

`node docs/videos/curio-s59/review/r2-merge/build-merge.mjs`；`node docs/videos/curio-s59/review/r2-merge/run-cli.mjs`。wrapper 退出 0，封存官方 CLI 退出 1（敘事 HOLD）。`node tools/tasks.mjs check`。

## Notes

A/B 各 12/13 YES；固定 OR 仍 12/13，唯一必過 NO 是 `no_recap`。A 指 s59077 後失敗事實重述，B 指 s59013→s59014 紙盤點劃重述。另有獨立書面畫面 HOLD，故 R3 必須重新凍結並重新雙盲／來源覆核。R2 五檔未修改。
