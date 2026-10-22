---
id: 2026-10-22-verify-patagonia-c09-script-sources
title: Independently verify Patagonia C09 script and shot sources
status: done
priority: P2
area: docs
owner: codex-c09-independent-script-review
claimed_at: 2026-10-22T13:43:38Z
created_at: 2026-10-22T13:43:33Z
completed_at: 2026-10-22T13:45:36Z
branch: codex/brand-story-patagonia-c09-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09-script-review
---

# Independently verify Patagonia C09 script and shot sources

## Why

The owner adopted a SHA-bound C09 Patagonia Treatment, then the author wrote a new 101-ID script and matching visual plan. Treatment review and author self-check cannot substitute for another agent re-reading the source pages and checking every new factual implication before the owner considers the script.

## Definition of done

- [x] A separate review folder holds a source verdict bound to the exact script, visual and author-evidence SHA-256 inputs; the receipt covers every ID and states limitations.

## Steps

- [x] Verify the three input hashes and 101/101 ID alignment, with 84 illustration rows and 17 cards.
- [x] Reopen S1/S2/S3/S4/S6/S7/S9 directly and check original-versus-retrospective attribution, added S4 details, 1972 piton exception, 1977 observation and catalog-edition limits.
- [x] Record the verdict, exact coverage ranges and visual/editorial cautions in the independent review receipt.

## How to verify

`Get-FileHash docs/videos/story-everyday-patagonia-c09/{script,visual-plan,script-evidence}.md -Algorithm SHA256` (three explicit paths); `git diff --check`; `npm run check:tasks`. Reopen the seven direct publisher URLs linked in the review receipt, not only the author's quotations. Count `^| c09dddd |` rows in script and visual plans and compare ID sets.

## Notes

Source verdict: PASS, pending two genuinely cold narrative reads, separate visual preflight, owner script approval and real TTS duration. c090211's blurred hanger should be neutralized before generation; c090615's accounting shorthand should remain scoped to cited evidence. S4 online text discloses automated digitization, so any future verbatim quote should be checked against its print scan. The undated S8 catalog scan was not used to prove 1972 first-print merchandise. Local policy-blocked untracked orphan task copies predated this review and were left untouched.
