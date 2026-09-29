---
id: 2026-09-27-news-evidence-excerpts-stop-at-8
title: News evidence excerpts stop at 8,000 characters, so the checks never see the rest of the page
status: review
priority: P1
area: api
owner: codex-p1-news
claimed_at: 2026-09-29T01:55:01Z
created_at: 2026-09-27T09:42:28Z
completed_at:
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/evidence.py
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/ai.py
  - apps/api/tests/test_news_evidence.py
---

# News evidence excerpts stop at 8,000 characters, so the checks never see the rest of the page

## Why

The scanner stores each evidence page as `body_text[:8000]` / `linked_text[:8000]`
(`scanner.py`), and a refresh does the same (`validation.py`, `row.excerpt = article_text[:8000]`).
The writer, the fact check, the locale reviews and Jev all read only that excerpt. On
2026-09-27 an independent review of the 11 held news drafts found two published-quality
errors that came from the cut, not from the models:

- `ai-news-gemini-3-8-tts-20260923`: every locale's FAQ said Google "gave no availability
  details by region", and listed Gemini Enterprise as available. The post's closing rollout
  section, after the cut, says Enterprise API access is "coming soon". Its footnote also
  bars voice replication in Illinois, Texas, the EEA, the UK, Switzerland and India.
- `tech-news-github-css-modules-migration-20260925`: the draft's timeline stops at the May
  2026 sx-prop milestone. The post's last sections, after the cut, give the answer to the
  headline: github.com has run on 100% CSS Modules since June 2026.

A refresh cannot help either: it re-reads the page and truncates it at the same point.

## Definition of done

- [x] A long official post's later sections reach the writer and the checks, either by storing
      more text or by storing the article body without the page's navigation and boilerplate.
      The model stages stay within their token budgets.
- [x] A test with an evidence page longer than today's limit proves that a fact past the old
      cut-off is available to the fact check.

## Steps

- [ ] Measure the extracted text length of the last month's evidence pages, per source, to
      choose a limit or an extraction change.
- [x] Change the scanner and `refresh_evidence` together, so that a refresh never shortens
      what the first scan stored.
- [x] Check the prompts' input budgets (`ai.py` also cuts `excerpt[:6000]` for the duplicate
      check).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py tests/test_news_pipeline.py -q
```

## Notes

- Found in the 2026-09-27 review of the held drafts. The corrected drafts could only delete
  or soften the wrong statements, because the correct facts were not in the stored excerpts.
- 2026-09-29, `codex-p1-news`: confirmed the newer article extractor already retains up to
  40,000 characters, but scanning and refresh still reduced that body to 8,000. Both now use
  the same `evidence_excerpt` helper and retain the existing extraction ceiling. Primary
  and linked evidence have the same rule; refreshing an old 8,000-character row restores the
  available body even if the source's full-text hash is unchanged.
- Model input is never shortened to fit. Structured stages estimate instructions, full
  payload and reply schema together with the existing CJK-aware estimator, and reject input
  over 64,000 estimated tokens before constructing a provider. This is an application cap,
  not a guarantee of a vendor/model's context size; the existing 32,000 output allowance is
  separate. `NewsInputTooLarge` inherits `ValueError`, so the job records the failure for
  editorial review without RQ retries. Saved drafts and evidence remain intact.
- The semantic duplicate check no longer cuts the joined sources at 6,000 characters. It
  checks the complete state and question against both configured Jev caps before spending
  a daily call; over-budget input is `manual` with `JevRequestTooLarge`. Jev's final article
  assessment reads the article and evidence hash, not raw excerpts, and is unchanged.
- Offline regression fixtures put rollout restrictions and a completed-migration fact beyond
  character 8,000 in both a primary page and a linked official page. They traverse the real
  scanner, SQLite storage, refresh, writer, independent verifier and final editor request
  construction. Other cases cover five near-40k English sources, CJK overflow, schema/input
  overhead, duplicate-check tail facts, both Jev caps, and the pipeline/job's no-retry path.
- The last-month production length distribution has **not** been sampled: this task did not
  access production data or change host settings. The implementation preserves the existing
  extractor limit rather than deriving a new one from unmeasured data. Actual pages longer
  than 40,000 characters still have the documented extraction ceiling. Production sampling,
  rechecking previously held articles and deployment remain separate work requiring the
  owner's production authorization; no existing article was republished or source refreshed.
- Local validation: the initial new-plus-existing `test_news_evidence.py`,
  `test_news_automation.py` and `test_news_pipeline.py` run passed 82 tests. After adding
  explicit writer delivery and pipeline/job failure-preservation coverage, the final
  focused evidence suite passed all 10 tests. Ruff passed all six changed Python files;
  focused mypy passed the same six files. No live database, model, network fetch or
  paid generation was used by these tests.
