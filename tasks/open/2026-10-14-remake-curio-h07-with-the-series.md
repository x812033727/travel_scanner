---
id: 2026-10-14-remake-curio-h07-with-the-series
title: Remake Curio H07 with the series look
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-14T16:10:29Z
completed_at:
branch: codex/curio-h07-v2-review-20261018
depends_on: []
scope:
  - docs/videos/curio-h07-v2
---

# Remake Curio H07 with the series look

## Why

The owner asked to fetch main, update the H07 branch and remake the episode under the new Curio series rules. The already approved `curio-h07` final was made with a custom adult editorial look and 59 illustrations among 99 body scenes. The new `curio-episode` lint requires the unchanged `cute-mystery` preset, at least 70% illustrated body scenes and no more than three cards in a row. Keep the approved original project and its media intact; produce the revision under the separate `curio-h07-v2` slug.

## Definition of done

- [x] The isolated H07 revision follows the fixed series look and passes `lint` with zero errors, including the illustration ratio and card-run checks.
- [ ] Its narration, illustrations, storyboard, final cut and selected en/ja/ko tracks have current source-bound evidence and pass their applicable review gates.
- [ ] The revised package and exact backend receipts are delivered for owner playback and private Studio upload; no publication is inferred from local QA.

## Steps

- [x] Fetch origin, rebase the H07 branch onto current main, guard PR #1497 against auto merge and audit the changed rules and active media state.
- [x] Design replacement shots and cards, verify historical claims, estimate image count and spending cap, and record the owner budget decision before paid generation. The owner approved a US$6 estimated cap; 65 new shots were drawn and their selected images reviewed.
- [x] Bring the isolated slug through narration and full-storyboard review. The script, source check, cache audit and 13-question blind review are complete; the script approval remains bound to unchanged `script.md`. Twenty-one zh-TW lines were synthesized and 93 clips transcribed; offline Whisper cleared seven of the initial 21 audio flags. The owner listened and accepted the remaining 14, and the latest audio card was approved and read back. All 65 shots have selected images, zero machine `needs_review` flags and three contact sheets; the manifest SHA `830A745F…28C1F7` storyboard card was approved and read back at 2026-10-18T10:01:07Z.
- [x] Render the approved storyboard, assemble the local 1080p final, make four-language captions and localized thumbnails, and run local final QA. `final.mp4` SHA `9B059CC5…ADD72` has 16,903 frames (about 9:23.4); `checks.json` is `ok: true`, caption manifests show zero problems and final QA passed 11/11. Manual `qa` and final `review-push` each called Jev once; both verdicts passed.
- [x] Finish the owner-selected en/ja/ko tracks and their audio QA, then package and submit upload/language reviews; keep Studio upload and playback as later owner actions. The final card for `final.mp4` SHA `9B059CC5…ADD72` was approved and read back on 2026-10-18. The owner selected metadata, captions and dubs for all three languages in the backend at 10:37:54 UTC, and this choice was synchronized into `languages.json`. All three 93-line tracks and first-pass QA exist; the owner listened to and accepted en, ja and ko despite 18, 36 and 14 first-pass flags respectively. After the owner freed C: space, `package` passed 4/4; `upload/metadata.json` SHA-256 is `CE7D19F615FD7170C3DAA26CA5E157ECD1A56270A1691EF17837FDAA4586236A`. The `publish` card was approved and read back; the `languages` card was submitted and read back pending owner Studio upload. No YouTube upload is inferred.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-h07-v2`, `check-audio`, `keyframes --dry-run`, `qa`, `package` and `review-push`/`review-pull` for the relevant gates. Inspect keyframe/contact-sheet receipts, exact audio/video frames, hashes, and the live `/admin/videos` review state. Run `npm run test:docs-videos` and `npm run check:tasks` before pushing. Keep YouTube Studio upload and publication as separate owner actions.

## Notes

- The original `curio-h07` backend project has an approved zh-TW final but no YouTube ID, upload readiness or publication. It must not be overwritten; the new rules require a fresh slug for an approved film's rewrite.
- Original H07 lint on main had six errors. The isolated v2 now has **65/92** illustrated body scenes (70.7%), 93 total lines and `lint` 0 errors/1 warning: the machine duration estimate is 8.9 minutes versus the 9–11 minute target. The 30 fps audio timeline measures **531.2 seconds of body narration** before the outro and 537.43 seconds total, so the body passes the eight-minute floor. Current `video.json` SHA-256: `F0060544216F7084C26677743BAE6AB139BBA6CA7D89836DB618791030D23502`. The assembled `final.mp4` is 16,903 frames / about 563.4 seconds, 1920×1080 at 30 fps, H.264/AAC stereo, -14.1 LUFS, with intro inserted at frame 1,670 / 55.67 seconds; SHA-256 `9B059CC58B3AA236558A895F96C3E443CA53CF3A0EFE086A6F3042BA746ADD72`.
- Old paid WAVs remain cached in the isolated workdir. The 2026-10-18 `tts` run synthesized **21/93** zh-TW lines (533 billable characters; 21 new WAVs total about 116.39 seconds). The first `check-audio` run transcribed **93** clips and called Jev **once**; a second pass reused cache (0 new transcription/0 Jev). Offline Whisper then rechecked the 21 flags with one additional Jev call and no new Gemini transcription, clearing seven and leaving 14 for owner listening; neither earlier audio QA nor approval transfers.
- All 59 old illustrations were compared with the series look; 0 were safe to reuse. The new manifest SHA `830A745F…28C1F7` selects **65/65** images, with zero machine `needs_review` and three contact sheets. Human retake review is recorded in `keyframe-qa-1.md`, `keyframe-qa-2.md` and `keyframe-qa-3.md`. The media ledger records 118 ready images, 117 judge calls and **US$1.5795** cumulative server-estimated image/judge cost; one earlier terminal failed image is conservatively reserved at US$0.0035. The owner approved a US$6 all-in estimated cap. Actual vendor charges for completed TTS/transcription/Jev are unavailable, so `review/spend-ledger.json` holds a **US$0.50 planning reserve, not an actual bill**; estimated headroom is **US$3.9170**. Verify before another paid stage.
- Outline approval is current. The owner authorized deleting `7c22ba05`; fresh independent historical review and 13/13 narrative blind review passed. Two spelling cards and five illustration prompts then changed without altering narration; see `verify-3.md`. Later illustration repairs changed only visual prompts, as recorded in the keyframe QA receipts. `review-pull` recorded script approval, and local `approvals.json` binds unchanged `script.md` SHA `6BC0B080…0EC48D29` at 2026-10-18T07:46:13Z. Prompt-only changes to `video.json` do not stale this narrative-bound approval. Audio and storyboard have separate gates.
- The owner accepted the 93-line, 8:57 narration after listening. The audio review card binds `timeline.json` SHA `D43D89BA…98670DF` and was approved/read back; the storyboard card binds `keyframes/manifest.json` SHA `830A745F…28C1F7` and was approved/read back. The two-transcriber pass made one additional Jev call and left 14 flags, none established as a wrong take.
- `render` first drew 28 slide states with 0 reused; `clips` selected 65 stills and 0 paid clip seconds. The localized thumbnail headlines changed only line breaks; the subsequent render reused all 28 states and produced en/ja/ko thumbnails. After three-language dub completion, `captions/manifest.json` records zh-TW 99, en 103, ja 109 and ko 107 cues, each with zero problems and each selected language timed to its dub. En line `0231d434` was shortened to fit its slot. Local final QA passed 11/11; manual `qa` and final `review-push` called Jev once each. The backend final card is approved and exact-SHA read back. The language panel selected en/ja/ko metadata, captions and dubs. The four-language upload package passed 4/4 locally; backend publish/languages approval, Studio upload and publication remain separate gates.
- `npm run test:docs-videos` again hit the unrelated `imported-long-languages/runner.test.mjs` Windows child exit `3221226505`; a targeted rerun of its `initial runtime freezing` case reproduced that failure after C: had over 8 GB free, so it is not the previous `ENOSPC` condition. The broad rerun was then stopped after this concrete failure. H07 lint (0 errors/1 duration-estimate warning), `npm run check:tasks` and diff check passed. Earlier attempts to remove old installer Temp directories and one H07 derived intermediate were rejected `blocked by policy`; no alternate deletion was attempted. The user later freed C: space, permitting a clean package.
- PR #1497 remains draft with `no-auto-merge`. The local finish worktree is on `codex/curio-h07-v2-finish-20261018`, rebased onto origin/main but not pushed. This task's review branch is `codex/curio-h07-v2-review-20261018`, stacked on PR #1497's exact head so the isolated remake can be reviewed without rewriting that branch. Do not merge, publish or treat private upload as public release without the later owner gates.
- Draft PR #1569 is the stacked H07-v2 review artifact and carries `no-auto-merge`. The owner said they will create the new private H07-v2 video in Studio later. When they return with its URL and four-language playback result, read back the linked backend video and the `languages` card before marking Studio delivery complete. This ticket was released to the shared queue while awaiting that owner action.
