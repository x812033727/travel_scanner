---
id: 2026-10-01-translator-and-caption-reviewer-prompts-name
title: Translator and caption reviewer prompts name the narration locale as the source
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-translator-source
claimed_at: 2026-10-01T15:01:58Z
created_at: 2026-10-01T10:49:31Z
completed_at:
branch: claude/translator-source-locale
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

- [x] A translator or caption reviewer call for a video narrated in another locale says what the
      source language is, and zh-TW as a target gets its own register rule.
- [x] Prompts for zh-TW-narrated videos are unchanged byte for byte (a test shows it).

## Steps

- [x] Pass the narration locale in the payload (`translateLocale`, `shortenDub`, `rewordDub` in
      `flow.mjs`), or pick an instruction variant, and word the rules around "the source line".
- [x] Add a zh-TW target rule beside en / ja / ko / zh-CN.
- [x] Tests: the en fixture (`tools/video/core/fixtures/load.mjs` `enFixture`, used by
      `finishedVideo({ script: enFixture() })` in `automation.test.mjs`).

## How to verify

`node --test tools/video/automation/automation.test.mjs`, then `npm run test:tools`.

## Notes

- Filed by claude-opus-5-5-zh-tw-translation while finishing
  `2026-10-01-worker-translates-zh-tw-for-an`, which was scoped to the worker's language step and
  the final-review payload, not the prompts.
- Claimed with `--force` by claude-opus-5-5-translator-source: the claim was refused only for
  stale claims on `automation.test.mjs` / `flow.mjs` whose PRs are merged
  (`2026-09-28-drama-listener-stale-check` from PR #978, `2026-09-28-sothatswhy-shorts-from-episode`
  from PRs #904/#950/#962, `2026-09-30-video-worker-moves-two-videos-at` from PR #999).
- Decision: no new variant. The payload carries `source_locale` (only when the video is not
  zh-TW-narrated, so a zh-TW payload gains no field), and `stage()` in `flow.mjs` hands the same
  value to `instructionsFor(..., source)`, so the instructions can never name a different source
  than the payload shows. The variant stays `null` / `shorten` / `reword`, so the site's run
  records (`translator/shorten`) and its prompt-as-sent rows keep their keys; the row for
  `translator` simply shows whichever source was sent last.
- `prompts.mjs` `SOURCE_INSTRUCTIONS[source]` (en, ja, ko, zh-CN) is built from the zh-TW texts
  with `swap()`: a source-language opening instead of COMMON's first paragraph (COMMON's rules
  kept), "from <language>, the narration language" in the translator's first line, "the source
  line" for "the zh-TW line", `the <language> "source"` in shorten/reword, line lengths "ja, ko,
  zh-CN and zh-TW about 40" (zh-CN "about as long as the source" only fits a Chinese source), and a
  zh-TW register (Taiwanese wording in Traditional characters, the zh-TW interface's names,
  軟體/影片/設定 never 軟件/視頻/設置) in the translator's, reviewer's, shorten's and reword's
  register lists. A rule changed in a zh-TW text follows automatically; `swap()` throws at import
  when a phrase it replaces disappears, so the tests catch a drift.
- zh-TW unchanged, shown two ways in `automation.test.mjs`: SHA-256 of the four texts
  (translator, caption_reviewer, translator:shorten, translator:reword) captured from origin/main
  before the change and pinned, checked for source undefined / null / zh-TW / an unknown locale in
  both formats; and an end-to-end zh-TW video whose translator, reviewer, shorten and reword calls
  carry those exact bytes and no `source_locale`. The en fixture's video (zh-TW + ja with a dub
  that over-runs once and is misheard) shows all six calls with `source_locale: "en"` and the
  English texts; that test fails on the old `flow.mjs`.
