---
id: 2026-10-05-show-video-worker-handoff-state
title: Show video worker handoff state for unfinished projects
status: in-progress
priority: P1
area: web
owner: codex-video-handoff-state
claimed_at: 2026-10-05T10:27:46Z
created_at: 2026-10-05T10:27:19Z
completed_at:
branch: codex/news-video-stall-fixes-20261005
depends_on: []
scope:
  - apps/api/app/video_reviews/producer_state.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_producer_state.py
  - apps/web/components/admin-video-production-state.tsx
  - apps/web/components/admin-video-production-state.test.tsx
  - apps/web/components/admin-video-browser.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
---

# Show video worker handoff state for unfinished projects

## Why

An approved final can come from an external or isolated producer whose work is not
registered in the main worker's volume. The page reports missing language results but
does not show that the main worker has never taken over. A saved active job also does
not establish that a worker process is running. Keep output readiness, review approval,
YouTube publication, and the observed producer registration separate.

## Definition of done

- [x] Unfinished non-Shorts show whether the main worker has registered them, is blocked,
  has a STOP marker, or has recorded completion/drop; an unreadable mount/state is unknown.
- [x] Missing registration points the owner to the original production workflow and
  approved media, without automatically adopting, regenerating, or retrying a video.
- [x] The catalog and detail show consistent evidence while existing language results,
  ready-to-upload rules, approval records, and YouTube identity remain unchanged.
- [x] A completed Traditional-Chinese-only upload, ready-to-upload video, dropped video,
  or Short does not get a misleading missing-handoff notice.
- [x] Five-language copy and focused API/web regression checks pass.

## Steps

- [x] Verify active task/PR scopes and the original approved-final runner before changing code.
- [x] Add a bounded read-only observer for canonical worker state; expose it in list/browse/detail.
- [x] Add producer evidence alongside the existing output/publication pills and five-language help.
- [x] Cover read-only behavior, invalid/oversized state, path escapes, independent Shorts,
  partial language results, completed uploads, older APIs, and catalog/detail behavior.

## How to verify

From the repository root:

```powershell
npm run check:i18n
npm run lint:web
npm run typecheck:web
npm run test:web -- components/admin-video-production-state.test.tsx components/admin-video-reviews.test.tsx
```

From `apps/api`:

```powershell
uv run --no-sync ruff check app/video_reviews/producer_state.py app/video_reviews/schemas.py app/video_reviews/admin_service.py tests/test_video_producer_state.py
uv run --no-sync mypy app/video_reviews/producer_state.py app/video_reviews/schemas.py app/video_reviews/admin_service.py tests/test_video_producer_state.py
uv run --no-sync pytest tests/test_video_producer_state.py tests/test_video_reviews.py -q
```

Focused results on 2026-10-05: web 71 tests passed; API 62 passed, two symlink tests
skipped because this Windows session cannot create symlinks (they run on Linux CI);
mypy, ruff, full web lint, typecheck and five-locale/25-namespace i18n validation passed.

## Notes

- Main `auto` only enumerates directories with `auto.json`. A database report or a
  final review does not enqueue a video, and a missing worker-local MP4 does not prove
  review-store/external media is missing. The observer never touches media or work state.
- `registered` deliberately makes no process-liveness claim. `done` describes only the
  main worker's persisted workflow and cannot satisfy newly selected language outputs.
- The API already mounts `video_work` read-only. Missing configuration/mount, malformed
  JSON, oversize state, wrong slug/status, or an escaping resolved path yield `unavailable`.
- The original approved-final recovery runner is maintained by
  `2026-09-29-resume-imported-long-video-languages` and
  `2026-10-01-hand-off-owner-approved-renewed-finals` in worktree e82d. Its source/hash
  checks, STOP markers, locks, payment receipts and per-project progress remain intact.
  This change does not restart that producer or bypass its preflight/owner handoff.
- PR #1268 owns `admin-video-reviews.tsx`; this task leaves that file untouched and adds
  new message keys. Existing published/ready states and review truth are preserved.
- No production write, generation, paid retry, upload, publication, or deployment occurred.
- Independent review identified that a project symlink within the work base could falsely
  look registered, although the real worker excludes symlinks via `Dirent.isDirectory()`.
  The observer now checks the directory entry with `lstat` and `is_junction` before
  resolving it and returns `unavailable` for a project symlink or Windows junction.
  A source-bound within-base symlink regression runs on Linux CI and skips only when
  the local platform cannot create directory symlinks. A Windows-only NTFS junction
  regression creates a real within-base junction without requiring administrator access.
  The real NTFS junction regression passed locally; ruff, mypy and the focused API
  suite were rerun after the review fix.
