---
id: 2026-10-01-make-the-outdated-cli-refusal-test
title: Make the outdated-CLI refusal test independent of background usage probes
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-01T04:41:27Z
completed_at:
branch:
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

- [ ] The test cannot see a probe in flight: usage is stubbed or the probes are settled before the
  run, without weakening what it asserts (409, no rotation, nothing left busy or resting).
- [ ] Other tests in the file that use `queue_seconds: 0` are checked for the same race.

## Steps

- [ ] Confirm the race (run the test in a loop with a slowed probe).
- [ ] Fix the test setup; change server code only if a run with `queue_seconds: 0` really should
  not be refused for a probe.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_accounts_agent_runs.py -q -p no:randomly --count 50
```
(or a shell loop if pytest-repeat is not installed)

## Notes

Found while reading PR #1063's red `api` check; the job was re-run there.
