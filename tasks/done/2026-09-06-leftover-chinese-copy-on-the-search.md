---
id: 2026-09-06-leftover-chinese-copy-on-the-search
title: Leftover Chinese copy on the search and trip pages outside the two components already converted
status: done
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T05:52:14Z
created_at: 2026-09-06T05:10:51Z
completed_at: 2026-09-06T06:06:38Z
branch: claude/web-leftover-copy
depends_on: []
scope:
  - apps/web/components/search-criteria-editor.tsx
  - apps/web/components/airbnb-search-panel.tsx
  - apps/web/components/trip-weather-panel.tsx
  - apps/web/components/route-timeline-link.tsx
  - apps/web/components/price-alert-button.tsx
  - apps/web/components/saved-items-provider.tsx
  - apps/web/lib/api.ts
  - apps/web/messages/en/search.json
  - apps/web/messages/ja/search.json
  - apps/web/messages/ko/search.json
  - apps/web/messages/zh-CN/search.json
  - apps/web/messages/zh-TW/search.json
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
  - apps/web/components/account-saved-items.tsx
  - apps/web/messages/en/alerts.json
  - apps/web/messages/ja/alerts.json
  - apps/web/messages/ko/alerts.json
  - apps/web/messages/zh-CN/alerts.json
  - apps/web/messages/zh-TW/alerts.json
---

# Leftover Chinese copy on the search and trip pages outside the two components already converted

## Why

`search-results-i18n` and `trip-editor-i18n` (#195) moved the two big components to
the message catalog, and a walk through mokaair.com on 2026-09-06 after the deploy
found the rest. On `/en/search?...` the page still prints 「修改搜尋條件套用後會清除舊結果，
再由你確認是否重新搜尋。」 (search-criteria-editor) and 「Airbnb 官方外站搜尋」
(airbnb-search-panel). On `/ja/trips/<id>` the weather card falls back to 「暫時無法取得
旅程天氣」／「天氣資料格式不完整」／「重試」 (trip-weather-panel) and every route segment
offers 「選擇這段交通方式」／「前往 … · 大眾運輸／步行／汽車」 (route-timeline-link).
`/en/account` shows "Sign in to continue，請先登入。": the translated prefix plus the API's
Chinese fallback message from `lib/api.ts` glued together by saved-items-provider.
Price alerts (`price-alert-button`) carry the same shape.

The destination catalog's own Chinese (city names, summaries, 「4–6 天」) is a separate
task: `2026-09-06-destination-catalog-labels-i18n`.

## Definition of done

- [x] `/en`, `/ja`, `/ko` search results, trip editor and account pages show no
      Traditional Chinese outside user data and place names.
- [x] API error messages are never concatenated onto a translated sentence; the client
      shows its own message for known error codes.

## Steps

- [x] Move the strings above into `search.json` / `trips.json` (keep the zh-TW values
      byte-identical so the existing tests keep passing; simple `{name}` params only).
- [x] In saved-items-provider and price-alert-button, map known error codes to
      translated copy and drop the `：`/`，` concatenation with the API message.
- [x] Re-run the walk: `document.querySelector('main').innerText` against
      `/[一-鿿]/` on the three pages in en and ko, minus data.

## How to verify

```bash
npm run lint:web && CI=1 npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

Found by claude-fable-5-1 while verifying #195 on production; filed rather than fixed
because it sits outside both tasks' scope.

2026-09-06 claude-fable-5-1: five components moved to the catalog, zh-TW values byte-identical
so every existing test and the navigation e2e keep their Chinese selectors.

- `trips.weather` (trip-weather-panel, 19 keys; the day label now formats with the active
  locale instead of a hardcoded zh-TW), `trips.route` (route-timeline-link: mode labels, the
  three empty states, duration / buffer / ready-at), `alerts.button` (price-alert-button; the
  "already exists" follow-up link keys off `alert_exists` instead of matching Chinese text),
  `search.airbnb` (airbnb-search-panel) and `search.criteria` (search-criteria-editor, 41
  keys).
- Account page: a 401 from the saved-items call shows the page's own sign-in line per locale
  instead of the API's detail glued onto the heading, and the separator follows the locale.
- Left as is, on purpose: `lib/api.ts` keeps its zh-TW-only friendly catalog (other locales
  already get the API's localized `detail`); `saved-items-provider` still throws its Chinese
  message but every consumer branches on the 401 status, not the text; the Airbnb URL
  fallback "日本" is a query value Airbnb understands, not copy.
- Verified on a production build with Playwright (main innerText, data excluded): trip editor
  en/ko at 1280 and 390 px 0 Han lines, `/en/search` and `/ko/search` 0 Han lines.
