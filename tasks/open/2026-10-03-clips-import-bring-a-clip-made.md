---
id: 2026-10-03-clips-import-bring-a-clip-made
title: clips import: bring a clip made outside the pipeline (Hailuo web, Kling MCP) into a shot with its checks and a ledger entry
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-03T11:20:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/media/ledger.mjs
  - tools/video/cli.mjs
  - tools/video/core/state.mjs
  - docs/videos/DRAMA.md
  - .agents/skills/youtube-video/references/drama.md
  - .claude/skills/youtube-video/references/drama.md
  - .agents/skills/animation-production/references/providers-and-plans.md
  - .agents/skills/animation-production/references/stage-preconditions.md
---

# clips import: bring a clip made outside the pipeline (Hailuo web, Kling MCP) into a shot with its checks and a ledger entry

## Why

The owner wants the Hailuo web subscription and Kling's MCP used for clips (2026-10-03:
「我要補hailuo跟kling的方案使用」「kling有MCP可以控，hailuo就需要你用網頁控制了」): on a
Hailuo Pro plan (US$54.99 a month, 4,500 credits; US$30.40 a month billed yearly) an 8-second
768P H3 clip costs about US$0.38 of credits at the plan's own US$0.047/s against US$0.64 on the
API, and the Max plan runs Hailuo 2.0/2.3 without credits in a relax queue. Today a clip
made outside the pipeline can only be brought in by hand: copy the mp4 under
`<VIDEO_WORKDIR>/<slug>/clips/`, write its entry in `clips/manifest.json` with the
manifest's speech, visual and look hashes, and run `assemble`, which still compares the clip's frame 0 with the shot's keyframe
(PSNR) and refuses a frozen tail; the black-frame and scene-cut checks belong to the `clips`
stage's QC and never run on it. Nothing probes the file first, nothing judges it, the
ledger never sees it, `status` cannot tell it from a bought clip, and a typo in the hand
written entry stalls `assemble` after the next paid stage. The `animation-production` skill
describes the manual route and names this command as the fix.

## Definition of done

- [ ] `node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider
      hailuo-web|kling-mcp|external [--plan <plan id>] [--credits N] [--usd N] [--note "…"]`
      copies the file into `clips/<shot>-import-<n>.mp4`, probes it (`ffprobe`: duration,
      resolution, fps), runs the same QC as a bought take (black, freeze, scene cuts, first
      frame against the shot's keyframe), optionally the judge (`--judge`), and writes the
      manifest entry in the shape `clips` writes (`file`, `sha256`, `seconds`, `frames`,
      `needed_s`, `first_frame`, `qc`, `judge`, `takes`, `needs_review`) plus
      `provider`, `plan`, `credits` and `imported_at`.
- [ ] The ledger gets an entry `{ stage: "clips", kind: "clip", id, provider, plan, credits,
      cost_usd: --usd or 0, status: "imported" }`; `ledgerTotals` counts its seconds; the
      `clips` stage's dry run and `run_report.mjs` show imported clips apart from bought ones.
- [ ] A clip whose first frame is not the shot's keyframe (PSNR below `keyframe_min_psnr`)
      is `needs_review` with the reason, like a failed take; `--force` keeps it with a note.
- [ ] The storyboard gate rule holds: the import refuses a shot whose storyboard is not
      approved, as `clips` does (exit 3).
- [ ] `docs/videos/DRAMA.md` and the skill's `drama.md` describe the command; the
      `animation-production` references replace the manual route with it.

## Steps

- [ ] Read how `clips` builds a take record and `writeManifest` (`tools/video/media/clips.mjs`)
      and how `assemble` reads it (`tools/video/assemble/cli.mjs`, `layoutDrama`).
- [ ] Add the subcommand, the ledger entry and the status wording; tests in `clips.test.mjs`
      with a synthetic mp4 and a stubbed `clipQc`.
- [ ] Documents.

## How to verify

```bash
node --test tools/video/media/clips.test.mjs tools/video/core/state.test.mjs
node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider hailuo-web --plan pro --credits 32
node tools/video/cli.mjs status --slug <SLUG>
```

## Notes

- Filed by the `animation-camera-and-animation-production-skills` task; the routes, plans
  and prices are in `.agents/skills/animation-production/references/providers-and-plans.md`.
- `tools/video/media/clips.test.mjs` is bound by the duration receipt
  (`docs/videos/long-form/review.json`); changing it needs an independent increment.
