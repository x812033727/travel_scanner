---
id: 2026-10-09-video-languages-are-four-drop-zh
title: "Video languages are four: drop zh-CN from the video pipeline"
status: in-progress
priority: P1
area: tools
owner: claude-fable-5.1
claimed_at: 2026-10-09T15:27:00Z
created_at: 2026-10-09T15:26:00Z
completed_at:
branch: claude/video-languages-four
depends_on: []
scope:
  - apps/api/app/video_reviews
  - apps/api/app/video_automation
  - apps/api/app/video_shorts
  - apps/api/app/video_youtube
  - apps/api/app/video_speech
  - apps/api/migrations/versions
  - apps/api/tests
  - apps/web/components
  - apps/web/messages
  - tools/video
  - docs/videos/LANGUAGES.md
  - docs/videos/DUBS.md
  - docs/videos/DESIGN.md
  - docs/videos/AUTOMATION.md
  - docs/videos/README.md
  - docs/videos/STORY.md
  - docs/videos/MILLION-VIEWS.md
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
---

# Video languages are four: drop zh-CN from the video pipeline

## Why

On 2026-10-09 the owner, told that the dub tracks never reached YouTube and that most dubs
were skipped, added: 「另外幫我將簡體中文拿掉，預計四語就好」. A video is narrated in zh-TW and
may add en, ja and ko (titles and descriptions, CC, dub); Simplified Chinese leaves the
VIDEO pipeline. The site keeps its five locales (articles, UI, `apps/api/app/i18n.py`,
`usage.locales`, the `ck_*_locale` checks): those are not touched.

The four video languages are listed independently in four places that share no code
(survey of 2026-10-09): the API (`DubLocale`, `CaptionLocale`, `ShortsLocale`,
`TrackLanguage`), the web (`LOCALES`, `CAPTION_LOCALES`, `SHORTS_LOCALES`), the tools
(`core/schema.mjs` `LOCALES` plus copies in `production/retention.mjs`, `review/renewal.mjs`,
`review/renewal-handoff.mjs`, `shorts/package.mjs` `EXTRA_LOCALES`) and the docs. Every
video on production has zh-CN ticked for titles and CC (the default ticks are
`DEFAULT_CAPTION_LOCALES`), and `captionLocalesOf(null)` makes zh-CN captions for a video
with no choice at all.

## Definition of done

- [ ] The language panel, the settings tab's default ticks and the Shorts settings offer
      en, ja, ko only; `PUT /admin/videos/{slug}/languages` refuses zh-CN.
- [ ] The worker translates, captions and packages zh-TW plus the chosen languages only; no
      zh-CN sheet, caption file, description or dub is made for a new video.
- [ ] Existing data survives: a project whose stored `locales` has a zh-CN key, an approved
      languages batch whose manifest included zh-CN, and settings rows holding "zh-CN" are
      read as if zh-CN had never been there (a data migration strips it, and the readers
      tolerate it), so YouTube sync of their en/ja/ko parts keeps working.
- [ ] Old packages and reviews with `captions_zh_cn` / `dub_zh_cn` files still display and
      download; the aliases that read a zh-Hans caption track back from YouTube stay.
- [ ] Docs and the `youtube-video` skill say four languages; the contract fixtures under
      `apps/api/tests/fixtures/video_language_contract` are regenerated.

## Steps

- [x] Survey (read-only agent, 2026-10-09).
- [ ] Tools, docs and skill on branch `claude/video-languages-four-tools` (agent).
- [ ] API, migration and web on branch `claude/video-languages-four-apps` (agent).
- [ ] Merge both into `claude/video-languages-four`, regenerate the contract fixtures with
      `tools/video/review/language-contract.mjs`, run every check, open the PR.

## How to verify

`npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web`,
`npm run test:tools`, `cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest`.
After the deploy: open `/zh-TW/admin/videos?video=<a video with zh-CN ticked>`: the panel
shows three rows and the saved choice minus zh-CN; `/admin/videos?tab=settings` loads and
"照預設勾選" ticks en, ja, ko.

## Notes

- Videos already carrying zh-CN titles, descriptions or captions on YouTube keep them; the
  site only ever adds languages, and removing a track is the owner's job in Studio.
- The six imported `ai-real-world-*` videos (`2026-09-29-resume-imported-long-video-languages`)
  had zh-CN chosen; after the migration their choice is en/ja/ko metadata and captions.
