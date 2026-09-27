---
id: 2026-09-24-roll-out-the-ai-accounts-agent
title: Roll out the AI accounts agent and page on the production host
status: done
priority: P2
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-24T10:51:51Z
created_at: 2026-09-24T09:00:11Z
completed_at: 2026-09-24T10:55:40Z
branch: claude/ai-accounts-rollout
depends_on: []
scope:
  - ops/ai-accounts
---

# Roll out the AI accounts agent and page on the production host

## Why

`2026-09-24-host-agent-that-logs-the-root` (PR #728) adds the host agent and
`2026-09-24-admin-page-to-sign-the-host` adds `/admin/ai-accounts`; both ship inert. Turning
them on changes root's CLI setup on the production host: the existing Claude Code (Max) and
Codex (Pro) logins move into account A behind `/root` links. That needs the owner's go-ahead
for each host step, so it is its own ticket.

## Definition of done

- [x] `mokaair-ai-accounts` is active on the host, and an unsigned request to its socket
      gets 401.
- [x] The deployed API reaches the agent through the Compose mount: from inside the `api`
      container the overview reports the agent reachable, ten slots, and Claude A (Max) and
      Codex A (Pro) signed in. Without a session the route answers 401 and the page
      redirects to the login.
- [x] Plain `claude`/`codex` in a login shell are the default-slot functions and reach the
      same Claude Max login; `codex-a` is signed in with ChatGPT; the legacy
      `/root/.local/bin/claude` with no environment still reaches account A through the
      `/root/.claude` link; `claude-b` is empty.

## Steps

- [x] PRs #728 and #729 merged.
- [x] Installer run on the host from the merged `main` (bundle from `git archive
      origin/main`, before the deploy so one deploy picked up both the mount and the env):
      logins moved into account A behind `/root` links, `.env` stayed mode 600 and gained
      `AI_ACCOUNTS_AGENT_HMAC_KEY` and `AI_ACCOUNTS_ENABLED`, key and emails never printed.
- [ ] `AI_ACCOUNTS_ALLOWED_EMAILS` is still empty; the owner chose to fill it later. The page
      shows the warning until then.
- [x] `systemctl enable --now mokaair-ai-accounts` (after the unit fix below).
- [x] Deployed `d70c08de` (#729): 3/3 health, alembic head `0087_news_needs_evidence_status`,
      homepage 200 in 0.76 s; the deploy also carried #721 to #727.

## How to verify

The "Check it" section of `ops/ai-accounts/README.md`, plus opening `/admin/ai-accounts`.

## Notes

- **The unit failed its first start** with `226/NAMESPACE`: systemd builds the mount
  namespace for `ExecStartPre` as well, and `ReadWritePaths` named
  `/run/mokaair-ai-accounts` before that step had created it. The host unit was patched
  in place and the repo copy gets the same `-` prefix here. The deployment agent's unit has
  the same shape but its installer creates the directory, so it only breaks after a reboot;
  not touched here.
- **The installer now adds a missing final newline** to the runtime env before appending;
  the host run did that by hand first. The production `.env` did end with one.
- **`git show origin/main:path` from Git Bash needs `MSYS_NO_PATHCONV=1`**; without it the
  `origin/main:path` argument became a Windows path list and the first deploy attempt
  never reached the host.
- The agent's first real read took 3 s and did not touch either account's credential file.
