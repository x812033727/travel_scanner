---
id: 2026-10-20-s52-r19-independent-source-and-written
title: S52 R19 independent source and written visual audit
status: done
priority: P2
area: docs
owner: codex-s52-r19-source
claimed_at: 2026-10-20T21:39:20Z
created_at: 2026-10-20T21:39:17Z
completed_at: 2026-10-20T21:42:34Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s52/review/r19-source-independent.md
---

# S52 R19 independent source and written visual audit

## Why

R18 的雙人無背景敘事審核失敗，作者修成 R19。新版來源、逐句主張和書面畫面須由非作者按精確內容獨立覆核，不能沿用 R18 PASS。

## Definition of done

- [x] 產出綁定五檔 SHA-256 的 R19 獨立史料、115 句主張和書面畫面裁決回條。

## Steps

- [x] 重取三份固定原文，驗證 R19 修訂點、來源層級及畫面邊界。
- [x] 核對五檔 SHA、逐句對齊、lint 與最快文字時長，寫出 PASS／後續關卡。

## How to verify

`sha256sum docs/videos/curio-s52/{brief.md,research.md,claims.md,video.json,script.md}`；`node tools/video/cli.mjs lint --slug curio-s52 --json`；逐句解析 `claims.md` 與 `video.json` 的 ID／文字；固定 GitHub commit 原文重下載並核 SHA。結果見 `docs/videos/curio-s52/review/r19-source-independent.md`。

## Notes

史料、115／115 主張、書面畫面 PASS。R18 五檔完整快照不在工作區，故不聲稱 byte-level 反向重建；R19 的五檔 SHA 及作者列出的修訂點已逐一核對。下一關是新雙人無背景盲讀，音檔與媒體另驗。
