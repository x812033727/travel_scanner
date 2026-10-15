---
id: 2026-10-15-complete-owner-release-and-playback-checks
title: Complete owner release and playback checks for Curio H09
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-15T13:19:09Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-h09/production-plan.md
---

# Complete owner release and playback checks for Curio H09

## Why

H09 production and three foreign listening approvals are complete, and its verified package is available in /admin/videos. The publish and languages cards remain pending. Owner release decisions, actual Studio upload and playback have not occurred and must not be inferred from media QA.

## Definition of done

- [ ] Read back the owner decision on the current publish card, or address any concrete requested change.
- [ ] Record the actual owner-authorized Studio/private-upload outcome and YouTube ID without inventing an upload from audio acceptance.
- [ ] After real audio-track upload, record the owner languages confirmation and verify the intended video/audio/subtitle playback; keep publication/schedule choices explicit.
- [ ] Refresh the primary expedition update before any public release and record whether the existing as-of date/ending remains accurate.

## Steps

- [ ] Ask the owner to complete the publish card, and read the persisted result against current metadata.
- [ ] Continue only the actual upload/release actions explicitly authorized by the owner; preserve all approved source media and listening receipts.
- [ ] Verify reported Studio actions and playback, then update production-plan with evidence and the distinct release state.

## How to verify

Use review-pull --slug curio-h09 --gate publish and --gate languages with the existing media workdir. Inspect current /admin/videos persisted IDs/status and compare all selected audio hashes to owner-acceptance receipts. Verify actual player language/subtitle selection only after the video exists. Do not substitute status=ready, a pending card or a private link for playback.

## Notes

Existing production checkout: C:/Users/x8120/.codex/worktrees/curio-h09/travel_scanㄐ; media: C:/Users/x8120/mokaair-work/videos/curio-h09. Draft PR #1503 remains unmerged. Publish review0e344aeb-ccb2-46d3-b695-83063b89c67a and languages reviewe8f86dd8-5f83-4602-ba6f-eaa48d27fbe2 were pending at production closure. All EN/JA/KO audio is owner-accepted; the languages button means actual Studio upload, not listening acceptance. See review/production-completion-20261015.json and backend-delivery-20261015.json. This unclaimed handoff does not authorize uploading, publishing, scheduling, deleting or merging. Existing financial authorization is synthesis/QA only; there is no new media work to buy.
