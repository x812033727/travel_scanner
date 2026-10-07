---
id: 2026-10-07-continue-imported-language-units-before-requiring
title: Continue imported language units before requiring a merged locale artifact
status: review
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
  `<home>/.codex/scratch/native-unit-tests-20261007/final-targeted.log`.
  Runner SHA is
  `a93f99624227af2d2a6cee23b7e2d5c77c6e6075f43ab2954813b9dff6a1971e`;
  test SHA is
  `744cf2a83371ea89a84586a0e9ac0e29785f926bffd0ebe902c36fbde8f2e7f4`.
  The same exact production worker image independently passed all 35 checks
  plus three caller consumer checks, both actual exits 0, with network disabled,
  source/dependencies read-only and an unpaired empty HOME. Before/after hashes
  prove the production operator/profile runtimes and receipts stayed unchanged.
  `independent-native-unit-tests-20261007/downloaded-evidence/test-proof.json`
  SHA is `c911cb5ec77c9123adffe2f70f105e4dd1873ee347193122972811fc8aa25f95`.
  The new complete Windows tools run actually exited 1: 1,948 passed, 11 failed,
  13 platform skips. Its handoff-note host-path violation was repaired and the
  three hygiene checks passed; Windows FFmpeg/filter-path, path-separator and
  seven speech-journal atomic-rename failures are tracked separately. This is
  not a full-suite green claim.
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
  Japanese. At `04:00:38Z` it automatically stopped held, exit 1; EP04 Japanese
  caption translator unit 2/6 received HTTP 429 and its existing journal records
  one unknown result. No request was repeated. All 158 successful request/result
  records and 43 output artifacts were verified and preserved, with STOPs
  restored and no active producer lock. EP06 remained queued. Fresh deployed
  consumer verification at `04:03:57Z` confirms 13 cumulative R3 reviews all
  bound to the current final and approved base metadata: 26 parts ready (EP01/05
  four locales, EP02/03 English/Japanese, EP04 English). Full selected packages
  remain held for missing locales/dubs. No draft native code was deployed into it.

- The separate R5 production continuation started exactly once at
  `2026-10-07T04:59:21.522Z`, after a zero-request/zero-STOP-change dry-run and
  independent source review. It selects only EP02/03 remaining Korean/Simplified
  Chinese metadata/CC and EP06 all four metadata/CC locales: the exact native
  remaining plan is 88 subscription stages. EP04 and its existing unknown request
  remain excluded. Its 158 prior successful records, 43 previous outputs, all 179
  R3 preservation references and the unused R4 preparation are content-addressed
  and retained; no earlier producer is restarted.
  The new gate waits before the native journal records a dispatch, reading only
  the existing paired-tool counters and their natural expiry. Fourteen independent
  offline tests passed through the actual native journal, including waiting,
  known-result reuse, unknown-result/STOP/source/settings holds and unchanged
  request bytes. This does not claim a live-provider or full-suite test.
  Plan SHA is
  `25ddbe4050bb14571525dfb4977345abbca19e1e5463e29f42d96cec4fae7ed6`;
  independent review SHA is
  `e193575b4dd47b52dff61d65c309aada78d6362dbff7f8351e0b7c665981a3c5`.
  At `05:17Z`, EP02/03's profile is running with six actual successful stage
  responses and its next stage pending; EP06 is queued. This is unit progress,
  not additional completed locales or approved language packages. The last
  independently verified series count remains 26 metadata/CC parts, with all
  18 chosen series dubs held. All 18 canonical STOPs and the eight publish
  exclusions remain in place. A separately pinned, read-only verifier is armed
  once for producer exit; it creates new completion/held evidence and never
  submits model requests or clears holds. Read the R5 launch/state/wire receipts
  under `<home>/mokaair-work/handoff/renewed-finals-20261007` and their host
  counterparts; do not relaunch or infer completion from the background process.

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
  `<home>/mokaair-work/handoff/renewed-finals-20261007/translation-r3-independent-checkpoint-20261007.json`,
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
  `<home>/mokaair-work/handoff/renewed-finals-20261007`.
- Preserve frozen production runtime and native source receipts. Any temporary
  external operator adapter is separate from completing this native-tool ticket.
- The isolated `validateResumeSheet` call also receives native `unitVideo`, which
  retains every line in a selected scene. `mergeSheet` then requires lines outside
  the caption unit. Fix validation of the exact requested unit while retaining
  full source/completeness validation of the final merged locale; do not narrow
  or relabel the request to hide a missing answer.

- Final production readback at `2026-10-07T10:27:06.064Z` verified all 18 renewed
  canonical finals and STOPs, 10 current approved base publish reviews and the
  eight fact-check publish holds. Production remains `202430417`; PR #1359 is
  still draft and was not merged or deployed by this continuation.
- The six-series cohort now has 42/48 metadata/CC parts verified against native
  output, the API and the actual deployed full review-store consumer. The four
  retained videos independently passed a fresh 32/32 consumer readback at
  `2026-10-07T10:25:05Z`: together, the allowed ten have 74/80 free parts, or
  37/40 locale pairs. EP04 Japanese, Korean and Simplified Chinese remain held
  behind its unchanged original unknown response; all 41 original files remain
  exact. The 30 chosen paid dub parts remain held, so complete selected-language
  upload packages remain blocked. No YouTube upload, publication or paid-media
  regeneration occurred, and no owner language choices or shared settings changed.
- Once R7 completed with exactly five successful new subscription text stages,
  241 previous successful results preserved and zero repeated old subscription
  stage requests.
  Its three actual recovery events bind the original malformed response, the
  independently reviewed recovered unit and the complete native locale merge.
  Only a derived cached view gained the single missing structural brace; the
  original raw response and journal remain unchanged. The closed R6 attempt
  remains preserved at zero new model POSTs. The R7 pre-apply budget-order
  amendment archived the three original operator sources, plan and dry-run
  evidence; the original dry-run and old producers were never rearmed.
- Outside-Git receipts under
  `<home>/mokaair-work/handoff/renewed-finals-20261007`:
  `translation-r7-independent-completion-proof-20261007T102706064Z.json`, SHA
  `408f20750a308bb5361bcdc840ff1fc0e4436896bb62fb4bc55f91eefb596dda`;
  `retained-four-fresh-independent-consumer-20261007T102505Z.json`, SHA
  `9b789574a9770dbdb5248053a9e020ae624b8eb229246018246b993b82fe7487`;
  `current-production-checkpoint-20261007T102923Z.json`, SHA
  `94c8eb4174c2698e1fb6014847ec5bd9404bc3295c76cd306b792670ad0ef5bb`.
  The 20 green PR checks previously observed bind head `022ee882`, not any later
  documentation commit; this native repair task remains in review.

## Production continuation, 2026-10-07 13:42Z

- The owner's literal `沒有時效性` released the first eight publish exclusions.
  Actual production readback at `12:19:28.029Z` verified all 18 canonical approved
  finals and all 18 new approved base publish reviews, with canonical STOPs and
  inactive uploads preserved. A separate deployment changed production to
  `7524c25995d59f3826227e693d52f2ef5b3a19a2`; this session did not deploy it.
  Frozen operator sources remain pinned, with actual installed API compatibility
  checked against the original production contract. PR #1359 remains a draft.
- Five retained metadata/CC packages were submitted once and independently
  accepted by the actual deployed stored consumer: `ai-real-jobs-chart`,
  `google-vids-free-ai-video-omni-1-1`, `openai-agents-broke-in`,
  `siri-ai-ios-27-how-to-get-it` and `why-openai-killed-sora`. All 40 free parts
  passed. The 13:12Z completion proof binds the five actual current approved
  language reviews, stored file bytes, sources and the completed apply state.
  Together with the earlier 74 parts, 114/144 free metadata/CC parts have been
  verified; this combines separately dated snapshots rather than a new full
  114-part live readback.
- The new three-source producer stopped at `13:15:29.128Z`. Price war's first
  English metadata translator POST returned HTTP 502 after the account agent
  reported every Claude account with room busy. Its journal retains one unknown;
  provider attempt count is one, with zero PUT/language POST/media/YouTube calls.
  The original state, intent, wire, result, journal and both isolated STOPs remain
  unchanged. Free versus paid plans and DevDay are queued with zero attempts;
  a fresh 13:42Z witness confirms all six attempt/result artifacts absent for each,
  and their original manifests, namespaces and source proofs unchanged.
- Actual installed service/API/schema source pins and read-only database evidence
  were checked. These translators use synchronous `/run`; the settings value
  `durable_stage_runs=true` does not send them through `/run/jobs`. There is no
  saved exact answer or account allocation trace for this failed request. The
  agent may try another account after a quota refusal, so the final busy error,
  zero tokens, absent durable jobs or absent temporary directory do not establish
  no CLI execution. Preserve the unknown; do not resubmit or invent a succeeded
  native entry. The native runner has no formal verified-nondispatch reconciliation
  protocol. A future repair must preserve original accounting and request bytes.
- A new conservative read-only scheduling hint passed 11 focused tests and an
  independent review. It reads process ancestry and existing usage snapshots,
  starts no CLI or account/usage endpoint request, and is intended only for
  waiting before a new native journal intent. It is not an account reservation or
  evidence about an earlier request. At `13:39:24Z` it correctly held while two
  Claude descendants were live. After intent, capacity loss still requires an
  unknown hold rather than waiting or resending. The two untriggered scopes may
  continue independently; the failed price-war producer may not be rearmed.
- EP04's original unknown and its 41 retained files remain held. Six of its free
  parts are outstanding; this is one unresolved request, not six unknown calls.
  All 54 selected dub parts remain held. Twelve old paid tracks were independently
  verified in the actual store, but have no current source-bound QA/fit/cache
  proof, so they are not current-ready. No paid media was regenerated and no
  YouTube upload/publication occurred. Complete selected-language upload packages
  and the wider production handoff ticket remain unfinished.

Additional immutable receipts under
`<home>/mokaair-work/handoff/renewed-finals-20261007`:

- `owner-release-eighteen-readback-proof.json`, SHA
  `e88e7ed69e6a2e49ffa888ff061f1444796c39b33f5dc541abccc156f83d7262`.
- `retained-five-v2-actual-completion-independent-proof-20261007T131212243473Z.json`,
  SHA `e9c1439a11d7456fe9ebbd9063fe99891c7b746df491f5511999c77f31ed225a`.
- `released-three-free-language-v3-apply-state.json`, SHA
  `ae37181d1564f05b0dd9f52368567fff529438d8341d9f874af79829f5c079a6`.
- `released-three-durable-result-and-cached-room-independent-source-audit-20261007T134222375101Z.json`,
  SHA `7a851ec09a1cf26bde6d20042a1e979dfb676db07faad6d616ced24d0adcef7f`.
- `released-two-untriggered-continuation-witness-readonly.json`, SHA
  `eef406164c7a315713db74fa63e29e1809fcb043898c25dcf36300065271d793`.

### Untriggered two-source background restoration, 14:03Z

The new outer two-source wrapper passed 17 focused extracted-hook tests, two
syntax checks and independent byte-exact inverse review. It reuses the original
prepared manifests, native runtime, 48/64-call plans and request namespaces.
Both actual production dry-runs completed with exit 0, three source/settings GETs
each and zero provider/PUT/language POSTs. Actual dry state SHA is
`f85376390c482433949894271da1e73c7cfc024d985932568b0d2b5593602810`;
the separate final once review is `released-two-source-review-v4.json`, SHA
`4b89f114cf1f14c79e0c85be9c363591d5d0d8706743d9b4a036c1ef5bc643cb`.

The two-source producer was launched once, background PID `239396`. Actual
readback at `2026-10-07T14:03:14.341209Z` confirms it alive: free versus paid plans
has a durable cached-room wait before the native journal, and DevDay is serially
queued. Both native journals remain absent, with zero new model POST intents and
zero language submissions. The original price-war six files and closed v3 state
remain exact. This is a restored waiting producer, not completed translations or
an account reservation. No canonical STOP changes, paid media regeneration or
YouTube calls occurred. Read actual per-profile `released-two-v4-wire.jsonl` and
native journals for subsequent progress; the running driver's aggregate attempt
count is only refreshed when a profile ends.

Local snapshot: `released-two-v4-startup-readonly-20261007T1402Z.out`, SHA
`da0bb0ecca8d47f16669057fa04bbcdd7968e7ec4da1d2c10d22aa5c88bdee3e`.
The filename is a label; its actual observation time is 14:03:14Z. The 114 verified
free parts remain unchanged at this checkpoint. Keep original unknowns and paid
dub holds; never rerun a prior launcher or clear its intent/journal to resume.

### Known-result handoff, 2026-10-07 23:42 Asia/Taipei (15:42Z)

Four actual free-versus-paid-plan calls succeeded between 14:29Z and 14:33Z.
Independent readback matched every native request, original source unit, answer,
HTTP 200 and database run to the existing Claude Sonnet 5.5 configuration. The
native kept cache contains reviewed English metadata and the first 24 of 116
caption lines. These are two retained units, not a completed locale or language
package; the dated 114/144 aggregate has not increased.

The all-descendant scheduling hint also blocked available account D while
account A was busy. A new, separately pinned read-only hint maps only the fixed
`CLAUDE_CONFIG_DIR` slot value through a bounded byte stream. It compares the
pinned service and complete descendant graph; unknown ancestry, environment
mapping, PID reuse or read failure still holds all dispatch. It starts no account
CLI, reads no credential contents, makes no provider request and reserves no
account. Its 38 focused tests and independent review passed.

The owned v4 producer parked through its isolated parent STOP at
15:27:08.397Z, 0.310 seconds after its latest pre-journal wait, without a fifth
request, process kill or canonical change. Its real closed state is held with
four attempts; DevDay remains unattempted. The actual park witness preserves 57
immutable files, the four original native records, worksheets, unit caches,
source budgets and both original request namespaces. Price war's six original
files and closed v3 state remain exact. A failed initial read-only park precheck
created no intent or STOP; the later fresh conditional park is separately proved.

The new v5 envelope passed 15 focused tests, including actual D35 cache replay of
all four original answers with zero upstream calls and unchanged journal bytes.
Its driver/worker inverse reproduces all original v4 bytes. The unchanged native
runtime resumes at source index four, with at most 44 new calls for plans and 64
for DevDay. It preserves accounting and unknown holds; it neither starts a clean
namespace nor refunds or resets a worksheet budget.

Both actual v5 production dry-runs finished with exit 0, three source/settings
GETs each and zero model POSTs, attachment PUTs or language POSTs. The original four-record
journal and all archived evidence remain exact. This checks the concrete guarded
continuation, not completion of the remaining translations or selected dubs.

New immutable receipts under the same outside-Git handoff directory:

- `released-two-v4-four-stage-independent-progress-20261007T150655Z.json`, SHA
  `831974041c7f2ca2f126c87ff97bd66aa7e37f12ac7595a066d3ba208f481763`.
- `released-two-v4-park-witness-v5.json`, SHA
  `8d6311580796ea6c7f5a882cb5db9df21b202940b836cddd64940224b78f708a`.
- `released-two-v5-local-source-proof.json`, SHA
  `675c678e9a196e1522008d2242b9227b9153d9eaa999612b40d6b68212dd49e6`.
- `released-two-v5-resume-binding.json`, SHA
  `0cdaa6ea50cbacce40a02fa9762bf8ae1bf2fc7a0c079a08dd8fef61943399b8`.
- `released-two-free-language-v5-dry-run-state.json`, SHA
  `a6252170339a2a312ed82ced5300e7418f986ff98bc5888db00e9347825ff7d4`.

The wider handoff stays open. EP04 and price-war unknowns, all 54 selected dubs,
and the owner's no-upload/no-publication/no-paid-regeneration boundary remain.

### Nine-answer checkpoint after production advance, 2026-10-08 (Asia/Taipei)

The actual v5 apply launched once as PID `483509` after its separately bound
source/dry review. Five new subscription requests returned HTTP 200. Independent
native parsing and source-budget validation match all nine stored answers,
including the original four full records and unchanged identity, configuration,
choices and namespaces. English metadata and 72/116 caption lines are reviewed;
another 24 lines are translated only, with 20 lines not yet translated. The next
absent request is source index nine, the fifth unit's caption reviewer. No whole
locale, attachment PUT or language POST completed; the dated 114/144 free-part
aggregate has not increased.

The producer self-held at 2026-10-07 23:55:47 Asia/Taipei with a generic fresh
source/jobs/upload authority error. Actual readback at 23:58:46 confirms it dead,
exit 1, with nine succeeded native entries and no unresolved new request. DevDay
remains queued with no journal or request. The earlier running checkpoints are
historical snapshots, not the current process state.

Production HEAD advanced from `7524c25995d59f3826227e693d52f2ef5b3a19a2` to
`af596412c8f433b184c1e544d432f44145f666a8` at 23:55:29. The original v5 guard
rejects that current HEAD before executing its DB probe. Its saved generic error
alone cannot identify the historical failing assertion. Fresh individual DB
probes now confirm both sources' human final approvals, inactive uploads and no
active source jobs. All eighteen canonical STOP/source/handoff pins, all 57
archived v4 files and the original price-war evidence remain exact.

The incremental production difference contains exactly one news policy, its test,
a news review document and two task notes. Independent Git and actual checkout
comparison found no changed video contracts, BFF routes, dependencies or native
language runner. The API readiness endpoint confirms database/Redis readiness.
The API/web containers have no Docker healthcheck or revision label; the receipt
records those null values without fabricating container-health evidence. This
compatibility receipt binds a new guarded continuation; it does not rearm v5 or
authorize a clean namespace, budget reset or retry of either original unknown.

Additional immutable outside-Git receipts:

- `released-two-source-review-v5.json`, SHA
  `a4bfc9e46a959d1bccb21aeb99e440c6ba0a4b872f4d3962c58dcdf363d32c80`.
- `released-two-v5-first-resume-independent-progress-20261007T155651Z.json`, SHA
  `2b076eb94ff050b675de506ab890dc0b9f6b30c150ef1e091d63f45259f5aad5`.
- `released-two-v5-final-held-independent-progress-20261007T1605Z.json`, SHA
  `c198c19124a6f4a49dcc8d4d42ec7a59746e3b2c41afcdae57f2d6b9f557938e`.
- `released-two-v6-production-extension-readonly.json`, SHA
  `a6f2da2dd809593c67e8c9d19f7aad4cd40dcaf183a55d1ed39434a36aa55372`.
- `released-two-v6-production-extension-independent-review-20261007T161100315200Z.json`, SHA
  `4bad3be68b2dd9b7108d8955c9f8cb5c26b97d39ab3caf0d1b16f60952b10aaf`.

Neither base publish approval nor successful partial text answers make a complete
selected-language upload package. The broader ticket and original unknown/paid
dub holds remain open; no upload, publication, paid regeneration or deploy by
this operator occurred.

The new v6 read-only dry launch stopped before creating a driver state, native
worker or model request: its historical runtime image `2727fc02...` no longer
exists. PID `581544` exited 1; the actual log identifies Docker image inspection
inside `envelopeGuard`. All nine native answers and all 140 closed v5 witness
files remain exact. The absent state's attempt counter stays absent; zero new
dispatch is established by the pre-worker failure and absent v6 worker/wire.
The v6 once-launch intent, source, binding, reviews, log, PID and exit are retained.

A separate offline execution of the current installed video-worker image
`e4dd2511...` verified the same `/usr/bin/node`, Node 24.20.0, Linux amd64 and
FFmpeg 6.1.1. It used `--pull=never`, no network, no mounts and a read-only
filesystem; its disposable diagnostic container is explicitly counted. No image
pull/build, paid media generation, provider call or production deploy occurred.
The current-image proof is `released-two-v7-current-runtime-image-readonly.json`,
SHA `f63bfbcf9b0a35e8c98120c4b25952c97c31e50dba8eaaa1a3411ae72cbaa75e`.
The actual pre-worker failure proof is
`released-two-v6-preworker-image-failure-witness-readonly.json`, SHA
`17070ffb8c7e6053ac5b17ad42098ec064e74bba013e63ad024fe730c41f929f`.
These concrete receipts support a new envelope; they do not authorize changing
or retrying the attempted v6 envelope or either original uncertain request.

### Existing-image continuation, 2026-10-08 (Asia/Taipei)

The new v7 envelope binds the actual installed image and failed pre-worker v6
witness while preserving the original core, prepared native runtime, request
namespaces, budgets and nine successful answers. Ten focused v7 tests passed
independently; the original v6 fifteen-test proof remains a separate receipt.
Both real production v7 dry-runs completed with exit 0 at 00:47:58, three
source/settings GETs each, zero model POSTs, attachment PUTs or language POSTs.
The 00:48:25 readback confirms PID `645574` exited 0, all nine native records
remain succeeded, all 140 closed v5 evidence files and sixteen failed-v6 files
are exact, and DevDay remains unattempted. The next required native request is
the reviewer for the next 24 already-translated English caption lines. This is
native unit five (unit one is metadata), or caption batch four; no translator is
repeated.

A separate repeatable-read, read-only DB snapshot at 00:46:32 confirms all
eighteen current final and replacement base-publish reviews remain approved,
with matching IDs/hashes and no upload state. It does not claim to have rehashed
every media attachment again; the earlier complete source/store proof is retained.

- `released-two-v7-resume-binding.json`, SHA
  `21a46a95480dfa3185c2f4b13dff8ebfeecb9edafe2b8faa316ebc61dc6f3b4a`.
- `released-two-free-language-v7-dry-run-state.json`, SHA
  `0957f0099e02af4f36f083a08ac193ec2cacda28eb6ba36221104dcc5ce6c4a3`.
- `released-two-v7-second-dry-readonly.json`, SHA
  `1eab5dc0ff72efed9cf89a880f2dec4d92e7cbfced7bdafb6ac510930773b688`.
- `renewed-finals-eighteen-current-db-readonly-20261008.json`, SHA
  `115fc408e31bdfc4ecd18dcc5af52611898cd1de29f91146e7486dc38850da76`.

These are immutable actual dry-run and DB receipts, not an apply or language
completion claim. The 114/144 free-part aggregate is still a dated cohort total;
price-war/EP04 unknowns and all 54 selected dub parts remain held.

Independent actual-dry/source review `released-two-source-review-v7.json`, SHA
`207be140ad20e4938502d715d8f9dc56b41816d9db73311c0235548ba439b6de`,
approved one new metadata/CC apply. The separately late-bound launcher, SHA
`0a52907048ed2f85f732ede51362d635679363298fd81a1deaf7a3e16086de92`,
passed Bash syntax, both Python AST checks and root's independent bytes/AST audit.
The original placeholder draft is retained. All launch-time source, existing-image,
checkpoint, immutable evidence, canonical and old-process checks passed before
its exclusive/fsynced once intent at 01:03:16. The producer launched once as PID
`686752`; no prior envelope was rearmed.

The 01:03:50 and 01:05:24 actual readbacks confirm the producer alive, plans
running and DevDay queued. A consistent read-only evidence capture at 01:07:27
preserves the unchanged nine-entry journal and English unit cache; its wire has
three waits before creating any new native request and zero new stage/language
POSTs. The conservative cached-room hint found slot a busy and no idle fresh
eligible slot. It does not observe hidden allocation/model-family rest, reserve
an account or reconcile an old unknown. The native source cursor and all review,
rate and settings guards remain active while waiting. Full free-part completion
has not increased; paid dubs, both original unknowns and upload/publication remain
held. These are dated startup observations, not a guarantee of later liveness.

- Local copy `released-two-v7-actual-apply-launch-once.intent.json`, SHA
  `3dc1d4bdab5f53c0075912dd8a47f44e875a9e90be262d1fa1f4d62632b44526`.
- `released-two-v7-first-apply-readonly-20261008.json`, SHA
  `ca8726b62904c6040015de99f4bab7f4eae26a7da4e46fad4547e38c8de81be3`.
- `released-two-v7-actual-startup-evidence-bundle-20261008.json`, SHA
  `7c3ebc4c54d09aec951821562543588ea00d82102c1985f737523300f4debc6e`.

Independent startup/wait acceptance confirms the actual nine answers through D35
parsing, source-budget and kept-cache validation, with zero readiness increase.
Its remote 140+16 file checks are explicitly the root readback attestations,
not an invented independent remote rehash. The native first-new audit candidate
is retained for a real future request; it was not used to fabricate progress.
The 01:11:34 root readback still finds PID `686752` alive, plans waiting before
dispatch, DevDay queued, six recorded waits and zero new stage or language POSTs.

- `released-two-v7-startup-wait-independent-acceptance-20261008.json`, SHA
  `202cb69a14873b010649cdba927d5cb7ba887d6a2876fb002c21ceff4101c35c`.
- `released-two-v7-third-apply-readonly-20261008.json`, SHA
  `97f669a2b1a8d57b3096c1ee1595b13fa48cb893b2a803607dcaa680c3d11e3b`.

The corrected human handoff is
`renewed-finals-status-20261008T0111-Taipei.md` outside Git. It distinguishes
translation/review POSTs from continuing read-only checks, and describes native
unit five as the next 24 caption lines rather than a fifth caption batch.
