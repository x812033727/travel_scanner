---
id: 2026-10-21-curio-s38-r8h-pf004-age-identity-repair
title: Remove unsupported age and likeness cues from S38 pf004
status: done
priority: P2
area: docs
owner: codex-s38-r8g-author
claimed_at: 2026-10-21T00:22:00Z
created_at: 2026-10-21T00:22:00Z
completed_at: 2026-10-21T00:23:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/video.json
  - docs/videos/curio-s38/verify-18-r8h-author.md
  - docs/videos/curio-s38/verify-18-r8h-structured-diff.json
---

# Remove unsupported age and likeness cues from S38 pf004

## Why

The untested R8g prompt said `middle-aged` and supplied specific hair and beard features for an implied Pepys figure. The site-fixed D4b/D5 diary passages do not establish those features, and the age cue would make a man in his thirties look older.

## Definition of done

- [x] Revise only `pf004`'s prompt to depict an adult in his thirties without specific likeness features.
- [x] Keep the full-body wide garden view and distant fire concept without changing the series look.
- [x] Freeze five creative SHA-256 values, visual hash, and reversible single-leaf R8g→R8h diff in [the author receipt](../../docs/videos/curio-s38/verify-18-r8h-author.md).
- [x] Preserve private STOP, media budget, and owner website cards without a new paid call.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-s38 --json`; compare [structured diff](../../docs/videos/curio-s38/verify-18-r8h-structured-diff.json) and reconstructed R8g SHA `dbd6a5c262674507e7e58097a436f2ff470fab89e21589ef5b83056b4742b2dd`.

## Notes

Author proposal only. Independent written review and one bounded native-media retry remain pending.
