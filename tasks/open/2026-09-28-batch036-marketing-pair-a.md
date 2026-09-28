---
id: 2026-09-28-batch036-marketing-pair-a
title: Batch036 localize marketing pair A in five languages
status: review
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-09-28T10:23:38Z
created_at: 2026-09-28T09:19:38Z
completed_at:
branch: codex/article-localization-036-marketing-a
depends_on: []
scope:
  - apps/api/app/guides/content/marketing-plan-small-business.json
  - apps/api/app/guides/content/paid-vs-organic-marketing.json
  - apps/web/public/guides/marketing-plan-small-business
  - apps/web/public/guides/paid-vs-organic-marketing
  - docs/article-localization/batch036-marketing-pair-a-evidence.md
  - tasks/open/2026-09-28-batch036-marketing-pair-a.md
---

# Batch036 localize marketing pair A in five languages

## Why

Both public guides had only the published zh-TW v4 document at the pinned
read-only inventory. Four locale rows per article were missing. Add complete
repository drafts and translated original illustrations before guarded import.

## Definition of done

- [x] Add complete zh-CN/en/ja/ko documents for both articles, preserving 33
      source blocks, tables, source dates/URLs, and article-reference targets.
- [x] Add and render 24 localized image assets with original credits intact.
- [x] Obtain independent editorial review of meaning, figures and navigation.
- [ ] Obtain green PR checks before merge.
- [ ] Correct the inherited Google SEO page title and `hl=zh-Hant` source
      metadata through a versioned source follow-up before publication.
- [ ] Import/publish guarded locale revisions and verify live pages separately.

## Steps

- [x] Pin production and repository source versions and claim the pair scope.
- [x] Author eight target documents and 24 language assets.
- [x] Run content, asset, SVG-browser, focused tests and task checks.
- [x] Open draft PR and record its URL and CI status.

## How to verify

From `apps/api`, run `uv run python -m app.guides.pack_cli lint --kind life
--slug <slug>` for both slugs, then `uv run pytest
tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`.
From the root, run `npm run test --workspace @travel-scanner/web --
components/content-blocks.test.tsx` and `npm run check:tasks`. The scoped
evidence document pins source, document, asset and render hashes.

## Notes

The original subagent completed the marketing-plan documents and art but hit a
usage limit before finishing the second article. Codex-root released and
reclaimed this task, completed paid-vs-organic in four target languages and
made its localized hero/diagram from the original SVGs. The first SVG browser
run detected two overflowing English headings; both were reduced by 2 px and
the next run passed all 16 assets. Both packs lint with source no-summary and
advisory long-English-body warnings only. API tests: 12 passed, 5 skipped;
web tests: 65 passed. Independent read-only editorial review marked both
articles GO. The reviewer found a zh-CN `照著` typo, corrected in the pack;
the SEO source page title and Google Ads forced-language URL remain inherited
source-metadata follow-up. Public browser QA is pending.
Draft PR: https://github.com/x812033727/travel_scanner/pull/908.
CI began on the submitted branch; merge remains gated on independent editorial
review and green checks.
