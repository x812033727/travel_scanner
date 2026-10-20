---
id: 2026-10-20-curio-s43-darwin-beagle-audited-script
title: Curio S43 Darwin Beagle audited script preproduction
status: in-progress
priority: P2
area: docs
owner: codex-s43-darwin-source
claimed_at: 2026-10-20T09:26:27Z
created_at: 2026-10-20T09:26:23Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s43
---

# Curio S43 Darwin Beagle audited script preproduction

## Why

S43 source feasibility is complete in task `2026-10-20-curio-s43-darwin-beagle-nose-source`. The parent requested a source-audited A-option long script, matching visual claims and a manual site outline handoff, without borrowing approval or budget from other episodes. The owner has not chosen this episode's outline.

## Definition of done

- [ ] The A/B brief is parsed by the site and its exact version is submitted to the manual outline gate; pending owner choice is recorded, not treated as approval.
- [ ] Candidate A long-body script, scene/visual claims, and local manifest pass timing, Curio picture proportion and narrative lint.
- [ ] Two independent first-read narrative audits and a separate complete source/visual audit pass against the exact files, with durable hashes and findings.
- [ ] No script gate, TTS, paid imagery/music, render, upload, or fabricated owner approval before this episode's owner outline decision.

## Steps

- [x] Claim S43 scope separately from the finished source-feasibility ticket.
- [x] Reformat the existing A/B plan into `outlineOptions`' exact heading/summary/hook shape.
- [ ] Draft A script and manifest; preserve edited-letter versus retrospective-memory attribution.
- [ ] Run local lint and duration check; remove unsupported visuals and padding.
- [ ] Arrange two blind first-viewer reads and a separate source/visual audit of the frozen version.
- [ ] Submit report-only site registration and manual outline review, then pull pending status; record receipt.

## How to verify

Run `node --input-type=module -e 'import {outlineOptions} from "./tools/video/review/sync.mjs"; ...'` to confirm two A/B options, then `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s43 --json` and `... narrative --slug curio-s43 --json` once the manifest exists. `npm run check:tasks` and `npm run test:docs-videos` cover board and video docs. Independent readers receive only the final script hash; source auditor reopens the three pinned hashes and checks every spoken factual claim and nonliteral visual prompt. `review-pull --gate outline` must say approved for any dependent gate; a pending result is a stop.

## Notes

2026-10-20: Parent specifically requested continuation after scoped source research commit `d9d5154a`. A is an editorial candidate, not an owner-approved outline. The fixed witness set is in `research.md`. `brief.md` now has two parser-ready `### 選項 A／B` sections, each with `一行說明` and `開場鉤子`. User's broad permission to keep making recommended episodes does not turn the site's exact-file manual gates into local approvals.
