---
id: 2026-10-07-autodeploy-host-poller
title: Auto deploy main from a host-side poller that runs the existing deploy script
status: in-progress
priority: P1
area: ops
owner: claude-fable-5-1-autodeploy
claimed_at: 2026-10-07T00:33:38Z
created_at: 2026-10-07T00:00:00Z
completed_at:
branch: claude/auto-deploy-cloud-backup-hylcsz
depends_on: []
scope:
  - ops/autodeploy
---

# Auto deploy main from a host-side poller that runs the existing deploy script

## Why

Nothing deploys `main` after a merge. Every deploy is a person (or an agent that first
has to leave auto mode) opening SSH and running `/root/deploy-travel-scanner.sh`, so merged
work sits undeployed until someone remembers, and the agent-side classifier blocks the call
half the time (skill `deploy`, rule 3). The admin deployment centre (`ops/deployer`) is not
the answer: it is off, it ignores the deploy hold, it only builds `api` and `web`, and it
uses its own release layout and Compose project name, so enabling it would run a second
stack next to the one the script manages.

Design and the owner's decisions are in `docs/ops/auto-deploy-and-cloud-backup-plan.md`.
The short form: a root systemd timer runs `ops/autodeploy/autodeploy.py tick` every few
minutes; when `origin/main` is ahead of live and that SHA's `CI` workflow is `success`, it
runs the existing script. The script stays the only executor, so the hold file, rule 1, the
flock, the rollback and the logs all keep working without a new lock.

## Definition of done

- [x] `ops/autodeploy/autodeploy.py` with `tick`, `tick --dry-run` and `status`
      subcommands, standard library only, importable and tested on Windows (no `fcntl`,
      like `ops/release/hold.py`).
- [x] One tick, in this order, each step logged with its decision: paused file present →
      do nothing; `git fetch origin main` and compare to live `HEAD` → nothing new → done;
      newest commit younger than the quiet period → wait; GitHub Actions `CI` for that SHA
      not `success` (pending or failed) → wait; `/root/deploy-travel-scanner.sh --dry-run`
      refuses (exit 3: hold or an unactivated staged release) → wait; a `running`
      `video_stage_jobs` row (same two selects as `host-preflight.sh`) and waiting for paid
      work is on → wait; a configured blocked window → wait; otherwise run the deploy
      script with its output in `/root/deploy-logs/auto-<ts>.log`.
- [x] Deploy exit 0 → run `host-verify.sh` with `EXPECTED_SHA` set to the new SHA and
      record `PASS`/`FAIL` with the log path in the state file. Any other exit (the script
      has already rolled back) → write `/root/travel-scanner-autodeploy.paused` (line 1
      human readable within 600 bytes, line 2 JSON with `sha`, `log`, `exit`, `created_at`),
      and later ticks print the reason and stop. Only a person removes the file.
- [x] State in `/var/lib/travel-scanner-autodeploy/state.json`: last tick, last decision,
      last deployed SHA and time, last verify result, how long paid work has been holding
      a deploy back. Never any secret.
- [x] Config from `/etc/travel-scanner/autodeploy.env` (root, 0600):
      `AUTODEPLOY_ENABLED`, `AUTODEPLOY_GITHUB_TOKEN` (fine-grained PAT, this repository,
      `Actions: Read` only, as `ops/deployer/README.md` describes), `AUTODEPLOY_QUIET_MINUTES`
      (20), `AUTODEPLOY_WAIT_FOR_PAID_WORK` (true), `AUTODEPLOY_BLOCKED_WINDOWS` (empty;
      `HH:MM-HH:MM` in `Asia/Taipei`, comma separated), `AUTODEPLOY_NOTIFY_URL` (optional
      webhook, posted on deploy, pause and when paid work has blocked for more than
      `AUTODEPLOY_PAID_WORK_NOTIFY_HOURS`).
- [x] `travel-scanner-autodeploy.service` (`Type=oneshot`, root) and
      `travel-scanner-autodeploy.timer` (`OnCalendar=*:0/5`, `RandomizedDelaySec=30`);
      systemd never starts the service while a previous run is active, so ticks cannot
      overlap and the poller needs no lock of its own. `install.sh` copies the module to
      `/opt/travel-scanner-autodeploy/` like `ops/deployer/install.sh`, installs the units,
      creates the state directory and the env file from `autodeploy.env.example`, and does
      not enable the timer.
- [x] `ops/autodeploy/test_autodeploy.py` drives one tick through a fake command runner
      and a fake GitHub client for every branch above (paused, nothing new, quiet period,
      CI pending, CI failed, dry-run refusal, paid work, blocked window, deploy success with
      verify PASS and FAIL, deploy failure writing the paused file) and for the paused
      file's format. `python -m unittest discover -s ops/autodeploy -v` passes on Linux
      and Windows.
- [x] `ops/autodeploy/README.md`: install, the env file, the decision order, the paused
      file, how to read the state and the logs, how to stop it (`systemctl disable --now`
      or `AUTODEPLOY_ENABLED=false`), and that upgrading the module is a manual host action.

## Steps

- [x] Read `ops/release/README.md`, skill `deploy` (`SKILL.md`, `references/runbook.md`,
      `references/preflight.md`, `scripts/host-preflight.sh`, `scripts/host-deploy.sh`,
      `scripts/host-verify.sh`) and `apps/api/deployment_agent/executor.py` (`_ci`,
      `_target`): the CI lookup and the paid-work selects already exist, copy their shape.
- [x] Write the module with a `CommandRunner` seam and a GitHub client seam so the tests
      need neither the host nor the network; `urllib` is enough for the Actions API.
- [x] Units, installer, example env, README, tests.
- [ ] On the host (owner present, skill `deploy` rule 4: one SSH call per script): run
      `install.sh`, fill the env file with `AUTODEPLOY_ENABLED=false`, run
      `autodeploy.py tick --dry-run` by hand and check its decision against
      `host-preflight.sh`. Enabling the timer belongs to
      `2026-10-07-autodeploy-rollout-and-skill-docs`.

## How to verify

```bash
python -m unittest discover -s ops/autodeploy -v
bash -n ops/autodeploy/install.sh
systemd-analyze verify ops/autodeploy/travel-scanner-autodeploy.service   # on a systemd host
```

On the host: `python3 /opt/travel-scanner-autodeploy/autodeploy.py tick --dry-run` prints
one decision line per step and ends with what it would do; `status` prints the state file.

## Notes

- Owner decisions still open (plan, section 三, items 1–6): interval and quiet period,
  blocked windows, waiting for paid work and for how long, the notification channel, the
  PAT, and whether the deploy script should dump the database before every deploy (that
  change is to the host script, outside this scope, and needs the owner).
- Why pull, not push: a GitHub Actions job would need a host root key in repository secrets
  and inbound SSH from runner addresses on a host that has locked clients out for too many
  connections. The poller needs one read-only token and no inbound access, the same trust
  model as `ops/deployer`.
- The deploy script fetches and merges itself; the poller's own `git fetch` is read-only
  and only serves the comparison. Keep the poller out of the work tree otherwise: the
  script refuses a dirty tree.
- Every deploy recreates every container, including `video-worker` (runbook), which is why
  the paid-work wait exists. A `submitted` media job survives a restart and is printed,
  not waited for, exactly as `host-preflight.sh` does.
- The module lives in `/opt`, not in the checkout, so a deploy cannot change the poller
  underneath itself; the checkout's copy is the source of the next manual upgrade.
- 2026-10-07 (claude-fable-5-1-autodeploy): module, units, installer, env example, README
  and 29 unit tests are in `ops/autodeploy/`; `python -m unittest discover -s ops/autodeploy`
  passes and the API's ruff config is clean on it. Not done: the host steps (install, fill
  the token, one `tick --dry-run` checked against `host-preflight.sh`), which need the owner.
- Decisions taken while writing, to revisit if the owner disagrees: `AUTODEPLOY_ENABLED=false`
  is the dry run (every gate evaluated, `would_deploy` recorded, nothing run), so the week of
  watching needs no second mode; a live `HEAD` that is not an ancestor of `origin/main` waits
  for a person instead of letting the script's fast-forward fail and pause the timer; the
  notifier refuses a non-https URL; `host-verify.sh` is copied to `/opt` by the installer so
  the verification cannot change under a deploy either.
