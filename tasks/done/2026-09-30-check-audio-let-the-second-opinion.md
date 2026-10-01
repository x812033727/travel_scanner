---
id: 2026-09-30-check-audio-let-the-second-opinion
title: check-audio: let the second-opinion timeout and model be set per machine
status: done
priority: P3
area: tools
owner: claude-opus-5-5-second-opinion
claimed_at: 2026-10-01T03:38:09Z
created_at: 2026-09-30T10:01:50Z
completed_at: 2026-10-01T03:43:23Z
branch: claude/second-opinion-timeout
depends_on: []
scope:
  - tools/video/tts/second-opinion.mjs
  - tools/video/tts/second-opinion.test.mjs
  - .agents/skills/youtube-video/references/automated.md
---

# check-audio: let the second-opinion timeout and model be set per machine

## Why

`tools/video/tts/second-opinion.mjs` gives the whole batch of doubted clips a fixed 30-minute `timeout` (`TIMEOUT_MS`). On the owner's Windows ARM64 machine the local faster-whisper `medium` model takes about a minute per clip, and much longer when two checks run at once. On 2026-09-30 every `check-audio` run with more than about 15 doubted clips printed "the second transcriber failed" and kept all its flags, so dubs that were fine looked broken. Switching to `WHISPER_MODEL=small` and running one check at a time fixed it, but nothing in the tool or the skill says so.

## Definition of done

- [x] The second-opinion timeout can be set per machine (for example `VIDEO_SECOND_OPINION_TIMEOUT_MS`), and the default scales with the number of clips instead of being fixed at 30 minutes.
- [x] When the second opinion times out, the message says it timed out and how many clips it had, not just "failed".
- [x] `automated.md` (both skill copies) says: run one `check-audio` at a time, and use `WHISPER_MODEL=small` on slow machines.

## Steps

- [x] Read the timeout from the environment in `second-opinion.mjs`, with a per-clip default.
- [x] Distinguish a timeout from other failures in the error text.
- [x] Test both in `second-opinion.test.mjs`.
- [x] Update the skill reference; `npm run test:tools` keeps the two copies in step.

## How to verify

`node --test tools/video/tts/second-opinion.test.mjs`; on a slow machine, a `check-audio --locale ja` run with 30 doubted clips finishes its second opinion instead of reporting a failure.

## Notes

- 2026-09-30 (claude-fable-5-1): also on this machine, faster-whisper 1.2.1 with PyAV 19 needs `metadata_errors="ignore"` removed from `faster_whisper/audio.py`, and the script needs `PYTHONUTF8=1` to print CJK text on Windows. Those are local setup facts, not repository changes.
- 2026-10-01 (claude-opus-5-5-second-opinion): claimed with `--force`; the only refusal was the stale claim of `2026-09-30-video-worker-moves-two-videos-at`, whose PR #999 is merged.
- The default limit is now 10 minutes plus 2 minutes per clip for the whole batch (`TIMEOUT_BASE_MS`, `TIMEOUT_PER_CLIP_MS`): 30 clips get 70 minutes, about twice what Whisper `medium` needs on the slow ARM64 machine. `VIDEO_SECOND_OPINION_TIMEOUT_MS` replaces the whole limit; a value that is not a positive whole number fails the second opinion with a message naming the variable instead of being silently ignored.
- A timeout is told apart by execFile's `killed` flag, excluding the maxBuffer kill (`ERR_CHILD_PROCESS_STDIO_MAXBUFFER`). `check.mjs` (out of scope, unchanged) prints the error's first line inside "the second transcriber failed (…)", so the line now reads "the second transcriber failed (timed out after 70 min on 30 clips; set VIDEO_SECOND_OPINION_TIMEOUT_MS or a smaller WHISPER_MODEL, and run one check-audio at a time)". A test runs a real `node` child with a 300 ms limit to prove the `killed` detection works with the real execFile on Windows.
- There is only one copy of `automated.md`: `.claude/skills/youtube-video/` holds only `SKILL.md`, so the `.claude/.../references/automated.md` path was removed from the scope. The new sentences sit in the 收斂旁白 paragraph, away from the STOP paragraph that PR #1056 edits.
- Not verified here: a real 30-clip `check-audio --locale ja` run on the slow machine.
