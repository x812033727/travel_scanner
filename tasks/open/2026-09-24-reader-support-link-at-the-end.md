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
  - apps/web/components/guides/article-page.tsx
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
- [x] The link is an ordinary first-party anchor: no widget script, no iframe, no tracking parameter.
- [x] With no URL configured the line is not rendered at all.

## Steps

- [ ] Owner: pick the platform, create the page, send the URL.
- [x] Decide where the URL lives. A constant is enough for one URL; an admin setting only
      if the owner wants to change it without a deploy.
- [x] `support-link.tsx` plus five `common.json` strings. The copy must not ask readers to
      click ads or partner links (AdSense policy, relevant if the site reapplies).
- [x] Render it in `article.tsx` after the sources.
- [ ] Set `READER_SUPPORT_URL` in `components/guides/support-link.tsx` to the owner's page,
      deploy, and check one article per locale.

## How to verify

```bash
cd apps/web && npx vitest run components/guides/support-link.test.tsx components/guides/article.test.tsx
npm run check:i18n
```

## Notes

- `common.json` is in the scope of `2026-09-07-add-a-meal-to-a-day` (in review at the time
  of filing); claiming this ticket will be refused until that one lands.
- Keep it off share, trip and account pages; readers of those pages are users, not an audience.
- 2026-09-24: the owner chose "build it now, add the address later". What is on
  `claude/reader-support-link`:
  - `SupportLink` renders a plain `target="_blank" rel="noopener noreferrer"` link after the
    sources. It is wired through `GuideArticleLabels.support` from `article-page.tsx`, which
    is why that file joined the scope.
  - `READER_SUPPORT_URL` is `null`, so nothing shows yet.
  - The copy names no platform, so switching between Buy Me a Coffee and Portaly changes no
    text: `guides.supportText` and `guides.supportAction` in five locales.
  - `2026-09-07-add-a-meal-to-a-day`, which held `common.json`, had already landed (#565);
    the owner authorised closing it in the same PR.
  - The ticket goes back to `blocked`: the last Step is the owner's address plus a one-line change.
