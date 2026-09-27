---
id: 2026-09-27-batch030-host-diagram-label
title: Refine batch030 English diagram and Korean aftercare summary
status: done
priority: P2
area: docs
owner: codex-batch030-pair-b
claimed_at: 2026-09-27T11:37:07Z
created_at: 2026-09-27T11:37:05Z
completed_at: 2026-09-27T11:40:59Z
branch:
depends_on: []
scope:
  - apps/web/public/guides/wordpress-host-migration/diagram-1-en.svg
  - apps/api/app/guides/content/wordpress-migration-aftercare.json
---

# Improve English host migration diagram label

## Why

Independent review found two localized phrases to refine: the English host-move diagram card says the unnatural "Copy and new host"; the Korean aftercare description adds a migration tool that the published zh-TW description never mentions. Keep the change limited to these two fields.

## Definition of done

- [x] English diagram card reads "Copy site to new host" without overflow.
- [x] Korean aftercare description opens with the source meaning "after completing the move" and does not mention a tool.

## Steps

- [x] Change only the two phrases, preserve source and all other localized fields.
- [x] Re-render the SVG, inspect, rerun focused checks, and bind new hashes.

## How to verify

Render diagram-1-en.svg at 1600x900, verify the card text stays within its frame, run scoped pack lint and structural/source checks, and compare changed paths to the previous commit.

## Notes

This follows Pair B content commit a7ebd576. The original published zh-TW v4, #855 prerequisite, and other Pair B translations/assets remain unchanged.

- Verified by `C:\Users\x8120\.codex\article-localization-release\batch030-pair-b\pair-b-followup-validation.json` SHA-256 `f9acd011e9d5865d590f3c93b55a8c781f1408571aea1c4127ca90dae7cf08a6`. Deep comparison with a7ebd576 shows exactly two field/node changes. English diagram re-rendered at 1600×900 and visually inspected; card text has 27.656 px right margin. Pack lint exit 0.
