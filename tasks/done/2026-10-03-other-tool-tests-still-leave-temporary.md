---
id: 2026-10-03-other-tool-tests-still-leave-temporary
title: Other tool tests still leave temporary directories in TEMP
status: done
priority: P3
area: tools
owner: claude-opus-5-5-tts-ni-tempdirs
claimed_at: 2026-10-04T14:55:27Z
created_at: 2026-10-03T12:32:25Z
completed_at: 2026-10-04T15:32:24Z
branch: claude/tts-ni-variant-and-test-tempdirs
depends_on:
  - 2026-10-03-video-tool-tests-leave-a-sandbox
scope:
  - tools/tasks.test.mjs
  - tools/ci-auto-update.test.mjs
  - tools/video/core/paths.test.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/media/series-store.test.mjs
  - tools/video/tts/tts.test.mjs
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
| `video-home-` | 63 (some from media.test.mjs, fixed) | `tools/video/tts/tts.test.mjs:231` |
| `video-thumbs-` | 47 | `tools/video/package/package.test.mjs:332` |
| `video-qa-thumbs-` | 46 | `tools/video/qa/thumbnail.test.mjs:81` |
| `auto-update-` | 41 | `tools/ci-auto-update.test.mjs:159` |
| `anime-acts-test-` | 40 | `tools/video/automation/anime-write.test.mjs:12` |

## Definition of done

- [ ] One full `npm run test:tools` leaves no new directory with any of the prefixes above.

## Steps

- [x] Under `tools/video/`: make the directory with `tempDir(prefix)` from
      `tools/video/core/fixtures/load.mjs`, which removes it when the test process exits
      (`VIDEO_KEEP_SANDBOX=1` keeps it). All but `package.test.mjs`; see Notes.
- [x] `tools/tasks.test.mjs` and `tools/ci-auto-update.test.mjs` are not video tests: a
      `t.after(() => rmSync(dir, { recursive: true, force: true }))` in the test is enough.
- [x] Look for other `mkdtempSync` calls in `tools/**/*.test.mjs` without a matching removal.

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
- Measured on 2026-10-04 with the sandbox fix in place: `node --test "tools/video/**/*.test.mjs"`
  with `TEMP`/`TMP` pointed at an empty directory leaves 31 directories, 422 KB in all:
  `video-series-image-store-` 9, `video-atomic-` 8, `video-image-stage-` 7, `anime-acts-test-` 4,
  and one each of `video-home-`, `video-qa-thumbs-` and `video-thumbs-`. The other
  `mkdtempSync` callers under `tools/video` (`branding-*`, `shorts-*`, `renewal-*`, `story-plan-`,
  `dub-words-`, `screencast-`, `video-import-`, `anime-input-`, `admin-catalog-*`,
  `video-localization-retention-`, `video-branding-`) left nothing in that run. `tasks-` and
  `auto-update-` come from `tools/*.test.mjs` and were not in it.
- 2026-10-04 (claude-opus-5-5-tts-ni-tempdirs): claimed with `--force` over three overlaps, none
  live: `2026-10-03-illustrated-slides-round-2-a-family` and
  `2026-10-03-illustrated-slides-lint-heuristics-the-shorts` (claude-fable-5-1-illustration-round2,
  `review` since 2026-10-03T08:25Z, more than a day; their branch landed as #1172) on
  `media/stages.test.mjs`, and `2026-10-03-video-worker-narration-takes-made-stale`
  (claude-opus-5-5, no branch) on `tts/tts.test.mjs`, whose code landed as #1182 (cf9e04ead) and
  whose one unticked item is a check on the production host after a deploy.
- `tools/video/package/package.test.mjs` came out of the scope, so `video-thumbs-` is the one
  prefix left: `2026-10-01-hand-off-owner-approved-renewed-finals`
  (codex-video-stall-followthrough) claimed that file at 2026-10-04T10:14Z, less than a day
  before, and its package work has not landed (#1208 merged its other parts without touching
  `package.test.mjs`). The one-line change is filed as `2026-10-04-package-test-leaves-a-video-thumbs`;
  the Definition of done stays unticked for that prefix alone.
- What changed: `paths`, `stages`, `series-store`, `tts`, `qa/thumbnail` and `anime-write` tests
  make their directory with `tempDir(prefix)` and drop the unused `mkdtempSync`/`tmpdir` imports;
  `tasks.test.mjs`'s `workspace(t)` and the one `ci-auto-update` test remove theirs in `t.after`.
  Every other `mkdtemp` caller among the files `npm run test:tools` runs already removes its
  directory (`t.after` or `try`/`finally`), so nothing else was added to the scope.
- Measured with `TEMP`/`TMP` pointed at an empty directory under the scratch dir. Before, as on
  origin/main a266a5bba, the 34 test files that call `mkdtemp` left 46 directories:
  `tasks-` 14, `video-series-image-store-` 9, `video-atomic-` 8, `video-image-stage-` 7,
  `anime-acts-test-` 4, and one each of `auto-update-`, `video-home-`, `video-qa-thumbs-` and
  `video-thumbs-`. After, one full `npm run test:tools` (1,560 tests) left two entries:
  `video-thumbs-` 1 (above) and `node-compile-cache`, Node's own module compile cache, which keeps
  one fixed name and is reused rather than added to on each run.
- A TEMP path this long (about 170 characters) breaks tests that build deep trees in it:
  `tools/dots-series.test.mjs` (WinError 206) and six `tools/video/compile/compile.test.mjs` tests
  (ENOENT on `mkdtemp`) failed in that run and pass with the normal `TEMP`. Measure with a short
  empty directory such as `C:\t` next time.
- `tools/video/automation/anime-write.test.mjs` and `tools/video/tts/tts.test.mjs` are bound in
  `docs/videos/long-form/review.json`: the PR is a draft until an independent reviewer adds the
  duration-receipt increment.
