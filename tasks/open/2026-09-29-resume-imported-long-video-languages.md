---
id: 2026-09-29-resume-imported-long-video-languages
title: Resume selected languages for six imported long videos
status: in-progress
priority: P1
area: tools
owner: codex-video-stall-followthrough
claimed_at: 2026-10-04T10:51:05Z
created_at: 2026-09-29T11:13:51Z
completed_at:
branch: codex/video-approved-final-languages-20261004
depends_on: []
scope:
  - docs/videos/imported-long-languages
---

# Resume selected languages for six imported long videos

## Why

Six approved `ai-real-world-*` long videos were imported through `video import`,
which sends a final review but creates no automation project or narration timeline.
The owner selected en/ja/ko metadata, captions and dubs plus zh-CN metadata/captions,
then explicitly asked this chat to continue after PR #964 was merged and deployed.
The standard worker cannot adopt these external cuts automatically.

## Definition of done

- [ ] The active six-project batch's final hashes match the currently approved
  backend reviews (the 2026-09-29 batch is retained historical evidence).
- [ ] Current source timing is faithfully adapted with provenance that separates
  the original Hanhan narration from the Gemini target dub voice.
- [ ] An isolated, resumable runner makes only the six projects' selected languages,
  preserving the approved cuts and the owner's language and publication choices.
- [ ] Completed metadata/captions and checked dub tracks are submitted cumulatively;
  failures retain actual reasons and partial progress survives a restart.
- [x] Record real backend review state and remaining work without claiming human
  audio acceptance, Studio upload or publication.

## Steps

- [x] Read the video workflow and inspect competing work; keep Shorts out of scope.
- [x] Read-only preflight verifies all six exact approved hashes and language choices.
- [x] Build and independently check the adapter, runner and focused regression tests.
- [ ] Start the current approved-source language work and verify persisted
  progress in the backend; the previous producer has stopped.
- [x] Record the final receipt or the concrete continuation state.

## How to verify

Run the adapter and runner's Node tests, a read-only dry run against the paired
site, and compare the source/final hashes before and after. Verify each cumulative
review's locale payload and attached file hashes by reading the persisted project.
The job must not call the general auto loop, assemble, tidy or youtube-sync.

## Notes

- PR #1208's initial head 737d484 was merged at 2026-10-04T12:01:08Z after all
  CI checks passed. It has not been deployed or started a new language producer.
  Further actual-source corrections are on the approved-final-languages branch.
  Full web checks passed (351 files / 3,950 tests), API
  provider/job checks passed (85 tests plus Ruff/mypy). Full tools identified a
  transient Windows rollback rename obstruction; bounded retry preserves the
  original recovery-required failure state when it cannot restore the directory.
- Actual 18-current-final audit prepared all 18 snapshots offline: ten strict
  retained-body/bookend sources and eight separately approved current-body sources.
  All eight current script/body timeline/default-caption mappings passed the
  narrow approved-line-windows
  validator. Current narration attachments are AAC previews, separately hashed;
  they do not establish raw WAV identity or a fresh listening approval.
- A fresh read-only SQL snapshot at 2026-10-04T12:06:33Z matched all 18 exact
  current final IDs/SHA/decided_at to the source inventory. Each has a real
  decided_by_user_id and one same-actor video_review_approved audit bound to
  slug/gate/hash. This is an offline preparation input, not future fresh authority.
- The distinct approved-final-body-range reader/fresh-batch entry is being
  implemented for the six changed sources. It must preserve old translations,
  worksheets, runtime and unknown-paid accounting outside active discovery.
  Actual frozen CLI caption/dub dry-run and production acceptance remain required.

- 2026-10-04 source continuation: eight actual current finals passed complete
  media decode/body-range/bookend/audio-identity proofs and independent source
  readback; legacy preservation claims remain false for these changed sources.
  Native IDs use deterministic aliases while raw IDs/evidence remain intact.
  EP06 alone has an explicit native spelling annotation Anthropic:null, with a
  separate raw empty-lexicon snapshot and unchanged raw/native speech hashes.
  It does not claim pronunciation/listening approval. Exact profiles are
  01+05, 02+03+04, and 06; their union is the original six without duplication.
- Sync model stages now persist exact intent/result before dispatch/return.
  Restart after an unknown translator result makes no additional POST; source,
  namespace, owner choice, model/capability and same-unit request drift all hold
  existing receipts. A shared parent owner lock serializes sibling producers.
  The independent paid-speech journal passed 54 native/unknown/replay/drift tests
  and is wired into each new-source command's fetch. Two real default-CLI runner
  restart tests also pass: a lost speech response sends one POST across two
  invocations; a saved raw WAV replays after consumer failure with no new POST.
  The earlier complete docs suite passed 93 tests with no skips. V5 frozen
  captions/dub dry-run and changed-final refusal passed all six actual sources,
  zero network/paid, in three exact profiles. No new paid producer has started.

- Final 2026-10-04 source validation: the root independently passed the full
  imported-language suite, 115 tests / zero skips, after the actual runner and
  native-client STOP, lost-response, saved-WAV replay and same-invocation owner
  drift regressions. Each new-source translator/reviewer stage freshly verifies
  local evidence, current final/source, owner choices and selected configuration;
  cancelling a language after translation prevents the reviewer POST while
  retaining the first paid answer byte for byte. Stage intent/results now fsync
  their file and POSIX parent directory before dispatch/return. The speech guard
  remains local to this approved-final batch; the shared normal-client follow-up
  is explicitly unclaimed in its own task. Full tools also passed independently.
  Final V6 code-only refreeze retains each previous 334-file runtime and installs
  the actual reviewed code. All six real native captions/dub dry runs and changed
  final rejection passed, zero network/paid calls. All six STOP files remain;
  production activation and persisted new-language progress are still pending.

- 2026-10-04 fresh continuation: all six isolated producers are stopped, latest
  progress remains 2026-09-29T12:16:31.822Z; 279 English cues are preserved.
  All six latest human-approved finals were renewed, so the old final/source
  manifest correctly refuses restart. Previous checks below describe the old
  approval, not current approval equality or a running producer.
- New `prepareRenewedBatch` consumes verified handoff sources, preserves old
  paid outputs and freezes the reviewed portable runtime with STOP. Native
  captions/dub consumers use real retained subtitle timing; an unchecked cached
  dub does not replace narration timing. Independently tested portable captions
  and dub dry-run make zero network calls and reject changed final bytes.
- Author's 95 focused tests and independent 39-test source/runner run passed.
  Real six-source verification, renewed base package submission, deployment and
  restarted production are still pending. Do not retry an old uncertain POST.

- Preflight at 2026-09-29T11:17:06Z: six final hashes match approved reviews, no
  existing language review, Gemini configured and channel voice Sulafat.
- Source imports: `C:/Users/x8120/mokaair-work/videos/season1-import/`.
  Isolated output: `C:/Users/x8120/mokaair-work/imported-long-languages-20260929/`.
- Episode 01 uses the currently approved original cut. The separately merged
  image-trust opening revision is not substituted into that approval.
- Do not fabricate standard-render checks or previous approvals. Pull actual
  hash-bound approval, preserve external-render provenance, submit language files
  through the existing review API, and leave Studio confirmation to the owner.
- PR #981 owns production acceptance of #964; do not duplicate its task or report.
- Adapter/runner: 22 focused tests passed on bundled Node 24.19.0; task check passed.
  All 554 source SRT cues match the source timing within 0.5 ms. Independent review
  covered approval drift, immutable inputs, complete audio checks and cumulative
  submission preservation.
- Production trial found a successful 302,552 ms translator answer lost at the
  295,000 ms BFF timeout. The isolated transport/resume correction passes 29 tests
  and preserves the 94 already translated English lines for fresh independent
  review. The shared-worker follow-up has its own unclaimed task.
- Corrected host job `mokaair-imported-languages-20260929-v2` started at
  `2026-09-29T12:01:31.863243928Z` after a fresh successful six-video dry run.
  See `docs/videos/imported-long-languages/operations-20260929.md` for exact hashes,
  container IDs, interrupted-call evidence and the authoritative continuation path.
- At 12:03:20Z, episode 01 English metadata/captions reached backend `ready`,
  review `8901c581-edf5-4878-ae75-4a72d440c79e`. Both attached file hashes match
  the generated host files and the approved final remains unchanged. Episode 02
  English translation is active. All remaining locales/dubs still need production
  completion; keep this task in progress while its isolated container owns the work.
- Draft PR #986 preserves the tested code and operational record; it is not merged.
