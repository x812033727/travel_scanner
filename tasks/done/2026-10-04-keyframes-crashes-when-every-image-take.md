---
id: 2026-10-04-keyframes-crashes-when-every-image-take
title: Keyframes crashes when every image take is rejected
status: done
priority: P2
area: tools
owner: claude-opus-5-5-keyframes-all-rejected
claimed_at: 2026-10-05T00:15:07Z
created_at: 2026-10-04T12:07:14Z
completed_at: 2026-10-05T00:39:33Z
branch: claude/keyframes-all-rejected
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
---

# Keyframes crashes when every image take is rejected

## Why

When every image take is refused, keyframes records a needs-review shot without a file, then includes that record in pictureHashes. path.join receives undefined and the CLI throws a TypeError instead of reporting the original generation refusal. A two-shot LLM pilot reproduced this after the provider rejected its combined prompt length; no new image was created.

## Definition of done

- [x] An all-refused shot produces a clear nonzero generation/check result with its original refusal, without an undefined-path exception.
- [x] Existing valid shots, failed-job receipts and pending-job recovery remain intact; contact sheets and duplicate checks only inspect actual picture files.
- [x] A mixed successful/refused run and an all-refused run have meaningful regression coverage without external API calls.

## Steps

- [x] Reproduce the fileless needs-review record using the existing fake media client.
- [x] Guard post-generation picture processing and verify the terminal result preserves the refused-shot details.

## How to verify

`node --test tools/video/media/look-keyframes.test.mjs`

## Notes

- Reproduced 2026-10-04 with `keyframes --slug ai-term-large-language-model --shot counter-arrival,counter-handoff`. Both shots received three definitive MiniMax `prompt length must be less than 1500` refusals; six terminal failed receipts accounted for zero cost and local pending jobs were empty. Fourteen unaffected shot entries/verdicts and all 23 existing image caches were preserved exactly. This is a definite rejection, not an uncertain paid POST.
- `tools/video/media/keyframes.mjs` builds `drawn` from the presence of a shot record, which can have `takes: []`, `needs_review: true` and no file; `pictureHashes` then receives undefined. The saved private rejection log/audit is under `<home>/mokaair-work/ai-series-continuation-20261004`.
- Related source preflight gap: schema's 1000-character scene prompt limit does not include Style, Camera or the provider's appended Avoid text. The failed combined strings measured 1644/1640 characters; the author shortened only the two prompts to actual combined lengths 1350/1367, preserving narration. The subsequently integrated remote branch includes a MiniMax request-body length guard and parameter-error classification; preserve that work. This ticket covers the distinct fileless-shot crash. Check the current provider and task before proposing another shared preflight change; no deployment state was inferred.

- Done 2026-10-05 (claude-opus-5-5-keyframes-all-rejected, branch `claude/keyframes-all-rejected`). The two
  new tests in `look-keyframes.test.mjs` were run first against origin/main's `keyframes.mjs` and both
  failed with the reported `TypeError [ERR_INVALID_ARG_TYPE]: The "path" argument must be of type string.
  Received undefined` from `pictureHashes` (keyframes.mjs:497); with the fix the file passes 31/31.
- What changed in `keyframes.mjs`: the take loop keeps each retakeable refusal's text (the shot id prefix
  that `Stage.generate` puts on a failed job's message is cut off); a shot with no take is saved as
  `{ takes: [], needs_review: true, problems: ["no take could be generated: <refusal>", ...] }`, one problem
  per distinct refusal, and no longer spreads an earlier record into it (a stale `file`/`judge` from a
  record whose picture is gone would otherwise be hashed and tiled); `drawn` (the dHash check, the tiles,
  the summary count) and `thumbnail_source` take only entries with a `file`; `contactSheetPages([])`
  returns no page, so a run with no picture draws no sheet, removes an older one and records
  `contact_sheet: null`; the `ERROR <id>:` line of a fileless shot prints the refusal instead of "no take
  passed the judge". The exit code stays `EXIT.lint` (1), so `automation/flow.mjs` hands the shot to the
  writer's prompt fix, and `failedTargets` now gives the writer the provider's words (e.g. the prompt
  length limit) instead of a bare "no take could be generated".
- Kept as they were: failed jobs are still booked by `Stage.generate` at zero cost and forgotten from
  `media/jobs.json` (both tests assert the ledger rows and an empty jobs file), drawn shots keep their
  takes and verdicts, and a rerun once the provider takes the prompt draws only the refused shot.
- Like a shot not drawn yet, a refused shot is skipped by the look-alike check, so its two neighbours are
  compared with each other until it is drawn (that was already the behaviour for undrawn shots).
- Not done here: `tools/video/media/clips.mjs` has the same `problems: ["no take could be generated"]`
  record for an all-refused clip, without the refusal text. It does not crash (clips has no picture hash
  or sheet step), so it was left out of this scope.
- `look-keyframes.test.mjs` is one of the files `docs/videos/long-form/review.json` binds, so the PR needs
  an independent DURATION_ONLY receipt increment before `cli.mjs check` is green.
- Claimed with `--force` over 2026-10-03-illustrated-slides-round-2-a-family and
  2026-10-03-illustrated-slides-lint-heuristics-the-shorts (both claude-fable-5-1-illustration-round2, status
  review, branch claude/video-production-tutorial-optimization-f5d1bc, claimed 2026-10-03 08:24Z): that
  branch landed as PR #1172 (merged 2026-10-03T10:34Z), so both claims are stale.
