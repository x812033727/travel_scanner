---
id: 2026-09-29-language-choice-assumes-zh-tw-narration
title: Language choice assumes zh-TW narration: a video with narration_locale loses its own captions and description
status: done
priority: P3
area: tools
owner: claude-opus-5-5-language-choice
claimed_at: 2026-10-01T03:38:02Z
created_at: 2026-09-29T03:24:56Z
completed_at: 2026-10-01T03:52:07Z
branch: claude/language-choice-narration-locale
depends_on: []
scope:
  - tools/video/core/stages.mjs
  - tools/video/package/check.mjs
  - tools/video/package/cli.mjs
  - tools/video/qa/cli.mjs
  - tools/video/core/narration-locale.test.mjs
  - tasks/open/2026-10-01-worker-translates-zh-tw-for-an.md
---

# Language choice assumes zh-TW narration: a video with narration_locale loses its own captions and description

## Why

A video can now be narrated in a locale other than zh-TW (`narration_locale` in video.json,
`narrationLocale(doc)` in `tools/video/core/schema.mjs`). The owner's per-video language choice
(`languages.json`, docs/videos/LANGUAGES.md, #870) was written when every video was narrated in
zh-TW, and several readers of it still assume that:

- `captionLocalesOf(languages)` in `tools/video/core/stages.mjs` returns `[zh-TW, ...chosen]`.
  `runCaptions` adds the narration locale itself (merge of main into
  claude/ai-video-planning-l43qas, 2026-09-29). But `package/cli.mjs`, `qa/cli.mjs` and
  `package/check.mjs`'s `packageLocalesWanted` do not. An English-narrated video with a choice
  that does not tick English captions would ship without its own captions, and would be asked
  for zh-TW ones.
- `packageLocalesWanted` builds `descriptionLocales` as `[NARRATION_LOCALE, ...metadata]`, so it
  asks for a zh-TW description instead of the narration's.
- `readLanguages` drops any zh-TW entry. Since the site's panel never offers zh-TW, a video
  narrated in English cannot choose zh-TW captions or a zh-TW title and description.
- `package/cli.mjs` falls back to `DEFAULT_DUB_LOCALES` (the zh-TW narration's) rather than
  `defaultDubLocales(doc)`.

No video in docs/videos sets `narration_locale` yet (main's six "English-first" videos in #891
are narrated in zh-TW), so nothing is broken today. The first English-narrated video that goes
through the site worker will hit it.

## Definition of done

- [x] With a `languages.json` in the work directory, a video narrated in `en` gets its `en`
      captions and description from `captions`, `qa` and `package`, whatever the choice says.
- [x] Such a video can have zh-TW captions and a zh-TW title and description: either always,
      as zh-TW narration always gets them, or through a choice the site can express. Decide
      which one with the owner or the video-languages task owner. (Decided: always; see Notes.)
- [x] zh-TW videos behave byte for byte as before (the existing tests pass unchanged).

## Steps

- [x] Give `captionLocalesOf` and `packageLocalesWanted` the narration locale (package/check.mjs
      can read it from `metadata.json`'s `default_language`) and pass it from every caller.
- [x] Use `defaultDubLocales(doc)` in `package/cli.mjs`.
- [x] Decide the zh-TW question and implement it in `readLanguages` / `composeMetadata`.
- [x] Tests: an `en`-narrated fixture with a `languages.json` choosing only `ja` captions.

## How to verify

`node --test "tools/video/**/*.test.mjs"`, plus the English fixture
(`tools/video/core/fixtures/load.mjs`'s `enFixture`) taken through captions → qa → package
with a `languages.json` written by `writeLanguages`.

## Notes

- Scope overlaps `2026-09-26-video-dubs-worker` (claude-fable-5-1-video-languages, review) on
  `tools/video/core/stages.mjs`. Wait until that one is done, or coordinate on it. (It is in
  `tasks/done/` now.)
- 2026-10-01, claude-opus-5-5-language-choice. **Decision: zh-TW is always made**, the way a
  zh-TW narration always is. The owner and the video-languages owner could not be asked from this
  session, so this is the choice that needs no site change and can be reversed in one helper:
  the site's panel and `PUT /admin/videos/{slug}/languages` only take en, ja, ko and zh-CN, so
  "through a choice" would have needed API and web changes first; and zh-TW is
  the channel's own language, so an English video without a zh-TW title would hide from most of
  its viewers. If the owner wants zh-TW optional instead, change `alwaysLocales` in
  `tools/video/core/stages.mjs` to `[narration]` and let the panel offer zh-TW.
- What changed: `stages.mjs` has `alwaysLocales(narration)` (`[narration, "zh-TW"]`, one entry for
  zh-TW), and `captionLocalesOf(languages, narration)`, `metadataLocalesOf(languages, narration)`
  and `dubLocalesOf(languages, doc)` built on it; `runCaptions`, `qa`, `package` and
  `packageLocalesWanted` use them. `packageLocalesWanted(workdir, metadata)` reads the narration
  from `upload/metadata.json`'s `default_language`, and `readPackageReport` now reads metadata.json
  before it. `captionsCurrent` takes the narration (its zh-TW literal meant the narration).
  `readLanguages` is unchanged: it still drops a zh-TW entry, which is now redundant rather than
  lost. A ticked narration locale (the panel offers English to an English video) is folded into
  the narration and is never dubbed.
- zh-TW videos: every helper returns what the old code did (`[zh-TW, ...chosen]` captions,
  `composeMetadata` drops the narration from its `locales`, `defaultDubLocales(doc)` equals
  `DEFAULT_DUB_LOCALES`); the existing stages, qa, package, metadata and sync tests pass unchanged.
- Verified: `tools/video/core/narration-locale.test.mjs` takes the English fixture, translated
  into every locale, through `runCaptions` → `qa` → `package` with a `languages.json` ticking only
  ja captions: captions en, zh-TW, ja; descriptions en, zh-TW; package check passes. Both new tests
  fail without the source change.
- Left for `2026-10-01-worker-translates-zh-tw-for-an`: the site worker (`automation/flow.mjs`)
  only translates chosen locales, so for an English video it would never write `i18n/zh-TW.json`
  and `qa`/`package` would now ask for it; and `review/sync.mjs`'s final gate payload still lists
  only chosen metadata locales. Hand runs translate every target already.
