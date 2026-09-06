---
id: 2026-09-06-trip-editor-i18n
title: 行程編輯器 294 句硬編碼繁中未五語系化
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-06T00:52:44Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/trip-editor.tsx
  - apps/web/messages/en/trips.json
  - apps/web/messages/ja/trips.json
  - apps/web/messages/ko/trips.json
  - apps/web/messages/zh-CN/trips.json
  - apps/web/messages/zh-TW/trips.json
---

# 行程編輯器 294 句硬編碼繁中未五語系化

## Why

站台宣稱支援五種語言，但行程編輯器是使用者停留最久的畫面，裡面約 294 句可見文字寫死在
`trip-editor.tsx` 裡。英／日／韓／簡中的使用者打開自己的行程，看到的是外框是自己的語言、
內容整片繁體中文。

`LegacyUiLocalizer` 有一份 runtime 替換字典（`messages/*/legacy.json`），但只有 54 筆，
完全涵蓋不到這個檔案。2026-09-05 的全站健檢把首頁精靈（`search-workbench.tsx`，77 鍵）
與分享頁做完了，行程編輯器是剩下最大、也最值得做的一塊。

## Definition of done

- [ ] 以 `/en` 開啟一個有安排的行程，畫面上找不到任何繁體中文（`FoodMerchant` 之類的
      資料本身除外）。日、韓、簡中同樣。
- [ ] 所有新增字串都在 `messages/*/trips.json`，五個語系鍵完全一致。
- [ ] `CI=1 npm run check:i18n`、`npm run lint:web`、`npm run typecheck:web` 通過。
- [ ] `apps/web/components/trip-editor.test.tsx` 全數通過（它用中文 accessible name 查詢，
      改字串會連帶要改測試）。

## Steps

- [ ] 用 `scratchpad` 的方法把待翻字串列出來：對 `trip-editor.tsx` 抓 `"…"`／`'…'`／`>…<`
      裡含 Han 的片段，扣掉 `messages/en/legacy.json` 已有的鍵。
- [ ] 分批進行，一批一個區塊（工具面板 / 日面板 / 項目卡 / AI 浮層 / 航班浮層 / toast），
      每批都跑一次測試，不要一次改完 294 句。
- [ ] 帶參數的句子改成 ICU（例如 `{count} 個已安排 · 停留約 {duration}`），
      `check:i18n` 會驗五語系的 ICU 參數一致。
- [ ] 同步更新 `trip-editor.test.tsx` 裡以中文查詢的斷言。
- [ ] `activityDurationOptions`（`20 分鐘`／`1 小時`…）與 `plannerThemes`（森旅／海岸…）
      是模組層級常數，要改成在元件內用 `t()` 產生。

## How to verify

```bash
cd apps/web && npx vitest run components/trip-editor.test.tsx
cd ../.. && npm run lint:web && npm run typecheck:web && CI=1 node tools/check-i18n.mjs
```

再用 Playwright 開 `/en/trips/<id>`，抓 `#…` 容器的 innerText 對 `/[一-鿿]/` 比對，
應為空。2026-09-05 驗首頁精靈就是這樣做的（見 Notes）。

## Notes

**量測方法**：把下面存成一個 mjs 跑（2026-09-05 用過，可靠）：對 `components/`、`app/`、
`lib/` 掃 `.tsx`，用 `/"([^"\n]{1,90})"/g`、`/'([^'\n]{1,90})'/g`、`/>([^<>{}\n]{1,90})</g`
三個 pattern 抓字串，過濾含 Han 的，再扣掉 `messages/en/legacy.json` 的鍵。當時全站結果：
54 個檔案、1,858 句，其中 `trip-editor.tsx` 294 句居首。

**踩過的坑**：
- `messages/*/*.json` 千萬不要用 `JSON.parse` → `JSON.stringify` 回寫，會把整份檔案重排
  （單檔 92 行 diff），而且會默默吃掉重複鍵。要用純文字插入：找 `raw.lastIndexOf('}')`，
  在它前面插新鍵。
- `check:i18n` 的鍵一致性檢查**永遠會跑**（不只 CI）；Han 新增字檢查只在 `CI=1` 或有
  staged 變更時跑。所以本機驗要 `git add -A` 之後再跑，或直接 `CI=1`。
- `trips.json` 目前已有 `notes*`／`cost*`／`share*` 等鍵（2026-09-06 的備註與成本功能加的），
  新增時先確認鍵名沒撞到。

**不在本任務範圍**：`admin-*` 面板（另開 `2026-09-06-admin-panels-i18n`）、
`search-experience.tsx`（`2026-09-06-search-results-i18n`）、
`lib/destinations.ts` 的資料標籤（`2026-09-06-destination-catalog-labels-i18n`）。
