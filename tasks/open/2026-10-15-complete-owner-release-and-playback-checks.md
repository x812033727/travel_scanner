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
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/production-plan.md
---

# Complete owner release and playback checks for Curio H09

## Why

H09 production and three foreign listening approvals are complete. The current publish and languages cards are approved, and an owner-initiated private API upload has finished. Actual Studio dub delivery, playback and a publishable Studio upload remain to be verified; backend language declarations do not establish these outcomes.

## Definition of done

- [x] Read back the owner decision on the current publish card, or address any concrete requested change.
- [x] Record the actual owner-authorized Studio/private-upload outcome and YouTube ID without inventing an upload from audio acceptance.
- [ ] After real audio-track upload, record the owner languages confirmation and verify the intended video/audio/subtitle playback; keep publication/schedule choices explicit.
- [ ] Refresh the primary expedition update before any public release and record whether the existing as-of date/ending remains accurate.

## Steps

- [x] Ask the owner to complete the publish card, and read the persisted result against current metadata.
- [x] Continue only the actual upload/release actions explicitly authorized by the owner; preserve all approved source media and listening receipts.
- [ ] Verify reported Studio actions and playback, then update production-plan with evidence and the distinct release state.

## How to verify

Use review-pull --slug curio-h09 --gate publish and --gate languages with the existing media workdir. Inspect current /admin/videos persisted IDs/status and compare all selected audio hashes to owner-acceptance receipts. Verify actual player language/subtitle selection only after the video exists. Do not substitute status=ready, a pending card or a private link for playback.

## Notes

Existing production checkout: <repo>; media: <home>/mokaair-work/videos/curio-h09. Draft PR #1503 remains unmerged. Publish review0e344aeb-ccb2-46d3-b695-83063b89c67a and languages reviewe8f86dd8-5f83-4602-ba6f-eaa48d27fbe2 were pending at production closure. All EN/JA/KO audio is owner-accepted; the languages button means actual Studio upload, not listening acceptance. See review/production-completion-20261015.json and backend-delivery-20261015.json. Existing financial authorization is synthesis/QA only; there is no new media work to buy.

2026-10-15 release readback: publish approved at 13:27:46Z; languages approved at 13:27:56Z. All 22 backend attachment entries still match local SHA-256 and byte counts. Initial owner private API request failed at 14:31:36Z with YouTube 500 INTERNAL_ERROR. During read-only investigation, a subsequent request queued at 14:42:07Z completed at 14:42:33Z with video ID -P820NUSWlc; the agent did not press retry or submit a new request. Upload, details, four captions and thumbnail report done. No public schedule is set. The backend explicitly warns this unaudited API upload is locked private. At 14:43-14:44Z the watch page and Studio still showed media processing, so playback was not verified.

Purdue's new October 15 announcement reports unsafe weather paused shore work and an identification update was expected within 48 hours; it does not identify the object. The dated October 14 narration remains accurate, but the existing description's claim that October 14 is the latest announcement must be refreshed before formal release. Source and proposed wording are recorded in production-plan. Refresh again at actual release time.

PR head 2e4456416 failed web-checks and video-tests only because this task contained absolute personal host paths. They were replaced with portable placeholders; no hygiene allowlist or production code was changed. Focused validation and the next pushed SHA are recorded in production-plan.

14:45Z actual Studio language table: EN/JA/KO captions each show one published version and metadata show published, but all three audio cells show a dash. Playback remains unavailable while processing. Receipt: review/youtube-private-upload-readback-20261015.json; screenshot: review/studio-languages-20261015.png. The owner answered call_41f9ad1cd9d04797b4a09e8585f0b640 with "我自行操作 Studio 上傳". Studio upload is therefore an owner action; the agent must not create the second video, add tracks, publish or schedule it. The existing API test video stays intact.

Prepared review/studio-handoff-20261015/STUDIO-HANDOFF.md with exact paths for the approved final, thumbnail, four SRTs and three M4As. Separate four-language description copies replace only the dated update paragraph and add the October 15 primary source. Titles and chapters are unchanged; all four bodies are under 5000 UTF-8 bytes. The original approved upload package is unchanged. The local manifest records nine media hashes and description hashes. Independent wording review preserved the distinction between an expected identification update and an identified object. The source was successfully read earlier this turn; a later repeat fetch failed, so recheck it before public release. Next input is the owner's new Studio URL, followed by actual track/subtitle/player verification. Local repo-hygiene 3/3, check:tasks 1913 and diff checks pass; release this task while waiting for the owner.
