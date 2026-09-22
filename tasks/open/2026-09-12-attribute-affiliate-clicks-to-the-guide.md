---
id: 2026-09-12-attribute-affiliate-clicks-to-the-guide
title: Attribute affiliate clicks to the guide article that placed them
status: blocked
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-12T17:42:18Z
completed_at:
branch: codex/guide-diagram-dimensions
depends_on:
  - 2026-09-12-guide-offer-content-block
scope:
  - tasks/open/2026-09-12-attribute-affiliate-clicks-to-the-guide.md
---

# Attribute affiliate clicks to the guide article that placed them

## 2026-09-22 remaining live acceptance handoff

The implementation merged in PR #565 on 2026-09-19, commit
`d11178863d1a2a35ddfff17be65bcc2a63514194`. A normal stale-claim takeover
(without force) preserved the outstanding live acceptance instead of treating
merged code as proof of production partner-click attribution.

The owner-directed real partner click and corresponding analytics/ledger
inspection described below remain unverified. This localization task did not
generate a synthetic conversion or claim that acceptance passed. The task is
retained as blocked pending that live acceptance/disposition, with scope narrowed
to its own handoff record. Any implementation defect found by that acceptance
needs a separately claimed scope; the merged implementation paths are released.

## Why

Every guide click is recorded as `placement='guide'` with a `sub_id` of
`dst_{module}_{destination}_{locale}_guide`, so ten Tokyo transport articles collapse into
one bucket in `affiliate_clicks` and in the partners' dashboards. With editors now placing
buttons mid-article, "which article converts" is the feedback the placement rules need.
`sub_id` cannot carry a slug (64-character cap, `safe_sub_id` fail-closed regex), so the
attribution is our own column.

## Definition of done

- [x] `affiliate_clicks.article_slug` (String(120), nullable, indexed) via an additive
      migration; the append-only trigger only blocks UPDATE/DELETE, so no trigger change.
- [x] `POST /affiliates/destination-offers/{id}/clickout?placement=guide&article=<slug>`
      stores the slug when it matches `SLUG_PATTERN` and ignores it otherwise; no other
      behaviour of the clickout changes.
- [x] `DestinationAffiliateOptions` takes `article?: string` and appends it to the clickout
      URL; the article page passes `state.slug` for both inline and end-panel islands.
- [x] `GET /admin/analytics/affiliates` gains `by_article`, and the admin analytics panel
      shows it.

## Steps

- [x] Check `ls apps/api/migrations/versions | tail -3` right before writing the migration
      — parallel sessions take numbers — and revise the current head.
- [x] Router, model, analytics dimension, web prop, panel, tests, docs §8.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_affiliates.py tests/test_analytics_affiliates.py tests/test_guide_partner_links.py tests/test_affiliate_sub_id.py tests/test_schema.py -q
cd apps/web && npx vitest run components/destination-affiliate-options.test.tsx components/admin-analytics-panel.test.tsx components/guides/article.test.tsx
```

Then on production: open an article, click a partner button, and read one row back with
`select article_slug, placement, module from affiliate_clicks order by created_at desc limit 1`.

## Notes

- Keep `sub_id` as it is: partner-side reporting stays per destination × module × locale ×
  placement, and `test_affiliate_sub_id.py` fails CI on any new derivation site.
- 2026-09-13 (claude-opus-5, `2026-09-13-content-partner-links-in-articles-non`): non-travel
  partner links in articles now write their own rows from `POST
  /guides/{kind}/{slug}/partner-links/{key}/click` (`app/guides/service.py`
  `record_partner_click`): `status='clicked'`, `sub_id` prefix `cnt_`, `destination_id` null,
  and **the article slug in `destination_summary`**, because the ledger is append-only and
  waiting for this column would have lost the attribution for good. When `article_slug`
  lands, write it there as well, and backfill nothing: the report can read
  `coalesce(article_slug, destination_summary)` for `status='clicked'` rows.

### 2026-09-19 done in repo (claude-fable-5-1)

- Migration `0081_affiliate_click_article` (revises `0080_crypto_and_tech_topics`): adds
  `affiliate_clicks.article_slug` String(120) NULL plus `ix_affiliate_clicks_article_slug`, guarded
  like 0079 (a fresh database already has it from `0001_initial`). Additive only: the append-only
  trigger fires on UPDATE/DELETE, so it is untouched, and nothing is backfilled.
- Clickout: `article=` is a plain query parameter on `POST /affiliates/destination-offers/{id}/clickout`.
  It is stored only when it matches the guides' `SLUG_PATTERN` and is at most 120 characters (the
  column width); anything else is stored as NULL, never a 4xx. Not gated on `placement='guide'`,
  because `life` articles send their slug the same way. The redirect, `sub_id`, `placement` and
  `destination_summary` are unchanged and the new test pins all four.
- `record_partner_click` now writes `article_slug` and keeps writing `destination_summary`; the
  rows written between 2026-09-13 and this column only have the latter. The report's `by_article`
  reads `coalesce(article_slug, case when status='clicked' then destination_summary end)`, so those
  rows still count; clicks with no article (search, trip, city) fold into `unknown` like the other
  dimensions do.
- Web: `DestinationAffiliateOptions` appends `&article=<encoded slug>` to the API-built clickout URL
  client-side; it is not part of the request identity, so a rerender with or without it does not
  refetch. The article page passes `state.slug` to the inline `offer` islands and the end panel.
  The admin panel's "Article" tile keeps the ASCII title convention of its siblings, so no
  message catalog changed.
- Scope corrections: the report tests live in `tests/test_analytics_affiliates.py` (the
  `test_affiliate_analytics.py` this ticket named never existed); `app/guides/service.py`,
  `tests/test_guide_partner_links.py` and `docs/travel-guides.md` (two "until this ticket lands"
  sentences) were added to the scope before they were edited. `2026-09-13-google-ads-conversion-
  measurement` (blocked, unowned) lists the same files; nothing there was touched.
- Verified: the API and web commands in "How to verify" plus `ruff`, `mypy app`, `mypy tests`,
  `lint:web`, `typecheck:web`, `check:i18n` all pass. `test_migration_dead_branches.py` needs no
  case: the guarded branch only adds an empty column and index.
- Owner, after the deploy runs `alembic upgrade head`: open a guide that shows a partner button,
  click it, then `select article_slug, placement, module, status from affiliate_clicks order by
  created_at desc limit 1;` should show that article's slug with `placement='guide'` (or `life`)
  and `status='redirected'`. A partner-link click shows `status='clicked'` with the slug in both
  `article_slug` and `destination_summary`. The "Article" tile under 聯盟外連 in admin analytics
  should list it. Rows from before the migration keep `article_slug` NULL by design.
