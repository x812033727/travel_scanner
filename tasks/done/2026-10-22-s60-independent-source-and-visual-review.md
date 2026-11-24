---
id: 2026-10-22-s60-independent-source-and-visual-review
title: S60 independent source and visual review
status: done
priority: P2
area: docs
owner: codex-s60-source-review
claimed_at: 2026-10-22T00:38:26Z
created_at: 2026-10-22T00:38:20Z
completed_at: 2026-10-22T00:39:40Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s60/review/r1-independent-source-visual.md
---

# S60 independent source and visual review

## Why

S60 has an author-only candidate. Its fixed source claims and written shot plan need independent review before narrative/media work. The author is separately repairing the creative files; this task owns only the R1 review receipt.

## Definition of done

- [x] The two fixed primary texts and every line-level claim/visual have been independently checked, with a concrete PASS/HOLD and bounded correction list in [R1 receipt](../../docs/videos/curio-s60/review/r1-independent-source-visual.md).

## Steps

- [x] Verify the raw source SHA-256 digests and read P01–P14 anchors, including Amundsen's letters and Scott's Jan 16/18 journal entries.
- [x] Compare 110 claims rows with 110 spoken lines and inspect every shot prompt against its line.
- [x] Report the R1 HOLD and scoped defects to the author and root; leave new author revisions for a fresh independent check.

## How to verify

`sha256sum /tmp/curio-s60-sources/amundsen-4229.txt /tmp/curio-s60-sources/scott-11579.txt`; a read-only Python comparison of `claims.md` rows with `video.json` lines returned 110/110 exact ID/text matches. `git diff --check -- docs/videos/curio-s60/review/r1-independent-source-visual.md` passed. No media or site approval was run.

## Notes

R1 is **HOLD**: `s60052` implies unsupported causality, `s60087` needs the actual night-travel anchor, `s60102` compresses different locations, `s60105` needs narrower wording or more anchors; roughly forty shot prompts are mismatched, several materially misleading. The first author creative hashes and grouped scene IDs are in the receipt. The task-board overlap forced claim was limited to this exact review receipt path; the author controls `brief.md`, `research.md`, `claims.md`, `script.md` and `video.json`.
