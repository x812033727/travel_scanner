---
id: 2026-09-24-roll-out-the-ai-accounts-agent
title: Roll out the AI accounts agent and page on the production host
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-24T09:00:11Z
completed_at:
branch:
depends_on: []
scope:
  - ops/ai-accounts/README.md
---

# Roll out the AI accounts agent and page on the production host

## Why

`2026-09-24-host-agent-that-logs-the-root` (PR #728) adds the host agent and
`2026-09-24-admin-page-to-sign-the-host` adds `/admin/ai-accounts`; both ship inert. Turning
them on changes root's CLI setup on the production host: the existing Claude Code (Max) and
Codex (Pro) logins move into account A behind `/root` links. That needs the owner's go-ahead
for each host step, so it is its own ticket.

## Definition of done

- [ ] `mokaair-ai-accounts` is active on the host, and an unsigned request to its socket
      gets 401.
- [ ] `/admin/ai-accounts` on mokaair.com shows the existing Claude and Codex logins as
      account A, with Codex quota live and Claude quota after one SSH session.
- [ ] Plain `claude`/`codex` in a new SSH session and `claude-a`/`codex-a` reach the same
      logins as before the move.

## Steps

- [ ] Both PRs merged; deploy with the `deploy` skill (the Compose mount lands with it).
- [ ] With the owner's approval, and no `claude`/`codex` session open on the host:
      `bash ops/ai-accounts/install.sh --runtime-env /root/travel_scanner/.env` from the
      deployed checkout.
- [ ] Owner fills `AI_ACCOUNTS_ALLOWED_EMAILS` in `/etc/travel-scanner/ai-accounts.env`.
- [ ] `systemctl enable --now mokaair-ai-accounts`; recreate the `api` container.
- [ ] Checks from `ops/ai-accounts/README.md`, then sign a second account in from the page.

## How to verify

The "Check it" section of `ops/ai-accounts/README.md`, plus opening `/admin/ai-accounts`.

## Notes

- Codex account A (Pro) read 100 % of its weekly window used on 2026-09-24, resetting
  2026-09-27 03:30 Taipei time; a second Codex account is the first real use of the page.
