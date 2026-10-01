---
id: 2026-09-30-set-register-pause-beats-in-code
title: Set register pause beats in code instead of asking the model
status: done
priority: P3
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-01T03:17:30Z
created_at: 2026-09-30T09:40:10Z
completed_at: 2026-10-01T03:28:42Z
branch: claude/register-pause-beats
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/register.test.mjs
  - tools/video/automation/prompts.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/youtube-video/references/prompts/listener-register.md
  - .agents/skills/youtube-video/references/prompts/writer-video.md
---

# Set register pause beats in code instead of asking the model

## Why

The storytelling register asks the model to set `pause_after_ms` beats: the hook after the
cold open's first sentence, the reveal on the sentence before 「其實」, the cliffhanger on a
chapter's closing question (`tools/video/automation/register.mjs` REGISTER_RULES, repeated in
LISTENER_REGISTER, `script-writing.md`, `listener-register.md`, `writer-video.md`). All three
positions follow from the text, and `registerSummary` already detects the same things with
`QUESTION` and the chapter split. The model is placing values the code can compute.

## Definition of done

- [x] A `setPauseBeats(doc)` in `register.mjs` sets the three beats from the text for
  illustrated slides, and the flow calls it before `saveAndLint`.
- [x] The register rules and the references say the tool sets the beats.
- [x] Tests cover each beat and a document with none.

## Steps

- [x] Write `setPauseBeats` next to `registerSummary`, reusing its helpers.
- [x] Call it in `flow.mjs` after the writer and listener save.
- [x] Update the rule text in the four places.

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```

## Notes

Found by the 2026-09-30 prompt audit (medium confidence, Group 4). Check the scope against
`2026-09-28-sothatswhy-shorts-from-episode` and `2026-09-30-video-worker-moves-two-videos-at`
before claiming; both list `flow.mjs`.

### 2026-10-01 (claude-opus-5-5)

- Claimed with `--force`: the scope overlapped `2026-09-28-sothatswhy-shorts-from-episode`
  (claimed 2026-09-28, its PRs #904/#950/#962 merged), `2026-09-30-video-worker-moves-two-videos-at`
  (claimed 2026-09-30 01:13Z, PR #999 merged) and `2026-09-28-drama-listener-stale-check` (review,
  PR #978 merged); all three claims were over 24 hours old and no open PR from them touches these
  files. Open PR #1054 touches `flow.mjs` near line 1800 and #1062 touches `prompts.mjs` (the
  compilation planner); this change stays away from both. Added `register.test.mjs` and
  `prompts.test.mjs` to the scope: the tests that pin the rule text live there.
- Design: `setPauseBeats` owns the field. It clears every `pause_after_ms` on the script first,
  a model's included, then sets the three beats, so a value from an older prompt or a model that
  ignored the rule does not survive a save and a second run changes nothing. A line on two beats
  keeps the longer pause. "Sentence" is a line (one `lines[]` is one sentence), the reveal reaches
  back across scenes, the spoken form (`say`) decides, and the last chapter's question gets no
  cliffhanger (it answers the opening question; the same closers `registerSummary` counts).
- Where: `Automation.settled()` calls it for a video whose prompts carry REGISTER_RULES
  (`usesRegister`: not a drama, not a brand story, no variant), so every `saveAndLint` save
  (writer, lint fix, verifier, listener) gets the beats before lint, and `checkedIsSaved` compares
  the same settled script. That is every slides video on the default prompts, a superset of
  illustrated ones; a plain slides video reads the same rules, so it gets the same beats.
- `restyle` ignores a `pause_after_ms` in the answer (it used to accept or refuse it) and sets the
  beats from the retold text before lint. A restyle that accepts no line writes nothing, so an
  older script keeps its model-set pauses until it is next saved.
- `registerSummary` still only counts beats; nothing reports a missing beat as a problem, and the
  tool now sets every beat the text allows, so there is nothing to report.
- Not changed (outside the scope): `docs/videos/ILLUSTRATED.md` §說書式旁白 still lists the beats as
  part of the register without saying the tool sets them.
