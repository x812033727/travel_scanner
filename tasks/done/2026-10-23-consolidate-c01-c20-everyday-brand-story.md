---
id: 2026-10-23-consolidate-c01-c20-everyday-brand-story
title: Consolidate C01-C20 everyday brand-story plans for paused admin import
status: done
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-23T09:16:23Z
created_at: 2026-10-23T09:16:17Z
completed_at: 2026-10-23T11:11:52Z
branch: codex/everyday-story-review-import-20261023
depends_on: []
scope:
  - docs/videos/brand-stories-everyday-reversals-20261020
---

# Consolidate C01-C20 everyday brand-story plans for paused admin import

## Why

The owner asked to finish the C-series PR stack by first importing all twenty reviewed plans and eligible approved scripts into the video admin. The existing #1610 series folder has a topic order and C01/C02 materials but no twenty episode rows, no independent hash-bound plan reviews, and no compiled import file. Later treatment PRs hold the source-checked directions. A canonical plan package is needed before safe admin import and PR closure.

## Definition of done

- [x] Twenty C01–C20 episode rows reflect the owner-adopted treatment directions and their source limits.
- [x] Another reviewer verifies each row against original sources, with a current hash-bound review; the builder emits a validated twenty-row `stories.json` only after all reviews pass.
- [x] The admin imports the same twenty rows under a paused series and reads them back without launching paid work.

## Steps

- [x] Bring the #1610 series plan into the canonical integration branch without copying experimental media as completed films.
- [x] Author ten C01–C10 and ten C11–C20 episode rows from the adopted treatments.
- [x] Complete independent claim/source review and hash binding for all twenty rows.
- [x] Compile, run the JavaScript and Python validators, dry-run the production import, and read back the paused series.

## How to verify

`node docs/videos/brand-stories-everyday-reversals-20261020/build.mjs`; Python `check_story_file` on `stories.json`; exact production `video-story-import` dry-run followed by paused apply/readback and zero new worker requests. Script cards have a separate exact version and owner approval gate.

## Notes

2026-10-23: The owner clarified "先匯入20集企劃與合格稿件到影片後台". C03/C04/C05/C06/C07/C08/C10/C11/C14/C15 have owner script/storyboard approvals at historical hashes; C01/C02 and C09/C12/C13/C16/C17/C18/C19/C20 do not. Rebind hashes and source receipts before pushing script cards. C03 has an existing project; all other episodes are absent in the exact live series API. Import is held until the series is paused and C03 collision is safely reconciled. No production mutation or new paid work has occurred.

Claim override rationale: #1610's October 20 task covers this folder, but its branch is not checked out in any live worktree; the owner explicitly requested a new admin-first completion path. This integration branch preserves #1610's unique files and the review stack before any old PR is closed. The old task file was left untouched.

2026-10-23 production receipt: #1778 merged at `6f9aec8d1606829d81a3acfe926c8d303bb1b0d9`
after 24/24 CI checks and deployed with 11/11 host verification checks. The exact
`stories.json` dry-run accepted all 20 create rows with zero problems/refusals; the
same file applied 20 rows. Independent database readback found one paused story
series, 20 planned episodes numbered 1–20, and zero `video_drama_requests`.
