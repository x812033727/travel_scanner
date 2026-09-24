---
id: 2026-09-24-reader-support-link-at-the-end
title: Reader support link at the end of articles
status: blocked
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-24T00:30:06Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/guides/support-link.tsx
  - apps/web/components/guides/support-link.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-TW/common.json
---

# Reader support link at the end of articles

## Why

A plain link to a tip page ("buy me a coffee") is the cheapest revenue channel the site
could add: no third-party script, no consent banner, no CSP change, no review to pass
(`docs/monetization-alternatives.md`, sections 1 and 4.4). At the site's traffic it will
bring in little; it also costs almost nothing to keep.

**Blocked on the owner (decision D3)**: which platform, and creating the account (payout
details are personal). The document recommends Buy Me a Coffee, which pays out to Taiwan
through Stripe Express (help page updated 2026-08-24), because it serves readers in all
five locales; Portaly is the alternative when the owner wants Taiwanese payment methods.

## Definition of done

- [ ] Published articles in all five locales end with one short, plainly worded support
      line linking to the owner's page, below the sources and away from affiliate panels.
- [ ] The link is an ordinary first-party anchor: no widget script, no iframe, no tracking parameter.
- [ ] With no URL configured the line is not rendered at all.

## Steps

- [ ] Owner: pick the platform, create the page, send the URL.
- [ ] Decide where the URL lives. A constant is enough for one URL; an admin setting only
      if the owner wants to change it without a deploy.
- [ ] `support-link.tsx` plus five `common.json` strings. The copy must not ask readers to
      click ads or partner links (AdSense policy, relevant if the site reapplies).
- [ ] Render it in `article.tsx` after the sources.

## How to verify

```bash
cd apps/web && npx vitest run components/guides/support-link.test.tsx components/guides/article.test.tsx
npm run check:i18n
```

## Notes

- `common.json` is in the scope of `2026-09-07-add-a-meal-to-a-day` (in review at the time
  of filing); claiming this ticket will be refused until that one lands.
- Keep it off share, trip and account pages; readers of those pages are users, not an audience.
