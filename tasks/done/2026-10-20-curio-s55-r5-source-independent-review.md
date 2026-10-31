---
id: 2026-10-20-curio-s55-r5-source-independent-review
title: Curio S55 R5 independent source review
status: done
priority: P2
area: docs
owner: codex-s55-r5-source-independent
claimed_at: 2026-10-20T20:43:02Z
created_at: 2026-10-20T20:42:59Z
completed_at: 2026-10-20T20:44:42Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s55/review/r5-source-independent.md
---

# Curio S55 R5 independent source review

## Why

R4 獨立來源覆核因 Gonesse 破裂原因錯指富蘭克林為推測者而 HOLD；R5 作者修正旁白與一景投料示意，須由非作者對精確版獨立重查。

## Definition of done

- [x] 對 R5 五檔精確 SHA、固定 F／M／E 全文、兩個 R4 阻點、所有逐句連結和分鏡界線留下可重查的 PASS／HOLD 收據。

## Steps

- [x] 從固定提交重新取回三份全文並核 SHA；把 R5 修正對照 F 被動推測與投料機制原句。
- [x] 核 145 列 claim、147 句 script、159 個來源連結、135 景、14 loops 與 lint；寫入獨立收據。

## How to verify

`sha256sum docs/videos/curio-s55/{research.md,brief.md,video.json,script.md,claims.md}`；`VIDEO_WORKDIR=/tmp/curio-s55-r5-source-independent node tools/video/cli.mjs lint --slug curio-s55 --json`；`git diff --check`；`npm run check:tasks`。人工逐句／書面畫面結果見 [R5 獨立收據](../../docs/videos/curio-s55/review/r5-source-independent.md)。

## Notes

2026-10-20：**PASS**，R4 的 Gonesse 匿名推測歸屬與投料機制畫面阻點已解除。這只通過 R5 的來源／書面畫面；兩位新讀者敘事盲評及實際媒體仍屬 S55 主任務。
