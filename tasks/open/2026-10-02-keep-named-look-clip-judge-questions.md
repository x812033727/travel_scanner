---
id: 2026-10-02-keep-named-look-clip-judge-questions
title: Keep named-look clip judge questions within schema limit
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-02T19:20:02Z
completed_at:
branch:
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

- [ ] Every generated clip judge question satisfies the existing 400-character
  schema limit for supported character and named-look inputs.
- [ ] Named-look identity checks still distinguish facial identity from the
  requested clothing, hair and age, without losing relevant appearance context.
- [ ] Regression coverage includes the E1 Zhitang base look and a longer named
  appearance, while preserving the existing non-named-look behavior.

## Steps

- [ ] Reproduce the 422-character identity question from the existing E1 source.
- [ ] Adjust the clip rubric/context construction inside the declared scope;
  retain the backend schema limit and normal review gates.
- [ ] Add boundary and semantic regression checks to `clips.test.mjs`.
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
