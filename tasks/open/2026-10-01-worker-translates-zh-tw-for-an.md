---
id: 2026-10-01-worker-translates-zh-tw-for-an
title: Worker translates zh-TW for an English-narrated video and the final review sends its zh-TW title
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-01T03:50:41Z
completed_at:
branch:
depends_on:
  - 2026-09-29-language-choice-assumes-zh-tw-narration
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# Worker translates zh-TW for an English-narrated video and the final review sends its zh-TW title

## Why

Since `2026-09-29-language-choice-assumes-zh-tw-narration`, a video narrated in another locale
(`narration_locale`, e.g. `en`) always gets zh-TW captions, title and description, whatever the
owner's language choice says: `alwaysLocales(narration)` in `tools/video/core/stages.mjs` is
`[narration, "zh-TW"]`, and `captions`, `qa` and `package` ask for both. The site's panel never
offers zh-TW, so `languages.json` never lists it.

Two readers outside that ticket's scope still only look at the chosen locales:

- `tools/video/automation/flow.mjs` `languages()` / `pendingLanguages()` translates only the
  locales in the choice. For an English-narrated video the worker never writes `i18n/zh-TW.json`,
  so `qa` fails its captions and metadata items and `package` stops with "zh-TW: the title and
  description are not translated yet". A hand run (`i18n-sheet` without `--locale` translates
  every target, zh-TW included) is fine.
- `tools/video/review/sync.mjs` builds the final gate's `payload.metadata` with
  `chosenLocales(languages, "metadata")`, so the review card leaves out zh-TW for such a video
  (and `languagesSubmission` reports only chosen locales, which is right: zh-TW is not a choice).

No video in docs/videos sets `narration_locale` yet and the worker's prompts write zh-TW scripts,
so nothing is broken today.

## Definition of done

- [ ] The worker, on an `en`-narrated video with a decided choice, translates zh-TW (metadata and
      captions) before it runs `captions` and `package`, and only once (the sheet comes back done).
- [ ] The final review payload of such a video carries `en` and `zh-TW` titles and descriptions.
- [ ] zh-TW videos behave exactly as before.

## Steps

- [ ] `pendingLanguages` (or `languages()`): add zh-TW with `metadata,captions` when
      `narrationLocale(doc) !== "zh-TW"`; `translateLocale` already returns null on a done sheet.
- [ ] `sync.mjs` final gate: `metadataLocalesOf(languages, narrationLocale(doc))` instead of
      `chosenLocales(languages, "metadata")`.
- [ ] Tests with `enFixture` (`tools/video/core/fixtures/load.mjs`).

## How to verify

`node --test tools/video/automation/automation.test.mjs tools/video/review/sync.test.mjs`, then
`npm run test:tools`.

## Notes

- Filed by claude-opus-5-5-language-choice while finishing
  `2026-09-29-language-choice-assumes-zh-tw-narration`; the helpers to reuse are
  `alwaysLocales`, `captionLocalesOf`, `metadataLocalesOf` and `dubLocalesOf` in
  `tools/video/core/stages.mjs`.
- `docs/videos/LANGUAGES.md` and the `narration_locale` paragraph of
  `.agents/skills/youtube-video/references/automated.md` could say the same in one sentence
  ("an English-narrated video always gets zh-TW captions and title too") when this lands.
