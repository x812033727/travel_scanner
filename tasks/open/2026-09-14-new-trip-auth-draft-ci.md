---
id: 2026-09-14-new-trip-auth-draft-ci
title: Preserve new trip draft on authentication rejection
status: review
priority: P1
area: web
owner: codex-pr468-ci
claimed_at: 2026-09-14T00:57:48Z
created_at: 2026-09-14T00:57:08Z
completed_at:
branch: codex/pr468-ci-fix
depends_on: []
scope:
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
---

# Preserve new trip draft on authentication rejection

## Why

PR #468's web job 103822764282 failed because the authentication-rejection test read a
null sessionStorage draft. A definitive rejection cleared the full draft after resetting
pending state. React batching can make that state change a no-op, so autosave never
recreates the deleted data. Persist the editable form synchronously without the rejected
attempt instead.

## Definition of done

- [x] Definitive 400/401/403/422/429 rejection preserves an editable draft on remount.
- [ ] Local checks and updated PR #468 CI pass.

## Steps

- [x] Reproduce the draft deletion with five regression cases before fixing the handler.
- [x] Replace deletion with synchronous preservation of form fields, retiring only pending.
- [ ] Push the focused fix to codex/travel-articles-batch5 and verify CI.

## How to verify

From apps/web: `npx vitest run components/new-trip-form.test.tsx` and `npx tsc --noEmit`.
From root: `npm run lint:web`, `npm run check:i18n`, `npm run test:web`, `npm run check:tasks`.

Local validation: 42 NewTripForm tests passed; TypeScript, ESLint, five-locale validation,
28 tooling tests and task validation passed. Full web suite pending at time of writing.

## Notes

The user explicitly confirmed PR #468 is the requested CI repair. The unrelated image
retry fix remains on codex/article-image-retry and is not part of this PR.
The original article worktree has a different local HEAD, so use this isolated checkout
and a normal fast-forward push to the PR branch. Do not merge or deploy.
