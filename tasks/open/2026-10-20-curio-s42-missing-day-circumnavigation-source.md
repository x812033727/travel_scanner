---
id: 2026-10-20-curio-s42-missing-day-circumnavigation-source
title: Curio S42 missing day circumnavigation source and script preproduction
status: in-progress
priority: P2
area: docs
owner: codex-s42-missing-day
claimed_at: 2026-10-20T07:35:07Z
created_at: 2026-10-20T07:35:03Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s42
---

# Curio S42 missing day circumnavigation source and script preproduction

## Why

Pigafetta and Francisco Albo independently recorded that the Victoria crew called a Cape Verde landing Wednesday while island residents called it Thursday. A source-bound S-series episode can follow the single returning ship and its daily log to explain the discrepancy. The 1874 English collection includes eyewitness accounts, translations and editorial notes; these layers must remain distinct.

## Definition of done

- [ ] Distinct A/B brief, fixed primary-source text and claim matrix with independent evidence check.
- [x] Option A has an eight-minute-plus narration body, condensed cold open, series intro/outro and channel/source-link plan.
- [x] A source-tethered `video.json` with at least 70% `shot` scenes, no more than three consecutive cards, and no unsupported historical reconstruction.
- [ ] Two independent blind narrative reads and a separate complete scene/source audit; no site gate or paid media during this task.

## Steps

- [x] Check S01–S41 topics, task claims and PR scopes for duplication; claim `docs/videos/curio-s42` only.
- [x] Pin and read the translated firsthand accounts at an exact commit and hash; mark editor material and differing witness perspectives.
- [x] Draft A/B brief and research claim matrix; request independent source audit.
- [x] Build the local narration, visual shot plan and `video.json`; lint and run narrative review.
- [ ] Request independent blind and full scene/source audit; repair supported findings and record exact hashes.

## How to verify

Re-fetch the pinned raw `74723-0.txt`, compare SHA-256, reopen every linked line range and separate Pigafetta, Albo and later commentary. Run `NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s42`, `... narrative --slug curio-s42`, `npm run test:docs-videos` and `npm run check:tasks`. No site gate or paid command.

## Notes

2026-10-20: Existing S-axis topic bank ends at S36; S37–S41 have distinct tasks. Search found only an incidental Magellan reference in a St. Elmo's Fire card. No S42 scope or open PR. Same shared branch/PR as the current Curio batch; this claim only owns `docs/videos/curio-s42` and this ticket. Read-only feasibility located GITenberg `74723-0.txt` at commit `2c2276cebbf0ecd30bf46ddda5305d65aceb4002`, raw SHA-256 `d5c8c5548d57576da07be543263e06f2a20c71f6431222a6c28dc2e5338f9a5c`. Parent asked to continue scoped preproduction; site gates and paid media remain closed pending independent audits and owner workflow.

2026-10-20: Independent raw re-fetch and Q01–Q15 audit passed after four exact-line/attribution fixes. Pigafetta alone explains westward-day mechanism; Albo logs the mismatch and initially suspects a one-day error. `research.md` now labels the 1874 translation/editor and Barros/Navarrete transmission. Full receipt: `docs/videos/curio-s42/verify-sources.md`.

2026-10-20: Rebuilt A around Victoria and the dated voyage after older script blind reads failed 9/13 and 7/13. Current exact hashes, 80-scene structure, 9.2-minute local estimate, 0/0 lint, 236 passing docs-video tests, 2109 validated task files, and US$0.00 art dry-run are recorded in `docs/videos/curio-s42/verify-preproduction.md`. A new script-only blind and separate complete scene/source audit still remain. Do not send site gate or buy media on the current candidate yet.

2026-10-20 handoff: Revised script-only reads improved through 10/13, 11/13 and 12/13; last 12/13 reader flagged two remaining paraphrase repeats. Current script SHA `c07e98c4ff0055e320d38c17ef9de406264d0445ce3d5671e6120c219bc619c1` removes those repeats and adds exact-source story beats to strengthen the runtime margin. `lint` 0 errors/0 warnings, 83 body scenes, 77 illustrated shots, 9:17 estimated body (8:33 after condensed opening), art dry-run US$1.04 one take / US$3.12 three takes, US$0 spent. Full current details and exact video/claims hashes: `docs/videos/curio-s42/verify-preproduction.md`. **Need a new exact-version blind and a separate 83-scene source/visual audit before freezing this script.** Site/media stay held.
