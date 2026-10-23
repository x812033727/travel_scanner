---
id: 2026-10-23-intake-owner-approved-c-series-scripts
title: Intake owner-approved C-series scripts as manual admin review cards
status: in-progress
priority: P1
area: tools
owner: codex-c-series-integration
claimed_at: 2026-10-23T09:23:56Z
created_at: 2026-10-23T09:23:47Z
completed_at:
branch: codex/everyday-story-review-import-20261023
depends_on: []
scope:
  - tools/video/review/script-intake.mjs
  - tools/video/review/script-intake.test.mjs
---

# Intake owner-approved C-series scripts as manual admin review cards

## Why

The owner approved exact C03/C04/C05/C06/C07/C08/C10/C11/C14/C15 script and shot
directions in this conversation. The normal `review-push --gate script` rewrites
`script.md` from `video.json`, which would lose those approved bytes. The ten source
scripts use three different Markdown structures. Backend intake must preserve their
SHA-256 values, identify the approved episode, and avoid activating production.

## Definition of done

- [ ] All ten approved scripts appear on the correct `/admin/videos` episode cards with
      exact SHA-256 and line count readback, while C01/C02 and plan-only episodes do not.
- [ ] The series is paused, each episode planned, and no paid job is queued by intake.
- [ ] A second invocation is idempotent and a different live review is refused.

## Steps

- [x] Bind ten script paths, hashes, counts, owner approval PRs and basis in
      `approved-scripts.json`.
- [x] Dry-run the strict Markdown parser against all ten unchanged files.
- [ ] Pass mock transport tests and independent code review.
- [ ] Run production preflight, apply only after series readback, and verify all cards.

## How to verify

`node tools/video/review/script-intake.mjs` for local dry-run;
`node --test tools/video/review/script-intake.test.mjs` for HTTP gate behavior;
the same tool with `--apply` only after the paused backend series has been read back.

## Notes

The screenplay format covers C03/C04, table format C05/C06/C07/C08/C10/C11/C15,
and chapter bullets C14. The manifest excludes C01/C02 despite their local previews,
because a preview is not an exact owner script approval.
