---
id: 2026-10-16-bind-story-audits-and-narration-to
title: Bind story audits and narration to immutable per-story lexicon snapshots
status: in-progress
priority: P2
area: tools
owner: codex-gpt6-a01-lexicon
claimed_at: 2026-10-17T07:21:57Z
created_at: 2026-10-16T07:19:37Z
completed_at:
branch: codex/a01-lexicon-integration-20261017
depends_on: []
scope:
  - tools/video/core/story-lexicon.mjs
  - tools/video/core/story-lexicon.test.mjs
  - tools/video/core/lexicon-store.mjs
  - tools/video/core/lexicon-store.test.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
  - docs/videos/story-lexicon-integration.md
  - tools/video/automation/flow.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/paths.mjs
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/cli.test.mjs
  - tools/video/tts/tts.test.mjs
---

# Bind story audits and narration to immutable per-story lexicon snapshots

## Why

2026-10-17 owner authorization: release the merged #1481/#1508/#1521/#1520 claims and prioritize this integration in an independent branch, preserving #1518. The scoped force claim only coordinates this same conversation's unfinished #1510 budget overlap; no other worktree/branch is modified. Reuse the independently authored #1528 immutable format as an explicit code dependency. Production migration, host writes and paid work remain excluded.

A01's 80-event production story audit tip binds the whole shared
`docs/videos/lexicon.json`. The shared file gained `pull: null` and
`request: null` from an as-yet-unidentified writer, changing its mounted SHA-256 from `ebfa590a…` to
`835e09df…`. A01's narration uses neither term, yet a read-only snapshot
inspector correctly rejected the source as `SOURCE_DRIFT_FROM_TIP`. The
one-time, append-only A01 rebaseline candidate is scoped to those exact bytes;
the next unrelated lexicon edit would repeat the problem. Story audits and
narration need a stable, story-owned pronunciation input with an explicit
revision path when that input truly changes.

## Definition of done

- [ ] An unrelated shared lexicon edit cannot change a held story's source,
      approval, or speech hashes; the stored story input and its byte hash
      remain readable after a worker restart.
- [ ] A deliberate story lexicon revision changes only that story, records the
      old and new hashes in an append-only audit event, and requires fresh
      dependent reviews before paid work resumes.
- [ ] Existing audit chains and unstarted stories remain readable without
      rewriting historical evidence; old and new worker paths are covered by
      compatibility tests.
- [ ] No production migration, live A01 source mutation, paid call, or auto
      continuation occurs as part of this task without a separate release plan
      and owner decision.

## Steps

- [ ] Trace every story source-hash, approval, TTS, and listener read of the
      shared lexicon; specify one canonical per-story snapshot and pinning
      point, including existing rows and held work.
- [ ] Implement read and revision semantics with narrow tests for unrelated
      edits, deliberate revisions, worker restarts, and legacy audit history.
- [ ] Independently review the migration/compatibility plan and update the
      release gate before any production data change.

## How to verify

Run focused Node tests for the files in this scope with the bundled Node 24.19
runtime, then `npm run test:tools`, `npm run check:tasks`, and an isolated
legacy 80-link fixture check. Verify that editing only the shared lexicon
leaves a pinned story's source and speech hashes byte-identical; a deliberate
story revision must produce a new bound event and keep the old 80 links intact.

## Notes

2026-10-18 owner-authorized narrow transfer: release only
`docs/videos/long-form/review.md` and `review.json` to the A01 duration task.
The 80-to-81 production transition and all other scope remain in progress;
reclaim the receipt paths if later lexicon edits require another review.

Evidence: `docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-live-readback-20261016.md`
and the offline `A01-lexicon-rebaseline-candidate/README.md`. The latter is
HOLD and does not solve future shared-file drift. `tools/video/automation/story.mjs`
and `flow.mjs` call `lexiconFile(root)`; `tools/video/tts/check.mjs` and
`cli.mjs` also read the shared dictionary. Coordinate with the active A01
pilot and #1517 owners before claiming overlapping files.

## 2026-10-17 fresh A01 evidence and integration boundary

The [fresh A01 read-only capture](../../docs/videos/brand-stories-pilot-v2-20261015/preproduction-20261016/A01-live-readback-20261017.md) found the worker-mounted shared lexicon at SHA-256 `e6403c82…`: 23 added terms since the 80-link tip `ebfa590a…`, with no old term removed or changed. The prior 81st-event candidate pins the earlier two-term `835e09df…` file and cannot be used for this live state. No current A01 narration line contains one of the 23 newly added terms in a literal boundary scan, but that is not a pronunciation or approval verdict.

Current `story.mjs` and `flow.mjs` mutate the shared lexicon without a common writer lock. A per-video LEASE does not exclude another video's lexicon writer; production has separate `video_docs` and `video_work` volumes. Draft #1528 supplies a strict per-story snapshot format/reader only: it does not connect the writer, worker or TTS and cannot migrate the existing A01 80-link chain. Draft #1518 also edits `story.mjs`, so its owner and the A01/#1510 owner must coordinate before this unclaimed integration task touches those files. Design the common writer admission, durable cross-volume commit/recovery record, legacy-chain transition and genuine worker/TTS binding before requesting any production A01 append or paid work.

## 2026-10-17 draft implementation and verification

Draft PR #1548 contains the shared writer admission, per-story immutable publisher/reader, dual-volume intents and exact committed-only recovery, worker pronunciation proposals, pinned project/listener/TTS/audio/dub inputs, and paid legacy-story HOLD. The original #1518/#1387 branches remain untouched; #1528's exact formatter/reader is included as an explicit dependency.

Independent review found no additional P1/P2 in this draft runtime scope. Commit b31b4ce88 independently binds the three duration-covered files after verifying their 66092d968 baseline hashes. Strict reader/runtime/receipt tests passed 20/20, the two focused consumer regressions passed, long-form check passed all 473 plans, task check passed, and local docs-video suite passed 215/215. Hosted web, video-tests, containers and api checks passed on code-identical head 0d616f39479d61269256ea0fcdee165d62fc6c2e; remaining smoke/Lighthouse were still running when recorded. The duplicate full local tools/consumer runs were intentionally stopped after hosted affected suites passed; they are not recorded as local all-pass. Logs are in the local Codex captures directory under a01-lexicon-final-*.

This task remains in-progress. A01's actual 80-to-81 audit/snapshot transition, new source-inspector compatibility and independent release gate are still required. The 80-link fixture currently proves byte preservation and refusal, not successful production migration. No host, deploy, import, paid call, retry or upload was made.

2026-10-18 narrow claim release (owner-authorized): #1548 merged the
`story.mjs` and `story.test.mjs` pronunciation changes into main at
`4f02734769f683615d1ca8b641026ac8cf1f87b5`, which remains their latest
main commit. Release only those two completed code-file claims so the A01
duration worker can claim them independently. Preserve this ticket's other
scopes and incomplete production transition; reclaim the files if later edits
are needed. Draft #1518 remains untouched.

2026-10-19 owner-authorized narrow claim release: release only
`tools/video/automation/flow.mjs` and
`tools/video/automation/automation.test.mjs` for task
`2026-10-19-host-explainer-route-always-adds-the`. Keep `flow.test.mjs`, the
remaining scope, the A01 80-to-81 transition, and its release gate in progress.
Reclaim these two files later if the lexicon work needs them again.
