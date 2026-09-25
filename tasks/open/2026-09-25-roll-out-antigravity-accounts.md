---
id: 2026-09-25-roll-out-antigravity-accounts
title: Roll out Antigravity accounts on the host and check the first sign-in
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-25T12:52:52Z
completed_at:
branch:
depends_on:
  - 2026-09-25-antigravity-subscription-accounts
scope:
  - ops/ai-accounts/README.md
  - apps/api/ai_accounts_agent/antigravity.py
  - apps/api/tests/test_ai_accounts_antigravity.py
---

# Roll out Antigravity accounts on the host and check the first sign-in

## Why

`2026-09-25-antigravity-subscription-accounts` taught the AI accounts agent and
/admin/ai-accounts to sign Google's Antigravity CLI (`agy`) in to the owner's Google AI
Pro/Ultra accounts. The code was built from what agy 1.2.11 showed on the host before any
sign-in, plus the strings in its binary. Three things could only be seen after a real login,
and this rollout is where they are checked:

- which pages agy shows right after the token is saved (onboarding, terms, colour scheme);
- where the account's email and plan appear;
- the exact layout of the `/usage` ("Models & Quota") page, which the probe parses.

Every host step needs the owner's approval (see the `deploy` skill and
`ops/ai-accounts/README.md`).

## Definition of done

- [ ] /admin/ai-accounts shows an Antigravity section, and account A is signed in from the
      page with one of the owner's Google accounts.
- [ ] The card shows the email and the quota windows, matching what `/usage` shows in
      `agy-a` over SSH (compare the percentages and refresh times; they must not be
      inverted between "left" and "used").
- [ ] `agy` over SSH starts on the default account without asking to sign in, and git inside
      it still sees `/root/.gitconfig`.

## Steps

- [ ] Merge the code PR; deploy (skill `deploy`).
- [ ] From the deployed checkout, rerun `bash ops/ai-accounts/install.sh` (it restarts the
      agent). It creates `agy-a` … `agy-e`, the `/root/.gemini/antigravity-cli` link, the
      `agy-?` commands and the `agy()` shell function. agy 1.2.11 is already at
      `/root/.local/bin/agy` (installed 2026-09-25, sha512 checked).
- [ ] Add the owner's Google emails to `AI_ACCOUNTS_ALLOWED_EMAILS` in
      `/etc/travel-scanner/ai-accounts.env` if they differ from the Claude/Codex ones, then
      restart the agent.
- [ ] Owner: sign in Antigravity account A on the page.
- [ ] If the card says the first-run setup is needed, the owner runs `agy-a` once over SSH,
      then presses Refresh on the page.
- [ ] If the card says the quota page could not be read, read
      `journalctl -u mokaair-ai-accounts` for the page the probe saw (emails masked), fix
      `parse_quota` and the fake page in `tests/test_ai_accounts_antigravity.py` to match.
- [ ] Record what the real pages looked like in the Notes of this ticket and in
      `ops/ai-accounts/README.md`.

## How to verify

```bash
# on the host
cd /opt/mokaair-ai-accounts && set -a && . /etc/travel-scanner/ai-accounts.env && set +a
python3 -m ai_accounts_agent.client GET /v1/accounts   # agy-a: logged_in, email masked
journalctl -u mokaair-ai-accounts --since -1h           # no "no quota rows found"
```

Then `agy-a` over SSH, `/usage`, and the page side by side.

## Notes

- The agent answers only the per-folder trust question, and only for its own empty probe
  folder. It never answers terms, colour scheme or telemetry pages; those are the owner's.
- If the login itself fails after the code is pasted, the page shows the last error line
  agy printed; the fallback is `agy-a` over SSH and choosing Google OAuth there.
