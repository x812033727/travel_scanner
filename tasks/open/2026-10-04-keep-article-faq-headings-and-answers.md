---
id: 2026-10-04-keep-article-faq-headings-and-answers
title: Keep article FAQ headings and answers together
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-10-04T07:55:27Z
completed_at:
branch: codex/adsense-review-audit-20261004
depends_on: []
scope:
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
---

# Keep article FAQ headings and answers together

## Why

On the published article
https://mokaair.com/zh-TW/life/crypto-news-cardano-petrobras-fuel-traceability-20260930,
the table of contents points to a residual FAQ H2 in the body, while the real five
questions and answers appear after related-reading and travel recommendations.
Extraction in lib/guides.ts removes the faq block but leaves the adjacent heading;
components/guides/article.tsx renders recommendations before the extracted FAQ.

## Definition of done

- [ ] FAQ contents and their heading/TOC target remain together before recommendations.
- [ ] No empty or duplicate FAQ heading is introduced when extracting existing blocks.
- [ ] FAQ schema and genuinely separate non-FAQ headings retain their behavior.
- [ ] Cover relevant heading/block arrangements and both FAQ-present/absent articles.

## Steps

- [ ] Inspect existing source/block shapes and all consumers before choosing extraction rules.
- [ ] Claim exact implementation/test paths; keep the fix narrow and do not rewrite published content.
- [ ] Add meaningful regression coverage, run relevant web checks, and verify desktop/mobile rendering.

## How to verify

Run focused guide/article tests, lint/typecheck and applicable navigation/SEO checks.
On a local equivalent of the affected article, clicking the FAQ TOC item must reach
the questions and answers rather than an empty heading; recommendations follow them.

## Notes

2026-10-04: found during a limited AdSense content audit; this is a reading defect,
not proof that Google selected this URL as the low-value rejection cause. No fix or
deployment was performed. Source evidence: lib/guides.ts near line 516 and
components/guides/article.tsx near lines 279/296. Recheck against latest main.
