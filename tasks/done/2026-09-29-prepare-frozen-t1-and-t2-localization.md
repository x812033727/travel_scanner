---
id: 2026-09-29-prepare-frozen-t1-and-t2-localization
title: Prepare frozen T1 and T2 localization release candidates
status: done
priority: P2
area: docs
owner: codex-release-candidate-prep
claimed_at: 2026-09-29T05:06:36Z
created_at: 2026-09-29T05:06:21Z
completed_at: 2026-09-29T05:21:41Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/article-localization/releases/p1-20260929-t1-t2
  - docs/work-status-2026-09-29-article-release-plan.md
---

# Prepare frozen T1 and T2 localization release candidates

## Why

The approved article release plan lists exact T1/T2 candidates but does not yet
contain a frozen handoff package. Preserve the existing reviewed bytes and make
the 16-document allowlist independently verifiable before any release work.

## Definition of done

- [x] Freeze exactly four articles and 16 target documents, with source, pack,
      localized artwork and existing review evidence hashes, outside the repo.
- [x] Independently verify the allowlist, bytes, schema and review bindings;
      prove changed or out-of-scope input cannot pass the offline validator.
- [x] Commit only a sanitized preparation README/evidence and updated PR
      prerequisites, without machine paths, database identifiers or credentials.
- [x] Retain T2 editorial review, guarded-write driver, same-image PostgreSQL
      rehearsal and fresh production authorization as explicit missing gates.

## Steps

- [x] Check active tasks, local/remote branches and open PR file scopes.
- [x] Build the private candidate-only package from exact merged Git blobs.
- [x] Run independent verification and record the results and limitations.
- [x] Update the existing approval plan and include preparation evidence in #966.

## How to verify

Use the frozen package's documented builder and read-only verifier with the API
Python environment. Record exact input/output hashes and meaningful negative
cases in the public evidence. Run `npm run check:tasks` and `git diff --check`.
The SQLite exercise verifies synthetic import mechanics only; it does not claim
a same-image PostgreSQL release rehearsal or authorize a live import.

## Notes

T1 is marketing-mix-models and brand-tone-vibe-marketing. T2 is
seo-keyword-research and seo-title-writing. All use en/ja/ko/zh-CN. The original
content scopes remain with their authors; this task changes only preparation
records and the shared approval plan. Original release tickets remain open.

The prior production inventory is a historical, approved read-only snapshot,
not fresh preflight. Docker is unavailable in this checkout environment.
Existing Route B inputs do not contain Route A pipeline review receipts; this
task must not invent those receipts or claim a guarded publisher was executed.

## Completion evidence

Prepared the private immutable candidate from source commit
`086e006cdfd5a982da9f412d28939ebb8eb4b453`, with manifest SHA-256
`d2e3fc9a7346b7e8345bcce13a0db7771be0bcffd79e4b0ed4adba49dcde5ab0`.
The public preparation record is
`docs/article-localization/releases/p1-20260929-t1-t2/README.md` with
`evidence.json`; no private receipts, database IDs or machine paths are committed.

- Author validator and separate ArticlePack/GuideDocument verification passed.
- Independent integrity and five tamper-rejection tests: 6 passed, 0 skipped.
- Synthetic SQLite import/replay test: 1 passed, 0 skipped. Both waves created
  only eight target locales each; all existing rows and revisions survived,
  and replay produced no writes. Synthetic IDs and versions were used.
- Scoped four-pack lint: 0 errors; existing warnings remain (20 no-summary,
  2 English text length, 8 localized internal links). No editorial waiver.
- Original T1 review retained; T2 editorial review, Route B transaction guard,
  same-image PostgreSQL rehearsal and newly approved live steps remain open.

Included in draft PR #966. Main integration updates #940/#941 to merged but
preserves their original review heads and does not assert deployed content.
