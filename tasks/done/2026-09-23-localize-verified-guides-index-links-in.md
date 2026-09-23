---
id: 2026-09-23-localize-verified-guides-index-links-in
title: Localize verified guides index links in article translations
status: done
priority: P1
area: tools
owner: codex-batch020-routes
claimed_at: 2026-09-23T09:44:09Z
created_at: 2026-09-23T09:44:08Z
completed_at: 2026-09-23T09:51:05Z
branch: codex/article-localization-batch020-digital-continuity
depends_on: []
scope:
  - tools/article-localization/pipeline.py
  - tools/article-localization/test_pipeline.py
  - tools/article-localization/README.md
---

# Localize verified guides index links in article translations

## Why

The reading-notes article links to the Traditional Chinese guides index. The
translation pipeline rejects that unreviewed route instead of producing a
same-language URL. Verify all five public index pages, then add only that exact
route to the existing allowlist while retaining strict URL/locale guards.

## Definition of done

- [x] All five guides-index routes return 200 without redirect and have matching
      locale, canonical and localized heading.
- [x] New translations mechanically use their own language's guides-index URL.
- [x] Existing private-article, query/fragment, alias and source-URL protections
      still pass tests; document the exact live verification receipt.

## Steps

- [x] Check live routes sequentially with the editorial browser identity.
- [x] Add /guides to the verified allowlist and extend route/materialization tests.
- [x] Run pipeline tests and code checks, review the exact small diff, then commit
      alongside the batch020 content that requires this route.

## How to verify

Run the API Python runtime against tools/article-localization/test_pipeline.py,
ruff on the two Python files, git diff --check and task validation. The existing
materialization regression verifies locale changes and preserved external/source
URLs; query, fragment and trailing-slash variants must still fail before output.

## Notes

Root-only implementation scope; content authoring stays in its separate task.
Live receipt outside Git:
C:/Users/x8120/.codex/article-localization-release/batch020-candidate-inventory/guides-root-public-route-v2-20260923.json
SHA256 2ccb48c9873e59db9a771142337b273f2ed5255e4e83f41af35b1490067a486e.
All five requested URLs remained unchanged, returned 200, and matched html lang,
canonical and localized H1. The first capture waited for networkidle and timed
out; its failed-attempt record remains preserved, with no success claim. The
second capture used DOMContentLoaded to inspect the server-rendered page.

Author documents and source URLs remain immutable outside Git. Root integration
will record the exact mechanical link transformation and retain the original
zh-TW document. No source URL/date, article identity or publication flag changes.

Validation completed: pipeline unittest 32 passed; ruff for both Python files and
git diff --check passed. Independent reviewer /root/batch018_resume_review passed
94 checks, including AST verification that only the exact allowlist entry changes
execution, 25 source/target locale pairs, five actual materializations from the
reading-notes source and fourteen refused URL variants with no output artifacts.
Review receipt outside Git:
batch020-digital-continuity/independent-route-review/receipt-pass.json,
SHA256 9532fadd4ac123638f7ff196975c8e33026f5daa44c266b41be15590ce2f642b.
No network or production writes are performed by this tooling change. The
separate batch020 content task still owns author approval, mechanical integration,
CI and its release handover.
