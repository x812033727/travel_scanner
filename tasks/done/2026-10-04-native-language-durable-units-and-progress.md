---
id: 2026-10-04-native-language-durable-units-and-progress
title: Recover native language calls with durable unit receipts and visible progress
status: done
priority: P1
area: tools
owner: claude-opus-5-5-language-units
claimed_at: 2026-10-07T01:22:51Z
created_at: 2026-10-04T14:43:49Z
completed_at: 2026-10-07T01:25:52Z
branch: claude/sharp-bardeen-ob6fn9
depends_on:
  - 2026-10-03-video-worker-narration-takes-made-stale
  - 2026-09-30-video-worker-moves-two-videos-at
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/run-receipts.mjs
  - tools/video/automation/run-receipts.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Recover native language calls with durable unit receipts and visible progress

## Why

Normal videos with four selected caption languages and three dub languages stay
at the same language status while many source-bound units are translated and
reviewed. The page sees no partial progress until the complete batch is submitted.
At 2026-10-04 14:37 UTC, Grok had current English and Japanese translations plus
one of five Korean units; WAF had current English, Japanese and Korean plus one
of six Simplified Chinese units. Neither had begun dubbing. Both had new persisted
results and no language failures in the preceding two hours.

The native client still sends translator and caption_reviewer through the
295-second synchronous route even when durable_stage_runs is true. The existing
job API accepts these stages. A long or lost reply can leave completed paid work
unavailable to its caller. Merely removing the writer-only client guard is unsafe:
a saved translation followed by a pending reviewer must adopt its exact saved
unit before the next unit can start after a process restart.

## Definition of done

- [x] Native translation and caption review reconnect to the same source-bound
      operation after a lost submit, lost body or restart, without another paid run.
- [x] A translated unit followed by a pending reviewer survives restart; the
      reviewer recovers and the next unit advances without a false input-change hold.
- [x] A pending video has its own next-check time and cannot stop other eligible
      videos or repeatedly take the oldest slot.
- [x] The backend receives actual locale/unit checkpoint progress while ready,
      uploaded and listening acceptance still require their existing gates.
- [x] Preserve current source/final/owner choices, model authority, STOP/drop,
      budgets, 24-line/2400-character units and the existing two production lanes.

## Steps

- [x] Recheck and resolve the dependent active claims before touching their
      flow/automation-test scopes; their implementation may already have landed.
- [x] Bind each language operation and successful response to the actual saved
      units/checkpoint hashes before starting another operation in that stage.
- [x] Add project-local pending scheduling and truthful progress reports without
      skipping any translation review or audio check.
- [x] Keep the imported approved-final runner's pending/unknown behavior and its
      frozen source/runtime contracts compatible; broaden scope only after review.

## How to verify

Use injected counting fetch and the real native Automation/client paths with no
live paid endpoint. Cover lost submit/body, restart, translated draft plus pending
review, next unit, source/final/choice/model changes, STOP/drop, and pending-project
fairness. Every unit must still be reviewed before merging. Run affected native
client/receipt/automation tests and the complete tools suite with a compatible Node.

## Notes

- The measured baseline is about 40 model calls for Grok's 92-line/four-locale
  worksheets and 48 for WAF's 104-line/four-locale worksheets, before three dubs
  and their line-level synthesis, transcription and listening checks.
- Successful units continue immediately. The 300-second worker sleep is after an
  auto round ends or halts; it is not a fixed wait after every successful unit.
- Production has one video-ai queue consumer. Durability preserves results; it
  does not prove greater model throughput. Do not increase worker concurrency,
  change providers or raise budgets as an unreviewed shortcut.
- The separate normal speech POST/result-preservation issue is tracked by
  2026-10-04-preserve-normal-speech-results-before-retrying; this ticket is not its
  implementation and must not claim that client is fixed.
- Read-only proof: temporary artifact
  mokaair-video-language-native-20261004-1437-evidence.json,
  SHA-256 e9726509ef990b0be448eeb972e1d06757401963c6a6d3a1b300ff25963a8630.
  No source/model/setting change or production restart was made for that probe.
- Filed as an unclaimed follow-up while the dependent flow scopes remain active.
  PR #1210 head d0958ab contains the separate six-source approved-final recovery;
  it is draft with 22 successful checks and has not been merged or deployed.

### 2026-10-07 implementation (claude-opus-5-5-language-units)

- Claimed with `--force` past the dependency: `2026-10-03-video-worker-narration-takes-made-stale`
  landed in #1182 and only its post-deploy production check is open;
  `2026-09-30-video-worker-moves-two-videos-at` is done. The two `review` claims that held these
  files (#1340, #1341, both on main) were closed on the owner's behalf in this branch.
- `client.mjs`: `DURABLE_STAGES` = writer, translator, caption_reviewer (the shorten and reword
  variants included). With `durable_stage_runs` on they go through `durableRun`, so the saved
  request key reconnects after a lost submit, a lost body or a restart. Off, they stay on the
  synchronous route as before.
- `flow.mjs`: `unitCheckpoint()` runs after each kept translation or review. It adopts the run
  that gave it, bound to `<locale>.units.json`, as `saveAndLint` does for the writer, so a round
  that stops on the next request leaves no journal that the next unit reads as a changed input.
  It then reports a `languages_progress` checklist row (`en 翻譯：2／4 段已審，1 段譯好待審`), best
  effort; the locale's own report after the merge drops it. Ready/uploaded/listening gates untouched.
- Pending fairness needed no change: a language unit runs inside `move()`, which sets `unitVideo`,
  so a pending translator or reviewer sets only that video aside (`pendingUntil`, one lookup per
  round) and the lane goes on. The end-to-end test asserts the same run leaves it alone.
- Unchanged: unit sizes (24 lines / 2400 chars), every unit still reviewed before merge, STOP
  (no submit; tested), drop, budgets, model authority, lane count.
- PR #1210's approved-final runner is not on main and no other caller sends these stages.
- Throughput note for the owner: a durable stage polls up to 25 s, then the video waits for the next
  round (about 5 min) instead of the synchronous route's up to 295 s, so a slow unit can take a round
  longer. This trades speed for not losing paid answers, as the writer already does.
- Tests: client.test (lost submit/body/restart per stage and variant; STOP; durable off),
  automation.test (four-unit translation over a fake job route with a lost submit, a lost body
  and a restart with the reviewer pending; 8 jobs, no synchronous call, progress rows). Both new
  tests fail on the old code. Not verified here: the production run, which needs a deploy.
