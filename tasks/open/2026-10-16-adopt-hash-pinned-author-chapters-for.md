---
id: 2026-10-16-adopt-hash-pinned-author-chapters-for
title: Adopt hash-pinned author chapters for brand stories
status: in-progress
priority: P1
area: tools
owner: codex-brand-author-adoption
claimed_at: 2026-10-16T00:11:21Z
created_at: 2026-10-16T00:07:46Z
completed_at:
branch: codex/story-author-chapters-20261016
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - docs/videos/STORY.md
---

# Adopt hash-pinned author chapters for brand stories

## Why

Five brand-story episodes have reviewed full narration and six-chapter formal prototypes, but the normal story importer carries only a plan and the worker asks a model to write the chapters again. Passing the prototypes through `readChapterAnswer` would also discard title cards and normalize author claims. A distinct, explicit adoption path must preserve the exact chapter bytes and leave claims `UNCHECKED` for the worker's real verifier.

## Definition of done

- [x] An operator can stage one exact six-chapter package with SHA-256 pins before the worker's first writer step; the worker adopts it as its actual chapters without calling the writer.
- [x] The adoption validates the current series plan, exact slug, every chapter, scene/line/claim reference and `UNCHECKED` verdict before writing, then enters the existing lint, verifier, listener and narrative gates.
- [x] Invalid/stale packages and authored lint errors stop safely; no automatic writer rewrites or fabricated approval/paid media occur.

## Steps

- [x] Add a narrowly scoped package contract and adoption step to `story.mjs`, retaining original chapter JSON and hash evidence.
- [x] Test valid adoption, changed hashes/plan, invalid claims and continued verification without a writer call.
- [x] Document the staging order and the remaining human review and production gates.

## How to verify

Run the bundled Node runtime on `tools/video/automation/story.test.mjs` and focused story tests. Inspect `auto.json`, six installed chapter hashes, merged `video.json` and claims table; confirm the first paid/AI next step is the ordinary verifier, with no writer call.

## Notes

2026-10-16 collision survey: the overlapping `2026-10-14-support-10-minute-minimax-cute-brand` ticket is in `review` under this same 8a78 task's `codex-8a78-story-route` owner. Its PR #1499 merged as `a1b6b1149` on 2026-10-15; its old branch has no active worktree or remote head, and `who-is-on-it --scope tools/video/automation/story.mjs` found no open PR touching this file. The root task explicitly confirmed this provenance and permits a documented, scoped `--force` claim if ordinary claim refuses. Work starts from fresh `origin/main=a291eb788` in a separate worktree. This ticket does not authorize production writes, paid model/media calls, deployment or publication.

Local focused test: three author-package cases passed, including 13 existing verifier/listener/narrative calls without a writer call or media creation. `npm run check:tasks` exited 0 with existing stale-owner and overlap warnings, including the documented same-chat stale #1499 scope. Full story suite running. No production, supplier or model calls were made.
