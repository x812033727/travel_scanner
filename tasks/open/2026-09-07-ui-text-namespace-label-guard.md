---
id: 2026-09-07-ui-text-namespace-label-guard
title: check-i18n does not guard the ui-text editor's own namespace labels
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-07T06:51:48Z
completed_at:
branch:
depends_on: []
scope:
  - tools/check-i18n.mjs
  - docs/ui-text-overrides.md
---

# check-i18n does not guard the ui-text editor's own namespace labels

## Why

`/admin/ui-text` labels each namespace by hand in `admin.uiText.namespaces`. Adding a
namespace to the editable allowlist without adding a label there makes the picker show
its raw key — in all five locales at once, with nothing failing.

`tools/check-i18n.mjs` already cross-checks the allowlist in `apps/api/app/ui_text/schemas.py`
and `apps/web/lib/ui-text.ts` against the catalog directory. This is the third list that
has to agree and the only one nothing checks.

Blocked until the editor is on main (`claude/ui-text-admin-editor`), because the guard
reads `uiText.namespaces` out of `admin.json`.

## Definition of done

- [ ] `npm run check:i18n` fails when a locale's `uiText.namespaces` is missing an
      editable namespace, or carries one that is not editable.
- [ ] `docs/ui-text-overrides.md` describes the editor screen.

## How to verify

Delete one entry from `apps/web/messages/ja/admin.json`'s `uiText.namespaces`, run
`npm run check:i18n`, and see it named. (Restore with git afterwards — but note the
file is not in HEAD until the editor lands, so save a copy first.)

## Notes

Written and verified once already, then dropped along with a duplicate editor: this
session and another built `/admin/ui-text` at the same time, and the other one is the
better implementation. The guard and the doc section are the parts that did not
duplicate anything. The patch is 102 lines and adds, after the `allowlists` loop:

```js
// The editor's namespace picker labels each namespace by hand. A namespace added to the
// allowlist without a label would show its raw key there, in every locale at once.
for (const locale of locales) {
  const labels = JSON.parse(
    readFileSync(join(root, "apps/web/messages", locale, "admin.json"), "utf8"),
  ).uiText?.namespaces;
  const missing = editable.filter((name) => !labels || !(name in labels));
  const extra = Object.keys(labels || {}).filter((name) => !editable.includes(name));
  if (missing.length || extra.length) {
    errors.push(
      `apps/web/messages/${locale}/admin.json: uiText.namespaces does not match the editable ` +
        `namespaces (missing: ${missing.join(", ") || "none"}; extra: ${extra.join(", ") || "none"})`,
    );
  }
}
```

Two lessons for whoever reads this next: an unclaimed P2 on the board is not evidence
nobody is on it — `git branch --list` in the shared checkout shows sibling worktrees'
branches before they are pushed, and `git worktree list` shows who is where. Check both,
not just `git branch -r` and `gh pr list`. See [[travel-scanner-parallel-session-overlap]].
