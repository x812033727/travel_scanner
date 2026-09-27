---
id: 2026-09-24-let-a-news-candidate-held-for
title: Let a news candidate held for changed evidence be re-checked against the current page
status: done
priority: P2
area: api
owner: claude-opus-5-5-news-final-editor
claimed_at: 2026-09-26T04:28:57Z
created_at: 2026-09-24T11:21:13Z
completed_at: 2026-09-26T04:38:57Z
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/router.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/policy.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_review_actions.py
  - apps/api/tests/test_news_pipeline.py
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages/en.json
  - apps/web/lib/admin-news-messages/ja.json
  - apps/web/lib/admin-news-messages/ko.json
  - apps/web/lib/admin-news-messages/zh-CN.json
  - apps/web/lib/admin-news-messages/zh-TW.json
  - docs/news-automation.md
---

# Let a news candidate held for changed evidence be re-checked against the current page

## Why

A candidate held with `news_evidence_changed` can never leave that state except by a
rejection. `revalidate_evidence` (`apps/api/app/news_automation/validation.py`) re-fetches
each evidence page and compares it with the stored `content_hash`, and nothing ever
updates that hash. Publish, re-verify and retry all reach the same comparison, so every
attempt finds the same change. Pages whose extracted text moves a little (view counters,
"related" lists, a corrected typo) therefore turn a finished, Jev-reviewed article into
a dead end. Since 2026-09-24 `/admin/news` offers only 退件 for this hold and says why.

## Definition of done

- [x] An editor can re-check a `news_evidence_changed` candidate against the current
      pages: the new text replaces the stored excerpt and hash, and the candidate is
      re-verified (fact check, locale reviews, Jev) against it, never published on the
      old verification.
- [x] The evidence gate and host rules still apply to the refreshed pages.

## Steps

- [x] Decide where the refresh lives (a service action, or re-verify refreshing first).
- [x] Implement it with a test that a refreshed candidate cannot publish without a new
      passing verification.
- [x] Offer the action in `/admin/news` (`situationActions.evidenceChanged` in
      `apps/web/components/admin-news-workspace.tsx`) and update the copy.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py tests/test_news_review_actions.py -q
```

## Notes

- Found while making the review queue actionable
  (task 2026-09-24-make-the-news-review-queue-actionable).
- Built on 2026-09-26 after the owner asked for it. That morning the Bitget/Circle story passed every
  gate, with Jev acting on all five locales, and still stopped here because CoinDesk had
  updated the report. The action is 「用最新來源重新查核」 (`POST …/refresh-evidence`,
  `service.refresh_candidate_evidence`, `validation.refresh_evidence`). The rerun marker is
  `news_evidence_refreshed`, and it runs Jev's last call even though the text is the saved
  article's.
