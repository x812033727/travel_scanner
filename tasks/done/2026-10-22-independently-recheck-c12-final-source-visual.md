---
id: 2026-10-22-independently-recheck-c12-final-source-visual
title: Independently recheck C12 final source visual repair
status: done
priority: P2
area: docs
owner: codex-c12-source-delta
claimed_at: 2026-10-22T16:51:02Z
created_at: 2026-10-22T16:50:57Z
completed_at: 2026-10-22T16:53:23Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v5.md
---

# Independently recheck C12 final source visual repair

## Why

The C12 author repaired three source/chronology HOLDs and adjusted adjacent lines and visuals. The new script and visual hashes need an independent, narrowly scoped source and visual recheck.

## Definition of done

- [x] Save a signed SHA-bound PASS/HOLD receipt for five changed narration and six changed visual IDs.
- [x] Check adjacent E09–E11 and T01–T12 chronology and material boundaries against museum and company originals.

## Steps

- [x] Verify head, both file hashes, changed rows, and 80 unique IDs per file.
- [x] Reopen the Corning Museum and Corning Incorporated originals and save the verdict.
- [x] Run final whitespace/task checks and close this ticket.

## How to verify

`Get-FileHash` for both inputs; `git diff --unified=0 1c050e00f 1efbd8ee...` for exact row changes; `git diff --cached --check`; `npm run check:tasks`.

## Notes

Receipt: `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v5.md`. Source and visual delta PASS; preserve the two unrelated pre-existing open/done ghost copies in this checkout.

`npm run check:tasks` exits 1 only for those two pre-existing duplicate ghost IDs. Input hashes and 80 unique IDs per file match. Final staged whitespace check is performed before commit.
