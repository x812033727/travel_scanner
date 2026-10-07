---
id: 2026-10-07-deployer-agent-honors-deploy-hold
title: The admin deployment agent refuses to deploy while the deploy hold exists
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-07T00:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/deployment_agent
  - apps/api/tests/test_deployment_agent_contract.py
  - apps/api/tests/test_deployment_center.py
  - ops/deployer/README.md
---

# The admin deployment agent refuses to deploy while the deploy hold exists

## Why

`ops/release/README.md` ends with "the admin deployment centre is a third deployment path;
before it is enabled it should honour the same hold file; that is another ticket". This is
that ticket. The agent (`apps/api/deployment_agent/executor.py`, `_deploy_locked`) checks
its own flock, `main`, CI and disk, but not `/root/travel-scanner-deploy.hold` nor rule 1
(a `/root/mokaair-*/state.json` built but not activated within 24 hours), so an operator
pressing the button mid-way through a staged release would rebuild the containers the
release depends on.

## Definition of done

- [ ] `preflight` and `_deploy_locked` fail with a new `deployment_hold_active` code when
      the hold file exists, carrying the hold's first line (sanitised, 600 bytes) as the
      detail; the same for rule 1 with `deployment_staged_release_in_progress`.
- [ ] The hold path and the staged-release glob are compiled into `AgentConfig`, not
      accepted from a request.
- [ ] The agent reads `hold.py`'s format by itself (it runs from `/opt`, so it cannot
      import `ops/release/hold.py`); a copy of the two-line parser with a test that it
      accepts what `ops/release/test_hold.py` writes.
- [ ] `ops/deployer/README.md` lists both refusals, and the sentence in
      `ops/release/README.md` that calls this "another ticket" can be updated by whoever
      closes it (that file is in `2026-10-07-autodeploy-rollout-and-skill-docs`'s scope;
      coordinate rather than edit it here).

## Steps

- [ ] Read `ops/release/README.md` for the hold format and rule 1.
- [ ] Add the two checks and the failure codes; the web admin page maps failure codes to
      copy, so check `apps/web` for the code table and add the two strings there in a
      follow-up if it is not in this scope.
- [ ] Tests in `apps/api/tests/test_deployment_agent_contract.py` and `test_deployment_center.py` (the fake runner lives there).

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_deployment_agent_contract.py tests/test_deployment_center.py
```

## Notes

- Low priority because the agent is off and `2026-10-07-autodeploy-host-poller` makes the
  script the automatic path. Do it before anyone enables `DEPLOYMENTS_ENABLED=true`.
- The agent's release layout (`/srv/travel-scanner`, project `travel-scanner`, only `api`
  and `web`) still differs from the script's; honouring the hold does not make the two
  interchangeable. Say so in the README.
