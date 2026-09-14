---
id: 2026-09-14-aio-article-citations-and-llms-txt
title: AIO: article graph carries its dated sources, and an llms.txt
status: in-progress
priority: P2
area: web
owner: claude-opus-5-aio
claimed_at: 2026-09-14T13:33:21Z
created_at: 2026-09-14T13:30:54Z
completed_at:
branch: claude/keen-sagan-q7xitd
depends_on: []
scope:
  - apps/web/lib/structured-data.ts
  - apps/web/lib/structured-data.test.ts
  - apps/web/components/guides/article-page.tsx
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
  - apps/web/app/llms.txt
  - docs/seo.md
---

# AIO: article graph carries its dated sources, and an llms.txt

## Why

"AIO" here is AI-search optimisation: being the page an answer engine is willing to *cite*,
not just crawl. What decides that is provenance — a claim that is dated and sourced — and this
site has more of it than almost anything it competes with and publishes none of it to machines.

Measured over `apps/api/app/guides/content/*.json`: **498 of 498 localized documents carry
sources, 4,322 rows in total, averaging 8.7 per document, and every single row has a
`checked_on` date.** `components/guides/article.tsx` renders the whole list with a
`<time dateTime>` per row. The JSON-LD said nothing about any of it.

The graph was also the one on the site built outside `lib/structured-data.ts` — an object
literal inline in `article-page.tsx`, hardcoding `@context` and the brand name, with no unit
test. Which is exactly why it had drifted to six fields while the page under it rendered the
source list, the topic chips, the destination and the reading time.

## Definition of done

- [x] The article graph is a tested builder in `lib/structured-data.ts`, not a literal in a page.
- [x] Every source the page lists reaches the graph as `citation`, through the same
      `contentBlockLink` sanitizer the visible list is drawn with.
- [x] The newest `checked_on` is published as `lastReviewed` on the article's `mainEntityOfPage`
      WebPage node, with `reviewedBy` — not on the Article, where neither property is valid.
- [x] `about` points at the destination's own page, and only for an id that has one.
- [x] `keywords`, `articleSection`, `timeRequired`, `isAccessibleForFree` and an `ImageObject`
      hero carrying its real dimensions.
- [x] `/llms.txt` answers `text/plain` with the site's annotated map, gated by the same switches
      as the sitemap so the two can never disagree.
- [x] `docs/seo.md` records what is emitted, what is deliberately absent and why, and who can
      actually read `/llms.txt`.
- [x] `npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web` green.

## Steps

- [x] `brand()` factored out of `organization()` so nested `publisher`/`reviewedBy`/`author`
      nodes reuse it without repeating `@context`.
- [x] `guideArticle(locale, input)` added beside `touristDestination`, same conventions:
      pure, spread-conditional optionals, every internal URL through `localeUrl`.
- [x] `article-page.tsx` calls it; the inline literal is gone and the orphaned `siteUrl`
      import narrowed to `localeUrl` (`eslint --max-warnings=0` fails otherwise).
- [x] `app/llms.txt/route.ts`, reusing `SITEMAP_ROUTES` for the gating.
- [x] 20 cases in `lib/structured-data.test.ts`, 12 in `app/llms.txt/route.test.ts`, and 5 in
      the article route's own test, which renders the page and reads the graph back out of it.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run check:tasks
npx vitest run --root apps/web lib/structured-data.test.ts "app/llms.txt/route.test.ts"
```

Then paste a built article's JSON-LD into the Schema Markup Validator (validator.schema.org) and
Google's Rich Results Test. `citation`, `lastReviewed` and `reviewedBy` are consumed by neither
Google rich result, so the Rich Results Test should report no change; the Schema Validator is the
one that proves they are well-formed.

## Notes

**Scope claim.** `claim` refused this at first: `2026-09-14-claude-code-tutorial-center`
(`review`, `codex-claude-tutorials`) holds `apps/web/components/guides` by prefix. Its PR #485
merged at 2026-09-14T05:58Z and its branch has no open PR, so the hold was stale bookkeeping and
no unmerged branch could conflict — the same situation PR #496 described as "留在 review …
會繼續佔住檔案 scope 擋掉別的 agent". Claimed with `--force` on that evidence. Its task file was
not touched; flipping someone else's status is theirs to do.

**Three graphs rejected on measurement, so the next model does not re-propose them.** The
reasoning is written into the foot of `lib/structured-data.ts` and into `docs/seo.md`:

- `HowTo` — 20 of 106 `howto` slugs hold an ordered list at all, and they are itineraries.
  `taoyuan-airport-departure-guide` holds *two*, one procedural and one enumerating who is
  barred from e-Gate, so "take the first ordered list" is a coin flip between a procedure and
  its inverse. Google retired HowTo rich results in 2023, so there is no payoff on offer either.
- `FAQPage` — 10 of 498 documents hold two question-heading/answer pairs, and the matching
  headings are section titles with colons. No FAQ member exists in `RichContentBlock` or the API
  block union; a real FAQ needs an authored `faq: list[FaqItem]` on `GuideDocument`, not a
  scraper. (The `2026-09-10-seo-structured-data` ticket ticked `faqPage` in its DoD and its own
  note recorded it as skipped — the builder never existed.)
- `expires` from `valid_until` — this one was written, then removed. schema.org reads `expires`
  as *stop serving this*, while the product deliberately keeps an expired intel notice online:
  `article.tsx` states it as "no expiry banner, no date it applied until". It would publish a
  withheld date in order to ask answer engines to stop citing 19 pages.

**`dateAccessed` is not a schema.org property.** It was proposed for the citation entries and
checked against schema.org directly: it does not exist. `lastReviewed`/`reviewedBy` are WebPage
properties only, which is why they sit on `mainEntityOfPage` — the same trap `touristDestination`
already records for `inLanguage`.

**`lastReviewed` decays if nobody re-checks.** All 4,322 `checked_on` values are one of two dates,
so it currently reads as a bulk verification stamp. It is honest today because the page prints the
same dates. It stops being honest the moment republication stops updating them.

**A test that passed for the wrong reason, now fixed.** `vitest.setup.tsx`'s `next-intl/server`
mock carries zh-TW only, ignores the `locale` it is handed, and has no `metadata` namespace — so
every annotation in `/llms.txt` came back as its own key and the "strips the brand suffix"
assertion passed without ever seeing a suffix. `route.test.ts` mocks `next-intl/server` itself
against the real `messages/en/metadata.json`. Adding `metadata` to the shared setup would fix
this for everyone but is outside this scope.

**The end-to-end harness already existed**, which is how the change was caught: the article
route's own test renders the page and parses its `<script type="application/ld+json">` back out.
Its `image` assertion failed on the new `ImageObject`, and it is now extended to cover `citation`,
`lastReviewed`, `about`, `keywords`, `articleSection` and `timeRequired` against the same rendered
page — including that a `javascript:` source is dropped from the graph and from the visible list
together, and that a destination with no page behind it produces no `about`. That test file was
added to this scope for the same reason: a task owns the tests its change breaks.
