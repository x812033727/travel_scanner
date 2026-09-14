---
id: 2026-09-14-new-trip-auth-draft-ci
title: Repair PR 468 draft persistence and article content CI
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
  - apps/api/app/guides/content/backup-and-restore-home-files.json
  - apps/api/app/guides/content/browser-bookmark-project-folders.json
  - apps/api/app/guides/content/desk-cable-charging-organization.json
  - apps/api/app/guides/content/digital-receipt-archive.json
  - apps/api/app/guides/content/email-triage-three-actions.json
  - apps/api/app/guides/content/file-naming-system-for-home.json
  - apps/api/app/guides/content/gadget-purchase-needs-checklist.json
  - apps/api/app/guides/content/household-inventory-spreadsheet.json
  - apps/api/app/guides/content/meeting-notes-action-template.json
  - apps/api/app/guides/content/notification-focus-boundaries.json
  - apps/api/app/guides/content/phone-document-scanning-workflow.json
  - apps/api/app/guides/content/phone-photo-declutter-workflow.json
  - apps/api/app/guides/content/reading-notes-that-you-reuse.json
  - apps/api/app/guides/content/shared-household-calendar.json
  - apps/api/app/guides/content/weekly-review-reset-routine.json
---

# Repair PR 468 draft persistence and article content CI

## Why

PR #468's web job 103822764282 failed because the authentication-rejection test read a
null sessionStorage draft. A definitive rejection cleared the full draft after resetting
pending state. React batching can make that state change a no-op, so autosave never
recreates the deleted data. Persist the editable form synchronously without the rejected
attempt instead.

The rerun's API job 103825379292 additionally found that the 15 new lifestyle
articles have numbered SVG steps without those numbers in visible article text.
Add faithful step descriptions to their captions, preserving the content lint rules.
The user explicitly requested fixing PR #468, including these article files despite
the original article task's overlapping review scope.

## Definition of done

- [x] Definitive 400/401/403/422/429 rejection preserves an editable draft on remount.
- [x] Numbered lifestyle diagrams have corresponding visible step descriptions.
- [ ] Local checks and updated PR #468 CI pass.

## Steps

- [x] Reproduce the draft deletion with five regression cases before fixing the handler.
- [x] Replace deletion with synchronous preservation of form fields, retiring only pending.
- [x] Push the draft fix to codex/travel-articles-batch5; its full web CI passed.
- [ ] Push the caption correction and verify the final API CI rerun.

## How to verify

From apps/web: `npx vitest run components/new-trip-form.test.tsx` and `npx tsc --noEmit`.
From root: `npm run lint:web`, `npm run check:i18n`, `npm run test:web`, `npm run check:tasks`.

Local validation: 42 NewTripForm tests passed; TypeScript, ESLint, five-locale validation,
28 tooling tests and task validation passed. CI run 34794680669 passed the complete web
job, containers and full-stack smoke; its API job passed 4118 tests and failed only the
lifestyle diagram number lint. With the caption correction, the local content-pack and
pack-ingest tests pass: 29 passed, 5 PostgreSQL-only variants skipped. Caption step labels
and numbers were checked against each of the 15 SVGs before editing.

## Notes

The user explicitly confirmed PR #468 is the requested CI repair. The unrelated image
retry fix remains on codex/article-image-retry and is not part of this PR.
The original article worktree has a different local HEAD, so use this isolated checkout
and a normal fast-forward push to the PR branch. Do not merge or deploy.
