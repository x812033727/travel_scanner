---
id: 2026-09-30-check-audio-let-the-second-opinion
title: check-audio: let the second-opinion timeout and model be set per machine
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-30T10:01:50Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/second-opinion.mjs
  - tools/video/tts/second-opinion.test.mjs
  - .agents/skills/youtube-video/references/automated.md
  - .claude/skills/youtube-video/references/automated.md
---

# check-audio: let the second-opinion timeout and model be set per machine

## Why

`tools/video/tts/second-opinion.mjs` gives the whole batch of doubted clips a fixed 30-minute `timeout` (`TIMEOUT_MS`). On the owner's Windows ARM64 machine the local faster-whisper `medium` model takes about a minute per clip, and much longer when two checks run at once. On 2026-09-30 every `check-audio` run with more than about 15 doubted clips printed "the second transcriber failed" and kept all its flags, so dubs that were fine looked broken. Switching to `WHISPER_MODEL=small` and running one check at a time fixed it, but nothing in the tool or the skill says so.

## Definition of done

- [ ] The second-opinion timeout can be set per machine (for example `VIDEO_SECOND_OPINION_TIMEOUT_MS`), and the default scales with the number of clips instead of being fixed at 30 minutes.
- [ ] When the second opinion times out, the message says it timed out and how many clips it had, not just "failed".
- [ ] `automated.md` (both skill copies) says: run one `check-audio` at a time, and use `WHISPER_MODEL=small` on slow machines.

## Steps

- [ ] Read the timeout from the environment in `second-opinion.mjs`, with a per-clip default.
- [ ] Distinguish a timeout from other failures in the error text.
- [ ] Test both in `second-opinion.test.mjs`.
- [ ] Update the skill reference; `npm run test:tools` keeps the two copies in step.

## How to verify

`node --test tools/video/tts/second-opinion.test.mjs`; on a slow machine, a `check-audio --locale ja` run with 30 doubted clips finishes its second opinion instead of reporting a failure.

## Notes

- 2026-09-30 (claude-fable-5-1): also on this machine, faster-whisper 1.2.1 with PyAV 19 needs `metadata_errors="ignore"` removed from `faster_whisper/audio.py`, and the script needs `PYTHONUTF8=1` to print CJK text on Windows. Those are local setup facts, not repository changes.
