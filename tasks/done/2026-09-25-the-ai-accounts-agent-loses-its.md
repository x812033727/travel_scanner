---
id: 2026-09-25-the-ai-accounts-agent-loses-its
title: The AI accounts agent loses its socket group on every restart
status: done
priority: P1
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-25T01:21:27Z
created_at: 2026-09-25T01:20:50Z
completed_at: 2026-09-25T01:23:10Z
branch: claude/ai-accounts-socket-restart
depends_on: []
scope:
  - ops/ai-accounts/mokaair-ai-accounts.service
  - apps/api/tests/test_ai_accounts_agent.py
---

# The AI accounts agent loses its socket group on every restart

## Why

After `install.sh` restarted `mokaair-ai-accounts` on 2026-09-24 (the #737 update), AI 設定
reported the agent unreachable. The socket was `root:root`, so the API container, which gets
in through group `travel-api`, got EACCES on connect. The first start after install had
worked. On a restart the previous run's `agent.sock` is still in place, so `ExecStartPost`
found it at once and chgrp'd that old file. Only then did the agent unlink it and bind a
fresh socket as `root:root`. Every restart would repeat it, and so would a reboot if systemd
kept `/run` contents (it does not, which is why only restarts showed it).

## Definition of done

- [x] `ExecStartPre` removes a stale `agent.sock`, so `ExecStartPost` waits for the new one.
- [x] A test pins the unit's start hooks, the `-` on the socket directory in `ReadWritePaths`,
      and the absence of `MemoryDenyWriteExecute`.
- [x] The host unit carries the same line: patched in place on 2026-09-25 and `daemon-reload`ed,
      the live socket chgrp'd, and the API container reaches the agent again.

## Steps

- [x] Unit fix.
- [x] Test.
- [x] Host hotfix (done before this PR; the next `install.sh` run writes the same unit).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_accounts_agent.py -k unit_hands
```

On the host, after any `systemctl restart mokaair-ai-accounts`:
`stat -c '%G' /run/mokaair-ai-accounts/agent.sock` prints `travel-api`.

## Notes

- `ops/deployer/travel-scanner-deployer.service` has the same `ExecStartPost` shape, and
  `deployment_agent.server.serve` unlinks and rebinds the same way. It is disabled on this host;
  worth the same one-line fix before anyone enables it.
