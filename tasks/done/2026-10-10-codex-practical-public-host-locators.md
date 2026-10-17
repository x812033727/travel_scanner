---
id: 2026-10-10-codex-practical-public-host-locators
title: Sanitize public Codex course evidence host locators
status: done
priority: P1
area: docs
owner: codex-gpt6-practice-design
claimed_at: 2026-10-10T18:39:38Z
created_at: 2026-10-10T18:39:34Z
completed_at: 2026-10-10T18:46:01Z
branch: codex/codex-practical-series-20261011
depends_on: []
scope:
  - docs/videos/codex-practical-01-cli/PRODUCTION-STATE.md
  - docs/videos/codex-practical-01-cli/claims.md
  - docs/videos/codex-practical-01-cli/verify-1.md
  - docs/videos/codex-practical-01-cli/verify-media.md
  - docs/videos/codex-practical-series/README.md
  - docs/videos/codex-practical-series/STATUS.md
  - docs/videos/codex-practical-series/VALIDATION.md
  - docs/videos/codex-practical-series/episodes/codex-practical-17-cli/brief.md
  - docs/videos/codex-practical-series/evidence/advanced-browser.json
  - docs/videos/codex-practical-series/evidence/final-build.json
  - docs/videos/codex-practical-series/evidence/independent-final-review.json
  - docs/videos/codex-practical-series/evidence/lesson-01-http-preview.json
  - docs/videos/codex-practical-series/evidence/lesson-01-media.json
  - docs/videos/codex-practical-series/evidence/validation.json
  - docs/videos/codex-practical-series/evidence/zip-followalong.json
  - docs/videos/codex-practical-series/lessons/17.md
  - tasks/done/2026-10-10-codex-practical-curriculum.md
  - tasks/done/2026-10-10-codex-practical-zip-root-followalong.md
  - tasks/open/2026-10-10-codex-practical-01-production.md
  - tasks/open/2026-10-10-codex-practical-02-production.md
  - tasks/open/2026-10-10-codex-practical-03-production.md
  - tasks/open/2026-10-10-codex-practical-04-production.md
  - tasks/open/2026-10-10-codex-practical-05-production.md
  - tasks/open/2026-10-10-codex-practical-06-production.md
  - tasks/open/2026-10-10-codex-practical-07-production.md
  - tasks/open/2026-10-10-codex-practical-08-production.md
  - tasks/open/2026-10-10-codex-practical-09-production.md
  - tasks/open/2026-10-10-codex-practical-10-production.md
  - tasks/open/2026-10-10-codex-practical-11-production.md
  - tasks/open/2026-10-10-codex-practical-12-production.md
  - tasks/open/2026-10-10-codex-practical-13-production.md
  - tasks/open/2026-10-10-codex-practical-14-production.md
  - tasks/open/2026-10-10-codex-practical-15-production.md
  - tasks/open/2026-10-10-codex-practical-16-production.md
  - tasks/open/2026-10-10-codex-practical-17-production.md
  - tasks/open/2026-10-10-codex-practical-18-production.md
  - tasks/open/2026-10-10-windows-automation-fixture-import.md
  - tasks/open/2026-10-10-windows-ffmpeg-empty-reference-range.md
---

# Sanitize public Codex course evidence host locators

## Why

Draft PR #1429 at head aeba5e61abe95965a913601e6a7e48a52d9bb745 failed web-checks and video-tests because new course documents and task records include personal Windows profile paths. The exact raw job log identifies 38 unique offending files. These public locators must be redacted without changing the teaching material, original evidence bytes or recorded receipt hashes.

## Definition of done

- [x] All 38 newly introduced host-locator files use public placeholders, with explicit non-executable locator notes.
- [x] Raw before copies and their content hashes are saved outside Git; receipt/source/approval hashes remain bound to original artifacts.
- [x] CLI 01 claims locator-only change is independently audited and its current hash is rebound in verify-1; the existing 20 PASS verdicts remain unchanged.
- [x] Public-redaction edits preserve protected video/script/authoring/author-evidence, the hygiene policy and unrelated files; the root agent's separate visual-only source change is audited independently.
- [x] Repo hygiene, task validation and relevant course/video checks pass; no commit, push or CI rerun is performed.

## Steps

- [x] Save the completed web-checks job log, head, job result and before-byte manifest outside Git.
- [x] Claim the precise scope with the root agent's explicit same-chat delegation for overlapping delivery/pilot documents.
- [x] Replace only public locator strings; make README build instructions portable and remove host-specific ZIP links.
- [x] Have another agent audit the redaction delta, preserve raw evidence bindings and update verify-1.
- [x] Run the narrow checks, record their real exit codes and close this task.

## How to verify

Run `node --test tools/repo-hygiene.test.mjs`, `node tools/tasks.mjs check`, `node tools/codex-practical/course.mjs check`, the CLI 01 lint and `git diff --check`. Compare current protected source hashes with the preserved before manifest. Independently compare parsed evidence JSON and the claims C01-C20 table so every change is a locator or explicit public-copy note, never a numeric result or evidence digest.

## Notes

2026-10-11: Root explicitly authorized `--force` for this same-chat delegated follow-up and paused its changes to these public documents and task records until freeze. This is not a takeover of another chat's ownership. Only the scope listed above is changed, plus this task's own lifecycle file.

Raw files and the private before/after mapping are preserved under `<home>/mokaair-work/codex-practical-series/runs/ci-host-sanitization-PR5B2q`. This is a redacted locator, not a command argument. The downloaded web-checks log SHA-256 is `a57f7ea6f4197a62396462d348306a95045a059c594681bb1f7de7a2e45ec7c2`; it records 2,215 tests, 2,202 passing, one failure in `tools/repo-hygiene.test.mjs:159`, and 12 expected skips. This was an actual new-document defect, not a flake. Advisory npm audit output was not the failing step.

The historical source hashes and approval hashes in `evidence/lesson-01-media.json` are preserved and explicitly described as bindings to the original artifacts. Existing ZIP, manifest, curriculum and generator hashes do not change because public locator prose is not part of those materialized packages. The current public claims hash is the sole source binding that verify-1 must update.

Independent privacy audit by rename_code_audit: 38/38 authorized document deltas PASS, seven parsed JSON records preserve all previous numeric results and digests, C01-C20 table byte-identical. Final audit receipt SHA-256 `bd4099c940b77a2fd695955793f119c645c7c9bb7f3d5167220612a2d7728644`; current claims SHA-256 `a73120df8d9a55cb5ea736425ca9c5c4d41cc5dfd95061d976390e92b22882f7` is rebound in verify-1. The private before manifest has 38 scope entries and seven protected files. Root's later authored visual-only outro change is recorded separately in verify-1; it preserves all 162 spoken lines/IDs and 20 claims, and is not part of the privacy delta.

Narrow checks used bundled Node v24.19.0, all actual exit 0: repo-hygiene 3/3 (no skipped/TODO tests), task validation 1,764 files, curriculum check 18 lessons/36 episodes/no errors, CLI 01 lint zero errors/zero warnings. Logs use new `sanitization-*-1.log` names in the external evidence directory; no historical check log was overwritten. Hygiene log SHA-256 `010392aad0eef1d944384c8ee8beb400437a38d1cd7e5d8a9ffcf0993a22f8bd`. Same-chat overlap warnings are intentional and authorized. Full CI remains the root agent's follow-up after push; this task does not call a local narrow pass a CI success.
