---
id: 2026-09-06-admin-panels-i18n-remaining
title: 後台其餘三個面板文案硬編碼繁中
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-06T09:04:16Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-hotspot-places-panel.tsx
  - apps/web/components/admin-deployments-panel.tsx
  - apps/web/components/admin-users-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 後台其餘三個面板文案硬編碼繁中

## Why

`2026-09-06-admin-panels-i18n` 把最大的三個後台面板（settings／hotspots／food merchants）的文案搬進
`messages/*/admin.json` 之後，剩下三個還是寫死繁中：`admin-hotspot-places-panel.tsx` 約 55 句、
`admin-deployments-panel.tsx` 約 51 句、`admin-users-panel.tsx` 約 47 句。切到 `/en/admin` 這幾頁仍是中英夾雜。

跟上一張一樣是 P3：後台目前只有站長在用，繁中對他不是問題；列出來是為了讓「站台支援五語言」有一天能成立。

## Definition of done

- [ ] 三個面板在 `/en/admin` 沒有繁體中文（資料本身除外）。
- [ ] 新字串進 `messages/*/admin.json`，五語系鍵一致，照面板分組（`hotspotPlacesPanel`／`deploymentsPanel`／`usersPanel`）。
- [ ] 三個面板各自的 `.test.tsx` 通過。
- [ ] `CI=1 npm run check:i18n`、`lint:web`、`typecheck:web`。

## Steps

- [ ] 一個檔案一個 commit，不要一次三個。
- [ ] 沿用上一張的手法：`const t = useTranslations("admin")`，zh-TW 的值逐字照抄搬走的字面，
      測試裡的中文 accessible name 查詢就不用改；帶數字的句子用簡單 `{name}` 參數（vitest 的 mock 是 `replaceAll`，
      別用 plural／select）。
- [ ] `admin.json` 用純文字插入，不要 JSON round-trip（會重排整份檔案、默默吃掉重複鍵）。
- [ ] 可有可無的說明文字用 `t.has()`（`vitest.setup.tsx` 的 mock 已支援）。
- [ ] `usersPanel` 已經有一個物件（帳號面板的部分字串），新鍵併進去，不要另開同名的第二個。

## How to verify

```bash
cd apps/web && npx vitest run components/admin-hotspot-places-panel components/admin-deployments-panel components/admin-users-panel
cd ../.. && npm run lint:web && npm run typecheck:web && CI=1 node tools/check-i18n.mjs
```

## Notes

2026-09-06 立案時的參考實作：`admin-settings-panel.tsx`（`providerFields`／`providerSecrets`／`settingsPanel`，
包含 `t.has()`、`useLocale()` 格式化日期數字、`FieldOption.label` 可省略改查 catalog 的寫法）與
`admin-hotspots-panel.tsx`（`hotspotsPanel.*`，`Translator` 型別給 helper 用）。
所有 `admin-*.tsx` 都在 2026-09-06 補過 optional chaining（`data?.items?.map`），翻譯時不要把那些 `?.` 拿掉。
