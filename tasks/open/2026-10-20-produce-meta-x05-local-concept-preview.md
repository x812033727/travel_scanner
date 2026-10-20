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

- [x] Measure the 30–60-second hook and at least eight minutes of substantive Sulafat narration; machine-check every spoken line against the script. Human-ear review remains open on 24 flagged lines.
- [ ] Generate MiniMax `image-01` / `cute-mystery` images, reuse the account's previously generated X03 Lyria bed for this concept only, and make captions plus a reviewable local long-video cut within the US$25 all-in cap. Keep the official X05 music stage incomplete.
- [ ] Record actual media ledger, visual/audio QA, concept-bookend limitations, and local artifact hash; update draft PR without calling it a published film.

## Steps

- [x] Synthesize and machine-check 84 lines in the **pinned** `/workspace/.brand-video-workdir` project volume; export an indexed narration-review MP3 for the outstanding human-ear checks.
- [x] Re-measure the v14 50.67-second hook and **8:23.37 substantive body** excluding the final three native closing lines; verify and import the X03 soundtrack under `review/local-preview/` without an X05 `music/manifest.json`.
- [x] Complete exact-SHA source and two fresh independent blind reviews of v14; regenerate eleven changed spoken lines and machine-check all 84.
- [x] Pilot three v14 object-based prompts with one MiniMax `image-01` take each; inspect every generated image. Two failed the judge, and the third needs visual review; retain the paid-generation STOP.
- [x] Replace only those three prompts in v15 and freeze the exact JSON hash; await root's independent visual-only delta review before a bounded new pilot.
- [ ] Resolve visual defects and 24 human-ear narration flags. If prompts or narration change, repeat the corresponding exact-SHA independent reviews. Only then complete the 64-shot illustrated set (at most three actual takes per shot), render, and assemble passed images.
- [ ] Save local preview and handoff receipts; run video-doc tests, task checks, and diff checks before pushing.

## How to verify

Run `node tools/video/cli.mjs lint --slug story-everyday-meta-x05`, then use the paired CLI with `--workdir /workspace/.brand-video-workdir` and `NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1` for `tts --dry-run`, `check-audio`, `keyframes --takes 3 --dry-run`, `music --dry-run`, `media-status`, `qa`, and `package` as applicable. Check actual `timeline.json` durations rather than prose estimates. Run `npm run test:docs-videos`, `npm run check:tasks`, and `git diff --check` for tracked files.

## Notes

2026-10-20: Paired site media status and dry-runs succeeded through the session proxy. The v10 64-shot image estimate is US$0.86 for one take or US$2.59 for three; the eight initial v9 requests already cost US$0.108. TTS used the site's monthly free tier. The formal `sothatswhy` branding selection is null and no package is installed here. The server's US$200 per-video cap is **not** the owner's US$25 cap; this task must check the local ledger and reserve all other paid costs. Monthly music quota showed one track remaining at 17:42 UTC, then **zero** before X05 could book a track; do not call fresh music generation.

The first two document/measurement shots failed all six attempts, with readable invented words or digits (`judge.scores.text = 0`). The next office-notice shot also failed twice. A `STOP` file in the pinned project volume ended the batch after eight paid image/judge pairs. None of those rejected selected images may enter a preview. Visual v10 converted the two exhausted shots to source-backed native cards and replaced the remaining 64 prompts with physical objects and actions. The independent v10 source difference review passed, but blind reader O found one spoken table-of-contents transition and an early visual reveal. V11 fixed those; its exact-SHA source review passed, but two fresh readers both failed chapter linkage, one flagged a repeated line, and both found the fourth chapter title revealed RL's result too early. Their FAIL receipts remain in Git. V12 repaired those transitions and passed source review; reader P passed its story check, but reader O failed `no_recap`, and both found chapter or card visuals that revealed answers before narration. V13 removed the repeated product-P&L denial and moved four suspense payoff cards behind their spoken answers. Its exact-SHA source review and blind O passed; blind P failed `no_toc` for 「回到開場」 and found four more same-scene numeric reveals. V14 turns that callback into a report fact and shifts those four number cards behind their spoken answers, keeping the Shorts source shot IDs and the 64-shot/20-card count. Its source and two blind reviews subsequently passed, and its changed audio was synthesized and measured as recorded below. The local preview assembler and independent QA both reject any image whose selected judge did not pass, and check the MiniMax model, generation cache, paid receipt, image bytes, illustration share of at least 70%, and no more than three consecutive cards.

The local concept instead reuses the owner's paired-site X03 Netflix Lyria-3.5 bed, generated at 2026-10-20 15:05:42 UTC. Original MP3 SHA-256 `452887ff91f0f6956d350b9c902cc273b82cc3c1fdae9a7524e330ddcda7b2de`; original music manifest SHA-256 `174b3c0edc140db7e7f45264d4b9ccba1044660ece7d65a834c2c79e71383019`; original completed ledger row US$0.08. Its prompt and mix settings match X05. The tracked `local-preview-reuse-music.mjs` verifies those records and writes only `review/local-preview/reused-music.json` plus a copied MP3; official X05 `music/manifest.json` remains absent, and the local preview sidecar records provenance. This is a concept soundtrack, **not** newly generated X05 music or official music-stage completion.

A first TTS start mistakenly used `/workspace/.video-tool-home/mokaair-work/videos`, before the pinned workdir was identified. It was stopped after two Sulafat lines. That separate volume was preserved; its media ledger reported US$0.00, no images, no judge calls, and no music. The two audio takes are **not** being reused. The active TTS run now uses `/workspace/.brand-video-workdir`, which contains the earlier manually reviewed lexicon transaction `5b35f7fc-d370-4c39-a86a-19bb5bee11bf`.

The v14 exact-SHA source review and two fresh blind reads all passed. Incremental Sulafat synthesized 11 lines (307 billable characters) and reused 73. Actual substantive narration is **8:23.37**, excluding both the hook and last three native closing lines. The latest audio check retained **24 human-ear flags**; the full 96 kbps narration MP3, per-line time index, hashes, and semantic concerns are recorded in `reviews/audio-qa.md`. This is not audio approval.

Three revised v14 object prompts were tested at one MiniMax `image-01` take each. `x05-b01-s04` and `x05-b06-s13` failed the judge and visual inspection because they introduced detached character heads; the latter also shows suspected pseudo-letters missed by the judge. `x05-b03-s03` passed the judge but has a color/detail mismatch and an unclear earlier/later comparison, so the author holds it for visual review. See `reviews/image-pilot-v14.md`. The three image/judge pairs cost **US$0.0405**; ledger is now **US$0.1485** (11 images and 11 judges cumulative), far below the user US$25 total cap but with quality unresolved. The `STOP` file is restored in the pinned volume. There is no finished MP4, official intro/outro asset, or Studio end-screen link to claim.

v15 修正只涉及 `x05-b01-s04`、`x05-b03-s03`、`x05-b06-s13` 的畫面提示詞；`video.json` SHA-256 為 `077a5a6b541cb9e5a181786b8ed2d3d00816263dc68a71db625a1a0c0520b12a`，Shorts SHA-256 仍為 `52e2812e2bbf409b3edab3e935dcf65f3768e79b0e9c0522a898e0b9d024dfd2`。作者差異證據在 `reviews/visual-prompt-v15-author.md`；新圖尚未生成、US$0.1485 帳本及 `STOP` 未變。`compose-video.mjs` 的既有 CARD-row assert 目前阻止從 TSV 全量重生；請只讀修訂場景欄與現稿 JSON，不把全量重生當成已完成。下一步由另一位審查者先鎖相同 SHA 做視覺差異審，然後在即時額度與整片 US$25 下，三鏡各最多三次重新試圖。
