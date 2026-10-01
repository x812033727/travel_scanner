---
id: 2026-10-01-translator-and-caption-reviewer-prompts-name
title: Translator and caption reviewer prompts name the narration locale as the source
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-01T10:49:31Z
completed_at:
branch:
depends_on:
  - 2026-10-01-worker-translates-zh-tw-for-an
scope:
  - tools/video/automation/prompts.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Translator and caption reviewer prompts name the narration locale as the source

## Why

Since `2026-10-01-worker-translates-zh-tw-for-an`, the worker translates an English-narrated
video (`narration_locale: "en"`) into zh-TW, and into the locales the owner ticks, with the
`translator` and `caption_reviewer` stages. Their instructions in
`tools/video/automation/prompts.mjs` still describe every video as a zh-TW one: `COMMON` opens
with "ONE zh-TW (Traditional Chinese, Taiwan) YouTube video ... told by a synthesized Taiwanese
Mandarin narrator", the translator's dub rule says "in the time the zh-TW line takes", and the
reviewer is told to fix "meaning that differs from the zh-TW line" as a viewer "who also reads
Traditional Chinese". The register list has no rule for zh-TW as a target (Taiwanese wording,
Traditional characters, the zh-TW interface names). The worksheet's `source` is English for such
a video, so the model gets told one thing and shown another. The shorten and reword variants
(`TRANSLATOR_SHORTEN`, `TRANSLATOR_REWORD`) say "the zh-TW source" too.

Nothing is wrong today for zh-TW videos, and no video in docs/videos sets `narration_locale` yet.

## Definition of done

- [ ] A translator or caption reviewer call for a video narrated in another locale says what the
      source language is, and zh-TW as a target gets its own register rule.
- [ ] Prompts for zh-TW-narrated videos are unchanged byte for byte (a test shows it).

## Steps

- [ ] Pass the narration locale in the payload (`translateLocale`, `shortenDub`, `rewordDub` in
      `flow.mjs`), or pick an instruction variant, and word the rules around "the source line".
- [ ] Add a zh-TW target rule beside en / ja / ko / zh-CN.
- [ ] Tests: the en fixture (`tools/video/core/fixtures/load.mjs` `enFixture`, used by
      `finishedVideo({ script: enFixture() })` in `automation.test.mjs`).

## How to verify

`node --test tools/video/automation/automation.test.mjs`, then `npm run test:tools`.

## Notes

- Filed by claude-opus-5-5-zh-tw-translation while finishing
  `2026-10-01-worker-translates-zh-tw-for-an`, which was scoped to the worker's language step and
  the final-review payload, not the prompts.
