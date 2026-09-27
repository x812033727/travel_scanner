---
id: 2026-09-27-video-drama-settings-ux
title: Video admin: drama settings live on the drama tab with their own save, and a greyed save says which permission is missing
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-drama-ux
claimed_at: 2026-09-27T05:10:51Z
created_at: 2026-09-27T05:10:49Z
completed_at: 2026-09-27T06:00:42Z
branch: claude/video-drama-settings-ux
depends_on: []
scope:
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/components/admin-video-drama-settings.tsx
  - apps/web/components/admin-video-drama-settings.test.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-settings-permission.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
---

# Video admin: drama settings live on the drama tab with their own save, and a greyed save says which permission is missing

## Why

The owner reported on 2026-09-27 that the drama settings on `/admin/videos` could not be
saved, and that the video admin was hard to use and to manage. The save button was grey.
The settings tab is guarded by `settings.manage`, while everything else on `/admin/videos`
(reviews, series, filing a drama) needs only `content.manage`. An account with the
`content` role could therefore run and review dramas but never change their settings, and
the page only said that the manage-settings permission was needed, never which role that
is or who grants it. The code path is correct for an account in `ADMIN_EMAILS`, which gets
the `owner` role and every capability.

Three more things made the area hard to use. The drama settings sat at the bottom of the
settings tab, after every tutorial setting, so drama was run from one tab and configured
from another. One save sent the whole page, so any invalid tutorial field also blocked the
drama settings. And the drama tab never said that the route was off: the worker makes
nothing while `drama_enabled` is false (the API's two job endpoints, the media jobs and
`tools/video/automation/series.mjs` all check it), so a filed episode waited forever
without a word.

## Definition of done

- [x] A read-only settings form names the roles the signed-in account holds and how to get
      the missing one, in the words of the members page.
- [x] The drama settings live on the drama tab with their own save. A save replaces only the
      drama block of the settings the API holds at that moment.
- [x] The settings tab no longer sends the drama block, so neither tab can block or
      overwrite the other.
- [x] Turning the route on with a media vendor that has no key warns before saving.
- [x] The drama tab says whether the route is on, and opens its settings while it is off.
- [x] One-off episodes that wait for the owner come first, and a stopped one is marked.
- [x] The permission rules are unchanged: the owner chose on 2026-09-27 to keep
      `settings.manage` for these settings and to fix the account's role instead.

## Steps

- [x] `SettingsPermissionNotice` and `dramaSaveBody` in `admin-video-settings.tsx`, whose
      `saveBody` now leaves the drama block out.
- [x] `admin-video-drama-settings.tsx`: the drama form moved out of the settings tab, with
      its own save and the missing-key warning.
- [x] `admin-video-series.tsx`: the on/off banner, the drama settings read once, and the
      one-off episodes ordered by what needs the owner.
- [x] Twelve strings in each of the five locales.
- [x] Component tests, each checked by removing its fix and watching it fail.

## How to verify

```bash
npm run check:i18n
npm run lint:web && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-settings.test.tsx components/admin-video-drama-settings.test.tsx components/admin-video-series.test.tsx components/admin-video-reviews.test.tsx
```

On the site, as an account with only the `content` role, open the settings tab of
`/admin/videos`: the notice names the role and the fix. Open the drama tab: it says the
route is off and shows the drama settings open.

## Notes

- The settings are read once on the drama tab, not with its 60-second refresh
  (`REFRESH_MS`): a re-read would throw away what the owner is typing.
- The pointer from the settings tab to the drama tab is a button that calls
  `adminNavigate`. The tab state (`useAdminQueryState`) listens for `popstate`,
  `hashchange` and `admin:location-change` only, so a plain link would change the address
  and leave the settings tab on screen. The test asserts the event.
- Role names come from `lib/admin-users-copy.ts` and the members page name from
  `admin.navigation.users` (「會員與次數」), so the notice uses the words the owner sees.
- The Korean strings quote placeholders with `‘…’`. An ASCII apostrophe before `{` is ICU
  quoting and prints the placeholder literally; three older Korean strings already do
  that, filed as `2026-09-27-korean-placeholders-escaped-by-apostrophes`.
- The web typecheck failed at first on `qrcode` because this worktree's `node_modules` was
  older than the lockfile; `npm ci` fixed it.
- No admin override keys were renamed: every string is a new key, and the existing
  `videoSettings.readOnly` stays as the notice's first line.
