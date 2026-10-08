---
id: 2026-10-07-localize-twelve-web-design-and-seo
title: Localize twelve web design and SEO life articles
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T14:06:21Z
created_at: 2026-10-07T14:05:49Z
completed_at: 2026-10-07T17:31:13Z
branch: codex/article-locales-wave4-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/css-layout-basics.json
  - apps/api/app/guides/content/image-formats-compression.json
  - apps/api/app/guides/content/responsive-layout-basics.json
  - apps/api/app/guides/content/web-layout-hierarchy.json
  - apps/api/app/guides/content/website-color-system.json
  - apps/api/app/guides/content/website-information-architecture.json
  - apps/api/app/guides/content/website-cache-cdn.json
  - apps/api/app/guides/content/search-crawlers-explained.json
  - apps/api/app/guides/content/structured-data-basics.json
  - apps/api/app/guides/content/sitemap-website-submission.json
  - apps/api/app/guides/content/web-design-project-workflow.json
  - apps/api/app/guides/content/seo-content-cannibalization.json
  - apps/web/public/guides/css-layout-basics
  - apps/web/public/guides/image-formats-compression
  - apps/web/public/guides/responsive-layout-basics
  - apps/web/public/guides/web-layout-hierarchy
  - apps/web/public/guides/website-color-system
  - apps/web/public/guides/website-information-architecture
  - apps/web/public/guides/website-cache-cdn
  - apps/web/public/guides/search-crawlers-explained
  - apps/web/public/guides/structured-data-basics
  - apps/web/public/guides/sitemap-website-submission
  - apps/web/public/guides/web-design-project-workflow
  - apps/web/public/guides/seo-content-cannibalization
  - docs/article-localization/source-corrections/wave4-web-life-20261007.md
---

# Localize twelve web design and SEO life articles

## Why

Twelve published life articles about web design and SEO lack en, ja, ko and
zh-CN. The owner requested all missing travel/life languages. These twelve are
outside the first reviewed 32-article release and have their own authoring scope.

Six original sources passed independent full-source review. Six were rejected
for eight unrelated AI article links and one simplified character. Translating
those mistakes would reproduce incorrect associations in four languages.

## Definition of done

- [x] Preserve all original source text, metadata, citations and images except
      independently approved exact source corrections for six rejected articles.
- [x] Corrected sources pass a reviewer independent of both proposal and application.
- [x] All twelve packs include reviewed en, ja, ko and zh-CN documents and native
      localized diagram text, with document/asset/artifact hashes bound to reviews.
- [x] Applicable local content checks pass; the final PR's exact SHA must pass CI
      before merge. GitHub records that independent gate for the resulting head.
- [x] A narrow release task records that merge, deployment, publication and public
      verification still require their actual guarded release phases.

## Steps

- [x] Recheck the open queue, worktrees, remote main and open PRs; claim this scope.
- [x] Freeze original full sources and primary citations; record genuine PASS/FAIL.
- [x] Apply only the nine proposed leaves to external candidates, preserve originals,
      reverse the changes to prove exact scope, and validate GuideDocument.
- [x] Obtain distinct independent source-correction reviews of those candidates.
- [x] Capture a fresh official baseline and reconcile exact approved source changes.
- [x] Translate through the existing ChatGPT-only CLI pipeline with three workers
      and zero automatic retries; preserve STOP, quota and uncertain requests.
- [x] Render original/localized diagrams and independently review every language.
- [x] Assemble/install once, verify preservation/replay and run scoped checks.
- [ ] Open the scoped content PR and verify CI at its final head before merge.

## How to verify

Use the unchanged official source-correction, localization, assembly and installation
guards. Compare canonical source hashes and original media bytes before/after;
only approved leaf changes may differ. Review each full translated document and its
actual native-language images. Authoring success does not establish public availability.

## Notes

- Worktree starts at merged main `7524c25995d59f3826227e693d52f2ef5b3a19a2`;
  fresh remote main matches it. Eight open PRs concern separate news/video scopes.
- Original selection receipt SHA:
  `1beac38a5db8a3e24255847326230d68851206798df6365be324dd52ff48ee3e`.
- Six external corrected-source candidates / nine exact leaves have receipt SHA
  `01b6b044f5c837b03156cba14a859a286c952419602a43e45e23188fa1c12783`.
  That receipt is a preparation result, not source approval or publication.
- Cross-review assignments exclude proposal authors: color/information architecture
  by news reviewer; crawler/structured-data by inventory reviewer; sitemap/cannibalization
  by HK reviewer. The original rejected reviews and unchanged evidence remain retained.
- Existing source cutoffs and citation checked_on dates stay intact. No October facts
  or new dates are inferred from the translation work.
- First32 actual publication and its hold/journals continue separately. This task
  neither expands that approved cohort nor changes production settings.

### Actual local completion on 2026-10-07

- All six exact source corrections passed distinct independent verification. The
  original production baseline remains unchanged; the explicitly admitted working
  baseline SHA is `7194d18dc7f1880aa4b16e5e37adf14b411d1eacf4f8d0b85ee6c62cb363dced`.
- All 48 translations have genuine full-text, native-media, glyph and link reviews.
  Original CLI translator threads and failed attempts remain preserved. Four Korean
  protected-token spelling repairs and one Korean stale-date wording repair were
  separately applied and rechecked against freshly rendered artifacts.
- Unchanged official assembly completed: 12 articles, 156 assets, six source reviews;
  manifest `a175e63ec2a7ef5b845e5416bd3b6f4f0a41ca8e2b90f9428ddb5cd8d6e2594c`.
- Official local install and identical replay both exited zero. Final checks verify
  all 168 journal operations, every original source image and external review job,
  plus unchanged captured asset/journal/receipt bytes on replay. Completion receipt
  SHA `f9cd63964fc2da6faf6c4da836412ad75ea5bc1c3a5b24140d2bb0819df58ab1`.
- Scoped pack lint passed (12 entries); translation checks reported zero hits.
  Content-pack tests: 9 passed, 5 skipped. Localization tool tests: 68 passed.
  Existing no-summary and text-length warnings are retained; no source text was cut.
- No merge, deployment, database publication or public acceptance is established by
  these local results. The global missing-language task remains open.
- Local authoring is complete and is closed in the content PR as the task-board
  protocol requires. The remaining unchecked PR/CI step is the external merge gate,
  and must be verified on the resulting final head before any owner-approved merge.
  Fresh pre-PR verification checked33 worktrees,6,494 task snapshots and all8 open
  PR paginated file sets; no current ownership overlap exists. Historical AIO claims
  were explicitly reduced to their task-record scope on main, not assumed released.
  Receipt SHA: `00262a476a50abfbf811b272ed8b43cd2f6d0e8413705c92b429ba6d61132872`.
