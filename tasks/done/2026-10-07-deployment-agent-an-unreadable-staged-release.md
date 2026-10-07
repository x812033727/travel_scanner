---
id: 2026-10-07-deployment-agent-an-unreadable-staged-release
title: Deployment agent: an unreadable staged-release root reads as no staged release
status: done
priority: P3
area: api
owner: claude-opus-5-5-staged-guard
claimed_at: 2026-10-07T04:19:11Z
created_at: 2026-10-07T04:01:01Z
completed_at: 2026-10-07T05:06:28Z
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - apps/api/deployment_agent/release_guard.py
  - apps/api/tests/test_deployment_center.py
  - ops/deployer/README.md
---

# Deployment agent: an unreadable staged-release root reads as no staged release

## Why

`apps/api/deployment_agent/release_guard.py` (#1360) fails closed on the hold: a hold file that
exists but cannot be read counts as a hold. `staged_release_reason()` does not: it lists
`<root>/mokaair-*/state.json` with `Path.glob`, which returns nothing, without raising, when
`root` cannot be listed, and its `except OSError: return None` treats any other listing error
the same way. A root the agent may not read then looks like "no staged release".

Today this is covered by the hold check: under the shipped unit (`ProtectHome=true`, user
`travel-deployer`, `/root` 0700) reading the hold already fails, so the agent refuses before
rule 1 is asked. It matters once the host gives the agent read access to the hold file alone
(the natural first step before `DEPLOYMENTS_ENABLED=true`): rule 1 would then pass silently.

## Definition of done

- [x] A staged-release root that exists but cannot be listed refuses with
      `deployment_staged_release_in_progress` and a reason that says it could not be read; a root
      that does not exist still holds no staged release.

## Steps

- [x] List the root with `os.scandir` (or `iterdir`) so a PermissionError surfaces, keep
      FileNotFoundError as "none", and refuse on any other OSError.
- [x] Test with a root that is a file (NotADirectoryError stands in for EACCES when tests run as
      root) and with a missing root.

## How to verify

`cd apps/api && uv run pytest tests/test_deployment_center.py`, plus ruff and both mypy runs.

## Notes

- Found 2026-10-07 by claude-opus-5-5-deploy-hold while reconciling a parallel implementation of
  2026-10-07-deployer-agent-honors-deploy-hold with #1360.
- Done 2026-10-07 by claude-opus-5-5-staged-guard. `staged_release_reason()` lists the root with
  `iterdir()` (FileNotFoundError is "none", any other OSError refuses), and a `mokaair-*`
  directory whose `state.json` cannot be stat'ed or read refuses too. It looks at every release
  directory before reporting an unreadable one, so a release that is definitely staged is named
  even when an older directory beside it cannot be read. An unreadable hold now says "could not
  read the hold file" instead of "hold file exists", since a 0700 `/root` gives the same
  PermissionError either way.
- Tests: a file standing in for the root (NotADirectoryError), a directory standing in for
  `state.json` (read fails), and a patched `Path.stat`/`Path.read_text` raising PermissionError,
  which is what the agent gets on the host; tests run as root and cannot get it from chmod.
- Consequence an independent review found: the drivers create `/root/mokaair-*` 0700 as root,
  so an agent given read access to `/root` alone refuses on every release directory for as long
  as it exists, not for 24 hours, because the age of a state file it cannot stat is unknown.
  That is the safe side; `ops/deployer/README.md` now says so, and the access the agent needs
  (or a marker it can read instead) is 2026-10-07-deployment-agent-needs-read-access-to.
