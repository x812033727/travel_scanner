---
id: 2026-09-29-language-choice-assumes-zh-tw-narration
title: Language choice assumes zh-TW narration: a video with narration_locale loses its own captions and description
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-09-29T03:24:56Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/stages.mjs
  - tools/video/package/check.mjs
  - tools/video/package/cli.mjs
  - tools/video/qa/cli.mjs
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

- [ ] With a `languages.json` in the work directory, a video narrated in `en` gets its `en`
      captions and description from `captions`, `qa` and `package`, whatever the choice says.
- [ ] Such a video can have zh-TW captions and a zh-TW title and description: either always,
      as zh-TW narration always gets them, or through a choice the site can express. Decide
      which one with the owner or the video-languages task owner.
- [ ] zh-TW videos behave byte for byte as before (the existing tests pass unchanged).

## Steps

- [ ] Give `captionLocalesOf` and `packageLocalesWanted` the narration locale (package/check.mjs
      can read it from `metadata.json`'s `default_language`) and pass it from every caller.
- [ ] Use `defaultDubLocales(doc)` in `package/cli.mjs`.
- [ ] Decide the zh-TW question and implement it in `readLanguages` / `composeMetadata`.
- [ ] Tests: an `en`-narrated fixture with a `languages.json` choosing only `ja` captions.

## How to verify

`node --test "tools/video/**/*.test.mjs"`, plus the English fixture
(`tools/video/core/fixtures/load.mjs`'s `enFixture`) taken through captions → qa → package
with a `languages.json` written by `writeLanguages`.

## Notes

- Scope overlaps `2026-09-26-video-dubs-worker` (claude-fable-5-1-video-languages, review) on
  `tools/video/core/stages.mjs`. Wait until that one is done, or coordinate on it.
