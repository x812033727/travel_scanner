---
id: 2026-09-06-trip-editor-i18n
title: 行程編輯器 294 句硬編碼繁中未五語系化
status: done
priority: P1
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-06T03:32:53Z
created_at: 2026-09-06T00:52:44Z
completed_at: 2026-09-06T04:03:30Z
branch: claude/web-i18n-p1
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

- [x] 以 `/en` 開啟一個有安排的行程，畫面上找不到任何繁體中文（`FoodMerchant` 之類的
      資料本身除外）。日、韓、簡中同樣。
- [x] 所有新增字串都在 `messages/*/trips.json`，五個語系鍵完全一致。
- [x] `CI=1 npm run check:i18n`、`npm run lint:web`、`npm run typecheck:web` 通過。
- [x] `apps/web/components/trip-editor.test.tsx` 全數通過（它用中文 accessible name 查詢，
      改字串會連帶要改測試）。

## Steps

- [x] 用 `scratchpad` 的方法把待翻字串列出來：對 `trip-editor.tsx` 抓 `"…"`／`'…'`／`>…<`
      裡含 Han 的片段，扣掉 `messages/en/legacy.json` 已有的鍵。
- [x] 分批進行，一批一個區塊（工具面板 / 日面板 / 項目卡 / AI 浮層 / 航班浮層 / toast），
      每批都跑一次測試，不要一次改完 294 句。
- [x] 帶參數的句子改成 ICU（例如 `{count} 個已安排 · 停留約 {duration}`），
      `check:i18n` 會驗五語系的 ICU 參數一致。
- [x] 同步更新 `trip-editor.test.tsx` 裡以中文查詢的斷言。
- [x] `activityDurationOptions`（`20 分鐘`／`1 小時`…）與 `plannerThemes`（森旅／海岸…）
      是模組層級常數，要改成在元件內用 `t()` 產生。

## How to verify

```bash
cd apps/web && npx vitest run components/trip-editor.test.tsx
cd ../.. && npm run lint:web && npm run typecheck:web && CI=1 node tools/check-i18n.mjs
```

再用 Playwright 開 `/en/trips/<id>`，抓 `#…` 容器的 innerText 對 `/[一-鿿]/` 比對，
應為空。2026-09-05 驗首頁精靈就是這樣做的（見 Notes）。

## Notes

**2026-09-06 完成。** 346 個字面（實際比 294 多，因為模板字串與超長 JSX 行裡的字串當初沒算到）搬進
`messages/*/trips.json` 的新物件 `editor`（五語系 236 鍵），元件加 `const te = useTranslations("trips.editor")`。
模組層級常數照 `stepKeys` 模式：`activityDurationOptions` 只留分鐘數、渲染處 `te(\`duration.m${minutes}\`)`；
`plannerThemes` 只留 id 與色票、名稱與描述用 `te(\`theme.${id}.name\`)`。`mobileDayHeading`／`durationSummary`／
`aiProviderLabel` 多一個 `te` 參數。`saveLabel` 改成 `te(\`saveState.${saveState}\`)`。
四個在 effect／callback 裡用到 `te` 的地方把它加進依賴陣列（eslint `exhaustive-deps`），
因此 `vitest.setup.tsx` 的 next-intl mock 改成每個 namespace 快取同一個函式——正式的 `useTranslations` 本來就是穩定的，
mock 每次 render 回新閉包會讓 effect 無限重跑，這是全站測試都受惠的修正。
刻意留下的繁中：`countryCodesForTrip` 用目的地名稱判國家的正則、`routeWarnings.some(w => w.includes("缺少已確認地點"))`
比對伺服器警告文字——兩者都是解析，不是顯示。
測試：`trip-editor.test.tsx` 33 則全過（zh-TW 值不變）；lint／tsc／`CI=1 check:i18n` 過；
Han 掃描只剩上述解析行。瀏覽器驗證見 PR。

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
