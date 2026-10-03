---
id: 2026-10-03-animation-skills-hailuo-kling-measurements
title: Animation skills: the 2026-10-04 Hailuo and Kling measurements replace inferred and unverified figures
status: done
priority: P2
area: docs
owner: claude-fable-5-1-animation-measurements
claimed_at: 2026-10-03T17:39:53Z
created_at: 2026-10-03T17:39:23Z
completed_at: 2026-10-03T17:49:18Z
branch: claude/gifted-volhard-19f52e
depends_on: []
scope:
  - .agents/skills/animation-production/SKILL.md
  - .agents/skills/animation-production/references/providers-and-plans.md
  - .agents/skills/animation-production/references/cost-model.md
  - .agents/skills/animation-production/scripts/episode_estimate.mjs
  - .agents/skills/animation-camera/SKILL.md
  - .agents/skills/animation-camera/references/model-misreads.md
  - .claude/skills/animation-production/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
  - tools/animation-production.test.mjs
---

# Animation skills: the 2026-10-04 Hailuo and Kling measurements replace inferred and unverified figures

## Why

The `animation-production` and `animation-camera` skills were written on 2026-10-03 from
the plan pages alone: Hailuo's credits per second were inferred from the "about N seconds a
month" figures, the pixel size of a 2K clip was "not read", the time one clip takes was "not
measured", Kling's official guide sat behind a login, and a third-party claim that Kling only
makes 5- or 10-second clips had become 「8 秒不是 Kling 的檔位」. On 2026-10-04 one clip was
made on the owner's Hailuo Max account and the Kling guide and CLI were read on the owner's
Kling account. Several of the statements marked 推算 or 未驗證 are now measured, two were wrong
(Kling's durations, and the advice to paste a keyframe into the Hailuo form as base64), and
an agent that follows the old text downloads the watermarked file or leaves Kling's audio
and multi-shot defaults on.

## Definition of done

- [x] `references/providers-and-plans.md` carries the measured Hailuo facts with 實測
      2026-10-04 (12 credits a second at H3 2K, about 4 min 40 s for one clip, 2560x1440 at
      24 fps with an AAC track, the settings popover's options and its 21:9 default, the
      watermarked `<video>` src against 無水印下載), how the form is driven, and that the
      built-in browser cannot upload a local keyframe; the base64 advice is gone.
- [x] The same file describes Kling's two official ways (MCP endpoint, CLI
      `@klingai/cli-global`), the commands, the `image_to_video` models and parameters, the
      two defaults a shot must pass as false, and keeps credits per clip, 1080p on a paid
      plan and which balance the CLI charges marked unverified.
- [x] `animation-production/SKILL.md` (three-routes table, decision rule 3, the 還沒驗 list),
      `scripts/episode_estimate.mjs` (PLANS notes, a `credits_basis` per Hailuo tier) and
      `animation-camera/SKILL.md` (the Hailuo / Kling rewrite table and its example) say the
      same thing; 「8 秒不是 Kling 的檔位」 is gone.
- [x] `clips import` (pull request #1183) is recorded as existing and as run with real
      ffmpeg on the downloaded clip.
- [x] The `.claude/skills/` copies of both `SKILL.md` files are byte-identical.

## Steps

- [x] Rewrite §1 (routes table), §1.2, §1.3, the §2 tables, §3, §4 and §5 of
      `providers-and-plans.md`.
- [x] Update both `SKILL.md` files and copy them to `.claude/skills/`.
- [x] Update `episode_estimate.mjs` and assert the new field and notes in
      `tools/animation-production.test.mjs`.
- [x] The same two statements repeated in `references/cost-model.md` §四 and
      `animation-camera/references/model-misreads.md` §五.

## How to verify

```bash
node --test tools/skills.test.mjs tools/animation-production.test.mjs tools/animation-camera.test.mjs
npm run test:tools
npm run check:tasks
node .agents/skills/animation-production/scripts/episode_estimate.mjs tools/video/core/fixtures/drama/video.json --plan hailuo:pro
```

The last command prints `H3 2k 12 credits/s（實測 2026-10-04）` on the plan line.

## Notes

- No number was added that the 2026-10-04 session did not measure. Still unverified and
  marked so: Hailuo 768P (credits a second, output size), queue time when anything else is
  queued, Kling credits per clip, 1080p through the CLI on a paid plan, whether the CLI
  charges membership credits (the account that authorised was NORMAL with 0 credits, so
  nothing was generated), and image-to-video from a pipeline keyframe on either service.
- The estimator's numbers did not change: `DEFAULT_MINUTES_PER_CLIP` stays 6 (one measured
  clip with an empty queue is not a queue time) and Kling is still priced per 5-second unit,
  because credits for any other duration have no source. Its notes say both.
- The route keeps the name "Kling MCP" in headings and in `clips import --provider
  kling-mcp` although the owner chose the CLI; a clip made with the CLI is imported with
  that provider value and a `--note`.
- Pull request #1183 (`clips import`) edits the same paragraphs. The work started on its
  head and #1183 was squashed into `main` (170f3b6c1) before this was committed, with an
  identical tree, so this task's commit sits directly on `main`.
- `.agents/skills/animation-production/references/stage-preconditions.md` and
  `post-mortem.md` name the route "Kling MCP" only as a label and were left alone.
