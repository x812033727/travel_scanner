---
id: 2026-10-22-independently-audit-c16-bialetti-treatment-sources
title: Independently audit C16 Bialetti Treatment sources
status: done
priority: P2
area: docs
owner: codex-c16-independent-source-review
claimed_at: 2026-10-22T18:20:43Z
created_at: 2026-10-22T18:20:38Z
completed_at: 2026-10-22T18:32:21Z
branch: codex/brand-story-bialetti-c16-treatment
depends_on: []
scope:
  - docs/videos/brand-story-independent-reviews/C16-bialetti-20261023.md
---

# Independently audit C16 Bialetti Treatment sources

## Why

PR #1698 proposes a C16 Bialetti Treatment and M01–M18 source matrix. Its author must not certify their own source work, and the owner needs a separate, exact-hash review before deciding whether to approve the direction. The parent task claims the Treatment directory, so this review uses one separate receipt path.

## Definition of done

- [x] An independently written, exact-hash PASS/HOLD receipt covers the six chapters and every M01–M18 claim, with direct source links and concrete corrections.
- [x] PR #1698 stays draft with `no-auto-merge`; the receipt is committed to its head and linked in the PR body.

## Steps

- [x] Check worktree, existing task and PR ownership; claim only the unique receipt file.
- [x] Open the prospectus, catalogue pages, museum objects, original research, fair advertisement and relevant patent/official records directly.
- [x] Record line-item verdicts tied to frozen hashes without changing the author's Treatment or matrix.
- [x] Run task/document checks, commit, push, and read back PR state.

## How to verify

`Get-FileHash docs/videos/story-everyday-bialetti-c16/{treatment,source-matrix}.md -Algorithm SHA256` individually; `npm run check:tasks`; `npm run test:docs-videos`; `git diff --cached --check`; `gh pr view 1698 --json headRefOid,isDraft,labels,body`.

## Notes

Review receipt: `docs/videos/brand-story-independent-reviews/C16-bialetti-20261023.md`. Frozen author SHA-256 values: Treatment `B0367876AF7F283ABEF9AA1F952918B3CE2653C28B48469375B25F813D1E6487`; matrix `02E1740E09E64C4BDAD90DFEAB01EBDCBA21DF89757029CEAC71D7E4888C85FF`.

Overall HOLD before owner Treatment approval: M18 confuses 1964 priority with 1965 Spanish filing and company assignee with an individual; M07's official INEI PDF is HTTP 404; M04/M05/M08's MIMIT excerpt PDF locator was not directly reproducible, though the identical ADI/Italian-patent-office catalogue pages were inspected in the complete PDF. The 1937 *Gazzetta Ufficiale* p.4219 directly confirms Spadini's separate model #14691, but not copying, collaboration, or a judgment; M17 remains HOLD. The narrative itself makes the key 1933 design vs. 1950/51 utility-model and moka vs. espresso distinctions.

Checks: `npm run check:tasks` exit 0 (2076 valid files; existing stale/overlap warnings). `npm run test:docs-videos` exit 1 because this worktree has no `pinyin-pro` package (`ERR_MODULE_NOT_FOUND` from `tools/video/tts/check.mjs`); no files in that dependency path were changed for this documentation review. The dependency was not installed solely for this unrelated suite failure.
