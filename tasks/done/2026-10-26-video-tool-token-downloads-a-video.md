---
id: 2026-10-26-video-tool-token-downloads-a-video
title: Video tool token downloads a video's live review attachments
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-26T06:05:09Z
created_at: 2026-10-26T05:55:27Z
completed_at: 2026-10-26T06:53:50Z
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - apps/api/app/video_reviews/tool_files.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/tests/test_video_reviews_tool_files.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/web/app/api/video/reviews/[...path]
  - tools/video/review/files.mjs
  - tools/video/review/files.test.mjs
  - tools/video/review/cli.mjs
  - tools/video/cli.mjs
  - docs/videos/BRANDING.md
---

# Video tool token downloads a video's live review attachments

## Why

A video made in a cloud session keeps its work directory only while the session lives. After
that, its approved cut, captions, descriptions, thumbnails and dub tracks exist only as
attachments in the site's review store, and until now only a signed-in owner could read them
(`GET /api/v1/admin/video-reviews/{slug}/files/{sha256}`). On 2026-10-26 the approved
`ollama-phonon-local-speech-language-gap` needed its channel intro and outro added; no session
held its files, so the owner had to copy them read-only off the host from their own PC. Any
later renewal or re-import of a cloud-made video would hit the same wall.

## Definition of done

- [x] The video tool token can read a file that a pending or approved review of the same video
      lists, and nothing else: rejected or superseded reviews' files, another video's files and
      unlisted store contents answer 404.
- [x] The same-origin forwarder passes that read through for `Bearer mkv_` tokens only, streams
      it, passes a single byte range through, and never lets it be cached.
- [x] `node tools/video/cli.mjs review-files --slug S --out DIR` copies a video's live
      attachments to `DIR/<gate>/<role>.<ext>`, checks each SHA-256 and size, keeps what is
      already there, and writes `review-files.json`.
- [x] docs/videos/BRANDING.md says when and how to use it.
- [x] Deployed, and one real `review-files --dry-run` against production lists a video's files.

## Steps

- [x] API: `tool_files.file_for_tool` and `GET /api/v1/video/reviews/{slug}/files/{sha256}` on
      the tool router, rate-limited per token (600 an hour), `private, no-store`, ETag, Range.
- [x] Tests: `test_video_reviews_tool_files.py` (live vs dead reviews, a vanished file, 401, 206,
      headers) and the integration test's new/old cut assertions.
- [x] Web: `download` kind in `apps/web/app/api/video/reviews/[...path]/forward.ts`, tests.
- [x] Tool: `tools/video/review/files.mjs`, wired as `review-files`, tests.
- [x] Docs: BRANDING.md "工作檔不在了：從審核區取回附件".
- [x] After deploy: `review-files --slug ollama-phonon-local-speech-language-gap --dry-run`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_reviews_tool_files.py && uv run ruff check . && uv run mypy app tests
npx vitest run --root apps/web "app/api/video/reviews"
node --test tools/video/review/files.test.mjs
# after deploy, with the token in ~/.mokaair/video-tool.json:
node tools/video/cli.mjs review-files --slug <a video with an approved final> --dry-run
```

## Notes

- Only `pending` and `approved` reviews are readable, matching what the owner can still see and
  decide; superseded ones are history and stay owner-only.
- The store verifies a file's SHA-256 when its last part arrives, not on every read; the tool
  checks it again after the download and deletes a mismatching file.
- The command changes nothing on the site. Its output is the starting point for `renewal.mjs
  stage` or `import --from`; an already-uploaded video still cannot be renewed and needs a new
  slug.
- 2026-10-26, after the deploy of #1862: `--dry-run` for `ollama-phonon-local-speech-language-gap`
  listed 43 files (audio, final, publish approved; languages pending), and `--gate final --out`
  fetched preview.mp4, contact_sheet.png and thumbnail.jpg with matching SHA-256; a second run
  kept all three. The scratch copy was deleted afterwards.
- Captions go up as `text/plain`, so they come back as `captions_<locale>.txt`; the bytes are
  SubRip. Naming them `.srt` by role would read better, but nothing depends on it.
