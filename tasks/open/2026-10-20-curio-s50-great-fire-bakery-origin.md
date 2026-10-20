---
id: 2026-10-20-curio-s50-great-fire-bakery-origin
title: Curio S50 Great Fire bakery origin sourced preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T15:02:41Z
completed_at:
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s50
---

# Curio S50 Great Fire bakery origin sourced preproduction

## Why

The next Curio history long video needs a distinct, sourced story. S38 already follows Pepys evacuating possessions during the Great Fire; S50 asks the narrower question whether the baker's oven can be blamed for “destroying London.” A preproduction draft must keep the recorded starting house, unknown ignition method, and conditions that spread the fire at different evidence levels.

## Definition of done

- [x] A recommended A/B brief, line cited research and claim map, Traditional Chinese 8+ minute body script, and matching Curio `video.json` exist under `docs/videos/curio-s50`.
- [x] The R1 and R2 exact content hashes, author only checks, lint result, and known source access limits are recorded in `docs/videos/curio-s50/author-selfcheck.md` and `docs/videos/curio-s50/review/r2-author-freeze.md`.
- [x] An independent R2 source/written-visual review and two different blind readers assess the same pinned R2 script hash.
- [x] Apply the R2 narrative FAIL corrections and freeze the R3 content; R3 independent source review found a narrow HOLD and R4 author repaired it.
- [x] Obtain an independent R4 narration/written-visual differential review; all three repaired lines and the revised booklet prompt PASS, but research metadata has a narrow HOLD.
- [x] Corrected the contradictory `research.md` boundary sentence; an independent reader passed its exact differential recheck.
- [x] Obtain two new script-only blind reads before site outline/script approval (generic-instruction isolation caveat recorded in R4 panel receipt; site cards remain pending).
- [x] Preserve one exact R4 full Jev policy FAIL, then freeze R5 author candidate: neutral spoken source-link outro, stale brief surveyor wording corrected and channel URL added.
- [ ] Independently recheck exact R5 source/brief/written-visual differential, ask two new script-only readers, and run one new full policy request only if those gates pass.
- [ ] The site and production gates accept the revised script and completed video, including measured TTS body duration and final 16 second Studio end screen links.

## Steps

- [x] Read series skills, compare S01–S49 topics, and keep S50 separate from S38/P17.
- [x] Read pinned Pepys, 1667 testimony booklet and Vincent text; cite exact lines and raw byte hashes.
- [x] Draft A/B, recommend A, write 116 scene story, 119 spoken lines and matched claim rows.
- [x] Fix Pepys Tower sequence and narrow witness/fireline claims after a read only source audit.
- [x] Run lint and exact text mapping; write author selfcheck and hash manifest.
- [x] Address all R1 independent HOLD findings in script, claims, research and written illustration prompts; freeze R2 hashes and rerun author checks.
- [x] Obtain independent R2 decision on the same five content hashes in `review/r2-author-freeze.md`; do not treat author corrections as approval.
- [ ] Reopen Gazette and London Museum from a network that allows them; review `fire037` and `fire108` and all other source boundaries independently.
- [x] Obtain two blind narrative reads on the same R2 hash and record the formal merged verdict.
- [x] Repair the five jointly failed narrative criteria and freeze R3 author files.
- [x] Obtain an independent R3 source/written-visual review; it identified three surveyor overreaches.
- [x] Repair the three R3 surveyor overreaches in R4 and freeze all five content hashes.
- [x] Obtain an independent R4 source/written-visual differential review; repaired narration/visuals PASS, research metadata narrow HOLD.
- [x] Obtain another reader's research-only recheck; the one-line differential passed.
- [x] Obtain a fresh script-only two-reader narrative panel; then route site outline/script review.
- [x] R4 full Jev explainer policy request failed sponsored 0.33; preserve response and avoid retrying the identical payload.
- [x] Author R5 changed only the spoken outro, claims purpose, two stale brief phrases and description channel URL; freeze new five-file hashes.
- [ ] R5 independent source/brief/visual differential, fresh script-only two-reader panel, site card rebinding and new full Jev policy request.
- [ ] Plan and authorize full media budget before TTS, MiniMax images or music; complete downstream audio, storyboard, final and Studio checks.

## How to verify

From the repo root, run `node tools/video/cli.mjs lint --slug curio-s50 --json`, then `sha256sum docs/videos/curio-s50/brief.md docs/videos/curio-s50/research.md docs/videos/curio-s50/claims.md docs/videos/curio-s50/video.json docs/videos/curio-s50/script.md` and compare with `review/r5-author-freeze.md`. Compare all 119 JSON spoken lines against the same IDs in `claims.md` and in order against `script.md`. `npm run check:tasks` validates this ticket; preexisting stale claim and scope overlap warnings elsewhere do not fail it. Later, measure the generated TTS body from after the first 8 scenes to the last story scene and inspect the 21 second outro, with Studio links active during its last 16 seconds.

## Notes

- 2026-10-20: [R4 official narrative panel](../../docs/videos/curio-s50/review/r4-official-panel.md) **PASS 13/13** on exact script SHA `81766925948a74b1915ae86754e1ca01db1c187c3cdd092d73970e2137435e23`; both independent answers, merged verdict, CLI answer/payload and CLI `narrative --answers` PASS are preserved. A read the generic narrative code preamble before the fixed panel and B read the developer-mandated generic cloud setup skill; neither read S50 episode materials besides the script before answering. The site row was registered report-only as `explainer`/`drama`; outline and script cards are both **hand_pushed pending**. Local delegated approvals record recommended A and the exact R4 script, expressly not website approval. [One full Jev explainer policy request](../../docs/videos/curio-s50/review/r4-policy.md) **FAIL**: sponsored 0.33 > 0.30, with stance 0.79, demo N/A, advice 0.01. Jev did not name a sentence; do not infer the cause from the score or resubmit unchanged text. No TTS, audio check, art, music or film was started. Author must decide any justified revision, then rebind all affected gates. Released for the next owner; media remains blocked by this policy failure.
- 2026-10-20: [R4 independent source/written-visual review](../../docs/videos/curio-s50/review/r4-source-independent.md) found `fire008/073/078` and the repaired `fire073` prompt **PASS** against A L147–170; all 119 IDs and words align, lint 0/0. The **source package remains HOLD only for an older `research.md` boundary sentence** claiming surveyors did not count unburnt city area, although A L153–164 explicitly lists 75 acres 3 roods unburnt within the walls. Replace that sentence with the report's narrow source-faithful wording, freeze the new research hash, get another reader's differential recheck, then run two genuinely fresh script-only blind narrative reads. Gazette/Museum remain P17-derived because origin access is blocked; no media or site approval.
- 2026-10-20: [R4 author freeze](../../docs/videos/curio-s50/review/r4-author-freeze.md) narrows `fire008/073/078` to the **printed surveyor totals** and removes the pictured ruler; brief/research stay at R3 hashes. R4 `video.json` SHA `0fa7b40caee68e8d475827ca551d14b15eac14d7f85fec68c0497cd4f80d7a1f`, `script.md` SHA `81766925948a74b1915ae86754e1ca01db1c187c3cdd092d73970e2137435e23`, `claims.md` SHA `41ebfffe54f72c0fda9f1fd563d90613efb2dbb6757e2d49a8f2e832558b4805`. Lint 0/0 and all 119 lines align; estimated cold open 39–48 s and body 8:40–10:43 depending speech rate. Independent R4 differential source/visual review and new script-only double blind remain gates. No media/site claim.
- 2026-10-20: [R3 independent source/written-visual review](../../docs/videos/curio-s50/review/r3-source-independent.md) found a narrow **HOLD** in `fire008/073/078`: A L148–168 prints surveyors' totals but does not date their fieldwork or give a ruler method; R3 narration and `fire073` prompt add those details. All other changed primary-source claims and written visuals passed direct pinned-text checks, with Gazette/Museum still P17-derived. Author should make the three-line/minimal-prompt repair, regenerate `script.md` and `claims.md`, then request independent differential review and fresh blind panel on the final hash. No site/TTS/art gates yet.
- 2026-10-20: R3 author revision is frozen in [R3 author freeze](../../docs/videos/curio-s50/review/r3-author-freeze.md). It repairs the five shared R2 narrative No findings in the script and records exact five-file hashes, diff, 119-line mapping, clean lint and timing estimates. The R3 independent source/written-visual check, two fresh blind readers, and subsequent site/media gates remain pending; this author record does not approve them.
- 2026-10-20: The two-reader [R2 official narrative panel](../../docs/videos/curio-s50/review/r2-official-panel.md) used a byte-identical CLI payload (SHA-256 `5fabb78e84a137064916b175771586145ea08b51bed5e8200fe20de51a64688a`) on the five frozen R2 content hashes. Both readers scored 8/13 Yes, agreed on all 13 questions, and jointly failed five required criteria: `no_spoiler`, `one_line`, `chapters_link`, `payoffs`, `no_recap`. `mergePanelVerdicts` therefore returns **FAIL**. Raw answers and full merged result are saved beside the report. Script/site/media work must wait for R3 corrections and a new panel; R2 source review's limited PASS does not override this narrative FAIL.
- 2026-10-20: Independent R2 review is `docs/videos/curio-s50/review/r2-source-independent.md`: the three pinned primary texts and all five frozen R2 hashes match; direct primary-source claims and all written visuals PASS after the R1 fixes. All 119 spoken lines match across JSON, claims and script; video lint has 0 errors and 0 warnings. Gazette issue 85 and London Museum remain P17-derived, not directly reverified here (prior proxy CONNECT 403); their direct source check and all downstream gates remain open.
- 2026-10-20: At the author selfcheck stage, preproduction was complete. The content hash table and source byte hashes are in `docs/videos/curio-s50/author-selfcheck.md`. Independent review followed as recorded above; blind review, website approval, TTS, illustrations, music, upload and Studio work remain undone.
- Pepys diary, the 1667 printed testimony and Vincent's account were downloaded at fixed Git commits and read directly. London Gazette issue 85 and London Museum were blocked by the proxy's CONNECT 403 before an origin response. Their limited wording relies on repository P17 research from 2026-10-12 and must be checked afresh from the original sites. `fire037` cites Gazette and `fire108` cites Museum; do not label them directly verified today.
- A is the recommended local outline. At 250/300/325 CPM, the planned 8 scene cold open estimates 50.1/43.0/40.5 seconds and the later story body 624.9/537.4/506.2 seconds including scene pauses. Actual TTS duration remains a gate.
- Three card scenes are `fire029` (Pepys address), `fire079` (13,200 houses), and `fire095` (Farriner testimony). Other story scenes are illustrative `shot`; do not present them as historical images. Put the original 5 second intro after chapter one, use the shared 21 second v4 end screen, and set Studio elements to the final 16 seconds.
- 2026-10-20 R1 independent source and written-visual review is `docs/videos/curio-s50/review/r1-source-independent.md` and concluded **HOLD**. Author repaired its listed items in R2; exact new hashes and author evidence are in `review/r2-author-freeze.md`. R2 still requires independent re-review; no PASS is claimed. The Gazette and Museum failures were proxy CONNECT 403, not HTTP responses from the sites.
- 2026-10-20: Author changed only the one `research.md` semantic-boundary sentence to reflect A L153–164's burned and unburned measurements; [narrow author receipt](../../docs/videos/curio-s50/review/r4-research-boundary-author.md) records new research SHA `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95`. Script/video/claims hashes stay R4. Another independent reader must validate this one-line diff before source-package PASS; two fresh script-only narrative reads and all media gates remain pending.
- 2026-10-20: A separate reader [passed the exact research-only differential](../../docs/videos/curio-s50/review/r4-research-diff-independent.md). Pinned A L153–164 lists burned area, unburned area within the walls, and 13,200 burned houses in the same printed passage. The sole research line now matches it (SHA `27f9df563ab8376d2f6ee10837772821534515fd29b86b7e83e259eb56023a95`); R4 script/video/claims hashes remain unchanged. The research metadata HOLD is lifted; fresh script-only narrative double blind and all media/site gates remain pending. Gazette/Museum remain P17-derived until direct access works.
- 2026-10-20: [R5 author freeze](../../docs/videos/curio-s50/review/r5-author-freeze.md) addresses the unexplained R4 sponsored-policy FAIL as a hypothesis, not a diagnosed cause: `fire999c` now points to the already listed fixed Pepys/1667 booklet links instead of asking for spoken subscription. Visual `outro.data.cta` remains subscription. The same narrow edit also removes R3's unsupported surveyor street-entry wording still left in two `brief.md` phrases, and adds the channel URL to the YouTube description. Brief SHA `bac9d05082626689833057f30718c0f9d6d798562460335c8bcb834216ed1a3b`, video SHA `f994e4fee7268364caf049d3fd4a69e00011b06991c77acff03919b5e21ecc67`, script SHA `009d4ed8204dcd541fc7cfb05cad73d3081ae75fb96a2f9faa71d4361b0a7ad8`; 119/119 aligned, lint 0 errors/1 disclosed outro warning. R4 source/panel/site/local decisions do not auto-approve changed R5 hashes. Require independent brief/source/visual diff, two new script-only readers and one new full Jev policy before TTS. No paid media, upload or clickable Studio links.
