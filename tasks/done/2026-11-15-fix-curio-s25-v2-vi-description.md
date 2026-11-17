---
id: 2026-11-15-fix-curio-s25-v2-vi-description
title: Fix curio-s25-v2 vi description byte budget and es thumbnail headline overflow
status: done
priority: P2
area: docs
owner: antigravity
claimed_at: 2026-11-15T10:31:46Z
created_at: 2026-11-15T10:31:13Z
completed_at: 2026-11-15T10:47:20Z
branch: antigravity/curio-s25-v2-i18n-fix
depends_on: []
scope:
  - docs/videos/curio-s25-v2
---

# Fix curio-s25-v2 vi description byte budget and es thumbnail headline overflow

## Why

`curio-s25-v2` failed to package all eight translated languages cleanly for two reasons in its `i18n/` files:
1. `i18n/vi.json`'s `description` composed to `5,001` UTF-8 bytes (`1` byte above YouTube's `5,000`-byte limit).
2. `i18n/es.json`'s `thumbnail.headline` (`"Newton\n**¿Manzanazo?**"`) overflowed the layout `e` thumbnail headline width even at `60%` font scale, leaving `thumbnails/es.jpg` undrawn.

## Definition of done

- [x] `docs/videos/curio-s25-v2/i18n/vi.json` composes under `5,000` UTF-8 bytes without touching `lines` (preserving existing dub bindings).
- [x] `docs/videos/curio-s25-v2/i18n/es.json` `thumbnail.headline` fits cleanly and `render --thumbnails-only` draws `thumbnails/es.jpg`.
- [x] `node tools/video/cli.mjs lint --slug curio-s25-v2` and `npm run check:tasks` pass.

## Steps

- [x] Trim redundant pointer phrase in `docs/videos/curio-s25-v2/i18n/vi.json` (`Nguồn ở phần tham khảo bên dưới.` -> `Nguồn ở bên dưới.`).
- [x] Shorten line 2 of `docs/videos/curio-s25-v2/i18n/es.json` `thumbnail.headline` (`**¿Manzanazo?**` -> `**¿Le dio?**`).
- [x] Verify `lint` and `render --thumbnails-only` for `curio-s25-v2`.

## How to verify

```bash
node tools/video/cli.mjs lint --slug curio-s25-v2
npm run check:tasks
```

## Notes

- Neither `video.json` nor `i18n/*.json` `lines` were touched, so `speech_hash` and all eight MiniMax dub tracks remain bound to the approved `4c9cdcae37` cut.
