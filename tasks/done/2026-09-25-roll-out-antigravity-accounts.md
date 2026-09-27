---
id: 2026-09-25-roll-out-antigravity-accounts
title: Roll out Antigravity accounts on the host and check the first sign-in
status: done
priority: P2
area: ops
owner: claude-opus-5.5
claimed_at: 2026-09-25T13:53:30Z
created_at: 2026-09-25T12:52:52Z
completed_at: 2026-09-25T14:38:16Z
branch: claude/antigravity-quota-page
depends_on:
  - 2026-09-25-antigravity-subscription-accounts
scope:
  - ops/ai-accounts/README.md
  - apps/api/ai_accounts_agent/antigravity.py
  - apps/api/tests/test_ai_accounts_antigravity.py
  - apps/api/ai_accounts_agent/config.py
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

- [x] /admin/ai-accounts shows an Antigravity section, and account A is signed in from the
      page with one of the owner's Google accounts (x812…, Google AI Pro).
- [x] The card shows the email and the quota windows, matching what `/usage` shows in
      `agy-a` over SSH: the page's figures are the share left, and the probe now reads them
      as such, per group and window, with refresh times.
- [x] `agy` over SSH starts on the default account without asking to sign in (the owner ran
      `agy-a` and finished onboarding), and git inside it sees `/root/.gitconfig`.

## Steps

- [x] Merge the code PR; deploy (skill `deploy`). #760 went live as 734298bf, 13:44Z.
- [x] From the deployed checkout, rerun `bash ops/ai-accounts/install.sh` (it restarts the
      agent). It creates `agy-a` … `agy-e`, the `/root/.gemini/antigravity-cli` link, the
      `agy-?` commands and the `agy()` shell function. agy 1.2.11 is already at
      `/root/.local/bin/agy` (installed 2026-09-25, sha512 checked).
- [x] Add the owner's Google emails to `AI_ACCOUNTS_ALLOWED_EMAILS` in
      `/etc/travel-scanner/ai-accounts.env` if they differ from the Claude/Codex ones, then
      restart the agent.
- [x] Owner: sign in Antigravity account A on the page. The login worked at 13:47Z but the
      page reported a failure (see Notes); fixed in the follow-up PR on this branch.
- [x] Deploy the follow-up (#762, 051892d2, 14:28Z), rerun `install.sh`, and check that
      account A shows as signed in with its email.
- [x] The card said first-run setup was needed; the owner ran `agy-a` once over SSH.
- [x] The first readable page was parsed wrong (see Notes). Fixed `parse_quota` for the real
      layout, checked on the host against account A, and kept the page as a test fixture.
- [x] Record what the real pages looked like in the Notes of this ticket and in
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

- 2026-09-25, first real sign-in (account A, 13:47Z): agy 1.2.11 saved the login to
  `~/.gemini/antigravity-cli/antigravity-oauth-token`, not `jetski-standalone-oauth-token`
  (that name came from a report about an older version). The agent waited 90 s for the wrong
  file and reported a failure although the log said "OAuth: authenticated successfully as
  …@gmail.com" ("ChainedAuth: authenticated via keyring (effective: keyring)" is printed
  even when the file fallback served it). Two more clicks on the page then got a 503: agy
  with a saved login opens on its TUI, never printing a URL, and the agent waited 30 s, past
  the API's 25 s timeout, while holding the login registry lock (overview requests broke
  with BrokenPipe in the journal). Fix: both file names count, "sign in again" sets the
  saved login aside and restores it when the new one does not finish, and the URL wait is
  15 s. A clean login printed its URL in 0.5 s inside the systemd sandbox.
- After that login `cache/onboarding.json` says `"consumerOnboardingComplete": false`, so the
  first probe is expected to stop at a first-run page (`setup_needed`) until the owner runs
  `agy-a` once.
- 14:33Z, first readable quota page: the old parser took "Models within this group: …" as
  the label, found no window lengths or refresh times, and made a window of the "Quota
  available" line, because agy puts the window name on the line above the bar and the
  refresh time on the line below. The rewritten parser follows the group heading → name
  line → bar → refresh line structure; run against account A on the host it read Gemini
  weekly 99.93 % / five-hour 99.58 % left and Claude/GPT 100 %, matching `/usage`.
- The plan comes from the header ("Gemini 3.8 Flash (High) (Google AI Pro)"); the email
  from the header and from the log line.
- Allowlist (owner's choice): x812033727, s812033727, z812033727 @gmail.com and the two
  Apple private-relay addresses of Claude D and Codex D.
- The agent answers only the per-folder trust question, and only for its own empty probe
  folder. It never answers terms, colour scheme or telemetry pages; those are the owner's.
- If the login itself fails after the code is pasted, the page shows the last error line
  agy printed; the fallback is `agy-a` over SSH and choosing Google OAuth there.
