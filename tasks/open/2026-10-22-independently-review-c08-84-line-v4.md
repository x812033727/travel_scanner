---
id: 2026-10-22-independently-review-c08-84-line-v4
title: Independently review C08 84-line v4 repair delta
status: review
priority: P2
area: docs
owner: codex-c08-independent-v4
claimed_at: 2026-10-22T18:16:38Z
created_at: 2026-10-22T18:16:33Z
completed_at:
branch: codex/brand-story-kikkoman-c08-script
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-84-delta-v4.md
---

# Independently review C08 84-line v4 repair delta

## Why

PR #1681 v3 independent review held four story/source/visual points and three documentation inconsistencies. The author revised the 84-line draft, then pushed a final visual prompt cleanup. Review only that exact v4 repair delta and its adjacent narration/visual pairs without changing the author's files.

## Definition of done

- [x] A unique exact-hash v4 review receipt records PASS/HOLD for the repaired IDs, nearby lines, J1 evidence wording, and remaining production gates.
- [x] Only this ticket and its scoped review receipt enter the review commit; pre-existing untracked duplicate task copies stay untouched.

## Steps

- [x] Reopen J1 slide 15 and the K3/K6/K7/M1/E1/K4 primary or first-person pages; compare the final v4 input to v3 HOLD.
- [x] Verify every ID remains paired, check prompt/card boundaries and timing as estimates, then publish the narrow receipt.

## How to verify

`Get-FileHash` for the three authored inputs; `gh pr view 1681 --json headRefOid,isDraft,autoMergeRequest`; 84/84 unique ID comparison; `git diff --cached --check`; review the exact changed-file list and PR body readback.

## Notes

Final author input head `a8c6d326ca5e62683ce20a85a4d3dc9634f7dd60`; script SHA-256 `06A9429AE3730A55E6C43D2A867BE1E481747325B4E5FB95B262AA7B7D443EE2`, visual SHA-256 `FB559AEC23D55713843886CEACA91603D0F22C9BA4888A36B27A34E4276B0D18`, addendum SHA-256 `7BBEF819C0911CA16B372F904A0FBF5144C8C13CA409BE8A475C7A473391C452`. Narrow source/story/visual repair PASS; full video timing, actual illustrated seconds, blind reads and owner gates remain HOLD. Receipt: `docs/videos/story-everyday-kikkoman-c08/reviews/line-source-visual-review-20261023-84-delta-v4.md`. Six older duplicate open-task copies are pre-existing untracked files and must not be staged or removed.
