---
id: 2026-10-14-curio-episodes-keep-the-series-look
title: Curio episodes keep the series look: a shared skill and a lint gate
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-curio-skill
claimed_at: 2026-10-14T14:37:02Z
created_at: 2026-10-14T14:36:22Z
completed_at:
branch: claude/curio-series-skill
depends_on: []
scope:
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
  - tools/video/core/lint.mjs
  - .agents/skills/curio-episode
  - .claude/skills/curio-episode
  - .agents/skills/youtube-video/SKILL.md
  - .claude/skills/youtube-video/SKILL.md
  - AGENTS.md
  - docs/videos/history-curiosity/look.md
---

# Curio episodes keep the series look: a shared skill and a lint gate

## Why

The owner asked on 2026-10-14 why the 奇聞檔案局 episodes Codex remade (H04 佳特洛夫事件, H05, H06;
draft PR #1484) look nothing like H01–H03. H01–H03 v2 draw 86–95% of their body as MiniMax
`cute-mystery` illustrations; H04–H06 v2 ended with no `look`, no illustration and 82–89 text cards.
The series rules lived only in `docs/videos/history-curiosity/look.md` and one agent's notes, no
skill pointed at them, and no tool refused an episode without illustrations. Codex wrote empty
scenes, figures from behind and period-material constraints into prompts and style, reviewed the
pictures as evidence reconstructions (9 judge-passed images kept 0–1), asked the owner to authorise
three images at a time, and fell back to source cards.

## Definition of done

- [x] A shared `curio-episode` skill (Codex and Claude read the same file) states the series
      decisions, the route per case, how prompts are written, how pictures are accepted, the card
      limits and the whole-episode budget; AGENTS.md and the youtube-video skill point at it.
- [x] `lint` refuses a `curio-` slug whose look is not the `cute-mystery` preset word for word,
      whose body is under 70% illustrations, or that runs more than three cards in a row. All eight
      delivered episodes pass; H04–H06 v2 as on `codex/curio-h04-h06-v2-20261014` fail.
- [ ] Duration receipt rebound by an independent reviewer (lint.mjs, both youtube-video SKILL.md).
- [ ] H04–H06 remade under the skill (follow-up task; the owner chose it on 2026-10-14).

## How to verify

`node --test tools/video/core/curio.test.mjs`, `node --test tools/skills.test.mjs`,
`node tools/video/cli.mjs lint --slug curio-h01-v2` (0 errors).

## Notes

- Thresholds from the delivered episodes: illustration share 73% (U02 v1) to 95% (H01 v2); longest
  card run 3 (U02 v1). A curio episode is recognised by its slug, because H04–H06 v2 had dropped
  `look` altogether.
- New episodes take the host's cute-explainer route (`cute-mystery`), where `settle()` already drops
  a writer's `style`/`negative` and the nine-question judge reads every picture; Codex worked in
  local `slides` format, where none of that applies.
- On 2026-10-15 the owner explicitly transferred the two independent duration-review receipt files out of this task's scope so an independent H09 CI reviewer can update the stale `clips.test.mjs` binding. This task retains its other scope and definition of done; coordinate the receipt result without editing `docs/videos/long-form/review.md` or `review.json` under this claim.
