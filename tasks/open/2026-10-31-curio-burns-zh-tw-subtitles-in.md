---
id: 2026-10-31-curio-burns-zh-tw-subtitles-in
title: Curio burns zh-TW subtitles in again; brand stories stay on CC
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-curio-burn
claimed_at: 2026-10-31T07:39:43Z
created_at: 2026-10-31T07:39:28Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/explainer-family.test.mjs
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - docs/videos/channel-review-20261025-story-series/README.md
  - docs/videos/curio-s30-v2/video.json
  - docs/videos/history-curiosity/new-rules-migration-20261031.md
  - docs/videos/history-curiosity/old-rule-inventory-20261031.md
  - docs/videos/history-curiosity/brand-files-remake-20261031/README.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Curio burns zh-TW subtitles in again; brand stories stay on CC

## Why

站主 2026-10-31 定案：奇聞檔案局燒繁中字幕，規則重製與之後的集數都燒；品牌故事不燒（#1941 已合併的部分保留）。

## Definition of done

- [ ] 部署後，主機新開的 cute-mystery 單集燒字幕，品牌故事不燒。
- [x] 本機路線的 curio- slug 沒寫 `burn_in: true` 時 lint 警告。

## How to verify

`node --test tools/video/core/curio.test.mjs tools/video/automation/explainer-family.test.mjs`；`node tools/video/long-form/cli.mjs check`。

## Notes

站主同意過 --force 的先例是 #1941；這張票同樣只改 burn_in 一行，範圍與幾張舊的進行中票重疊。圖坦卡門與楊貴妃 s31-v2 已做成不燒，video.json 維持 false，等站主決定。
