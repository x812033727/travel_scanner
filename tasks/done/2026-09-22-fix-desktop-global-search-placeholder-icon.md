---
id: 2026-09-22-fix-desktop-global-search-placeholder-icon
title: Fix desktop global search placeholder icon overlap
status: done
priority: P2
area: web
owner: codex-search-spacing
claimed_at: 2026-09-29T10:04:17Z
created_at: 2026-09-22T08:19:52Z
completed_at: 2026-09-29T10:10:26Z
branch: codex/site-search-spacing
depends_on: []
scope:
  - apps/web/components/site-search/site-search.tsx
  - apps/web/components/site-search/site-search.test.tsx
---

# Fix desktop global search placeholder icon overlap

## Why

At the desktop viewport, the global article search magnifier overlaps the start
of the placeholder. This was observed in all five languages during the batch015
published-article and batch016 private-page visual checks on 2026-09-22. It is a
shared header issue; the article body and private draft protection passed.

## Definition of done

- [x] The search icon and placeholder have clear separation in all five locales.
- [x] Typed search text and focus styles remain readable on desktop and mobile.

## Steps

- [x] Reproduce against the current header and inspect icon/input spacing.
- [x] Make the narrow layout correction and check existing search interactions.

## How to verify

Render the signed-out global header at 1440px and 390px in zh-TW, zh-CN, en,
ja and ko. Check the empty field, entered text and keyboard focus. Run scoped
web lint/type checking and the existing site-search tests if touched.

## Notes

Observed deployed revision: d5f03e679bef2102e843426c42f045aef4ae08c0.
Evidence: `C:/Users/x8120/.codex/article-localization-release/batch015/public-qa-after-publish-20260922T0808`
and `batch016-llms/privacy-after-import-20260922T0808` under the same release root.
The private-page visual receipt SHA256 is
`e30c223090b26b8f46a76b1325cab76d8b017c73c1fee81bee910e072e67cb6b`.
No shared header implementation was changed during those content releases.

### 2026-09-29 implementation and local browser verification

- Claimed from main `716bd5dc81cb2ebef51e338be5a2e6a201314226` after
  checking active task scopes, remote heads, worktrees and open PR files.
  The final pre-PR scan found no overlapping files among 13 open PRs.
- Root cause: the unlayered `.app-field` shorthand padding overrides the
  Tailwind layer's `pl-9` / `pl-11`, leaving only 13.6px before the text.
  Set this input's `paddingInlineStart` to 2.25rem inline / 2.75rem in the
  dialog and remove the ineffective start-padding classes. Shared CSS,
  search handlers, ARIA attributes and right padding remain unchanged.
- Chromium checked the actual signed-out header at 1440px and its search
  dialog at 390px, in zh-TW, zh-CN, en, ja and ko. Empty, keyboard-focused
  and typed states give 30 checks. The computed text-start/icon gap changed
  from -13.4px / -17.4px to 9px / 13px. Keyboard focus passed 20/20;
  no horizontal overflow, page/console errors, first-party HTTP failures
  or external requests occurred in the clean baseline and final runs.
- Existing `site-search.test.tsx` and `site-search-dialog.test.tsx`:
  13 passed, 0 skipped. Scoped ESLint and independent visual/code review
  passed. No test duplicating a CSS value was added.
- Full web `tsc --noEmit` passed. The first run encountered a malformed
  generated `.next/dev/types/routes.d.ts` with a duplicated tail. After
  stopping both task-owned local servers, archived that generated type
  directory outside the checkout and regenerated with `next typegen`;
  the final typecheck exited 0. Restored the original `next-env.d.ts`
  bytes; neither generated files nor local server changes enter the PR.
- `check:i18n` passed all five locales / 25 namespaces. `check:tasks`
  validated 1,131 files with existing stale-claim / overlap warnings.
  The completed task has no duplicate copy in `tasks/open`.
- Evidence stays outside the repository under
  `C:/Users/x8120/.codex/tmp/site-search-20260929/`.
  Clean baseline receipt SHA256:
  `8bcb57090e5f2b3eef6aa52e4459dc19a456303227d80693da116f69fb6446f0`.
  Final receipt SHA256:
  `9fd7018d9f962c00b32a1425928ff45f6bfda53874f2a0cf3844fc97faf00ae4`.
  Final component SHA256:
  `27217f7210f3da39f42a5d5f442d770d08347bab333f3734b3aec32ac7861f10`.
- These are local Next dev / synthetic API checks, not a production or
  release-build acceptance. The first baseline's missing fake-API
  community-status responses remain recorded; the clean/final harness
  supplies six false community flags. Clear-button visibility was checked,
  not its native click behavior; desktop dialog was outside this matrix.
