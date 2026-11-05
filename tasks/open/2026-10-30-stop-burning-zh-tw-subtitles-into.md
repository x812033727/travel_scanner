---
id: 2026-10-30-stop-burning-zh-tw-subtitles-into
title: Stop burning zh-TW subtitles into story and curio videos
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-no-burn-in
claimed_at: 2026-10-30T18:57:48Z
created_at: 2026-10-30T18:26:39Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/explainer-family.test.mjs
  - tools/video/automation/story.test.mjs
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - docs/videos/channel-review-20261025-story-series/README.md
  - docs/videos/curio-h24/video.json
  - docs/videos/curio-s30-v2/video.json
  - docs/videos/history-curiosity/brand-files-remake-20261031/README.md
---

# Stop burning zh-TW subtitles into story and curio videos

## Why

站主 2026-10-25 試燒繁中字幕，2026-10-31 決定不燒：品牌故事與主機 cute-mystery 單集改回 CC。

## Definition of done

- [ ] 部署後，主機新開的品牌故事與 cute-mystery 單集 `subtitles.burn_in` 是 false，成片畫面沒有燒字幕。

## Steps

- [x] `flow.mjs settle()`、`story.mjs` 改 false，測試與 skill 跟著改。
- [x] `curio-h24`、`curio-s30-v2` 的 `video.json` 改 false。
- [ ] 時長收據增量、PR、部署。

## How to verify

`node --test tools/video/automation/story.test.mjs tools/video/automation/explainer-family.test.mjs tools/video/automation/automation.test.mjs`；`node tools/video/long-form/cli.mjs check`。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

站主 2026-10-31 同意用 --force 認領：範圍與幾張舊的進行中票重疊（flow.mjs 等），本票只改 burn_in 一行。已燒字幕的片怎麼處理，見 `docs/videos/history-curiosity/new-rules-migration-20261031.md`。
