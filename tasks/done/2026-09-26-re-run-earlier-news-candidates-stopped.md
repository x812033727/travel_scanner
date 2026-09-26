---
id: 2026-09-26-re-run-earlier-news-candidates-stopped
title: Re-run earlier news candidates stopped by old rules, and wait for subscription accounts instead of MiniMax
status: done
priority: P1
area: api
owner: claude-opus-5-5-news-final-editor
claimed_at: 2026-09-26T07:14:15Z
created_at: 2026-09-26T07:14:03Z
completed_at: 2026-09-26T07:22:37Z
branch: claude/news-backfill-and-wait
depends_on: []
scope:
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/jobs.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/app/admin/service.py
  - apps/api/app/config.py
  - apps/api/tests/test_news_backfill_cli.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_ai_subscription.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/news-automation.md
---

# Re-run earlier news candidates stopped by old rules, and wait for subscription accounts instead of MiniMax

## Why

On 2026-09-26 the owner noticed that the hourly news had produced almost nothing for days,
and asked to backfill the earlier stories as practice. 201 candidates had stopped because
evidence from one website was not enough (the rule until 2026-09-25), or because MiniMax's
drafts, checks or translations failed. 127 of them were published after 2026-09-15. Their
evidence is still stored. The owner chose to rerun all 127. When the Claude accounts are
full, the accounts should take turns and the run should wait, not switch to MiniMax.

## Definition of done

- [x] `backfill_cli --since` lists the pool: first-party stories first, then the newest.
      With `--apply` it reopens each one as a new draft with an audit row and queues it.
- [x] 「訂閱帳號都滿時」 (`ai_subscription_fallback`, owner only) chooses between MiniMax
      and waiting. When it waits, a news candidate goes back to the queue as
      `news_subscription_paused` and is tried again every 30 minutes.

## How to verify

`uv run pytest tests/test_news_backfill_cli.py tests/test_news_pipeline.py tests/test_ai_subscription.py`

## Notes

- After deploy: switch the card to 「等帳號恢復」, then run
  `backfill_cli --since 2026-09-15 --apply --actor-email <admin>`.
