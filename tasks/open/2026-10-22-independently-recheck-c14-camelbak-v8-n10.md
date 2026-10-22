---
id: 2026-10-22-independently-recheck-c14-camelbak-v8-n10
title: Independently recheck C14 CamelBak v8 N10 delta
status: review
priority: P2
area: docs
owner: codex-c14-independent-v8
claimed_at: 2026-10-22T19:11:01Z
created_at: 2026-10-22T19:10:56Z
completed_at:
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/reviews/independent-v8-n10-delta-review.md
---

# Independently recheck C14 CamelBak v8 N10 delta

## Why

The independent v7 review held only N10: a line inferred that water approached the mouth only while drinking, although the brand origin account already put the tube over the shoulder. The author submitted v8 with a narrower outlet-flow claim and a 0.5-second N10 shot adjustment. An independent delta receipt must bind the exact new files before fresh full-script blind reads.

## Definition of done

- [x] An exact-hash independent PASS/HOLD receipt checks N10 spoken wording, the paired concept shot and N08–N11 continuity against S2/S11.
- [x] Draft PR #1695 records the narrow verdict without author edits, paid media, merge or self-approval.

## Steps

- [x] Reopen CamelBak NZ history and the contemporaneous GearJunkie 2006 exhibition report.
- [x] Compare all 70 spoken rows and 70 JSON shot objects with the v7 reviewed commit; recompute paper duration and illustration share.
- [x] Commit and push the reviewer-only receipt, then read back draft PR head and body.

## How to verify

Compare the six SHA-256 values in `docs/videos/story-everyday-camelbak-c14/reviews/independent-v8-n10-delta-review.md` with `Get-FileHash -Algorithm SHA256`. Check the N10 source boundary and v7→v8 structural diff there. Verify `git diff --check`, PR #1695 head/draft/`no-auto-merge`, and PR-body readback after push.

## Notes

PASS for the v8 N10 source and text-visual delta only: both products afford user-controlled outlet flow, while the new line makes no claim about physical distance to the mouth or identical parts. The 70 spoken rows changed only at N10; JSON changed only N10 planned duration 7.4→7.9 seconds. Paper body 496.5 seconds is not measured TTS; two fresh full-script blind readers and normal-speed TTS remain. Existing untracked v4 open/done task duplicates were previously blocked by policy for deletion and remain untouched; local `check:tasks` fails on that duplicate ID, not this receipt.
