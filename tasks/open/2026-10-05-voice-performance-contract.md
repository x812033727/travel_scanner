---
id: 2026-10-05-voice-performance-contract
title: Voice performance contract: a performance plan on the voice and delivery cues on any line reach the TTS style
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:27Z
completed_at:
branch:
depends_on:
  - 2026-10-05-caption-translation-chain-upgrade
  - 2026-10-03-illustrated-slides-lint-heuristics-the-shorts
scope:
  - .agents/skills/youtube-video/references/prompts/writer-video.md
  - .agents/skills/youtube-video/references/prompts/writer-story.md
  - .agents/skills/youtube-video/references/prompts/writer-drama.md
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/lint.mjs
  - tools/video/tts/requests.mjs
  - tools/video/tts/tts.test.mjs
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Voice performance contract: a performance plan on the voice and delivery cues on any line reach the TTS style

## Why

Narration is "read naturally": the Gemini style prompt carries the accent and, for dramas,
each line's `emotion`, but nothing tells the voice where to slow down, lift or pause in an
explainer or a brand story. OpenMontage's voice-performance director (AGPL — idea only)
carries a performance plan from script to synthesis and samples the hardest section first;
`emotion` already exists on drama lines (`LINE_KEYS`), so the contract needs no new schema key.

## Definition of done

- [ ] `video.json.voice.performance` (register, pace, where to lift) and `emotion` on any line
      reach the Gemini style through `voiceFor`; Azure voices warn (existing `emotionProblems`).
- [ ] Writer prompts deliver cues on at least a third of lines; `lint` warns below that.
- [ ] Timelines without `emotion` keep their `speech_hash` (regression on the fixtures).
- [ ] `voice-audition.md`: the sample is the most performance-sensitive section, not the first.

## Steps

- [ ] Prompts (`writer-video.md`, `writer-story.md`, `writer-drama.md`, `prompts.mjs`), tests.
- [ ] `core/drama.mjs voiceFor` + `emotion` outside dramas, `timeline.mjs speechHash`,
      `lint.mjs` coverage warning, `tts/requests.mjs`; tests.
- [ ] Receipt increment by an independent agent (six bound files).

## How to verify

```bash
node --test tools/video/automation/prompts.test.mjs tools/video/core/drama.test.mjs tools/video/tts/tts.test.mjs tools/video/core/lint.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `automation/prompts.mjs`, `core/drama.mjs`, `core/drama.test.mjs`, `core/lint.mjs`,
  `core/timeline.mjs`, `tts/tts.test.mjs` — which is why this is P3 and last.
