---
id: 2026-10-21-imported-videos-send-an-upload-package
title: Imported videos send an upload package so the site can put them on YouTube
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-import-publish
claimed_at: 2026-10-21T06:20:09Z
created_at: 2026-10-21T06:19:42Z
completed_at:
branch: claude/import-publish-package
depends_on: []
scope:
  - tools/video/import
  - docs/videos/COMPILATIONS.md
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/prep-import.mjs
---

# Imported videos send an upload package so the site can put them on YouTube

## Why

A video made outside the pipeline goes to /admin/videos with `tools/video/cli.mjs import`: its
final cut (`import --from DIR`) and its languages (`--languages`). The pipeline's videos also send
a third review, the upload package (`publish` gate: metadata.json, final.mp4, thumbnail, captions),
made by `package` and `review-push --gate publish`, which need a `video.json` project and a work
directory an imported video does not have. Without an approved package `publish_approved_at` stays
null, the card never reaches 「可以上架」 and 「送到 YouTube」 never appears: the owner uploaded
every 種田娶妻打天下 episode and compilation in Studio by hand (owner, 2026-10-21: 「要怎麼自動上傳
跟其他影片一樣」).

The site already takes such a package (apps/api/app/video_youtube/sync.py `read_package`,
language_package.py `compose`): when the languages batch came before the package, it reads each
ticked language from the package's own files and `localizations`, with `skipped_*_locales` for a
part that was not made. A languages batch sent after the package has no source manifest and would
make the package unreadable, so the order is languages first, then the package.

## Checklist

- [x] `importPublish` in `tools/video/import/import.mjs` and `--publish` in its cli: metadata.json
      (title, description, tags, category_id, made_for_kids, the synthetic-media answer, zh-TW,
      final_sha256, chapters, localizations, language_choice, skipped parts), the cut, the
      thumbnail (≤ 2 MB), zh-TW captions and the ticked captions and dubs, hand-pushed.
- [x] Refuses before uploading: a cut not approved or not the site's newest, a ticked title the
      folder lacks, a dub of another length, a thumbnail over 2 MB, a non-drama without a
      disclosure answer; `--languages` refuses once a package was sent.
- [x] Tests in `import.test.mjs`.
- [ ] `prep-import.mjs` writes the compilation's tags and category id into meta.json.
- [ ] Send the package of 種田娶妻打天下 第1–5集 and have the owner approve it.
- [ ] `COMPILATIONS.md` says the step.
