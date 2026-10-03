---
id: 2026-10-03-video-length-floor-only
title: No upper bound on a video's length: only the eight-minute floor is enforced
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-03T17:11:05Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/automation/prompts.mjs
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/automated.md
  - .agents/skills/youtube-video/references/prompts/planner.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
  - docs/videos/README.md
  - docs/videos/DESIGN.md
  - docs/videos/AUTOMATION.md
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/components/admin-video-settings-tutorial.tsx
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# No upper bound on a video's length: only the eight-minute floor is enforced

## Why

The owner decided on 2026-10-04 (in chat): a video may run over 12 minutes; the only length
rule is "8 minutes or more". Dramas, Shorts, compilations, brand stories and long anime keep
their own formats. Until now the tools and documents treated 8-12 minutes as a range to stay
inside: `lint` warned when the estimate was above the upper end of `target_minutes`, the
planner and writer prompts said "within target_minutes", the skill said 「8–12 分鐘」, and the
admin field was labelled 「最長長度（分鐘）」. A writer that obeys those cuts sourced facts to
fit.

The owner chose the "tools and documents" level out of three: the admin setting
`target_minutes_max` stays (no API, schema, migration or worker-flow change; its 8..30
validation and its default of 12 stay) and becomes what the writer aims at, not a limit.

## Definition of done

- [x] `lint` does not warn when slides, a screencast or an explainer estimate above the upper
      end of `target_minutes`; under the eight-minute floor is still an error and under the
      lower end of the target is still a warning.
- [x] A drama, a brand story and a long anime lint exactly as before, on both sides.
- [x] The planner and writer prompts (slides and explainer), the youtube-video skill and its
      prompt references, and `docs/videos/README.md`, `DESIGN.md` and `AUTOMATION.md` say
      "8 minutes or more; the upper end is an aim, over it is fine; never cut a fact or pad".
- [x] The admin label of `target_minutes_max` no longer reads as a limit in the five locales,
      and one hint line under the two length fields says only the floor is enforced.
- [x] The dated note on measured narration speed is in `automated.md` and `writer-video.md`.
- [x] The duration receipt (`docs/videos/long-form/review.md` and `review.json`) is rebound by
      an agent other than the author.

## Steps

- [x] `tools/video/core/lint.mjs`: the upper half of the range warning is skipped where
      `needsMinimumLength(doc)` is true. The lower half stays, because between 8 minutes and
      the lower end it is the only early signal.
- [x] `tools/video/core/lint.test.mjs`: one test for both directions (slides and explainer over
      the upper end: no length warning; slides under the lower end: warning; a drama and a brand
      story over: still warn; slides under the floor, or a target that starts under it: still an
      error). A long anime and a compilation over the upper end are not asserted: a long anime's
      target must equal its story body, so the fixture cannot be put over it cheaply.
- [x] `tools/video/automation/prompts.mjs`: slides planner and writer, the explainer's common
      block and its two planners.
- [x] Skill: `SKILL.md` (route table, hard rule 10) copied byte-identically to `.claude/`,
      `references/automated.md`, `references/prompts/planner.md`, `writer-video.md`.
- [x] Docs: `docs/videos/README.md`, `DESIGN.md`, `AUTOMATION.md`.
- [x] Admin: `videoSettings.fields.target_minutes_max` and a new `videoSettings.lengthHelp` in
      the five `admin.json` files; the hint is rendered in `admin-video-settings-tutorial.tsx`.
- [x] Duration receipt increment by an independent agent (see Notes).

## How to verify

```bash
node --test tools/video/core/lint.test.mjs
npm run test:tools && npm run check:tasks
npm run check:i18n && npm run lint:web && npm run typecheck:web
```

On the site after a deploy: `/admin/videos` settings, the panel 成片參數 shows
「目標長度上緣（分鐘，可超過）」 and the hint under the two fields. If the label still shows the
old wording, look for an administrator copy override of
`videoSettings.fields.target_minutes_max`.

## Notes

- **The claim was refused and not forced.** `npm run tasks -- claim` reported an overlap with
  seven active tasks (several in `review` since 2026-09-27..30 hold `apps/web/messages`,
  `tools/video/core/lint.mjs`, `tools/video/automation/prompts.mjs`,
  `.agents/skills/youtube-video/references` and the duration receipt). The work was done on
  the owner's direct request on branch `claude/video-length-floor-only` by
  `claude-fable-5-1-length`; the coordinator has to look at open pull requests that touch the
  same lines before merging. The edits are one-line replacements, so a conflict is small.
- **Duration receipt: rebound on 2026-10-04** by `claude-pr-review-video-length-floor-only`
  (section "Branch video-length-floor-only increment: 14 files" in `review.md`). The same
  session also wrote the small review-fix commit before it (one sentence in `automated.md`, one
  phrase in `prompts.mjs`, the hint's first sentence in four locales, two assertions in
  `lint.test.mjs`); the report says so. Any later change to a bound file needs another
  increment, and a merge of main that touches the receipt needs a follow-up. `lint.mjs`, `lint.test.mjs`,
  `prompts.mjs`, both `SKILL.md` copies, `automated.md`, the five `admin.json`,
  `admin-video-settings-tutorial.tsx`, `docs/videos/README.md` and `DESIGN.md` are bound in
  `tools/video/long-form/review.mjs`. The author may not rebind them
  (`.agents/skills/dev-and-ci/references/duration-receipt.md`). The reviewer should say in
  Findings that this is the owner's 2026-10-04 decision: only the over-the-upper-end warning
  is removed for slides, screencasts and explainers; the 8-minute floor, the 480-second
  measured body and the 600/780-second targets are untouched.
- An explainer's target is `[10, 10]`, so before this change it warned on anything but exactly
  10.0 minutes; now only under 10. AI-terms episodes (`[9, 11]`) also stop getting the
  "about 12 minutes; the target is 9-11" warning. `docs/videos/ai-terms/README.md` line 15
  still describes that warning as one that "can stay"; the file belongs to the active
  `2026-09-29-ai-terms-video-pilot` task and was left alone. It needs a one-sentence update.
- The measured-speed note (estimate 12.2 minutes, synthesized 13.07, 2026-10-04, a
  storytelling-style illustrated video) contradicts the older "voice reads about 300 a
  minute, so the estimate runs long". Both are recorded side by side; the 250 constant was not
  changed. Re-measuring the speed per register is worth its own task.
- Accepted consequence: nothing caps a script's length now except the 8..30 validation of the
  aim, so narration, illustration and render cost grow with length. The writer prompt's
  "never pad to reach it" is the only guard.
- The one-off explainer request field still validates 8..20 minutes in the API
  (`EXPLAINER_MAX_MINUTES`); that is the request's target, not a cut's limit, and is out of
  scope here.
- The prompts take effect for stages run after a deploy of the worker.
