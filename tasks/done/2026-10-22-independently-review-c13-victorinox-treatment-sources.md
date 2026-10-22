---
id: 2026-10-22-independently-review-c13-victorinox-treatment-sources
title: Independently review C13 Victorinox treatment sources
status: done
priority: P2
area: docs
owner: codex-c13-independent-review
claimed_at: 2026-10-22T15:56:59Z
created_at: 2026-10-22T15:55:39Z
completed_at: 2026-10-22T16:06:40Z
branch: codex/brand-story-victorinox-c13-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-victorinox-c13/reviews/independent-treatment-review.md
---

# Independently review C13 Victorinox treatment sources

## Why

The C13 draft needs a separate reader to verify its 1989/1999 reversal, SABI versus Victorinox AG denominators, 2001–02 sales claims, product responses, retrospective testimony and story/visual limits before the owner can adopt it.

## Definition of done

- [x] A separate reviewer reopens S1–S9 and relevant contradictory originals, judges M01–M13 and the six-chapter treatment, and signs a PASS or HOLD receipt tied to SHA-256 of both reviewed files.
- [x] The review receipt states exact corrections and leaves author files, PR draft status and later production gates untouched.

## Steps

- [x] Check current PR/worktree ownership and claim the one-file review scope.
- [x] Read official Victorinox history, original SABI SEC filings, Swissinfo reporting, CEO interviews, TSA history and live list.
- [x] Compare M01–M13, causal boundaries, story duration evidence and visual rules; verify treatment/matrix SHA-256.
- [x] Sign the receipt under the scoped reviews path with source URLs and required corrections.

## How to verify

Run Get-FileHash on treatment.md and source-matrix.md and compare to the receipt; run git diff --check and npm run check:tasks; read back the receipt and PR #1693 draft/no-auto-merge state. No script, paid generation, import, upload, publishing or merging is in this task.

## Notes

2026-10-22: The author task scopes the parent C13 directory. The author explicitly requested this separate agent's independent receipt in a new exact review file; the claim used --force only for that known parent-directory overlap. No treatment or source-matrix edit was made.

2026-10-22: HOLD on M05. Swissinfo's 2002-01-29 English agency report says knife sales fell nearly one-third in 2001 Q4. Swissinfo's earlier 2002-01-25 direct interview with Victorinox export manager Paul Camenzin says ~30% applied only to October; its Portuguese edition says full-year pocketknife sales fell 7.5%, especially in the U.S. The receipt records both URLs, cause/denominator limits and other narrower corrections. M02 pre-9/11 watches/travel gear and M03/M07 separate-entity boundaries passed.
