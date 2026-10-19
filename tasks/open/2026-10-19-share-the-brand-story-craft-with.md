---
id: 2026-10-19-share-the-brand-story-craft-with
title: Share the brand-story craft with Codex as a repo skill
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-quirky
claimed_at: 2026-10-19T00:40:27Z
created_at: 2026-10-19T00:33:28Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/brand-story
  - .claude/skills/brand-story
  - AGENTS.md
---

# Share the brand-story craft with Codex as a repo skill

## Why

站主 2026-10-19 要 Codex 也能把品牌故事做得跟 Claude 一樣好。品牌故事的做法散在 `docs/videos/STORY.md`、
各批企劃包與 Claude 的私人記憶裡（站主的定案、改編五集的流程、盲評兩位讀者、念法審查要另一個代理、
重試不重置計數、部署前 drain……）；Codex 讀不到記憶，只讀 repo 的 `.agents/skills/`。

## Definition of done

- [x] `.agents/skills/brand-story/SKILL.md` 寫下站主定案、一批怎麼做、產線卡住怎麼辦、查核的教訓，
      `.claude/skills/brand-story/SKILL.md` 是位元相同的副本。
- [x] `AGENTS.md` 的 skill 清單列出 `brand-story`。
- [x] `node --test tools/skills.test.mjs` 綠。

## How to verify

`node --test tools/skills.test.mjs`；在新的 Codex session 打 `$brand-story`、Claude Code 打 `/brand-story` 能載入。

## Notes

- 工人每一步的細節仍在 `.agents/skills/youtube-video/references/story.md`，新 skill 只指過去，不重寫。
- 認領時 `AGENTS.md` 跟 `2026-10-14-curio-episodes-keep-the-series-look` 的 scope 重疊：那張票的 skill 與 lint
  已在 main（`.agents/skills/curio-episode/`、`tools/video/core/curio.mjs`），票本身停在 in-progress 沒收，
  所以用 `--force` 認領，只動 `AGENTS.md` 的 skill 清單一行。
