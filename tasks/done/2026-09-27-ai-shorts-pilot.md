---
id: 2026-09-27-ai-shorts-pilot
title: AI Shorts: vertical pilot pipeline and 90-day campaign
status: done
priority: P2
area: tools
owner: codex-ai-shorts
claimed_at: 2026-09-27T18:18:48Z
created_at: 2026-09-27T18:18:40Z
completed_at: 2026-09-27T18:51:25Z
branch: codex/ai-shorts-pilot
depends_on: []
scope:
  - tools/video/shorts
  - docs/videos/ai-shorts
---

# AI Shorts: vertical pilot pipeline and 90-day campaign

## Why

Implement the approved Mokaair faceless, Traditional Chinese AI experiment Shorts campaign. The existing renderer is landscape only. The first three Shorts must contain actual recorded model outputs, not invented wins or failures. Publishing and the 90-day observation period follow owner review.

## Definition of done

- [x] Independent 1080x1920 local render, narration, captions, evidence-bound package and checks; existing landscape behavior unchanged.
- [x] Fifteen actionable briefs, a 120-post / 90-day calendar, source register, budget and analytics tools.
- [x] Three actual experiment pilots with immutable inputs/outputs, independently checked conclusions and local MP4 previews.
- [x] Scoped and repository tooling checks pass; unfinished live publication and measurement work has an explicit handoff task.

## Steps

- [x] Check branch/worktree/remote/PR ownership and claim narrow scope.
- [x] Implement and verify the local Shorts tools.
- [x] Run experiments, author scripts and render the three pilots.
- [x] Independent review, visual inspection and handoff; this change is submitted as a draft PR.

## How to verify

`node --test tools/video/shorts/*.test.mjs`, `npm run test:tools`, `npm run check:tasks`; run the documented pilot build commands, inspect contact sheets and ffprobe/QA records.

## Notes

- Base: origin/main 5c586ed8. PRs #867/#868 author other video documents; #870 changes the shared drama workflow. This task adds independent tools/video/shorts and docs/videos/ai-shorts only.
- The board dates in UTC (2026-09-27); the user's local date is 2026-09-28 Asia/Taipei.
- No production release or publication is included in this local implementation. Media stays outside Git. Three pilot experiments use separate fresh-context Codex agents on the current session model; exact backend model version is not exposed and must not be invented.
- Delivery receipt: docs/videos/ai-shorts/delivery-2026-09-28.md and .json. Three final MP4s are 40.87 / 42.53 / 40.40 seconds, all technically checked and independently inspected as static contact sheets. Actual narration listening and phone/Studio playback remain owner review.
- Shorts tests: 28/28. Full tool tests on bundled Node 24.19.0: 490 pass, 1 skip, 0 fail. Initial system Node 24.13.0 crashed in existing tests with 0xC0000409; using the existing bundled runtime resolves the run. No global Node installation changed.
- check:tasks passes with existing stale-claim / overlap warnings. Four engineering review findings were fixed and independently rechecked. Final source and output hashes verified at receipt creation.
- Live review, publication and observation are explicitly tracked in tasks/open/2026-09-27-ai-shorts-owner-review-studio-launch.md. The 120-slot calendar is an example until the owner chooses the first actual public date; only fifteen topics and three MP4s are produced.
- Pre-PR ownership recheck: remote main still 5c586ed8; open #867/#868/#870 concern other video scopes, no collision with tools/video/shorts or docs/videos/ai-shorts.
