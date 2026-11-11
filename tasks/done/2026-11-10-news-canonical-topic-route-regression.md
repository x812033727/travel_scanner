---
id: 2026-11-10-news-canonical-topic-route-regression
title: Verify canonical topic links in the legacy article route
status: done
priority: P1
area: web
owner: codex-news-ci-fix
claimed_at: 2026-11-10T13:47:40Z
created_at: 2026-11-10T13:47:00Z
completed_at: 2026-11-10T13:54:06Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - apps/web/app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
---

# Verify canonical topic links in the legacy article route

## Why

PR #2061 now sends article topic links to the canonical topic hub. The legacy
article-route test still expects its footer to use a kind-specific query URL,
so CI fails although the new navigation is intentional.

## Definition of done

- [x] The route test independently verifies the breadcrumb and tracked footer link use the canonical topic hub.
- [x] Focused route tests, scoped lint and task validation pass in this worktree.
- [x] Root and an independent reviewer inspect the minimal change before it is committed or pushed.

## Steps

- [x] Retain the exact failing CI log and audit the route-test scope before claiming it.
- [x] Update the assertion without removing footer coverage.
- [x] Run checks and record the independent review outcome.

## How to verify

From apps/web, run Vitest for app/(ads-public)/[locale]/guides/[kind]/[slug]/page.test.tsx
and ESLint for that exact file. From the repository root, run node tools/tasks.mjs check.
Use this worktree's own npm ci and bundled Node v24.22.1.

## Notes

- Exact failing head: e0f2516806ad3d580e2b5d7da10ec3ff3b89d948; CI run 42825796014,
  web-unit (3/3) job 129862638208. The shard had 1 failed and 1,393 passed tests.
- Full failure log and scope audit are retained under
  <home>/.codex/tmp/mokaair-news-upgrade-20261110/.
- Scope audit found no active task or other open PR owning this exact route test.
- Runtime code, production, and the separate discovery worktree are outside this fix.
- Own-worktree npm ci passed with bundled Node v24.22.1; focused route Vitest passed
  all 24 tests (39.56 seconds, exit 0). Scoped ESLint and task validation also passed.
- Independent reviewer codex-layout-review found no blockers at route-test SHA-256
  253449f7ea2c070535fadee61fb8cf6515852c92c6d71c68759f34fd1728d25f;
  review receipt: <home>/.codex/tmp/mokaair-news-upgrade-20261110/canonical-topic-ci-independent-review.md.
- Root also reviewed the +8/-4 assertion diff and accepted it after the focused checks;
  root will stage and commit this fix with the separately reviewed API test-isolation fix.
