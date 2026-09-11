---
id: 2026-09-11-merchant-coordinate-queue-i18n
title: 店家座標佇列面板整個沒有 i18n
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-11T18:24:45Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-merchant-coordinate-queue.tsx
---

# 店家座標佇列面板整個沒有 i18n

## Why

`admin-merchant-coordinate-queue.tsx` 完全沒有 `useTranslations`，整個面板的文字都是寫死的繁體中文：欄名（`COLUMNS`）、「Google Places 金鑰未設定，無法解析候選。」、按鈕與狀態文字。

做 `2026-09-11-admin-tables-unusable-on-phone` 時發現的：要給每個 `<td>` 補欄名，只能直接引用那四個中文字串。當時把它們抽成一個 `COLUMNS` 常數讓 `<th>` 與 `data-label` 共用，避免把同樣的漢字再寫一次（`tools/check-i18n.mjs` 的漢字增量守門會擋），但面板本身仍然只有中文。

## Definition of done

- [ ] 面板沒有寫死的使用者可見中文。
- [ ] 五語系 catalog 齊全，`npm run check:i18n` 通過。

## Steps

- [ ] 字串搬進 `messages/*/admin.json`（照其他後台面板的做法，例如 `hotspotPlacesPanel.*`）。
- [ ] `COLUMNS` 改成從 catalog 取，`data-label` 跟著改。
- [ ] 加一個跨語系測試：catalog 回傳 key 時畫面零漢字（做法見 `components/account-list-i18n.test.tsx`）。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run test:web -- merchant-coordinate
```

## Notes

- 標 P2 是因為這是後台單一佇列面板，站主自己看得懂中文；但它和其他後台面板不一致，而且 `admin.json` 的 UI 文案編輯器編不到它。
