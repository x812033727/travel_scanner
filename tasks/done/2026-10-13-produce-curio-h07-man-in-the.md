---
id: 2026-10-13-produce-curio-h07-man-in-the
title: Produce Curio H07 Man in the Iron Mask
status: done
priority: P2
area: docs
owner: codex-gpt6-curio-h07
claimed_at: 2026-10-13T23:14:55Z
created_at: 2026-10-13T23:14:51Z
completed_at: 2026-10-14T12:06:26Z
branch: codex/curio-h07-production-20261014
depends_on: []
scope:
  - docs/videos/curio-h07
---

# Produce Curio H07 Man in the Iron Mask

## Why

H07 (the Man in the Iron Mask) is the next independently checked Curio topic with no episode package. H04-H06 v2 and the five older recuts are owned by other active worktrees. This task creates an isolated, evidence-bound episode without touching their files or media.

## Definition of done

- [x] A sourced Traditional Chinese H07 script, visual plan, and upload metadata pass local checks and independent editorial review.
- [x] Narration, illustrations, captions, and an 8-minute-or-longer final cut pass the pipeline's audio, pace, and final QA gates.
- [x] Owner-facing preview/package and exact hashes are recorded; owner-controlled upload and publication remain separate gates.

## Steps

- [x] Confirm H07 is checked and unused; check worktree, task, and PR ownership.
- [x] Create and claim the isolated H07 task/worktree.
- [x] Write brief, source register, claims, original script, and visual plan.
- [x] Obtain an independent factual and listening review; correct only evidenced issues.
- [x] Run lint and a no-cost media preflight before any paid generation.
- [x] Run narration, audio review, image generation, render, assembly, captions, QA, and package within available authorized budgets.
- [x] Record all approval, backend, upload, playback, and publication states independently.

## How to verify

`node tools/video/cli.mjs lint --slug curio-h07`; then inspect `status --slug curio-h07`, the audio and media receipts under the external `VIDEO_WORKDIR`, `checks.json`, final MP4 duration, captions, and `package` output. `npm run check:tasks` verifies the task record. A private link or local preview alone does not finish owner playback or publication.

## Notes

- 2026-10-14 Taipei: H07 topic-check has 13 claim checks and an independent review. The 1703 Bastille record says black velvet; Voltaire used the iron-mask name in a 1738 letter. Identity, mask duration, and the first use of "iron" remain unresolved. We will omit the unverified 1687 manuscript detail from narration and use original illustrations plus only individually verified assets.
- H04-H06 v2 production is active in `curio-h04-h06-remake`; H05 `check-audio` and H06 TTS held live leases at 23:13 UTC. Shared image-judge usage was reported at 10,000/10,000, so no H07 paid image batch is queued pending a fresh limit check and an owner budget decision if still capped.
- 2026-10-14 Taipei: Outline A was selected. `verify-1.md` independently passed the 100-scene factual review; the blind narrative review passed all 11 checks. `lint` has zero errors and one non-factual outro warning. Gemini Sulafat synthesized 100 lines in 09:37; `check-audio` is still running, so narration approval is not yet claimed. The latest media-status before image generation showed MiniMax image-01 and remaining shared quotas; rerun it when the audio project lock clears. A three-shot visual pilot will precede the full image batch.
- 2026-10-14 Taipei: First `check-audio` completed 100/100 and flagged 27 for a bounded second transcriber check; these are not yet proven audio errors. The three opening keyframes cost US$0.04 and each received 9.29/10, but human visual review rejected their childlike clerk and East Asian architecture. `visual-prompts.json` and `look` were revised before any full batch; retake the same three shots after the audio check releases the project lock. The 215 `test:docs-videos` tests passed with bundled Node 24.19.0; system Node 24.13.0 had the previously documented Windows native child-process crash in an unrelated test.

- 2026-10-14 Taipei: The revised three-shot opening pilot was generated and visually inspected: the clerk now reads as an adult and the courtyard as French stone. Its current manifest has 3 of 95 illustration shots, so the next visual gate is a diverse 8-12-shot representative batch before the remaining illustrations. The media ledger currently totals US$0.16 for 12 images and 12 judge calls, including superseded pilot attempts; the original rejected files were overwritten, while a snapshot of the current revised pilot is retained under the external H07 work directory. Nine narration lines were rewritten for oral clarity and independently fact-checked, and four illustration prompts were changed to depict Voltaire/1771 material as printed transcriptions or book pages. The current video.json SHA-256 is `3458BF098352B773F92AD0479255326CF785BC8F98EA43D3083DDC4DCC1654AB`. TTS regenerated only those nine lines (194 billable characters; 91 reused), yielding 09:26 narration. Audio recheck is still running; neither audio approval nor full storyboard approval is claimed.
- 2026-10-14 Taipei: The 09:26 narration passed `check-audio`; four remaining speech-recognition flags were sent for owner listening. The owner replied 「試聽後核准」, and `review-pull --gate audio` recorded backend approval. No spoken lines were changed afterward. The current script builder has 100 scenes and 78 illustration shots. Precise quotations, years, identity comparisons and model-resistant visuals were converted into deterministic evidence cards, retaining claims and sources. The 16-shot second batch generated 24 paid takes; three illustration prompts failed all three judge attempts, so two became evidence cards and one was redesigned. The media ledger after that batch and a two-shot retake was US$2.20. More keyframes, full storyboard review, render, assembly, captions, QA, and package remain open. No YouTube upload or publication is claimed.
- 2026-10-14 Taipei final delivery: Current 100-scene edit uses 59 accepted illustrations and 41 rendered card/screenshot states. The owner explicitly approved the 59-shot storyboard after reviewing three contact sheets; backend storyboard approval binds `keyframes/manifest.json` SHA-256 `C06C34938FDBBB7F4D049DB07450E19AD841D45223328C9BD13C9212B2BA8A46`. The 9:26 narration approval remains bound to its own timeline. The 9:52.900 final MP4 (17785 frames, 1920×1080, 30 fps, AAC stereo) passed all 11 final QA items; the zh-TW package passed 4/4 checks. Backend final gate autoapproved the exact MP4 after QA; this is not owner playback acceptance. Separate spot-checking of 15 actual final frames across scenes 74–78, 87–91 and 95–99 found no cut-off text or black frames. Paid image/judge ledger totals US$3.348, including retakes. `npm run test:docs-videos` passed 215/215 with bundled Node 24.19.0; `npm run check:tasks` passed before final ticket close. See `docs/videos/curio-h07/delivery.md` for package contents, exact hashes and gate receipts. The owner has not yet selected locales (`decided_at: null`), and backend `ready_to_upload: false`; YouTube upload, actual player check, schedule and publication have not occurred.
