---
id: 2026-10-17-migrate-a-story-started-before-lexicon
title: Migrate a story started before lexicon pinning (no narration yet) to a pinned snapshot
status: in-progress
priority: P1
area: tools
owner: claude-opus-5.5-lexicon-migrate
claimed_at: 2026-10-17T08:38:40Z
created_at: 2026-10-17T08:38:24Z
completed_at:
branch: claude/story-lexicon-started-migration
depends_on: []
scope:
  - tools/video/core/lexicon-migration.mjs
  - tools/video/core/lexicon-migration.test.mjs
  - tools/video/cli.mjs
  - docs/videos/story-lexicon-migration.md
---

# Migrate a story started before lexicon pinning (no narration yet) to a pinned snapshot

## Why

#1548 pins an immutable per-story pronunciation snapshot before a story's first chapter, and
`initializeStoryLexicon` refuses any story that has already started. A story that started before
#1548 was deployed therefore holds forever with `STORY_LEXICON_MIGRATION_REQUIRED`, even when no
narration was ever synthesized. Production's `story-adapt-seiko-quartz-astron` (B25) is such a
story: six chapters written, checked and heard, the script approved, no timeline and no audio.

A01 (`story-rolling-suitcase-v2`, 80 recheck-audit events) is out of scope: it needs the separate,
independently reviewed transition tracked in `2026-10-16-bind-story-audits-and-narration-to`.

## Definition of done

- [ ] An operator can see, without writing anything, whether a started story may be pinned, every
      precondition's result, and the snapshot SHA-256 it would get.
- [ ] With `--apply`, a story that passes every precondition gets the same genesis snapshot bytes
      `initializeStoryLexicon` would give a new story, through the same dual-lease, intent,
      read-back and receipt transaction, plus an immutable record saying it was a migration.
- [ ] A story with a timeline, narration audio, a recheck audit (A01) or an audio-or-later approval
      is refused with a specific error code and no byte changes.

## Steps

- [x] `tools/video/core/lexicon-migration.mjs`: preconditions, plan, transaction.
- [x] `node tools/video/cli.mjs story-lexicon-migrate --slug S [--apply]`.
- [x] Tests: allowed, idempotent, each refusal, A01 80-link fixture bytes unchanged.
- [x] `docs/videos/story-lexicon-migration.md`.

## How to verify

```bash
node --test tools/video/core/lexicon-migration.test.mjs tools/video/core/lexicon-store.test.mjs
npm run check:tasks
```

## Notes

Scope deliberately avoids `lexicon-store.mjs`, `story-lexicon.mjs` and
`story-lexicon-integration.md`, which the in-progress task
`2026-10-16-bind-story-audits-and-narration-to` (codex, A01 transition) still holds. Consequences:

- The transaction is a second copy of `lexicon-store.mjs`'s `publish` (same leases, intent, receipt
  format), so `recoverCommittedStoryLexicon` recovers it unchanged. A test asserts the migrated
  version/event/current bytes equal what `initializeStoryLexicon` writes for the same inputs, so the
  copies cannot drift silently. When the A01 task closes, `publish` could be exported and shared.
- The strict reader only accepts `reason: "initial_snapshot"` at sequence 1, so the genesis event is
  byte-identical to a normal genesis. The migration is recorded in an immutable sidecar
  `story-lexicon/migrations/<event_sha256>.json` (ignored by the reader) and in the intent/receipt.
- Review of #1550 (2026-10-17): with a wrong or empty work directory every work-side check passed
  and `--apply` wrote `current.json`. Fixed by `workdir_is_this_story` (work directory exists,
  `auto.json` names this slug and has story state, `story/chapters` has a chapter file), checked
  before either lease and again inside them; it replaces the old `started` check, which a docs
  `video.json` alone satisfied. On the host pass `VIDEO_WORKDIR=/var/lib/mokaair/video-work`.
