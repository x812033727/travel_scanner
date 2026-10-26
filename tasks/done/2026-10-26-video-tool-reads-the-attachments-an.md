---
id: 2026-10-26-video-tool-reads-the-attachments-an
title: Video tool reads the attachments an owner renewal retains
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-26T07:20:14Z
created_at: 2026-10-26T07:18:33Z
completed_at: 2026-10-26T08:20:51Z
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
- [x] Deployed, and the Ollama languages batch comes back with `review-files`.

## Steps

- [x] `tool_files.readable()`: live reviews, then the ones a live renewal retains.
- [x] Test: retained readable, unrelated superseded refused, rejected renewal retains nothing.
- [x] `files.mjs` `liveFiles` and its test.
- [x] Error sentences say "renewal-retained" in en, ja, ko, zh-CN.
- [x] After deploy: `review-files --slug ollama-phonon-local-speech-language-gap --out DIR`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_reviews_tool_files.py tests/test_error_localization.py
node --test tools/video/review/files.test.mjs
```

## Notes

- `retained_review_ids` is written by the owner renewal (admin_service, `RENEWAL_KEY`), and
  `kept_files` already keeps those reviews' bytes in the store; this only lets the tool read them.
- 2026-10-26, after the deploy of #1865: `review-files` fetched all 47 attachments of
  `ollama-phonon-local-speech-language-gap`, among them the 34 of the retained languages batch,
  each with a matching SHA-256. From them the upload package and the eight languages were rebuilt
  for the renewed final (dubs wrapped with the same bookend audio by `wrapAudio`, captions and
  chapter clocks moved by the 5-second intro) and sent hand-pushed: publish review
  `0bf980f0-6635-4dc5-aa5e-1214f39b0c26`, languages review `aeec7756-72fe-4b16-a871-a285cfc34c10`,
  both pending for the owner.
- The rebuild was a one-off script, not a pipeline command. The handoff tool's manual-import mode
  (`renewal-handoff.mjs`) holds dubs for a video without a retained script and timing adapter, and
  `import --languages` only takes videos the import command made; a pipeline video whose work
  directory is gone has neither. If this recurs, a `review-files`-based renewal command for
  package and languages would be the place to fold it in.
