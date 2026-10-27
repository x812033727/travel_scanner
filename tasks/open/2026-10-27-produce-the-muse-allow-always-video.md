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

- [x] The owner has chosen an outline from `brief.md` (A, 2026-10-27).
- [x] The Claude Code demonstration in 示範或實算 is run and logged.
- [ ] Script, two verifier passes, narration, final cut and publish package approved on the site.

## Steps

- [x] Search this week's Muse coverage and pull the official pages.
- [x] Write `brief.md` with three outlines.
- [ ] Find Meta's own Muse permission help page and its Japan/Taiwan availability announcement.
- [x] Run the demonstration (2026-10-27, Claude Code 2.1.311, see Notes).

## How to verify

`node tools/video/cli.mjs status --slug muse-allow-always-agent-permission`.

## Notes

- Workdir: the session scratchpad's `muse/` (sources in `muse/src/`).
- Reports disagree on prices and times; the brief keeps them out.
- Run log (2026-10-27 14:05–14:13 UTC, Claude Code 2.1.311 in manual mode, the owner asked the
  agent to run it): the push prompt offered "Yes, and don't ask again for: git push *"; choosing it
  wrote `Bash(git push *)` to `.claude/settings.local.json`; in a NEW session `git push --force`
  ran without a prompt and overwrote the remote main (69cd815 -> b2a3d6d); `/permissions` described
  the rule as "Any Bash command starting with git push / From project local settings"; after
  deleting it the force push asked again. Pane captures and RUNLOG.md are in the scratchpad's
  `muse/run/`.
