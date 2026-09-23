---
id: 2026-09-23-record-completed-localization-release-batches-007
title: Record completed localization release batches 007 and 017
status: done
priority: P1
area: docs
owner: codex-batch007-017-release
claimed_at: 2026-09-23T07:30:59Z
created_at: 2026-09-23T07:30:43Z
completed_at: 2026-09-23T07:41:16Z
branch: codex/localization-007-017-release-evidence
depends_on: []
scope:
  - docs/article-localization/releases/batch007-017
---

# Record completed localization release batches 007 and 017

## Why

Content PRs #660 and #659 are merged and their scoped production release completed
on 2026-09-23. Preserve the final per-article outcomes and evidence references so
the shared queue distinguishes content readiness from verified publication.

## Definition of done

- [x] Record all eight articles and forty language URLs with separate content,
  draft import, publication and browser acceptance results.
- [x] Bind final acceptance, journals, database protection, screenshots and hold
  clearance through hashes and precise evidence pointers.
- [x] Close the two completed content/release tasks using the task CLI.

## Steps

- [x] Independently check the candidate documents and every referenced evidence pin.
- [x] Preserve previous task findings and append verified completion records.
- [x] Keep raw snapshots, receipts and screenshots outside the repository.

## How to verify

Run `npm run check:tasks` and `git diff --check`. Resolve each evidence.json archive
path, recompute SHA256 and follow its JSON pointers. The release record covers
32 new language documents, 40 public URLs, 80 browser viewport cases and 40
expanded-source checks. Browser viewport evidence is not real device acceptance.

## Notes

See `docs/article-localization/releases/batch007-017/README.md` and its evidence
index. Existing deployed revision 6b2339ec89eda90ad37c9e99009723dfca89ba4a was adopted
after a fresh verified backup; application services were not restarted. The
post-clear read-only snapshot at 2026-09-23T07:28 confirms a clean host, no hold
and three healthy endpoints. No additional production operation is needed for
this documentation task. The global localization backlog remains open.
