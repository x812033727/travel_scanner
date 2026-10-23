---
id: 2026-10-23-independently-audit-c19-seven-bank-v5
title: Independently audit C19 Seven Bank v5 sources and visuals
status: review
priority: P2
area: docs
owner: codex-c19-v5-source-review
claimed_at: 2026-10-23T07:57:06Z
created_at: 2026-10-23T07:56:53Z
completed_at:
branch: codex/c19-seven-bank-v5-full-review
depends_on: []
scope:
  - docs/videos/story-everyday-seven-bank-c19/reviews/independent-v5-source-visual.md
---

# Independently audit C19 Seven Bank v5 sources and visuals

## Why

C19 Seven Bank v5 rewrote the 79-line story broadly, so the v4 independent receipts cannot certify the new narration or its paired visuals. This review must be pinned to the exact author commit and primary disclosures before the owner is asked to approve the v5 script.

## Definition of done

- [x] A separate, hash-bound receipt checks all 79 narration lines and all 79 paired visuals against primary sources and the Curio illustration rules.
- [x] The receipt distinguishes source PASS from visual HOLD by ID and names the minimal fixes without editing the author draft.
- [x] Publish the receipt as a draft PR stacked on the exact author head; leave author approval and production gates pending.

## Steps

- [x] Reopen official Seven Bank history, 2001 notice, 2002 disclosure, 2005 naming notice, 2010 annual report and 2024 integrated report.
- [x] Verify 79/79 ID, narration, source-note and MD/JSON visual parity plus four file SHA-256 hashes.
- [x] Review every current line and paired visual; write `docs/videos/story-everyday-seven-bank-c19/reviews/independent-v5-source-visual.md`.
- [x] Commit, push and create stacked draft PR #1769 with `no-auto-merge` label.

## How to verify

`python -c` parse of all four files yielded 79/79/79/79 rows, exact ID and text parity, 66 shots, 13 cards, maximum two consecutive cards and the receipt's four hashes. Read official sources linked in receipt. Run `git diff --check` and `npm run check:tasks` before push, then verify PR base/head with `gh pr view`.

## Notes

Audit base: PR #1742 head `8849fe98ee08b9741c67d715fbd781938799fa94`. Full result: narration/source 79/79 PASS; visuals 72/79 PASS, 7/79 HOLD (`c190204`, `c190309`, `c190403`, `c190504`, `c190516`, `c190517`, `c190610`) due to more than one person or simultaneous actions in MiniMax prompts. Actual TTS and rendered image time are still untested. Do not infer owner script approval or paid-media authorization from this review.

Draft reviewer PR: https://github.com/x812033727/travel_scanner/pull/1769 ; review commit `ba282bce3` (task bookkeeping may add one follow-up commit). The Codex app PR attachment tool returned unavailable; the PR URL remains in this task and parent handoff.
