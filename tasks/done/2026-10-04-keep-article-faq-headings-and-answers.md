---
id: 2026-10-04-keep-article-faq-headings-and-answers
title: Keep article FAQ headings and answers together
status: done
priority: P1
area: web
owner: codex-gpt6-faq
claimed_at: 2026-10-04T08:09:13Z
created_at: 2026-10-04T07:55:27Z
completed_at: 2026-10-04T08:44:59Z
branch: codex/adsense-content-fixes-20261004
depends_on: []
scope:
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
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

- [x] FAQ contents and their heading/TOC target remain together before recommendations.
- [x] No empty or duplicate FAQ heading is introduced when extracting existing blocks.
- [x] FAQ schema and genuinely separate non-FAQ headings retain their behavior.
- [x] Cover relevant heading/block arrangements and both FAQ-present/absent articles.

## Steps

- [x] Inspect existing source/block shapes and all consumers before choosing extraction rules.
- [x] Claim exact implementation/test paths; keep the fix narrow and do not rewrite published content.
- [x] Add meaningful regression coverage and run focused guide/article tests plus scoped lint.
- [x] Root integration: complete typecheck and desktop/mobile browser verification.

## How to verify

Run focused guide/article tests, lint/typecheck and applicable navigation/SEO checks.
On a local equivalent of the affected article, clicking the FAQ TOC item must reach
the questions and answers rather than an empty heading; recommendations follow them.

## Notes

2026-10-04: found during a limited AdSense content audit; this is a reading defect,
not proof that Google selected this URL as the low-value rejection cause. No fix or
deployment was performed. Source evidence: lib/guides.ts near line 516 and
components/guides/article.tsx near lines 279/296. Recheck against latest main.

2026-10-04 implementation by codex-gpt6-faq, awaiting root integration/closure:

- `splitArticleExtras` still hoists the first summary and returns the first FAQ for
  the existing FAQPage schema, but retains every FAQ block in the original body
  order. Published content and schema generation were not rewritten.
- The article preserves an immediately preceding authored H2 and its `section-N`
  anchor, without adding a second FAQ heading. A localized FAQ heading with
  introductory prose is recognized using the current label, Unicode normalization
  and locale casing; genuinely separate headings/prose remain intact. Unheaded
  FAQs use the translated label. Legacy multiple FAQs receive distinct IDs while
  the first keeps `article-faq`.
- Root approved the shared renderer scope extension. Its optional `renderFaq`
  callback keeps the existing one-pass H2/H3 numbering and leaves default/admin
  preview rendering unchanged. Absolute block positions remain correct across
  partner and ad slices; regression coverage exercises both.
- Relevant source shapes inspected: unheaded FAQ after prose, FAQ followed by
  disclosure, authored adjacent/non-adjacent H2, multiple FAQ blocks and absent
  FAQ. Tests include headings in all five site languages and cross-FAQ H3 IDs.
- Verified using Node v24.19.0: focused Vitest `lib/guides.test.ts`,
  `components/content-blocks.test.tsx`, `components/guides/article.test.tsx`, and
  `components/guides/article-page.test.tsx` with `--maxWorkers=1`: 4 files,
  172 tests passed, exit 0. Scoped ESLint over the six implementation/test paths
  with `--max-warnings=0` passed, exit 0; `git diff --check` passed.
- An initial lint pass caught React's immutability rule on a captured offset
  counter. Replaced it with pure offset reductions, then reran focused tests and
  lint successfully.
- No dependency install, full web suite, server/browser, SSH, commit, push,
  production write or deployment was performed. Root owns integration checks,
  desktop/mobile navigation validation and task closure.

2026-10-04 root integration evidence, local only:

- Complete `lint:web` passed, exit 0. After the city-copy catalog update, complete
  `typecheck:web` passed, exit 0, followed by scoped ESLint over
  `lib/destinations-copy.ts` and `e2e/guides-adsense.spec.ts`, exit 0. Complete logs
  are `lint-web-20261004.log`, `typecheck-web-20261004.log`, and
  `lint-city-e2e-20261004.log` in the local AdSense review evidence directory.
- Root confirmed the integrated i18n check passed and the local production-mode
  `next build --webpack` completed successfully, exit 0.
- Root ran the isolated `guides-adsense` FAQ regression on desktop-chromium and
  mobile-chromium: 2 tests passed in 13.8 seconds, exit 0. Root also manually
  verified the local FAQ reading position and contents target on desktop/mobile.
- These results verify local implementation and navigation. They do not mean
  the fix has been deployed to production or that Google has approved AdSense.
  This ticket is ready for root's PR integration; no commit or push was performed
  by codex-gpt6-faq.
