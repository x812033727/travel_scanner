---
id: 2026-09-28-offer-claude-fable-show-per-model
title: Offer Claude Fable, show per-model quota, and rotate subscription accounts without MiniMax fallback
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-28T02:21:37Z
created_at: 2026-09-28T02:21:23Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/ai/catalog.py
  - apps/api/app/ai/subscription.py
  - apps/api/ai_accounts_agent
  - apps/api/app/hotspots/ai_search.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/admin/service.py
  - apps/api/app/config.py
  - apps/api/tests/test_ai_subscription.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/api/tests/test_ai_accounts_agent.py
  - apps/api/tests/test_ai_catalog.py
  - apps/api/tests/test_video_automation_subscription.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-ai-model-overview.tsx
  - apps/web/components/admin-ai-model-overview.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - ops/ai-accounts/README.md
---

# Offer Claude Fable, show per-model quota, and rotate subscription accounts without MiniMax fallback

## Why

The owner (2026-09-28) could not pick Fable on the AI settings and saw no Fable quota on the
subscription accounts, and asked that a full account hand over to the next one (A -> B -> ...
-> A) on the same model instead of switching the call to MiniMax.

## Definition of done

- [x] `claude-fable-5-1` is offered wherever a Claude model is chosen, API key or Claude Code
      subscription (news, guide search, introductions, video stages).
- [x] Subscription calls never fall back to MiniMax; `ai_subscription_fallback` is removed and
      a stored value is ignored.
- [x] A per-family limit ("You've hit your Opus limit") moves the run to the next account
      and rests only that family on the spent one.

## Steps

- [x] Catalog entry and tests.
- [x] Remove the fallback from `SubscriptionResearchProvider`, `research_provider`, settings,
      admin card, overview labels and the five locales.
- [x] Agent: broader limit notice, per-family resting, ignore limit words inside long answers.
- [x] README in `ops/ai-accounts`.
- [ ] After deploy: the agent is a host service copied from `apps/api`; reinstall it
      (`ops/ai-accounts/install.sh`) or the family-limit change does not reach the host.

## How to verify

`uv run pytest tests/test_ai_subscription.py tests/test_ai_accounts_agent_runs.py
tests/test_ai_catalog.py tests/test_admin_provider_settings.py`, then on /admin/settings pick
Claude Fable 5.1 for a feature and see it in the video stage dropdown for Claude Code.

## Notes

- Claude Code's status line exposes only `five_hour`, `seven_day` (and `spend_limit` behind a
  gateway). There is no Fable-specific number to record; Fable counts in the shared windows the
  accounts page already shows. Per-family limits appear only as the CLI's limit message.
- Codex: the dropdown already lists the whole OpenAI catalog; Codex reports only its primary and
  secondary windows, which the page shows.
