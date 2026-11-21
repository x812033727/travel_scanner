---
id: 2026-10-20-s57-r6-fixed-or-narrative-merge
title: S57 R6 fixed OR narrative merge archive
status: done
priority: P2
area: docs
owner: codex-s57-author
claimed_at: 2026-10-20T23:43:56Z
created_at: 2026-10-20T23:43:53Z
completed_at: 2026-10-21T00:02:44Z
branch:
depends_on:
  - 2026-10-20-curio-s57-r6-author
scope:
  - docs/videos/curio-s57/review/r6-merge
---

# S57 R6 fixed OR narrative merge archive

## Why

R6 兩名隔離讀者已各交原票，須在作者改稿前把同一凍結稿的正式固定 OR 敘事結果封存。

## Definition of done

- [x] 原票、逐題轉錄與官方 CLI 的同版 HOLD 判定可由雜湊追溯。

## Steps

- [x] 確認 R6 來源報告已凍結，五份創作檔符合作者 SHA。
- [x] 複製兩份原票，逐題轉成有場景 ID 的答案並保留原理由／行號稽核。
- [x] 以官方固定 OR 合併、執行 narrative CLI，保存前後 SHA、stdout、狀態與正式紀錄。
- [x] 寫明正式 HOLD 與 R7 作者修法界線。

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`；`node tools/video/cli.mjs narrative --slug curio-s57 --answers docs/videos/curio-s57/review/r6-merge/merged-answers.json --workdir /tmp/curio-s57-r6-merge-formal-20261020 --json`；`npm run check:tasks`。

## Notes

[正式摘要](../../docs/videos/curio-s57/review/r6-merge/summary.md)：12／13 HOLD 只因兩票共同 `no_recap`；A `no_detour` 單票異議按固定 OR 過，仍保留。R6 獨立來源／claims PASS、書面畫面 `s57150` HOLD。五份創作檔 CLI 前後 SHA 完全相同。下一步由作者 R7 窄修、重新凍結與重審；本票沒有媒體操作。
