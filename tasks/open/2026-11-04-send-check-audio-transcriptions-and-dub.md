---
id: 2026-11-04-send-check-audio-transcriptions-and-dub
title: Send check-audio transcriptions and dub syntheses concurrently
status: in-progress
priority: P1
area: tools
owner: claude-opus-tech-signal
claimed_at: 2026-11-04T15:06:08Z
created_at: 2026-11-04T12:30:00Z
completed_at:
branch: claude/dazzling-wright-pqolfx
depends_on: []
scope:
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Send check-audio transcriptions and dub syntheses concurrently

## Why

The daily Tech Signal podcast (`daily-ai-` slugs, `.agents/skills/youtube-video/references/daily-brief.md`) ships eight
dubs, and every dub is listen-checked. On `daily-ai-20261104` (no quota errors, no restarts) the eight dubs took about
4.3 hours (~30 min each) and the first listen-check round about 5.5 hours (30–40 min each), 75% of a 13-hour day.

Both are strictly sequential:
- `tools/video/tts/check.mjs`: the loop `for (const { scene, line } of lines)` awaits one `transcribe(...)` per line.
- `tools/video/dubs/cli.mjs` (`dubLocale`): synthesis requests are sent one after another.

About 250 lines × 8 locales ≈ 2,000 requests a day, one at a time; the project lease also serialises dub and check-audio.
The owner approved (2026-11-04) sending several at once to cut this to about 3 hours.

## Definition of done

- [ ] check-audio transcribes up to N lines at once (default 4, environment variable to change it, 1 = today's behaviour).
- [ ] dub sends up to N synthesis requests at once, with the same knob.
- [ ] Results, the cache file, flags file and the speech journal are the same as a sequential run (order-independent):
      every answer is written to the cache as it arrives, a STOP or crash leaves a resumable state, and an answer the
      journal holds is never bought twice.
- [ ] A 429 / busy answer drops the run back to one at a time instead of failing more requests; `GIVE_UP_AFTER` still
      stops a run whose service keeps failing.
- [ ] Tests cover: same output as N=1, STOP mid-run then resume, 429 fallback, journal not double-charged.

## Steps

- [ ] Read how `journal.wrapTranscribe`, `journal.reused` and `journal.release()` work (`openSpeechJournal`) and make
      the per-request bookkeeping safe with requests in flight together.
- [ ] Add a small bounded-concurrency helper and use it in check.mjs's transcription loop.
- [ ] Do the same for dub synthesis.
- [ ] Try N=4 on one locale of the next Tech Signal episode; record time and any 429s here.

## How to verify

`npm run test:tools`; then on a real episode compare one locale's `check-audio --locale` and `dub --locale` wall time at N=1 and N=4.

## Notes

- 2026-11-04: claiming this was refused because three older tasks still list these files in their scope:
  `2026-10-13-dub-narrator-only-explainer-dramas-tool` (review, claimed 10-13),
  `2026-10-16-bind-story-audits-and-narration-to` (in-progress, claimed 10-17),
  `2026-10-19-worker-video-languages-five` (review, claimed 10-20). Check whether they are stale before claiming.
- 2026-11-04: the owner approved claiming over those three stale overlaps (「准許強制認領」). This task changes only how
  requests are sent in check.mjs and dubs/cli.mjs, on branch claude/dazzling-wright-pqolfx; it touches none of their branches.
