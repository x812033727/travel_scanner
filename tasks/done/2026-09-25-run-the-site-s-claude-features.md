---
id: 2026-09-25-run-the-site-s-claude-features
title: Run the site's Claude features on the host's subscription accounts
status: done
priority: P1
area: api
owner: claude-opus-5-5-news-subscription
claimed_at: 2026-09-25T12:49:48Z
created_at: 2026-09-25T12:49:43Z
completed_at: 2026-09-26T00:56:13Z
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

- [x] The "AI vendors" card has a Claude connection setting (API key or subscription accounts)
      and a usage cap. Only the owner can change them.
- [x] In subscription mode, the guide search, intros, guide review, simplified names, news and
      video "anthropic" stages all run through the agent. When no account can serve, they fall
      back to MiniMax.
- [x] Two runs can go at once on different accounts, and a run that hits the limit moves on to
      the next account instead of pausing the whole request.
- [x] The worker and news-worker containers can reach the agent's socket.
- [x] Readiness checks and the card's connection test understand subscription mode.

## Steps

- [x] Agent: per-account concurrency, a bounded wait, and rotation when a run hits the limit.
- [x] Site: the connection setting, `vendor_ready`, `SubscriptionResearchProvider`, and the
      MiniMax fallback.
- [x] Admin card, readiness checks, connection test, and web copy in five languages.
- [x] Compose mounts, docs, and tests.

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
- Merged as #761 and live since the deploy of 5591af82 on 2026-09-26. The agent in /opt was
  reinstalled at 00:37 UTC that day with the per-account runs; #774 then changed the pick to
  "each account until it is full, A -> B -> ... -> A".
- Probe on 2026-09-26 from the news-worker container through the socket: account C,
  claude-sonnet-5, 4 s. Asked to read /etc/hostname and run `id`, it answered "unavailable"
  for both, so the model has no tools.
- The card still said 「Claude 連線方式: API 金鑰」 after the deploy; the owner switches it.
