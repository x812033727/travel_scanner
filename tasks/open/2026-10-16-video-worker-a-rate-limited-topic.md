---
id: 2026-10-16-video-worker-a-rate-limited-topic
title: Video worker: a rate-limited topic lookup must defer the scheduled draft, not retry it every round
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-16T00:17:00Z
completed_at:
branch: claude/video-topics-rate-limit
depends_on: []
scope:
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - apps/api/app/video_automation/admin_api.py
  - apps/api/tests/test_video_automation_topics.py
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Video worker: a rate-limited topic lookup must defer the scheduled draft, not retry it every round

## Why

The production video worker wrote no scheduled draft from 2026-10-13 00:56Z (`last_draft_at` in
`auto-state.json`) to at least 2026-10-16. Every round (`VIDEO_WORKER_INTERVAL_SECONDS=300`, about
5.6 minutes with the round itself) printed `請求過於頻繁，請稍後再試` and `auto exited with 4`.

Read-only on the host, 2026-10-16 00:00–00:15Z:

- The only route answering 429 was `GET /api/v1/video/automation/topics` (20 of 20 since the
  23:52Z deploy); every other worker route answered 200.
- Its limiter `rate:video_topics:<token>` held 32 hits in a window of `TOPIC_LOOKUPS_PER_HOUR = 12`;
  the window's TTL was fine (it expires hourly).
- `Automation.draft()` asks the topics first and marks the draft (`markDrafted`) only after the
  planner: a 429 ended the round unmarked, so the next round asked again.
- `client.mjs` tries a 429 four times (sleeps 5, 10, 20 s, Retry-After capped at 120 s), each try
  counted by the window: 4–5 hits a round, about 40 an hour, so a fresh window was spent within
  minutes and never let a draft through.
- `rea-reverse-engineering-100k-stars-what-it-means` (a re-plan, which also reads the topics) was
  deferred 32 times by the same limit.

## Definition of done

- [x] A refused topic lookup says when its window opens (`Retry-After`).
- [x] The client does not try again a 429 whose Retry-After is longer than its longest sleep.
- [x] A scheduled draft that meets a passing refusal (topics or planner) waits until the
      Retry-After, or 30 minutes, in `auto-state.json` `draft_waits_until`; the round goes on.
- [x] Duration receipt rebound by an independent reviewer (DURATION_ONLY).
- [ ] Deployed; on the host the worker's rounds no longer exit 4 on the topics and a scheduled
      draft is written once the window opens.

## How to verify

```bash
node --test tools/video/automation/client.test.mjs
node --test --test-name-pattern="scheduled draft" tools/video/automation/automation.test.mjs
cd apps/api && uv run pytest tests/test_video_automation_topics.py -q
node tools/video/long-form/cli.mjs check
```

On the host after the deploy: `docker logs --since 1h travel_scanner-video-worker-1` shows
`the scheduled draft waits until …` at most once a window, and `auto-state.json` gets a new
`last_draft_at`.

## Notes

- Claimed with `--force`: the four active claims on these files (`2026-10-14-enforce-usd-25-all-in-cap`,
  `2026-10-14-support-10-minute-minimax-cute-brand`, `2026-10-14-curio-episodes-keep-the-series-look`,
  `2026-10-14-correct-a21-pringles-patent-fact-and`) belong to branches already merged
  (#1508, #1499, #1500) and were not closed; nobody is changing these files now.
- Not changed: the limit itself (12 an hour) and the limiter's counting of refused hits. With
  one lookup a round and the draft waiting out the window, 12 is enough.
- The owner asked for this on 2026-10-16 after the post-deploy check of #1516 showed the worker
  exiting 4 every round.


### 2026-10-17 owner-authorized claim release

Implementation in #1520 is merged. The owner authorized releasing this obsolete claim for independent A01 lexicon integration. This ticket remains open only pending archival; do not reimplement the merged work. No production action is authorized by this metadata change.
