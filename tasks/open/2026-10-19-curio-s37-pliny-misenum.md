---
id: 2026-10-19-curio-s37-pliny-misenum
title: S37 Pliny at Misenum history episode
status: in-progress
priority: P2
area: docs
owner: codex-s37-r6
claimed_at: 2026-10-20T01:00:48Z
created_at: 2026-10-19T23:53:49Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s37
---

# S37 Pliny at Misenum history episode

## Why

The next Curio history episode asks whether Pliny the Younger witnessed the Vesuvian disaster from Pompeii. The pinned letters show a different position and distinguish his escape from his report of his uncle's last hours.

## Definition of done

- [x] Reopen and hash pinned LXV/LXVI, record claims and source limitations.
- [x] Draft options, chosen brief, 8+ minute screenplay, 75–120 still shots and loop map.
- [x] Pass video lint and relevant documentation checks.
- [x] Fresh independent 13 question blind read and final source/visual review of the **R6 exact hash** before any paid media; R5 blind read reached 12/13 with `no_recap` blocked.
- [x] Delegated local review records the **current exact script**, zero-flag audio, and whole episode media budget under the owner's standing instruction, without claiming personal owner review.

## Steps

- [x] Create research, brief, claims, `video.json`, generated `script.md`, and verification handoff under `docs/videos/curio-s37`.
- [x] Correct R1 independent source and visual findings; remove unsupported exact date and firsthand Pompeii imagery.
- [x] Rebuild the story in chronological intercuts after R1 found a long rewind, repeated leave-behind line, and non-event chapters; correct `pl002` cloud position, `pl037` pillow placement, `pl026` bag, and remove the premature `pl066` held hand.
- [x] Run an independent R2 13 question panel and full pinned-source/visual pass; preserve the 12/13 narrative failure and source/pass notes in `verify-3.md`.
- [x] Revise the R3 first sentence after `[pl033]` to answer the boy's sleep question, remove the stale `[pl053] -> [pl054]` loop, and apply the independent precision notes.
- [x] Run independent R3 script-only 13 question panel and full pinned-source/91-prompt audit; preserve the 11/13 narrative failure and four daylight contradictions in `verify-4.md`.
- [x] Rebuild R4 as the nephew's continuous Misenum route, then reveal the uncle's end as a short reported outcome after the return; correct all four afternoon prompts and source chronology notes.
- [x] Run independent R4 script-only 13 question panel and full pinned-source/91-prompt audit; preserve the 10/13 narrative failure and two source/prompt issues in `verify-5.md`.
- [x] Rebuild R5 as one continuous Misenum route with a short letter-writing conclusion, remove the opening discovery spoiler and immediate courtyard/Livy repetition; fix `pl036` source causation and `pl086` night lighting.
- [x] Run independent R5 script-only 13 question panel and full pinned-source/88-prompt audit; preserve the 12/13 narrative failure and `pl087` daylight hold in `verify-6.md`.
- [x] Revise R6 adjacent building/crowd repeats as sequential dawn, hazard, departure, and pushing beats; correct `pl087` to night light and tighten mother's motive in `pl110`.
- [x] Run a **new R6** script-only 13 question panel and full pinned-source/88-prompt pass against the exact new hashes.
- [x] Run a fresh R7 script-only 13 question panel and full pinned-source/88-prompt audit after eleven audio wording repairs; narrative passed 13/13 but source audit found an attribution blocker, so no R7 TTS or script approval.
- [x] Run fresh R8 script-only 13 question panel and full pinned-source/88-prompt audit after the source precision repair; independently confirm the two R8a metadata payoff fixes before renewing exact-script approval and TTS.
- [ ] Complete audio, stills, music, cut and QA only after gates and budget review.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-s37 --json`, `npm run test:docs-videos`, and `npm run check:tasks`. The blind reader receives only `node tools/video/cli.mjs narrative --slug curio-s37` output, then submits answers from a fresh session. Source/visual reviewer compares every line and prompt to the fixed GITenberg letters. See `docs/videos/curio-s37/verify-1.md`.

## Notes

2026-10-20 R6 gate: the new independent blind reader passed 13/13 official narrative questions and the source/visual reviewer passed 91/91 claims plus 88/88 written prompts on the exact R6 hashes. Their full reports are `verify-7-r6-blind.md` and `verify-7-r6-source.md`; `verify-7.md` records the formal line-cited `narrative --answers` pass and the delegated local outline A and script approvals. The approval notes cite the owner's standing instruction to take recommended choices and continue; they do not claim the owner personally read S37. Gemini Sulafat TTS completed 89 requests/2,220 characters and measured 9:32.77 total, with **8:38.13 actual story body** excluding opener and outro. Site dry-runs quote 88 MiniMax images up to three takes **US$3.56** plus 578-second music **US$0.08**, a pre-art whole-episode image-and-music hard cap of **US$3.64**; both currently US$0.00 spent. Full `check-audio` is underway. No MiniMax image generation has begun; zero audio flags, shared S04/S23 hourly quota and branded intro/outro remain separate gates. Earlier failed rounds remain in `verify-2.md` through `verify-6.md`.

2026-10-20 R7 audio repair: R6 full checks ended with 31, 12, then 11 flags despite two targeted retakes; `review/check-flags.json` still held `pl008, pl009, pl020, pl017, pl051, pl052, pl055, pl026, pl059, pl085, pl099`. R6 audio is **not approved**. Only those eleven spoken lines were rewritten to simpler source-equivalent wording in `video.json`, `claims.md` and regenerated `script.md`; no prompts changed. [verify-8.md](../../docs/videos/curio-s37/verify-8.md) records each edit and the R7 hashes: script `b8c6cca751dc9801d09f8f4cb17b632e73cd7cf5b9ece13094c7550511490359`, video `31eb25bf7130bbcbd1e1a6f9f0bfbe78154dcf13d527e27738ea5dd4a05c7de2`, claims `2beae04c177796443055a56e0c6ef10e1a40b5163e4b812cdfe0b3a5b9d6730a`. Lint is 0/0; 91/91 text/claim alignment. A fresh context-isolated reviewer is now doing R7 blind and source/prompt audit. No R7 TTS or art before that result; R6 script approval, narrative record and measured timeline are stale for R7.

R7 review returned 13/13 blind story Yes but a source **blocker** at `pl020`: the rewritten pronoun could make the uncle the writer of the letter. The same reader asked to clarify `pl003`'s singular letter, remove `pl029`'s unsourced reported slow walk and `pl057`'s specific wheel support, and tighten five prompt details. The full result is `verify-8-r7-source.md`. No R7 TTS was ordered. R8 applies those four spoken and five prompt repairs; [verify-9.md](../../docs/videos/curio-s37/verify-9.md) records the ledger. A new isolated reader sealed 13/13 blind Yes and passed 91/91 claims and 88/88 written prompts, but asked to correct two loop-payoff metadata values. R8a changes only those two values; an independent exact-diff readback passed all 22 loop mappings. Current SHA-256: script `a838e16572f4a40c3d79c5874087900a8e8b808fceb35db9a03642bcc3412a62`, video `8d4b1a2c4cc85dad3e5f500eff643c4a7d7ecc70998443097e3a62c58f72a51c`, claims `ce7491625af59f27549fe4621e18917082946602474a99c1ea72e4f9f27d997a`. Lint remains 0/0; 91/91 alignment and 88 prompts. The written gate passed; image generation remains on hold for S04/S23 quota.

R8a production: the formal narrative importer passed 13/13, and local delegated outline A and exact-script approvals were renewed with explicit notes that the owner did not personally read S37. TTS synthesized 14 changed requests/329 characters, reused 75, and produced a 575.2-second timeline. The measured body from `pl007` to `pl099` is **519.5 seconds (8:39.5)**. Full `check-audio` checked 91/91, with 68 exact, 12 same-sound/filler, 11 accepted, **0 flags**. The audio gate was submitted to the site as pending owner decision; a local delegated audio approval records that the owner has not personally listened. Before art, the 88-still three-take image cap was quoted **US$3.56** and 581-second music **US$0.08**, whole-episode image-plus-music **hard cap US$3.64**. Gemini Lyria generated the quoted 581-second music for **US$0.08**; MiniMax S37 spend remains **US$0.00**, leaving **US$3.56** inside the cap for images. Its generation is held for the shared S04/S23 quota. The final brief hash `2e071d27805a68d2090e16686f7c7b649d43fab79f481ba3954fd910243df3a4` received renewed local delegated outline A approval and site pending submission. [verify-10.md](../../docs/videos/curio-s37/verify-10.md) records exact hashes and receipts; final media remains blocked by branded intro/outro installation.

R6 addresses only the remaining R5 blockers and its small source precision note. The opening and sole nephew route are unchanged. `[pl054]` shows the uncertain dawn light, `[pl025]` the hazardous shaking buildings, `[pl055]` mother and son leave, and `[pl026]` the crowd presses them; this removes the two adjacent repeated beats found by the blind reader. `[pl087]` remains in the anxious night under oil-lamp light; `[pl110]` now states the mother's reluctance to cause her son's death without claiming she literally saw his future safety. The independent R5 audit and R6 correction ledger are in `verify-6.md`.

R6 has 91 aligned spoken lines/claims, 88 still prompts, 22 ordered loops and 8 event chapters; estimated total 9:21.2 and story body 8:24.93. Lint 0 errors/0 warnings; no new paid media or quote. Exact SHA-256: script `40f08a2c803462115895102ab91cfbd192f209bd766a8bc070495c1b27cecc1f`; video JSON `b9a5576809829ca60bb1388fca3bf387cf3a453c8498638101ac27620e2e4af4`; claims `bf58eec85d6579dc06ab20a9f6a35c396b777fe816f6aa5b5a3377577c412a7d`. The pinned English translation remains SHA-256 `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` at GITenberg commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`.

R5 removes R4's opening body-discovery spoiler and the second chronological uncle track. After the uncle departs, the plot follows the nephew and mother through Misenum; the later writing desk conveys only the reported outcome, third-day discovery, conjectured cause, and source boundary. It removes the duplicate courtyard position and places the boy's continued Livy reading only after the visitor's rebuke. Source-backed additions are study until bathing, prepared chariots and pause beyond the houses, and the night prediction runners. `pl036` no longer claims ash caused weakened eyes; `pl086` now uses night oil-lamp light. The independent R4 audit and R5 correction ledger are in `verify-5.md`.

R5 has 91 aligned spoken lines/claims, 88 still prompts, 22 ordered loops, 8 event chapters; estimated total 9:23.37 and story body 8:27.1. Lint 0 errors/0 warnings, docs-video tests 236/236. New keyframes dry-run could not reach the quote endpoint, so there is no R5 media quote and no generation. Exact SHA-256: script `8a829acacf47da294a6fbd94ecd8e21527ced6362bbef6ca4db16974ea406db0`; video JSON `569b86421281b05ffee663d96f1010daf5d4e066ffaa66b03394a150e18eebcd`; claims `ebf270fe19d7bc8d50a80f895c57d6f018bcd3dc4f8ecf4fe6787de1067ce7e9`. The pinned English translation is unchanged, SHA-256 `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` at GITenberg commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`.

R4 narrows the on-screen timeline to one path: after the uncle's ship leaves, the plot stays with the nephew and mother from the Misenum earthquake through their return. When Tacitus later asks about the uncle, a short letter-bound report resolves the opening ship/body questions. The repeated witness-location assertions at old `[pl042]`, `[pl044]`, `[pl090]` are gone; only `[pl089]` attributes the beach discovery to near-time hearsay. All four afternoon `pl007/pl009/pl015/pl018` prompts now say afternoon; the old cross-bay instant chronology is no longer implied. The uncle's wake-up actor is omitted, sulfur smell explicitly precedes flames, and third-day body timing is tied to the uncle's fall. R4 has 94 aligned lines/claims, 91 still prompts and 21 ordered loops; estimate total 9:30.2 and story body 8:32.3. Lint 0 errors/0 warnings. Keyframes dry-run still quotes US$1.23 for one MiniMax take and US$3.69 at most for three; no generation occurred.

R4 exact SHA-256: script `1827212ba8c33a67df660ab6b8f9b20f86ddada9e4c1aba963cb5cb4deeb2836`; video JSON `3119b930da51bacf85002a8268af301bd66c237ac5659d8fabbbf6a59d752e16`; claims `80436b3cebc71c08eff7b1717302ae73caf2e5534fbabe5de35fc83ce91e88bb`. The pinned English translation remains `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` at GITenberg commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`. No TTS or paid imagery/music ordered.

R3 corrects the only remaining R2 narrative blocker: the new chapter's first line `[pl047]` now directly answers `[pl033]` before asking about the stronger quake, which `[pl048]` resolves. The loop table now has 21 valid entries; the stale `[pl053] -> [pl054]` entry is gone. The R2 source/prompt auditor found no historical blocker among 94 lines or 91 images, only five line-precision and three illustration-precision notes; R3 addresses all eight without changing the story outcome. `lint` is 0 errors/0 warnings; estimated story body is 513.7 seconds (8:33.7). R3 script SHA-256 `91697aaab93400a16b226308a3b45aee35e14bacadec53ca20f3711a5d956cc5`; video JSON SHA-256 `fd2e427bee1caff84dfe005cf4485bcedbbb38352db11244a30b7de1f2d4730c`; claims SHA-256 `21541e383cdbdc6249aac6b4c78c17701ddc4920342c8851820529a3eba0e68f`. No paid media has been ordered for this version.

R2 reorganized the 94 lines in two-bank night and morning order, with 91 still prompts and 22 declared open loops; it no longer finishes the uncle's death and then rewinds to the nephew's departure. `pl047`, `pl046`, `pl020`, and `pl092` add only details present in the pinned LXV/LXVI letters (earlier tremors, his own doubt about reading Livy, the cloud's changing colour, and his own fear). The current `keyframes --dry-run --takes 3` quote is 91 stills, US$1.23 for one pass, US$3.69 at three takes; **no image generation or other paid media was run**. Music quote is unavailable before TTS timeline creation. Lint is 0 errors/0 warnings; local docs-video tests passed 236/236 and task check exited 0 with pre-existing and temporarily overlapping S37-review task warnings. Estimated body excluding opener/outro is over eight minutes, subject to real TTS measurement.

R2 SHA-256: `script.md` `06b5ed9b368b0d9fed3f22bd1fbb88897fb6e1f44b87a092fd1002bb6b91b71c`; `video.json` `c8e03ce56afa489a4669dd47573f9ce79556cdad46bbb38dc46431ba9c12bd19`; `claims.md` `4ceafd1a13008d46d6bba3624b1943e83540a83208c2d10559cf3d49cf072286`. The 94 claim rows exactly match the 94 spoken lines and line IDs in JSON, in playback order. Pinned English translation text remains `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995` from commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`.

The 2026-10-20 preproduction JSON SHA-256 is `0a39ca65fd132a03b836597bdbd624f125ae79f2948812ab088323a75a8ce1bd`. Source text SHA-256 is `9f5fd6bc997d9386987a0d5ae184961f2c0f88f9a8912baa0cd7848687da4995`; commit `959ded9fab0f9d54768d2dbfad860b79c864c4c8`. The source is a Melmoth/Bosanquet English translation, not collated Latin. It prints 24 August but manuscript date variants are unresolved for this production, so the spoken script gives no exact date. Elder Pliny's Stabiae final moments are reports, not the nephew's eyewitness experience; cause of death is explicitly his conjecture. No paid media has been ordered.
