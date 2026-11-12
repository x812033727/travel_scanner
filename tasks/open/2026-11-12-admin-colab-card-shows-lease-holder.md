---
id: 2026-11-12-admin-colab-card-shows-lease-holder
title: Admin Colab card shows which agent leases each account and lets the owner end a lease
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-11-12T23:49:32Z
completed_at:
branch:
depends_on:
  - 2026-11-12-colab-account-leases-parallel-agents
scope:
  - apps/web/components/admin-ai-accounts-panel.tsx
  - apps/web/components/admin-ai-accounts-panel.test.tsx
  - apps/web/messages
  - apps/api/app/admin_ai_accounts
---

# Admin Colab card shows which agent leases each account and lets the owner end a lease

## Why

2026-11-12-colab-account-leases-parallel-agents lets several agents each lease a Colab account
on the site (Redis, `admin_ai_accounts/colab_leases.py`). Agents see the holders with
`accounts.py list`, but the owner's `/admin/ai-accounts` Colab cards do not: the owner cannot see
which agent is on which account, and a lease left by a crashed agent can only run out (up to 24 h).

## Definition of done

- [ ] Each Colab card shows the holder, the token prefix and the expiry when the account is leased.
- [ ] The owner can end a lease from the card (owner-only route, audited `ai_account.colab_lease_broken`).
- [ ] Copy in the five locales; panel test covers both.

## Steps

- [ ] API: add the leases to the admin overview (or a sibling route) and a break-lease route.
- [ ] Web: card line and button, messages.

## How to verify

`npm run test:web -- admin-ai-accounts-panel`, `cd apps/api && uv run pytest tests/test_ai_accounts_admin.py`.

## Notes

The agent-facing view (`ColabAccounts`) deliberately carries no email; the admin one may.
