---
id: 2026-10-07-a-tidied-video-s-skipped-language
title: A tidied video's skipped-language batch carries no source proof
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T08:03:28Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# A tidied video's skipped-language batch carries no source proof

## Why

After the worker tidies a video (`tools/video/automation/tidy.mjs`), a language the owner ticks
later cannot be made, so `tidiedLanguages()` in `tools/video/automation/flow.mjs` posts a
`languages` review that marks the new parts skipped. It posts no files: no `metadata` and no
`languages_manifest`.

That review is the video's newest language batch, and YouTube sync composes only from the
newest one: `apps/api/app/video_youtube/language_package.py` `compose()` then refuses with
"舊語言審核缺少可驗證的來源清單與 metadata，請重新送審", so the video can no longer be synced
at all (also not the languages that were made before the tidy). It is also a partial batch
(only the newly ticked parts), while `compose()` needs every chosen part in the newest batch.

## Definition of done

- [ ] Ticking a language after a tidy leaves the video's earlier languages syncable, and the
      panel still says why the new parts were not made.

## Steps

- [ ] Decide what the batch can bind to after a tidy (the approved confirmation and final are
      still on the site; the package files may be gone), or whether the skip should be reported
      some other way than as the newest language batch.
- [ ] Implement it in `flow.mjs` and cover it in `automation.test.mjs` (both bound by the
      duration receipt; rebind independently).

## How to verify

`node --test tools/video/automation/automation.test.mjs`, plus a consumer check of the batch the
test produces (see `apps/api/tests/test_video_youtube_language_contract.py`).

## Notes

- Found while binding normal batches to their source (claude-happy-carson, PR #1361);
  docs/videos/APPROVED-LANGUAGE-PACKAGE.md describes what the consumer needs.
