---
id: 2026-10-08-video-teaching-outcomes-and-examples
title: Require useful learning outcomes and transferable examples in tutorial writing
status: done
priority: P1
area: tools
owner: codex-teaching-outcomes
claimed_at: 2026-10-08T17:56:20Z
created_at: 2026-10-08T17:56:13Z
completed_at: 2026-10-08T18:05:30Z
branch: codex/mods-clarity-20261009
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
---

# Require useful learning outcomes and transferable examples in tutorial writing

## Why

The tutorial-writing contract can produce a coherent API tour without teaching a useful viewer task. The owner explicitly rejected this outcome after comparing two reference tutorials. A recurring example and honest untested labels are necessary but do not establish educational value.

## Definition of done

- [x] Planning, writing and listener guidance require a useful audience outcome, a complete main example, a contrast and a transfer exercise.
- [x] Missing demonstrations or learner steps require a writer revision; passing layout/runtime checks and expected-result labels cannot stand in for practical teaching evidence.
- [x] Shared skill guidance and existing route-boundary tests remain consistent, without changing translation, story/drama, voice or media duration rules.

## Steps

- [x] Update the shared teaching contract and writing guidance.
- [x] Independently review the change and run affected prompt/register, skill parity and task checks.

## How to verify

Run `node --test tools/video/automation/prompts.test.mjs tools/video/automation/register.test.mjs`, the existing skill parity test and `node tools/tasks.mjs check`. Inspect the actual assembled planner/writer/listener prompts and preservation of other routes. These checks establish delivery of instructions, not that generated videos teach effectively; actual learner review remains part of production.

## Notes

Scope collision checks found only this task's existing draft PR #1390 on these paths. The duration review registry does not bind these source/test files, as independently checked by `review_own_video`; no receipt is rewritten for them. Do not edit `prompts.mjs` or `automation.test.mjs` under this scope. The Claude skill directory has no separate references tree; writing references remain under `.agents`, and mirrored SKILL.md entrypoints are unchanged.

Validation: existing prompt/register tests pass 27/27; shared skill checks pass 7/7; task validation passes 1,685 files with existing stale-claim warnings. Independent read/diff review by `review_own_video` found no blocking issue. These are writing/review instructions, not a newly implemented runtime/schema gate and not proof of audience learning. Source hashes reviewed: register `2563e3c73a5bc5ba3fd3a303d08daeb4fd64a99c4438f0fc1714c17c44488895`, prompt test `b81974d00f60aded043ab5956b336efc597bdeb28a5748a86cc729b3ec07708e`, writing reference `19ce64ba48f94b40f676d1606f608226aca496de2e5cdeda8ab75399f98924ac`.
