---
id: 2026-10-04-dedupe-intl-messageformat-to-one-major
title: Dedupe intl-messageformat to one major once next-intl accepts 12
status: blocked
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-10-04T01:12:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/package.json
  - package-lock.json
---

# Dedupe intl-messageformat to one major once next-intl accepts 12

## Why

Two majors of `intl-messageformat` are installed at once. Dependabot's #1164
(11.2.15 to 12.1.2) was merged on 2026-10-03 while it was meant to be on hold. The
lock could not move the whole tree, because `use-intl` (next-intl's runtime) depends
on `intl-messageformat ^11.1.0`. As of main 47933cdf:

| Copy | Version | Who uses it |
| --- | --- | --- |
| `node_modules/intl-messageformat` | 11.2.15 | next-intl/use-intl 4.14.8, and `tools/check-i18n.mjs` and its test, which resolve from the repository root |
| `apps/web/node_modules/intl-messageformat` | 12.1.2 | `apps/web/lib/ui-text.ts` and its test (`apps/web/package.json` pins `12.1.2`) |

So `npm run check:i18n` validates messages with 11, the app formats its admin-overridable UI
text with 12, and next-intl renders every other message with 11. Today the formatting is the
same: 12's only breaking change is requiring TypeScript 5.4 or newer, plus typed ICU
contracts, and both copies use `@formatjs/icu-messageformat-parser` 3.5.x. A future parser
change could make the check and the renderers disagree without any test noticing. This
is the same two-copies shape as `2026-09-14-typescript-7-upgrade`.

## Definition of done

- [ ] `package-lock.json` has exactly one `intl-messageformat` entry, and next-intl, `ui-text.ts`
      and `tools/check-i18n.mjs` all resolve that one copy.

## Steps

- [ ] Wait for a next-intl/use-intl release whose `dependencies` accept `intl-messageformat`
      12. Check with `npm view use-intl@latest dependencies`.
- [ ] Bump next-intl (and use-intl through it), then `npm install` and confirm the nested
      `apps/web/node_modules/intl-messageformat` entry is gone from the lock.
- [ ] If next-intl stays on 11 for long, the alternative is to pin `apps/web/package.json` back
      to `11.2.15` and add `intl-messageformat` to the major-version ignore list in
      `.github/dependabot.yml`. That needs the owner's agreement, since 12 is already on main.

## How to verify

```bash
node -e 'const l=require("./package-lock.json").packages; console.log(Object.keys(l).filter(k=>k.endsWith("/intl-messageformat")))'
# expect exactly ["node_modules/intl-messageformat"]
npm run check:i18n && npm run typecheck:web && npm run test:web && npm run test:tools
```

## Notes

- Blocked on upstream: `use-intl` 4.14.8 still declares `intl-messageformat ^11.1.0`.
- Review of #1164 before it merged: CI was green; no engines floor; the 12.0.0 changelog lists
  only the TypeScript 5.4 requirement and typed ICU contracts as breaking. The PR comment on
  x812033727/travel_scanner#1164 records the split.
