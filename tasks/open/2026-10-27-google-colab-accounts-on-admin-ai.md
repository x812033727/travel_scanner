---
id: 2026-10-27-google-colab-accounts-on-admin-ai
title: Google Colab accounts on /admin/ai-accounts with compute units, and a token-paired credential handoff for cloud sessions
status: review
priority: P2
area: api
owner: claude-fable-5-1-colab-accounts
claimed_at: 2026-10-27T23:33:50Z
created_at: 2026-10-27T23:29:19Z
completed_at:
branch: claude/colab-accounts-admin
depends_on: []
scope:
  - apps/api/ai_accounts_agent
  - apps/api/app/admin_ai_accounts
  - apps/api/app/video_speech
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/migrations/versions/0142_video_tool_token_colab_access.py
  - apps/api/tests/test_ai_accounts_colab.py
  - apps/api/tests/test_ai_accounts_admin.py
  - apps/api/tests/test_ai_accounts_agent.py
  - apps/api/tests/test_video_pairing.py
  - ops/ai-accounts
  - apps/web/components/admin-ai-accounts-panel.tsx
  - apps/web/components/admin-ai-accounts-panel.test.tsx
  - apps/web/components/video-tool-tokens.tsx
  - apps/web/components/video-tool-tokens.test.tsx
  - apps/web/app/api/video/colab-credentials
  - apps/web/messages
  - tools/video/tts/cli.mjs
  - tools/video/tts/pairing.mjs
  - tools/video/tts/tts.test.mjs
  - .agents/skills/minimax-h3-colab
  - .claude/skills/minimax-h3-colab
  - tools/minimax-h3-colab.test.mjs
---

# Google Colab accounts on /admin/ai-accounts with compute units, and a token-paired credential handoff for cloud sessions

## Why

After PR #1894 (skill `minimax-h3-colab`: a cloud session drives MiniMax H3 on Colab with a
Colab CLI token stored as an environment secret) the owner asked for the same thing the
admin already does for Claude Code, Codex and Antigravity (2026-10-27: 「我想要有多個google帳號的
管理，就像後台的有多個claude跟codex」「在後台用多個google帳號然後可以看點數google colab」「你透過權杖跟後台
配對來做」): several Google accounts managed on `/admin/ai-accounts`, each showing its Colab
compute units, and the cloud session pairing with the backend through a token instead of
holding a Google token of its own.

## Definition of done

- [x] The host agent has a fourth tool, `colab` (slots A–E, each a HOME of its own): sign-in
      through the Colab CLI's own `accounts.google.com` code paste, the account's email, sign
      out, default slot, and `colab usage` as the status check so each card shows the balance,
      the hourly rate and the running runtimes.
- [x] `/admin/ai-accounts` shows a "Google Colab" section with those cards, in the five locales.
- [x] A paired cloud session gets a signed-in account's `token.json` from the site: a video
      tool token marked `colab_access` (a pairing that asked for Colab with `login --colab`
      and was allowed on the card, or the box when the owner makes a token) calls
      `GET /api/video/colab-credentials?slot=<a-e|default>`; every fetch is audited; tokens
      without the flag get 403; the skill's `bootstrap.sh token` uses it before any secret.
- [x] The host side is installable: `ops/ai-accounts/install.sh` makes the slots, links
      `colab-a` … `colab-e`, moves root's `~/.config/colab-cli` into account A; README updated.
- [x] Tests: the agent with a fake Colab CLI (`tests/test_ai_accounts_colab.py`), the API route
      and pairing flag, the panel and token card, the tool's `--colab`, the bootstrap against a
      fake site.
- [ ] On the host: install google-colab-cli for root, run `install.sh`, sign one account in on
      the page and see its compute units; pair one cloud session with `login --colab` and run
      `bootstrap.sh` there (owner's accounts and compute units; not done from this session).

## Steps

- [x] Agent: `ai_accounts_agent/colab.py`, config, server route `/v1/accounts/colab/<slot|default>/credentials`.
- [x] API: migration 0142 (`video_tool_tokens.colab_access`), pairing/token schemas and flows,
      `admin_ai_accounts` schemas (`compute_units`, `ColabCredentials`), the tool-token route,
      web BFF route `apps/web/app/api/video/colab-credentials`.
- [x] Web: accounts panel (tool, compute units, Colab steps), token card (pairing notice, create
      box, badge), messages ×5.
- [x] Tool and skill: `login --colab`, bootstrap's site route, references.
- [ ] Owner: host install and the first real pairing (above).

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_ai_accounts_colab.py tests/test_ai_accounts_agent.py tests/test_ai_accounts_admin.py tests/test_video_pairing.py tests/test_schema.py -q
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-ai-accounts-panel video-tool-tokens
node --test tools/skills.test.mjs tools/minimax-h3-colab.test.mjs tools/video/tts/tts.test.mjs
```

On the host after deploy: `bash ops/ai-accounts/install.sh --runtime-env /root/travel_scanner/.env`
(with `uv tool install --python 3.12 google-colab-cli` done for root first), restart the
service, open AI 設定 → 訂閱帳號 and sign a Google account in under Google Colab.

## Notes

- Claimed with `--force`: the scope overlaps stale (> 24 h) directory-wide claims of
  `2026-10-12-let-managers-link-a-private-studio` (admin.json ×5),
  `2026-10-19-worker-video-languages-five` (`apps/web/messages`, `apps/api/app/video_speech`,
  `tools/video/tts`) and `2026-10-16-bind-story-audits-and-narration-to` (`tools/video/tts/cli.mjs`,
  `tts.test.mjs`); this ticket touches different lines (new keys, new flags) and the skill
  ticket `2026-10-27-minimax-h3-on-colab-from-a` is this agent's own (release PR #1895).
- The handoff is the one place a credential leaves the host, on purpose and by the owner's
  request. The Colab CLI's token carries Google's `cloud-platform` scope, so the README and the
  sign-in dialog say to use accounts with nothing but a Colab plan (no GCP projects, no billing).
  A leaked video tool token with `colab_access` is revoked on the card like any other.
- `colab usage` refreshes the OAuth token and rewrites `token.json`; two CLIs on one token at
  once can fail the refresh (the Codex failure), so the agent caches the status 300 s and
  refuses the credential handoff while a sign-in holds the account.
- The CLI prints its code prompt without a newline, so its last words follow the prompt on
  the same line; the failure detail reads past the prompt (test: a rejected code names
  `invalid_grant`, masks the email and never echoes the code).
- Not measured here: whether the API container's `urllib` call to `googleapis.com` (the email
  lookup) passes the host's network, and the real CLI's exact output; the fake CLI in the
  tests mirrors google-colab-cli 0.7.5's `auth.py` and `usage` as read on 2026-10-27.
