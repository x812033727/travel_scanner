---
id: 2026-10-14-keep-curio-source-card-footers-clear
title: Keep Curio source card footers clear of YouTube CC
status: done
priority: P1
area: tools
owner: codex-gpt6-curio-cc
claimed_at: 2026-10-14T06:54:33Z
created_at: 2026-10-14T06:54:01Z
completed_at: 2026-10-14T07:53:05Z
branch: codex/curio-h04-h06-v2-20261014
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
---

# Keep Curio source card footers clear of YouTube CC

## Why

The source-led Curio H04-H06 slides place source labels and photo captions into
the lower 15% of a 1080p frame reserved for optional YouTube captions. The
shared theme currently permits content to y=948, past the y=918 safe boundary.
These episodes need an opt-in layout adjustment that keeps their footers legible
with CC on without changing narration or affecting unrelated videos.

## Definition of done

- [x] Flagged scenes keep source labels and image captions above the lower
      15% caption area at 1080p and 720p; other scenes keep their current layout.
- [x] The change has a narrow automated test and the three Curio renders are
      visually checked with representative two-line CC.

## Steps

- [x] Add an opt-in scene layout flag to the template renderer.
- [x] Flag the affected Curio scenes under the separately claimed remake task.
- [x] Run template tests and inspect rendered frames with CC overlays.

## How to verify

Run `node --test tools/video/templates/templates.test.mjs`, then render the
three current episodes and inspect representative one- and two-line CC at
1920x1080 and 1280x720.

## Notes

The existing `2026-10-13-narrated-videos-tell-one-story-with` task owns only a
terminal fixture below `tools/video/templates`; the first broad scope for this
ticket overlapped it, so this ticket is narrowed to two exact renderer files.

The scoped implementation adds `data.cc_safe: true`, setting the template's
`--safe-bottom` to 212px for that scene. It leaves unflagged pages byte-for-byte
unchanged and rejects non-boolean flag values. A targeted test covers stats,
screenshot and photo templates; 27/27 tests pass. H04/H05/H06 flag 59/49/45
scenes respectively. Full renders completed; H04's 100-state CC overlay scan
found zero direct source-text collision after the fix, H05's 102-state scan
found zero direct glyph collision, and H06's two-line 1080p/720p samples kept
source text above the CC. Their audio timelines stayed unchanged by the flag.
