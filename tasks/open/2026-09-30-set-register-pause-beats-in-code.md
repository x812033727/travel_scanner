---
id: 2026-09-30-set-register-pause-beats-in-code
title: Set register pause beats in code instead of asking the model
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-30T09:40:10Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
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

- [ ] A `setPauseBeats(doc)` in `register.mjs` sets the three beats from the text for
  illustrated slides, and the flow calls it before `saveAndLint`.
- [ ] The register rules and the references say the tool sets the beats.
- [ ] Tests cover each beat and a document with none.

## Steps

- [ ] Write `setPauseBeats` next to `registerSummary`, reusing its helpers.
- [ ] Call it in `flow.mjs` after the writer and listener save.
- [ ] Update the rule text in the four places.

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```

## Notes

Found by the 2026-09-30 prompt audit (medium confidence, Group 4). Check the scope against
`2026-09-28-sothatswhy-shorts-from-episode` and `2026-09-30-video-worker-moves-two-videos-at`
before claiming; both list `flow.mjs`.
