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

`tools/video/tts/second-opinion.mjs` runs the second transcriber (`check-audio --second-opinion`, usually `whisper_second_opinion.py`) once for every clip Jev doubts, with a fixed `TIMEOUT_MS` of 30 minutes and no way to change it. On the owner's Windows ARM64 laptop faster-whisper `medium` takes about a minute a clip on the CPU, more when another transcription runs at the same time, so any check with more than about 15 doubted clips ends with 「the second transcriber failed (Command failed …)」 and every flag stands as if Whisper had heard nothing. On 2026-09-30 this happened to the Google Vids narration (22 clips), the price war narration (33), the Siri ja dub (16), the AI agents ko dub (18) and the free-vs-paid ja dub (32); the same runs pass with `WHISPER_MODEL=small` or when the batch is smaller. The failure message does not say it was a timeout, so it looks like a broken install.

## Definition of done

- [ ] The second-opinion timeout can be raised per machine (an environment variable such as `VIDEO_SECOND_OPINION_TIMEOUT_MS`, or a `--second-opinion-timeout` flag), and a timeout is reported as a timeout, with the clip count and the limit.
- [ ] Clips go to the transcriber in batches (for example 8 at a time) so one slow batch cannot lose the whole run, or the transcripts already produced are kept when the run is cut off.
- [ ] `automated.md` (both copies) says which model and timeout to use on a CPU-only machine, and that only one `check-audio` should run at a time.

## Steps

- [ ] Read the env or flag in `second-opinion.mjs`; keep 30 minutes as the default.
- [ ] Batch the clip list, or parse partial stdout on timeout.
- [ ] Tests in `second-opinion.test.mjs` for the env override and the timeout message.
- [ ] Doc lines in the skill reference.

## How to verify

```bash
node --test tools/video/tts/second-opinion.test.mjs
VIDEO_SECOND_OPINION_TIMEOUT_MS=1 node tools/video/cli.mjs check-audio --slug <slug> --second-opinion "<program>"   # reports a timeout, not a bare command failure
```

## Notes

- Filed by claude-fable-5-1 on 2026-09-30 while producing the million-views batch; the workaround used that day was `WHISPER_MODEL=small` and running the checks one after another.
