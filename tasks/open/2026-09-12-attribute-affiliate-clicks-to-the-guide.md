---
id: 2026-09-12-attribute-affiliate-clicks-to-the-guide
title: Attribute affiliate clicks to the guide article that placed them
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-12T17:42:18Z
completed_at:
branch:
depends_on:
  - 2026-09-12-guide-offer-content-block
scope:
  - apps/api/app/models.py
  - apps/api/migrations/versions
  - apps/api/app/affiliates/router.py
  - apps/api/app/analytics/affiliates.py
  - apps/api/tests/test_affiliates.py
  - apps/api/tests/test_affiliate_analytics.py
  - apps/web/components/destination-affiliate-options.tsx
  - apps/web/components/destination-affiliate-options.test.tsx
  - apps/web/components/admin-analytics-panel.tsx
  - apps/web/components/admin-analytics-panel.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - docs/affiliate-configuration.md
---

# Attribute affiliate clicks to the guide article that placed them

## Why

Every guide click is recorded as `placement='guide'` with a `sub_id` of
`dst_{module}_{destination}_{locale}_guide`, so ten Tokyo transport articles collapse into
one bucket in `affiliate_clicks` and in the partners' dashboards. With editors now placing
buttons mid-article, "which article converts" is the feedback the placement rules need.
`sub_id` cannot carry a slug (64-character cap, `safe_sub_id` fail-closed regex), so the
attribution is our own column.

## Definition of done

- [ ] `affiliate_clicks.article_slug` (String(120), nullable, indexed) via an additive
      migration; the append-only trigger only blocks UPDATE/DELETE, so no trigger change.
- [ ] `POST /affiliates/destination-offers/{id}/clickout?placement=guide&article=<slug>`
      stores the slug when it matches `SLUG_PATTERN` and ignores it otherwise; no other
      behaviour of the clickout changes.
- [ ] `DestinationAffiliateOptions` takes `article?: string` and appends it to the clickout
      URL; the article page passes `state.slug` for both inline and end-panel islands.
- [ ] `GET /admin/analytics/affiliates` gains `by_article`, and the admin analytics panel
      shows it.

## Steps

- [ ] Check `ls apps/api/migrations/versions | tail -3` right before writing the migration
      — parallel sessions take numbers — and revise the current head.
- [ ] Router, model, analytics dimension, web prop, panel, tests, docs §8.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_affiliates.py tests/test_affiliate_analytics.py -q
cd apps/web && npx vitest run components/destination-affiliate-options.test.tsx components/admin-analytics-panel.test.tsx components/guides/article.test.tsx
```

Then on production: open an article, click a partner button, and read one row back with
`select article_slug, placement, module from affiliate_clicks order by created_at desc limit 1`.

## Notes

- Keep `sub_id` as it is: partner-side reporting stays per destination × module × locale ×
  placement, and `test_affiliate_sub_id.py` fails CI on any new derivation site.
