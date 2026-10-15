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
- [x] Submit and read back the applicable backend document/script approvals; quote all new images and an episode cost ceiling once to the owner before paid generation.
- [ ] Produce, inspect and review the narration, illustrations, final cut, captions and package; check the expedition's latest primary update before finalizing a time-sensitive ending.

## How to verify

Check the current source hashes and `node tools/video/cli.mjs lint --slug curio-h09` when local source exists; run narrative, historical, audio, keyframe/contact-sheet, QA, package and `review-push`/`review-pull` gates for the chosen route. Inspect current `/admin/videos` persisted state and final media frames. Run `npm run test:docs-videos`, `npm run check:tasks` and relevant tooling checks before pushing.

## Notes

- At 2026-10-15 local time, current backend GETs found no H09/Earhart video or drama request. The cute-mystery one-off host route is enabled, MiniMax `image-01` is configured, and the only active request is for another work. No H09 request or paid work has been started.
- The independently reviewed H09 source is on `claude/curio-topic-bank-second-batch` commit `949bb91fc`, not yet on main. It reports 20 rows rechecked, 19 upheld and one partly refuted then corrected. Use it read-only and recheck drift before delivery.
- The H09 review predates Purdue's October 12, 2026 update: a 17-person team reached Nikumaroro to inspect the unverified Taraia lagoon anomaly. Primary update: https://www.purdue.edu/newsroom/2026/Q4/earhart-expedition-update-crew-arrives-at-nikumaroro-launches-critical-phase-of-amelia-earhart-plane-search/ . Treat that as an ongoing test, not a found aircraft; refresh before the script and again before final QA.
- The H08 card is not usable as-is: its claim that South Australia Police later announced Carl Webb's official identification conflicts with the latest located police statement reported by ABC on 2026-07-06; H08's topic-check task is claimed elsewhere. No H08 files are changed here.
- `docs/videos/curio-h09/claims.md` records H09-C01–C17; the primary sources require **350 nautical miles**, not the old card's 350 miles, and separate Deep Sea Vision's 2024 deep-sea rock from ALI's Taraia lagoon target. After Purdue's October 14 update and a chronological F-section rewrite, `verify-1.md` and `narrative-blind.md` PASS `script-draft.md` SHA `361ECEA6E3FFDF8283F7B3C1C325E1C9B83FA122E67AACB3C637A41BDCA11F83`; independent `visual-qa.md` PASS binds `video.json` SHA `F3159462A1B030FE197E2B35D552D6AE74B3EF40587B6C4ACDAE2842AE2766D2`. Purdue's latest located primary update is dated 2026-10-14: drone plus magnetometer/side-scan survey began, data await analysis, no object identification.
- Read-only live admin/settings audit on 2026-10-15: `drama_enabled=true`, `series_script_gate=true`, `auto_pick_look=true`, `auto_approve_storyboard=true`, `max_usd_per_video=US$200` shared across the drama route. The script gate can hold paid pictures, but approving it would allow automatic art under a cap far above H09's yet-to-be-approved batch amount. No H09 **automated one-off drama request** was created; planning/script AI in that route would also incur cost. Local `format:drama` with the pinned `image-01` model was used for controlled dry runs and a concrete image-batch quote, and only unpaid outline and script reviews were submitted; outline A and the formal script are both approved.
- On 2026-10-15 the local H09 source has 100 scenes (92 illustrated stills, 7 cards, one outro), 0 lint errors, 3 narrative warnings, formal `script.md` SHA `3B1ECF0743F7BD83333ED68E697219333E81BBDCF7392C92D976F62BA6627D4C`, 100 dry-run TTS requests for about 2,654 billable characters, and a 92-image quote of about US$1.24 first pass or US$3.73 for three attempts each; no H09 media spend. The updated outline A was approved on `/admin/videos` and recorded in `approvals.json` with matching brief SHA; the formal script was approved on `/admin/videos` and read back with matching SHA at approved_at=`2026-10-14T23:51:59.021Z`. At that checkpoint the H09 media budget was not yet approved; the later authorization is recorded below. `npm run check:tasks` previously passed; docs-video tests passed 214/215 with an unrelated Windows child-process crash in `imported-long-languages/runner.test.mjs`, repeated in isolation.
- 2026-10-15 再查 Purdue／PRF 官方最新仍是 10／14 水下測勘公告，尚無機體確認，現行劇本未因時效查核而變動。TTS 向 Gemini 送完整稿件的執行被 auto-review 拒絕（劇本核准未被視為明確的外部合成授權），沒有合成或費用；待站主明確授權後才可再試。
- 2026-10-15 live dry runs quote 100 Gemini Sulafat lines / 2,654 characters; official gemini-3.8-flash-tts rate implies about US$0.16 for an 11.2-minute first narration, with actual tokens/duration pending. The 92-image MiniMax image-01 batch at up to three takes is quoted at US$3.73 including judge. Proposed H09 authorization: narration up to US$0.50, whole image batch up to US$4.00, combined ceiling US$4.50; later authorized together with the separate Gemini transcription/Jev QA under the same total cap. Later languages remain out of scope. Shared US$200 server setting is not an H09-specific cap.
- 2026-10-15 owner then explicitly authorized sending the H09 script to Gemini Sulafat for 100 zh-TW lines and generating the whole 92-image MiniMax image-01 batch, with US$4.50 combined stop ceiling; separately authorized Gemini transcription and TypeSafe Jev audio QA within that same ceiling. First TTS exited 0: 100/100 lines, 2,654 billable characters, 10:57.933 narration, complete ffmpeg decode; estimated Google audio output cost about US$0.1480, actual text-input/billing unknown. Image media ledger remains US$0.00. One proven `say` duplication in h1j3jy6q was fixed without changing the approved body text; regenerated `script.md` SHA `7294FD9410349DCBA89347631DF46A551C8A6C570A58983BE11E58A073FA41D5` was re-submitted and then read back approved at 2026-10-15T00:10:29.529Z because the speech hash changed. The second TTS pass synthesized only 1/100 requests (28 characters), reused 99 cached paid takes, and produced a decodable 657.233-second narration; final dry-run has zero requests. Owner also authorized paid Gemini transcription/Jev QA under the same US$4.50 total ceiling. The 100-line QA completed with 20 ASR flags; owner listened and accepted the narration. Backend audio gate was read back approved at 2026-10-15T00:46:46.700Z, bound to timeline.json SHA dd46e9cc89c4bbc03c0500ba98aeb973b1d6328c6c3792cb0c56349d21bd8cf7. The paid image command was rejected by auto-review before execution because offline preflight quoted US$39.74 using the wrong image model and only the global US$200 cap existed. Images have not started. Ticket 2026-10-15-enforce-episode-local-video-media-cost owns the cost-control correction; do not retry the paid command until verified and resubmitted to review.
- Later 2026-10-15 checkpoint: the price and episode cap fix was pushed in PR #1503 at `5800dd6c2`, and the unchanged 92-shot paid command was accepted. A bounded first run generated 7 shots using 11 image and 11 judge calls, ledger US$0.1485 with zero pending reservations, then H09 `STOP` paused further work. Two shots exhausted three takes and still need review; cold inspection also rejected several judge-passed frames. Six shot prompts were revised without changing the approved narration or fixed look; current `video.json` SHA `C8EA0BB8352FFEE86A2B7D113D1256C86321045EE39C18A8D8E94381A70B5075`. See `visual-qa.md`. The first cost-control commit also exposed six Linux media integration assertions; fixes are local under the cost-control ticket and a separate narrow test ticket. Do not restart paid art until the follow-up CI is green; then run and inspect the revised seven-shot pilot before the remaining 92-shot batch. Provider invoice totals for completed TTS/QA are unavailable, so US$4.50 control remains list-price based.
