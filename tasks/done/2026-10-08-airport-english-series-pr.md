---
id: 2026-10-08-airport-english-series-pr
title: Audit and preserve the airport English sixty-day prototype
status: done
priority: P2
area: docs
owner: codex-airport-english-pr
claimed_at: 2026-10-08T11:45:56Z
created_at: 2026-10-08T11:45:44Z
completed_at: 2026-10-08T12:03:13Z
branch: codex/airport-english-series-pr-20261008
depends_on: []
scope:
  - docs/videos/airport-english-60-days
---

# Audit and preserve the airport English sixty-day prototype

## Why

The previously delivered 60-day airport listening series was built outside the
repository with a custom prototype generator. Basic decoding and duration checks
were incorrectly presented as completion. The user requested a PR, then a full
recheck against this repository's video rules. Preserve the teaching sources and
record the actual compliance findings before any production release claim.

## Definition of done

- [x] All 60 episodes have an auditable technical/content review with explicit limits.
- [x] Text-only sources are preserved with hashes and an unapproved status.
- [x] Unfinished remediation is recorded in an open task; the draft PR reports the
      audit without implying that the original media are ready for publication.

## Steps

- [x] Check local worktrees, remote branches, open PRs and task scopes; claim work.
- [x] Read channel rules and distinguish explicit user requirements from defaults.
- [x] Consolidate media, captions/player and independent content audit evidence.
- [x] Preserve sources without media, credentials or private hosting identifiers.
- [x] Run applicable repository checks and repeat the collision check before PR.

## How to verify

Run `npm run test:tools`, `npm run test:docs-videos`, and `npm run check:tasks`.
Verify the source-snapshot manifest hashes, audit totals and links. The media
audit reads all 300 original streams, subtitle review uses the repository's
`checkCues`, and content review checks actual quiz replay selections. These are
audit checks, not a substitute for production `check-audio`, `qa` or approvals.

## Notes

- Isolated worktree `/workspace/airport-pr`, based on `origin/main` at `c6454463`.
- Media remain outside Git. Source-snapshot flags such as `script_ready` are
  historical generator output and do not confer approval.
- User requirements retained: English default/always visible, four translated
  CC and teaching-audio choices, English dialogue, 600 seconds and 60 days.
- No upload, publication, paid synthesis, re-encoding or production approval is
  part of this audit. Follow-up remediation must use the official workflow.
- Use a draft PR: this repository automatically merges eligible non-draft PRs.
- Full audits: 300 media, 300 SRTs, 180 quizzes; 30 replay selections need repair,
  all masters fail channel video settings and all audio fails format/loudness.
- Snapshot: 487 sources hash-verified; 486 unchanged, one private URL redacted
  with source/copied hashes. All JSON parse and documentation links resolve.
- Validation: test:tools 2,185 passed / 4 skipped / 0 failed; test:docs-videos
  199 passed; check:tasks passed (existing unrelated stale-claim warnings only).
- Historical 63 SRTs contain 1,155 trailing-whitespace findings. They are preserved
  byte-for-byte; diff whitespace checks pass outside those historical SRTs.
- Repeated who-is-on-it after fetch: only this task owns the scope; no other
  airport PR or origin/main change found. Source/media rules independently reviewed.
- Unfinished work: `2026-10-08-airport-english-series-remediation` remains open.
