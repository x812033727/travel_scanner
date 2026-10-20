---
id: 2026-10-20-s52-r17-source-independent
title: S52 R17 independent source and visual diff review
status: done
priority: P2
area: docs
owner: codex-s52-r17-source
claimed_at: 2026-10-20T21:15:09Z
created_at: 2026-10-20T21:15:07Z
completed_at: 2026-10-20T21:16:37Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s52/review/r17-source-independent.md
---

# S52 R17 independent source and visual diff review

## Why

S52 R17 在兩輪定點重配後改了唯一一行旁白。舊版史料、敘事及音訊判定都綁 R16 雜湊，須獨立核新稿來源、改動範圍和書面畫面。

## Definition of done

- [x] `review/r17-source-independent.md` 有五檔雜湊、固定原文核對、R16→R17 精確差分及 PASS／HOLD 界限。

## Steps

- [x] 重讀固定 Cook 日誌與 1771 原報 OCR，檢查新句及緊接答句的可說範圍。
- [x] 逆換一行驗 claims／video 舊版雜湊，重生舊版 script 驗雜湊；核全篇對齊及 lint。

## How to verify

`sha256sum docs/videos/curio-s52/{brief.md,research.md,claims.md,video.json,script.md}`；`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s52 --json`；見報告中的逆換及 `screenplay()` 重生結果。

## Notes

PASS 只涵蓋 R17 史料、主張與書面畫面。新讀者、TTS 和完整音訊尚須單獨完成。單純逆換 `script.md` 句子無法恢復 R16 SHA，因劇本尾端有 narrative／speech 內容雜湊；從逆換後的 video.json 重生則完全吻合 R16。
