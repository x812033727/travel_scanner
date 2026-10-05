---
id: 2026-10-05-nginx-detector-pipefail-test-times-out
title: nginx detector pipefail test times out on Windows
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T01:25:32Z
completed_at:
branch:
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

- [ ] On Windows with Git Bash, the test either passes or is skipped with a stated reason, and it
  still catches the SIGPIPE race under `set -o pipefail` on Linux.

## Steps

- [ ] Measure one attempt's time in Git Bash. Then either scale `attempts` by platform, raise the
  `spawnSync` timeout for this case, or skip it on `win32` with a reason that names the Linux CI
  run as its proof.
- [ ] Keep the 300 attempts on Linux, where the race is reproducible.

## How to verify

`node --test tools/nginx-install.test.mjs` on Windows (Git Bash on PATH) and in Linux CI: 6 of 6
pass, or the one case reports a skip with a reason on Windows.

## Notes

- Seen on 2026-10-05 by claude-opus-5-5-automation-judge-paid-retries. It failed twice in the full
  suite and once run alone (90.5 s, `spawnSync bash ETIMEDOUT`). The branch had not changed
  `tools/nginx-install.test.mjs` or `ops/`. The test came in with #1175.
