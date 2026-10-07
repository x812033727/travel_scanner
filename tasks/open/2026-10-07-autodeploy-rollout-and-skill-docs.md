---
id: 2026-10-07-autodeploy-rollout-and-skill-docs
title: Roll out the auto deploy timer and teach the deploy skill about it
status: in-progress
priority: P1
area: docs
owner: claude-fable-5-1-autodeploy
claimed_at: 2026-10-07T00:55:01Z
created_at: 2026-10-07T00:00:00Z
completed_at:
branch: claude/auto-deploy-cloud-backup-hylcsz
depends_on:
  - 2026-10-07-autodeploy-host-poller
scope:
  - .agents/skills/deploy
  - .claude/skills/deploy
  - ops/release/README.md
---

# Roll out the auto deploy timer and teach the deploy skill about it

## Why

Once `ops/autodeploy` exists, the host has a fourth way to deploy and the skill and the
release README still describe three. An agent that does not know the timer is running will
race it (start a manual deploy while the timer is about to), misread a `/root/deploy-logs/auto-*`
log, or clear a paused file without reading it. The rollout itself (dry-run week, then
enable) also needs a written checklist so it happens once and is recorded.

## Definition of done

- [x] `host-preflight.sh` prints an `-- auto deploy --` section: timer enabled or not, the
      state file's last tick, last decision and last deployed SHA, and the paused file's
      first line when present (same byte-identical copy under `.claude/skills/deploy`,
      `npm run test:tools` checks it).
- [x] Skill `deploy`: the host table lists the timer, the paused file and the state file;
      the "不變的規矩" say that a manual deploy first checks the timer is not mid-tick
      (`systemctl is-active travel-scanner-autodeploy`) and that a paused file is read and
      its deploy log looked at before anyone deletes it; `references/preflight.md` gets the
      paused-file case next to the hold-file case; `references/runbook.md` names the
      `auto-<ts>.log` files.
- [x] `ops/release/README.md`: the two-paths table becomes three rows (the timer runs path
      A on its own, so the hold file and rule 1 stop it too), and "放棄一個發布" says the
      timer deploys as soon as the hold is removed.
- [ ] Rollout done on the host and recorded in this task's Notes: a week of
      `AUTODEPLOY_ENABLED=false` ticks whose logged decisions were checked against what a
      person would have done; then `AUTODEPLOY_ENABLED=true` and `systemctl enable --now
      travel-scanner-autodeploy.timer`; the first automatic deploy's SHA, duration and
      verify result written here.

## Steps

- [x] Wait for the poller task to land and be installed on the host.
- [x] Preflight section, skill text, release README; `npm run test:tools`.
- [ ] Dry-run week: read `/var/lib/travel-scanner-autodeploy/state.json` and the tick logs
      once a day; every "would deploy" must coincide with a green merged SHA and no hold.
- [ ] Enable with the owner present; watch the first real deploy end to end with
      `host-verify.sh`.

## How to verify

```bash
npm run test:tools
MSYS_NO_PATHCONV=1 <SSH> -m .agents/skills/deploy/scripts/host-preflight.sh   # shows the auto deploy section
```

## Notes

- The notification channel (plan, section 三, item 4) is decided before enabling; until
  then a failed automatic deploy is only visible as the paused file and in preflight.
- Keep the skill edits to what changed; the rules in `ops/release/README.md` are not
  copied into the skill.
- 2026-10-07 (claude-fable-5-1-autodeploy): the repository half is done in the same pull
  request as the poller (x812033727/travel_scanner#1354): `host-preflight.sh` has an
  `-- auto deploy --` section (timer enabled/active/tick, `state.json`'s last decision and
  last auto deploy, the paused file's first line; exercised against a fake state file and
  without one), skill `deploy` has the timer in its host table, rules 9 and 10 and a
  "跟自動部署 timer 共存" section in `runbook.md`, `preflight.md` has the paused-file case,
  and `ops/release/README.md` lists the timer as a path that runs the script. Only
  `SKILL.md` is mirrored under `.claude/skills/deploy` (`tools/skills.test.mjs` passes).
  Left: the host rollout (install, token, dry-run week, enable, first automatic deploy),
  which needs the owner on the host.
