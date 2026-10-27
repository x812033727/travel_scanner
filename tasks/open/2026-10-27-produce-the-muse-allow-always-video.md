---
id: 2026-10-27-produce-the-muse-allow-always-video
title: Produce the Muse Allow Always video: the agent permission you granted once (muse-allow-always-agent-permission)
status: in-progress
priority: P2
area: docs
owner: claude-muse-video
claimed_at: 2026-10-27T11:03:19Z
created_at: 2026-10-27T11:03:17Z
completed_at:
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - docs/videos/muse-allow-always-agent-permission
---

# Produce the Muse Allow Always video: the agent permission you granted once (muse-allow-always-agent-permission)

## Why

The owner chose this topic on 2026-10-27 from the week's candidates. Meta's Muse agent gave a
Toronto YouTuber's address to a Marketplace buyer; Meta said Muse followed instructions and asked
for permission correctly, and the owner had pressed "Allow Always". Muse is not available in
Taiwan, so the video turns the same button in tools Taiwanese viewers use into a check: Claude
Code's "Yes, and don't ask again" (saved permanently per repository, prefix wildcards) and
Google's agent access filter.

## Definition of done

- [ ] The owner has chosen an outline from `brief.md`.
- [ ] The Claude Code demonstration in 示範或實算 is run and logged, or downgraded to CITED.
- [ ] Script, two verifier passes, narration, final cut and publish package approved on the site.

## Steps

- [x] Search this week's Muse coverage and pull the official pages.
- [x] Write `brief.md` with three outlines.
- [ ] Find Meta's own Muse permission help page and its Japan/Taiwan availability announcement.
- [ ] Run the demonstration.

## How to verify

`node tools/video/cli.mjs status --slug muse-allow-always-agent-permission`.

## Notes

- Workdir: the session scratchpad's `muse/` (sources in `muse/src/`).
- Reports disagree on prices and times; the brief keeps them out.
