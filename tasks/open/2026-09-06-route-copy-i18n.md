---
id: 2026-09-06-route-copy-i18n
title: 路線卡與路線面板的文案硬編碼繁中
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T10:22:52Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/route-segment-card.tsx
  - apps/web/components/route-mode-panel.tsx
  - apps/web/components/route-timeline-link.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 路線卡與路線面板的文案硬編碼繁中

## Why

`route-mode-panel.tsx`（約 60 句）與 `route-segment-card.tsx`（約 25 句）整份寫死繁體中文：
起訖標題、交通方式分頁、「近期參考班次」、「詳細移動步驟」、以及每個步驟的
`月台 {platform}`／`出口 {exit_name}`／`建議車廂 {recommended_car}` 標籤。
`/en/trips/<id>` 打開路線抽屜就是中英夾雜。

`trips.json` 已經有 `route` 群組（`route-timeline-link.tsx` 在用，13 個鍵），
所以這張是把剩下兩個檔案的字串搬進同一個群組，不是新開一套。

2026-09-06 `2026-09-06-honest-leg-guard` 想在面板補這三個標籤時才發現它們早就存在（只是繁中），
那張的 scope 只有 `routing.py` 與 `route-mode-panel.tsx`，所以另開這張把兩個檔案一起做完。

## Definition of done

- [ ] 這三個檔案在 `/en/trips/<id>` 的路線抽屜沒有繁體中文（資料本身除外）。
- [ ] 新字串進 `messages/*/trips.json` 的 `route` 群組，五語系鍵一致。
- [ ] `route-mode-panel.test.tsx`、`route-segment-card` 相關測試通過（它們用中文 accessible name 查詢）。
- [ ] `CI=1 npm run check:i18n`、`lint:web`、`typecheck:web`。

## Steps

- [ ] `useTranslations("trips.route")`，zh-TW 的值逐字照抄搬走的字面，測試就不用改。
- [ ] 帶數字或名稱的句子用簡單 `{name}` 參數（vitest 的 next-intl mock 是 `replaceAll`，不要用 plural／select）。
- [ ] `messages/*/trips.json` 用純文字插入，不要 JSON round-trip。
- [ ] 面板裡的 `aria-label`（如「路線起訖與交通方式」「選擇交通工具」）也要一起搬，
      螢幕閱讀器讀到的語言要跟畫面一致。

## How to verify

```bash
cd apps/web && npx vitest run components/route-mode-panel components/route-segment-card
cd ../.. && npm run lint:web && npm run typecheck:web && CI=1 node tools/check-i18n.mjs
```

## Notes

參考實作：`route-timeline-link.tsx`（同一個 `trips.route` 群組）與 2026-09-06 的三個後台面板
（`admin.json` 的 `hotspotsPanel`／`foodMerchantsPanel`／`settingsPanel`）。
可有可無的說明文字用 `t.has()`，`vitest.setup.tsx` 的 mock 已支援。
