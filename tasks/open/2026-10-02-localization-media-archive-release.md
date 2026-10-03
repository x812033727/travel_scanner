---
id: 2026-10-02-localization-media-archive-release
title: Verify localization source archives before explicit media-retention release
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-02T14:14:45Z
completed_at:
branch:
depends_on:
  - 2026-10-02-ten-drama-audio-handoff-audit
scope:
  - tools/video/production/archive.mjs
  - tools/video/production/archive.test.mjs
  - tools/video/production/retention.mjs
  - tools/video/production/retention.test.mjs
  - tools/video/automation/tidy.mjs
---

# Verify localization source archives before explicit media-retention release

## Why

Chinese-first dramas promise later independent cast audio and CC. The retention
guard intentionally holds their paid picture sources, dry takes and M&E rather
than treating an empty current language selection as completed delivery. An
explicit release operation remains unimplemented; elapsed time and manual
status edits must never substitute for a verified archive and owner instruction.

## Definition of done

- [ ] Define a source-bound archive covering scripts, line/speaker IDs, accepted
  picture master, dry takes, narration, music, SFX, room tone and actual hashes.
- [ ] Verify the archive is complete and recoverable before any source removal.
- [ ] Require a concrete owner instruction for release or cancellation and keep
  the audit record; repair/invalid metadata must continue to hold media.
- [ ] Test loss, corruption, partial archives and episode/compilation relationships.

## Steps

- [ ] Design the archive destination and inventory before implementing release.
- [ ] Build read-only verification and restoration proof.
- [ ] Implement explicit release after verification with history preserved.

## How to verify

Use local fake media and a restored archive. Missing or mismatching members,
unknown outcomes and an unverified destination cannot enable tidy. Ordinary
slides keep their current retention policy. This ticket authorizes no production
cleanup, paid media generation or publication.

## Notes

- Follow-up to the ten-drama audit, not a prerequisite to keeping current media.
- Current safe behavior is to retain the marked episodes and their compilation.
- No media exists for the ten target series yet; owner archive storage and release
  can be decided when there are concrete completed deliveries to preserve.
