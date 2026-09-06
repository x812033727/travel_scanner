---
id: 2026-09-06-leftover-chinese-copy-on-the-search
title: Leftover Chinese copy on the search and trip pages outside the two components already converted
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T05:10:51Z
completed_at:
branch:
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
---

# Leftover Chinese copy on the search and trip pages outside the two components already converted

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

- [ ] `/en`, `/ja`, `/ko` search results, trip editor and account pages show no
      Traditional Chinese outside user data and place names.
- [ ] API error messages are never concatenated onto a translated sentence; the client
      shows its own message for known error codes.

## Steps

- [ ] Move the strings above into `search.json` / `trips.json` (keep the zh-TW values
      byte-identical so the existing tests keep passing; simple `{name}` params only).
- [ ] In saved-items-provider and price-alert-button, map known error codes to
      translated copy and drop the `：`/`，` concatenation with the API message.
- [ ] Re-run the walk: `document.querySelector('main').innerText` against
      `/[一-鿿]/` on the three pages in en and ko, minus data.

## How to verify

```bash
npm run lint:web && CI=1 npm run check:i18n && npm run typecheck:web && npm run test:web
```

## Notes

Found by claude-fable-5-1 while verifying #195 on production; filed rather than fixed
because it sits outside both tasks' scope.
