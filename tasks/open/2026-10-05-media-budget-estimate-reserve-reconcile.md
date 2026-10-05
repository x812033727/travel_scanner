---
id: 2026-10-05-media-budget-estimate-reserve-reconcile
title: Media budget gate: estimate, reserve, reconcile; judge calls and clip imports count against the cap
status: in-progress
priority: P2
area: tools
owner: claude-fable-5-1-budget
claimed_at: 2026-10-05T16:52:49Z
created_at: 2026-10-05T16:08:24Z
completed_at:
branch: claude/media-budget-reserve
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

- [x] `Stage.generate` writes a `reserved` ledger entry at list price before submitting and
      `bookJob` reconciles it; `capProblem` counts reserved money; a crash between submit and
      reconcile leaves a visible `reserved` row that `media-status` prints.
- [x] `Stage.judge` and `clips import --usd` refuse past the per-video cap (judge at
      `JUDGE_USD_PER_CALL`); no `--force` is added.
- [x] `episode_estimate.mjs` prints worst case, spent + reserved from the ledger, and the
      remainder; `tools/animation-production.test.mjs` pins it.

## Steps

- [x] `ledger.mjs`: `reserve`, `reconcile`, totals including `reserved`; `stages.mjs` uses them.
- [x] `clips.mjs importClip`: `spend()` before booking; `media-status` shows reserved rows.
- [x] `episode_estimate.mjs` reads the ledger; `DRAMA.md` §費用.
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
- Claimed with `--force` over the open, unowned `depends_on`
  `2026-10-04-native-video-project-stop-and-producer-exclusion`: that ticket is about an atomic
  project lease and STOP fencing across producers, and shares only the file `stages.mjs` with
  this one. Nothing in it is a precondition for reserving and reconciling money (the ledger is
  per work directory and the cap reads it at each call); whichever lands second rebases
  `stages.mjs`. Its own DoD and Notes were not touched.
- What was built (2026-10-05):
  - `ledger.mjs`: `reserve` (upsert by request `key`, status `reserved`, list price), `release`
    (drop by key), `reservedEntries`; `bookJob` replaces the hold under the entry's `key` when
    the job id is new, and drops the hold when the id is already booked (a resubmission that the
    server answered with the same job: without this the hold stayed beside the job's row — two
    existing stage tests caught it); `bookImport` takes an optional `key`, replaces the hold and
    records the row without it. `totalsOf` adds `reserved` (USD) and `reservations` (count);
    `totals.usd` is committed money (charged + held), so `capProblem` and `media-status`'s
    "this video" line count holds without touching `media/cli.mjs` (out of scope). `capProblem`
    takes a `what` ("generation" | "judge call" | "import") and names the held part.
  - `stages.mjs`: `generate` reserves after `spend` and before `submit`; a server refusal
    (`MediaError` with an HTTP status) releases, a lost connection (`code: "network"`) keeps the
    hold (the request may have landed; the rerun re-reserves the same key once and books the
    job). `judge` calls `spend(JUDGE_USD_PER_CALL, "judge call")` before asking; booked after,
    no hold (one cent; a crash mid-call under-records at most one row).
  - `clips.mjs importClip`: with `--usd` > 0 (or `--judge`) it reads `status` once, `spend`s
    the dollars, holds them under `import:<shot>:<sha256>` before copying anything, and the
    booking replaces the hold; `try/finally` releases a hold that was never booked (STOP before
    the judge, missing ffmpeg, a judge refused by the cap). An import without `--usd` and
    `--judge` still never calls the site.
  - `episode_estimate.mjs`: `--workdir <dir>` (reads `<dir>/media/ledger.json`, empty when
    absent) or `--ledger <file>` (must exist); `ledgerView` → `report.ledger`
    `{ spent_usd, reserved_usd, reservations, committed_usd, remaining_usd, reserved[] }`,
    `verdict.{spent_usd, reserved_usd, remaining_usd}`; the cap verdict compares the worst case
    with the remainder and the text lists each hold.
  - Old ledgers: no `reserved` rows → `reserved: 0`, other totals unchanged (pinned in
    `media.test.mjs`).
- Not done here (out of scope), for whoever takes it: `media/cli.mjs statusText` prints only
  `totals.usd`; the holds are visible as money in the text line and as `totals.reserved` /
  `reservations` in `--json`, but not as rows; a line "reserved: US$x for N requests (stage/id…)"
  would need `cli.mjs`. `run_report.mjs` counts a leftover `reserved` row as spend (it sums
  `cost_usd` by kind and stage); correct for a dead run's committed money, but it could mark the
  row as held. `.agents/skills/animation-production/references/stage-preconditions.md` quotes
  `stages.mjs` line numbers for `Stage.spend` (148-151) that have drifted by this change.
- Receipt: only `tools/video/media/clips.test.mjs` among the changed files is in `REVIEW_FILES`;
  the author did not touch `review.md`/`review.json`; an independent reviewer adds the increment.
