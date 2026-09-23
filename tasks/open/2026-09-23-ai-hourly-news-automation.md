---
id: 2026-09-23-ai-hourly-news-automation
title: AI hourly multilingual news automation
status: in-progress
priority: P1
area: api
owner: codex
claimed_at: 2026-09-23T12:30:56Z
created_at: 2026-09-23T12:28:42Z
completed_at:
branch: codex/ai-news-automation
depends_on: []
scope:
  - apps/api/app/news_automation
  - apps/api/app/main.py
  - apps/api/app/worker.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/admin/operations_service.py
  - apps/api/app/i18n.py
  - apps/api/migrations/versions/0084_ai_news_automation.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_admin.py
  - apps/api/tests/test_guides_publish_bundle.py
  - apps/api/tests/test_admin_operations.py
  - apps/web/app/[locale]/admin/news
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news.ts
  - apps/web/lib/admin-news-copy.ts
  - apps/web/lib/admin-operations.ts
  - apps/web/lib/admin-workspace-navigation.ts
  - apps/web/lib/admin-workspace-navigation.test.ts
  - apps/web/components/admin-nav.tsx
  - apps/web/components/admin-nav.test.tsx
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/travel/[...path]/route.test.ts
  - apps/web/app/guides/news-assets/[filename]/route.ts
  - docker-compose.yml
  - docker-compose.prod.yml
---

# AI hourly multilingual news automation

## Why

Mokaair currently publishes multilingual news from source-controlled packs and human-run
imports. Add a disabled-by-default hourly automation that discovers allow-listed news,
keeps evidence and model decisions auditable, drafts all five locales, asks Jev for the
final editorial decision, and either atomically publishes the five-locale bundle or
routes it to an admin review queue.

## Definition of done

- [ ] Enabled sources can be scheduled hourly without overlapping scans; hostile URLs,
      redirects, robots failures and unsupported bodies fail closed.
- [ ] Candidates retain evidence, deterministic duplicate keys, stage attempts and
      five-locale drafts; no failed stage can become published.
- [ ] Jev act/confirm/hold/error outcomes map to shadow/manual/published exactly as the
      approved state machine requires, and five locales publish in one transaction.
- [ ] Administrators can manage sources/settings and review, retry, reject or publish a
      candidate from `/admin/news`; the navigation badge shows pending review work.
- [ ] Brand assets have stable same-origin URLs and the BFF streams only allowed image
      content types; the feature and all vertical auto-publish switches ship off.
- [ ] Focused API and web tests cover security, idempotency, rollback and review flows.

## Steps

- [ ] Add schema, state machine, safe fetch/feed parsing, scheduler/jobs and AI/Jev stages.
- [ ] Add atomic guide bundle publication, admin API, asset endpoint and audit metadata.
- [ ] Add the five-language admin workspace, review badge and binary asset proxy.
- [ ] Add disabled scheduler services, focused tests and repository checks.

## How to verify

```bash
cd apps/api && uv run ruff check app/news_automation tests/test_news_automation.py tests/test_news_admin.py tests/test_guides_publish_bundle.py
cd apps/api && uv run mypy app && uv run pytest tests/test_news_automation.py tests/test_news_admin.py tests/test_guides_publish_bundle.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
npm run test:web -- admin-news-workspace admin-nav admin-workspace-navigation
npm run check:tasks
```

## Notes

- The existing Jev advisory task still owns `app/ai/jev.py`; this task only calls its
  public client/quota/routing API and does not edit that file.
- `models.py` and the shared five `admin.json` files were deliberately removed from
  scope because the already-merged merchant-platform task still claims them. News ORM
  models and localized copy live inside the new module instead.
- No production deploy, migration, source activation or auto-publish activation is part
  of this task.
