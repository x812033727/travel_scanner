---
id: 2026-10-05-delivery-promise-and-continuity-locks
title: Delivery promise and continuity locks in the plan lock: a clip may not quietly become a still
status: done
priority: P2
area: tools
owner: claude-fable-5-1-promise
claimed_at: 2026-10-05T16:23:41Z
created_at: 2026-10-05T16:08:24Z
completed_at: 2026-10-05T16:53:38Z
branch: claude/delivery-promise-continuity-locks
depends_on: []
scope:
  - .agents/skills/animation-preproduction/scripts/plan_lock.mjs
  - .agents/skills/animation-preproduction/scripts/shot_plan.mjs
  - .agents/skills/animation-production/scripts/drama_preflight.mjs
  - .agents/skills/animation-production/scripts/run_report.mjs
  - tools/animation-preproduction.test.mjs
  - tools/animation-production.test.mjs
  - .agents/skills/animation-preproduction/references/preproduction-flow.md
  - .agents/skills/animation-production/references/stage-preconditions.md
---

# Delivery promise and continuity locks in the plan lock: a clip may not quietly become a still

## Why

Nothing records what a shot was promised to be. A shot planned as a clip can be rewritten
into a still or a `fit: freeze` and nobody is asked; the only record of the kind is
`plan/lock.json`'s `visual_kind` written by `plan_lock.mjs`, and `compareLock` reports the
change but no stage refuses it. Continuity (props, costume, time of day) is likewise only in
prompts. OpenMontage's "delivery promise" and the Chinese drama skill packs' continuity locks
(drama-skills, MIT; shuohao-skills, Apache-2.0) are the ideas; the lock file is where they fit
without touching the bound `core/drama.mjs`.

## Definition of done

- [x] `plan/lock.json` records a `promise` per shot (`visual_kind`, bought seconds, route) and
      `continuity` locks (`depends_on` shot ids, locked prop / costume / time-of-day strings),
      written by `shot_plan.mjs`.
- [x] `drama_preflight.mjs` exits with the lint code when a shot promised `clip` is now `still`
      or `fit: freeze` without a change-order line in `changes.jsonl`, or when a locked string is
      missing from a dependent shot's prompt; `compareLock` keeps reporting kind changes.
- [x] `run_report.mjs` lists promised vs delivered per shot and the saved / spent delta.

## Steps

- [x] Schema of the lock (`preproduction-flow.md` §鎖定包), `shot_plan.mjs` writes it,
      `plan_lock.mjs` compares it.
- [x] `drama_preflight.mjs` findings `promise.broken`, `continuity.broken` with the fix text;
      `stage-preconditions.md` rows.
- [x] `run_report.mjs` columns; tests in `tools/animation-preproduction.test.mjs` and
      `tools/animation-production.test.mjs`.

## How to verify

```bash
node --test tools/animation-preproduction.test.mjs tools/animation-production.test.mjs
node .agents/skills/animation-production/scripts/drama_preflight.mjs --slug <episode>   # exit 1 on a broken promise
```

## Notes

- No bound file. An `intent` key on `video.json` shots is a possible follow-up once
  `SHOT_KEYS` is free to change.
- Also carries the research's "shot dependencies and continuity locks" item.

### Done (2026-10-05)

- **Lock schema, version 3** (`plan_lock.mjs` `LOCK_VERSION`): each shot in `plan/lock.json`
  carries `promise: { visual_kind, buy_s, route, fit }` and
  `continuity: { depends_on, locks: { prop, costume, time_of_day } }`, both computed by
  `shot_plan.mjs` (`planEpisode` puts them on every shot; `--markdown` prints a 承諾與連戲鎖
  section, `--csv` gains `fit`, `depends_on`, `locks`). The top-level `visual_kind` / `buy_s`
  stay, so `compareLock` keeps reporting `kind: [before, after]`. A version-2 lock makes
  `--check` / `--ready` / `--accept` exit 2 as before ("lock again with --write --force");
  the preflight only notes it. `fit` is part of the promise so a shot locked with
  `fit: freeze` (the drama fixture's sea-storm) is not a break.
- **Continuity extraction** (`shot_plan.mjs` `continuityTerms`, `continuityLocks`,
  `CONTINUITY_TERMS`): strings come from each shot's `prompt` through three word lists (props
  = the risk table's weapons and small props plus scene props; costume; time of day). A prop or
  costume string is locked on a shot only when another shot of the same chapter writes the same
  string (both ends of the thread hold it); a time of day locks on every mention. Each noun is
  locked as written and once more with the one adjective in front of it (`jade hair cord`), so
  `jade` → `red` is caught; possessives, articles and frame positions are not adjectives.
  `depends_on` = earlier shots in the chapter sharing a locked string, plus `source.shot` and
  `start_frame.shot`. The strings are exact (lowercase, word-bounded): write an anchor the same
  way in every shot.
- **What breaks a promise** (`plan_lock.mjs` `promiseBreak`): a shot promised `clip` that is
  now `still`, `cut` (`source`), deleted, or `fit: freeze` when the lock's fit was not
  freeze. The expensive direction (still → clip) only appears in the change order.
- **Change-order line shape** (`plan/changes.jsonl`, `changeOrderLine`): the existing re-lock
  line plus `status` (`"accepted"` from the new `plan_lock.mjs --accept --note "<站主的話>"`,
  `"settled"` from `--write --force`; older lines without `status` count as settled),
  `shots: [{ id, kind, fit, buy, continuity }]`, `added`, `removed`. `coveringOrder` accepts
  a break only from a line whose `previous_lock` is the current lock's `created_at` and whose
  `shots` entry for that id records that very change (same target kind / fit, every missing
  string listed; a deleted shot via `removed`). `--accept` requires `--note`, exits 1 when
  nothing changed, 2 without a lock.
- **Preflight** (`drama_preflight.mjs`): runs the two checks at every stage when
  `plan/lock.json` exists; findings carry `id` `promise.broken` / `continuity.broken`
  (level refuse, exit `EXIT.lint` = 1) or `promise.signed` / `continuity.signed` (note); the
  result gains `lock: { file, created_at, version, problem, broken, signed }`. Episodes
  without a lock are unaffected; the stage modules themselves still do not read the lock
  (documented in `stage-preconditions.md`).
- **Run report** (`run_report.mjs`): `promises` (null without a lock) lists per shot the
  promise, the current kind/fit, what `clips/manifest.json` delivered, what the ledger spent
  (US$ on the server route, credits from imported entries on a web route), `kept`, `change`
  (`downgrade` / `upgrade`), `signed`, `delta` (spent − promised one-take price; negative is
  saved) and totals plus the count of accepted / settled change orders; printed in the text
  report and as a table in the post-mortem markdown.
- Technique attributed by name only: "delivery promise" (OpenMontage, AGPL, idea only) and
  "continuity locks" (drama-skills, shuohao-skills); no outside code was read or copied.
- **Deferred / limits**: a shot that never named a time of day and later gains a different
  one is only a visual change in `--check`, not a continuity break (only locked strings are
  checked); the word lists are modest and exported for extension; singular/plural are
  different strings; `fit` changes other than freeze are listed in the change order but not
  refused; the `intent` key on `video.json` stays a follow-up.
- Verified: `node --test tools/animation-preproduction.test.mjs tools/animation-production.test.mjs`
  31/31; `npm run test:tools` 1699 pass, 0 fail, 2 skipped (pre-existing); `npm run check:tasks`
  validated; `node tools/video/long-form/cli.mjs check` PASS.
