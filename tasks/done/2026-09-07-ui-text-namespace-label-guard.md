---
id: 2026-09-07-ui-text-namespace-label-guard
title: check-i18n does not guard the ui-text editor's own namespace labels
status: done
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T07:57:53Z
created_at: 2026-09-07T06:51:48Z
completed_at: 2026-09-07T07:59:19Z
branch:
depends_on: []
scope:
  - tools/check-i18n.mjs
  - docs/ui-text-overrides.md
---

# check-i18n does not guard the ui-text editor's own namespace labels

## Why

Filed after this session duplicated `2026-09-07-ui-text-admin-editor`: the guard and a
doc section were the only parts of the discarded work that did not overlap with the
editor that shipped (#323).

**Half of it was already there.** #323 added the same check against `locales[0]`, and
`check-i18n` already requires every locale's key set to match `en`, so one locale's copy
is enough — a second per-locale loop would only restate it. Nothing to add.

**The doc was the real gap.** `docs/ui-text-overrides.md` is titled "Editing the site's
copy from the admin panel" and described the table, the API, the cache and the merge, but
never the screen: not where it is, not what the query string carries, not that an empty
box is how you restore a default.

## Definition of done

- [x] `check:i18n` fails when a namespace has no label in the editor's picker — already
      true via #323 plus the existing key-parity check; verified, nothing added.
- [x] `docs/ui-text-overrides.md` describes the editor screen.

## How to verify

Read `## The editor` against `apps/web/components/admin-ui-text-panel.tsx` and
`apps/web/app/[locale]/admin/ui-text/page.tsx`. Every claim in it was checked against
that code: the three query parameters and their silent fallback, the server-side catalog
load, `row.shown.trim() === "" ? null : row.shown`, `chunk(entries, UI_TEXT_BATCH_LIMIT)`,
the reload-and-trim on failure, and `PAGE_SIZE = 50`.

## Notes

`git branch --list` shows a sibling worktree's branch with a leading `+` before it is ever
pushed. `git branch -r` and `gh pr list` do not, which is how the duplication happened.
See [[travel-scanner-parallel-session-overlap]].
