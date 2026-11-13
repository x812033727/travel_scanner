---
id: 2026-11-11-curio-pool-remaining-dangling-ids-in
title: Curio pool: remaining dangling ids in notes (N194, N210, ...) and stale revision stamps in topics.json
status: done
priority: P3
area: docs
owner: claude-sonnet-3-8
claimed_at: 2026-11-13T01:41:08Z
created_at: 2026-11-11T02:33:06Z
completed_at: 2026-11-13T03:01:51Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/history-curiosity/topics.json
  - docs/videos/history-curiosity/topics-fg.json
---

# Curio pool: remaining dangling ids in notes (N194, N210, ...) and stale revision stamps in topics.json

## Why

奇聞檔案局素材池在部分批次的 `notes` 與 `not_added` 裡提到不在奇聞池中的題號（如跨系列的 `N194`、`N210`，或當批覆核退回／合併而未入池的 `N1105`、`N1224`、`N1463`、`N1705`、`N510`、`N2461`、`N2782`、`N5103`、`N5403`，以及已撤回的題案 `T30`），容易誤導後續查重；此外 `topics.json` 與 `topics-fg.json` 的 `pool.revision` 仍停在 `2026-11-02-curio-pool-761`。

## Definition of done

- [x] 各批次 `notes`／`not_added` 裡指到不在素材池的題號與撤回題案，皆明確標註去向或跨系列代號（如 `原來如此事務所 LEG-N194`、`題案已撤回`、`不在素材池`）。
- [x] `topics.json`（224 題）與 `topics-fg.json`（61 題）的 `pool` 欄位更新為目前版本 `2026-11-12-curio-pool-1412`，並重新建置與驗證素材池。

## Steps

- [x] 修正 `wave2-legacy`、`wave10`、`wave11`、`wave15`、`wave19`、`wave20`、`wave21`、`wave25`、`wave45`、`wave47` 中懸空題號與撤回題案 `T30` 的備註說明。
- [x] 依目前 `pool.json` 與 `themes.json` 重新計算並寫回 `topics.json` 及 `topics-fg.json` 的 `pool` 狀態與版本戳。
- [x] 執行 `cli.mjs build`、`cli.mjs check` 與單元測試確認無誤。

## How to verify

`node tools/video/curio/pool/cli.mjs build && node tools/video/curio/pool/cli.mjs check && node --test tools/video/curio/pool/pool.test.mjs`。

## Notes

- `wave2` 的 `M07`、`M23` 提及的 `N194`、`N210` 為原來如此事務所的 `LEG-N194`、`LEG-N210`；`L31`–`L34` 提及的 `T30` 為已撤回題案，皆已在備註加註。
- 其餘未入池的同批退回或合併題號皆已加註去向。
