---
id: 2026-09-11-travel-guides-web
title: Travel guides web pages admin and navigation
status: review
priority: P1
area: web
owner: claude-opus-5-guides
claimed_at: 2026-09-11T13:09:17Z
created_at: 2026-09-11T13:09:13Z
completed_at:
branch: claude/travel-info-guide-section-4ulqsj
depends_on:
  - 2026-09-11-travel-guides-api
scope:
  - apps/web/app/[locale]/guides
  - apps/web/app/[locale]/admin/guides
  - apps/web/components/guides
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/site-page-content.tsx
  - apps/web/lib/site-pages.ts
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/components/guides-navigation.test.tsx
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/guides.server.ts
  - apps/web/lib/guides.server.test.ts
  - apps/web/lib/nav-links.ts
  - apps/web/lib/frontend-navigation.ts
  - apps/web/lib/admin-operations.ts
  - apps/web/components/site-navigation.tsx
  - apps/web/components/site-navigation.test.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/en/navigation.json
  - apps/web/messages/ja/navigation.json
  - apps/web/messages/ko/navigation.json
  - apps/web/messages/zh-TW/navigation.json
  - apps/web/messages/zh-CN/navigation.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-CN/metadata.json
---

# Travel guides web pages admin and navigation

## Why

`2026-09-11-travel-guides-api` gives the site a first-party article store with per-locale
publication. This is the half a reader and an editor actually touch: the public `/guides`
section, the authoring panel, and reaching both from every navigation mode.

## Definition of done

- [x] `/guides`, `/guides/{kind}` and `/guides/{kind}/{slug}` render server-side in five
      languages, with filters resolved for the URL the reader is on.
- [x] An article advertises hreflang only for the locales actually published, and a locale
      that was never written is `noindex` and says so.
- [x] An administrator with the `content` role can create, draft, preview, publish,
      withdraw and restore from `/admin/guides`.
- [x] The section is reachable from the header in all three navigation modes.
- [x] The block renderer and its link sanitizer are shared with the managed site documents
      rather than copied.

## Steps

- [x] `lib/content-blocks.ts` + `components/content-blocks.tsx`, with `lib/site-pages.ts`
      and `components/site-page-content.tsx` delegating to them.
- [x] `lib/guides.ts` (types, guards, `guideHref`, `isExpired`) and `lib/guides.server.ts`.
- [x] `components/guides/{card,filters,article}.tsx` and the three public pages.
- [x] `components/admin-guides-panel.tsx` and `/admin/guides`, plus the admin nav entry.
- [x] `primaryNavLinks`, the desktop header, the phone header and `frontendActive`.
- [x] Copy in five locales: reader copy in `common.json → guides`, panel copy in
      `admin.json → guides`, page title in `metadata.json`, nav label in `navigation.json`.
- [x] Tests for the lib, both page types, the renderer, the panel and the navigation modes.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web
npm run test:web        # 225 files / 2,218 cases pass
npm run build:web       # /[locale]/guides, /guides/[kind], /guides/[kind]/[slug], /admin/guides
```

## Notes

**Declared scope overlaps, all against merged work.** `claim` refused three paths, and each
holder turned out to be stale bookkeeping rather than live work:

- `messages/*/metadata.json` — held by `2026-09-10-seo-destination-landing-pages`, whose
  branch `claude/seo-optimization-planning-xq1vjl` merged as PR #388 on 2026-09-11.
- `messages/*/admin.json` — held by `2026-09-11-food-reservation-platforms`, whose branch
  merged as PR #392; `19a9429` is an ancestor of this branch.

Seven other `2026-09-10-seo-*` tasks and the food one are all `review` on merged branches.
They should be moved to `done`; this session was not permitted to run `tasks -- done` on
another owner's task, so they are left as they are and recorded here instead.

**Decisions worth keeping:**

- Reader copy went to `common.json → guides` rather than a new `guides.json` namespace: a
  new namespace is a six-file change that includes `admin.json`, and `common.json` already
  groups feature copy in nested objects (`placePicker`, `cardActions`). Panel copy did go to
  `admin.json → guides`, where every other admin panel's copy lives.
- `[kind]` is a dynamic segment with two literal values so only the hub needs
  `metadata.json` keys (`app/[locale]/metadata.test.ts:47` skips `[`-prefixed directories).
  The cost is that `kind` must never change once a locale is published, which the API
  enforces by keeping it in the URL.
- The header link sits outside the three navigation-mode branches. Adding it to
  `primaryNavLinks` alone reproduces `2026-09-11-no-sign-in-entry-in-discovery`.
- The bottom tab bar stays at four tabs in discovery mode; `/guides` was added to the
  explore prefix list in `frontendActive` instead.
- Publish and restore now have separate reason fields. Sharing one piece of state gave two
  inputs the same visible label and let a reason typed for one action be recorded for the
  other.
- `react-hooks/set-state-in-effect` rejects a synchronous `setState` at the top of an
  effect. Selection changes are event-driven, so the loading/empty reset lives in the
  handler and the effect only fetches.

**Not done:** `apps/web/app/sitemap.ts` (held by `2026-09-10-seo-robots-sitemap` and
`2026-09-11-pr388-seo-review`; the API already serves `GET /guides/sitemap` for it),
`components/site-footer.tsx`, the destination-page cross-link, and relabelling discovery's
`kinds.article` off 攻略 in `lib/discovery-copy.ts`.
