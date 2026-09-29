---
id: 2026-09-27-ai-shorts-owner-review-studio-launch
title: AI Shorts: owner review, Studio launch and 90-day measurement
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-27T18:47:02Z
completed_at:
branch:
depends_on:
  - 2026-09-27-ai-shorts-pilot
scope:
  - docs/videos/ai-shorts/releases
---

# AI Shorts: owner review, Studio launch and 90-day measurement

## Why

The local Shorts implementation provides three evidence-bound pilots and fifteen detailed briefs. Real audience performance and the 90-day goal require owner-reviewed publication and actual YouTube Studio exports. Local rendering does not establish public release, audience retention, or ten million views.

## Definition of done

- [ ] Owner listens to all three pilots and checks typography/captions on a phone; approve the local Hanhan voice or provide approved replacement narration.
- [ ] Export the existing channel's last 90 days of Shorts analytics, or record that no historical Shorts exist. Preserve raw files outside Git.
- [ ] Owner privately uploads the pilots in Studio, verifies playback/CC/cover and disclosure/audience settings, and explicitly chooses public release times.
- [ ] Record actual video IDs and public timestamps; initialize tracking from the first public date, not the illustrative calendar date.
- [ ] Capture actual 24h/72h/7d snapshots, costs and status changes. Review five mature samples per series before applying the editorial rules.
- [ ] Run weekly topic selection and budget review for 90 days; report the real outcome and missing observations without inventing retrospective snapshots.

## Steps

- [ ] Read docs/videos/ai-shorts/README.md and the delivery receipt; inspect the local artifact paths and manifests.
- [ ] Complete owner review and channel baseline before expanding production.
- [ ] Keep releases/ receipts for reviewed, uploaded and published states separately; private metrics/media remain outside Git.
- [ ] Produce subsequent topics from the campaign briefs and weekly evidence. Preserve existing original experiment outputs.

## How to verify

Use YouTube Studio Analytics → Advanced mode → Shorts → Export, preserving export time, filters and units. Run `node tools/video/shorts/cli.mjs track-init --dir <outside-repo-empty-dir> --start <actual-first-public-date>` and `report --dir <same-dir>`. Verify public playback and captions only after owner-authorized publication. An empty report must stay `no_metrics`; incomplete raw rows go to staging, never zero-fill.

## Notes

- Scope is release receipts; new scripts/tool changes need their own task and scope check.
- This ticket is not authorization to publish, buy subscriptions, alter production settings, or change the YouTube API quota.
- Targets: 120 slots over 90 days (30/45/45); 10,000,000 cumulative public views is a stretch goal. First three pilots <= NT$300; each 30-day period <= NT$3,000, soft stop at NT$2,400; total <= NT$9,000.
- Existing tests used the same session model in two fresh contexts, one bundled response each. They do not establish a model-brand ranking or general accuracy.
