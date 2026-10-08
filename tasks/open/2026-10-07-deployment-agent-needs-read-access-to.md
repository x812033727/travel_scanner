---
id: 2026-10-07-deployment-agent-needs-read-access-to
title: Deployment agent needs read access to the hold and the staged release state before it can deploy
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-07T04:58:46Z
completed_at:
branch:
depends_on: []
scope:
  - ops/deployer
  - ops/release
  - apps/api/deployment_agent/release_guard.py
  - apps/api/deployment_agent/config.py
  - apps/api/tests/test_deployment_center.py
---

# Deployment agent needs read access to the hold and the staged release state before it can deploy

## Why

The deployment agent refuses to deploy while the host's other release paths say a release is in
progress: the hold `/root/travel-scanner-deploy.hold`, or a `/root/mokaair-*/state.json` changed
in the last 24 hours with `built_at` and neither `activated_at` nor `failed_at`
(`apps/api/deployment_agent/release_guard.py`, `ops/deployer/README.md`). Both checks fail
closed: anything the agent cannot read counts as "a release may be in progress".

The shipped unit runs the agent as `travel-deployer` with `ProtectHome=true`, so `/root` is out of
reach and every deployment request refuses with `deployment_hold_active` ("could not read the hold
file"). Once the hold is readable it refuses with `deployment_staged_release_in_progress`
instead ("could not check ..."): the per-batch release drivers
(`docs/ai-terms-series/release_host.py`, `docs/ai-news-2026-ytd/deploy_release.py`,
`docs/ai-news-2026-09/deploy_release.py`, all `umask 077` and `mkdir(mode=0o700)`) create each
`/root/mokaair-*` directory 0700 as root, so the agent cannot stat any `state.json` and refuses
on every release directory for as long as it exists, not just for 24 hours. Nothing removes
release directories (an abandoned one gets an `abandoned.md`), so the existing ones keep it
refusing until their permissions change on the host. Until this is
settled the agent cannot deploy at all once `DEPLOYMENTS_ENABLED=true`, which is safe but means
the switch does nothing.

## Definition of done

- [ ] With `DEPLOYMENTS_ENABLED=true` on the host, the agent's `preflight` reports `release_guard`
      passed when no hold exists and no release is staged, and failed while either holds, the
      same answers `/root/deploy-travel-scanner.sh` gives at that moment.
- [ ] The agent still cannot write the hold or anything under the release directories.

## Steps

- [ ] Decide between:
      (a) read-only access for `travel-deployer` to the hold and to each
      `/root/mokaair-*/state.json` (a group or ACL; `ProtectHome=read-only` plus
      `ReadOnlyPaths=` in the unit). This needs a one-time change on the host to the existing
      0700 release directories, and future drivers creating theirs with that group or ACL;
      `ops/release/README.md` says finished drivers are not edited, so this is a rule written
      there for new drivers, not an edit to the old ones.
      (b) a new root-owned marker, readable by the agent, that says whether rule 1 holds. No
      such marker exists today: it means a new writer, and a change to
      `/root/deploy-travel-scanner.sh`, which is not in git and which `ops/release/README.md`
      says may change only with the owner's approval. The agent would read it through a new
      `AgentConfig` path (`apps/api/deployment_agent/config.py`), keeping the fail-closed
      reading in `release_guard.py`.
- [ ] Change the unit (`ops/deployer/travel-scanner-deployer.service`) and, for (a), the access
      on the host and the rule for new drivers; for (b), the marker's writer, the script (with
      the owner's approval) and `AgentConfig`.
- [ ] Re-check on the host with reads as `travel-deployer`, then with the agent's preflight.

## How to verify

On the host: `systemctl show travel-scanner-deployer -p ProtectHome -p ReadOnlyPaths`, then the
admin deployment panel's preflight with no hold, with a hold written by hand, and with a release
prepared but not activated.

## Notes

- Filed 2026-10-07 by claude-staged-guard after an independent review of
  2026-10-07-deployment-agent-an-unreadable-staged-release found the 0700 consequence. The
  refusal is the safe side, so this is about making the agent usable, not about safety.
- The agent's own release layout (`/srv/travel-scanner/releases`, Compose project
  `travel-scanner`) still differs from the script's; `ops/deployer/README.md` says enabling the
  agent on a script-managed host starts a second stack. Settle that before, or together with,
  this ticket.
