---
id: 2026-09-28-check-audio-gemini-transcriber-rewrites-unfamiliar
title: check-audio: Gemini transcriber rewrites unfamiliar model versions and years
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-29T02:58:51Z
created_at: 2026-09-28T06:03:30Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts
---

# check-audio: Gemini transcriber rewrites unfamiliar model versions and years

## Why

`check-audio` transcribes every narration clip with Gemini and sends the lines whose transcript
differs to Jev. On the zh-TW pricing video (`gpt6-vs-opus55-worth-paying`, 2026-09-28) three
lines stayed flagged through three takes and two rewordings of `say`:

- `qx54` Gemini 3.8 Flash came back as 「Gemini 一點五 Flash」 every time.
- `ypij` 2026 came back as 二零二三, then 兩千零二十四.
- `xiua` Grok 四點七 came back as 「Grok 視覺」.

A local Whisper (faster-whisper `medium`, int8, CPU) heard all three clips correctly
("Gemini 3.8 Flash", "Grok 4.7", "2026年9月28日"), and it heard the neighbouring lines the same
way. So the audio was right and the transcriber was pulling the text toward model names and
years it already knows. Each extra round cost quota and left the audio gate showing flags that
are not real, with nothing in the tool to say a second opinion cleared them.

## Definition of done

- [ ] A flagged line can be cleared by a second, independent transcript that matches the
      script, and the audio gate shows that it was cleared and by what.
- [ ] Or: the transcription request carries the script's expected product names and numbers as
      context, and the pricing video's three lines pass without a `say` change.

## Steps

- [ ] Decide between a second-opinion transcript (Whisper on the owner's machine or the worker)
      and a context-primed Gemini request; measure both on the three clips above.
- [ ] Record the outcome in `review/check.json` so `review-push --gate audio` can show it.

## How to verify

```bash
node tools/video/cli.mjs check-audio --slug gpt6-vs-opus55-worth-paying --workdir <VIDEO_WORKDIR>
```

## Notes

- Whisper setup used for the cross-check: `python3 -m venv asr && asr/bin/pip install faster-whisper`,
  then `WhisperModel("medium", device="cpu", compute_type="int8")` with `language="zh"`; about a
  minute for five clips on four cores.
- 命令列 kept coming back as 命令行 on `openai-agents-broke-in` (`td49`); that one may be the voice
  and was fixed with `say` 終端機版.
- The transcription is billed against the site's monthly Gemini characters: checking six dub tracks
  on 2026-09-28 took the month from 21,622 to 8,106 left (the retakes in between were about 400).
  That makes a second-opinion transcript that runs locally worth more than a better prompt.
- On the same day it also wrote Gemini 1.5 Flash's real old prices into a Japanese line that said
  something else entirely (qx54), so a transcript that differs in numbers is not proof the voice
  said them.
