---
id: 2026-10-05-delivery-promise-and-continuity-locks
title: Delivery promise and continuity locks in the plan lock: a clip may not quietly become a still
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:24Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/animation-preproduction/scripts/plan_lock.mjs
  - .agents/skills/animation-preproduction/scripts/shot_plan.mjs
  - .agents/skills/animation-production/scripts/drama_preflight.mjs
  - .agents/skills/animation-production/scripts/run_report.mjs
  - tools/animation-preproduction.test.mjs
  - tools/animation-production.test.mjs
  - .agents/skills/animation-preproduction/references/preproduction-flow.md
  - .agents/skills/animation-production/references/stage-preconditions.md
---

# Delivery promise and continuity locks in the plan lock: a clip may not quietly become a still

## Why

Nothing records what a shot was promised to be. A shot planned as a clip can be rewritten
into a still or a `fit: freeze` and nobody is asked; the only record of the kind is
`plan/lock.json`'s `visual_kind` written by `plan_lock.mjs`, and `compareLock` reports the
change but no stage refuses it. Continuity (props, costume, time of day) is likewise only in
prompts. OpenMontage's "delivery promise" and the Chinese drama skill packs' continuity locks
(drama-skills, MIT; shuohao-skills, Apache-2.0) are the ideas; the lock file is where they fit
without touching the bound `core/drama.mjs`.

## Definition of done

- [ ] `plan/lock.json` records a `promise` per shot (`visual_kind`, bought seconds, route) and
      `continuity` locks (`depends_on` shot ids, locked prop / costume / time-of-day strings),
      written by `shot_plan.mjs`.
- [ ] `drama_preflight.mjs` exits with the lint code when a shot promised `clip` is now `still`
      or `fit: freeze` without a change-order line in `changes.jsonl`, or when a locked string is
      missing from a dependent shot's prompt; `compareLock` keeps reporting kind changes.
- [ ] `run_report.mjs` lists promised vs delivered per shot and the saved / spent delta.

## Steps

- [ ] Schema of the lock (`preproduction-flow.md` §鎖定包), `shot_plan.mjs` writes it,
      `plan_lock.mjs` compares it.
- [ ] `drama_preflight.mjs` findings `promise.broken`, `continuity.broken` with the fix text;
      `stage-preconditions.md` rows.
- [ ] `run_report.mjs` columns; tests in `tools/animation-preproduction.test.mjs` and
      `tools/animation-production.test.mjs`.

## How to verify

```bash
node --test tools/animation-preproduction.test.mjs tools/animation-production.test.mjs
node .agents/skills/animation-production/scripts/drama_preflight.mjs --slug <episode>   # exit 1 on a broken promise
```

## Notes

- No bound file. An `intent` key on `video.json` shots is a possible follow-up once
  `SHOT_KEYS` is free to change.
- Also carries the research's "shot dependencies and continuity locks" item.
