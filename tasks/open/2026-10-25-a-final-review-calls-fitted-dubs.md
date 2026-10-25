---
id: 2026-10-25-a-final-review-calls-fitted-dubs
title: A final review calls fitted dubs ready before audio checks pass
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-25T19:13:21Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/stages.mjs
  - tools/video/review/sync.mjs
---

# A final review calls fitted dubs ready before audio checks pass

## Why

The normal final-review builder calls dubsForUpload, which can label a current fitted M4A ready and attach it before the locale's current-WAV audio check has passed. During ForTy production, VI fitted all 89 windows and had a measured M4A while the genuine 92-line audio check still had 10, then 6/4 flags. A successful fit/meter is not evidence of accepted speech.

## Definition of done

- [ ] A final review only marks/attaches a foreign dub as ready when its latest current-WAV audio evidence passes; a missing, flagged or stale check stays explicitly unready.
- [ ] A previously passing check cannot certify replacement WAV/M4A bytes. Existing checked language submissions remain usable.

## Steps

- [ ] Claim after checking current branches, worktrees and open PRs; inspect core/stages and review/sync call paths.
- [ ] Reuse current audio-evidence validation rather than create a new weaker readiness definition.
- [ ] Add focused coverage for fitted-unchecked, flagged, stale-after-retake and genuinely checked tracks.

## How to verify

Run relevant native stage/review tests and the docs-video suite. In fixtures, a fitted current VI track with 92 lines but unresolved current flags must never be represented as ready. Verify current transcript/WAV binding, not only a historic zero flags file.

## Notes

2026-10-25 observed during PR1851; no shared tool code changed in the production work. Current workaround: sole producer completes genuine VI audio checks and pauses before EN; root then submits the main final, audits every attached locale and attaches full 1080p evidence, then releases the remaining locales. Never clear flags or attach an unchecked dub just to deliver the main. No production repair, merge, deploy or broad-scope claim is included in this ticket.
