---
id: 2026-09-25-rotate-subscription-accounts-in-slot-order
title: Rotate subscription accounts in slot order, staying on one until it is full
status: done
priority: P1
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-25T15:13:54Z
created_at: 2026-09-25T15:12:15Z
completed_at: 2026-09-25T15:24:20Z
branch: claude/quota-rotation-logic-e8f23f
depends_on: []
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/ai_accounts_agent/config.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - ops/ai-accounts/README.md
---

# Rotate subscription accounts in slot order, staying on one until it is full

## Why

The host's AI accounts agent picks which Claude subscription runs a site prompt. Since #761 it
takes the account with the lowest usage every time, so every account is worn down together and
all of them reach their cap around the same moment. The owner asked on 2026-09-25 for a
rotation instead: keep using one account until it is full, then move to the next slot, and
after the last slot come back to A (A -> B -> C -> ... -> A).

## Definition of done

- [x] A run uses the current account until it is at the cap or its run reports the limit.
- [x] Then the next signed-in slot in order takes over, wrapping from E back to A, and the
      agent remembers the current account across restarts (`current-{tool}` in the state root).
- [x] A busy current account sends a parallel run to the next slot without moving the pointer.
- [x] Setting the default account on /admin/ai-accounts restarts the rotation there.
- [x] The rotation is written per tool, so Codex runs use it when they are offered.

## Steps

- [x] `pick_slot` walks the slots from the current one; unknown usage counts as room.
- [x] Server keeps `current-{tool}`, advances it when the current account is spent.
- [x] Tests and the README's state file list.

## How to verify

`cd apps/api && uv run pytest tests/test_ai_accounts_agent_runs.py tests/test_ai_subscription.py`.
After the agent is redeployed on the host, `cat /var/lib/mokaair-ai-accounts/current-claude`
shows the account in use, and it changes only when that account fills up.

## Notes

- Claimed with --force: the overlapping ticket `2026-09-25-run-the-site-s-claude-features`
  landed its code in #761 and is only waiting on its rollout check; no branch touches these
  files.
- The pointer moves only when the current account is not busy and was passed over, so a
  parallel run on the next slot never steals the turn. Unknown usage (right after sign-in)
  now counts as room, because the slot order is what decides.
- The overview now carries `current` next to `defaults`; the admin page does not show it yet.
