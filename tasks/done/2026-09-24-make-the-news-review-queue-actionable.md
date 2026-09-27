---
id: 2026-09-24-make-the-news-review-queue-actionable
title: Make the news review queue actionable: needs_redraft list, not-duplicate action, next-step guidance, bulk reject
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-24T10:45:13Z
created_at: 2026-09-24T10:45:04Z
completed_at: 2026-09-24T11:22:11Z
branch: claude/ai-hourly-news-review-process-d46e01
depends_on: []
scope:
  - apps/api/app/news_automation/models.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/app/news_automation/policy.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/router.py
  - apps/api/app/news_automation/duplicates.py
  - apps/api/app/i18n.py
  - apps/api/app/admin/operations_service.py
  - apps/api/migrations/versions/0088_news_needs_redraft_status.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_news_admin.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_admin_operations.py
  - apps/api/tests/test_news_review_actions.py
  - apps/api/tests/test_migration_0088_news_needs_redraft_status.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news.ts
  - apps/web/lib/admin-news-copy.ts
  - apps/web/lib/admin-news-messages
  - docs/news-automation.md
---

# Make the news review queue actionable: needs_redraft list, not-duplicate action, next-step guidance, bulk reject

## Why

On 2026-09-24 the site owner opened `/admin/news`, found about 66 candidates under 待審查
and could not tell what to press. The list mixes three different things and shows only
raw codes (`manual_review`, `news_verification_failed: Independent verification did not
pass.`):

- Only `shadow_review` and `news_jev_manual` (about 2 rows) have a five-locale article a
  person can publish or reject, and only those decisions count toward the auto-publish
  gate (`service.py` `gate_for` counts rows whose `would_publish` is set).
- `news_verification_failed` (~38), `news_locale_review_failed` (~8),
  `news_hard_checks_failed`, `news_claim_source_invalid` and `news_event_date_invalid`
  stopped before `pipeline.py` saved the guide article, so 發布 and 重新查核 are always
  disabled; the only moves are a full redraft (MiniMax cost) or reject.
- `news_duplicate_uncertain` (~15) has no "not a duplicate" decision: retry just asks
  Jev again, and the page does not show what it was compared with.

All four action buttons stay grey until a reason is typed, with no hint; the 缺證據 hint
tells the owner to run again later, which cannot add evidence; there is no bulk action
and no paging.

Owner decisions (2026-09-24): move the stopped-before-draft rows to their own list (the
#724 pattern), add a "not a duplicate, continue" action that shows the closest existing
titles, and add bulk reject only (no bulk rerun, it spends model calls).

## Definition of done

- [x] 待審查 lists only `manual_review` + `shadow_review`; the five stopped-before-draft
      codes land in a new status `needs_redraft` (list 需重寫, together with `failed`),
      existing rows moved by migration 0088; the sidebar badge counts the same two
      statuses as 待審查.
- [x] A `news_duplicate_uncertain` candidate shows its five closest known titles and can
      be sent on with 不是重複，繼續寫; the pipeline then skips the Jev duplicate check
      for that evidence.
- [x] Every candidate shows a zh-TW explanation of what happened and only the buttons
      that can work for it; statuses, codes, assessment verdicts and Jev reasons are
      translated; the reason box says it is required and offers quick picks.
- [x] 待審查 / 需重寫 / 缺證據 support selecting rows and rejecting them in one go; every
      list pages past 100 rows through `?page=`; a read-only 已退件 list exists.
- [x] `docs/news-automation.md` explains each list and each hold reason.

## Steps

- [x] API: `needs_redraft` status, pipeline stops, retry/reject accept it, migration 0088
      with test, exception handler keeps terminal statuses.
- [x] API: `duplicates.py` (known titles + similar titles), `similar_titles` on the
      detail, `POST .../not-duplicate`, pipeline honours a human duplicate pass, i18n.
- [x] API: badge counts manual_review + shadow_review; service tests for every action.
- [x] Web: copy moved to `lib/admin-news-messages/*.json`; five lists, paging, row
      labels, bulk reject, next-step panel, reason quick picks, translated tables.
- [x] Docs, then close `2026-09-24-keep-every-news-review-item-reachable` (paging) here.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests
cd apps/api && uv run pytest tests/test_news_pipeline.py tests/test_news_admin.py tests/test_news_review_actions.py tests/test_news_automation.py tests/test_admin_operations.py tests/test_migration_0088_news_needs_redraft_status.py -q
npm run lint:web && npm run typecheck:web && npm run test:web -- admin-news-workspace admin-nav
git add -A && npm run check:i18n && npm run check:tasks
```

After deploying: `alembic current` shows 0088; `/zh-TW/admin/news` 待審查 holds only Jev
holds and shadow candidates, 需重寫 holds the verification / locale-review failures.

## Notes

- Out of scope, filed separately: `2026-09-24-let-a-news-candidate-held-for` (a
  `news_evidence_changed` hold can never be published because stored evidence hashes are
  never refreshed) and `2026-09-24-save-news-drafts-that-fail-hard` (hard-check failures
  are not saved as editable articles).
- A stop before the article exists goes to `needs_redraft` only when the candidate has no
  `guide_article_id`. A re-verified article that fails again stays in manual review so it
  can be edited and verified again; migration 0088 moves only rows without an article.
- 「不是重複，繼續寫」 stores a `duplicate` assessment with provider `human` and the
  candidate's `evidence_hash`; the pipeline skips Jev when one exists for the current
  evidence. With an article it re-verifies (like 重新查核), otherwise it drafts anew.
  `_known_titles` moved to `news_automation/duplicates.py` because the service needs it
  for the detail's `similar_titles` and the pipeline already imports the service.
- The sidebar badge (`news_review_pending`) now counts `manual_review` + `shadow_review`
  only, the same rows as 待審查; `failed` joined `needs_redraft` in 需重寫.
- The page copy moved to `apps/web/lib/admin-news-messages/*.json`: with changes staged,
  `check:i18n` refuses new Han strings in `lib/*.ts` (in CI the check runs with a
  one-commit checkout, so `HEAD^` is missing and it silently skips; run it locally).
- Checked by eye against a mock API (e2e fixture API plus a news mock) in Edge through
  Playwright at 1280 and 390 px: no horizontal overflow after giving the review grid
  `grid-cols-1` below `xl`; a bulk reject of a full page (50 rows) went through and the
  counts refreshed.
