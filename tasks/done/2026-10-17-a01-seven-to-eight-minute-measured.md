---
id: 2026-10-17-a01-seven-to-eight-minute-measured
title: A01 seven to eight minute measured QA
status: done
priority: P1
area: tools
owner: codex-gpt6-a01-duration
claimed_at: 2026-10-17T23:15:16Z
created_at: 2026-10-17T23:14:12Z
completed_at: 2026-10-18T15:11:20Z
branch: codex/a01-seven-eight-minute-qa-20261018
depends_on: []
scope:
  - tools/video/core/duration.mjs
  - tools/video/core/duration.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/qa/duration.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - tasks/open/2026-10-14-correct-a21-pringles-patent-fact-and.md
  - tasks/open/2026-10-14-curio-episodes-keep-the-series-look.md
  - tasks/open/2026-10-16-bind-story-audits-and-narration-to.md
  - tasks/open/2026-10-17-a01-public-sources-from-cited-claims.md
---

# A01 seven to eight minute measured QA

## Why

A01 `story-rolling-suitcase-v2` has an owner-approved seven to eight minute
story target. The shared long-video QA still requires eight minutes, and script
lint skips narrative rules below eight minutes. The change must be limited to
this exact A01 episode. B18 and other narrated films keep their current gates.

## Definition of done

- [x] The current measured A01 narration body passes only from 420 through 480
      seconds, inclusive; bookends cannot supply missing body time.
- [x] A01 still receives the narrated episode and hook lint at seven minutes.
- [x] B18 and all other existing duration and narrative thresholds are unchanged.

## Steps

- [x] Release only already-merged file claims from the two completed-scope
      parts of older tickets under the owner's prior explicit authorization.
- [x] Add exact A01 identity recognition and measured QA bounds.
- [x] Give only A01 an effective eight-minute writing budget and 420–480
      second measured TTS band, while its shared series target remains ten.
- [x] Apply the narrative lint gate to exact A01 at seven to eight minutes.
- [x] Add meaningful frame-boundary, identity, bookend and B18 tests.
- [x] Obtain independent long-form duration receipt review before merging.

## How to verify

`node --test tools/video/core/duration.test.mjs tools/video/core/lint.test.mjs
tools/video/qa/duration.test.mjs tools/video/automation/story.test.mjs`,
`npm run check:tasks`, then `node tools/video/long-form/cli.mjs check` after
an independent reviewer binds the changed files.

## Notes

2026-10-18 integration after main #1565, #1568 and #1564: the A01 code was
rebased onto `7468c19a3`. `story.test.mjs` retains both the new
`thumbnail.brand` test and the A01 legacy-script HOLD tests; the code changes
in `story.mjs` combine without a semantic conflict. A separate duration
receipt reviewer preserved main's four #1565 bindings and one #1568 binding,
then added the five already independently reviewed A01 bindings. All 108
current file hashes match the merged report and JSON; final report SHA-256 is
`d69abc46569fc19777672b85d59a72c75c95e1342f30e54068828917fa7f0a18`.
The long-form CLI passed 473 plans and receipt regression passed 2/2. The six
affected duration, lint, story, timeline and template suites passed 146/146
with bundled Node v24.19.0 (exit 0). Main's A01 plan has no
`thumbnail.brand`, so this merge does not itself change A01's
thumbnail. The #1568 task's other active scope remains untouched. New hosted
CI and A01 formal production gates are still separate.

The earlier `dd18c5bc...` report SHA below is the historical receipt for the
pre-#1565/#1568 branch; the integrated report SHA above supersedes it.

2026-10-18 independent receipt closeout on rebased code `f9580975f`: a
separate reviewer inspected the five changed duration/lint/QA files and
updated only their SHA bindings in the 108-file long-form receipt. The other
103 bindings did not change. Final report SHA-256 is
`dd18c5bcb30df873840817ac378a3c76c93e96fbd3b6c1344f3eb48f53f10e94`.
`node tools/video/long-form/cli.mjs check` passed 473 plans and the receipt
regression passed 2/2. The coordinating agent ran the four complete focused
suites with bundled Node v24.19.0: 100/100 passed; `npm run check:tasks`
passed. PR #1563 remains a draft with `no-auto-merge`; CI on this new head,
merging, deployment and the separate A01 host transition are not claimed.

2026-10-18: Owner-authorized scope transfer takes only the two long-form
duration receipt paths from the A21, curio-look and lexicon tickets. Their
other scope, ownership, unfinished work and draft branches stay intact.
This task now owns independent SHA rebinding for A01's five changed files.
The unclaimed #1517 receipt cleanup task remains open; other draft PRs that
edit the receipt require a fresh binding check at integration. No merge,
deploy, host write or paid work is authorized by this transfer.

2026-10-18: `origin/main` is f9afbafa3. The curio task still claims
`lint.mjs`, although #1500 merged its lint change; the lexicon task still claims
`automation/story.mjs` and `story.test.mjs`, although #1548 merged those parts.
The owner authorized releasing only the completed claims while preserving the
other open work and #1518. This ticket records those narrow task-file changes.

Draft #1518 still touches `story.mjs` and `story.test.mjs` and currently reports
DIRTY against main. Its branch is preserved untouched. This A01 work starts
from current main and must be reconciled with #1518 before either merges.

2026-10-18: A01-only worker and QA changes have focused coverage for both
inclusive 30 fps boundaries, bookends, stale timelines, B18 480-second floor,
and a seven-minute draft that still receives hook/outro/loop checks. The
shared `series.json.target_minutes` remains 10; the A01 episode writer payload
sets an explicit eight-minute budget. `qa/cli.mjs` continues to pass current
audio and presentation timelines through `assembleItem` to
`knowledgeDurationProblems`; no flow override is needed.

`check:tasks` passes with pre-existing stale and overlapping-scope warnings.
The changed `duration.mjs` and `lint.mjs` are bound by
`docs/videos/long-form/review.json`; a different reviewer must inspect and
update that receipt before merge. Several other active tasks still claim those
receipt files, so ownership requires coordination first. Separately,
`composeStory` copies all plan sources into `video.json`; filtering A01 to
claim-cited source indexes is the separate, unclaimed
`2026-10-17-a01-public-sources-from-cited-claims` task and is outside this
change.

Independent code review identified an existing-host transition risk: an A01
already stopped after six chapters can still carry `video.json.target_minutes`
`[9,11]`. Its ordinary retry now fails closed before any relint, narrative
panel or paid TTS call; it does not overwrite the old merged script or six
chapters. If an A01 `video.json` exists but any chapter file is missing, the
retry also holds for both old and new targets instead of recreating a chapter
or replacing the merged script. The independent script-review checker also compares the persisted
target with a fresh compose from those six chapters, so an old receipt cannot
approve the legacy target. A separate host transition must inspect current
paid assets, preserve the old files and hashes, recompose an A01 `[7,8]`
candidate from the six chapters, rerun lint and storytelling review, and
independently bind a new script-review receipt before explicit retry. This
code change does not perform that host transition.

Local verification on bundled Node 24.19.0: core duration/lint plus QA
duration suites passed 69/69; full story suite passed 28/28 before the final
legacy-guard ordering adjustment; the five affected pilot/worker tests passed
5/5 after that adjustment. `npm run check:tasks` passed for 1,936 files with
pre-existing stale-claim and overlapping-scope warnings. The long-form
duration receipt remains stale on five changed files until independent review.
The hold persists auto.json state and may initialize a pronunciation snapshot;
its preservation guarantee is the existing chapter files and video.json,
with zero new writer/TTS calls. The post-review 4/4 pilot regression rerun
included the missing-chapter plus legacy and current target cases.

The static story prompt still describes a generic ten-minute cute story. For
exact A01, the writer call now carries top-level `target_minutes: 8`, a
chapter-specific eight-minute budget, and an explicit owner instruction to
override that generic example. This makes the request unambiguous but cannot
mechanically prove how a model will respond; actual chapters and measured TTS
remain gated by the existing independent script review and duration checks.
