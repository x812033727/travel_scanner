---
id: 2026-10-26-qa-warns-when-a-long-video
title: QA warns when a long video is cut with no channel bookends installed
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-26T01:47:53Z
created_at: 2026-10-26T01:47:44Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/qa/cli.mjs
  - tools/video/qa/qa.test.mjs
  - .agents/skills/youtube-video/references/automated.md
---

# QA warns when a long video is cut with no channel bookends installed

## Why

The channel intro and outro package lives only on the host and the owner's computer. A hand run in a cloud container has no `_branding/` in its work directory, so `assemble` silently cuts a long video with no bookends and every QA item still passes. The PHP2Shell news video reached the owner that way on 2026-10-25.

## Definition of done

- [x] QA's assemble item warns when a narrated long video was cut without bookends because no package is installed.
- [x] The youtube-video skill says to install the package before a hand-run assemble.

## Steps

- [x] Warning in `tools/video/qa/cli.mjs`, asserted in `qa.test.mjs`.
- [ ] Rebuild PHP2Shell with the package once the owner provides it (the PHP2Shell ticket).

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
