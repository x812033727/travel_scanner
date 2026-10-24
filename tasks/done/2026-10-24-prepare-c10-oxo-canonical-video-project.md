---
id: 2026-10-24-prepare-c10-oxo-canonical-video-project
title: Prepare C10 OXO canonical video project without paid calls
status: done
priority: P1
area: docs
owner: codex-c-series-integration
claimed_at: 2026-10-24T03:17:22Z
created_at: 2026-10-24T03:17:17Z
completed_at: 2026-10-24T04:20:37Z
branch: codex/c10-oxo-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-oxo-c10
---

# Prepare C10 OXO canonical video project without paid calls

## Why

The owner-approved C10 OXO script and visual plan were source-backed Markdown/JSON but lacked the canonical video project files used by the local lint and QA path. This task converts those locked originals into a machine-readable, nonpaid project without treating a paper duration estimate as finished media or changing the owner-approved bytes.

## Definition of done

- [x] The approved script, visual JSON and visual Markdown retain their owner-bound SHA-256 hashes.
- [x] video.json and series.json express the 80-line, 80-scene six-chapter episode with 71 stills, nine cards, the Curio look, correct bookends, narrator and series identity.
- [x] brief.md, claims.md, verify-1.md and a conversion receipt record source boundaries, exact parity and the remaining media/approval gates.
- [x] Focused lint and factsChecks pass without paid generation.
- [x] Document the independent diagnosis of the core/drama.test.mjs process-level failure without changing unrelated tests or code.
- [x] Read back the non-author conversion review before task closure.

## Steps

- [x] Read C10 approval receipts and hash the locked source artifacts.
- [x] Convert each approved narration row and paired visual in order, without changing script.md or visual-plan files.
- [x] Recheck 80/80 parity, card runs, say_for hashes and source/visual limitations.
- [x] Run nonpaid lint, factsChecks, focused core tests and check:tasks.
- [x] Review the independent diagnosis of core/drama.test.mjs.
- [x] Incorporate the non-author conversion review and record remaining PR/CI gates.

## How to verify

- Get-FileHash docs/videos/story-everyday-oxo-c10/script.md,docs/videos/story-everyday-oxo-c10/visual-plan.json,docs/videos/story-everyday-oxo-c10/visual-plan.md -Algorithm SHA256
- node tools/video/cli.mjs lint --slug story-everyday-oxo-c10
- node --test tools/video/core/schema.test.mjs tools/video/core/lint.test.mjs tools/video/core/story.test.mjs tools/video/core/curio.test.mjs tools/video/core/drama.test.mjs tools/video/qa/facts.test.mjs
- npm run check:tasks
- Compare every video.json line to the approved script table and each scene kind/prompt or stats text to the approved visual-plan.json. The conversion receipt records the counts and outcome.

## Notes

Nonpaid canonical files are in docs/videos/story-everyday-oxo-c10. The approved source hashes are script 04A5945DDF219868CDC8E52936447A6D7329544976F6A2DC72A7F3B6841175A1, visual JSON A73BDCCCC62026AEB6F156BD4479E295C7A5C9B5021A0A4E1382CF67F06CD781, visual Markdown C4D5ADBDA74FF30AAB774DB2288F9FA8C9134360B4D1D619964BBCF256C0A1CA. Exact 80/80 parity and factsChecks passed. Lint is 0 errors and nine warnings; paper-only body is 566.93 seconds with 87.52% still time, not actual speech or final screen time. All paid execution, import, upload and publication gates remain closed.

The six-file targeted test command returned 84/85 passes; core/drama.test.mjs exited as a whole child process with code 1 and no stack or individual test output. An independent read-only diagnosis localized the failure to the existing a drama's status fixture, where Windows Node fs.cpSync exits 0xC0000409. The same file's other 30 tests passed when that test was excluded; the failing test reads no C10 files. This is a local environment limit, not a green suite. No unrelated test or code was changed. The independent non-author review at docs/videos/story-everyday-oxo-c10/reviews/independent-canonical-conversion-20261024.md passed: 80/80 narration/visual/claims/verify parity, 71/9 scene types, six say_for bindings and approved source hashes. Local pre-PR checks are complete: hash lock, independent conversion PASS, lint 0 errors, factsChecks PASS, check:tasks exit 0 and staged diff check PASS. Required remote PR CI, exact-head merge and any deploy/import remain outside this local check; task stays in-progress until the PR is handled. The two concept cards c100211 and c100603 remain flagged for later visual acceptance. The user approved a C10 local pilot at US$25 but provider routing, historical charge attribution and actual post-hook narration >=480 seconds remain prerequisites to buying images.

2026-10-24 closeout: PR #1809 passed the four required remote checks at exact head `1ad638efa61eef00ea7080849690627201a85a66` and was squash-merged as `029f357b4c7b3ff373059de8669262caf5cbbc4c`. This closes only the nonpaid canonical conversion; the earlier sentence that PR CI and merge were pending describes the pre-PR checkpoint. `tasks/open/2026-10-23-reconcile-c-series-prior-charges-and.md` retains the attributable budget-route/old-charge HOLD; actual TTS duration, image-time percentage, media QA, import and upload are still later production gates. The pilot cap is not an instruction to spend before those gates.
