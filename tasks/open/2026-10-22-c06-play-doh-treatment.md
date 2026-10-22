---
id: 2026-10-22-c06-play-doh-treatment
title: Research and outline C06 Play-Doh everyday reversal
status: review
priority: P2
area: docs
owner: codex-gpt6-c06-treatment
claimed_at: 2026-10-22T03:40:58Z
created_at: 2026-10-22T03:40:53Z
completed_at:
branch: codex/brand-story-play-doh-c06-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-play-doh-c06
---

# Research and outline C06 Play-Doh everyday reversal

## Why

The 20-episode series names Play-Doh as C06, but the roster is a research lead,
not a verified film. Distinguish the wallpaper-cleaner business, the later
classroom account, product reformulation, Rainbow Crafts, the 1960 patent and
the 1965 sale before any script or paid media is approved.

## Definition of done

- [x] A six-chapter, hook-led nonpaid Treatment follows one causal object story
      and explicitly applies the Curio illustration and duration rules.
- [x] A source matrix links each factual premise to directly read company,
      collecting-institution or original patent material with claim boundaries.
- [x] An independent checker reviews the exact document hashes and records a
      PASS or required corrections.
- [x] A draft PR exposes the Treatment and source review for owner direction;
      no script or media approval is inferred.

## Steps

- [x] Read Kutol, Hasbro, The Strong and the original US3167440A record.
- [x] Draft Treatment and source matrix in the C06 folder only.
- [x] Resolve independent source-check findings, then bind final hashes.
- [x] Run task/doc checks, commit and open a draft PR.

## How to verify

Reopen each linked source, check `Get-FileHash` for Treatment/matrix and the
independent review, run `npm run check:tasks` and relevant docs-video lint/tests.

## Notes

2026-10-22: Official Kutol company history supports the Kroger agreement and
Kay Zufall account but supplies no dated original contract or classroom log.
The Strong's archive article supplies 1950s chronology while acknowledging
a later toy-history book as part of its basis. Patent US3167440A was filed in
1960 and granted in 1965, after the 1956 toy debut; it cannot prove that the
1930s cleaner and current toy use an unchanged recipe. Hasbro confirms the
wallpaper-cleaner origin but its current market numbers are not history.
Rainbow Crafts, not all of Kutol, was sold to General Mills in 1965.

Independent read-only reviewer `/root/c06_source_independent` first returned
NEEDS_FIX for a 1955/1956 first-sale overstatement, same-institution double
counting, stale present-tense evidence and an unsupported patent-motive hook.
The author corrected all three issue groups. Reviewer reread the final
Treatment SHA 14B33CCB9C51E3451D9A0D2FE287056185E15FDDCCD3DB3A5CA284D76BB950A1
and source matrix SHA D18F1BBC58E6A141B957EAD9AC42A7A4375E2004A7736D0D6C57B59044D58FD2;
verdict PASS for nonpaid Treatment only. See `reviews/source-review.md`.

Draft PR #1674 is stacked on the 20-episode series branch and labeled
`no-auto-merge`. The owner has not yet approved this C06 direction. No C06
script, priced production, media, import, upload or publication exists.
`npm run check:tasks` exited 0 with unrelated existing claim warnings;
`git diff --check` exited 0. The ticket stays `review` until owner direction
and the PR disposition are known.
