---
id: 2026-09-28-correct-misleading-ai-links-before-batch038
title: Correct misleading AI links before Batch038 translation
status: done
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-09-28T11:19:23Z
created_at: 2026-09-28T11:19:12Z
completed_at: 2026-09-28T12:16:36Z
branch: codex/article-localization-038-source-links
depends_on: []
scope:
  - apps/api/app/guides/content/customer-journey-funnel.json
  - apps/api/app/guides/content/ugc-word-of-mouth.json
  - apps/api/app/guides/content/marketing-copywriting.json
  - apps/api/app/guides/content/landing-page-cta.json
  - docs/article-localization/batch038-source-link-corrections.md
  - tasks/open/2026-09-28-correct-misleading-ai-links-before-batch038.md
---

# Correct misleading AI links before Batch038 translation

## Why

Four published zh-TW marketing guides link ordinary words such as「標記」、
「參數」and「工具使用」to unrelated AI glossary entries. The links misdirect
readers and would be copied into four translations per guide. Correct the
published-language source packs first, then use a guarded new source revision
as the Batch038 translation baseline.

## Definition of done

- [x] Replace only the five unrelated AI article inlines with identical plain
      words; preserve all other body text, images, metadata, sources and links.
- [x] Pin the current published zh-TW source versions and record exact source
      and corrected pack hashes with a structural diff receipt.
- [ ] Open a reviewed PR with focused pack and task checks. Live source
      revision and translation import remain separate guarded steps.

## Steps

- [x] Identify the five unrelated links in four explicit article packs and
      claim narrow scope.
- [x] Verify production published source still matches repository baseline.
- [x] Apply five exact replacements and validate the complete JSON diff.
- [ ] Open PR and record its CI result.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --kind life --slug <slug>`
for all four slugs, focused guide pack/link tests from `apps/api`, and
`npm run check:tasks`. Compare normalized JSON and assert exactly the five
article-inline-to-text changes.

## Notes

Source links: `customer-journey-funnel` blocks 7 and 19,
`ugc-word-of-mouth` block 0, `marketing-copywriting` block 16, and
`landing-page-cta` block 21. Existing destination article links at each
guide's end are intentional and remain untouched.

The 2026-09-28T11:23:03Z guarded read-only source snapshot found all four
published zh-TW version 4 documents equal to the repository baseline. The
five-change exact diff receipt is documented in
`docs/article-localization/batch038-source-link-corrections.md`. No live
revision was written.

Draft PR #913 is open; full CI is pending. The task remains in review until
that check completes and the PR merges.

Four focused pack lints passed with inherited `no_summary` advisories. API
content/link tests passed (12 passed, 5 environment skips); `npm run
check:tasks` and `git diff --check` passed. PR CI remains pending.
