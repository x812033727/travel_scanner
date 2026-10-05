---
id: 2026-10-04-avoid-claiming-owner-youtube-upload-when
title: Avoid claiming owner YouTube upload when pulling automatic publish approval
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-04T17:29:40Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# Avoid claiming owner YouTube upload when pulling automatic publish approval

## Why

`recordApproval` returns “the owner confirmed the upload” for every newly pulled publish approval, including automatic package approval. During the LLM episode's normal publish-pull, the backend automatically approved the complete package while `youtube_video_id` remained null. The command therefore reported an owner upload that had not happened. Package approval and actual YouTube upload must remain distinct.

## Definition of done

- [ ] Pulling a current automatic publish approval reports package approval without asserting owner upload or YouTube publication.
- [ ] Existing approval persistence and hash checks remain intact; already-recorded and other gate messages are covered by focused fixtures.

## Steps

- [ ] Check active scopes and the existing review message tests before claiming this fix.
- [ ] Replace the inaccurate publish message and add a fixture with an approved package and no YouTube ID.

## How to verify

Run the focused `tools/video/review/sync.test.mjs` tests. Assert that a newly pulled publish approval records the actual metadata hash while its text makes no claim of owner upload or publication. Do not perform a real YouTube upload for this verification.

## Notes

- Observed 2026-10-04T17:24Z through unchanged normal publish-pull for `ai-term-large-language-model`. Publish review `cbf8689a-a38a-48fc-bce8-51e15188980d` was automatically approved at 17:18:41.446916Z with QA4/4; all five backend package attachments matched local SHA-256 and size, but the actual YouTube ID was null.
- The message is emitted at `tools/video/review/sync.mjs:1026`, after ordinary hash-bound approval recording. The producer preserved the raw stdout and explicitly classified it as a legacy label. No shared-code fix, owner approval, upload or publication was performed in the production ticket.
