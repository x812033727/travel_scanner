---
id: 2026-10-20-curio-s39-r3a-prompt-recheck
title: Independently recheck S39 R3a still prompts
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T01:08:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/verify-8.md
---

# Independently recheck S39 R3a still prompts

## Why

R3 independently passed narrative 13/13 and historical claims 89/89, but static prompt review blocked 13 document surfaces. The author changed prompts only and recorded old/new hashes in `docs/videos/curio-s39/verify-7.md`.

## Definition of done

- [ ] Independent checker confirms the exact only differences from R3 are `data.prompt` on `cs052`, `cs056`, `cs057`, `cs058`, `cs061`, `cs062`, `cs073`, `cs075`, `cs078`, `cs080`, `cs081`, `cs083`, `cs086`.
- [ ] Each of those 13 prompts makes **every visible document surface** blank or unmarked, with no competing focal subject; a quick pass over the other 73 prompts finds no newly relevant flaw.
- [ ] Record an explicit pass/block decision against R3a `video.json` SHA-256 `cefceb2ab42451f962bdad8f4910ac12b2aae849b927f6bc363c527e2d214264` before any media generation.

## How to verify

Compare R3a file hashes with `docs/videos/curio-s39/verify-7.md`; inspect a structured old/new `video.json` diff and run `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json`.

## Notes

The independent R3 report is `/tmp/curio_s39_r3_source_visual_audit.md`. This task is a **focused prompt recheck**; the R3 narrative and source verdicts only carry forward if their artifact hashes remain identical.

2026-10-20 03:17 UTC：86 張 still 的獨立史料／年代預檢無阻擋；六個 prompt-only 定點修訂處理凱撒雕像、未載石椅與刺殺動作，第二位讀者對現行 video SHA `da7103cb7f19ce07ca48956c46a7bdf26216d25f46a63cb4f3c4cba7e898308c` 覆核 PASS，lint 0／0。尚未購買插圖；詳 [verify-11.md](../../docs/videos/curio-s39/verify-11.md)。
