---
id: 2026-10-03-clips-import-bring-a-clip-made
title: clips import: bring a clip made outside the pipeline (Hailuo web, Kling MCP) into a shot with its checks and a ledger entry
status: in-progress
priority: P2
area: tools
owner: claude-fable-5-1-clips-import
claimed_at: 2026-10-03T16:07:33Z
created_at: 2026-10-03T11:20:00Z
completed_at:
branch: claude/kling-hailuoai-video-integration-3b73d6
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
  - .agents/skills/animation-production/SKILL.md
  - .claude/skills/animation-production/SKILL.md
  - .agents/skills/animation-production/references/providers-and-plans.md
  - .agents/skills/animation-production/references/stage-preconditions.md
  - .agents/skills/animation-production/references/error-catalogue.md
  - .agents/skills/animation-production/references/cost-model.md
  - .agents/skills/animation-production/references/post-mortem.md
  - .agents/skills/animation-production/scripts/run_report.mjs
  - .agents/skills/animation-production/scripts/drama_preflight.mjs
  - .agents/skills/animation-production/scripts/episode_estimate.mjs
  - .agents/skills/animation-camera/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
  - .agents/skills/animation-camera/references/model-misreads.md
  - tools/animation-production.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
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

- [x] `node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> --provider
      hailuo-web|kling-mcp|external [--plan <plan id>] [--credits N] [--usd N] [--note "…"]`
      copies the file into `clips/<shot>-import-<n>.mp4`, probes it (`ffprobe`: duration,
      resolution, fps), runs the same QC as a bought take (black, freeze, scene cuts, first
      frame against the shot's keyframe), optionally the judge (`--judge`), and writes the
      manifest entry in the shape `clips` writes (`file`, `sha256`, `seconds`, `frames`,
      `needed_s`, `first_frame`, `qc`, `judge`, `takes`, `needs_review`) plus
      `provider`, `plan`, `credits` and `imported_at`.
- [x] The ledger gets an entry `{ stage: "clips", kind: "clip", id, provider, plan, credits,
      cost_usd: --usd or 0, status: "imported" }`; `ledgerTotals` counts its seconds; the
      `clips` stage's dry run and `run_report.mjs` show imported clips apart from bought ones.
- [x] A clip whose first frame is not the shot's keyframe (PSNR below `keyframe_min_psnr`)
      is `needs_review` with the reason, like a failed take; `--force` keeps it with a note.
- [x] The storyboard gate rule holds: the import refuses a shot whose storyboard is not
      approved, as `clips` does (exit 3).
- [x] `docs/videos/DRAMA.md` and the skill's `drama.md` describe the command; the
      `animation-production` references replace the manual route with it.

## Steps

- [x] Read how `clips` builds a take record and `writeManifest` (`tools/video/media/clips.mjs`)
      and how `assemble` reads it (`tools/video/assemble/cli.mjs`, `layoutDrama`).
- [x] Add the subcommand, the ledger entry and the status wording; tests in `clips.test.mjs`
      with a synthetic mp4 and a stubbed `clipQc`.
- [x] Documents.

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
- Claimed with `--force` on 2026-10-04: the board refused because
  `2026-10-03-illustrated-slides-round-2-a-family` (status `review`) still holds
  `.agents/skills/youtube-video/references` and the two receipt files. Its pull request (#1172)
  merged on 2026-10-03 and the ticket was never closed, so nobody is in those files; its last
  unticked step (the first illustrated video after a deploy) is its owner's to close.
- What the command does beyond the contract above, and why:
  - **A production profile is refused (exit 3)** before anything is copied. `status` and
    `assemble` hold the manifest to the profile's model (`productionClipProblems`), so an
    imported entry could only ever read as "does not match"; letting a profile name an outside
    route is the owner's decision and a ticket of its own.
  - **Shots cut from the imported shot follow it** (`data.source`): their entries copy the
    source clip's file and hash, so without this the cut would keep playing the replaced clip.
    A cut the new clip is too short for is `needs_review` and the command exits 1.
  - **`--force` overrides the whole verdict**, not only the first-frame check: the entry gets
    `forced: true`, `needs_review: false`, and the measured problems stay in `qc.problems`.
  - **The ledger entry is written for a failed import too** (the credits are spent), keyed by
    shot and file hash so the same file brought in twice is one entry. `--usd` counts toward
    the per-video cap; without it the entry is US$0 and the tool converts nothing.
  - **No requested length**: nothing was asked of a server, so "shorter than asked" is not
    checked. A clip shorter than its lines only prints a note; `assemble`'s fit decides.
  - `clips --force` still buys an imported shot again (its request key is not in the cache);
    the dry run with `--force` prices it, without `--force` lists it as imported.
- `status` shows the imports through a new `detail` on the step (`pipelineStatus`), printed
  whether or not the step is done; `review/sync.mjs` sends only `id`, label and `done`, so the
  site's report is unchanged.
- The two skill scripts read the flat `provider` / `plan` / `credits` / `imported_at` and the
  ledger's `status: "imported"`, and still recognise entries put there by hand before the
  command existed (`provider: "external"`, or no ledger job), which they now call 手放.
- Not done here: a Kling provider card (`2026-09-26-video-drama-kling-provider-card`), and a
  profile field that admits an outside route. Neither Hailuo's web form nor Kling's MCP has
  been driven from a signed-in account yet, so no real clip has gone through the command.
