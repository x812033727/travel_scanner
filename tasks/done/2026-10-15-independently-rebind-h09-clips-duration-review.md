---
id: 2026-10-15-independently-rebind-h09-clips-duration-review
title: Independently rebind H09 clips duration review
status: done
priority: P1
area: docs
owner: codex-gpt6-h09-duration-review
claimed_at: 2026-10-15T02:04:41Z
created_at: 2026-10-15T02:04:21Z
completed_at: 2026-10-15T02:13:53Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Independently rebind H09 clips duration review

## Why

The H09 branch changed the bound `tools/video/media/clips.test.mjs` in b44dde2c3 and 8cd022593. The independent long-form duration receipt still has the pre-change SHA, so `node tools/video/long-form/cli.mjs check` fails. The owner transferred the two receipt files out of the earlier Curio series-look task's scope for this independent review.

## Definition of done

- [x] An independent reviewer inspects the exact final clips test diff and confirms the eight-minute, catalog-body, frame/FPS, target, and media-length rules are unchanged.
- [x] The genuine report and receipt bind only the final reviewed `clips.test.mjs` bytes, identify separate author and reviewer, and preserve all other bindings.
- [x] The duration CLI check, review regression test, and task-board check pass on the new receipt.

## Steps

- [x] Verify active scope ownership and claim only the two receipt files.
- [x] Compare the old receipt SHA with the pre-change Git blob and inspect b44dde2c3 plus 8cd022593.
- [x] Wait for the final Linux clips test result and stable commit SHA.
- [x] Add the independent DURATION_ONLY report increment and rebind review.json.
- [x] Run receipt and board checks; close this task in the same H09 branch.

## How to verify

`node tools/video/long-form/cli.mjs check`
`node --test tools/video/long-form/review.test.mjs`
`npm run check:tasks`

## Notes

Pre-change `clips.test.mjs` SHA256 was 626e678fc76d08210aad82a850f393c66009e9c3a7fce815a8097e686602b238, matching the current receipt. The committed 8cd022593 version is 48c4cb7de8e837575539aa7222460f904d4d87528a4cfadb2275764132d86d87. Current CLI failure names only that file. The affected test assertions cover reported cost for provider-refused seeds, no rebuy of charged failures, and a concurrent judge reservation for an imported paid clip; no duration behavior was changed in the inspected diff. Local Windows Node test execution crashes at the file level without assertion diagnostics, so Linux CI is the test gate.

Independent DURATION_ONLY verdict: pass for committed 8cd02259373762b806b67815f098a1a377f9d5d5. The final clips.test.mjs SHA256 is 48c4cb7de8e837575539aa7222460f904d4d87528a4cfadb2275764132d86d87; report SHA256 is dbdb1cf72e0faa7ca609a179a1d6436e077294235b34a2947a84046386c2c0cd. All 108 receipt bindings were retained, with only clips.test.mjs updated. Verification: long-form CLI check passed all 473 plans; review.test.mjs passed 2/2; npm run check:tasks validated 1876 task files; git diff --check passed. Root confirmed Linux smoke, web-checks and video-tests at 8cd each only showed the stale duration binding, while the new seed-4 media test passed. I did not independently fetch CI logs; local Windows Node runner did not provide an assertion result.
