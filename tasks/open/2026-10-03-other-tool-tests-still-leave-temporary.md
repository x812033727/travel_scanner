---
id: 2026-10-03-other-tool-tests-still-leave-temporary
title: Other tool tests still leave temporary directories in TEMP
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-03T12:32:25Z
completed_at:
branch:
depends_on:
  - 2026-10-03-video-tool-tests-leave-a-sandbox
scope:
  - tools/tasks.test.mjs
  - tools/ci-auto-update.test.mjs
  - tools/video/core/paths.test.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/media/series-store.test.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/package/package.test.mjs
  - tools/video/qa/thumbnail.test.mjs
  - tools/video/automation/anime-write.test.mjs
---

# Other tool tests still leave temporary directories in TEMP

## Why

`npm run test:tools` used to leave tens of thousands of directories in the system's temporary
directory; the big ones (`video-core-*`, `video-tidy-*`, `video-media-*`) are removed at process
exit since `2026-10-03-video-tool-tests-leave-a-sandbox`. Smaller piles with the same cause
remain: a test makes a directory with `mkdtempSync(tmpdir(), ...)` and never removes it. On the
owner's machine on 2026-10-03 `%TEMP%` held, from these tests:

| Prefix | Directories | Made by |
| --- | --- | --- |
| `tasks-` | 588 | `tools/tasks.test.mjs:12` |
| `video-image-stage-` | 412 | `tools/video/media/stages.test.mjs:120` |
| `video-series-image-store-` | 387 | `tools/video/media/series-store.test.mjs:18` |
| `video-atomic-` | 352 | `tools/video/core/paths.test.mjs:11` |
| `video-home-` | 63 (some from media.test.mjs, fixed) | `tools/video/tts/tts.test.mjs:230` |
| `video-thumbs-` | 47 | `tools/video/package/package.test.mjs:332` |
| `video-qa-thumbs-` | 46 | `tools/video/qa/thumbnail.test.mjs:81` |
| `auto-update-` | 41 | `tools/ci-auto-update.test.mjs:159` |
| `anime-acts-test-` | 40 | `tools/video/automation/anime-write.test.mjs:12` |

## Definition of done

- [ ] One full `npm run test:tools` leaves no new directory with any of the prefixes above.

## Steps

- [ ] Under `tools/video/`: make the directory with `tempDir(prefix)` from
      `tools/video/core/fixtures/load.mjs`, which removes it when the test process exits
      (`VIDEO_KEEP_SANDBOX=1` keeps it).
- [ ] `tools/tasks.test.mjs` and `tools/ci-auto-update.test.mjs` are not video tests: a
      `t.after(() => rmSync(dir, { recursive: true, force: true }))` in the test is enough.
- [ ] Look for other `mkdtempSync` calls in `tools/**/*.test.mjs` without a matching removal.

## How to verify

```bash
ls -d "$TEMP"/{tasks,video-image-stage,video-series-image-store,video-atomic,video-home,video-thumbs,video-qa-thumbs,auto-update,anime-acts-test}-* | wc -l
npm run test:tools
# the same count again: no new names
```

## Notes

- `tools/video/automation/anime-write.test.mjs`, `tools/video/package/package.test.mjs` and
  `tools/video/tts/tts.test.mjs` are bound by SHA-256 in `docs/videos/long-form/review.json`;
  changing them needs a duration-receipt increment like any other bound file, or the main smoke
  turns red.
- Not from `test:tools`, so not in scope here: `character-look-offline-fixture-*`,
  `source1-normal-synthetic-*`, `sothatswhy-completion-negative-*`,
  `receipt-v4-signature-tests-*` (none of these names appear under `tools/`).
