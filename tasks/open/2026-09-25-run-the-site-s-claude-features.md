---
id: 2026-09-25-run-the-site-s-claude-features
title: Run the site's Claude features on the host's subscription accounts
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-news-subscription
claimed_at: 2026-09-25T12:49:48Z
created_at: 2026-09-25T12:49:43Z
completed_at:
branch: claude/site-ai-on-claude-subscription
depends_on: []
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/app/ai/subscription.py
  - apps/api/app/admin_ai_accounts/agent.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/app/admin/service.py
  - apps/api/app/config.py
  - apps/api/app/news_automation/settings_cli.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/api/tests/test_ai_subscription.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_ai_accounts_admin.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docker-compose.prod.yml
  - ops/ai-accounts/README.md
  - docs/news-automation.md
---

# Run the site's Claude features on the host's subscription accounts

## Why

The owner decided on 2026-09-25 that every site feature that uses Claude should run on the
Claude subscription accounts the host signs in at /admin/ai-accounts, not on an API key. The
site has no Anthropic key, so choosing a Claude model for the news writer failed every
candidate. When every account is at its cap, the call falls back to MiniMax. The owner was
told about the terms, quota and speed risks first and chose this anyway.

The video pipeline (#756) already added `POST /v1/runs` to the host agent: Claude Code with
every tool off, on the signed-in account with the most room below a cap. This task reuses
that route for the rest of the site.

## Definition of done

- [ ] The "AI vendors" card has a Claude connection setting (API key or subscription accounts)
      and a usage cap. Only the owner can change them.
- [ ] In subscription mode, the guide search, intros, guide review, simplified names, news and
      video "anthropic" stages all run through the agent. When no account can serve, they fall
      back to MiniMax.
- [ ] Two runs can go at once on different accounts, and a run that hits the limit moves on to
      the next account instead of pausing the whole request.
- [ ] The worker and news-worker containers can reach the agent's socket.
- [ ] Readiness checks and the card's connection test understand subscription mode.

## Steps

- [ ] Agent: per-account concurrency, a bounded wait, and rotation when a run hits the limit.
- [ ] Site: the connection setting, `vendor_ready`, `SubscriptionResearchProvider`, and the
      MiniMax fallback.
- [ ] Admin card, readiness checks, connection test, and web copy in five languages.
- [ ] Compose mounts, docs, and tests.

## How to verify

- `uv run pytest tests/test_ai_accounts_agent_runs.py tests/test_ai_subscription.py tests/test_admin_provider_settings.py`
- After deploy: switch Claude to subscription on /admin/settings, set the news writer to Claude
  Opus 5.5, and press "not a duplicate" on one candidate. A zh-TW draft appears, and its run
  shows claude-opus-5-5.

## Notes

- Codex is not offered. `codex exec` keeps a shell (see `ai_accounts_agent/runs.py`). Its
  `--disable shell_tool` and web-search flags could not be tried on 2026-09-25 because every
  Codex account was at 100% until 9/27. That work has its own ticket.
- The reader-facing planner and the trip parser are out of scope; they get a separate ticket.
