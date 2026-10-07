# Auto deploy: a timer that runs the deploy script when main is green

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
| 3 | newest commit younger than `AUTODEPLOY_QUIET_MINUTES` | `wait` (merges inside the period become one rebuild; every deploy restarts every container) |
| 4 | the `CI` workflow run for that SHA is not `success` (pending, red, missing, API unreachable) | `wait` (a red main already opens an issue through `ci-red-main.yml`) |
| 5 | an `AUTODEPLOY_BLOCKED_WINDOWS` window is open (Asia/Taipei) | `wait` |
| 6 | `/var/lock/travel-scanner-deploy.lock` is held, or `deploy-travel-scanner.sh --dry-run` exits 3 (hold file, or a staged release prepared but not activated) | `wait`, with the script's own reason |
| 7 | a `running` row in `video_stage_jobs` and `AUTODEPLOY_WAIT_FOR_PAID_WORK=true` | `wait`; one notification after `AUTODEPLOY_PAID_WORK_NOTIFY_HOURS` |
| 8 | everything above passed | `would_deploy` when `AUTODEPLOY_ENABLED=false` or `tick --dry-run`; otherwise run the script |

After a deploy that exits 0 the tick runs `host-verify.sh` (copied here by the installer
from the `deploy` skill) with `EXPECTED_SHA` filled in and records `PASS` or `FAIL` from its
`TOTAL` line. Any other exit means the script already rolled back: the tick writes the
paused file and every later tick stops at gate 1 until a person deletes it.

Gate 7 uses the same two selects as `host-preflight.sh`: a `running` stage job is a paid
model call in flight and would turn uncertain if its worker restarted; a `submitted` media
job survives a restart and is printed, not waited for.

## Files on the host

| Path | What |
| --- | --- |
| `/opt/travel-scanner-autodeploy/autodeploy.py`, `host-verify.sh`, `README.md` | The module and the verify script, copied by `install.sh`. A deploy must not change the poller underneath itself, so it does not run from the checkout; upgrading it is `sudo bash ops/autodeploy/install.sh` from a reviewed checkout, a manual host action like `ops/deployer`. |
| `/etc/travel-scanner/autodeploy.env` (root, 0600) | Configuration, see `autodeploy.env.example`. Read on every tick: a change needs no restart. |
| `/var/lib/travel-scanner-autodeploy/state.json` | Last tick, last decision (action, reason, gate, SHA), last deploy (SHA, previous, times, exit, log, verify result), how long paid work has been holding a deploy back. Never a secret. |
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
green merged SHA with no hold and nobody mid-release. Then set `AUTODEPLOY_ENABLED=true`.
The checklist and the record of the first automatic deploy belong to
`tasks/open/2026-10-07-autodeploy-rollout-and-skill-docs.md`.

## Reading it

```bash
sudo python3 /opt/travel-scanner-autodeploy/autodeploy.py status
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
back for longer than `AUTODEPLOY_PAID_WORK_NOTIFY_HOURS`. A failed post is printed and
ignored; it never blocks a deploy.

## Tests

```bash
python -m unittest discover -s ops/autodeploy -v
```

A temporary directory stands in for the host, a fake runner for every command and a fake
GitHub client; nothing needs root, Docker or the network, and the tests run on Windows.
Standard library only, no `fcntl`, Python 3.11 or newer (the host runs 3.14).
