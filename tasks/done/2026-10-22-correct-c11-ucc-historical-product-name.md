---
id: 2026-10-22-correct-c11-ucc-historical-product-name
title: Correct C11 UCC historical product name in script
status: done
priority: P2
area: docs
owner: codex-c11-ucc-author
claimed_at: 2026-10-22T17:22:06Z
created_at: 2026-10-22T17:21:47Z
completed_at: 2026-10-22T17:24:19Z
branch: codex/brand-story-ucc-c11-script
depends_on: []
scope:
  - docs/videos/story-everyday-ucc-c11/script.md
  - docs/videos/story-everyday-ucc-c11/script-source-notes.md
  - docs/videos/story-everyday-ucc-c11/reviews/script-source-v5-c110410-author-repair.md
---

# Correct C11 UCC historical product name in script

## Why

The independent v5 C11 source/visual review holds only `c110410`: saying the 1969 product was "then named" a constructed Chinese title claims a historical exact name not found in UCC's source. Both cited UCC retrospectives record `UCCコーヒーミルク入り`. Correct one spoken line without changing the reviewer's receipt, paired visual card, other narration or IDs.

## Definition of done

- [x] `c110410` states only the April 1969 launch of UCC's milk-containing canned coffee, without inventing its contemporary title.
- [x] Script status/source notes and an author repair record preserve the old v5 HOLD and bind new hashes; visual bytes and 78 IDs remain unchanged.
- [x] Focused checks pass, the draft PR is updated, and new independent source and two fresh blind gates remain pending. No paid generation or publication.

## Steps

- [x] Read the independent v5 HOLD receipt and directly reopen both UCC pages for the name/date.
- [x] Correct the one line, record hash-bound author repair and preserve source/visual gates.
- [x] Run focused checks and push the original draft PR branch.

## How to verify

Compare committed old/new narration rows; verify 78 ordered script/visual IDs and no changed visual objects; parse JSON and mirror Markdown rows; `git diff --cached --check`; verify working and committed SHA-256 values; read back draft PR #1691 head. Independent source and blind judgments must come from other reviewers.

## Notes

U1 and U2 explicitly write the then-name as `UCCコーヒーミルク入り`, with April 1969 launch. The new narration uses a description, not a translated product name. The unchanged postproduction date card writes only the date and category. Old v5 independent receipt is HOLD for old script SHA `82618E246DFBFA75F453224A5D79B18A6E9C8E16F44DBF7549D3F6CC50F138BA`; it cannot certify the new script. This worktree also retains eight untracked orphan open-task copies from earlier C11 work, outside this task's scope; exclude them from the PR.
