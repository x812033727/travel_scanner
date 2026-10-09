---
id: 2026-10-08-mods-tutorial-clarity
title: Rebuild Claude Code Mods tutorial around one concrete example
status: done
priority: P1
area: docs
owner: codex-7645-video-clarity
claimed_at: 2026-10-08T16:10:35Z
created_at: 2026-10-08T16:10:09Z
completed_at: 2026-10-08T16:40:38Z
branch: codex/mods-clarity-20261009
depends_on: []
scope:
  - docs/videos/claude-code-mods-no-sandbox-before-install
---

# Rebuild Claude Code Mods tutorial around one concrete example

## Why

The owner compared our Mods video with Gary Chen's tutorial and asked us to start improving it. The original changes metaphors across chapters and spends substantial time on version labels without showing one complete operation. Rebuild the local source around the official tool-call counter so the viewer can explain what changes, why it changes and how to check it.

## Definition of done

- [x] A complete Traditional Chinese tutorial script follows one tool-call counter from visible outcome through mechanism, trust checks, loading, expected results and troubleshooting.
- [x] Original voice settings are preserved, official facts are sourced, and expected/demo output is distinguished from actual local execution.
- [x] The source passes lint and independent content review, with rendered visuals available for owner review.
- [x] Remaining audio, final-video and publication work is explicitly recorded without reusing original approvals.

## Steps

- [x] Read the original source, narration and live official documentation.
- [x] Rewrite the complete source and create a stable progressive diagram.
- [x] Render and inspect the visual sample; correct independent-review findings.
- [x] Save a reviewable handoff and verification evidence.

## How to verify

Run `node tools/video/cli.mjs lint --slug claude-code-mods-no-sandbox-before-install`; render into `<home>/mokaair-work/mods-clarity-20261009/preview/` and inspect the resulting frames. Use repository video-document and task checks before pushing. The local Mod candidate is not a successfully executed demo.

## Notes

2026-10-09 (Taipei): Work is a local revision only. Original source SHA-256 is `bd703aad6591a898ecbb46a824b76cfa2a5cdab05a856a857b8dbb50fad6103c`; immutable source/approval snapshots are outside the repo under `<home>/mokaair-work/mods-clarity-20261009/source/`. A selected-English-dub producer lease exists on the original; a read-only process check timed out, so liveness is unknown. Do not replace production source or reuse its approvals.

Automatic approval review rejected the combined isolated CLI `--version` / `plugin validate` / `plugin test` execution with only `blocked by policy`. It was not retried. Fixtures and tests are candidates, not successful execution evidence; the tutorial must label official/illustrative output accordingly. No paid speech or image generation has been started for this revision.

Delivered 139-line source, claims and demo template, five original diagrams and 93 static states with narration. Lint 0 errors/0 warnings; independent reading and static reviews completed; counted-event reveal mismatch fixed. Estimated longest state 10.9 s, not measured media timing. New narration/cut/QA/publication remains explicitly open in `2026-10-08-mods-tutorial-revision-production`. Full evidence and hashes: `docs/videos/claude-code-mods-no-sandbox-before-install/revision-review.md`.
