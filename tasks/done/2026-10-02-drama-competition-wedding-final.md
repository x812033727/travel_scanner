---
id: 2026-10-02-drama-competition-wedding-final
title: Prepare wedding drama competition final optimization package
status: done
priority: P1
area: docs
owner: codex
claimed_at: 2026-10-02T14:58:09Z
created_at: 2026-10-02T14:58:09Z
completed_at: 2026-10-02T15:10:11Z
branch: codex/drama-competition-wedding-20261002
depends_on: []
scope:
  - docs/videos/series-plans/competition-20261002
---

# Prepare wedding drama competition final optimization package

## Why

The owner asked Codex to select one of its five existing original dramas for a
three-month YouTube competition against Claude and prepare the final optimization
before production. The selected work is wedding-reckoning; delivery requires Veo
3.1 Lite and zh-TW/ja/ko/en cast audio plus switchable CC on one main video.

## Definition of done

- [x] Compare the five current sources and select one with concrete narrative and production reasons.
- [x] Prepare forty episode-specific polish instructions, a 60-second opening and four-language line drafts.
- [x] Record user-confirmed competition rules, budget authorization and honest media readiness.
- [x] Independently review the complete handoff and validate its source links and hashes.
- [x] Save a reviewable draft PR and record the separate production follow-up.

## Steps

- [x] Read the latest source, production profile, reviews, tools and competing work.
- [x] Confirm one-video/own-three-calendar-month rules with the owner.
- [x] Owner accepted USD 3,000 target plus USD 1,000 reserve and separate views/cost evaluation.
- [x] Rebuild a selected review bundle outside Git; no media was generated.
- [x] Complete independent review and source-bound handoff; commit/push with a draft PR.

## How to verify

Run `node tools/video/cli.mjs production-check --slug wedding-reckoning` and
`node tools/video/cli.mjs production-build --slug wedding-reckoning --out
/workspace/mokaair-work/competition-20261002/review`; both are offline. Check forty
source-matching episode rows, four locales per pilot line, contiguous planned
shot windows, links and SHA-256 file bindings. Run `npm run check:tasks` and
`git diff --check`. These checks do not establish media quality or native listening.

## Notes

Production follow-up: `2026-10-02-wedding-competition-pilot-four-languages`.
Existing source/design and historical review receipts remain unchanged. This is a
concrete final-polish execution package, not forty completed screenplays or a film.
The generated bundle alone does not inject the new director overlay into writer;
the handoff explicitly requires it during per-episode authoring and verification.

Live preflight found missing video-tool pairing in this cloud environment;
unauthenticated speech/media GET routes respond 401, and `media-status` exits 3.
Do not read or disclose secrets. Node/ffmpeg are available. Pairing is needed before
already-authorized pilot spending; budget approval does not need to be requested again.

Independent review resolved opening-version conflicts, human-listening budget scope,
localized complete-film metadata, E30 flashback constraints, and visible-face
costume-continuity validation. No outstanding textual P1/P2 findings remain.
Package validation passed: forty episodes, fifteen shots, eleven lines, forty-four
localized variants. All ten source file hashes and twelve package file hashes matched.
