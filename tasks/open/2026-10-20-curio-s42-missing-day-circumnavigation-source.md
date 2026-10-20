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

- [x] Distinct A/B brief, fixed primary-source text and claim matrix with independent evidence check.
- [x] Option A has an eight-minute-plus narration body, condensed cold open, series intro/outro and channel/source-link plan.
- [x] A source-tethered `video.json` with at least 70% `shot` scenes, no more than three consecutive cards, and no unsupported historical reconstruction.
- [x] Two independent blind narrative reads and a separate complete scene/source audit; no paid media during preproduction.

## Steps

- [x] Check S01–S41 topics, task claims and PR scopes for duplication; claim `docs/videos/curio-s42` only.
- [x] Pin and read the translated firsthand accounts at an exact commit and hash; mark editor material and differing witness perspectives.
- [x] Draft A/B brief and research claim matrix; request independent source audit.
- [x] Build the local narration, visual shot plan and `video.json`; lint and run narrative review.
- [x] Request independent blind and full scene/source audit; repair supported findings and record exact hashes.

## How to verify

Re-fetch the pinned raw `74723-0.txt`, compare SHA-256, reopen every linked line range and separate Pigafetta, Albo and later commentary. Run `NODE_USE_ENV_PROXY=1 VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s42`, `... narrative --slug curio-s42`, `... tts --slug curio-s42 --dry-run`, `... status --slug curio-s42`, `npm run test:docs-videos` and `npm run check:tasks`. Read `docs/videos/curio-s42/verify-3.md` and the current `review/check-flags.json` before any further paid media command. Preserve the held `md083` journal request; its earlier HTTP 502 provider charge remains unknown and the identical request must not be resent.

## Notes

2026-10-20: Existing S-axis topic bank ends at S36; S37–S41 have distinct tasks. Search found only an incidental Magellan reference in a St. Elmo's Fire card. No S42 scope or open PR. Same shared branch/PR as the current Curio batch; this claim only owns `docs/videos/curio-s42` and this ticket. Read-only feasibility located GITenberg `74723-0.txt` at commit `2c2276cebbf0ecd30bf46ddda5305d65aceb4002`, raw SHA-256 `d5c8c5548d57576da07be543263e06f2a20c71f6431222a6c28dc2e5338f9a5c`. Parent asked to continue scoped preproduction; site gates and paid media remain closed pending independent audits and owner workflow.

2026-10-20: Independent raw re-fetch and Q01–Q15 audit passed after four exact-line/attribution fixes. Pigafetta alone explains westward-day mechanism; Albo logs the mismatch and initially suspects a one-day error. `research.md` now labels the 1874 translation/editor and Barros/Navarrete transmission. Full receipt: `docs/videos/curio-s42/verify-sources.md`.

2026-10-20: Rebuilt A around Victoria and the dated voyage after older script blind reads failed 9/13 and 7/13. Current exact hashes, 80-scene structure, 9.2-minute local estimate, 0/0 lint, 236 passing docs-video tests, 2109 validated task files, and US$0.00 art dry-run are recorded in `docs/videos/curio-s42/verify-preproduction.md`. A new script-only blind and separate complete scene/source audit still remain. Do not send site gate or buy media on the current candidate yet.

2026-10-20 handoff: Revised script-only reads improved through 10/13, 11/13 and 12/13; last 12/13 reader flagged two remaining paraphrase repeats. Current script SHA `c07e98c4ff0055e320d38c17ef9de406264d0445ce3d5671e6120c219bc619c1` removes those repeats and adds exact-source story beats to strengthen the runtime margin. `lint` 0 errors/0 warnings, 83 body scenes, 77 illustrated shots, 9:17 estimated body (8:33 after condensed opening), art dry-run US$1.04 one take / US$3.12 three takes, US$0 spent. Full current details and exact video/claims hashes: `docs/videos/curio-s42/verify-preproduction.md`. **Need a new exact-version blind and a separate 83-scene source/visual audit before freezing this script.** Site/media stay held.

2026-10-20 R11 preproduction handoff: After the 83-scene complete source/visual review and focused fixes, two fresh no-history readers scored the exact `script.md` SHA `b70b82c4eb73fc997d2eb5e3ca55b1766a66a218d6c4d093406fb789905e284d` **13/13 each**. Independent focused source/visual checks cover each later changed line and image prompt; exact receipts and hashes are in `docs/videos/curio-s42/verify-preproduction.md`. `lint` 0 errors/0 warnings, estimated 9:19 body including the 0:44 cold open; actual voice length still needs measurement. The 83 body scenes include 77 illustrations (92.8%) and six data cards. One source-linked, six-beat `shorts.json` draft passes schema/episode checks, without media. Installed global 5-second intro follows the cold open at assemble, 21-second outro follows voice; final 16 seconds are for Studio links. Source/channel URLs are in both long and Short metadata. No voice, art, music, render, upload or paid call for S42. Next supported step is report-only site outline/script preflight, then manual owner gates; a `pending owner` receipt is not approval for voice or media.

2026-10-20 site handoff: `review-push --report-only` passed; first outline submission revealed that the A/B headings lacked the parser's `選項` prefix. `brief.md` now exposes both existing options and their one-line summaries/hooks to the site parser at SHA `29beb1e0307a117470445b2aa23a120073e27f101ec6fa2a32dfdb9f58ba4bb7`. The newer manual outline submission superseded the old one; Jev recommended A (0.98), but `review-pull --gate outline` says `waiting for the owner` (exit 3). Exact receipt: `docs/videos/curio-s42/verify-site-gates.md`. Do not send script gate until the owner chooses the outline; no TTS/art/music/site approval was invented. After outline choice, verify the exact brief hash, then submit the script and rehash `script.md` because that command regenerates it.

2026-10-20 production gate continuation: Site formally chose outline A for the same brief hash. Current script SHA-256 `3a0f9748ae41cfebf9853a9fcf3413dd6937b464bdb6b8210e1b335d72db0677` has fresh independent 13/13 narrative validation and source/visual checks; precise receipt in `docs/videos/curio-s42/verify-2.md`. The exact script was submitted to the site and remains **pending**; user standing instruction authorized a clearly labeled local delegated script approval. Initial 86 Gemini voice lines completed. First audio check flagged 14, and 13 targeted redos completed, but the `md083` redo returned HTTP 502 with uncertain provider outcome and a held journal. A zero-pending/zero-paid `tts` safely rebuilt the mixed current audio; second `check-audio` still flags **8/86** (`md043`, `md053`, `md065`, `md068`, `md069`, `md070`, `md072`, `md083`). Do not forget/reissue held request `ac8ad4385d8f2a5fde8e24640f53eb41d75dd83e11417b8ae09f2417d6de5e52` before provider usage is reconciled. Audio review, images, music and render remain closed. Whole-episode image/music cap US$3.44 was conditional and **US$0 art/music spent**.

2026-10-20 eight-line narration repair: The eight flagged script lines were minimally rewritten against the pinned source; exact `script.md` SHA-256 `ddccd9cdf418412bbcaa5159ae9ad6fe6acb4cabbde76a70640405e65b5d7b4c`. Two independent fresh readers produced 12/13 and 13/13; official merged narrative verdict is 13/13 PASS, preserving reader A's `no_recap` concern as an individual answer. Policy precheck PASS; `lint` 0 errors/1 existing warning. Script and audio were sent to the site and both await the owner's decision. TTS synthesized only the eight changed-hash lines (214 billable characters), reusing 78 cached lines. `check-audio` now flags **0/86**. The old `md083` held request was untouched; its possible provider charge remains unknown. See `docs/videos/curio-s42/verify-3.md` for the source delta, review hashes and audio receipts. No art, music or final cut was made in this repair.

2026-10-20 MiniMax three-shot pilot blocker: Source review corrected only `md001`'s prompt to show an empty basket in daylight; exact `video.json` SHA-256 `8b8dd7b5a9754938693f758bdf3c90622a1b815ff72d6dd7c5becd19b56bfb50`, with script/audio content unchanged. Under the existing US$3.44 art-plus-music ceiling, generated only `md001`, `md010`, `md041` one take each (three images and three judges, ledger US$0.0405). Judge failed `md001` and `md010`; original-image review also found a modern motor ferry in `md001`, modern cabin/figure in `md010`, and a possible third ship in judge-passed `md041`. This is a cross-scene historical vessel/character error: **STOP paid art**, preserve all three 1280×720 images and manifest, obtain shared original-image review before any revised prompt pilot or wider batch. No storyboard, music or final cut. Precise paths, hashes, source delta and judge results: `docs/videos/curio-s42/verify-4.md`. Script and audio remain site pending; no owner approval inferred.
