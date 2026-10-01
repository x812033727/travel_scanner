---
id: 2026-10-01-make-the-outdated-cli-refusal-test
title: Make the outdated-CLI refusal test independent of background usage probes
status: done
priority: P2
area: api
owner: claude-opus-merge-train
claimed_at: 2026-10-01T11:55:06Z
created_at: 2026-10-01T04:41:27Z
completed_at: 2026-10-01T11:55:17Z
branch: claude/ticket-outdated-cli-flake
depends_on: []
scope:
  - apps/api/tests/test_ai_accounts_agent_runs.py
---

# Make the outdated-CLI refusal test independent of background usage probes

## Why

`apps/api/tests/test_ai_accounts_agent_runs.py::test_an_outdated_cli_refusal_does_not_rotate_or_leave_the_account_busy`
(added by #1010) failed on PR #1063, whose change has nothing to do with it:
`assert (503, 'subscription_busy') == (409, 'subscription_cli_outdated')` (CI run 36810886165,
2026-10-01 03:51Z). main passed the same test before and after.

The likely race: `AgentApplication.run` (ai_accounts_agent/server.py, the `while True` loop around
`pick_slot`) builds `busy` from `_runs_busy` plus `probing`, the slots whose usage probe is running
(`_usage_running`). `self.overview(False)` can start usage probes in the background; when both
slots a and b are still probing, `pick_slot` raises `subscription_busy`, and with the test's
`queue_seconds: 0` the deadline has already passed, so the 503 surfaces instead of the outdated-CLI
409.

## Definition of done

- [x] The test cannot see a probe in flight: usage is stubbed or the probes are settled before the
  run, without weakening what it asserts (409, no rotation, nothing left busy or resting).
- [x] Other tests in the file that use `queue_seconds: 0` are checked for the same race.

## Steps

- [x] Confirm the race (run the test in a loop with a slowed probe).
- [x] Fix the test setup; change server code only if a run with `queue_seconds: 0` really should
  not be refused for a probe.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_accounts_agent_runs.py -q -p no:randomly --count 50
```
(or a shell loop if pytest-repeat is not installed)

## Notes

Found while reading PR #1063's red `api` check; the job was re-run there.
Hit again on PR #1077 (CI 2026-10-01 11:50Z), whose change does not touch the agent.

- 2026-10-01 (claude-opus-merge-train): confirmed. With `Accounts.refresh_usage` slowed to 0.3 s
  this test failed every time with 503 `subscription_busy` and the other 43 tests in the file
  passed: the run's own `overview(False)` starts usage probes for a and b (signed in through
  claude.ai, no `recorded_at`), both count as busy while the probes run, and `queue_seconds: 0`
  refuses at once. Fix: the test calls `overview(False)` and waits for `_usage_running` to empty
  before the runs; neither account is due again within `claude_usage_min_interval_seconds` (60 s),
  so the three runs never meet a probe. The assertions are unchanged; no server change, since a
  run that cannot wait is right to be refused while both accounts are probing.
- Other `queue_seconds: 0` users: `test_a_request_gives_up_when_every_account_with_room_stays_busy`
  expects 503 either way; `test_a_probe_keeps_runs_off_its_account_and_the_turn_waits_for_it` and
  `test_a_run_waiting_for_the_only_account_gets_it_when_the_probe_ends` call `_claim_run_slot`
  after their probe has started, and passed with the slowed probe. With the fix and the normal
  probe, the test passed 30 runs in a row.
