---
id: 2026-09-23-guide-badges-use-the-undefined-fg
title: Guide badges use the undefined --fg token and fail contrast
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-23T23:33:28Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/guides/related-grid.tsx
  - apps/web/components/guides/partner-link.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/search-results.tsx
  - apps/web/app/globals.css
---


# Guide badges use the undefined --fg token and fail contrast

## Why

Several guide badges are styled `rounded-full bg-[var(--line)] ... text-[var(--fg)]`, but no
stylesheet defines `--fg`. The declaration is invalid at computed time, so the badge
inherits its parent's `--muted` colour: 3.54:1 on `--line`, under the 4.5:1 that
`e2e/readability.spec.ts` enforces. PR #702 hit this in `GuideCard` on the home page and
fixed only `components/guides/card.tsx` (now `--ink`).

## Definition of done

- [ ] No component or stylesheet references `var(--fg)`; every badge reads at 4.5:1 or better.

## Steps

- [ ] `text-[var(--fg)]` -> `text-[var(--ink)]` in `related-grid.tsx`, `partner-link.tsx`,
      `article.tsx`, `search-results.tsx`.
- [ ] `app/globals.css` (around line 3593, `color: var(--fg)`): find what it styles, use `--ink`.

## How to verify

`grep -rn "var(--fg)" apps/web --include=*.tsx --include=*.css` returns nothing (node_modules
excluded); `npx playwright test e2e/readability.spec.ts` passes.

## Notes

Found by CI on PR #702 (2026-09-23).
