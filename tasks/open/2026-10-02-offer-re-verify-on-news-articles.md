---
id: 2026-10-02-offer-re-verify-on-news-articles
title: Offer re-verify on news articles saved after failing hard checks
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-02T14:53:57Z
completed_at:
branch:
depends_on:
  - 2026-09-24-save-news-drafts-that-fail-hard
scope:
  - apps/web/components/admin-news-workspace.tsx
  - apps/web/components/admin-news-workspace.test.tsx
  - apps/web/lib/admin-news-messages
---

# Offer re-verify on news articles saved after failing hard checks

## Why

Since task 2026-09-24-save-news-drafts-that-fail-hard, a news candidate whose five-locale
article fails a hard check (a missing FAQ block, a missing topic link, a forbidden word in
one locale) is saved as an unpublished guide article and waits in 待審查 as `manual_review`
with `error_code = news_hard_checks_failed` and `guide_article_id` set. The API lets an
editor fix it in the guide editor and press 重新查核 (`POST …/verify`, which
`service.reverify_candidate` accepts for any `manual_review`). `/admin/news` does not offer
that button in every case (`situationOf` in `apps/web/components/admin-news-workspace.tsx`):

- An owner-confirmed candidate (`human_decision = "publish"`) falls into `translationHold`,
  which offers only 「重新翻譯並發布」 and 退件. The editor links show (the page shows them
  whenever `guide_article_id` is set), but after editing there is no 重新查核, and
  「重新翻譯並發布」 translates the four locales again over the editor's fixes.
- An unconfirmed (automatic-mode) candidate falls into `fixArticle` (重新查核, 退件), which is
  right, but its explanation reads "the edited article did not pass its checks again",
  which is wrong for an article nobody has edited yet.

## Definition of done

- [ ] A `manual_review` candidate with `news_hard_checks_failed` and a saved article offers
      重新查核 and 退件 (and, when confirmed, still 「重新翻譯並發布」), whether or not the
      owner confirmed it.
- [ ] Its explanation says the article is saved unpublished, which locales failed are
      listed under the lint, and that it should be fixed in the guide editor then
      re-verified; in all five locales.

## Steps

- [ ] A situation (or a branch in `situationOf`) for `news_hard_checks_failed` with
      `guide_article_id`, placed before the `translationHold` fallback.
- [ ] Its copy in `apps/web/lib/admin-news-messages/*.json` (five locales).
- [ ] A row in the situation table test of `admin-news-workspace.test.tsx`.

## How to verify

```bash
cd apps/web && npx vitest run components/admin-news-workspace.test.tsx
npm run typecheck:web && npm run lint:web && npm run check:i18n
```

## Notes

- Filed by claude-opus-5-5-news-drafts while doing the API side; the API needs nothing
  more: `reverify_candidate` already accepts `manual_review`, and publication still runs
  every check (`service.publication_bundle`).
