---
id: 2026-09-29-video-language-summary-stalls-worker
title: Video language summary overflow stalls the worker queue
status: done
priority: P1
area: tools
owner: codex-video-language-recovery
claimed_at: 2026-09-29T00:52:09Z
created_at: 2026-09-29T00:48:26Z
completed_at: 2026-09-29T00:58:13Z
branch: codex/video-language-review-recovery
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Video language summary overflow stalls the worker queue

## Why

Read-only production diagnosis on 2026-09-29 00:46-00:49 UTC found that
`openai-academy-learning-paths` repeatedly fails language submission with
`summary：內容太長`. Its generated summary is 673 characters; the API accepts at
most 500. Full English/Korean dub failure commands are copied into the summary
(264 characters each); the Japanese skipped-dub reason adds 65 characters.

The worker treats this deterministic validation error as a temporary outage:
`languages()` calls `later()`, which halts the whole run. Oldest-first processing
hits the same video on every five-minute run, preventing the six later active
videos and subsequent series/draft work from advancing. The failing video's
local state is `done`, so this does not appear as the normal blocked/retry case.

## Definition of done

- [x] A language batch with long skipped-dub reasons submits within the API's
  500-character summary limit while preserving full reasons in its payload.
- [x] A persistent per-video submission validation error cannot indefinitely
  starve later videos; it has a visible, bounded recovery path.
- [x] Genuine service/authorization/quota failures retain appropriate stopping
  behavior and do not become an unbounded paid retry loop.
- [x] Regression tests cover long multilingual reasons and progress of a later
  video after the earlier video's permanent submission failure.

## Steps

- [x] Bound the human summary in `review/sync.mjs`; keep diagnostics in the
  existing `payload.locales[locale].dub.reason` field.
- [x] Classify and isolate persistent language-submission failures in the worker,
  preserving approvals, files, language choices, and existing retry guarantees.
- [x] Run focused review/automation tests and task validation.
- [x] Track separately authorized production deployment and acceptance in
  `2026-09-29-verify-video-language-queue-recovery`.

## How to verify

`node --test tools/video/review/sync.test.mjs tools/video/automation/automation.test.mjs`

`npm run check:tasks`

Production acceptance requires fresh logs and persisted project/review state;
container uptime or a successful retry click alone is insufficient.

## Notes

- The owner approved implementing the fix and opening a draft PR. No production
  writes, retries, restarts, deployments, or approvals were performed.
- Implemented a compact summary fallback, preserving full reasons and hash-bound
  language manifests. Only review POST/file PUT HTTP 413 or 422 is classified as
  invalid submission; project reports, reads, authentication, quota, network and
  server errors keep their previous behavior.
- Invalid language submissions persist as blocked while the worker continues to
  other videos. One-shot retries preserve the original done/active state, including
  retry acknowledgement recovery after restart, so finished videos do not rerun
  their production stages.
- Focused review and automation tests: 84 passed using bundled Node 24.19.0;
  independent read-only code review found no actionable regressions.
- Full tools suite with the same runtime: 678 passed, 2 skipped, 0 failed
  (`node --test tools/*.test.mjs "tools/video/**/*.test.mjs"`). Production
  acceptance remains in the separate open follow-up ticket.
- Claim used --force only after verifying the blocking legacy tasks' changes were
  merged as PR #870 and #904. The current knowledge-series branch has no remaining
  automation diff against main. Open PR #933 changes other flow sections; this fix
  does not take over its story worker work. No other owner's task was modified.
- Observed production revision: `717e16280977fb5e024947bde000adbe0fe4d752`.
  The deployed revision contains the same unbounded summary and halt behavior.
- Worker logs show the same failure from 2026-09-28 16:21:52 UTC through at least
  2026-09-29 00:44:23 UTC. Worker restart count 0, OOM false, global/per-video
  STOP absent, filesystem 59% used with 81 GiB available. Restart alone repeats
  the deterministic error.
- Code: `review/sync.mjs` appends full skipped reasons at lines 540-555;
  `apps/api/app/video_reviews/schemas.py` caps `ReviewSubmit.summary` at 500;
  `automation/flow.mjs` line 1607 calls `later()`, lines 434-437 set `halted`,
  and `automation/cli.mjs` line 111 stops the run. Full errors already exist in
  the structured payload; do not discard them to shorten the summary.
- Six active worker videos follow the failing Academy video: ENISA denominator,
  GPT-6 Sol/Luna, Claude Opus three numbers, Google Vids quota, WordPress 7.1.2,
  and OpenAI/Cursor wind-down. Four site rows remain `retrying` even though the
  retry requests were acknowledged; two retain the pre-final-approval stage.
- Local tasks and open PRs were checked for duplicates; PR #945's six post-deploy
  audit defects do not include this error. Recheck ownership before implementation,
  especially other tasks editing `automation/flow.mjs`.

### Separate backlog work observed during diagnosis

These are not all fixed by the summary patch. Continue them through their owning
content tasks and original producer workspaces, without inventing approvals:

- 48 non-dropped projects were present. Fifteen pending reviews are all Shorts:
  12 imported `cut` clips and 3 `lab` pilots. Stored QA failures: facts 15, policy
  15, narration 14, layout/evidence/metadata/links 12 each, loudness 7, profile 2,
  variety 2. `channel_stance` is empty. Sample facts failure is missing
  `verify.json`; imported cuts lack `check.json`, measured layout, and a parent
  video URL. Two clips are below the 25-second minimum. Do actual checks/rebuilds
  and regenerate QA; never mark missing evidence as passed.
- Existing follow-up: `2026-09-28-video-shorts-pilot-launch` covers the 3 pilots
  and notes the 12 imported clips from PR #880. Required work includes channel
  stance, source/fact review, audio/visual review, duration/loudness correction,
  parent-video linkage, and resubmission. Stored parent-approval failures predate
  the owner's later approval of the six parent videos and need fresh evaluation.
- Eleven projects have stored stage `outline approved` and eight have
  `final video approved`, but the corresponding server reviews are already
  approved. Stage means the next unfinished milestone from the last producer
  report. Approving a review does not refresh the project checklist; the producer
  must pull the hash-bound decision and continue/report.
- None of those eleven outline-stage projects or the six imported
  `ai-real-world-*` long videos has `auto.json` in the server worker volume.
  Website registration is not automatic adoption by the server worker. Resume
  from the original workdir/import producer, preserving hashes and media; do not
  fabricate `auto.json` or repeat the owner's approval. The six imported finals
  were approved around 2026-09-29 00:29-00:30 UTC; their package/language delivery
  still needs the originating producer to continue. The other two final-stage
  projects are the worker's WordPress/Cursor videos blocked behind Academy.
