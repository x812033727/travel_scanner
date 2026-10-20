---
id: 2026-10-20-produce-meta-x05-local-concept-preview
title: Produce Meta X05 local concept preview
status: in-progress
priority: P2
area: docs
owner: codex-meta-x05-preview
claimed_at: 2026-10-20T17:41:40Z
created_at: 2026-10-20T17:41:37Z
completed_at:
branch: codex/brand-story-meta-x05
depends_on: []
scope:
  - docs/videos/story-everyday-meta-x05
---

# Produce Meta X05 local concept preview

## Why

The X05 Meta preproduction package is source-reviewed and has a draft PR, but it has no measured narration, illustrated footage, music, captions, or playable cut. The owner asked to continue making videos under the existing brand-story rules. Produce a local concept preview while keeping the official 5-second intro, 21-second outro, and YouTube Studio end-screen links explicitly pending.

## Definition of done

- [x] Measure the 30–60-second hook and at least eight minutes of substantive Sulafat narration; check every spoken line against the script. Human-ear review remains open on 23 flagged lines.
- [ ] Generate MiniMax `image-01` / `cute-mystery` images, reuse the account's previously generated X03 Lyria bed for this concept only, and make captions plus a reviewable local long-video cut within the US$25 all-in cap. Keep the official X05 music stage incomplete.
- [ ] Record actual media ledger, visual/audio QA, concept-bookend limitations, and local artifact hash; update draft PR without calling it a published film.

## Steps

- [x] Synthesize and machine-check 84 lines in the **pinned** `/workspace/.brand-video-workdir` project volume; export an indexed narration-review MP3 for the outstanding human-ear checks.
- [x] Measure a 50.67-second hook and 8:36.43 substantive body excluding the final three native closing lines; verify and import the X03 soundtrack under `review/local-preview/` without an X05 `music/manifest.json`.
- [ ] Complete exact-SHA source and two fresh independent blind reviews of v13, regenerate and check the ten changed spoken lines, then pilot approved object-based prompts. Generate 64 illustrated shots with MiniMax `image-01` and no more than three actual attempts per shot, render and assemble only passed images.
- [ ] Save local preview and handoff receipts; run video-doc tests, task checks, and diff checks before pushing.

## How to verify

Run `node tools/video/cli.mjs lint --slug story-everyday-meta-x05`, then use the paired CLI with `--workdir /workspace/.brand-video-workdir` and `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1` for `tts --dry-run`, `check-audio`, `keyframes --takes 3 --dry-run`, `music --dry-run`, `media-status`, `qa`, and `package` as applicable. Check actual `timeline.json` durations rather than prose estimates. Run `npm run test:docs-videos`, `npm run check:tasks`, and `git diff --check` for tracked files.

## Notes

2026-10-20: Paired site media status and dry-runs succeeded through the session proxy. The v10 64-shot image estimate is US$0.86 for one take or US$2.59 for three; the eight initial v9 requests already cost US$0.108. TTS used the site's monthly free tier. The formal `sothatswhy` branding selection is null and no package is installed here. The server's US$200 per-video cap is **not** the owner's US$25 cap; this task must check the local ledger and reserve all other paid costs. Monthly music quota showed one track remaining at 17:42 UTC, then **zero** before X05 could book a track; do not call fresh music generation.

The first two document/measurement shots failed all six attempts, with readable invented words or digits (`judge.scores.text = 0`). The next office-notice shot also failed twice. A `STOP` file in the pinned project volume ended the batch after eight paid image/judge pairs; no further requests were made. None of those rejected selected images may enter a preview. Visual v10 converted the two exhausted shots to source-backed native cards and replaced the remaining 64 prompts with physical objects and actions. The independent v10 source difference review passed, but blind reader O found one spoken table-of-contents transition and an early visual reveal. V11 fixed those; its exact-SHA source review passed, but two fresh readers both failed chapter linkage, one flagged a repeated line, and both found the fourth chapter title revealed RL's result too early. Their FAIL receipts remain in Git. V12 repaired those transitions and passed source review; reader P passed its story check, but reader O failed `no_recap`, and both found chapter or card visuals that revealed answers before narration. V13 removes the repeated product-P&L denial, gives the cost-driver question a direct answer, and moves four suspense payoff cards to the scene after each spoken answer. Ten Sulafat lines now need synthesis and rechecking before relying on the original 8:36.43 substantive-body timing. V13 needs a new exact-SHA source review and two fresh blind reads before `STOP` is removed. The local preview assembler and independent QA both reject any image whose selected judge did not pass, and check the MiniMax model, generation cache, paid receipt, image bytes, illustration share of at least 70%, and no more than three consecutive cards.

The local concept instead reuses the owner's paired-site X03 Netflix Lyria-3.5 bed, generated at 2026-10-20 15:05:42 UTC. Original MP3 SHA-256 `452887ff91f0f6956d350b9c902cc273b82cc3c1fdae9a7524e330ddcda7b2de`; original music manifest SHA-256 `174b3c0edc140db7e7f45264d4b9ccba1044660ece7d65a834c2c79e71383019`; original completed ledger row US$0.08. Its prompt and mix settings match X05. The tracked `local-preview-reuse-music.mjs` verifies those records and writes only `review/local-preview/reused-music.json` plus a copied MP3; official X05 `music/manifest.json` remains absent, and the local preview sidecar records provenance. This is a concept soundtrack, **not** newly generated X05 music or official music-stage completion.

A first TTS start mistakenly used `/workspace/.video-tool-home/mokaair-work/videos`, before the pinned workdir was identified. It was stopped after two Sulafat lines. That separate volume was preserved; its media ledger reported US$0.00, no images, no judge calls, and no music. The two audio takes are **not** being reused. The active TTS run now uses `/workspace/.brand-video-workdir`, which contains the earlier manually reviewed lexicon transaction `5b35f7fc-d370-4c39-a86a-19bb5bee11bf`.
