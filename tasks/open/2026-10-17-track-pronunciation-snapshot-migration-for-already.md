---
id: 2026-10-17-track-pronunciation-snapshot-migration-for-already
title: Track pronunciation snapshot migration for already started non-A01 brand stories
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-17T08:30:40Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/story-lexicon-integration.md
---

# Track already-started brand stories after immutable pronunciation deployment

## Why

After approved runtime #1548 was deployed as 4f02734769f683615d1ca8b641026ac8cf1f87b5, the 16:30 Taipei worker log reported story-adapt-seiko-quartz-astron blocked by STORY_LEXICON_MIGRATION_REQUIRED. This is the deliberate legacy safeguard, not a failed model request. Its existing owner/project was not modified by this session. Other already-started stories may also need an independently reviewed source-preserving migration.

## Definition of done

- [ ] Read-only inventory identifies the exact non-A01 stories affected, existing task/worktree owners and current source/audit/media state.
- [ ] Coordinate each existing owner before taking project scope or performing data writes; preserve their original work and paid media.
- [ ] Document a reviewed source-bound migration and rollback/recovery plan for each authorized story, with actual runtime/host and owner gates.
- [ ] Record persisted readback and UI state; never treat a new lexicon snapshot alone as script or media approval.

## Steps

- [ ] Inventory held stories and match existing owners/tasks.
- [ ] Review each required migration and obtain any missing project-specific authority.
- [ ] Perform only authorized transitions, then read back and document the result.

## How to verify

Use current production read-only evidence and exact project/source hashes, then project and shared writer leases for any separately authorized operation. No paid call, retry, takeover or other-story data mutation is authorized by filing this ticket.

## Notes

A01 remains under 2026-09-28-video-story-pilot and 2026-10-16-bind-story-audits-and-narration-to; its pin migration does not authorize copying A01 assumptions to this Seiko story.
