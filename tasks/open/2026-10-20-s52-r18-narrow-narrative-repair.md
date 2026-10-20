---
id: 2026-10-20-s52-r18-narrow-narrative-repair
title: S52 R18 narrow narrative repair
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T21:18:49Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s52/video.json
  - docs/videos/curio-s52/claims.md
  - docs/videos/curio-s52/script.md
  - docs/videos/curio-s52/review/r18-author-fix.md
---

# S52 R18 narrow narrative repair

## Why

R17 兩位隔離讀者按正式 OR 僅 12／13，兩人共同否決 `no_recap`；開場地點特有的問句也有一名讀者認為未回答。需要只改受影響句子和主張，維持真實史料範圍與至少八分鐘正文。

## Definition of done

- [x] R18 五檔凍結、逐句主張對齊，刪去具體重述；lint 0／0、最快正文估時仍逾八分鐘。

## Steps

- [x] 對照 R17 兩份凍結答卷，處理共同 `no_recap` 與開場問句範圍。
- [x] 同步 `video.json`、`claims.md`，重生 `script.md`，記錄精確五檔雜湊及後續獨立關卡。

## How to verify

`node tools/video/cli.mjs script --slug curio-s52`、`node tools/video/cli.mjs lint --slug curio-s52 --json`、逐句比對 116 行與主張、`estimateTimeline(doc,325)`、`git diff --check`；數值與雜湊見 `docs/videos/curio-s52/review/r18-author-fix.md`。

## Notes

R18 仍是作者候選，必須重新獨立來源／畫面及全新兩名隔離盲讀。R17 盲票和 R16 語音不適用新雜湊；本輪不做 TTS 或生圖。
