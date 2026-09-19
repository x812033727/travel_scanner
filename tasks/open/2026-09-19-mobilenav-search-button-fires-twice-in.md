---
id: 2026-09-19-mobilenav-search-button-fires-twice-in
title: MobileNav search button fires twice in discovery mode
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-19T14:14:09Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
---

# MobileNav search button fires twice in discovery mode

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

## Why

`npm run test:web` fails on main. Found while working on the indexing fixes
(2026-09-19-home-page-renders-as-a-skeleton); nothing in that work touches this component.

```
FAIL components/mobile-nav.test.tsx > MobileNav > opens the article search from the header row (discovery: true)
AssertionError: expected "vi.fn()" to be called 1 times, but got 2 times
 -> components/mobile-nav.test.tsx:42
```

Deterministic: three isolated runs of `npx vitest run components/mobile-nav.test.tsx`
all gave `1 failed | 12 passed`. One `fireEvent.click` on the "開啟搜尋" button calls
`search.open` twice. The run also logs `An update to ThemeProvider inside a test was not
wrapped in act(...)`, which may or may not be the same cause.

Both `components/mobile-nav.tsx` and its test are untouched by the indexing branch
(`git status` confirms), so this is either already on main or arrived with a recent merge.

## Definition of done

- [ ] `npx vitest run components/mobile-nav.test.tsx` is green
- [ ] the cause is named: a doubled handler, a duplicated listener, or a test that clicks a
      nested button as well as its parent
- [ ] `npm run test:web` has no failures other than the `qrcode` module resolution one

## Notes

Unrelated second failure in the same run: `components/shared-trip-view.test.tsx` cannot
resolve `qrcode`. That is an install gap, not a code bug -- `qrcode` and `@types/qrcode` are
both declared in `apps/web/package.json`, but the shared `node_modules` this worktree
resolves through (`C:/Users/x8120/mokaair/node_modules`, 396 packages) does not carry it.
A clean `npm ci` fixes it; no repository change needed.
