---
id: 2026-09-12-shared-trip-partner-cta
title: Partner call-to-action on the shared trip page behind a share placement
status: done
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-12T13:27:22Z
created_at: 2026-09-12T13:27:21Z
completed_at: 2026-09-19T04:11:45Z
branch: claude/trip-partner-offers
depends_on:
  - 2026-09-12-trip-partner-cta
scope:
  - apps/web/lib/hotel-booking-placement.ts
  - apps/web/components/shared-trip-view.tsx
  - apps/web/components/shared-trip-view.test.tsx
  - apps/web/components/travel-services/admin.tsx
  - apps/web/components/travel-services/admin.test.tsx
---

# Partner call-to-action on the shared trip page behind a share placement

## Why

`/share/{token}` is the only planning surface a visitor sees without signing in, and it
ended with no partner entrance. It is also a different audience from the owner, so it gets
its own switch rather than inheriting the trip surface.

## Definition of done

- [x] The shared trip page mounts the destination-offer panel with `placement="share"` when
      the share payload says a module is ready; otherwise it makes no partner request.
- [x] `share` is a third content-surface checkbox in Release controls, off by default.

## Steps

- [x] `hotel-booking-placement.ts`, `shared-trip-view.tsx`, `travel-services/admin.tsx`, tests.

## How to verify

```
cd apps/web && npx vitest run components/shared-trip-view.test.tsx components/travel-services/admin.test.tsx
```

Then: enable `share` in Release controls, open a share link for a city with approved offers.

## Notes

The `qrcode` dependency this page imports must be installed locally (`npm ci` at the repo
root) or its test and `tsc` fail to resolve the module.

### 標記完成（由站主授權，非原持有者，2026-09-19）

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

完成條件 3／3 都已打勾，工作隨 PR #436 於 2026-09-12 合併，之後部署過多次。原持有者 claude-fable-5-1 的認領從 2026-09-12 起沒有更新，這張票的 scope 擋住 1 張票。
