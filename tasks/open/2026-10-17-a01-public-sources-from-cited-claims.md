---
id: 2026-10-17-a01-public-sources-from-cited-claims
title: A01 public sources from cited claims only
status: review
priority: P1
area: tools
owner: codex-gpt6-a01-source-filter
claimed_at: 2026-10-18T22:58:25Z
created_at: 2026-10-17T23:43:02Z
completed_at:
branch: codex/a01-public-sources-20261019
depends_on:
  - 2026-10-17-a01-seven-to-eight-minute-measured
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
---

# A01 public sources from cited claims only

## Why

For A01 `story-rolling-suitcase-v2`, `composeStory` currently copies every
`plan.sources` entry into the public `video.json.sources`. The r23 editorial
plan has 23 URLs; its isolated 104→105 revision proposal expands the internal
plan to 25, while the six-chapter draft's effective scene claims cite 18.
Unused plan research should not appear as a source for the finished
story, and future chapter remerges must not restore it. This is a source-index
and editorial-integrity fix separate from the seven-to-eight-minute runtime.

## Definition of done

- [x] A01's public sources contain only source indexes cited by effective
      non-`NOT FOUND` claim rows in the current six chapters, preserving plan
      order and source metadata.
- [x] B18 and other stories keep their current source behavior until their
      own reviewed evidence and requirements authorize a change.
- [x] A fresh and repeated chapter remerge cannot restore uncited A01 URLs.

## Steps

- [x] Confirm the r23 chapter source indexes against the proposed 25-source A01 plan and
      independent factual review; do not infer them from the old r8 video.json.
- [x] Implement the A01-only filter in `composeStory`, covering partial and
      complete chapter merges without invalid indexes or false citations.
- [x] Add tests for 25-to-18 A01 sources, `NOT FOUND` exclusion, stable order,
      remerge, and unchanged B18 output.

## How to verify

Run `node --test tools/video/automation/story.test.mjs`, `npm run check:tasks`
and the bound long-form duration check if any bound file changes. Compare the
resulting A01 `video.json.sources` with independently reviewed claim evidence.

## Notes

2026-10-18: Filed unclaimed at the owner's request while the duration task
still owns `story.mjs`/`story.test.mjs`. Start only after that task's changes
are integrated and its claim is released. Preserve #1518 and any production
chapter/media artifacts; no host rewrite or upload is authorized by this file.

2026-10-19: The owner authorized removing only these two paths from the
completed, merged #1562/#1568 task scopes; all other claims and draft #1518
remain untouched. The 25-to-18 count comes from the isolated r23 104→105
offline proposal, not a newly read production chapter set. Its six JSON
chapters contain 74 effective claim rows citing indexes 0, 1, 2, 5, 6, 8, 11,
12, 13, 15, 16, 17, 18, 19, 21, 22, 23 and 24; the proposed diagnostic
`video.json` still exposed all 25. The independent r23 fact-delta review
reports P0/P1/P2 = 0/0/0 for the editorial candidate, but leaves it on HOLD.
This branch changes task records, code and tests only; a host readback, new independent
script review, merge and deployment remain separate gates.

Code receipt: `node --test tools/video/automation/story.test.mjs` passed
33/33 from a short ASCII drive alias on Windows; `npm run check:tasks` and
`node tools/video/long-form/cli.mjs check` passed. The new composer applied
read-only to the isolated 104→105 r23 JSON returned 18 public sources in
plan order from 25 internal sources, with source metadata unchanged. An
independent code reviewer found no blocking issue. A broader Windows
`npm run test:tools` attempt showed one failure in unrelated
`tools/video/adult_english/pipeline.test.mjs` and ran for over 40 minutes
without completing; it was stopped. CI remains to be checked on the PR.

Task closure is pending: `npm run tasks -- done` wrote a done copy but could
not remove the open file. A subsequent exact-file removal was rejected by
automatic approval policy with no detailed reason. The done copy is untracked
and deliberately excluded from this draft PR; no alternate deletion was
attempted. The task remains in review until it can be closed safely.
