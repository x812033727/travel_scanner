---
id: 2026-10-21-paper-slide-look-key-band-icons
title: Paper slide look: key band, icons, numeral card, human terminal typing
status: in-progress
priority: P1
area: tools
owner: claude-fable
claimed_at: 2026-10-21T13:48:38Z
created_at: 2026-10-21T13:46:37Z
completed_at:
branch: claude/paper-slide-look
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/templates/icons.mjs
  - tools/video/templates/fixtures/paper
  - tools/video/templates/terminal/terminal.mjs
  - tools/video/templates/terminal/terminal-human.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/render/browser.mjs
  - tools/video/render/browser.test.mjs
  - tools/video/render/cli.mjs
  - tools/video/render/repeat.mjs
  - tools/video/render/render.test.mjs
  - tools/video/screencast/scene.mjs
  - tools/video/screencast/steps.mjs
  - tools/video/qa/pace.mjs
  - tools/video/qa/pace.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/schema.test.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/timeline.test.mjs
  - docs/videos/PAPER.md
  - docs/videos/README.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
  - .agents/skills/youtube-video/references/visuals.md
  - .agents/skills/youtube-video/references/automated.md
---

# Paper slide look: key band, icons, numeral card, human terminal typing

## Why

The owner judged the two slides tutorials of #1643 "weak on screen": every card is dark text on a
dark ground, nothing moves inside a state, and the terminal card types its command in 0.6 s, which
reads as a cut. The reference channel's slides are cream paper with ink text and one red accent, a
big numeral beside a word, a simple line icon per idea, one key sentence under every card, and
commands typed at a human pace. The approved plan (2026-10-21, 教學片改版) splits the renderer
work into four pieces that must not move any existing video's frame keys: the keys hash
theme.css, so all new CSS is inlined per page and attached only when a card uses the field.

## Definition of done

- [ ] `theme: "paper"`, `data.keys`/`data.key`, `big.numeral`, `icon` on big/bullets/steps/compare and
      `terminal.typing: "human"` render as docs/videos/PAPER.md describes; a video without them is
      byte for byte what it was (templates.test.mjs holds the showcase heads to it).
- [ ] render refuses a human-typed state its narration cannot carry; qa repeats it on the measured timeline.
- [ ] `theme` passes the schema and moves visualHash only when set; docs and the review receipt follow.

## Steps

- [x] PR 1 (no receipt-bound file): icons.mjs, numeral, key band, stateCount, human typing,
      maxFrames, PAPER_CSS/themeCss, the paper fixture, visuals.md, PAPER.md, tests.
- [ ] PR 2 (receipt-bound files, stacked on PR 1): schema.mjs TOP_KEYS, timeline.mjs visualHash,
      qa/pace.mjs terminalHoldProblems + qa/cli.mjs, docs/videos/README.md, automated.md; an
      independent reviewer rebinds docs/videos/long-form/review.json.

## How to verify

`node --test tools/video/templates/templates.test.mjs tools/video/templates/terminal/terminal-human.test.mjs tools/video/render/render.test.mjs tools/video/render/browser.test.mjs`,
`npm run test:tools`, and
`node tools/video/render/repeat.mjs --file tools/video/templates/fixtures/paper/video.json --channel msedge --runs 2 --out <dir>`
(the fixture runs two minutes, so `render` stops at the eight-minute floor; repeat.mjs draws without
lint): open run-1/'s stills and the terminal states' transition frames.

## Notes

- Claimed with --force on 2026-10-21: the overlapping claims (duration-review, curio-thumb,
  story-thumb-brand, eight/five languages) were stale claims on the receipt files, not live work on these.
- Plan deviations: `terminalSeconds(scene, stateIndex)` takes the scene, not its data, because the
  reveals that decide which output part a state prints live on the lines; `stateReveals` lives in
  terminal.mjs (templates.mjs imports it) so both count states the same way without an import cycle.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
