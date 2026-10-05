---
id: 2026-10-05-news-generated-punctuation-before-review
title: Normalize generated CJK news punctuation before review
status: done
priority: P1
area: api
owner: codex-news-punctuation
claimed_at: 2026-10-05T10:28:20Z
created_at: 2026-10-05T10:28:18Z
completed_at: 2026-10-05T10:48:24Z
branch: codex/news-video-stall-fixes-20261005
depends_on: []
scope:
  - apps/api/app/news_automation/typography.py
  - apps/api/app/news_automation/schemas.py
  - apps/api/tests/test_news_typography.py
---

# Normalize generated CJK news punctuation before review

## Why

New news candidates can finish drafting, translation and final editing, then stop
at `news_hard_checks_failed` for ASCII punctuation next to CJK text. The final
editor only repairs hard-check problems its correction newly introduced; an
existing punctuation problem can survive a passing edit. Rewriting the entire
article wastes already completed model work.

Provider replies already have a controlled document-validation boundary before
the pipeline reviews or fingerprints their text. Normalize only generated prose
there, keeping the existing punctuation policy and publication gates intact.

## Definition of done

- [x] Generated writer, verifier, translation and locale/final-editor documents
      enter the pipeline with full-width punctuation at immediate CJK adjacency.
- [x] URLs, link targets, code, source metadata, credits, Latin/numeric punctuation
      and the original block/inline structure remain unchanged.
- [x] Review fingerprints describe the normalized provider text. Saved articles
      and direct `GuideDocument` human edits keep their original text and hashes.
- [x] Focused regression and existing news compatibility checks pass.

## Steps

- [x] Add a pure document typography helper with URL masking and rich-inline
      boundary handling matching the existing hard-policy detector.
- [x] Add `NewsProviderReply` to the four news reply schemas, retaining their
      existing provider JSON schemas and strict shape validation.
- [x] Test actual punctuation gates, untouched non-prose fields, schema inputs,
      idempotence and pipeline review/hash binding.
- [x] Record final check results before handing the changes to the parent task.

## How to verify

```powershell
cd apps/api
uv run pytest tests/test_news_typography.py tests/test_news_automation.py tests/test_news_pipeline.py tests/test_news_review_actions.py tests/test_news_resume_saved_bundle.py tests/test_news_backfill_cli.py tests/test_news_assets_storage.py -q -p no:cacheprovider
uv run ruff check app/news_automation/typography.py app/news_automation/schemas.py tests/test_news_typography.py
uv run mypy app/news_automation/typography.py app/news_automation/schemas.py tests/test_news_typography.py
```

## Notes

- Scope audit: do not touch `pipeline.py` or existing news test files owned by the
  fresh-switches and saved-bundle follow-ups. Open PRs #1269 and #1272 also change
  `ai.py` and `test_news_pipeline.py`; these changes use `schemas.py` and new files.
- Replies for translation and locale review contain no locale field, so the
  generated-output rule follows Han/kana adjacency in every locale. Japanese
  commas next to CJK also become full-width; whole Latin runs and numeric marks
  stay unchanged. This does not loosen the existing locale-specific hard checks.
- The helper returns a new validated document and never changes its input. It
  runs on provider documents only, before pipeline assessments are recorded.
- Old held bundles are deliberately unchanged. Their recorded reviews are not
  rebound; recovery still needs the supported saved-bundle/editor/reverify path
  and the applicable publication decisions.
- No provider, budget, auto-publish setting, production row, paid generation,
  retry or publication was changed.
- Validation on 2026-10-05: the focused suite plus six existing news suites passed
  267 tests in 66.99 seconds, with exit 0. New coverage has 42 cases including an
  actual pipeline run that checks the saved normalized text against all five
  final-review hashes and the Traditional Chinese verification hash. Scope Ruff
  and mypy passed with exit 0; `git diff --check` was clean.
- API dependencies were installed with `uv sync --frozen` in this worktree's
  ignored `.venv`. These are offline model/network fixtures, not a live provider
  call, production publication, deployment, or owner content acceptance.
- Independent review by `video_flow` completed. It confirmed that all four news
  reply models retain byte-equivalent `model_json_schema()` results compared
  with their pre-change schemas, while generated prose is normalized before
  pipeline review fingerprints are recorded.
- After integrating current main, the combined API check passed 166 tests with
  1 skip. It included the 42 new typography cases, news pipeline compatibility,
  producer-state and related backend coverage. The full repository suite is
  still running under the parent task; this completed implementation task does
  not claim that broader result. Production has not been deployed, and held
  saved articles have not been retried or published by this task.
