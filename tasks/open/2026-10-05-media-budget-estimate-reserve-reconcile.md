---
id: 2026-10-05-media-budget-estimate-reserve-reconcile
title: Media budget gate: estimate, reserve, reconcile; judge calls and clip imports count against the cap
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:24Z
completed_at:
branch:
depends_on:
  - 2026-10-04-native-video-project-stop-and-producer-exclusion
scope:
  - tools/video/media/ledger.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/media/media.test.mjs
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - .agents/skills/animation-production/scripts/episode_estimate.mjs
  - tools/animation-production.test.mjs
  - docs/videos/DRAMA.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Media budget gate: estimate, reserve, reconcile; judge calls and clip imports count against the cap

## Why

The per-video cap is checked only at `Stage.generate` ("spent + this call ≤ cap"); judge calls
(`Stage.judge`, US$0.01 each) and `clips import --usd` never go through it, there is no
reservation between submit and reconcile, and `episode_estimate.mjs` compares the worst case
with the cap without subtracting what the ledger already spent. The server reserves monthly
units but has no per-video view. OpenMontage's budget governor (estimate → reserve →
reconcile; AGPL — idea only) is the shape; the ledger already has the entries to carry it.

## Definition of done

- [ ] `Stage.generate` writes a `reserved` ledger entry at list price before submitting and
      `bookJob` reconciles it; `capProblem` counts reserved money; a crash between submit and
      reconcile leaves a visible `reserved` row that `media-status` prints.
- [ ] `Stage.judge` and `clips import --usd` refuse past the per-video cap (judge at
      `JUDGE_USD_PER_CALL`); no `--force` is added.
- [ ] `episode_estimate.mjs` prints worst case, spent + reserved from the ledger, and the
      remainder; `tools/animation-production.test.mjs` pins it.

## Steps

- [ ] `ledger.mjs`: `reserve`, `reconcile`, totals including `reserved`; `stages.mjs` uses them.
- [ ] `clips.mjs importClip`: `spend()` before booking; `media-status` shows reserved rows.
- [ ] `episode_estimate.mjs` reads the ledger; `DRAMA.md` §費用.
- [ ] Receipt increment by an independent agent for `media/clips.test.mjs`.

## How to verify

```bash
node --test tools/video/media/media.test.mjs tools/video/media/stages.test.mjs tools/video/media/clips.test.mjs tools/animation-production.test.mjs
node tools/video/cli.mjs media-status --slug <video>     # reserved rows visible
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `tools/video/media/clips.test.mjs`.
- `clips.mjs` / `stages.mjs` are also named by `2026-10-04-fault-checks-for-the-drama-judges`,
  `2026-09-28-video-shorts-worker-drama`, `2026-10-03-illustrated-slides-round-2-a-family`
  and `2026-10-05-clips-a-shot-every-seed-is` (all unclaimed); claim order decides who rebases.
- The server keeps the monthly meter (`meter.py`); this is the per-video view.
