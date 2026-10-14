---
id: 2026-10-14-produce-curio-h09-amelia-earhart-episode
title: Produce Curio H09 Amelia Earhart episode
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h09
claimed_at: 2026-10-14T17:13:01Z
created_at: 2026-10-14T17:12:45Z
completed_at:
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09
---

# Produce Curio H09 Amelia Earhart episode

## Why

The owner asked for another 奇聞檔案局 episode after H07. H08 is still an unchecked candidate and its current card overstates official confirmation in the Somerton Man case. The next independently reviewed history topic is H09, Amelia Earhart's 1937 disappearance, on the concurrently owned topic-bank branch at commit `949bb91fc`. Produce H09 in its own `curio-h09` scope under the fixed `cute-mystery` series rules. Do not edit the other agent's `history-curiosity/topic-checks` or `topics.json` files.

## Definition of done

- [ ] A source-checked, narratively coherent H09 Chinese episode uses the fixed series look, at least 70% illustrated body shots and no more than three consecutive cards.
- [ ] The outline/script, audio, storyboard and final film have current source-bound evidence and their applicable owner/backend approvals; new art stays within one approved whole-episode cost ceiling.
- [ ] A checked upload package is handed to the owner. Private upload, publication and owner playback remain separately recorded, never inferred from local QA.

## Steps

- [x] Audit current worktrees, tasks, open PRs and backend for a conflicting H09 production; create an isolated branch/worktree and claim this narrow task.
- [x] Pin and independently refresh the H09 fact-check, including the October 2026 Purdue/Nikumaroro field expedition; record exactly which claims are archival fact and which are competing hypotheses.
- [x] Prepare the H09 brief, one-story outline, claim/source register, narration script, loops and visual plan under `docs/videos/curio-h09`; run lint and independent narrative/source reviews before paying for production.
- [ ] Submit and read back the applicable backend document/script approvals; quote all new images and an episode cost ceiling once to the owner before paid generation.
- [ ] Produce, inspect and review the narration, illustrations, final cut, captions and package; check the expedition's latest primary update before finalizing a time-sensitive ending.

## How to verify

Check the current source hashes and `node tools/video/cli.mjs lint --slug curio-h09` when local source exists; run narrative, historical, audio, keyframe/contact-sheet, QA, package and `review-push`/`review-pull` gates for the chosen route. Inspect current `/admin/videos` persisted state and final media frames. Run `npm run test:docs-videos`, `npm run check:tasks` and relevant tooling checks before pushing.

## Notes

- At 2026-10-15 local time, current backend GETs found no H09/Earhart video or drama request. The cute-mystery one-off host route is enabled, MiniMax `image-01` is configured, and the only active request is for another work. No H09 request or paid work has been started.
- The independently reviewed H09 source is on `claude/curio-topic-bank-second-batch` commit `949bb91fc`, not yet on main. It reports 20 rows rechecked, 19 upheld and one partly refuted then corrected. Use it read-only and recheck drift before delivery.
- The H09 review predates Purdue's October 12, 2026 update: a 17-person team reached Nikumaroro to inspect the unverified Taraia lagoon anomaly. Primary update: https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-crew-arrives-at-nikumaroro-launches-critical-phase-of-amelia-earhart-plane-search/ . Treat that as an ongoing test, not a found aircraft; refresh before the script and again before final QA.
- The H08 card is not usable as-is: its claim that South Australia Police later announced Carl Webb's official identification conflicts with the latest located police statement reported by ABC on 2026-07-06; H08's topic-check task is claimed elsewhere. No H08 files are changed here.
- `docs/videos/curio-h09/claims.md` records H09-C01–C17; the primary sources require **350 nautical miles**, not the old card's 350 miles, and separate Deep Sea Vision's 2024 deep-sea rock from ALI's Taraia lagoon target. After Purdue's October 14 update and a chronological F-section rewrite, `verify-1.md` and `narrative-blind.md` PASS `script-draft.md` SHA `361ECEA6E3FFDF8283F7B3C1C325E1C9B83FA122E67AACB3C637A41BDCA11F83`; independent `visual-qa.md` PASS binds `video.json` SHA `F3159462A1B030FE197E2B35D552D6AE74B3EF40587B6C4ACDAE2842AE2766D2`. Purdue's latest located primary update is dated 2026-10-14: drone plus magnetometer/side-scan survey began, data await analysis, no object identification.
- Read-only live admin/settings audit on 2026-10-15: `drama_enabled=true`, `series_script_gate=true`, `auto_pick_look=true`, `auto_approve_storyboard=true`, `max_usd_per_video=US$200` shared across the drama route. The script gate can hold paid pictures, but approving it would allow automatic art under a cap far above H09's yet-to-be-approved batch amount. No H09 **automated one-off drama request** was created; planning/script AI in that route would also incur cost. Local `format:drama` with the pinned `image-01` model was used for controlled dry runs and a concrete image-batch quote, and only an unpaid outline review was submitted.
- On 2026-10-15 the local H09 source has 100 scenes (92 illustrated stills, 7 cards, one outro), 0 lint errors, 3 narrative warnings, formal `script.md` SHA `3B1ECF0743F7BD83333ED68E697219333E81BBDCF7392C92D976F62BA6627D4C`, 100 dry-run TTS requests for about 2,654 billable characters, and a 92-image quote of about US$1.24 first pass or US$3.73 for three attempts each; no H09 media spend. The updated outline A was re-pushed to `/admin/videos` and read back as waiting for owner. Script review is not yet submitted, and H09 budget is not approved. `npm run check:tasks` previously passed; docs-video tests passed 214/215 with an unrelated Windows child-process crash in `imported-long-languages/runner.test.mjs`, repeated in isolation.
