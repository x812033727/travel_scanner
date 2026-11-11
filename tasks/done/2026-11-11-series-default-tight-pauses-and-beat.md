---
id: 2026-11-11-series-default-tight-pauses-and-beat
title: Series default: tight pauses and beat still motion for curio and sothatswhy episodes
status: done
priority: P1
area: tools
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T00:43:31Z
created_at: 2026-11-11T00:34:59Z
completed_at: 2026-11-11T00:59:57Z
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
---

# Series default: tight pauses and beat still motion for curio and sothatswhy episodes

## Why

The owner set tight pauses (`pauses: { line_ms: 0, scene_ms: 150 }`) and beat stills (`still_motion: "beat"`) for
奇聞檔案局 on 2026-11-05, but each video.json had to opt in, and none of the episodes written since did
(curio-w01, s42, h24, w03, sothatswhy-p05). So the cuts keep the 7-10% silence and the slow glide that
`.agents/skills/producer/references/pace-targets.md` measured as the biggest gap to the reference channels.
The owner asked on 2026-11-11 to make both the series default for 奇聞檔案局 and 原來如此事務所.

## Definition of done

- [x] A new host episode of either series (cute-mystery or cute-cartoon preset) gets both settings when the writer wrote neither.
- [x] A local curio- or sothatswhy- drama without them is warned by lint, and nothing is changed behind an approved timeline.
- [x] The skill says so.
- [x] The duration review is rebound by an independent reviewer (flow.mjs, lint.mjs and automation.test.mjs are bound).

## Steps

- [x] `core/curio.mjs`: `SERIES_PACING`, `isPacedSeries`, `pacingWarnings`; `core/lint.mjs` calls it.
- [x] `automation/flow.mjs` `settle()`: `PACED_PRESETS` adds the copy when absent; the writer's own choice stays.
- [x] Tests in `core/curio.test.mjs` and `automation/automation.test.mjs`.
- [x] Independent duration review increment (claude-review-series-pacing-20261111, PASS).

## How to verify

`node --test tools/video/core/curio.test.mjs tools/video/automation/automation.test.mjs tools/video/long-form/review.test.mjs`
and `node tools/video/long-form/cli.mjs check`.

## Notes

- Tight pauses shorten the estimated timeline of the same script (0.3 s a line, 0.55 s a scene). The
  `longExplainer` fixture grew only to 8.5 minutes at the default pauses and fell under the 8-minute floor
  once settle() tightened them, so the narrative panel skipped it; the fixture now measures with the series
  pauses. A real script near the floor needs more content, not longer pauses.
- Claimed with `--force` (owner's go-ahead, 2026-11-11): the overlapping claims on flow.mjs and
  automation.test.mjs were seven tasks in review since 2026-10-24 to 2026-11-04, past the 24-hour stale mark.
- `tools/deploy-host-verify.test.mjs` fails 16 tests on main as well in this container; unrelated.
