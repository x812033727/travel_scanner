---
id: 2026-10-05-voice-performance-contract
title: Voice performance contract: a performance plan on the voice and delivery cues on any line reach the TTS style
status: done
priority: P3
area: tools
owner: claude-fable-5-1-voice
claimed_at: 2026-10-05T18:26:44Z
created_at: 2026-10-05T16:08:27Z
completed_at: 2026-10-05T18:42:34Z
branch: claude/voice-performance
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

- [x] `video.json.voice.performance` (register, pace, where to lift) and `emotion` on any line
      reach the Gemini style through `voiceFor`; Azure voices warn (existing `emotionProblems`).
- [x] Writer prompts deliver cues on at least a third of lines; `lint` warns below that.
- [x] Timelines without `emotion` keep their `speech_hash` (regression on the fixtures).
- [ ] `voice-audition.md`: the sample is the most performance-sensitive section, not the first.
      (Not done: the file is not in this ticket's scope; see Notes.)

## Steps

- [x] Prompts (`writer-video.md`, `writer-story.md`, `writer-drama.md`, `prompts.mjs`), tests.
- [x] `core/drama.mjs voiceFor` + `emotion` outside dramas, `timeline.mjs speechHash`,
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
- 2026-10-05, claude-fable-5-1-voice, branch `claude/voice-performance` (starts from
  `claude/caption-translation-chain`, PR #1301, whose `prompts.mjs` edits this sits beside; not
  rebased, main is merged in by the coordinator when #1301 lands):
  - **Claimed with `--force` over the open dependency**
    `2026-10-03-illustrated-slides-lint-heuristics-the-shorts`: every code item of that ticket
    landed in #1172 (`SHOT_SIZE`, `LOOK_WORDS`, `motifOf`, `choiceFor`, the two 56% mentions);
    its one open step is its own receipt rebind, which shares no code path with this work and
    is not a precondition.
  - **`voice.performance` lives in `core/drama.mjs`** (`validatePerformance`, `PERFORMANCE_MAX`
    200): a non-empty string, and with `voice.style` inside the server's 400-character style
    (`style + "。" + plan`), on the document's voice alone; a character's voice keeps its own
    style and refuses the field as an unknown one. `schema.mjs`'s `VOICE_KEYS` does not list the
    key and the file is outside this scope (and receipt-bound), so `validatePerformance` takes
    back the one unknown-field error `validateVoice` pushed for the path `voice.performance`
    and checks the field itself; `validateVideo` runs the two in that order on one `errors`
    array. The cleaner form is one word in `VOICE_KEYS`; whoever next touches `schema.mjs` can
    move it there and drop the take-back. The 200 leaves the channel's register style (about
    110 characters) and an 80-character cue room inside 400.
  - **`voiceFor`** composes `voice.style`。plan。`emotion`。pronunciation readings (order kept:
    the plan is the general direction, the cue the line's), slices at 400 as before, strips
    `performance` from the voice it returns (so `voiceFields` never sends it and the clip key
    is the style it produced), and applies the plan to the narrator's lines only. A doc without
    a plan or a cue gets the same voice object as before, so every pinned clip key in
    `tts.test.mjs` holds.
  - **`emotion` on any format's line**: the drama-only list in `validateDrama` is now
    `speaker`, `audio_ref`; the 80-character check runs for every format. `speechHash` adds
    `["emotion", …]` to a slides line's fields only when the line has one, so a timeline from
    before this change stays current: `drama.test.mjs` pins the six fixtures' hashes
    (`af5d5f5eb75aaa69`, `24b8bd53672b91e8`, `3701f1baabd22734`, `9fea1c4d8c68e0dc`,
    `1a23e4d697759dd1`, `01f2da6b69601188`, recorded on the start branch before the change).
  - **Lint** (`cueCoverageProblems` in `drama.mjs`, wired in `lint.mjs` beside
    `emotionProblems`, which now runs for every format and also warns about a plan on an Azure
    voice): a script is in the contract once it carries a plan or any cue; then the lines a cue
    can reach (Gemini voices; in a drama with a cast the characters' lines, since the narrator
    bridges) must carry one on at least `CUE_SHARE_MIN` (1/3) or lint warns
    `N of M lines carry a performance cue`. Gated on purpose: an unconditional warning would
    fire on every existing video and on the illustrated, explainer and story fixtures, whose
    suites (`lint.test.mjs`, `explainer.test.mjs`, `story.test.mjs`, outside this scope) pin an
    empty warning list; the gate keeps them byte-stable and the worker's fix loop reads errors
    only anyway. The drama example's three character lines all carry a cue, so it stays clean.
  - **Prompts**: the slides writer (`INSTRUCTIONS.writer`), the drama `SHOT_GUIDE` lines bullet
    and the explainer's lines bullet ask for the plan and the cues with one shared phrase,
    `at least a third of the lines carry one (lint warns below that)`, which `prompts.test.mjs`
    pins in the three worker texts and in `writer-video.md`, `writer-drama.md`,
    `writer-story.md` (and in the drama phrase cross-check). The brand story's worker text
    (`automation/story-prompts.mjs`) is outside the scope, so only `writer-story.md` says it,
    and says so.
  - **Gaps, not fixed here** (outside the scope): (1) the worker route's `settle()`
    (`automation/flow.mjs`) replaces the writer's `voice` with the settings tab's, so a plan the
    worker's writer returns is dropped there (the cues on the lines survive); keeping
    `video.voice.performance` in `settle()` is a one-line follow-up, and the settings tab's
    `VoiceSettings` has no such field. The local skill route writes `video.json` directly and
    keeps it. (2) `dubs/plan.mjs` `dubVoice` spreads `doc.voice`, so a plan rides into every
    dub's locale style (cues already did for dramas); drop it there with `rate` and `lang` or
    keep it on purpose. (3) `voice-audition.md` (DoD item 4) is not in the scope. (4)
    `docs/videos/DRAMA.md` §句子 and `references/drama.md` still describe `emotion` as a
    drama field; `ILLUSTRATED.md` §聲音表演 is the current description.
  - Verified: `node --test tools/video/automation/prompts.test.mjs tools/video/core/drama.test.mjs
    tools/video/core/lint.test.mjs tools/video/core/timeline.test.mjs tools/video/tts/tts.test.mjs
    tools/video/core/explainer.test.mjs tools/video/core/story.test.mjs` (143 pass),
    `npm run test:tools` (only `review.test.mjs` red: the receipt, which #1301's files already
    leave stale and this ticket's bound files add to), `npm run check:tasks`. The receipt
    increment is the independent reviewer's: bound files changed by this branch are
    `tools/video/automation/prompts.mjs`, `tools/video/core/drama.mjs`,
    `tools/video/core/drama.test.mjs`, `tools/video/core/lint.mjs`, `tools/video/core/timeline.mjs`,
    `tools/video/tts/tts.test.mjs`.
