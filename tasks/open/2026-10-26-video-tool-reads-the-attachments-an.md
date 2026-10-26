---
id: 2026-10-26-video-tool-reads-the-attachments-an
title: Video tool reads the attachments an owner renewal retains
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-26T07:20:14Z
created_at: 2026-10-26T07:18:33Z
completed_at:
branch: claude/focused-hopper-zq70n8
depends_on: []
scope:
  - apps/api/app/video_reviews/tool_files.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_video_reviews_tool_files.py
  - tools/video/review/files.mjs
  - tools/video/review/files.test.mjs
  - docs/videos/BRANDING.md
---

# Video tool reads the attachments an owner renewal retains

## Why

`review-files` (#1862) only read pending or approved reviews. An owner renewal of an approved
final marks the old final, publish package and languages batch superseded but keeps their
attachments (`retained_review_ids` on the new final), because the publish package and every
language are rebuilt from exactly those files. On 2026-10-26 the Ollama renewal
(`ollama-phonon-local-speech-language-gap`) was submitted before its eight languages' dubs,
captions and descriptions had been fetched, and the tool could no longer read them.

## Definition of done

- [x] The tool route also serves files of reviews a pending or approved renewal retains; any
      other superseded or rejected review stays 404, and a rejected renewal retains nothing.
- [x] `review-files` writes them under `DIR/retained/<gate>/`, apart from the renewed cut.
- [x] BRANDING.md says so.
- [ ] Deployed, and the Ollama languages batch comes back with `review-files`.

## Steps

- [x] `tool_files.readable()`: live reviews, then the ones a live renewal retains.
- [x] Test: retained readable, unrelated superseded refused, rejected renewal retains nothing.
- [x] `files.mjs` `liveFiles` and its test.
- [x] Error sentences say "renewal-retained" in en, ja, ko, zh-CN.
- [ ] After deploy: `review-files --slug ollama-phonon-local-speech-language-gap --out DIR`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_reviews_tool_files.py tests/test_error_localization.py
node --test tools/video/review/files.test.mjs
```

## Notes

- `retained_review_ids` is written by the owner renewal (admin_service, `RENEWAL_KEY`), and
  `kept_files` already keeps those reviews' bytes in the store; this only lets the tool read them.
