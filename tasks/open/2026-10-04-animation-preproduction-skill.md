---
id: 2026-10-04-animation-preproduction-skill
title: animation-preproduction skill: plan, risk-grade and lock an animated episode before paying Hailuo, Kling or the server
status: in-progress
priority: P1
area: docs
owner: claude-opus-5-5-animation-preproduction
claimed_at: 2026-10-04T14:40:06Z
created_at: 2026-10-04T14:40:03Z
completed_at:
branch: claude/hailuoai-kling-animation-optimize-208bc1
depends_on: []
scope:
  - .agents/skills/animation-preproduction
  - .claude/skills/animation-preproduction
  - AGENTS.md
  - tools/animation-preproduction.test.mjs
  - .agents/skills/animation-production
  - .claude/skills/animation-production
  - .agents/skills/animation-camera/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
  - .agents/skills/animation-camera/references
  - tools/animation-production.test.mjs
  - docs/videos/drama-craft
---

# animation-preproduction skill: plan, risk-grade and lock an animated episode before paying Hailuo, Kling or the server

## Why

The owner (2026-10-04): 「邊做邊修改最消耗成本」. Before any credit is spent on Hailuo, Kling
or the server, the scenes, camera setups, each shot's route and seconds, first and last
frames, risks and budget should be planned and confirmed once, then produced in batches.
The owner pointed at the channel 真一隻布袋喵 as the way of making it to follow or beat.

The two animation skills say how to write a shot (`animation-camera`) and how to spend and
account (`animation-production`), but nothing covers the step between: there is no locked
shot list, no per-shot spec sheet for the web routes (seconds to buy, first-frame file and
hash, end frame, final prompt, credits), no animatic, no batch order, no checklist of what to
confirm with the owner, and no change control after a lock. The code also hides an expensive
trap the skills never mention: `visualHash` (`tools/video/core/timeline.mjs`) covers the whole
`scene.data`, so editing one word of a shot's `motion` (which the image model never reads)
re-judges every keyframe, stales the storyboard approval and forces imported clips to be
imported again.

## Definition of done

- [x] A new shared skill `animation-preproduction` (mirrored SKILL.md, listed in AGENTS.md)
      takes an agent from an approved script to one owner-confirmed lock package: conditions
      card, scene and setup plan, shot list with route, seconds, first/end frame, risk grade,
      expected and capped credits, a free animatic, a three-shot pilot choice, batch order,
      readiness checklist and change control.
- [x] Three offline scripts (`shot_plan.mjs`, `animatic.mjs`, `plan_lock.mjs`) produce the
      shot list, the animatic and the lock/change order, with tests in `npm run test:tools`.
- [x] The 真一隻布袋喵 production grammar is measured (cuts, sizes, motion, structure, how AI
      weaknesses are hidden), cross-checked by a second agent, recorded in
      `docs/videos/drama-craft/`, and used as the skill's reference.
- [x] Kling is priced per second from the official guides; Hailuo's official camera commands
      and prompt structure replace "unverified" where the official pages settle it.
- [x] Known contradictions in the animation references are fixed; the shot_reading
      offscreen-target false positive is fixed (its own task).
- [x] A fresh agent using only the skill produces a lock package for the example scene.

## Steps

- [x] Research workflow: channel measurement, official Hailuo/Kling docs, pre-production practice.
- [x] Kling per-second pricing in `episode_estimate.mjs` and its tests.
- [x] New skill: SKILL.md, references, scripts, tests.
- [x] Updates to animation-production and animation-camera.
- [x] Forward-use test and adversarial review; fix what they find.
- [x] File the follow-up tasks (profile works on external routes; paid verification list;
      stray `.claude/skills/youtube-video/references/` copies).

## How to verify

```bash
node --test tools/skills.test.mjs tools/animation-production.test.mjs tools/animation-camera.test.mjs tools/animation-preproduction.test.mjs
npm run test:tools
npm run check:tasks
```

## Notes

- Owner decisions 2026-10-04 (AskUserQuestion): a third skill rather than a section of
  animation-production; documentation plus offline scripts only (no `tools/video` change, no
  credits spent); production-profile works on Hailuo/Kling become a separate task; unverified
  numbers become a paid-verification list for the owner to approve.
- `youtube-video/SKILL.md` and the `tools/video` core files are bound by the long-form review
  receipt (`docs/videos/long-form/review.json`); this task touches neither.
- Research (2026-10-04/05, workflow): seven Budaimiao videos measured shot by shot, two
  cross-checked by a second agent; recorded in
  `docs/videos/drama-craft/reference-study-20261004-budaimiao.md` and its per-shot JSON. The probe
  is unreliable on effect-heavy videos (it merges back-to-back cuts; a contact-sheet count counts
  flashes), so the study quotes ranges only: battle-video median about 0.75-1.0 s. B's numbers
  were recomputed from the verifier's listed false and missed cuts (225-246 shots, median
  0.88-1.0 s); A's false cuts are not listed one by one, so A stays an estimate. "Re-cut one clip
  at lightning flashes" was refuted (lightning inside one shot).
- What the skill took from it: scene types in P2 (dialogue scenes follow `drama-craft.md`,
  battle scenes the measured grammar), move chains in P3, colour and anchor decisions before the
  look gate, a four-shot move-chain pilot, and the cost rule that battle scenes cost per
  composition, not per second.
- Forward-use test: a fresh agent locked a redesigned 12-shot fight scene offline with only the
  skill; its findings (fight wording misread by the risk grader, plan_lock missing shot_plan's
  flags) were fixed before the review commit.
- Follow-ups filed: `2026-10-04-profile-works-external-clip-route`,
  `2026-10-04-paid-verification-hailuo-kling-web` (about 350 credits, for the owner),
  `2026-10-04-stray-youtube-video-reference-copies`, `2026-10-04-minimax-h3-adapter-v2-shape`,
  `2026-10-04-drama-montage-beats-flash-cuts`, `2026-10-04-yt-shot-probe-merges-back-to`.
