---
id: 2026-10-19-worker-video-languages-five
title: Video worker makes es, pt, id, vi, th captions, titles and dubs
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-19T23:53:40Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core
  - tools/video/i18n
  - tools/video/dubs
  - tools/video/tts
  - tools/video/render/fonts.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/shorts
  - tools/video/review/language-contract.mjs
  - tools/video/production/retention.mjs
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/video_shorts/schemas.py
  - apps/api/tests/test_video_languages_worker.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-shorts-data.ts
  - apps/web/messages
  - services/youtube-uploader/src/contract.mjs
  - package.json
  - package-lock.json
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
- [ ] `schema.mjs`: split `NARRATION_LOCALES` (four) from `TARGET_LOCALES` (eight). Every
      importer in the table moves to the one it means.
- [ ] Translator, caption-reviewer, shorten and reword texts: a register and a line length per
      locale.
- [ ] The script check in `i18n-merge` (ported from `dub-lines.mjs`).
- [ ] Captions: rules for the five, plus Thai word segmentation and a width that skips combining
      marks. Test them with a real Thai line and a vi line with stacked diacritics.
- [ ] Metadata labels and caption words, compilation episode labels, the Thai thumbnail font.
- [ ] API: the five become worker locales for the chosen categories; the settings tab gets the
      rows and the `max_length`; tests in `apps/api/tests/test_video_languages_worker.py`.
- [ ] Uploader language names, LANGUAGES.md, the duration receipt increment.
- [ ] Pilot: one finished video with captions and titles in all five. Spot-check the th and vi
      captions with a native speaker (or a second model's review) before the panel offers them
      widely.

Phase 2: **dubs** (TTS spend starts).
- [ ] `RATE_RATIOS`, `DEFAULT_RATES` and `DUB_STYLES` from the tables above.
- [ ] Server transcription prompts and `TrackLanguage`, the Whisper second-opinion languages, and
      the vi tone-mark fold in `comparable()`.
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
