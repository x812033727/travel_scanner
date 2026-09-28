---
id: 2026-09-28-ai-video-season-one-review-pack
title: Package AI video season one review materials
status: done
priority: P2
area: docs
owner: codex-ai-video-season
claimed_at: 2026-09-28T01:51:48Z
created_at: 2026-09-28T01:51:37Z
completed_at: 2026-09-28T01:53:35Z
branch: codex/ai-video-season-01
depends_on: []
scope:
  - docs/ai-video-season-01
---

# Package AI video season one review materials

## Why

Preserve the completed Chinese AI explainer season as a reviewable source package without committing large local media exports or unrelated product changes.

## Definition of done

- [x] Six episode scripts, twelve thumbnails, source ledger, subtitles, operations plan and build tools are reviewable in Git.
- [x] Local-only video outputs are identified by checksums and documented rebuild requirements.

## Steps

- [x] Isolate the package on a branch from origin/main and check scope collisions.
- [x] Copy editorial inputs and QA receipts; exclude audio/video caches and archive outputs.

## How to verify

Run Python compilation for tools, validate episode/source JSON and thumbnail inventory, and run npm run check:tasks. Full media validation was run in the original production folder; validation.json and media-checks.json retain those results. New checkouts require Windows Hanhan Desktop, Pillow and ffmpeg plus rebuilding before --validate.

## Notes

This task covers packaging for review only. Human pronunciation review, final scene editing and YouTube publication remain unfinished and are recorded in release-checklist.csv and the follow-up task. No production or account changes. Review exports are not final cinematic videos and one million views is an unverified target.
