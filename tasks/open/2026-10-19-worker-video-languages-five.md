---
id: 2026-10-19-worker-video-languages-five
title: Video worker makes es, pt, id, vi, th captions, titles and dubs
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-worker-dubs-five
claimed_at: 2026-10-20T05:30:03Z
created_at: 2026-10-19T23:53:40Z
completed_at:
branch: claude/worker-video-dubs-five
depends_on: []
scope:
  - tools/video/core/schema.mjs
  - tools/video/core/stages.mjs
  - tools/video/core/narration-locale.test.mjs
  - tools/video/dubs
  - tools/video/tts
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
  - apps/api/app/video_speech
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_youtube/requests.py
  - apps/api/tests/test_video_languages_worker.py
  - apps/api/tests/test_video_languages_imported.py
  - apps/api/tests/test_video_youtube.py
  - apps/api/tests/test_migration_0136_video_languages_eight.py
  - apps/api/tests/test_video_speech_check.py
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
  - docs/videos/LANGUAGES.md
  - docs/videos/DUBS.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Video worker makes es, pt, id, vi, th captions, titles and dubs

## Why

On 2026-10-09 the owner fixed a video's languages at four: zh-TW narration plus en, ja and ko
(`docs/videos/LANGUAGES.md`). On 2026-10-18/19 they had 種田娶妻打天下 made in five more:
Latin-American Spanish (YouTube `es-419`), Brazilian Portuguese (`pt-BR`), Indonesian,
Vietnamese and Thai. Those files were made outside the pipeline and attached with
`tools/video/cli.mjs import --languages` (#1593, live 292cdda11). So today only an imported
video's language panel lists the five. Every pipeline video still lists en, ja and ko, and the
API refuses the five there (422 `video_locales_imported_only`), because the host worker cannot
make them: a ticked cell would stay "working" forever. The owner then asked why other videos
cannot choose them. This task is the plan for letting the worker make them, with its costs.

**Do not start the build before the owner has answered.** Extending the languages reverses the
2026-10-09 decision. It also more than doubles the translation and TTS work of a video that ticks
all of them. The owner's answer goes under Notes.

## What limits the worker to en, ja, ko today

Every place below has to learn the five. Otherwise the cell never leaves "working", or a check
refuses the locale. Line numbers are on origin/main 1e60f734e.

| Where | What it holds | What the five need |
| --- | --- | --- |
| `tools/video/core/schema.mjs:23` `LOCALES` | zh-TW, en, ja, ko. It is both the narration languages **and** the translation targets: `i18n/cli.mjs` `targetLocales`, `dubs/plan.mjs` `dubLocales`, `tts/check.mjs` `DUB_LOCALES`, and flow, package, render, qa and shorts all import it | Split it in two. `NARRATION_LOCALES` stays the four (narration, `prompts.mjs` `SOURCE_NAMES`, the listener texts). `TARGET_LOCALES` is the four plus es, pt, id, vi, th |
| `tools/video/automation/prompts.mjs:427` translator, `:1424`, `:1710`, `:1734` shorten/reword | Line lengths and register for en/ja/ko only (en plain, ja です／ます, ko 합니다체) | A register per locale: es-419 neutral *tú* (no *vosotros*, no voseo), pt-BR *você*, id conversational Jakarta Indonesian, vi *bạn*, th with the female narrator's ค่ะ/นะคะ used sparingly (the channel voice Sulafat is female). Line length about 80 characters for the Latin four and about 40 for th |
| `tools/video/core/captions.mjs:19` `LOCALE_RULES` | Cue width, lines and reading speed for zh-TW/en/ja/ko | es/pt/id/vi: 42 characters × 2 lines, 17 cps, word breaks. **th has no spaces between words**: it needs `Intl.Segmenter("th", {granularity: "word"})` to find break points. Its width must not count combining vowels and tone marks (U+0E31, U+0E34–0E3A, U+0E47–0E4E). Start at 35 × 2, 15 cps |
| `tools/video/core/metadata.mjs:22` `LABELS`, `:33` `CAPTION_TAGS` | Description section labels and the title's caption word for the four | Labels in the five. Caption words as the API already has them (`video_youtube/requests.py:58`: ｜CC, ｜Legendado, ｜Sub Indo, ｜Vietsub, ｜ซับไทย), and the `TAG_TAIL` pattern that strips them |
| `tools/video/core/compilation.mjs:61` | Episode label per locale (第n話, n화) | Episodio n, Episódio n, Episode n, Tập n, ตอนที่ n |
| `tools/video/render/fonts.mjs:33` `LOCALE_FONTS` | Thumbnail fonts of their own for ja and ko | th needs `@fontsource-variable/noto-sans-thai`, a new dependency. es/pt/id/vi are covered by Noto Sans TC's latin and vietnamese subsets. Render refuses an uncovered character, so a gap shows up |
| `tools/video/dubs/plan.mjs:54` `RATE_RATIOS`, `:56` `DEFAULT_RATES`, `:67` `DUB_STYLES` | Starting speaking rates and the voice's language clause for en/ja/ko | Rates from the table below. Styles from the 種田娶妻 glossary leads (`dub-glossary.json` `lead`: Mexican-standard Latin-American Spanish, São Paulo Portuguese, Jakarta Indonesian, Hanoi Vietnamese, Bangkok Thai), with the explainer manner in place of the voice-actor wording |
| `tools/video/tts/check.mjs:68` `DUB_LOCALES` and `comparable()` | Which dubs check-audio hears; transcripts are compared after NFKC | Follows `TARGET_LOCALES`. vi transcripts may place tone marks differently (hoà/hòa), so compare after a vi-specific fold, or Jev gets lines that are the same word |
| `apps/api/app/video_speech/checking.py:45` transcription prompts, `:77` `SOUND_ALIKE_SCRIPT`, `schemas.py:136` `TrackLanguage` | The server transcribes a track only in zh-TW/en/ja/ko; any other language raises `no transcription prompt` | A prompt per locale: Thai script, Vietnamese with its diacritics, English terms in Latin letters |
| `tools/video/tts/whisper_second_opinion.py:28` `LANGUAGES` | The faster-whisper second opinion's languages | es, pt, id, vi, th (Whisper large-v3 has all five) |
| Translation script check | None in the pipeline, so a th sheet answered in English would merge | Port `SCRIPT` from `docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub-lines.mjs:29` into `i18n-merge`. The Latin locales may carry no CJK, Hangul or Thai; th must carry Thai and no CJK or Hangul |
| `apps/api/app/video_reviews/schemas.py:56` `WorkerLocale`, `:63` `ImportedLocale`; `admin_service.py:2084` | The five are imported-only; the dub retry endpoint takes `WorkerLocale` | Move the five into `WorkerLocale` for the categories the owner picks, and keep the 422 for the rest |
| `apps/api/app/video_automation/schemas.py:32` `CaptionLocale`, `models.py:66` `DEFAULT_CAPTION_LOCALES`, `max_length=3` at `:171` and `:209` | The settings tab's pre-ticks (`caption_locales`, `drama_caption_locales`) | A Literal of eight and `max_length=8`. The defaults stay en, ja, ko unless the owner says otherwise. No migration: the columns are json lists |
| `apps/web/components/admin-video-settings.tsx:27` `CAPTION_LOCALES`, `apps/web/messages/*/admin.json` | The settings tab's checkboxes | Eight rows (the language names exist since #1593) |
| `apps/api/app/video_shorts/schemas.py:51` `ShortsLocale`/`SHORTS_LOCALES`, `tools/video/shorts/package.mjs:22` `EXTRA_LOCALES`, `apps/web/components/admin-video-shorts-data.ts:12` | Shorts add en/ja/ko only | Only if the owner wants Shorts in the five |
| `services/youtube-uploader/src/contract.mjs:8` `LANGUAGES` | The Studio dropdown names the VPS uploader clicks (English Studio UI) | "Spanish (Latin America)", "Portuguese (Brazil)", "Indonesian", "Vietnamese", "Thai". Check the exact option text in Studio once; the uploader is not live yet (`2026-10-09-vps-studio-uploader-uploads-the-dub`) |
| `tools/video/review/language-contract.mjs`, `tools/video/production/retention.mjs:15` | Fixtures, and the retention plan's en/ja/ko | Extend the fixtures. Retention stays as it is unless a drama ticks the five |
| `docs/videos/long-form/review.json` | The duration receipt binds several of these files by SHA-256 | A reviewer increment from a separate agent, as #1593 needed |

These are not limits:
- The YouTube sync and the retitle tool already send `es-419`/`pt-BR` (#1593).
- `video_projects.locales` and `dub_retries` are json without a key check.
- The worker's language round (`flow.mjs`) iterates whatever the panel chose.

## Speaking rates

The pipeline counts **every** character of a translation, spaces and punctuation included
(`plan.mjs` `estimatedLengths`: `[...text].length`). The 種田娶妻 rates were measured without
spaces and punctuation. They convert by each language's ratio of all characters to bare ones,
measured on the 946 dubbed lines of e001–e024 (2026-10-20):

| | bare cps (種田娶妻) | all/bare | pipeline cps | `RATE_RATIOS` (÷ zh-TW 5.8) |
| --- | ---: | ---: | ---: | ---: |
| en (check) | 11.6 | 1.264 | 14.7 | 2.6 today (15) |
| es | 10.7 | 1.242 | 13.3 | 2.3 |
| pt | 9.5 | 1.257 | 11.9 | 2.05 |
| id | 10.9 | 1.218 | 13.3 | 2.3 |
| vi | 13.2 | 1.321 | 17.4 | 3.0 |
| th | 11.9 | 1.050 | 12.5 | 2.15 |

The en row is the check. Counted the pipeline's way, the acted drama lines ran at 14.7 against the
narration's 15. So "drama is slower than narration" was mostly the two ways of counting. These
are starting values only: a finished dub writes its measured rate into `fit.json`, and the next
budgets use that.

How hard each language fits, per zh-TW character:

| | en | es | pt | id | vi | th |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Characters the fitted 種田娶妻 dubs used | 3.07 | 2.79 | 2.67 | 2.89 | 3.00 | 2.47 |
| Room at the 1.15× tempo limit (ratio × 1.15) | 2.99 | 2.65 | 2.36 | 2.65 | 3.45 | 2.47 |

So expect pt to need the most shortening rounds, and to skip the most dubs. es and id should need
about as many rounds as en, th sits at the edge, and vi has room.

## Costs

The table is per **10 minutes of narration** (600 s of speech), for the five new languages with
all three parts ticked. Prices are the site's constants (`video_speech/admin_api.py:104`, paid
rates through 2026-12-31).

| | Five new languages | en+ja+ko today, for comparison |
| --- | --- | --- |
| TTS characters (rate × 600 s) | es 7,980 + pt 7,140 + id 7,980 + vi 10,440 + th 7,500 = **≈41,000** | en 9,000 + ja 4,680 + ko 4,020 = ≈17,700 (zh-TW narration: 3,480) |
| … with retakes (scene mode re-records scenes it cannot split, up to 1.5×, DUBS.md) | 41,000–62,000 | 17,700–26,500 |
| Gemini TTS money (`gemini-3.8-flash-tts`: audio at US$9 per M tokens × 25 tokens/s = US$0.0135 a minute; text input negligible) | 5 × US$0.135 = **US$0.68–1.01** | US$0.41–0.61 |
| check-audio transcription (`gemini-3.8-flash`, one pass per locale) | ≈ US$0.05–0.10 | ≈ US$0.03–0.06 |
| Jev (TypeSafe, output free) | Negligible money, but each locale's check takes ⌈doubted lines / 40⌉ of the **200 calls a day** (`jev_daily_call_budget`) | Same |
| Translation (host Claude Code subscription, no per-token bill) | Per locale, one translator call (`claude-sonnet-5`, three passes in one answer) and one caption-reviewer call (`claude-opus-5-5`) per sheet unit. Dubbed locales add up to 2 shorten rounds and reword passes. **+10 to +30 model calls a video** | 6 to 18 calls today |

So the money is small: about **US$1 (≈NT$33) per 10-minute video** with all five dubbed. The
real limits are three quotas.

- **Monthly character limit**, `VIDEO_SPEECH_GEMINI_MONTHLY_CHARACTER_LIMIT`, 300,000 by default.
  Its comment puts that at about a hundred zh-TW-only 10-minute videos. A 10-minute video uses:

  | Languages | Characters | Videos 300k covers |
  | --- | ---: | ---: |
  | zh-TW only | ≈3,500 | about 86 |
  | + en/ja/ko dubs | ≈21,000 | about 14 |
  | **all eight** | **≈62,000** (up to ≈90,000 with retakes) | **about 4–5** |

  The brand-story line alone is planned at two 12–15-minute videos a day. Dubbing all of them in
  eight languages would need ≈5M characters a month, about US$90 of TTS.

  The limit is a cost ceiling, not a price. Latin-script dubs cost about US$0.019 per 1,000
  characters (12–17 cps), zh-TW narration about US$0.039. So a limit of 1.5M characters a month
  caps the bill at about US$30–60.
- **Daily requests**: 10,000 a day for `gemini-3.8-flash-tts` on the site's paid Tier 2 key.
  - Scene mode is about one request per scene (15–25 for 10 minutes), plus per-line retakes.
    `--line-by-line` is one request per line (100–150 for 10 minutes).
  - Eight dubs line by line come to ≈1,200 requests a video, so ≈8 fully dubbed videos a day fit.
  - The worker makes one dub at a time (`flow.mjs` returns after one `makeDub`), so it paces itself.
    The 2026-10-19 exhaustion came from ten dub agents running in parallel outside the worker, with
    every line its own request.
- **Claude Code weekly quota** on the host accounts. The Opus caption reviewer is most of the
  translation cost. If the quota pinches, the five's review can run on Sonnet, but that needs a
  per-locale stage override, which does not exist yet.

## Plan (after the owner says yes)

Phase 1: **captions and titles** (no TTS spend).
- [x] `schema.mjs`: split `NARRATION_LOCALES` (four) from `TARGET_LOCALES` (eight). Every
      importer in the table moves to the one it means.
- [x] Translator, caption-reviewer, shorten and reword texts: a register and a line length per
      locale.
- [x] The script check in `i18n-merge` (ported from `dub-lines.mjs`).
- [x] Captions: rules for the five, plus Thai word segmentation and a width that skips combining
      marks. Test them with a real Thai line and a vi line with stacked diacritics.
- [x] Metadata labels and caption words, compilation episode labels, the Thai thumbnail font.
- [x] API: the five become worker locales for the chosen categories; the settings tab gets the
      rows and the `max_length`; tests in `apps/api/tests/test_video_languages_worker.py`.
- [x] Uploader language names, LANGUAGES.md, the duration receipt increment.
- [ ] Pilot: one finished video with captions and titles in all five. Spot-check the th and vi
      captions with a native speaker (or a second model's review) before the panel offers them
      widely.

Phase 2: **dubs** (TTS spend starts).
- [x] `RATE_RATIOS`, `DEFAULT_RATES` and `DUB_STYLES` from the tables above.
- [x] A dub-locale list of its own (`DUB_TARGET_LOCALES`), followed by every importer.
- [x] Server transcription prompts and `TrackLanguage`, the Whisper second-opinion languages, and
      the vi tone-mark fold in `comparable()`.
- [x] API and panel: the 422 `video_locales_dub_imported_only` and the greyed dub boxes go; the
      dub retry takes the eight. Dramas whose characters speak stay refused.
- [x] DUBS.md, LANGUAGES.md, the duration receipt increment.
- [ ] Pilot: one 10-minute video dubbed in pt (the hardest fit) and th (the new script) with
      `--line-by-line`. Record its characters, requests, shortening rounds and measured rates in
      this file.
- [ ] Raise the monthly character limit if the owner chose to (host `.env`, with the owner's
      approval).

Phase 3: Shorts, only if the owner wants them.

## How to verify

Run:
- `node --test tools/video/core tools/video/i18n tools/video/dubs tools/video/tts`
- `cd apps/api && uv run pytest tests/test_video_languages_worker.py tests/test_video_languages_imported.py`
- `npm run test:web`

After the deploy:
- A pipeline video's panel on `/zh-TW/admin/videos` lists the eight rows for the chosen categories.
- Ticking th captions makes the worker send a `languages` batch whose `th.srt` cues break between
  Thai words.

## Notes

- 2026-10-20 (claude-opus-5.5-worker-languages): mapped on origin/main 1e60f734e. The plan and
  the costs above are this session's, put to the owner before any code. Status `blocked` until
  the owner answers whether to build it and for which categories.
- 2026-10-20, the owner's answers (asked in the planning session, PR #1608):
  - **Build it in phases**, as planned: captions and titles first with one pilot video, then
    dubs with one pt and one th pilot.
  - **Categories: all of them.** That means brand stories (`story`), the explainer and tutorial
    group (`ai-terms`, `ai-news`, `tutorial`, `comparison`, `explainer`) and **Shorts** (phase 3).
    The drama group (`drama`, `long-drama`, `anime`) gets captions and titles only, since
    multi-character dubs are still phase two of DUBS.md. So the 422
    `video_locales_imported_only` goes away for captions and titles; for dubs it stays wherever
    a dub is refused today.
  - **Monthly character limit: raise it to 1,500,000** (≈24 fully dubbed eight-language 10-minute
    videos, a ceiling of about US$30–60 a month). This is a host `.env` change: make it with
    phase 2, under the deploy rules.
  - **Defaults: pre-tick captions and titles for all languages.** The settings tab's language
    defaults tick metadata and captions for all eight (en, ja, ko, es, pt, id, vi, th). Dubs are
    never pre-ticked. This changes the 2026-09-27 default for en/ja/ko (pre-ticks only; nothing
    is made until the owner saves a video's panel). Every saved panel then costs translation
    calls for eight locales, about +10 calls a video over today's three.
- 2026-10-20 (claude-opus-5.5-worker-languages-phase1), phase 1 built on branch
  `claude/worker-video-languages-five` (from the plan branch, PR #1608 not merged yet). Claimed
  with `--force`: every overlapping claim was over 24 hours old, and the 2026-10-19
  eight-languages one has its code merged (#1593). The scope grew to the files the split
  touches (package, qa, render, review, compile, import, flow, the prompt references, the
  contract fixtures); they are listed above.
  - **Three lists, not two.** `NARRATION_LOCALES` (four: narration and dubs), `TARGET_LOCALES`
    (nine: translations, captions, titles, language thumbnails) and `DEFAULT_LOCALES` (the
    four). The third keeps a video with no language choice (a pre-panel package, a hand run,
    the examples) and **compilations** on the four. Without it every old package failed its
    captions check for five missing files, and a compilation's QA wanted es…th captions from
    every episode. So compilations do not make the five yet; the episode labels are in place
    for when they do. `i18n-sheet` without `--locale` still translates into the four; with
    `--locale` it takes any of the nine.
  - **Thai line length is about 60, not 40.** The fitted 種田娶妻 dubs used 2.47 Thai characters
    per zh-TW character against English's 3.07. With English at 80, Thai would be about 64,
    and 40 would force heavy cutting. Thai is counted without its combining marks.
  - **The script check covers only the five.** On en, ja and ko it would have broken the test
    fixtures, which fill ja sheets with English placeholders, for no gain. Scanning all 12,108
    committed translated lines with the full table found 4 hits. All were real slips: an English
    curio title ending on 「奇聞檔案局」, and a Korean line that dropped its words.
  - The language-thumbnail gap notes and `render`'s output list the five only once a video has
    their translation, so existing renders stay byte-identical.
  - API: every video's panel offers the eight. A five-language dub on a pipeline video is a 422
    `video_locales_dub_imported_only`, and the panel greys those boxes out. Migration 0136 writes
    the eight into `caption_locales` and `drama_caption_locales`. Story videos decide their
    languages from `drama_caption_locales`, so new brand stories get eight titles and captions.
  - **Deploy order:** the worker image must ship with the API, or no later than it. Otherwise the
    panel and the story decision tick languages an old worker cannot make, and the cells stay
    "working".
  - Uploader: Studio names for the five are not yet checked against a real dropdown. The
    manifest file cap went from 12 to 20, which covers 9 captions, 8 dubs, the final cut and
    the thumbnail.
  - Duration receipt: 22-file increment by `claude-pr-review-worker-languages-five`, PASS.
  - Checks (Windows): tools 2572 tests. The only failures are the 5 that also fail on a clean
    checkout of the base (backup ×2, whisper second opinion, adult-English, elementary). The
    duration-receipt test now passes. docs-videos 236/236. API: targeted files pass; the full
    run fails only 27 anime-policy/planning tests on Windows `charmap`, which pass with
    PYTHONUTF8=1. The 0136 SQL runs only in CI (no local Postgres). Web: lint, i18n, typecheck,
    4186/4186.
  - **Pilot: not done; it is the owner's next step after the deploy.** Choose es, pt, id, vi and
    th titles and captions on one finished video. Then have a native speaker or a second model
    read the th and vi captions before the panel is used widely.
- 2026-10-20 (claude-opus-5.5-worker-dubs-five), phase 2's code on branch
  `claude/worker-video-dubs-five` from origin/main 8e613894e (phase 1 live). Re-claimed with
  `release` then `claim --force`: the phase-1 owner's session had finished (#1611 merged), and
  the five overlapping claims are older than 24 hours or their code is merged. The scope is now
  only what phase 2 touches (listed above).
  - **A fourth list, `DUB_TARGET_LOCALES`** (`core/schema.mjs`, the nine of `TARGET_LOCALES`).
    `dubs/plan.mjs` `DUB_LOCALES`/`dubLocales`, `dub --locale`, `tts/check.mjs` `DUB_LOCALES`
    and `parseDubLocale`, and `automation/tidy.mjs` (through `DUB_LOCALES`) read it.
    `NARRATION_LOCALES` stays the four, so `narration_locale` can never be one of the five.
  - **The default dubs stay en, ja and ko.** `DEFAULT_DUB_LOCALES`/`defaultDubLocales` now come
    from `DEFAULT_LOCALES`, not from the dub list: a package from before the panel, or `dub`
    without `--locale`, would otherwise start paying for five more tracks. `stages.mjs`
    `dubLocalesOf` needed no change (the chosen ones, or that default).
  - `state.mjs` `dubsStatus` lists the five as "missing" until made; `cli.mjs status` already
    hides "missing", and the worker reads only the chosen locales. The worker's language round
    (`flow.mjs`) and the shorten/reword prompts (`TARGET_REGISTERS`, phase 1) needed no change.
  - **vi fold:** `comparable(text, locale)` moves each syllable's tone mark (NFD U+0300, 0301,
    0303, 0309, 0323) to the syllable's end for vi, so hoà/hòa and thuỷ/thủy compare equal while
    má/mà, a dropped tone, â/a and đ/d still differ. Only `matchKind`'s "exact" uses it; the rest
    is Jev's, as for en/ja/ko.
  - **Thai budget count:** dub budgets count every code point (`[...text].length`), Thai combining
    marks included, as the 種田娶妻 rates did. The phase-1 caption line length counts Thai
    without them; the two are separate numbers. Watch in the pilot whether the shorten pass's
    `max_chars` for th is read the same way by the translator.
  - **API:** `video_reviews/schemas.py` names the lists by role: `NARRATION_LOCALES` (en, ja, ko),
    `ADDED_LOCALES` (the five), `DUB_LOCALES` (eight), `WORKER_DUB_LOCALES` = the eight.
    `IMPORTED_DUB_LOCALES`, `WorkerDubLocale`, `imported()` and `IMPORTED_CHECKLIST_KEY` went with
    the 422. `retry_dub` takes `DubLocale`. `video_youtube/requests.py` reads `NARRATION_LOCALES`
    for the narration languages and `ADDED_LOCALES` for the combined-title rule (unchanged
    behaviour).
  - **Panel:** the five's dub boxes are no longer greyed and `dubWorkerLater` left the five
    `admin.json` files. An imported video still offers "再做一次" only for en, ja and ko, as
    before (its five tracks are made outside the pipeline).
  - Production runs Whisper `medium` (`WHISPER_MODEL`, DUBS.md), which also has the five.
  - **Owner's next steps, not done here:** (1) after the deploy, the pilot above: one 10-minute
    video dubbed in pt and th with `--line-by-line`, recording characters, requests, shortening
    rounds and measured rates in this file; (2) raising
    `VIDEO_SPEECH_GEMINI_MONTHLY_CHARACTER_LIMIT` to 1,500,000 in the host `.env`, only with the
    owner's explicit approval. Deploy order is as in phase 1: the worker image with the API, or
    before it, or a ticked five-language dub stays "working" on an old worker.
