---
id: 2026-10-24-bind-c20-short-v8-backend-plan
title: Bind C20 Zippo short v8 plan to approved script
status: in-progress
priority: P1
area: docs
owner: codex-c20-backend-plan
claimed_at: 2026-10-24T08:41:47Z
created_at: 2026-10-24T08:41:15Z
completed_at:
branch: codex/c20-short-v8-backend-plan-20261024
depends_on: []
scope:
  - docs/videos/brand-stories-everyday-reversals-20261020/episodes/C20.json
  - docs/videos/brand-stories-everyday-reversals-20261020/episodes/reviews/C20.json
  - docs/videos/brand-stories-everyday-reversals-20261020/build.mjs
  - docs/videos/brand-stories-everyday-reversals-20261020/stories.json
  - docs/videos/brand-stories-everyday-reversals-20261020/reviews/c20-short-v8-plan-review-20261024.md
---

# Bind C20 Zippo short v8 plan to approved script

## Why

The twenty-row backend story bundle still presents C20 as its earlier long
plan. The owner subsequently approved the precise 36-line Zippo short-v8
script and visual direction. The backend plan must faithfully reflect that
approved version before any guarded same-row import; the old plan remains in
Git history and the original source/project documents.

## Definition of done

- [x] C20's six beats, source matrix and exact short-v8 slug match the approved
      script without adding a new narrative direction.
- [x] An independent source receipt binds the final plan hash and the compiled
      bundle contains exactly 20 rows, with only C20 changed from main.
- [ ] Local plan, task-board and bundle checks pass; a draft PR is available.
- [x] This task does not run a production import, modify script-intake manifest,
      generate paid media, or upload/publish a video.

## Steps

- [x] Claim the five exact plan/compiler/receipt paths on one shared checkout.
- [x] Project the owner-approved short-v8 story into the C20 plan.
- [x] Obtain an independent, hash-bound source review and write its receipt.
- [ ] Rebuild and inspect the 20-row bundle, test, push and open draft PR.

## How to verify

Run `node docs/videos/brand-stories-everyday-reversals-20261020/build.mjs`,
`npm run check:tasks`, relevant plan tests and `git diff --check`. Compare
the compiled C20 row to the plan and all other rows to `origin/main`; confirm
the old and new slug are distinct and production has not been called.

## Notes

The owner adopted the C20 direction and approved the exact short-v8 36-line
script/36-scene direction. The new plan is a faithful projection of those
approvals; it preserves the original title/thumbnail packaging and avoids the
old wartime, Arc, date-code and tracked-shipping branches. Importer and
approved-script manifest paths belong to separate work. The first candidate
source hash `6864b6bf7b6f79bbc5ada2b09edf68d83e746eb49c102324187c779ba55c0161`
was held by the independent reviewer for one source mapping and one
regional-scope sentence. The next candidate hash
`08f2737e70e6e9b1a0cefafca6e9def65d8ca9c1aad51f3531a7859fbebd9de1`
needed a final source-index description fix. Independent reviewer `/root` opened
all nine sources and signed final hash
`a473ba0aefa3ede0f234cb9b9b352361c16009752c75aa3e5cbed48b3dd1a057`.
Compiled bundle has 20 rows; only C20 story and C20 review certification
differ from `origin/main`.
