---
id: 2026-10-06-translated-cc-cues-take-their-times
title: Translated CC cues take their times from the narration's measured cue boundaries
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-06T00:48:32Z
completed_at:
branch:
depends_on:
  - 2026-10-01-hand-off-owner-approved-renewed-finals
  - 2026-10-05-long-video-cc-from-aligned-times
scope:
  - tools/video/core/stages.mjs
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
---

# Translated CC cues take their times from the narration's measured cue boundaries

## Why

Since `2026-10-05-long-video-cc-from-aligned-times`, a narration line whose `timeline.json` entry
carries `timing.chars` (an Azure voice timed through `speech/align`) has its narration-locale CC
cues start when their first character is spoken. A translated locale (en, ja, ko, zh-CN, or
zh-TW under an English narration) still shares the line's window by text weight, so its cue
changes do not line up with the narration's. That ticket's last definition-of-done item,
"translated locales keep their own split but inherit the zh-TW cue boundaries' times", could not
be done there: `buildCues(timeline, texts, locale)` gets only that locale's texts, timeline lines
carry no text, and `timing.chars` holds the narration's written units without their spaces or
locale, so the narration's own cut cannot be recomputed exactly. `core/stages.mjs` (the
captions stage) has to pass the narration's texts and locale, and the Codex ticket
`2026-10-01-hand-off-owner-approved-renewed-finals` holds that file.

## Definition of done

- [ ] A translated locale's cues keep their own cut, and each cue boundary takes a time from the
      narration's measured cue boundaries of the same line (the rule for unequal counts is
      written down and tested).
- [ ] A line without timing, a dub-timed locale, and a narration line whose text does not line up
      with its chars keep today's weighted split byte for byte.

## Steps

- [ ] `buildCues(timeline, texts, locale, narration = null)` with `narration = { locale, texts }`:
      for a locale other than `narration.locale`, cut the narration text with its own rules,
      time it with `line.timing.chars` (`timePieces`), and give the translated pieces those
      boundaries. Suggested rule: equal counts take them one for one; fewer translated pieces
      take, in order, the nearest unused narration boundary to each weighted boundary; more
      translated pieces keep weighted shares inside the narration span they fall in.
- [ ] `runCaptions` (`core/stages.mjs`) passes `{ locale: narrationLocale(doc), texts: texts[narration] }`
      for every locale that is not dub-timed.
- [ ] Tests in `core/captions.test.mjs`, including the byte-identical pins added by the parent ticket.

## How to verify

```bash
node --test tools/video/core/captions.test.mjs tools/video/core/stages.test.mjs
```

## Notes

- Filed 2026-10-06 by claude-opus-5-5-cc-aligned from
  `2026-10-05-long-video-cc-from-aligned-times`, whose notes have the details.
