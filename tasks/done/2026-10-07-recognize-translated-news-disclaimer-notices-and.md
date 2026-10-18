---
id: 2026-10-07-recognize-translated-news-disclaimer-notices-and
title: Recognize translated news disclaimer notices and avoid source claims in site notices
status: done
priority: P1
area: api
owner: codex-news-notices
claimed_at: 2026-10-07T13:13:07Z
created_at: 2026-10-07T13:11:35Z
completed_at: 2026-10-07T13:28:48Z
branch: codex/news-backlog-review-20261007
depends_on: []
scope:
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_policy.py
---

# Recognize translated news disclaimer notices and avoid source claims in site notices

## Why

Fifteen held crypto translations already have explicit investment disclaimers in a
callout title or a Japanese/Korean negative phrase. The news helper recognizes only
the exact marker in the body, adds another notice, and the locale reviewer removes
the duplicate. The helper then adds it again. The site's generated notice also
claims official sources were used even when the article has only a newsroom source.

## Definition of done

- [x] Explicit existing disclaimers survive correction without a second notice.
- [x] Newly generated notices do not claim sources that the article did not use.
- [x] Historical site notices keep their existing fingerprint exclusion; authored
  warning edits still require a new verification hash.
- [x] General risk warnings do not replace the required disclaimer, and financial
  recommendation checks remain enforced.

## Steps

- [x] Recognize canonical title/body markers and the observed Japanese/Korean
  negative variants, canonicalizing the same callout for shared finance lint.
- [x] Keep full callouts intact when the canonical text cannot fit.
- [x] Add source-neutral generated notices and regression coverage in all five locales.
- [x] Validate policy, pipeline and saved-bundle behavior.

## How to verify

From `apps/api`:

```powershell
& .venv/Scripts/python.exe -m ruff check .
& .venv/Scripts/python.exe -m mypy app
& .venv/Scripts/python.exe -m mypy tests
& .venv/Scripts/python.exe -m pytest tests/test_news_policy.py tests/test_news_automation.py tests/test_news_pipeline.py tests/test_news_resume_saved_bundle.py
```

All lint/type checks passed; the four affected suites passed 262 tests.

## Notes

This is a code repair, not a production release or a review approval. Live backlog
execution and rollout are tracked in
`2026-10-07-resolve-current-news-review-and-redraft`. No model settings, evidence
hashes, review decisions or retry caps were changed by this patch.
