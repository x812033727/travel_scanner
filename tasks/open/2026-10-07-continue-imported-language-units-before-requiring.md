---
id: 2026-10-07-continue-imported-language-units-before-requiring
title: Continue imported language units before requiring a merged locale artifact
status: in-progress
priority: P2
area: tools
owner: codex-renewed-finals-native-units-20261007
claimed_at: 2026-10-07T03:36:12Z
created_at: 2026-10-07T02:05:34Z
completed_at:
branch: codex/renewed-finals-host-handoff-20261007
depends_on: []
scope:
  - docs/videos/imported-long-languages/runner.mjs
  - docs/videos/imported-long-languages/runner.test.mjs
---

# Continue imported language units before requiring a merged locale artifact

## Why

The shared native translation flow retains one reviewed worksheet unit per call
and returns before the locale is fully merged. The imported language runner then
hashes `i18n/<locale>.json` immediately. On the 2026-10-07 approved-final handoff,
EP01 and EP05 each completed a translator and reviewer successfully, but paused
with ENOENT because only their first units were ready. Successful answers must
remain reusable; this is not permission to repeat a model request or reset spend.

The continued actual run exposed a second integration defect after both English
artifacts were successfully merged: `run()` passed the remote API projection to
`submitSnapshot`, whose renewed-source binder requires the verified native project.
The real adapter guard correctly refused before a language review POST.

## Definition of done

- [x] A completed unit is persisted and reported as partial progress until every
      source-bound locale unit is reviewed and actually merged.
- [x] The runner consumes exact retained answers and continues only unanswered
      units; it never hashes a missing locale file or treats a partial unit as a
      complete translation, caption set or language package.
- [x] Existing unknown-result, source/configuration drift, STOP and producer-lock
      guards remain intact; incomplete/rejected model output stays held.
- [x] A caption unit is checked against its exact original lines without claiming
      that other lines in the same scene were requested or reviewed; the final
      merged locale still requires every original selected line.
- [x] Renewed-language submission receives the current verified native project,
      retaining adapter, metadata and presentation-caption hash checks; completed
      translations can be submitted without another provider call.

## Steps

- [x] Review the exact pinned native flow and imported-runner contract, including
      existing PR #1355 work, before selecting the narrow integration change.
- [x] Add multi-unit regressions for restart after one reviewed unit, no repeated
      successful calls, a unit inside a longer scene, actual locale merge, rejected
      output and unknown response.
- [x] Validate captions and emitted language manifests through the real consumer.
- [x] Exercise the actual run-to-submission caller, with completed source-current
      locale artifacts, real native captions/binder and an unknown POST regression.

## How to verify

Use meaningful multi-unit fixtures and request counters. One successful chunk
must not require a merged file; restarting must keep its original result and
request count. Full completion requires the actual merged locale artifact and
source-bound metadata/CC review readback. No paid media or production operations
are authorized by this follow-up.

## Notes

- Current native integration checkpoint, 2026-10-07: the runner now drains the
  exact native unit plan, records partial counts and retained-cache SHA, and only
  records a complete translation after this invocation's real successful merge.
  Every cached translator/reviewer worksheet must match its exact succeeded
  native stage-journal request and result. Unknown results, altered paid answers,
  unknown cache keys and merge failures remain held without another provider
  request. Full merged output retains the original per-line dub budgets; optional
  thumbnail omission keeps native fallback behavior. The provider's original
  scene-sized context and worksheet request are unchanged.
- A complete artifact without a verified completion receipt stays held for
  inspection before another provider request, including merge-then-crash with
  either a filled or absent todo worksheet. Partial validation permits only the
  exact requested caption IDs; mixed whole sheets and final merge still require
  every original selected source line.
- Independent code review found no remaining required changes. Actual Windows
  native integration/regression checks passed 35/35, exit 0, in 67.054 seconds,
  including real native worksheet, unit cache, stage journal, merge, captions and
  renewed-source package binding. Raw log is
  `C:/Users/x8120/.codex/scratch/native-unit-tests-20261007/final-targeted.log`.
  Runner SHA is
  `a93f99624227af2d2a6cee23b7e2d5c77c6e6075f43ab2954813b9dff6a1971e`;
  test SHA is
  `744cf2a83371ea89a84586a0e9ac0e29785f926bffd0ebe902c36fbde8f2e7f4`.
  Exact-worker-image independent checks and a new full-tools run are still
  awaiting actual exits at this checkpoint; they are not claimed as passed.
- Production remains on the separate immutable R3 operator runtime. At
  `2026-10-07T03:37:44Z`, actual deployed consumer/review-store verification passed
  all four metadata/CC locales for EP01 and EP05 (16 parts), with selected dubs
  held. Latest cumulative approved reviews are
  `157b627b-75be-43c6-9582-55c1de1caa85` and
  `4be19081-8f29-400c-ac40-13a334dcd775`. Evidence outside Git is
  `translation-r3-completed-fourlocale-proof-20261007T033746Z.json`, SHA
  `641469989ba2c2b8a033872132e1af6ab5435240704fba846f489b889b730501`.
  Fresh guard checks confirm all 18 canonical STOPs, 10 current approved base
  publish reviews, zero live publish reviews for the eight excluded slugs, and
  unchanged owner choices/paid-media counts. At 03:52Z, EP02/03/04 each had a
  confirmed English submission and the same serial producer was continuing
  Japanese; EP06 remained queued. No draft native code was deployed into it.

- Fresh collision inspection before the narrow 2026-10-07 caller repair found the
  old 2026-09-29 claim at 64 hours. Its checked-out branch had no tracked source
  changes, both runner paths were identical to landed `origin/main`/PR #1210, its
  remote branch was absent and no open PR touched either path. The board-release
  PR #1357 independently records that only production work remains. Only this new
  narrow follow-up was force-claimed; the old owner's record and worktree were not
  modified. Existing PR #1355 flow/lease changes were inspected and not touched.
- The native repair is exactly one argument: pass the freshly loaded `project`
  rather than `remote` to `submitSnapshot`. An actual `run()` regression with
  source-current merged output, native captions and the real renewed-source binder
  passes, and rejects the original caller. A separate integrated four-locale
  fixture confirms all eight metadata/CC parts without provider calls, and a lost
  review POST retains its submitting receipt and forbids another submission.
- In the exact production worker image, with network disabled and no paired home
  mounted, 16 relevant native checks and all three caller integration checks
  passed. Original failed test-envelope logs are preserved; the successful second
  envelope only supplies the required root user for the read-only source mount.
- Actual R2 stopped held at `2026-10-07T02:29:57.967Z`, exit 1. EP01 and EP05 each
  have a complete, independently verified English artifact: 101/103 current source
  lines, 11/11 chapters and 107/118 exact narration-timed cues. All 24 translator
  and reviewer results are successful and preserved; no language POST occurred.
  All canonical/profile/project STOPs were restored, producer locks were absent
  and the other two profiles remained untouched.
- The immutable `known-r2-successes-proof.json` binds every request key, full
  record/result SHA, both merged English artifacts, all three profile manifests
  and all six source contracts. Host/local SHA is
  `dff1bf570edcc515c7f1d37cfc7a870d0935de041fc4ebaf3610bd49807c91ea`.
- An explicit separate `operator-runtime-r3` retains the exact deployed Git archive
  and changes only the reviewed caller argument. Its runner SHA is
  `d35c10786d5d19e46efffe7ca14ddba9f5eab923eb603304f6e05b7739732645`;
  all original native/runtime/source/manifests and prior attempts stay preserved.
  The independent-reviewed R3 wrapper is
  `21c6975a7b28bedd27a417690c016f2345abbe680da5d0a2819452d2ac717d51`,
  and driver is
  `fa36e8aeb71bba03fa5bab5caca9638709bba9f5a530d1f2b4253542ac4debb4`.
- R3 was dispatched once as PID `3221499`, first submitting only existing verified
  English outputs, then continuing the three isolated profiles serially. Read
  `/root/renewed-finals-20261007/translation-resume-r3-state.json`, actual language
  reviews and `retained-English-r3-result.json`; a dispatched PID is not completion.
  The exact 24 successful results are checked before continuation. Language POST
  intent is matched to the full native request and fsynced before dispatch.
  Retained-only failures preserve its own locks; normal native handled failures
  still retain journals/unknown receipts and restore STOP through the held driver.
  No paid media, chosen-dub skip, YouTube upload or publication is authorized.
- Actual R3 started at `2026-10-07T02:43:13.430Z`; all three dry-runs passed before
  the first profile began at `02:43:58.200Z`. Retained English submission made
  zero subscription calls and confirmed two approved reviews: EP01
  `0bd4c1c2-731d-48f1-967e-34bcbd3c192f` and EP05
  `d4e3d1fa-0e56-4d2a-965d-18ebdc3e9c3a`. Other selected metadata/CC locales
  continue through the serial driver; these two reviews are English-only, not
  complete selected-language packages or dub readiness.
- Independent fresh GET and actual deployed database/consumer verification at
  `2026-10-07T02:49:46-50Z` passed for both approved English reviews, their source
  contracts and full actual review-store files: 17 unique files / 134125134 bytes
  for EP01 and 15 / 133419395 for EP05. Description and exact narration-timed SRT
  bytes match the preserved complete English artifacts. All 24 previous full
  request/result records and both merged English hashes are unchanged. Eight new
  Japanese translator/reviewer results were also independently confirmed in the
  native journal and actual database; later units continue serially.
- The read-only verifier made zero provider or YouTube calls. All eight excluded
  slugs still have zero current live publish reviews. The complete selected
  package consumer still holds incomplete locale/dub parts; existing
  English/Japanese/Korean metadata/CC/dub and Simplified Chinese metadata/CC choices
  remain unchanged. The latest separate root driver readback remains running
  with all 18 canonical STOPs retained.
- Immutable local checkpoint:
  `C:/Users/x8120/mokaair-work/handoff/renewed-finals-20261007/translation-r3-independent-checkpoint-20261007.json`,
  SHA `1ce895e9d5082f089807837b86439d9f6eee4dc6537a3dedbe959cfc089bf65f`.
  It binds independent review/consumer evidence SHA
  `e6ea969ae84ea6ab9acb1ae1ecc21e85ae98a28fa409e944be4cbfee121eddb4`,
  preserved-result proof, derived runtime receipt and the two actual worker-image
  test logs/exits (16 native checks plus three integrated checks, all passed).
- The Windows full tools and native-runner attempts lost their execution sessions
  before final summaries or exits and are not reported as completed suites. The
  retained tools log also exposes an independently reproduced existing no-cut
  FFmpeg range failure, filed separately as
  `2026-10-07-handle-a-no-cut-range-in`. The native full-attempt log contains an
  unknown-speech regression failure that requires its own isolated diagnostic;
  this does not override the 19 passed source/current-submission guards above.
- Release the repository claim at this checkpoint; only the caller repair is
  implemented here. Native unit draining and exact-unit validation remain open.
  The host R3 producer retains its own locks/journals and continues independently;
  repository release is not permission to reset it, invoke another launcher or
  retry an unresolved result. Use R3 state and actual review readback rather than
  the preserved historical R1/R2 checkpoint when continuing this production run.

- First host attempt is preserved at
  `/root/renewed-finals-20261007/translation-resume-state.json` and profile logs;
  it exited held at `2026-10-07T02:04:22.951Z` with all isolated STOPs restored.
- Fresh native journal, HTTP and database readback confirmed exactly four
  successful subscription stages and zero unresolved results for EP01/EP05;
  no language review had been submitted. Operator evidence is outside Git at
  `C:/Users/x8120/mokaair-work/handoff/renewed-finals-20261007`.
- Preserve frozen production runtime and native source receipts. Any temporary
  external operator adapter is separate from completing this native-tool ticket.
- The isolated `validateResumeSheet` call also receives native `unitVideo`, which
  retains every line in a selected scene. `mergeSheet` then requires lines outside
  the caption unit. Fix validation of the exact requested unit while retaining
  full source/completeness validation of the final merged locale; do not narrow
  or relabel the request to hide a missing answer.
