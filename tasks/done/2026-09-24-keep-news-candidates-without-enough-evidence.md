---
id: 2026-09-24-keep-news-candidates-without-enough-evidence
title: Keep news candidates without enough evidence out of manual review
status: done
priority: P1
area: api
owner: claude-opus-5.5
claimed_at: 2026-09-24T07:31:28Z
created_at: 2026-09-24T07:31:17Z
completed_at: 2026-09-24T07:40:31Z
branch: claude/news-needs-evidence-status
depends_on: []
scope:
  - apps/api/app/news_automation/models.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/router.py
  - apps/api/migrations/versions/0087_news_needs_evidence_status.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_news_admin.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-copy.ts
  - docs/news-automation.md
---

# Keep news candidates without enough evidence out of manual review

## Why

After the first production day (2026-09-24) the manual review queue held 147 candidates,
83 of them stopped at the evidence gate (`news_evidence_insufficient`). Those have no
draft and nothing an editor can fix, yet they sat beside the two articles that were
actually waiting for a decision. The review list also fetched the newest 100 candidates
of every status and filtered them in the browser, so rows nobody acts on could push the
real work out of it. The owner asked for them to be moved out of manual review.

## Definition of done

- [x] A candidate that fails the evidence gate gets status `needs_evidence`, not
      `manual_review`, and is not counted as pending review or in the admin badge.
- [x] The candidates already waiting that way are moved by the migration.
- [x] `/admin/news` asks the API for exactly the statuses of the chosen list
      (待審查, 已發布, 缺證據), kept in the URL; a `needs_evidence` candidate can be
      rejected or run again.
- [x] `needs_evidence` titles are left out of the duplicate check, so they cannot block a
      later, better-sourced candidate for the same story.

## Steps

- [x] Status in the model, schemas and transition table; migration
      `0087_news_needs_evidence_status` (widen the check, move the rows; downgrade
      reverses both).
- [x] Pipeline gate sets the status; reject and retry accept it.
- [x] `GET /admin/news/candidates` takes a repeatable `status`, validated against the
      known statuses.
- [x] Workspace list filters with counts from the stats, and the 缺證據 explanation.
- [x] Tests: gate, repeatable filter (router and service), migration on PostgreSQL,
      workspace requests.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py tests/test_news_admin.py tests/test_migration_0087_news_needs_evidence_status.py -q
npm run test:web -- admin-news-workspace
```

On the host after deploying: `alembic current` shows 0087, no `manual_review` candidate
has `news_evidence_insufficient`, and `/admin/news` shows the 缺證據 list separately.

## Notes

- The duplicate check already only compares against `manual_review`, `shadow_review`
  and `published` candidates, so moving the rows out also removes them from it.
- The operations badge counts `manual_review`, `shadow_review` and `failed`, so it drops
  by the moved rows without a change there.
- Paging of the lists is still the open task 2026-09-24-keep-every-news-review-item-reachable.
