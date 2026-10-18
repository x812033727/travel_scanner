---
id: 2026-10-07-preschool-video-backend-profile
title: Support preschool English productions in the backend video pipeline
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T19:07:44Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/schema.mjs
  - tools/video/core/stages.mjs
  - tools/video/render/cli.mjs
  - tools/video/dubs/plan.mjs
---

# Support preschool English productions in the backend video pipeline

## Why

The requested preschool course uses 3–5 minute episodes, embedded English text, shared English demonstration takes, and zh-TW/zh-CN/ja/ko teaching tracks and CC. The first five offline pilots are complete, but the existing backend production route cannot represent this contract without violating its long-form rules.

## Definition of done

- [ ] An explicit preschool profile accepts short lessons without weakening the existing long-form duration floor.
- [ ] English remains embedded in the picture while selectable CC contains only the four requested languages.
- [ ] All language tracks reuse the same English demonstration takes and localize only teaching instructions.

## Steps

- [ ] Add profile-aware duration, embedded-text and CC policies.
- [ ] Support zh-TW teaching audio for an English source and shared demonstration takes across dubs.
- [ ] Exercise the configured backend voice and preview flow after the tool is paired; extend the task scope if backend/UI changes are required.

## How to verify

Use docs/videos/english-preschool-pilot/lessons.json and localizations.json as the five-episode acceptance corpus. Verify durations, no English CC stream, exact English take reuse, fixed English text, and language selection. Keep existing long-form tests passing.

## Notes

- Offline deliverables exist in /workspace/preschool-pilot-output and use explicitly labeled Edge read-aloud trial voices, not the configured production voice.
- Confirmed gaps: schema.mjs has an 8-minute floor; stages.mjs always includes source CC and drops zh-TW from language choices; render/cli.mjs burns subtitles only for drama; dubs/plan.mjs replaces whole lines rather than reusing English demonstrations.
- No backend setting change, deployment, public upload or tool pairing has been performed. This ticket records future production adoption and does not block viewing the completed five pilots.
