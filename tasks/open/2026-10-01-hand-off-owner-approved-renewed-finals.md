---
id: 2026-10-01-hand-off-owner-approved-renewed-finals
title: Hand off owner-approved renewed finals to canonical and imported upload packages
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-01T09:53:00Z
completed_at:
branch: codex/renewed-finals-host-handoff-20261007
depends_on:
  - 2026-10-01-long-video-renewal-tools-and-ui
scope:
  - tools/video/review/renewal-handoff.mjs
  - tools/video/review/renewal-handoff.test.mjs
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/package/cli.mjs
  - tools/video/package/package.test.mjs
  - tools/video/core/stages.mjs
  - tools/video/dubs/cli.mjs
  - docs/videos/BRANDING.md
---

# Hand off owner-approved renewed finals to canonical and imported upload packages

## Why

The owner can stage a replacement final and create a new human-pending review, but
approval alone does not replace the canonical worker's old final, branding pin,
checks, timeline, captions or upload package. The renewal submission guard deliberately
refuses those old bytes. An explicit source-bound handoff is still required before
automatic production can continue, including manual imported cuts with no normal TTS
or scene timeline. Production operations require direct owner instructions; the
authorized 2026-10-07 scope and limits are recorded below.

## Definition of done

- [x] For the six isolated v1 revisions with a verified canonical body, the owner can
      adopt only the exact newly approved review/hash/branding into a fresh, verified
      work snapshot; canonical originals, approval decisions and body proof are archived.
- [x] The transfer rechecks owner approval and upload inactivity immediately before an
      atomic activation. Failure, stale approval or ambiguous result keeps the old worker
      held and preserves both snapshots; changing an approval id alone is impossible.
- [x] Imported season and legacy candidates have a separate explicit manual-package
      handoff binding original/final/body proofs, translated metadata and every caption
      offset. Missing timeline/TTS/scene evidence is reported rather than fabricated.
- [ ] Newly approved final identity and all applicable source reviews are reflected in
      publish/language manifests, canonical approval artifacts and actual uploaded bytes.
- [ ] Renewed compilations either gain verified episode/body/caption source transfer or
      retain a precise documented hold with their own follow-up; no old merged SRT reuse.
- [x] No paid regeneration occurs unless a separately authorized body change needs it;
      unchanged narration and source caches are retained.

## Steps

- [x] Freshly collision-check and claim the exact files before implementation.
- [x] Define a receipt with old and new final identities, body/pin/check/timeline hashes,
      owner approval identity, archived original paths and activation result/readback.
- [x] Build the normal-workdir transfer from the six v1 candidate proofs without
      overwriting the existing workdir during preparation or rewriting checks to pass.
- [x] Define the separate imported manual-package contract; fail closed when the
      available source evidence cannot prove chapter/subtitle offsets and retained body.
- [ ] Add stale approval, concurrent worker, interrupted activation and old-language
      regressions; exercise actual emitted bytes through the API package consumer.
- [x] Document owner initiation, stage/approve/adopt/package separation and recovery.

## How to verify

Run focused Node tests for renewal/handoff/sync/package, the real Python YouTube package
consumer against emitted fixtures, tools checks and task validation. Compare retained
original media hashes and every caption's first/last cue against the new presentation
timeline. A successful HTTP response is not approval, canonical activation or upload.

## Notes

- Read-only implementation audit on 2026-10-04: live final reviews for the 18
  affected slides are approved renewal candidates, while publish approval is false
  and chosen languages still await the canonical source-bound handoff. This is not
  a request for another owner final approval or an upload authorization.
- The initial read-only audit found the old
  `<home>/mokaair-work/channel-intro-20260930` candidate evidence directory absent.
  Subsequent exact-hash recovery and real media verification prepared all 18 local
  snapshots as documented below; the absent directory is historical evidence,
  not a current count of unverified candidates. No paid media was regenerated.
- DevDay retains canonical source files under
  `<home>/mokaair-work/videos/openai-devday-2026-recap` and the candidate
  under `branding-audit-20261004`: 153 audio segments, timeline/narration hashes,
  source checks and preservation proof. Its old local pending receipt is a stale
  snapshot; use the fresh approved backend identity. Preserve the original
  publish thumbnail, not an arbitrary newer final-review thumbnail.
- The initial implementation audit called for a prepare/verify snapshot receipt, guarded
  activation with worker STOP/idle and fresh upload/owner activity checks, and the
  separate imported manual-package consumer. Existing source-hash guards remain
  intact. The 2026-10-04 recovery branch fixes writer, image completeness and
  status-report code; it does not activate these renewal candidates.

- Filed unclaimed; the predecessor implements a concrete staged-candidate and manual
  pending-review entry point only. No live deployment, import, upload or publication.
- Six v1 candidates have canonical retained body copies/hashes and original
  checks/timeline/video.json available outside the repository. Six season imports have
  final/meta/zh-TW SRT/thumbnail plus normalization/source/body proof but lack a normal
  pipeline timeline. Five legacy candidates originate from approved publish attachments
  and contain translated captions/metadata; do not invent source scene/TTS evidence.
- Candidate media remains outside Git. Read the latest rollout receipts and owner review
  state at execution time; an earlier pending review may already have been decided.
- The existing guard intentionally rejects renewed compilation producer output and any
  normal worker still holding old final/branding/caption bytes. Keep that protection
  until this source-bound transfer exists. Never delete an old approval or use force.

## Authorized production continuation, 2026-10-07

- The owner's current instruction explicitly authorizes guarded activation, new
  publish reviews and selected-language continuation on deployed PR #1210. It
  explicitly forbids YouTube upload/publication and paid media regeneration. The
  first eight videos remain excluded from publish while Claude checks current
  figures: DevDay, price war, Sora, Google Vids, Siri, agents broke in, jobs chart
  and the free/paid plans comparison. Prior broader media permissions do not
  override this instruction.
- Deployed Git was freshly pinned to
  `2024304170c6b43ecb4259e6b4fb0ce8a60d9893`. All 18 actual current human-approved
  review identities, decision audit rows, final-store hashes and upload/job
  inactivity were reread before guarded operations. An owned global STOP drained
  the worker; preexisting provider work was allowed to finish and not retried.
- All 18 source-bound snapshots were freshly prepared, verified and canonically
  activated with exact native final approval pull/readback, worker UID 1001
  restored and individual STOP retained. The actual aggregate
  activation audit passed at `2026-10-07T01:23:28.492Z`; no paid media or YouTube
  operation occurred. Operator artifacts are outside Git at
  `<home>/mokaair-work/handoff/renewed-finals-20261007` and on the host at
  `/root/renewed-finals-20261007`.
- Fresh receipt inventory confirms all 18 previous host canonical inventories
  were empty. Activation reserved archive paths but created no old-directory
  archives; actual archive existence is zero. Original local snapshots, approved
  review-store media, source bundles, failed preparations and receipts remain
  preserved. A reserved archive path is not evidence of an existing archive.
- DevDay's earlier retained-caption mapping failed closed before activation.
  A fresh sibling preparation used the deployed `approved-line-windows` adapter:
  153 real source lines and 161 actual approved cues passed exact text/number/time
  checks. Only the explicit adapter mapping changed; media, approved SRT and
  timing bytes were unchanged. The failed snapshot and proof were preserved.
- Six current-source videos were prepared in three isolated profiles with their
  exact separate lexicons using `prepareApprovedFinalBatch`, without any model
  request. Original
  358 artifacts, 279 old English translations, ledgers and uncertain request
  accounting remain archived and charged. Existing English/Japanese/Korean dub
  choices and Simplified Chinese metadata/CC choices were not broadened or skipped.
- The worker's writable docs volume contained an old executable language runner,
  although deployed Git had the required export. The failed import created no
  language workspace, lock or request. The original frozen runtime was preserved;
  a separate exact deployed-Git `runtime-v2` with pinned dependencies prepared the
  profiles successfully. Follow-up:
  `2026-10-07-keep-executable-language-runtime-current`.
- All ten allowed new base publish reviews are confirmed approved, with complete
  review-store file hashes and the actual deployed Python package consumer
  checked. All 18 current human-final/canonical/source identities passed the
  aggregate readback at `2026-10-07T02:00:20.638Z`; the excluded eight still have
  no current pending or approved publish review. Base approval is separate from
  a complete selected-language package or upload readiness.
- EP01 and EP02 originally failed before review POST because their approved PNG
  thumbnails exceed 2 MiB. Their explicit codec projections are now approved:
  EP01 `574e74fd-7086-44b2-81b5-e19c40974b84`, EP02
  `afa7d310-e34b-4b97-a367-92eaad66b854`. EP01 uses an explicitly lossy JPEG with
  unchanged geometry/composition (PSNR 50.3422 dB, SSIM 0.995318); EP02 uses
  a PNG with exactly identical decoded pixels (SSIM 1). Full original evidence,
  canonical metadata and native receipts are unchanged. Each received one POST,
  and independent actual-store verification passed. This is encoding evidence,
  not new human artwork approval or paid generation. Native encoding/MIME support
  remains in `2026-10-07-support-proven-thumbnail-encoding-in-renewal`.
- Four retained legacy language reviews are confirmed approved for all selected
  metadata and CC: RTX `c1cdb9b8-8211-45a7-bff8-1e3d110f6eae`, always-on agent
  `04e33e0b-8128-4530-8e79-ba0d2aca18ce`, agent costs
  `61079dd0-b9db-4d42-a4af-9bdeaea41829`, vibe coding
  `61c62386-507a-40c6-b9e1-8d9d4d02f20a`. Actual deployed schema, source checks,
  retained chapter/caption offsets and every review-store file passed. All 32
  metadata/CC parts are ready; 12 chosen dub parts remain working. The actual
  complete-package consumer still refuses missing selected dubs rather than
  treating these four videos as upload-ready.
- Selected-language continuation is limited to metadata and CC on the existing
  subscription providers. All selected dubs remain held; choices are retained,
  and no skip, audio QA, media generation or upload readiness is fabricated.
- The first serial attempt ran four successful subscription stages (EP01/EP05
  English metadata translator and reviewer), then held at
  `2026-10-07T02:04:22.951Z`: native translation returns one reviewed unit before
  the full locale merge, while the imported runner tried to hash the missing
  locale artifact. All four actual results, request journals and accounting are
  preserved; fresh readback confirmed zero unresolved results and all isolated
  STOPs restored. Follow-up:
  `2026-10-07-continue-imported-language-units-before-requiring`.
- A separate external operator adapter now drains only unanswered native units,
  preserves provider payloads and validates caption units against their exact
  original lines. Completion requires this invocation's successful native merge
  plus full current-source metadata/CC checks. Source, STOP, unknown-result,
  settings and producer guards remain active. All 21 tests passed in the exact
  pinned worker image against the actual production `runtime-v2`, with network
  disabled and source mounts read-only. The native runtime, manifests, prior
  attempt logs and canonical receipts remain unchanged.
- The known-result continuation started once at
  `2026-10-07T02:17:53.938Z`, background PID `3176196`. All three startup dry-runs
  passed; the first profile began at `02:18:33.561Z`, with the other two durably
  queued. Its first new caption-unit translator returned successfully without
  repeating the preserved metadata pair. Read
  `/root/renewed-finals-20261007/translation-resume-r2-state.json`, native journals,
  `translation-unit-progress.jsonl` and the actual backend language reviews for
  completion. Driver running or a successful unit is not full locale completion.
  Unknown results stop the serial driver and preserve every request and answer.
- EP03-EP06 still need source-bound image MIME repair before any future upload:
  their approved PNG bytes were declared JPEG by the native filename-based
  transport. The actual Python parser accepts this but does not sniff image
  bytes. This is recorded in the encoding follow-up; no prior review or source
  receipt was mutated to hide it.

Authorized production checkpoint:

- [x] Activate and read back all 18 exact approved canonical finals.
- [x] Submit and read back new approved base publish reviews for the allowed ten.
- [x] Keep all eight fact-check exclusions out of publish.
- [x] Rebind the four retained metadata/CC language packages to their new finals.
- [x] Start guarded serial metadata/CC continuation for the six current-source videos.
- [ ] Finish all six selected metadata/CC sets and read back their actual new language reviews.
- [ ] Apply the eight fact-check results before their future publish submissions.
- [ ] Resolve selected dub holds under separate owner authorization.
- [ ] Repair EP03-EP06 image MIME through a versioned source-bound contract before upload.

The repository claim is released after recording this checkpoint. This does not
release/reset the ongoing host producer locks or journals. Continue only from the
R2 state and actual process/review readback; do not start another launcher or
retry an unresolved unit. The wider ticket remains open for the documented holds.

## Recovery continuation, 2026-10-04

- Prepare/verify/guarded activation and explicit manual imported package/source
  contracts are implemented. Owner identity, content, caption timing, adapter,
  assets and frozen runtime are rechecked; rollback retains both snapshots and
  successful activation retains STOP. Native captions and dub dry-run consume
  the actual source contract instead of requiring fabricated normal TTS/checks.
- 95 focused author tests and an independent 39-test source/runner run passed.
  Independent frozen-runtime CLI evidence: captions offset 5 seconds, real dub
  windows, zero fetches, no fabricated checks/narration, changed final refused.
- Actual DevDay verification passed for all 24,061 retained body video packets,
  complete decode and audio difference about -72.82 dB. Subsequent actual checks
  prepared all 18 base snapshots: ten strict retained-body/cut sources and eight
  separately approved current-body sources. Nine real language adapters exist;
  the other nine lack actual script/body timing evidence for language production.
  These offline proofs are not canonical activation, backend package approval,
  resumed language production or upload.

- Scope extended to the two native caption/dub consumers after fresh collision
  inspection: no active claim owns core/stages; the wedding pilot dubs ticket is
  unclaimed. The imported runner's tests own the real consumer regression.
  Manual renewed media must use verified presentation evidence, never fabricated
  normal-render checks or a paid re-assembly of the approved cut.

- Human requested fixing the live stalled queues and ongoing status tracking. This
  includes resuming source-bound production; it does not authorize fabrication of
  owner reviews or enabling uploads/publication.
- Claim collision was a stale `codex-ten-drama` listener ticket from 2026-09-28.
  Fresh GitHub inspection confirmed its PR #978 merged on 2026-09-29 and its branch
  is not checked out in any active worktree. Only this task was force-claimed; the
  other owner's task was not modified. Keep implementation inside this scope.
- Live 41f2f36 snapshot 2026-10-04T10:21:21Z: 18 renewed finals owner-approved,
  every review-store final has matching bytes/hash, none has a YouTube ID, schedule
  or upload session. Canonical snapshot/package source transfer is still required.
- Three remaining legacy writer requests were confirmed completed subscription
  calls with unavailable old answers and no active durable job for those slugs.
  The official audited one-shot retry service queued requests at 10:23:55Z; already
  resuming Claude mods was skipped. Completion remains to be verified.
- Heartbeat automation `automation-2` tracks this conversation every 15 minutes,
  silent on unchanged state and active until actionable technical recovery is done.
- The owner explicitly allowed individually exceeding already exceeded media caps.
  This applies to six existing videos, including Grok/SEC whose stale blocker showed
  only missing assembly images. Global/per-new-video caps and uploader settings
  remain unchanged. Exact paid caches are recovered before any bounded new purchase.
- Actual preparation now covers all 18 base snapshots; the eight changed-current
  sources have real whole-media/body-range/bookend/AAC proofs and the independent
  current-source contract. Raw historical body/voice differences and false listening
  claims remain visible. Nine actual language adapters exist; nine retained-body
  packages still lack source script/timing adapters for new language production.
  All snapshots remain stopped and local; fresh production canonical/owner/idle/
  upload probes and guarded activation are not yet performed. The six-language
  producer follows its separate claimed task and preserves all 358 historical
  artifacts, 279 English translations and unknown-paid/budget accounting.

- Final local validation: full tools passed independently with the final handoff
  source/test hashes; the imported-language suite passed 115 tests with zero
  skips. Windows rollback retries are bounded and require the original directory
  identity and a truly absent target on every attempt; a permanent obstruction
  retains STOP and both snapshots for recovery. Production canonical activation,
  backend package acceptance and resumed language production remain separate
  unfinished steps, not consequences of these passing local tests.

## 2026-10-07 看板總整理（由站主授權，非原持有者）

釋出過期認領（認領超過 24 小時，主要工作已落地）。程式已在 main（renewal-handoff.mjs、prepareRenewedBatch，#1208）；分支已不在遠端；剩正式站的交接。
