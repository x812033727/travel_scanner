---
id: 2026-10-05-caption-translation-chain-upgrade
title: Caption translation chain: split rules, a glossary, and translate then reflect then refine in one call
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:08:23Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/youtube-video/references/prompts/caption-translate.md
  - .agents/skills/youtube-video/references/prompts/caption-review.md
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
  - tools/video/core/lexicon.mjs
  - tools/video/core/lexicon.test.mjs
  - docs/videos/AUTOMATION.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Caption translation chain: split rules, a glossary, and translate then reflect then refine in one call

## Why

The caption translator (`prompts/caption-translate.md`, `automation/prompts.mjs`) translates
line by line with no glossary and no second look; the reviewer prompt catches some of what a
reflection pass would have fixed. Translate-then-reflect-then-refine with a terminology table
is the chain the strongest open translators use (VideoLingo, Apache-2.0; pyvideotrans, GPL,
idea only). Our en, ja, ko and zh-CN CC and metadata go through this prompt for every video.

## Definition of done

- [ ] The translator answers `{draft, critique, final}` in one call; only `final` is used,
      and an answer without a critique is refused and retried.
- [ ] The prompt carries a glossary built from the lexicon terms the video uses plus its
      `sources` names, and the zh-TW cue boundaries, so the translator sees where cues split.
- [ ] `splitText` prefers clause ends and never splits a number from its unit.
- [ ] `prompts.test.mjs` pins the prompt sections; a fixture shows a glossary term kept the
      same across all four locales.

## Steps

- [ ] Rewrite `caption-translate.md` (three passes, glossary table, cue boundaries) and
      `caption-review.md` (review against the glossary).
- [ ] `automation/prompts.mjs`: build the glossary and the boundaries into the request, parse
      the three-part answer; `prompts.test.mjs`.
- [ ] `core/captions.mjs splitText`: clause-end preference, number+unit tokens; `core/lexicon.mjs`
      exposes the terms a video used.
- [ ] `docs/videos/AUTOMATION.md`: the translator stage.
- [ ] Receipt increment by an independent agent for `automation/prompts.mjs`.

## How to verify

```bash
node --test tools/video/automation/prompts.test.mjs tools/video/core/captions.test.mjs tools/video/core/lexicon.test.mjs
node tools/video/cli.mjs i18n-sheet --slug <video>     # the sheet carries the glossary and the boundaries
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `tools/video/automation/prompts.mjs` → receipt increment. `flow.mjs` is deliberately
  untouched: the three passes are one call.
- `prompts.mjs` is also named by `2026-10-03-illustrated-slides-round-2-a-family`; claim order
  decides who rebases.
- Technique from VideoLingo (Apache-2.0) and pyvideotrans (GPL — idea only); nothing copied.
