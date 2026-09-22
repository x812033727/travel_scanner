---
id: 2026-09-22-preserve-reviewed-unselected-repository-locale-edits
title: Preserve reviewed unselected repository locale edits in localization bundles
status: in-progress
priority: P1
area: tools
owner: codex-source-preservation
claimed_at: 2026-09-22T04:58:51Z
created_at: 2026-09-22T04:40:57Z
completed_at:
branch: codex/article-localization-source-edit-preservation
depends_on: []
scope:
  - docs/article-localization/assemble_bundle.py
  - docs/article-localization/publish_bundle.py
  - docs/article-localization/repository_preservation.py
  - docs/article-localization/test_assemble_bundle.py
  - docs/article-localization/test_publish_bundle.py
  - tasks/open/2026-09-21-authorize-reviewed-source-corrections-in-localization.md
  - tasks/done/2026-09-21-authorize-reviewed-source-corrections-in-localization.md
  - tasks/open/2026-09-22-compare-deployed-localization-packs-by-validated.md
  - tasks/done/2026-09-22-compare-deployed-localization-packs-by-validated.md
  - tasks/open/2026-09-22-preserve-reviewed-unselected-repository-locale-edits.md
---

# Preserve reviewed unselected repository locale edits in localization bundles

## Why

The localization baseline correctly chooses the live published document when an
unpublished repository document differs. A later five-language pack must keep that
live document as its translation and version guard, but it must not silently erase a
separately reviewed repository-only description edit when the other four locales are
released. The existing fail-closed guards reject this case, and a generic drift bypass
would weaken protection for selected locales and concurrent editor work.

## Definition of done

- [x] An exact independent PASS receipt can preserve only `/description` from the
      final Git pack for an existing clean published locale that remains unselected.
- [x] The final Git commit, raw pack SHA-256, Git blob, live article/locale versions,
      live and baseline hashes, repository document hash and exact pointer diff are
      all revalidated by assembler and publisher.
- [x] Selected, publish, translation/publication target, batch and source-correction
      locales cannot use the preservation path.
- [x] The assembled full ArticlePack must equal the final Git ArticlePack before its
      exact raw bytes are copied; deployed full-pack equality and all runtime guards
      remain unchanged.
- [ ] Independent code review and draft pull request are complete.

## Steps

- [x] Align the closed receipt and manifest schema with independent read-only design.
- [x] Add shared receipt verification and explicit assembler opt-in.
- [x] Revalidate the receipt and unselected-locale constraint in the publisher.
- [x] Cover tamper, selected/target/source-correction overlap, final-pack source,
      metadata and target drift, runtime version conflict, deployed drift, rerun and
      backward compatibility.
- [ ] Freeze for independent review, address findings, then open a draft PR.

## How to verify

From the repository root with `apps/api` on `PYTHONPATH`:

`python -m pytest docs/article-localization/test_assemble_bundle.py docs/article-localization/test_publish_bundle.py docs/article-localization/test_install_bundle.py -q -o asyncio_mode=auto`

`ruff check tools/article-localization docs/article-localization`

Then run `npm run check:tasks` and `git diff --check`.

## Notes

The preservation receipt is a new approval; the batch015 read-only design report is
not itself authorization. Baseline `source_document`, `source_sha256` and
`locale_documents` remain live published bytes. The final release baseline must be
rebuilt at the final translation head so `repo_commit` and `pack_sha256` bind the
complete five-locale Git pack. No database schema or write operation changed.

The initial task claim incorrectly used `--force` while two merged tasks still held
overlapping scopes in `review`. Root verified both merged heads and their 9/9 CI runs,
then explicitly authorized correcting and closing those completed release records.
Their exact open/done task paths are included in this task's scope for that bounded
queue repair. This task must be released and claimed again without `--force` after the
old records are archived, before product-code validation continues.

Local validation before independent review: 125 passed, 59 skipped across all five
article-localization test modules; repository-wide article-localization Ruff, task
check and `git diff --check` passed. Task-check warnings are pre-existing stale claims
and unrelated overlaps. The two merged task records were archived with root-verified
merge, 9/9 CI and production-use evidence; this task was then released and reclaimed
without `--force`, removing its original scope overlap before validation resumed.
