---
id: 2026-09-25-add-backend-conventions-skill
title: Add the backend-conventions skill
status: done
priority: P2
area: tools
owner: claude-opus-5-5-backend-conventions
claimed_at: 2026-09-25T15:15:22Z
created_at: 2026-09-25T15:14:48Z
completed_at: 2026-09-25T15:24:04Z
branch: claude/skill-backend-conventions
depends_on: []
scope:
  - .agents/skills/backend-conventions
  - .claude/skills/backend-conventions
---

# Add the backend-conventions skill

## Why

The rules for writing an Alembic migration, for helpers that write on the caller's
session, and for adding an admin page or setting were spread across long docs, test
docstrings and personal notes. Each has cost a failed deploy or a page that was
forbidden in production (a jsonb operator on a json column, a revision id chained by
filename, an admin page registered only in the web fallback). A model starting such a
change had to re-derive them every time.

## Definition of done

- [x] `.agents/skills/backend-conventions/` holds a SKILL.md (rules, the two workflows,
      commands, a pointer table) and four references: migrations, migration tests,
      session helpers, admin pages and settings.
- [x] `.claude/skills/backend-conventions/SKILL.md` is a byte-identical copy.
- [x] Every path, symbol and command in it was checked against main.

## Steps

- [x] Verify the notes against the code: migration tree, `tests/test_schema.py`,
      `tests/test_migration_*.py`, `app/cli.py`, `NAVIGATION_REGISTRY`, the web and e2e
      navigation lists, `_admin_path_capability`, step-up scopes, settings ownership,
      `providerCategoryOf`, `tools/check-i18n.mjs`.
- [x] Write SKILL.md and the references; mirror SKILL.md.
- [x] `node --test tools/skills.test.mjs`.

## How to verify

```bash
node --test tools/skills.test.mjs
cd apps/api && uv run alembic heads   # the head the skill's workflow starts from
```

## Notes

- Out-of-date notes corrected while writing: `NAVIGATION_REGISTRY` still exists (API
  side); the page registration is four places, but the isolated e2e fixture pair
  (`tools/e2e-runtime-api.mjs` and `e2e/admin-operations.spec.ts`) only has to agree
  with itself, and today both leave out news and videos. `tests/test_schema.py` no
  longer pins the head, so a renumber does not touch it. New migrations (0083 on) use
  `op.get_context().as_sql` rather than `context.is_offline_mode()`. CI does run the
  PostgreSQL migration tests (`RUN_INTEGRATION_TESTS=1`); only a plain local run skips them.
- `admin-workspace-navigation.ts` is the in-page tab/URL-state adapter, not the
  sidebar registry.
- Unregistered `/admin/...` API paths behind `AdminUser` resolve to `roles.manage`
  (owner only) in `_admin_path_capability`; the skill says so.
- `met_norway` still has no `providerCategoryOf` entry and shows under 其他.
- `tasks/open/2026-09-12-test-warning-codes-allowlist-misses-its.md` looks fixed in
  code (`test_warning_codes.py` now uses `as_posix()`); left for whoever owns it.
