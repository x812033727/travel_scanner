---
id: 2026-10-07-the-final-gate-s-owner-exit-names
title: The final gate's owner exit names the video tool token even when Jev's key is not set
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T11:30:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# The final gate's owner exit names the video tool token even when Jev's key is not set

## Why

`tools/video/review/sync.mjs` `qualityCheck` turns `qa`'s exit 3 into "the quality check needs the
owner (the video tool token); see above". Until `2026-10-07-jev-s-unconfigured-503-is-held-as`,
every owner answer that reached the policy item was about the token. Since then, Jev's unset key
(503 `provider_unavailable`) is the owner's too. So the parenthetical points at the token when the
fix is to set Jev's key in the site's settings.

Nothing behaves differently: the worker defers and then blocks on exit 3 as it did on exit 4, and
`review/qa.json` and the printed policy line carry the real detail ("尚未設定 Jev API 金鑰").

## Definition of done

- [ ] The owner exit names what to fix, or names nothing and points at the policy line.

## Steps

- [ ] Word the message generically, for example "the quality check needs the owner (the video
  tool token or a site setting); see the policy line in review/qa.json", or carry the policy
  item's detail into it.
- [ ] Adjust the test in `review/sync.test.mjs` that pins the wording, if any.

## How to verify

`node --test tools/video/review/sync.test.mjs`. `sync.mjs` and `sync.test.mjs` are bound by the
duration receipt, so the change needs an independent re-bind (`node tools/video/long-form/cli.mjs
check`). Ride along with the next change to `sync.mjs` rather than spending a re-bind on it alone.

## Notes

- Found by the review of `2026-10-07-jev-s-unconfigured-503-is-held-as` (2026-10-07), as a nit.
