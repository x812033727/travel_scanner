---
id: 2026-11-10-news-reader-value-supplemental-evidence
title: Improve news reader value and opt-in official document evidence
status: done
priority: P2
area: api
owner: codex-news-editorial-supplemental
claimed_at: 2026-11-10T12:58:34Z
created_at: 2026-11-10T12:58:01Z
completed_at: 2026-11-10T13:27:48Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/supplemental.py
  - apps/api/tests/test_news_supplemental_evidence.py
---

# Improve news reader value and opt-in official document evidence

## Why

News should explain a concrete reader consequence without inventing testing or local
availability. The scanner currently skips an official article's own supporting documents,
even when those contain the account, pricing or usage limits needed to report the change.

## Definition of done

- [x] Writer/editor instructions retain evidence and publication rules while making the reader question and constraints explicit.
- [x] Official supplemental documents are disabled by default and bounded to two same-host, first-party in-story links without increasing independent-source counts.
- [x] Offline helper, scanner and existing AI tests plus Ruff and mypy pass in this worktree's own environment.

## Steps

- [x] Prepare a four-file candidate and exact source hashes outside the repository.
- [x] Obtain explicit owner approval for the two named overlapping file scopes.
- [x] Claim this task with the approved narrow exception, verify hashes and apply the candidate.
- [x] Run focused checks and hand the unchanged scope to the coordinating agent for PR/CI.

## How to verify

From `apps/api`, use this worktree's `.venv/Scripts/python.exe`:

`-m pytest tests/test_news_supplemental_evidence.py tests/test_news_ai.py tests/test_news_automation.py::test_scanner_fetches_only_articles_on_other_websites_as_evidence tests/test_news_automation.py::test_scanner_files_a_lead_only_page_only_when_it_links_to_evidence -q`

Run Ruff and strict mypy on the four scope files, then `node tools/tasks.mjs check`
from the repository root. No paid model calls or production configuration changes.

## Notes

- On 2026-11-10 the owner explicitly approved the concrete `ai.py` / `scanner.py`
  overlap exception and requested completing the PR and CI. Root delegated applying this
  exact four-file candidate to `codex-news-editorial-supplemental`; no merge or deployment
  authorization is inferred. `--force` is used only for this approved claim, not to take
  over, release or close any other task.
- Retained holders: `2026-10-29-news-automation-drafts-notable-new-ai`
  (`claude-opus-5-5`, ai.py/scanner.py),
  `2026-10-29-news-automation-reads-taiwan-tech-media`
  (`claude-opus-5-5`, scanner.py), and
  `2026-10-11-news-fetcher-is-refused-by-cloudflare`
  (`claude-opus-5-5-news-sources`, scanner.py). Open PR #1857 also changes ai.py;
  its branch and files are preserved. No other holder's task file is modified.
- Candidate: `<home>/.codex/tmp/mokaair-news-upgrade-20261110/backend-candidate/`.
  Original SHA-256: ai.py `cf2ff8fd6ec295e94b96ae84aaf1bbb0b18b3fd926ea54306ea3185aec1b07e1`;
  scanner.py `b57beca9f542b5fdfecc2bd19b4e767bd00d5f8af1fe1394cdffc9024310b2e0`.
- No schema fields, migration, new Jev/model calls, source entries, source settings or
  publication gates are added. Existing source configuration is untouched.
- The coordinating root agent owns committing, PR creation and CI; this delegated
  implementation does not commit or push. Local validation results will be appended here.
- Applied patch SHA-256: `692e6e11207a582abc11141f04ccd13e63df6605a14d565795fb0aabcdf78050`.
  `git apply --check` passed and all four resulting files matched the candidate SHA-256.
  An earlier patch-format check stopped before changes because new-file mode headers
  were missing; only the package headers were corrected before the successful check/apply.
- Direct post-application validation with this worktree's new Python 3.13.15 venv:
  **64 passed** (44 dedicated supplemental tests, 18 existing AI tests, 2 existing scanner
  regressions); strict mypy **4 files passed**; Ruff passed; scoped `git diff --check` passed.
  Logs are `applied-pytest.txt`, `applied-mypy.txt`, and `applied-ruff.txt` in the candidate
  directory above. All tests are offline mocks/SQLite; no paid model or production calls.
- The source configuration remains unchanged and the helper is therefore disabled unless
  a source explicitly sets `supplemental_paths`. Supplemental pages must meet the existing
  body-fingerprint readability floor. Review and CI are still root's next steps.
