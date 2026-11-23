---
id: 2026-11-11-curio-and-sothatswhy-length-follows-the
title: Curio and sothatswhy length follows the content: no 8-minute floor, warn under 5 minutes
status: done
priority: P1
area: tools
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T01:11:55Z
created_at: 2026-11-11T01:11:28Z
completed_at: 2026-11-11T01:30:00Z
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/duration.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/checks.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/automation.test.mjs
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - docs/videos/long-form
---


# Curio and sothatswhy length follows the content: no 8-minute floor, warn under 5 minutes

## Why

On 2026-11-11 the owner asked to drop the eight-minute floor for 奇聞檔案局 and 原來如此事務所
(first a warning under five minutes, then under eight). It was implemented in `093cd193` and
`fdd49471` on draft PR #2069.

## Outcome: reverted by the owner's decision, not shipped

The same day, before the duration review increment was written, the owner reversed it:
「8 分鐘下限也幫我留著好了」. The floor stays everywhere. Instead the topic pools are reviewed so a
topic whose material cannot carry eight minutes without padding goes to a reserve list, to be made
later only when related material can join it. Both commits were reverted in one commit; the bound
files are back at the bytes of the series pacing default increment, so the duration review needs
no new increment.

## Notes

- `followsContentLength` was keyed on the cute-mystery/cute-cartoon explainer look and had to
  exclude brand stories in the same look (`story-` slug, `brand-stories*` series, category story),
  which C08/C20 short-band tests caught. Keep that in mind if this comes back.
- Claimed with `--force` over the same stale review-state claims as the pacing task.
