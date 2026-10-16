---
id: 2026-10-16-durable-client-tests-in-client-test
title: Durable client tests in client.test.mjs time out under CI load on a 5 ms poll budget
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-16T07:04:38Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/client.test.mjs
---

# Durable client tests in client.test.mjs time out under CI load on a 5 ms poll budget

## Why

`tools/video/automation/client.test.mjs` fails now and then in CI's `video-tests` job (and so in
`web`), on tests that pass every time when the file runs alone. Each time the error is
`video_ai_run_pending` ("the saved stage run is still pending; its receipt will be recovered next
round") from `durableRun` in `tools/video/automation/client.mjs`, where the test expected the
saved answer.

Seen twice on 2026-10-16, both on code that does not touch `client.mjs` or its test:

- CI run 38861857885 (PR #1391, head `12db7abd5`), job `video-tests`: the test at line 518, "a
  translation's translator and caption reviewer are durable jobs too: a lost submit, a lost body or
  a restart reconnects to the same operation". It failed at `await translate(restarted)` after
  5012 ms. The rerun of the failed jobs passed on the same commit.
- A local `npm run test:tools` (Linux, Node 22.22.0, all of `tools/` in one run): the test at line
  1155, "all budgeted story chapters always use saved jobs for writing and checks". Running
  `node --test tools/video/automation/client.test.mjs` alone, twice on main `3cdbbd68b` and twice on
  the PR, gave 43/43 every time.

Likely cause: the `durableClient` helper (line 483), and the story-chapter test that builds its own
client, pass `durablePollMs: 5, durablePollIntervalMs: 5`. `durableRun` measures that budget with
`Date.now()` and gives the POST or look-up `AbortSignal.timeout(remaining)`. When the event loop
stalls for more than 5 ms under the full suite's load, the budget runs out before the mocked
`fetch` answers, so the client reports the run as pending instead of taking the answer. Not yet
proven: a fake clock or an instrumented run would confirm it.

## Definition of done

- [ ] The durable-client tests no longer depend on a few milliseconds of real time: a stalled event loop cannot turn a mocked answer into `video_ai_run_pending`.
- [ ] What each test asserts stays the same: one server operation per lost submit or body, a restart looks the job up and posts nothing, a budgeted story chapter always uses the durable route.

## Steps

- [ ] Confirm the cause, for example by injecting a delay or a fake `Date.now()` that pushes `durablePollMs` past its budget and reproducing the failure on demand.
- [ ] Fix it in the test only: either drive the budget from an injected clock if `automationClient` already accepts one, or give the clients that are meant to succeed a budget wide enough not to matter (keep the 5 ms one only where a test checks that the budget runs out).
- [ ] Look for other tests in the file with the same 5 ms budget that expect success, and treat them the same way.

## How to verify

```bash
node --test tools/video/automation/client.test.mjs
npm run test:tools        # several times, or under load (e.g. alongside another full run)
```

`client.mjs` is not in `REVIEW_FILES` (`tools/video/long-form/review.mjs`), so a test-only change
here needs no duration receipt; check that again before pushing.

## Notes

- Several open tasks list `tools/video/automation/client.test.mjs` in their scope
  (`2026-10-14-enforce-usd-25-all-in-cap`, `2026-10-16-story-budget-rollback-compat`,
  `2026-10-16-video-worker-a-rate-limited-topic`); check who is on it before claiming.
- Found while merging PR #1391; that PR's own change (the Windows-only rename retry in
  `tools/video/core/paths.mjs`) does not run on Linux and is not the cause.
