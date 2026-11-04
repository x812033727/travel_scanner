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
  - tools/video/tts/concurrency.mjs
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

- [x] check-audio transcribes up to N lines at once (default 4, environment variable to change it, 1 = today's behaviour).
- [x] dub sends up to N synthesis requests at once, with the same knob.
- [x] Results, the cache file, flags file and the speech journal are the same as a sequential run (order-independent):
      every answer is written to the cache as it arrives, a STOP or crash leaves a resumable state, and an answer the
      journal holds is never bought twice.
- [x] A 429 / busy answer drops the run back to one at a time instead of failing more requests; `GIVE_UP_AFTER` still
      stops a run whose service keeps failing.
- [x] Tests cover: same output as N=1, STOP mid-run then resume, 429 fallback, journal not double-charged.

## Steps

- [x] Read how `journal.wrapTranscribe`, `journal.reused` and `journal.release()` work (`openSpeechJournal`) and make
      the per-request bookkeeping safe with requests in flight together.
- [x] Add a small bounded-concurrency helper and use it in check.mjs's transcription loop.
- [x] Do the same for dub synthesis.
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
- 2026-11-04 (implementation, uncommitted on claude/dazzling-wright-pqolfx): `tools/video/tts/concurrency.mjs` holds
  the knob (`VIDEO_SPEECH_CONCURRENCY`, whole number ≥ 1, default 4, anything else a UsageError, exit 2), `sendInOrder`
  (starts jobs in script order, at most `limit()` out, jobs sharing a key never out together, a failure stops
  launching and the jobs out finish before it is thrown), `watchBusy` (tells the caller of a 429 or a
  busy/rate-limit code without changing what the client does with it) and `inRunOrder` (writes cache keys in a
  sequential run's order). What the bookkeeping relies on:
  - each request opens its own `openSpeechJournal` over the shared directory, so `reused` and `release()` are per
    request; a shared journal's `release()` after one line is saved would drop another line's answered-but-unsaved
    entry, and a crash then would buy it again;
  - a job's keys are the request sha256 of every body it may send (check: the transcription body; dub: the scene
    body and every line-alone body for retakes or a failed split), so the same body is never out twice in one run:
    the later job waits until the earlier is saved and released, as one at a time did (otherwise it would find this
    live process's `sent` entry and hold it as SPEECH_UNCERTAIN);
  - a run sends one at a time until a request it bought is saved (proves token, service and disk), so a refused
    token or a lost answer costs one request, not N; existing `check-journal.test.mjs` and the dub STOP test pass
    unchanged at the default because of this.
- The knob is not written into docs/videos/DUBS.md: that file is in the scope of several active tasks. When it is
  free, one line beside the STOP paragraph (§92) would do: 「`VIDEO_SPEECH_CONCURRENCY`（預設 4）是 dub 與 check-audio
  同時送出的請求數；第一個請求單獨送，遇到 429 或忙碌就改回一次一個；1 等於以前的逐一送出。」
- Still to do: the real-episode timing (Steps, last item).
