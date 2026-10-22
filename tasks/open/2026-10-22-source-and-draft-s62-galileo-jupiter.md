---
id: 2026-10-22-source-and-draft-s62-galileo-jupiter
title: Source and draft S62 Galileo Jupiter observations episode
status: in-progress
priority: P2
area: docs
owner: codex-s62-new-episode
claimed_at: 2026-10-22T01:25:25Z
created_at: 2026-10-22T01:25:22Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s62
---

# Source and draft S62 Galileo Jupiter observations episode

## Why

The channel needs a new history episode after S61. A single night of Galileo's 1610 observation of Jupiter shows fewer light points than the later four-point record, so the story needs a fixed primary account that separates what he saw each night from his guesses and later inference. The author package must be independently reviewable before any paid voice or illustration work.

## Definition of done

- [x] S62 has a distinct A/B outline and a recommended A story, with a 30–60 second condensed opening, more than eight minutes of body at the conservative 325 CPM estimate, and the fixed 5-second intro and 21-second outro plan.
- [x] A fixed edition of Galileo's published account has a raw SHA-256, line anchors, limitations, and a one-to-one claim and visual map for every narration line.
- [x] The author candidate `video.json` and generated `script.md` pass the video lint with zero errors and zero warnings, use 70%+ unique original illustration prompts, and leave no fabricated video ID or paid-media receipt.

## Steps

- [x] Check S01–S61 briefs, topic index, and active tasks for overlap; choose a separate historical puzzle.
- [x] Pin and read the 1610 `Sidereus Nuncius` text through the 1880 Carlos translation and write the source boundary in `research.md`.
- [x] Draft `brief.md`, `video.json`, `claims.md`, generated `script.md`, and the author freeze for independent reviewers.
- [ ] Parent workflow obtains an independent source and picture audit, two blind story reads, and the station owner's choice and script approval before any media production.

## How to verify

From `/workspace/travel_scanner`:

```bash
sha256sum /tmp/curio-s62-sidereal.txt
VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s62 --json
npm run check:tasks
git diff --check
```

The first SHA must be `74fc9b817b64bc33415c6a44100c30f48952bc531d380682e5f4f1a26cc56fb5`. The fixed raw URL, commit and line map are in `research.md`; `/tmp` is a disposable local cache and not a Git deliverable.

## Notes

The episode follows 7 January–2 March 1610 and asks why Galileo sometimes counted three, sometimes two, sometimes four nearby points. His 10 January idea that one point was behind Jupiter remains attributed as his guess. The Carlos footnote that calls these objects “satellites” is editorial and does not become Galileo's original wording. The star diagrams are represented by tool text cards; image prompts are original illustrative actions, not exact sky reconstructions. Source, candidate hashes and local mechanical results are in `docs/videos/curio-s62/review/r1-author-freeze.md`. No TTS, image, music, rendering, upload or payment was attempted.
