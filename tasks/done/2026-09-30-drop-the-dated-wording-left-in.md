---
id: 2026-09-30-drop-the-dated-wording-left-in
title: Drop the dated wording left in the automated video reference
status: done
priority: P3
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-01T03:15:04Z
created_at: 2026-09-30T09:40:13Z
completed_at: 2026-10-01T03:16:39Z
branch: claude/audit-followups
depends_on: []
scope:
  - .agents/skills/youtube-video/references/automated.md
---

# Drop the dated wording left in the automated video reference

## Why

`.agents/skills/youtube-video/references/automated.md` still states two current rules as
history: line 3 「關卡有四個，2026-09-27 起（`docs/videos/HANDS-OFF.md`）前三個由 AI 決定」 and line
93 「2026-09-26 參考一支同類影片後加了四種」. A dated rule reads as one incident's patch.

## Definition of done

- [x] Line 3 reads 「關卡有四個（`docs/videos/HANDS-OFF.md`），前三個由 AI 決定」.
- [x] Line 93 reads 「放具體例子的四種」.

## Steps

- [x] Claim after `2026-09-30-video-worker-moves-two-videos-at` releases the file (its #999 is
  merged; the ticket may only need closing by its owner).

## How to verify

`node --test tools/skills.test.mjs`

## Notes

Left out of the medium-confidence audit PR because an active ticket's scope holds this file.

Done 2026-10-01. Claimed with `--force`: `2026-09-30-video-worker-moves-two-videos-at` holds this
file, but its claim (2026-09-30 01:13Z) is more than 24 hours old, it records no branch, and its work
landed in #999. Open PR #1056 edits line 154 of the same file, far from these two lines.
