---
id: 2026-10-19-imported-video-languages-eight
title: Imported videos may add es, pt, id, vi, th besides en, ja, ko
status: in-progress
priority: P2
area: api
owner: claude-opus-5.5-eight-languages
claimed_at: 2026-10-19T11:17:04Z
created_at: 2026-10-19T11:16:44Z
completed_at:
branch: claude/epic-mestorf-3bbb2c
depends_on: []
scope:
  - apps/api/app/video_reviews
  - apps/api/app/video_youtube
  - apps/api/tests/test_video_languages_imported.py
  - apps/api/tests/test_video_youtube.py
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-review-card.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
  - tools/video/import
  - docs/videos/LANGUAGES.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Imported videos may add es, pt, id, vi, th besides en, ja, ko

## Why

On 2026-10-09 the owner set a video's languages to zh-TW plus en, ja and ko (#1413,
`docs/videos/LANGUAGES.md`). On 2026-10-18 they asked for 種田娶妻打天下 in Latin-American
Spanish, Brazilian Portuguese, Indonesian, Vietnamese and Thai as well, to reach viewers outside
the zh/en/ja/ko audiences (`tasks/done/2026-10-18-dubs-and-cc-in-es-id.md`). Episodes 1–24 and
the 1–5 compilation have the five languages' dubs, CC and translated titles in their import
folders (`~/mokaair-work/videos/zhong-tian-qu-qi-import/<slug>/`), but the language panel offers
only en, ja and ko, so `tools/video/cli.mjs import --languages` (#1570) can send only those.

## Scope (decided here)

- The five new languages are for **imported** videos only (a project whose checklist carries
  `imported`, as `tools/video/import` reports). The owner asked for them for one imported
  series; the host worker cannot translate or dub them (`tools/video/core/schema.mjs` `LOCALES`
  stays zh-TW/en/ja/ko), so offering them on a pipeline video would be a promise nothing keeps.
  `PUT /admin/videos/{slug}/languages` refuses them elsewhere (422 `video_locales_imported_only`).
- The worker, the default ticks (`caption_locales`, `drama_caption_locales`,
  `DEFAULT_CAPTION_LOCALES`, `CaptionLocale`) and the Shorts (`SHORTS_LOCALES`) are unchanged:
  no new translation or TTS spend.
- The dub retry endpoint keeps taking en, ja, ko only: only the worker remakes a dub.
- A narration language stays zh-TW, en, ja or ko.
- On YouTube the site keeps its short codes and sends BCP-47 tags: es → `es-419`, pt → `pt-BR`,
  id, vi and th as they are. Each new language's captions tag is its local search term
  (Sub Indo, Vietsub, ซับไทย, Legendado; es keeps "CC"), as the 10-18 titles already end.
- No migration: `video_projects.locales` is json without a key check, and the languages gate and
  file roles take any locale already.

## Definition of done

- [x] The language panel of an imported video lists eight languages; other videos still three.
- [x] `import --languages` sends `description_<l>`, `captions_<l>`, `dub_<l>` for es, pt, id, vi,
      th when ticked (test), and the batch's language states read "ready".
- [x] en, ja, ko behave as before (existing tests pass).
- [x] YouTube sync and the retitle tool send `es-419`/`pt-BR` and keep the local caption words.

## Steps

- [x] API: locale literals, imported-only rule, `locale_options` on the project, YouTube codes.
- [x] Web: panel rows from `locale_options`, language names in five site locales.
- [x] tools/video/import: the eight languages.
- [x] Docs (`LANGUAGES.md`), checks, PR with the post-deploy steps.

## How to verify

`cd apps/api && uv run pytest tests/test_video_languages_imported.py`,
`node --test tools/video/import/import.test.mjs`, `npm run test:web`; after the deploy, an
imported episode's panel on `/zh-TW/admin/videos?video=zhong-tian-qu-qi-e001` lists eight rows.

## Notes

- Claimed with `--force`: the overlapping claims (2026-10-12 Studio link, 2026-10-13 narrator
  dubs, 2026-10-17 import languages) are stale or have their code merged.
- 2026-10-19 (claude-opus-5.5-eight-languages): the bound files changed, so the duration review
  receipt got an increment from a separate reviewer (`claude-pr-review-imported-languages-eight`).
- Imported videos have no upload package (`publish` review), so neither the API sync nor the VPS
  uploader handles them today; their titles, CC and dubs still go up through Studio from the
  languages card. The `es-419`/`pt-BR` tags are unverified against YouTube until a first API sync.
- Local runs on Windows: tools failures in adult_english, elementary/profile and tts/check, and
  the API's `test_video_anime_planning_cli` encoding failure, fail the same on clean origin/main.
