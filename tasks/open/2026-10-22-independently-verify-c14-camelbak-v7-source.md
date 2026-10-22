---
id: 2026-10-22-independently-verify-c14-camelbak-v7-source
title: Independently verify C14 CamelBak v7 source and visuals
status: review
priority: P2
area: docs
owner: codex-c14-independent-v7
claimed_at: 2026-10-22T19:02:01Z
created_at: 2026-10-22T19:01:56Z
completed_at:
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/reviews/independent-v7-source-visual-review.md
---

# Independently verify C14 CamelBak v7 source and visuals

## Why

The C14 CamelBak author rewrote and shortened the v6 narration after two blind readers split HOLD/PASS. New factual wording and 70 paired shots require an independent source and text-visual check on exact v7 hashes before fresh blind reads.

## Definition of done

- [x] A new exact-hash independent v7 PASS/HOLD receipt with direct original-source links and actionable IDs is committed in this narrow scope.
- [x] Draft PR #1695 records the verdict without merging, owner adoption, paid media or self-approval.

## Steps

- [x] Reopen CamelBak history, 1998/2005 patents, the 2003 military report, 2006 exhibition report, 2007 company release and 2014 10-K.
- [x] Check all changed narration and paired visual directions for chronology, attribution, causation and denominator.
- [x] Recompute 70 unique line/shot IDs, planned seconds, card run, illustration share and hook gaps.

## How to verify

Compare the six SHA-256 values in `docs/videos/story-everyday-camelbak-c14/reviews/independent-v7-source-visual-review.md` with `Get-FileHash -Algorithm SHA256`. Read the one-line N10 HOLD and v7 arithmetic there. Verify `git diff --check`, PR #1695 head/draft/`no-auto-merge` and PR-body readback after push.

## Notes

All changed claims checked except N10. N10 says both systems bring water near the mouth *only* when drinking; the brand's hose is already over the shoulder and clamped at the end, while the 2006 exhibition report supports a flip-up bite valve, not a time/position measurement. Narrow the line to outlet-flow control, recheck new hash and paired shot, then send full narration to two fresh blind readers. Paper body 496.0s has only 16.0s margin above 480 and is not measured TTS. Old v4 untracked open/done task ghosts remain untouched after policy-blocked deletion; local `check:tasks` fails on their duplicate ID.
