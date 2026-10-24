---
id: 2026-10-24-integrate-approved-c08-and-c20-backend
title: Integrate approved C08 and C20 backend intake
status: done
priority: P1
area: tools
owner: codex-root
claimed_at: 2026-10-24T09:30:59Z
created_at: 2026-10-24T09:30:48Z
completed_at: 2026-10-24T09:39:07Z
branch: codex/c08-c20-backend-intake-20261024
depends_on: []
scope:
  - docs/videos/brand-stories-everyday-reversals-20261020/approved-scripts.json
  - tools/video/review/script-intake.mjs
  - tools/video/review/script-intake.test.mjs
  - docs/videos/brand-stories-everyday-reversals-20261020/reviews/c20-short-v8-script-intake-20261024.md
---

# Integrate approved C08 and C20 backend intake

## Why

The production series has 20 paused, planned episode rows, but C08 and C20 still
point to historical long-version slugs. Their short scripts and directions have
since been approved by the owner. Importing a changed slug without the exact
plan and script guards could create a duplicate row or attach an old approval
to the new text. This integration collects the reviewed C08 and C20 changes in
one release so the host can update the same rows and accept new pending cards.

## Definition of done

- [x] C08 and C20 short-v8 plans, same-row importer and exact script entrances
      are in one branch, with the original projects and source material intact.
- [x] C20's 36 narration lines and six chapters are bound to the owner's exact
      approved candidate, projection and canonical video hashes.
- [x] Local tests and build checks pass; a separate reviewer found no blocker
      in the exact C20 approval, parser, plan update or same-row importer.
- [x] Production import, payment, worker start, upload and publication remain
      separate guarded steps with persisted readback.

## Steps

- [x] Inspect production read-only state: paused series, 20 planned rows and
      old C08/C20 slugs; preserve C08's historical approved script card.
- [x] Integrate reviewed C08 script PR #1823, C20 plan PR #1824 and C20
      same-row importer PR #1826 onto current main in the shared checkout.
- [x] Add the C20 exact approved-script manifest entry, strict single-table
      parser, source/video parity guards, and targeted negative tests.
- [x] Obtain final independent review and run relevant checks; prepare the
      shared branch for one integration PR/CI cycle and finish original tickets.

## How to verify

`node tools/video/review/script-intake.mjs --id C08` and `--id C20` must each
report 36 lines and `dry-run-local-only`. Run
`node --test tools/video/review/script-intake.test.mjs`,
`node docs/videos/brand-stories-everyday-reversals-20261020/build.mjs --check`,
focused `apps/api/tests/test_video_story_import.py`, `npm run check:tasks`,
and `git diff --check`. Inspect exact PR head and strict CI before merge.
On the host, require the separate deploy preflight and an import dry run with
only C08/C20 updates, then apply and read back the same 20 episode IDs and two
new pending cards.

## Notes

No new worktree or clone was opened. The shared checkout was handed over clean
after C12's local WIP commit. The pre-integration host is at `c9cbf0022`,
database revision 0138, and currently has neither a deploy hold nor an active
deploy lock. Main already includes migration 0139, so manual deployment needs
full preflight and the deploy skill's separate owner decision about carrying
this migration. The auto-deploy timer is not installed. A local script dry run
does not mean that the host has imported a script card.

Non-author C20 reviewer checked the three frozen SHA-256 values and 36/36 ID
and narration parity, 5/5 C20 API tests, 15/15 script-intake tests and the
20-row compiler, and reported PASS with no blocker. Root also ran 22/22 full
focused API tests, Ruff and mypy on the importer paths, both C08/C20 local
dry runs, and `git diff --check`. The broad `test:docs-videos` sweep was
stopped after unrelated long-running media tests; the focused gates passed
and CI will run the repository suite on the exact PR head.
