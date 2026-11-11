---
id: 2026-11-10-news-freshness-advisory
title: Flag published news source changes for editorial review
status: done
priority: P1
area: api
owner: codex-news-freshness
claimed_at: 2026-11-10T12:52:52Z
created_at: 2026-11-10T12:52:50Z
completed_at: 2026-11-10T13:27:43Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - apps/api/app/news_automation/freshness.py
  - apps/api/app/news_automation/router.py
  - apps/api/app/news_automation/jobs.py
  - apps/api/app/news_automation/scheduler.py
  - apps/api/tests/test_news_freshness.py
  - apps/api/tests/test_news_freshness_integration.py
  - apps/web/app/[locale]/admin/news/page.tsx
  - apps/web/components/admin-news-editorial.tsx
  - apps/web/components/admin-news-editorial.test.tsx
  - apps/web/lib/news-editorial-messages
  - apps/web/lib/news-editorial.ts
  - docs/news-reader-enhancements/freshness.md
  - docs/news-reader-enhancements/README.md
---

# Flag published news source changes for editorial review

## Why

Published news can keep pointing at changed sources. Editors need a bounded, visible
review queue without refreshing publication evidence, extending excerpt retention or
triggering another paid drafting cycle.

## Definition of done

- [x] An enabled news scheduler performs bounded advisory checks and exposes outcomes.
- [x] Editors can filter overdue/changed articles and page through every matching result.
- [x] Real PostgreSQL tests prove concurrency limits and protected article/evidence state.
- [x] Five-language UI and independent review pass; the PR records its separate CI gate.

## Steps

- [x] Audit exact scopes; integrate a separate component at the unheld admin route.
- [x] Use transient evidence copies and existing safe validation; store only advisory receipts.
- [x] Add a transactional daily cap, candidate/day identity and bounded network time.
- [x] Fix review findings: due pagination, corrupt receipt isolation, precise coverage wording.
- [x] Complete integration and browser validation; retain fixed review/test evidence for the PR.

## How to verify

API: pytest tests/test_news_freshness.py tests/test_news_freshness_integration.py,
the latter with RUN_INTEGRATION_TESTS=1 against local isolated PostgreSQL.
Web: vitest components/admin-news-editorial.test.tsx; lint, i18n and typecheck.
Open admin news, expand source review, filter due/changed, page and follow an article.

## Notes

2026-11-10: The owner requested all six news improvements. This task changes no production
settings, publication records or evidence baselines. Global news automation controls
the scheduled check. Scope covers pipeline-created published news in the last 90 days,
including articles approved by a person. Each attempted article waits seven days,
including unsuccessful or interrupted attempts; uncertainty remains visible to editors.
The maximum is 20 reservations per UTC day across workers, four sources per article,
25 seconds per article and a 540-second batch budget. No model calls or automatic retries.

Initial Windows-to-WSL service connection failed; those failures remain in the local
test log. A separate Linux runner and isolated test services were prepared, and the
Windows venv subsequently reached those services for the final tests. The three owned
test containers were stopped after validation; their data was retained. No production
service was contacted or changed.

Final local validation: 17/17 tests, including six real PostgreSQL cases, passed both
the author and independent reviewer runs. The old midnight race was independently
reproduced before the fix; the final version allows only one reservation. API-wide
Ruff and mypy app/tests passed. Eight UI tests and the shared production build passed.
The final browser capture covers all five locales, desktop/390/320 and dark mode,
including due filtering, page two and valid candidate links; independent visual review
passed. CI on the resulting PR head remains a separate required merge gate.
