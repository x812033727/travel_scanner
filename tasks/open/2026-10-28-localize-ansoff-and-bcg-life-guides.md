---
id: 2026-10-28-localize-ansoff-and-bcg-life-guides
title: Localize Ansoff and BCG life guides in four languages
status: in-progress
priority: P1
area: api
owner: codex-gpt6-article-locales-20261028
claimed_at: 2026-10-28T02:08:48Z
created_at: 2026-10-28T02:08:31Z
completed_at:
branch: codex/article-locales-completion-20261028
depends_on: []
scope:
  - apps/api/app/guides/content/ansoff-growth-options.json
  - apps/web/public/guides/ansoff-growth-options
  - apps/api/app/guides/content/bcg-portfolio-review.json
  - apps/web/public/guides/bcg-portfolio-review
  - docs/article-localization/reviews/two-life-20261028
  - docs/article-localization/installations/ansoff-growth-options.json
  - docs/article-localization/installations/bcg-portfolio-review.json
  - docs/article-localization/installations/bundles/5717849d1e3407a3
  - docs/article-localization/installations/.lock
  - .codex/l10n/tl-5717849d1e3407a3
---

# Localize Ansoff and BCG life guides in four languages

## Why

The owner requested the missing languages for published travel-information and
life-sharing articles. The fresh 2026-10-28 census finds these two published life
guides have only zh-TW; en, ja, ko and zh-CN have no database rows or repository
documents. This narrow authoring wave supplies eight complete translations and
their text-bearing images without changing the published originals.

## Definition of done

- [x] Eight complete target documents and localized image text pass the official pipeline.
- [x] Independent final text, glyph and image reviews bind exact source/document/artifact hashes.
- [x] Official assembly and installation preserve both zh-TW documents and original assets.
- [ ] Selected lint, translation/content checks and task validation pass; content PR is reviewable.
- [x] A separate release task retains merge, deployment, fresh dry-run, backup, publication and public acceptance gates.

## Steps

- [x] Claim exact pack/media scopes and check existing ownership.
- [x] Independently audit both original sources, five primary references and original diagrams.
- [x] Bind current public zh-TW v4 documents and prepare eight jobs from the current official baseline.
- [x] Translate and render all eight jobs without retrying quota/auth failures.
- [x] Apply independent review findings, revalidate and install only reviewed artifacts.
- [ ] Prepare the content PR and separate publication handoff.

## How to verify

Run the unchanged official pipeline, render, assembly and installation tools with
the pinned external baseline and explicit two-slug selector. Use the real
GuideDocument validator, selected pack lint, translation character checks and
content tests. Compare original source/media hashes before and after. Publication
is separate and must use fresh actual database guards, backup and public checks.

## Notes

- Source audit PASS with no blocking findings, SHA256
  `8ac2c99188d5b2cd09aebe445583190f63be13bfc899309208a8e6eab819e52a`.
- Both live zh-TW v4 documents equal their drafts and repository sources:
  Ansoff `4bb11afb53360aac604818614a9e131c0df916b4d58864b521544648a78312df`;
  BCG `556de90a7da2e66c2ef558ad4b9c46c317f022170a8a38eb739e1bf804942880`.
- The BCG article accurately distinguishes the original study's denominator from
  its own illustrative calculation. Do not rewrite this qualified source detail.
- Work, raw snapshots, CLI attempts, source captures and rendering evidence remain
  in the owner's persistent external work directory. No paid API provider is used.
- Eight final jobs are rendered and independently reviewed. The original pipeline
  exited 1 on a Korean protected numeric token; its preserved single attempt was
  corrected to a written-out word and materialized without a model retry. A
  distinct applicator applied 20 reviewed exact related-title findings.
- Final review SHA `98838ba8367685e9e76dc2fdc6ec7fef4cce3e2d0e106ca2e0c5043052e588c7`;
  manifest `5717849d1e3407a3dd1fe762a96067236837562aed3fc8c1faeb575c160668d1`.
- Install and identical-argument replay actually exit 0. Journal/two receipts are
  byte-identical on replay. Exactly two packs and 24 localized assets are installed.
- Independent preservation audit passes 39 checks: 1,202 other packs and all 6,689
  original public files remain byte-identical; stage/external jobs and frozen inputs
  remain unchanged. Audit SHA
  `a23ecd9beb2bfe04c31dbbf44fc91b0b1341ec31ce4a899a74c21f14b89fe197`.
- Source canonical hashes are unchanged. Exact serializer differences are only an
  omitted empty image description at zh-TW blocks/27 in each pack, named empty root
  defaults and same-multiset topic ordering. Raw dictionary identity is not claimed.
- Lint exits 0 with ten no-summary and two English-length advisories retained;
  character checks have zero findings. Pipeline 35, geometry/artifact 25 and
  content-pack nine tests pass; five database tests skip. Full Windows tools exits
  1 (1,487 pass, 64 fail, 23 skip); the native-fast-fail follow-up retains diagnostics.
