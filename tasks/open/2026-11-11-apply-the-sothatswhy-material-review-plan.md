---
id: 2026-11-11-apply-the-sothatswhy-material-review-plan
title: Apply the sothatswhy material review: plan verdicts, reserve and merge plans get no brief
status: in-progress
priority: P1
area: tools
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T01:49:32Z
created_at: 2026-11-11T01:49:32Z
completed_at:
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - tools/video/so-thats-why/episode-plan.mjs
  - tools/video/so-thats-why/program.mjs
  - tools/video/so-thats-why/cli.mjs
  - tools/video/so-thats-why/catalog.test.mjs
  - docs/videos/so-thats-why/refresh-20261101/episodes.json
  - docs/videos/so-thats-why/refresh-20261101/EPISODES.md
  - docs/videos/so-thats-why/refresh-20261101/DURATION-AUDIT.md
---


# Apply the sothatswhy material review: plan verdicts, reserve and merge plans get no brief

## Why

On 2026-11-11 the owner approved the material review of the 19 unmade P-plans
(`docs/videos/so-thats-why/material-20261111/README.md`): 9 ready, 2 merge (P16 tides with P24 tsunami), 8 reserve.
The eight-minute floor stays and nothing is turned into Shorts.

## Definition of done

- [x] `episode-plan.mjs` `MATERIAL_REVIEW` gives each reviewed plan its verdict, estimate and what is missing. `episodes.json` carries it as `material`.
- [x] `episodeBrief` refuses a reserve or merge plan, or a topic that leads to one, and names what is missing. Ready plans and plans already made are unchanged.
- [x] `EPISODES.md` shows each verdict. `cli.mjs check` passes, with tests in `catalog.test.mjs`.
- [ ] P16 + P24 written as one merged plan (follow-up).

## Notes

- Claimed with `--force` over 2026-11-01-sothatswhy-episode-depth (codex), which has been in review since 2026-11-01 and is past the 24-hour stale mark. The owner approved stale take-overs this session.
- The reviewer stored `missing` as lists. The README table had printed Python list text and is fixed, and review.json now stores strings.
