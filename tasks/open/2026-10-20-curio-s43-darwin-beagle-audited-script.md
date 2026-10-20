---
id: 2026-10-20-curio-s43-darwin-beagle-audited-script
title: Curio S43 Darwin Beagle audited script preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
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

- [x] The A/B brief is parsed by the site and its exact version is submitted to the manual outline gate; pending owner choice is recorded, not treated as approval.
- [x] Candidate A long-body script, scene/visual claims, and local manifest pass timing, Curio picture proportion and narrative lint.
- [ ] Two independent first-read narrative audits and a separate complete source/visual audit pass against the exact files, with durable hashes and findings.
- [ ] No script gate, TTS, paid imagery/music, render, upload, or fabricated owner approval before this episode's owner outline decision.

## Steps

- [x] Claim S43 scope separately from the finished source-feasibility ticket.
- [x] Reformat the existing A/B plan into `outlineOptions`' exact heading/summary/hook shape.
- [x] Draft A script and manifest; preserve edited-letter versus retrospective-memory attribution.
- [x] Run local lint and duration check; remove unsupported visuals and padding.
- [ ] Arrange two blind first-viewer reads and a separate source/visual audit of the frozen version.
- [x] Submit report-only site registration and manual outline review, then pull pending status; record receipt.

## How to verify

Run `node --input-type=module -e 'import {outlineOptions} from "./tools/video/review/sync.mjs"; ...'` to confirm two A/B options, then `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s43 --json` and `... narrative --slug curio-s43 --json` once the manifest exists. `npm run check:tasks` and `npm run test:docs-videos` cover board and video docs. Independent readers receive only the final script hash; source auditor reopens the three pinned hashes and checks every spoken factual claim and nonliteral visual prompt. `review-pull --gate outline` must say approved for any dependent gate; a pending result is a stop.

## Notes

2026-10-20: Parent specifically requested continuation after scoped source research commit `d9d5154a`. A is an editorial candidate, not an owner-approved outline. The fixed witness set is in `research.md`. `brief.md` now has two parser-ready `### 選項 A／B` sections, each with `一行說明` and `開場鉤子`. User's broad permission to keep making recommended episodes does not turn the site's exact-file manual gates into local approvals.

2026-10-20: Manual outline handoff is live at `/admin/videos`. `review-push --report-only` passed, `review-push --gate outline` submitted the two options and Jev recommended A (0.92), but this hand-pushed episode still requires the site's owner decision. `review-pull --gate outline` returned `waiting for the owner`, exit 3, on `brief.md` SHA `00b591b66f75f90899af6e9dd21ec5e88083c69cb7f27e85f7eec3391c178ec6`. Receipt: `docs/videos/curio-s43/verify-site-gates.md`. No script gate or media activity. A candidate is being drafted locally; do not treat it as approved while the outline is pending.

2026-10-20 handoff: Candidate A has `video.json`, generated `script.md`, and 89-row `claims.md` at hashes and static results in `docs/videos/curio-s43/verify-preproduction.md`: local lint 0/0, 7 chapters, 89/89 illustrated body scenes, 15 loops, 10.16 minute **estimate** including 3 outro lines. Corrected edited-letter silence as such; source and visuals have not had a separate full pass. Two independent blind first reads and a complete source/visual audit are required on these exact files. Parent requested this worker yield after scoped commit for S41 reviews; release the ticket for a later independent worker or re-claim once capacity returns. Site outline still pending owner, no script gate or paid media.
