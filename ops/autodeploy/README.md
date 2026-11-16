# Auto deploy: a timer that runs the deploy script when main is green

This is the repository design and installation guide. The production host did
not have this timer installed at the 2026-10-16 read-only check. Before relying
on it, check `systemctl is-enabled travel-scanner-autodeploy.timer` and
`systemctl list-timers travel-scanner-autodeploy.timer` on that host, then verify
the installed poller bytes and its configured timeout.

`main` used to be deployed only when a person opened SSH and ran
`/root/deploy-travel-scanner.sh`. This directory is a root systemd timer that does the same
thing on its own: every five minutes `autodeploy.py tick` walks a fixed list of gates and
either does nothing, waits, or runs that script. The script stays the only executor, so
everything in `ops/release/README.md` (the deploy hold, rule 1, the flock, the rollback,
the logs) keeps working without a second lock; this module only decides whether to run it
now. Design and the owner's decisions: `docs/ops/auto-deploy-and-cloud-backup-plan.md`.

## The gates, in order

| # | Gate | Decision |
| --- | --- | --- |
| 1 | `/root/travel-scanner-autodeploy.paused` exists | `paused`: print its first line, do nothing |
| 2 | `git fetch origin main`; live `HEAD` equals `origin/main` | `idle` |
| 2b | live is not an ancestor of `origin/main` (the script's fast-forward would refuse) | `wait` for a person |
| 2c | `AUTODEPLOY_DEPLOY_WINDOWS` is set and none of its windows is open (Asia/Taipei) | `wait` (gate `schedule`; GitHub is not asked) |
| 2d | `AUTODEPLOY_MAX_AUTO_DEPLOYS_PER_DAY` successful automatic deploys already happened on this Asia/Taipei date | `wait` (gate `daily_limit`) |
| 3 | newest commit younger than `AUTODEPLOY_QUIET_MINUTES` | `wait` (merges inside the period become one rebuild; every deploy restarts every container) |
| 4 | the `CI` workflow run for that SHA is not `success` (pending, red, missing, API unreachable) | `wait` (a red main already opens an issue through `ci-red-main.yml`) |
| 5 | an `AUTODEPLOY_BLOCKED_WINDOWS` window is open (Asia/Taipei) | `wait` |
| 6 | `/var/lock/travel-scanner-deploy.lock` is held, or `deploy-travel-scanner.sh --dry-run` exits 3 (hold file, or a staged release prepared but not activated) | `wait`, with the script's own reason |
| 7 | a `running` row in `video_stage_jobs` and `AUTODEPLOY_WAIT_FOR_PAID_WORK=true` | `wait`; one notification after `AUTODEPLOY_PAID_WORK_NOTIFY_HOURS` |
| 8 | everything above passed | `would_deploy` when `AUTODEPLOY_ENABLED=false` or `tick --dry-run`; otherwise run the script |

After a deploy that exits 0 the tick runs `host-verify.sh` (copied here by the installer
from the `deploy` skill) with `EXPECTED_SHA` filled in and records `PASS` or `FAIL` from its
`TOTAL` line. Any other exit means the deploy and video-ai-worker state require
readback: the tick writes the paused file and every later tick stops at gate 1
until a person reconciles the state and deletes it.

Gate 7 uses the same two selects as `host-preflight.sh`: a `running` stage job is a paid
model call in flight and would turn uncertain if its worker restarted; a `submitted` media
job survives a restart and is printed, not waited for.

Gate 7 is an early scheduling decision, not the final restart boundary. A stage can
start during the build after this check. The host-only `deploy-travel-scanner.sh`
must also have the `ops/release/video_stage_drain.sh` hook installed at **both**
normal and rollback `compose up` sites (see `ops/release/README.md`). The timer
calls that same host script, so it cannot substitute its own earlier paid-work
select for the final warm drain. Installation is a separate approved host action;
the repository copy by itself does not protect a production deploy.
When this repository version is installed and enabled, the poller's 90-minute
deploy timeout is below systemd's two-hour unit timeout. An offline test confirms
that a timed-out subprocess produces an exit-124 paused receipt. This is not a
claim that the timer or a paused receipt exists on today's production host.
The child Docker stop may outlive the killed poller subprocess; an unresolved
warm-drain marker blocks another signal until exact worker/RQ/DB readback.

## Once a day: the deploy window

The owner chose on 2026-11-16 to deploy at most once a day, between 04:30 and 06:00 Taipei
time: `AUTODEPLOY_DEPLOY_WINDOWS=04:30-06:00` and `AUTODEPLOY_MAX_AUTO_DEPLOYS_PER_DAY=1`.
The timer still ticks every five minutes. Outside the window a tick with a new commit stops
at gate 2c; inside it the remaining gates run as before, so a CI run still in progress or a
paid video job only delays the deploy to a later tick of the same window. A window may wrap
midnight (`23:30-01:00`); a blocked window (gate 5) still wins inside a deploy window. The
daily count is kept in `state.json` as `auto_deploys_today` and counts only automatic deploys
that exited 0; a dry run never counts.

When a window closes while a newer commit was still waiting on a gate (CI red, paid work, a
hold, the lock), the first tick after it posts one notification naming the window, the SHA
and the last gate, and keeps it in `state.json` as `last_missed_window`. A deploy, an idle
tick or a failed deploy (which notifies on its own) inside the window clears the pending
record; a paused tick leaves it alone. Both settings empty keep the old behaviour: deploy
once the quiet period has passed. Background: `docs/ops/admin-redeploy-button-and-daily-autodeploy-plan.md`.

## The admin button

With `DEPLOYMENT_EXECUTOR=host_timer` and `DEPLOYMENTS_ENABLED=true` in the application
environment, `/admin/deployments` has two buttons, "deploy latest" and "rebuild current
version", which only the owner role can press (owner's decision, 2026-11-16) after typing
their password. The API never touches the host: it inserts a `queued` `deployment_runs` row with
`metadata_json = {"executor": "host_timer", "mode": "latest" | "rebuild", "wait_for_paid_work": ...}`.
Every tick first looks for such a row and claims it with
`UPDATE ... SET status = 'preflight' WHERE id = ... AND status = 'queued' RETURNING id`, so a
request is picked up within one tick (about five minutes); a request nobody claims in ten
minutes is marked `failed` (`deployment_executor_unavailable`) by the API.

A request skips the schedule (quiet period, deploy windows, daily limit, blocked windows) and
then walks the remaining gates. A gate that would make an automatic deploy wait **refuses** the
request instead, with a fixed `failure_code` the page shows: `deployment_autodeploy_paused` (no
forced deploys past the paused file, owner's decision), `deployment_already_current`,
`deployment_not_fast_forward`, `deployment_ci_not_green` (not checked for a rebuild),
`deployment_lock_held`, `deployment_hold_active`, `deployment_paid_work_running` (unless the
request unticked it), `deployment_dry_run` (`AUTODEPLOY_ENABLED=false`: the request records what
would have happened). Otherwise it runs the script (`--force` for a rebuild) with its log in
`/root/deploy-logs/button-<ts>.log`, then `host-verify.sh`, writing stages and events to the row:
`succeeded`, `manual_intervention_required` (`deployment_verify_failed`), or `failed`
(`deploy_script_exit_<n>`). A failed button deploy writes the paused file exactly like an
automatic one. Button deploys do not count toward the daily limit.

## The heartbeat the admin page reads

Every tick ends by upserting the single row of `deployment_host_status` (migration 0146): live
and target SHA, the target's subject, the CI result it read for that target, the paused file's
first line, whether it is a dry run, and a subset of `state.json` (last decision, last deploy,
today's count, the last missed window, the deploy windows, the commits between live and target).
With `AUTODEPLOY_NOTIFY_URL` empty (owner's choice, 2026-11-16) this page is the only place a
failure, a pause or a missed window shows up. A row older than 15 minutes makes the page say the
timer is not responding and refuse requests. A failed upsert is printed and never blocks a tick.

## Files on the host

| Path | What |
| --- | --- |
| `/opt/travel-scanner-autodeploy/autodeploy.py`, `host-verify.sh`, `README.md` | The module and the verify script, copied by `install.sh`. A deploy must not change the poller underneath itself, so it does not run from the checkout; upgrading it is `sudo bash ops/autodeploy/install.sh` from a reviewed checkout, a manual host action like `ops/deployer`. |
| `/etc/travel-scanner/autodeploy.env` (root, 0600) | Configuration, see `autodeploy.env.example`. Read on every tick: a change needs no restart. |
| `/var/lib/travel-scanner-autodeploy/state.json` | Last tick, last decision (action, reason, gate, SHA), last deploy (SHA, previous, times, exit, log, verify result), how long paid work has been holding a deploy back, today's automatic deploy count (`auto_deploys_today`), a window still waiting (`window_miss`) and the last window that closed without a deploy (`last_missed_window`). Never a secret. |
| `/root/travel-scanner-autodeploy.paused` | Written after a failed automatic deploy. Line 1 for people, 600 bytes at most; line 2 JSON (`sha`, `exit`, `log`, `created_at`). Only a person removes it, after reading the log. |
| `/root/deploy-logs/auto-<ts>.log`, `auto-verify-<ts>.log` | The deploy script's output and the verification's output for each automatic run, next to the manual `wrapper-*.log` files. |
| `/etc/systemd/system/travel-scanner-autodeploy.{service,timer}` | `Type=oneshot` every five minutes with 30 s jitter; systemd never starts a tick while the previous one is still running, so a long build cannot overlap the next tick. |

## Install and roll out

```bash
sudo bash ops/autodeploy/install.sh                      # copies files, installs units, does not enable
sudo vi /etc/travel-scanner/autodeploy.env               # AUTODEPLOY_GITHUB_TOKEN; keep ENABLED=false
sudo python3 /opt/travel-scanner-autodeploy/autodeploy.py tick --dry-run
sudo systemctl enable --now travel-scanner-autodeploy.timer   # still a dry run while ENABLED=false
```

The token is a fine-grained personal access token for this repository with only
`Actions: Read`, the same specification as `ops/deployer/README.md`.

Watch it for a week with `AUTODEPLOY_ENABLED=false`: `journalctl -u travel-scanner-autodeploy`
and `autodeploy.py status` show one decision per tick, and every `would_deploy` must be a
green merged SHA with no hold and nobody mid-release. With a deploy window set, a dry run prints `would_deploy` on every tick inside the window (a dry
run never counts toward the daily limit) and `wait: schedule` outside it. Then set `AUTODEPLOY_ENABLED=true`.
The checklist and the record of the first automatic deploy belong to
`tasks/open/2026-10-07-autodeploy-rollout-and-skill-docs.md`.

## Reading it

```bash
sudo python3 /opt/travel-scanner-autodeploy/autodeploy.py status   # also: the deploy window, open or when it next opens
journalctl -u travel-scanner-autodeploy --since -2h
systemctl list-timers travel-scanner-autodeploy.timer
```

Each tick prints one line per gate (`<time> ci: CI for <sha> is success (<url>)`) and ends
with `decision: <action>: <reason>`. Exit codes: 0 for every decision but a failed deploy,
1 for a failed deploy (so `systemctl --failed` shows it), 2 for a configuration error.

## Stopping it

- Pause for a while: `AUTODEPLOY_ENABLED=false` in the env file (ticks go on, deploys do not).
- Stop the timer: `systemctl disable --now travel-scanner-autodeploy.timer`.
- Hold a staged release: the normal deploy hold (`ops/release/README.md`) stops the timer's
  deploys exactly as it stops a manual one, at gate 6. Remember the timer deploys as soon as
  the hold is removed and the next tick comes.
- A manual deploy while the timer runs: check `systemctl is-active travel-scanner-autodeploy`
  first; a tick mid-deploy holds the deploy lock, and `host-deploy.sh` refuses on that anyway.

## Notifications

`AUTODEPLOY_NOTIFY_URL` gets one JSON POST per event, `{"text": ..., "content": ...}`, which
a Slack or Discord incoming webhook accepts as is and Telegram's
`https://api.telegram.org/bot<token>/sendMessage?chat_id=<id>` accepts as well. Events: a
deploy (with its verify result), a failed deploy (now paused), and paid work holding a deploy
back for longer than `AUTODEPLOY_PAID_WORK_NOTIFY_HOURS`, and a deploy window that closed without
deploying a waiting commit (once per window). A failed post is printed and
ignored; it never blocks a deploy.

## Tests

```bash
python -m unittest discover -s ops/autodeploy -v
```

A temporary directory stands in for the host, a fake runner for every command and a fake
GitHub client; nothing needs root, Docker or the network, and the tests run on Windows.
Standard library only, no `fcntl`, Python 3.11 or newer (the host runs 3.14).
