---
id: 2026-09-24-host-agent-that-logs-the-root
title: Host agent that logs the root CLIs into two Claude and two Codex subscription accounts
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-24T08:14:39Z
created_at: 2026-09-24T08:13:58Z
completed_at: 2026-09-24T08:36:46Z
branch: claude/ai-accounts-agent
depends_on: []
scope:
  - apps/api/ai_accounts_agent
  - apps/api/tests/test_ai_accounts_agent.py
  - ops/ai-accounts
---

# Host agent that logs the root CLIs into two Claude and two Codex subscription accounts

## Why

The site owner uses Claude Code and the Codex CLI as root over SSH on the production host,
billed to their Claude and ChatGPT subscriptions rather than API keys. Until now each login
was done by hand in an SSH session (Claude with `/login`, Codex with
`codex login --device-auth`), there was room for one account per tool, and the remaining
quota could only be seen inside a running CLI.

The owner asked for three things: to do the login from the admin site, to keep several accounts
per tool (two at first, then "even three"; the agent allows five, slots a-e) with a default that plain `claude` and `codex` use in SSH plus
`claude-a`…`codex-e` to pick one, and to see each account's name and remaining quota.

The API container cannot reach the host, and must not get the CLIs or their credentials.
This ticket is the host half, built the same way as the deployment agent
(`ops/deployer/`, `apps/api/deployment_agent/`): a root systemd service that only answers a
fixed set of HMAC-signed requests on a Unix socket the API container can open. The admin page
and API routes are a separate ticket.

Facts checked on the host on 2026-09-24, so nobody has to rediscover them:

- `claude auth login --claudeai` with no browser prints the authorize URL (wrapped in an OSC 8
  hyperlink escape) and waits at `Paste code here if prompted >`, reading the code from the TTY.
- `claude auth status --json` returns `loggedIn`, `authMethod`, `email`, `orgName`,
  `subscriptionType`. `CLAUDE_CONFIG_DIR` relocates `.claude.json` too, so it is the documented
  way to keep two logins apart.
- Claude has no documented way to read plan usage outside a session. The status line input has
  `rate_limits.five_hour|seven_day.{used_percentage,resets_at}` for Pro/Max after the first API
  response of an interactive session, so a status line recorder writes the latest snapshot per
  account. The owner chose this over Anthropic's undocumented usage endpoint.
- `codex app-server` (0.156.1) speaks JSON-RPC over stdio: `account/read` (email, planType),
  `account/rateLimits/read` (primary/secondary windows with `usedPercent`, `resetsAt`),
  `account/login/start {type:"chatgptDeviceCode"}` → `verificationUrl`, `userCode`,
  `account/login/completed`, `account/login/cancel`, `account/logout`. `CODEX_HOME` separates
  accounts.

## Definition of done

- [x] A signed `GET /v1/accounts` over the socket lists ten slots (two tools, a-e) with
      logged-in state, email, plan and quota windows; an unsigned, replayed, skewed or
      tampered request gets 401 (tests, including a real Unix socket on Linux).
- [x] A login for any slot can be started, completed and cancelled through the socket alone:
      Codex by device code, Claude by returning the authorize URL and accepting the pasted
      code (tests with fake CLIs; the real CLIs were probed on the host with throwaway dirs).
- [x] A login that ends on an account outside `AI_ACCOUNTS_ALLOWED_EMAILS` is signed out
      again, and the pasted code never comes back in any response.
- [x] The installer moves the existing logins into slot A behind `/root` links, installs
      `claude-a`…`codex-e`, the default-slot shell functions and the unit, and never prints
      the key. Running it on the host belongs to the rollout of the follow-up ticket.

## Steps

- [x] `ai_accounts_agent` package: config, HMAC, Codex app-server client, Claude PTY login,
      status line recorder, login sessions, HTTP server, host client for checks.
- [x] `ops/ai-accounts`: systemd unit, installer, account commands, profile snippet, README
      with the trust boundary and the undo steps.
- [x] Tests with fake CLIs for both login flows, the signature checks and the recorder.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests   && uv run pytest tests/test_ai_accounts_agent.py
```

Four tests need a POSIX terminal or Unix socket and skip on Windows; CI runs them. On this
Windows machine they ran in WSL with the venv's pure-Python pytest on `PYTHONPATH`
(28 passed).

## Notes

- Probed on the host on 2026-09-24 with throwaway state directories under /tmp, touching no
  real login: Codex status 0.3 s, device code start and cancel work; Claude status 0.2 s,
  the authorize URL comes out of the OSC 8 hyperlink in 0.2 s, cancel ends the CLI (143).
- A read of the existing Codex login showed the Pro plan has one weekly window
  (`windowDurationMins` 10080, `secondary` null) and `resetsAt` in seconds; the read did not
  touch `auth.json`.
- `codex app-server` writes sqlite files, a `.tmp` and bundled skills into `CODEX_HOME` on
  first start; that is why every slot is a directory of its own.
- `apps/api/pyproject.toml` is in the scope of `2026-09-14-redis-py-8-migration`, so the
  package carries inline `# noqa` for the bandit rules it needs instead of a per-file entry.
- Do not set `MemoryDenyWriteExecute` in the unit: the Codex node wrapper and the Bun-built
  Claude binary both need JIT. Do not use `RuntimeDirectory=`: it removes the socket
  directory on stop and strands the API container's bind mount.
- Plain `claude`/`codex` from scripts, cron or `ssh host cmd` keep using account A through
  the `/root` links; only interactive shells follow the default. That was chosen over
  moving a `default` symlink, which would let a running session write its refreshed token
  into another account's directory after a switch.
