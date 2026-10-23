---
id: 2026-10-13-correct-held-news-event-dates-with
title: Correct held news event dates with audited CAS before bundle ingestion
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-13T09:27:26Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/service.py
  - apps/api/app/news_automation/router.py
  - apps/api/tests/test_news_review_actions.py
---

# Correct held news event dates with audited CAS before bundle ingestion

## Why

Fixed-cohort Visa stablecoin candidate `e0fee63a-ce83-4d71-b6a7-c5093001b227` is held in `needs_redraft/news_locale_review_failed` with `event_date=2026-10-10`. [Visa's first-party announcement](https://www.visa.com.sg/about-visa/newsroom/press-releases/nearly-half-of-asia-pacific-consumers-open-to-using-stablecoins-in-the-next-five-years-visa-study-finds.html) is dated **2026-10-05**. The stored CoinDesk source was published 2026-10-09 23:00 EDT, or 10-10 in Taipei, so its separate `source_date=2026-10-10` is defensible. The candidate event date appears to have been copied from the report date.

The completed audited held-bundle ingestion path requires the package event date to equal the persisted candidate event date. It cannot repair this error by supplying the correct 10-05 date, and there is no admin action for a scoped event-date correction. Re-running the whole writer may incur costs and does not provide an audited correction. This candidate also needs the separate [audited source-extension task](2026-10-10-add-audited-source-extension-for-held.md) to add Visa's official announcement; changing the date alone does not make the article publishable.

## Definition of done

- [ ] An authorized operator can correct a held, unpublished candidate's event date with an explicit reason, expected current value/version, first-party date evidence and a durable before/after audit; concurrent or already-published changes are refused.
- [ ] The operation leaves `source_date`, source evidence, drafts, prior run history and judge holds intact. It cannot bypass normal verification, five-locale review or publication gates.
- [ ] The Visa candidate can be changed from event date 10-10 to 10-05 only after its source evidence is extended and checked, then a complete reviewed five-locale bundle can pass the existing native ingestion and re-verification path without a whole paid writer retry.

## Steps

- [ ] Inspect the current candidate/Guide/revision state and the held-bundle ingestion preconditions; design a narrow compare-and-set event-date action with source-date separation and audit reason. Recheck the live state before mutation.
- [ ] Add tests for wrong expected value, duplicate/concurrent action, published/active-run refusal, unchanged evidence and judge gate, and one successful Visa-shaped correction. If implementation needs a migration or another file, update this ticket's scope before touching it.
- [ ] Apply to the exact Visa ID only after the [source-extension task](2026-10-10-add-audited-source-extension-for-held.md) has a reviewed first-party receipt. Read back candidate date, audit, held-bundle dry run, and later run/Guide/public-page states separately.

## How to verify

Run the focused `apps/api/tests/test_news_review_actions.py` checks, Ruff and targeted mypy; verify the admin action's persisted audit and idempotent/conflict behavior. For Visa, read back candidate `event_date=2026-10-05` while CoinDesk `source_date=2026-10-10` remains unchanged. A successful date correction is **not** publication: require the existing five-language package, native re-verification/judge and public-page checks before terminal status.

## Notes

2026-10-13 read-only admin check: Visa has `guide_article_id=null`, only cached zh-TW/en documents, `judge_decision=manual`, and a discarded English correction whose fingerprint matches the original; the English callout still ends `not investment advice.`. The second English locale run succeeded, but the following redraft judge returned manual. The current UI exposes only whole-draft retry or reject, not targeted editing. Existing held-bundle ingestion requires all five reviewed documents, unchanged saved source refs and an exactly matching event date; the Visa official source is absent from candidate evidence. Do not use a flagless backfill, ordinary retry or an invented local Guide edit as a shortcut. See `docs/news-hourly-backlog-2026-10-13.md` row #24 and draft PR #1480.
