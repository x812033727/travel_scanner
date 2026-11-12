---
id: 2026-11-12-colab-account-leases-parallel-agents
title: Each Colab account works on its own: a site-held lease per account so parallel agents never share one, and a per-account CLI home
status: review
priority: P2
area: api
owner: claude-opus-5-5-colab-leases
claimed_at: 2026-11-12T23:29:13Z
created_at: 2026-11-12T23:29:00Z
completed_at:
branch: claude/zealous-ritchie-yipfth
depends_on: []
scope:
  - apps/api/app/admin_ai_accounts
  - apps/api/app/main.py
  - apps/api/tests/test_ai_accounts_admin.py
  - apps/api/tests/test_ai_accounts_colab_leases.py
  - apps/web/app/api/video/colab-accounts
  - apps/web/app/api/video/colab-credentials
  - .agents/skills/minimax-h3-colab/SKILL.md
  - .agents/skills/minimax-h3-colab/references/cloud-pairing.md
  - .agents/skills/minimax-h3-colab/scripts
  - .claude/skills/minimax-h3-colab/SKILL.md
  - tools/minimax-h3-colab.test.mjs
---

# Each Colab account works on its own: a site-held lease per account so parallel agents never share one, and a per-account CLI home

## Why

The owner signs several Google accounts in on `/admin/ai-accounts` (Colab slots A–E) and wants
different agents to make videos at the same time, each on an account of its own (2026-11-12:
「幫我做成每個帳號都可以獨立製作，讓我不同的agent可以做不同帳號的colab」). Before this, a paired
session could already fetch any slot's `token.json` with `COLAB_ACCOUNT_SLOT`, but nothing stopped
two agents from picking the same account (they then fight over its GPU and its concurrent-runtime
limit), an agent could not see the balances to choose, and two agents on one machine overwrote
each other's `~/.config/colab-cli/token.json` (the CLI has no flag to move it).

## Definition of done

- [x] The site holds one lease per Colab account: `GET /api/video/colab-accounts` (balances,
      signed in, holder; never an email or credential), `POST …/{a-e|auto}/lease` (take or renew;
      `auto` = the free signed-in account with the most compute units, or the one the holder has),
      `POST …/{slot}/lease/release` (holder only). Redis WATCH/MULTI, so two agents racing for one
      account get one lease. Every change is audited with holder and token prefix.
- [x] `colab-credentials` refuses an account another holder leased (409 `colab_account_leased`),
      and takes an optional `holder`.
- [x] `scripts/accounts.py` (list, claim, renew, release, env) writes the account's token into a
      HOME of its own and a `colab` shim; `h3.sh`, `h3_detached.py`, `images.py`, `colab_detached.py`
      pick the account by `COLAB_ACCOUNT_SLOT`; `h3_detached.py` renews every 30 minutes;
      `bootstrap.sh` leases when `COLAB_ACCOUNT_HOLDER` is set.
- [x] Tests: API (`test_ai_accounts_colab_leases.py`, fakeredis, including a six-way race), tools
      (two agents on one machine, h3.sh and the Python scripts run the CLI in the leased account's HOME).
- [x] Skill: SKILL.md rule 1 and the flow, cloud-pairing.md §2b.
- [ ] On the host after deploy: two cloud sessions each `accounts.py claim`, `list` shows both
      holders, each runs `h3.sh usage` on its own account (owner's accounts; not done from this session).

## Steps

- [x] API: `admin_ai_accounts/colab_leases.py`, schemas, routes in `router.py`, `main.py`.
- [x] Web BFF: `apps/web/app/api/video/colab-accounts/**`, `holder` on `colab-credentials`.
- [x] Skill scripts and docs.
- [ ] Deploy and the host check above.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_accounts_colab_leases.py tests/test_ai_accounts_admin.py
node --test tools/minimax-h3-colab.test.mjs
npm run lint:web && npm run typecheck:web
```

## Notes

- Leases live in Redis only (no migration): an expired lease frees the account by itself, and a
  Redis outage makes the lease routes and the credentials route answer 503 `colab_lease_unavailable`.
- The holder name is the agent's board-claim name; nothing checks it beyond the pattern. It is
  coordination between cooperating agents, not a security boundary: every agent uses the same
  owner-issued video tool token anyway.
- `npm run test:tools` has 16 failures that are identical on the untouched tree (checked with
  `git stash`), none in `minimax-h3-colab.test.mjs`.
- Not done here: the admin card does not show who leases an account, and the owner cannot break
  a lease from the page (filed as 2026-11-12-admin-colab-card-shows-lease-holder).
