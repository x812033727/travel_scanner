---
id: 2026-10-16-allow-brand-story-dub-preselection-while
title: Allow brand story dub preselection while final cut remains gated
status: done
priority: P2
area: web
owner: codex-story-dub-preselect-8a78
claimed_at: 2026-10-16T14:09:44Z
created_at: 2026-10-16T14:09:04Z
completed_at: 2026-10-16T14:48:31Z
branch: codex/story-dub-preselect-20261016
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/tests/test_video_reviews.py
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/DUBS.md
  - docs/videos/LANGUAGES.md
---

# Allow brand story dub preselection while final cut remains gated

## Why

Brand story A01 currently has English, Japanese and Korean title/description and CC choices,
but the dub boxes cannot be selected until a clean final is approved. The owner explicitly
chose to save dub intent now and make the tracks only after the exact Chinese final passes
review and proves switchable zh-TW CC.

## Definition of done

- [x] Brand story dub boxes can be selected and saved before its first final cut; other
  ineligible drama categories remain locked.
- [x] No translation, dub, retry or paid work starts for a preselected story until the current
  final is approved with full QA and `subtitles_burned_in=false` bound to its hash.
- [x] Initial cut submission/approval retains preselection; a replacement of an approved cut
  withdraws old dub consent. The UI distinguishes selected intent from production readiness.
- [x] API, UI and worker tests cover the gates; language policy docs match the behavior.

## Steps

- [x] Add API selection and final-cut lifecycle rules.
- [x] Add worker fail-closed dispatch checks.
- [x] Update the admin panel, translations, tests and docs.

## How to verify

Run the focused API video review tests, web video review tests and video automation tests,
then the affected lint, i18n and typecheck checks. Read back saved choices in the admin UI.

## Notes

2026-10-16 ownership audit: the board reports overlap with four old tickets, but their PRs
#1475, #1482, #1499 and #1520 are all merged; no open PR or checked-out worktree owns their
target files. The #1520 claim is still less than 24 hours old but its PR merged at 01:38 UTC.
This ticket covers only the named files and will use `claim --force` to override stale board
metadata, not another agent's active work. A01 production is blocked at narrative review and
has no final.mp4, final review or paid media work; source `burn_in=false` is not QA evidence.

2026-10-16 implementation: `story_dub_preselectable` allows saving EN/JA/KO dub intent,
while `dub_allowed` remains the production gate. The worker binds the actual local final.mp4
SHA to the current approved site final and rechecks before each paid translation/dub call,
including retry. First final submission retains the choice; submitting a replacement of an
approved clean final withdraws the old choice. The UI labels selected intent as waiting for
this cut's approved switchable-CC QA; locale-selection time is never final-approval proof.
The independent reviewer signed the 11-file duration receipt in the paired done task.
Focused API tests: 154 passed; worker targeted tests: 6 passed; API Ruff and focused mypy
passed; web targeted tests/lint/typecheck were run while broader checks were in progress.
Production UI readback and paid work remain separate release/owner gates.
