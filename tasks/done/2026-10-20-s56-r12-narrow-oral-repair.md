---
id: 2026-10-20-s56-r12-narrow-oral-repair
title: S56 R12 narrow oral repair
status: done
priority: P2
area: docs
owner: codex-s56-r12-author
claimed_at: 2026-10-20T23:09:05Z
created_at: 2026-10-20T23:09:02Z
completed_at: 2026-10-20T23:10:36Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s56/video.json
  - docs/videos/curio-s56/claims.md
  - docs/videos/curio-s56/script.md
  - docs/videos/curio-s56/review/r12-author-oral-repair.md
---

# S56 R12 narrow oral repair

## Why

S56 R11 音檢在完整 154 句與兩輪限定重錄後仍有 `s56096`、`s56174` 兩旗標。作者需修成較不易誤聽的說法，並重新凍結精確五檔，讓新稿回到獨立查源與盲評關卡。

## Definition of done

- [x] 只修改兩句口播、同步主張表與劇本，保存 R11／R12 五檔 SHA 及史料邊界。
- [x] 154 句、121 景、18 loops 不變；`lint` 為零錯誤／零警告，並交接新稿的獨立覆核與語音要求。

## Steps

- [x] 依 Foster 固定原文核對 `packing`、越河後兩處火勢合流；把 `他／收` 與 `新火` 改成較清楚的口語。
- [x] 由 `video.json` 重產 `script.md`，記錄新舊五檔 SHA；沒有使用付費 TTS、圖片或配樂。

## How to verify

`sha256sum docs/videos/curio-s56/{brief.md,research.md,claims.md,video.json,script.md}` 對照 [作者交接](../../docs/videos/curio-s56/review/r12-author-oral-repair.md)；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s56` 回 0／0；另跑 `npm run test:docs-videos`、`npm run check:tasks` 與 `git diff --check`。

## Notes

R11 最終 9 → 2 → 2，並非 R12 合格證據。R12 作者不能自行核准史料／書面畫面、雙盲敘事、政策或音檢；`STOP` 仍保留。逐項理由、精確 SHA 和後續次序在 [R12 交接](../../docs/videos/curio-s56/review/r12-author-oral-repair.md)。
