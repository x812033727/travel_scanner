---
id: 2026-10-06-translated-cc-cues-take-their-times
title: Translated CC cues take their times from the narration's measured cue boundaries
status: done
priority: P3
area: tools
owner: claude-cc-translated
claimed_at: 2026-10-07T02:10:49Z
created_at: 2026-10-06T00:48:32Z
completed_at: 2026-10-07T02:21:48Z
branch: claude/happy-carson-c1hy91
depends_on:
  - 2026-10-01-hand-off-owner-approved-renewed-finals
  - 2026-10-05-long-video-cc-from-aligned-times
scope:
  - tools/video/core/stages.mjs
  - tools/video/core/captions.mjs
  - tools/video/core/captions.test.mjs
  - tools/video/review/renewal.mjs
  - tools/video/review/renewal-handoff.mjs
  - tools/video/review/renewal.test.mjs
  - docs/videos/DESIGN.md
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

- [x] A translated locale's cues keep their own cut, and each cue boundary takes a time from the
      narration's measured cue boundaries of the same line (the rule for unequal counts is
      written down and tested).
- [x] A line without timing, a dub-timed locale, and a narration line whose text does not line up
      with its chars keep today's weighted split byte for byte.

## Steps

- [x] `buildCues(timeline, texts, locale, narration = null)` with `narration = { locale, texts }`:
      for a locale other than `narration.locale`, cut the narration text with its own rules,
      time it with `line.timing.chars` (`timePieces`), and give the translated pieces those
      boundaries. Suggested rule: equal counts take them one for one; fewer translated pieces
      take, in order, the nearest unused narration boundary to each weighted boundary; more
      translated pieces keep weighted shares inside the narration span they fall in.
- [x] `runCaptions` (`core/stages.mjs`) passes `{ locale: narrationLocale(doc), texts: texts[narration] }`
      for every locale that is not dub-timed.
- [x] Tests in `core/captions.test.mjs`, including the byte-identical pins added by the parent ticket.

## How to verify

```bash
node --test tools/video/core/captions.test.mjs tools/video/core/stages.test.mjs
```

## Notes

- Filed 2026-10-06 by claude-cc-aligned from
  `2026-10-05-long-video-cc-from-aligned-times`, whose notes have the details.

## 2026-10-07 implementation (claude-cc-translated)

- Claimed with `--force`: its dependency `2026-10-01-hand-off-owner-approved-renewed-finals` was
  listed only because that Codex ticket held `core/stages.mjs`; its claim was released in the
  2026-10-07 board sweep (#1357) and only production work is left on it.
- `buildCues(timeline, texts, locale, narration = null)`, `narration = { locale, texts }`. For a
  translated locale on a line with `timing.chars`, the narration's text is cut with its own rules
  and timed (`narrationBoundaries`); when its pieces line up with the characters, the
  translation's weighted cues move onto the narration's cue changes (`inheritBoundaries`).
- The rule as built: the cut, the first start and the last end stay. Equal counts take the
  narration's changes one for one. Fewer translated changes each take, in order, the nearest
  narration change not yet taken (leaving room for the rest). More translated changes pin each
  narration change to the nearest translated one, in order, and the others keep their weighted
  shares of the span between the pins around them (a linear map of the weighted times).
- Guard: the line keeps its weighted times when the move would leave a cue shorter than
  MIN_CUE_MS, or reading faster than the locale's maxCps, where its weighted time was not. A dense
  English translation under a long pause hits the reading-speed guard (tested), which is the
  intended trade: readable before aligned.
- The translation's first cue still starts at the window start, not at the narration's first
  measured character (tens of milliseconds); only the changes between cues move.
- `runCaptions` passes `{ locale: narrationLocale(doc), texts: texts[narration] }` unless the
  locale is dub-timed (its own track's timeline, `narration` null).
- Unchanged byte for byte: an untimed line, a dub-timed locale, a narration text the characters
  were not measured on, a line the narration has no text for (tests compare SRT output); the
  existing pins in `captions.test.mjs` still pass untouched.
- Tests: three in `captions.test.mjs` (the rules, the guards, end to end through `buildCues`) and
  one in `stages.test.mjs` that fails when `runCaptions` drops the narration (checked by
  reverting the stage line).
- `stages.test.mjs` is bound by the duration receipt (`docs/videos/long-form/review.json`), so an
  independent reviewer rebinds it in a separate commit.
- 2026-10-08 (claude-happy-carson), found by the review of #1361 rebased onto main: the renewal
  checks rebuilt the translated captions they expect with `buildCues(...)` and no narration, so
  once `runCaptions` moved a translation's cue changes onto the narration's, a renewed final
  narrated through the aligned route refused its own captions ("en caption bytes have stale
  offsets or text", exit 2, every run). `core/stages.mjs` now exports `localeCues`, which
  `runCaptions`, `review/renewal.mjs` (`bindRenewalSubmission`, the narration's and each
  translation's) and `review/renewal-handoff.mjs` (`bindManualLanguageSubmission`) all use. A
  renewal test with a measured narration line binds the bytes `runCaptions` writes and refuses the
  weighted ones; it fails with the renewal check's old formula. The manual-import check has no
  language-submission test of its own: it shares the helper. `docs/videos/DESIGN.md` no longer
  says translations cannot follow the narration's measured changes.
