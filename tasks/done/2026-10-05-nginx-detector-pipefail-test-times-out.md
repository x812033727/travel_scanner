---
id: 2026-10-05-nginx-detector-pipefail-test-times-out
title: nginx detector pipefail test times out on Windows
status: done
priority: P3
area: tools
owner: claude-opus-5-5-nginx-test-windows
claimed_at: 2026-10-05T12:49:16Z
created_at: 2026-10-05T01:25:32Z
completed_at: 2026-10-05T13:04:13Z
branch: claude/nginx-test-windows
depends_on: []
scope:
  - tools/nginx-install.test.mjs
---

# nginx detector pipefail test times out on Windows

## Why

On the Windows development machine, `npm run test:tools` fails "nginx detector never misses an
early marker in a large site under pipefail" in `tools/nginx-install.test.mjs`, with
`spawnSync bash ETIMEDOUT` after 90 s. The test runs the real `looks_like_mokaair_site` detector
from `ops/nginx/install.sh` 300 times in Git Bash over a fixture of more than 2 MB, and the
`spawnSync` timeout is 90 000 ms. Git Bash starts each `grep` slowly, so the loop does not finish
in time. Linux CI is not affected. The failure is a second Windows-only red beside the known
`tools/video/tts/check` one, so an agent comparing against the baseline has to rule it out by hand
every time.

## Definition of done

- [x] On Windows with Git Bash, the test either passes or is skipped with a stated reason, and it
  still catches the SIGPIPE race under `set -o pipefail` on Linux.

## Steps

- [x] Measure one attempt's time in Git Bash. Then either scale `attempts` by platform, raise the
  `spawnSync` timeout for this case, or skip it on `win32` with a reason that names the Linux CI
  run as its proof.
- [x] Keep the 300 attempts on Linux, where the race is reproducible.

## How to verify

`node --test tools/nginx-install.test.mjs` on Windows (Git Bash on PATH) and in Linux CI: 6 of 6
pass, or the one case reports a skip with a reason on Windows.

## Notes

- Seen on 2026-10-05 by claude-opus-5-5-automation-judge-paid-retries. It failed twice in the full
  suite and once run alone (90.5 s, `spawnSync bash ETIMEDOUT`). The branch had not changed
  `tools/nginx-install.test.mjs` or `ops/`. The test came in with #1175.

### 2026-10-05 fix (claude-opus-5-5-nginx-test-windows)

- Chose to scale the attempts by platform, not to skip, so Windows still runs the real detector
  over the 2 MB fixture under pipefail: `RACE_ATTEMPTS` is 20 on `win32` and 300 everywhere
  else. The `spawnSync` timeout stays 90 s for every case, and the other five cases are unchanged.
- Measured in Git Bash 5.3.15 (MSYS, the `bash` Node finds first from Git Bash): bash start-up
  0.29 s; one attempt 1.3 s alone, then 0.59 s an attempt over 20 and up to 0.87 s an attempt
  while other agents loaded the machine, and 0.11 s an attempt when it was quiet. 300 attempts
  therefore take roughly 35 to 260 s, which is why the case hit the 90 s timeout under load.
- In Git Bash the race is deterministic, not occasional: a `grep -Eq` reader (the bug #1175
  fixed) missed the early marker on 20 of 20 attempts. A copy of the test run against an installer
  with that reader failed on attempt 1 ("expected 0, got 1"), so 20 attempts still catch the
  regression on Windows.
- Linux side checked in WSL Ubuntu, bash 5.3.9 (no Node there, so the script ran the test's
  loop directly): the real detector found the marker 300 of 300 times in 14.1 s, and the
  `grep -Eq` reader missed 300 of 300. Linux CI's tools job is the run of record for the 300.
- Results on this machine: `node --test tools/nginx-install.test.mjs` 6 of 6 pass, the race case
  in 2.2 to 17.5 s depending on load. `node --test --test-concurrency=4 tools/*.test.mjs`: the
  race case passed in 6.9 s; 258 pass, 1 skip, 1 fail, and the fail is
  `tools/animation-production.test.mjs` unable to import `pinyin-pro`, because this worktree had
  no node_modules (its `package-lock.json` no longer matches the shared copy, so none was linked).
