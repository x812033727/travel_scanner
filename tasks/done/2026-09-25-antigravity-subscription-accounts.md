---
id: 2026-09-25-antigravity-subscription-accounts
title: Sign the host's Antigravity CLI (agy) in to subscription accounts from AI settings
status: done
priority: P2
area: ops
owner: claude-opus-5.5
claimed_at: 2026-09-25T12:18:47Z
created_at: 2026-09-25T12:18:33Z
completed_at: 2026-09-25T13:00:12Z
branch: claude/antigravity-subscription-quota-2ecb59
depends_on: []
scope:
  - apps/api/ai_accounts_agent/config.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/ai_accounts_agent/runner.py
  - apps/api/ai_accounts_agent/security.py
  - apps/api/ai_accounts_agent/antigravity.py
  - apps/api/ai_accounts_agent/screen.py
  - apps/api/app/admin_ai_accounts/schemas.py
  - apps/api/tests/test_ai_accounts_agent.py
  - apps/api/tests/test_ai_accounts_antigravity.py
  - apps/api/tests/test_ai_accounts_admin.py
  - apps/web/components/admin-ai-accounts-panel.tsx
  - apps/web/components/admin-ai-accounts-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - ops/ai-accounts
---

# Sign the host's Antigravity CLI (agy) in to subscription accounts from AI settings

## Why

The owner asked on 2026-09-25 to use their Google AI Pro/Ultra subscriptions for Gemini
models on the host, the way /admin/ai-accounts already does for Claude Code and Codex: sign
in on the web page, up to five accounts, see each one's remaining quota, pick a default,
and run `agy` / `agy-b` over SSH.

- Gemini CLI can no longer do this: Google stopped serving Pro/Ultra through its "Login with
  Google" on 2026-06-18. The official replacement is the Antigravity CLI, `agy`.
- The owner chose "host use only". The site's own Gemini features keep their API key:
  Antigravity's terms (section 6) forbid using the service with products Google does not
  provide, and paid accounts were banned without refund for it in 2026-02 and 2026-09. The
  agent therefore only drives the official binary (login, `/usage`), never takes its token
  to call Google itself, and `/v1/runs` stays Claude-only.

## Definition of done

The code half. Checking it against a real account on the host is
`2026-09-25-roll-out-antigravity-accounts`.

- [x] /admin/ai-accounts shows an Antigravity section next to Claude Code and Codex.
- [x] Signing in from the page: the agent picks Google OAuth, the page shows Google's sign-in
      link, the owner pastes the code (it contains `/`), and the saved token file decides
      the outcome; the card then shows the email from agy's log.
- [x] Each signed-in account shows its quota windows (per model group) read from agy's own
      `/usage` page on the Claude probe schedule, and the refresh button re-reads them.
- [x] `agy` over SSH uses the default account; `agy-a` … `agy-e` pick one; each account is a
      home of its own with `/root`'s git, GitHub and npm settings linked in.
- [x] The host allowlist signs an account outside `AI_ACCOUNTS_ALLOWED_EMAILS` out again, and
      with a list set, a login whose email cannot be read is signed out too.

## Steps

- [x] Agent: `antigravity.py` backend (PTY login, token-file status, `/usage` probe) and a
      stdlib screen renderer (`screen.py`); `TOOLS` gains `agy`; routes built from `TOOLS`;
      usage probing keyed by tool.
- [x] API schema: `Tool` gains `agy`, the code pattern allows `/`, windows carry a label.
- [x] Web panel and five locales (also corrects "the site's features never use these
      accounts": video automation's writing uses the Claude accounts since #757).
- [x] ops: slot homes, `agy-[a-e]` wrappers, `agy()` shell function, installer, README.
- [x] Tests: `test_ai_accounts_antigravity.py` (a fake agy in a real PTY: login, rejected
      code, allowlist, trust prompt, first-run page, quota page), updated agent, admin and
      panel tests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_accounts_agent.py tests/test_ai_accounts_antigravity.py tests/test_ai_accounts_admin.py
npm run test:web -- admin-ai-accounts-panel
```

The PTY tests skip on Windows; on this machine they ran in WSL (52 passed).

## Notes

Probed 2026-09-25 with agy 1.2.11 (linux_amd64, installed at `/root/.local/bin/agy` with the
owner's approval; the installer's `agy install` step, which edits shell rc files, was not run):

- A fresh HOME shows "Welcome to the Antigravity CLI. You are currently not signed in." and
  "Select login method: > 1. Google OAuth / 2. Use a Google Cloud project"; Enter picks OAuth.
- It then prints an OSC 8 link to `https://accounts.google.com/o/oauth2/auth?…` with
  `redirect_uri=https://antigravity.google/oauth-callback`, PKCE and `access_type=offline`,
  and waits at "If you aren't automatically redirected, paste the authorization code below:".
- The token goes to the Secret Service keyring when one answers, otherwise (strings in the
  binary: "Failed to save token to keyring, falling back to file") to
  `$HOME/.gemini/antigravity-cli/jetski-standalone-oauth-token`. The host has no keyring
  daemon; the wrappers and the agent point `DBUS_SESSION_BUS_ADDRESS` at nothing so every
  account always uses its file.
- The config directory is fixed at `~/.gemini/antigravity-cli/` with no env override, so
  each account slot is a HOME of its own.
- After login the language server logs "OAuth: authenticated successfully as <email>" to
  `~/.gemini/antigravity-cli/cli.log`; the TUI header shows the email and plan tier.
- Quota: the "Models & Quota" page (`/usage`, `/quota`) comes from `RetrieveUserQuotaSummary`
  (groups of buckets with `remaining_fraction` and `reset_time`), drawn with "Refreshes in".
  `agy -p /usage` was reported to send "/usage" to the model as a prompt, so the probe opens
  the TUI instead.
- Other strings in the binary the probe relies on: "Do you trust the contents of this
  project?" / "Yes, I trust this folder" (answered, for the probe's own empty folder only),
  and the first-run pages "Choose your color scheme:", "Terms and Privacy:" and "Yes, I agree
  to help improve …" (never answered; the page asks the owner to run `agy-<slot>` once).
- A percentage on the quota page is read as the share left unless the row says "used"; the
  quota service reports `remaining_fraction`. Unverified until the rollout.
- Not yet seen: the screens after a real login and the exact `/usage` layout. The probe logs
  the rendered screen (emails masked) to the journal when it cannot parse it; the owner's
  first login from the page is the check (rollout ticket).
- Gemini CLI (0.58.0 on the host) is not an alternative: its "Login with Google" stopped
  serving Pro/Ultra on 2026-06-18.
