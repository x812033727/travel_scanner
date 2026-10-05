---
id: 2026-10-05-clips-a-shot-every-seed-is
title: Clips: a shot every seed is refused for loses the provider's refusal
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-clips-refusal-kept
claimed_at: 2026-10-05T13:10:00Z
created_at: 2026-10-05T00:37:01Z
completed_at:
branch: claude/clips-refusal-kept
depends_on: []
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
---

# Clips: a shot every seed is refused for loses the provider's refusal

## Why

When the clip provider refuses every seed of a shot (a failed job with a retakeable code such as
`video_media_rejected` or `video_media_upstream_invalid`), `tools/video/media/clips.mjs` saves the
shot as `{ ...entry, needs_review: true, problems: ["no take could be generated"] }`. The provider's
words are printed once per seed on stdout and then lost: the `ERROR <id>: no take passed:` line and
the manifest say only "no take could be generated", and `automation/flow.mjs` `failedTargets` hands
that bare phrase to the writer's prompt fix, which then has nothing to go on (a prompt too long for
the model, a content filter). `keyframes` had the same gap and now keeps the refusal
(2026-10-04-keyframes-crashes-when-every-image-take); clips does not crash, it only loses the reason.

## Definition of done

- [x] A clip shot every seed is refused for is saved with one problem per distinct refusal
      (`no take could be generated: <provider detail>`), and its `ERROR <id>:` line shows that text
      rather than "no take passed".
- [x] The record of such a shot carries no field from an earlier record whose clip is gone (today
      `{ ...entry }` spreads `current` into it).
- [x] Failed-job ledger rows (zero cost) and `media/jobs.json` stay as `Stage.generate` leaves them, and
      a rerun once the provider takes the prompt draws only that shot.

## Steps

- [x] In the take loop of `clips.mjs`, keep each retakeable error's message (without the
      `<shot id>: ` prefix `Stage.generate` adds) and build the all-refused record from them, as
      `keyframes.mjs` does.
- [x] A test in `clips.test.mjs` with a fake server whose clip job fails with a retakeable code for every
      seed of one shot and not for another.

## How to verify

```bash
node --test tools/video/media/clips.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Found while fixing 2026-10-04-keyframes-crashes-when-every-image-take (PR on branch
  `claude/keyframes-all-rejected`); see that ticket's Notes for the keyframes side of the same change.
- `tools/video/media/clips.test.mjs` is bound by `docs/videos/long-form/review.json`: editing it needs an
  independent DURATION_ONLY receipt increment, so open the PR as a draft and report the stale list.
- The open ticket 2026-10-04-profile-works-external-clip-route also lists both files; check it is not
  claimed before claiming this one.
- Done 2026-10-05 (claude-opus-5-5-clips-refusal-kept, branch `claude/clips-refusal-kept`). The
  2026-10-04-profile-works-external-clip-route ticket was open and unclaimed, and who-is-on-it showed
  no active task or open PR on `clips.mjs`, so the claim went through without `--force`.
- What changed in `clips.mjs`, as #1236 did for keyframes: the take loop keeps each retakeable
  refusal's text, with the `<shot id>: ` prefix that `Stage.generate` puts on a failed job's message
  cut off. A shot with no take is saved as `{ takes: [], needs_review: true, problems: ["no take could
  be generated: <refusal>", ...] }`, one problem per distinct refusal. It no longer spreads the earlier
  record into the new one. In clips that only matters for an earlier record with an empty `takes` list
  that still names a clip, because `entry` is the earlier record itself with its takes, so any take means
  a best take. Such a record's `file`/`sha256` would otherwise stay: the clips hash would count a clip
  that is gone, and a shot continuing from it would try to take its last frame. The `ERROR <id>:` line of
  a shot with neither a clip nor a take prints the refusals without "no take passed: ". Every other
  shot's line is unchanged, including an interrupted record that has takes but no file. The exit code
  stays `EXIT.lint`, so `automation/flow.mjs` `failedTargets` now hands the writer the provider's words.
- The new test (`a shot every seed is refused for waits for a prompt fix with the provider's refusal,
  ...`) failed against origin/main's `clips.mjs`. The record kept the stale `file`, `sha256`, `seed`,
  `seconds` and `judge`, and its only problem was the bare "no take could be generated". With the fix,
  `node --test tools/video/media/clips.test.mjs` passes 25/25. The fake server now takes a
  `refuse(request)` that ends a clip job failed when it is polled, the way the server's worker reports
  a vendor refusal (`apps/api/app/video_media/jobs.py` `advance_job`). So each refused job is
  remembered in `media/jobs.json` and then forgotten: the test asserts an empty jobs file, zero-cost
  failed ledger rows, and a rerun that buys only `sea-storm` seed 1.
- Seen but not changed (outside this scope, not measured): a clip record whose passed take's file was
  removed from disk is not re-checked the way keyframes re-checks its takes. Its seeds with a `qc` are
  skipped, so the run either buys the next seed or rebuilds the record around the missing file.
- `tools/video/media/clips.test.mjs` is receipt-bound: `node tools/video/long-form/cli.mjs check`
  prints `FAIL: stale duration review binding: tools/video/media/clips.test.mjs` until an independent
  DURATION_ONLY increment is added. `clips.mjs` itself is not bound.
