---
id: 2026-10-01-worker-translates-zh-tw-for-an
title: Worker translates zh-TW for an English-narrated video and the final review sends its zh-TW title
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-zh-tw-translation
claimed_at: 2026-10-01T10:41:13Z
created_at: 2026-10-01T03:50:41Z
completed_at:
branch: claude/worker-zh-tw-for-english-narration
depends_on:
  - 2026-09-29-language-choice-assumes-zh-tw-narration
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - docs/videos/LANGUAGES.md
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

- [x] The worker, on an `en`-narrated video with a decided choice, translates zh-TW (metadata and
      captions) before it runs `captions` and `package`, and only once (the sheet comes back done).
- [x] The final review payload of such a video carries `en` and `zh-TW` titles and descriptions.
- [x] zh-TW videos behave exactly as before.

## Steps

- [x] `pendingLanguages` (or `languages()`): add zh-TW with `metadata,captions` when
      `narrationLocale(doc) !== "zh-TW"`; `translateLocale` already returns null on a done sheet.
      Done in `languages()` through a new `channelLocale()`, not in `pendingLanguages` (see Notes).
- [x] `sync.mjs` final gate: `metadataLocalesOf(languages, narrationLocale(doc))` instead of
      `chosenLocales(languages, "metadata")`.
- [x] Tests with `enFixture` (`tools/video/core/fixtures/load.mjs`).

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
- Claimed with `--force` by claude-opus-5-5-zh-tw-translation: the overlap was with stale claims
  whose PRs are merged (`2026-09-28-drama-listener-stale-check` from #978,
  `2026-09-28-sothatswhy-shorts-from-episode`, `2026-09-30-video-worker-moves-two-videos-at`
  from #999).
- Why not in `pendingLanguages`: the site never reports zh-TW (the panel does not offer it), so a
  zh-TW entry there would read as "working" forever and the worker would re-run `captions`,
  `package` and `review-push --gate languages` every round. Instead `channelLocale(project,
  workdir)` says zh-TW is owed while its translation is not current (`sheetDone(buildSheet(...))`
  in-process, no `i18n-sheet` run) or while an upload package written before it lacks
  `description.zh-TW.txt` / `captions/zh-TW.srt`. `languages()` translates it first, then the
  chosen locales; the batch still names only the chosen locales.
- The choice with nothing ticked ("only the channel language") is the likely one for an English
  season, and `package` already ran before the choice with English alone: then the worker
  translates zh-TW, then runs `captions` and `package` once with no languages batch (sending one
  would be refused: `languagesSubmission` throws on an empty choice).
- zh-TW videos: `languages()` reads `video.json` for the narration and returns where it did before,
  without `loadProject`; the Traditional-Chinese-only test now also asserts no command runs.
- Tidied videos (`tidiedLanguages`) are unchanged: their files are gone, nothing is made.
- Added `docs/videos/LANGUAGES.md` to the scope for one paragraph in §工人. The skill reference
  (`automated.md`, mirrored under `.claude/skills/`) is left as is.
- Filed `2026-10-01-translator-and-caption-reviewer-prompts-name`: the translator and caption
  reviewer prompts still describe the source as zh-TW.
- Verified: the three new tests fail with the source change reverted and pass with it;
  `node --test tools/video/automation/automation.test.mjs tools/video/review/sync.test.mjs` 105/105.
