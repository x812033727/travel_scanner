---
id: 2026-10-02-keep-named-look-clip-judge-questions
title: Keep named-look clip judge questions within schema limit
status: review
priority: P2
area: tools
owner: codex-named-look-question-20261003
claimed_at: 2026-10-03T11:39:02Z
created_at: 2026-10-02T19:20:02Z
completed_at:
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
---

# Keep named-look clip judge questions within schema limit

## Why

`clipRubric()` interpolates a character's full appearance into one identity
question whenever `shot_look` is present. The approved Wedding Reckoning E1
Zhitang base look produces a 422-character question, but `JudgeCriterion.question`
allows at most 400 characters (`apps/api/app/video_media/schemas.py`). A normal
clip judge request can therefore be rejected by request validation before the
judge runs, even though the character and named look are otherwise valid.

## Definition of done

- [x] Every generated clip judge question satisfies the existing 400-character
  schema limit for supported character and named-look inputs.
- [x] Named-look identity checks still distinguish facial identity from the
  requested clothing, hair and age, without losing relevant appearance context.
- [x] Regression coverage includes the E1 Zhitang base look and a longer named
  appearance, while preserving the existing non-named-look behavior.

## Steps

- [x] Reproduce the 422-character identity question from the existing E1 source.
- [x] Adjust the clip rubric/context construction inside the declared scope;
  retain the backend schema limit and normal review gates.
- [x] Add boundary and semantic regression checks to `clips.test.mjs`.
- [ ] Run the targeted tests, tools tests and task validation.

## How to verify

From the repository root, this read-only reproduction currently prints `422`:

```bash
node --input-type=module -e "import fs from 'node:fs'; import {clipRubric} from './tools/video/media/clips.mjs'; const doc=JSON.parse(fs.readFileSync('docs/videos/series-plans/competition-20261002/episodes/episode-01-voice.video.json','utf8')); const character=doc.characters.find(x=>x.id==='zhitang'); console.log(clipRubric([{...character,shot_look:'zhitang--base'}])[0].question.length);"
node --test tools/video/media/clips.test.mjs
npm run test:tools
npm run check:tasks
```

No provider generation or paid judge call is needed to reproduce or verify this
request-shape issue.

## Notes

- Filed as an open, unclaimed P2 while producing the two approved episodes;
  the production handoff does not claim or fix the media core.
- The problem is the question's **422 characters versus a 400-character
  maximum**, not a captured provider error. The offline Pydantic validation of
  that request rejects it; no failed paid call is required as evidence.
- `clipRubric([character])` without `shot_look` remains short enough for the
  current S01 base-look request. Its complete named appearance is still carried
  in the request's context. This scoped preparation is not a general code fix.
- Before filing, searched open/done tasks for `clipRubric`, named-look rubric
  length and judge 400-limit issues; no matching task was found. The task-board
  collision helper checked local worktrees, remote heads and open PRs for both
  scoped files: no active scoped claim or open PR touched them. The existing
  commits on `origin/main` did not resolve this issue.


### 2026-10-03 local correction (shared PR #1175)

- Fresh gate checked 481 distinct local/remote heads, 33 live remote branches, 28 registered worktrees and complete files of the sole open PR (#1175, own). No current active ancestor claim or dirty implementation matched these two files. Two historic scoped deltas are already present in main; a newer content branch's complete incremental comparison is disjoint. Evidence: `C:/Users/x8120/.codex/tmp/named-look-clip-question-20261003/scope-gate.json`. Normal claim succeeded without force.
- Named-look questions now use schema-bounded character/look IDs and refer to the full requested appearance in context. Context retains the exact full name and appearance and adds the matching IDs. Ordinary short-name question/context are unchanged; an ordinary question switches to the bounded ID form only when it would exceed 400 characters or its sheet label would exceed 80; the full name stays in context. No text is truncated, and facial identity/bone structure versus clothing/hair/age override remains explicit.
- Meaningful old-source RED: all three new cases failed on question-length assertions, including the original E1 Zhitang 422-character question. Final bundled Node 24.19.0 focused module: 20 passed, 0 failed in 18.23s. Cases cover the real E1 input, 800-character appearance, 24-character IDs, long display names and complete mocked judge context. All 17 pre-existing test blocks are unchanged.
- Final source/test hashes, fixture hash, RED/GREEN logs and unchanged run-function guard proof: `C:/Users/x8120/.codex/tmp/named-look-clip-question-20261003/implementation-receipt.json`. The run-function changes are judge context identity metadata and the overlong sheet-label fallback described below; duration/frame rules, request model/settings, approval/budget and retry/reservation behavior are unchanged. All media and judge activity was mocked.
- Remaining coordinated checks: complete `test:tools` and task validation, plus an independent DURATION_ONLY incremental review/rebind because `docs/videos/long-form/review.json` binds `clips.test.mjs`. This author has not changed either long-form review file, removed old bindings or self-signed a replacement. Keep status `review`; do not treat focused local tests as duration, media, publication or owner acceptance.

- Independent review caught an additional request-contract gap in the new long-name fixture: `JudgeFile.label` also has an 80-character maximum. The revised fixture failed against the first author implementation on that exact label assertion. Labels of at most 80 characters remain unchanged; longer labels use the bounded character ID, with full name and matching ID retained in context. A 75-character name exercises label-only fallback while its original ordinary question still fits 400; both the question and context must use the matching ID so the question never names a nonexistent full-name sheet label. The final test loops 74/75/540-character names and checks every request file label.
- Final after-review focused run: 20 passed, 0 failed in 9.15s, bundled Node 24.19.0; all 17 original test blocks remain unchanged. `label-red.log` and `label-final-green.log` are the additional evidence; the original local receipt is preserved as `implementation-receipt.pre-label.json`, with the current receipt updated to the final two hashes. Full tools/task checks and the separate independent duration binding remain pending as above.

- Final coherence correction: the 75-character label boundary now selects the ID/context question as well as the ID sheet label; the test explicitly rejects a question that claims a full-name label absent from `files`. `coherent-final-green.log` records the final 20/20 pass. Earlier label-only receipt bytes remain in `implementation-receipt.pre-coherence.json`; current source/test hashes are in the current receipt. Full tools and independent duration rebind remain pending.
