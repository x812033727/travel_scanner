---
id: 2026-09-06-hotspot-themes-admin-web
title: 後台主題管理畫面：taxonomy 表格與逐景點指派
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-06T17:18:35Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/components/admin-hotspot-themes-panel.tsx
  - apps/web/components/admin-hotspot-theme-editor.tsx
  - apps/web/components/admin-hotspots-workspace.tsx
  - apps/web/components/admin-hotspots-panel.tsx
  - apps/web/i18n/request.ts
  - apps/web/vitest.setup.tsx
  - apps/web/messages/en/hotspotThemes.json
  - apps/web/messages/ja/hotspotThemes.json
  - apps/web/messages/ko/hotspotThemes.json
  - apps/web/messages/zh-TW/hotspotThemes.json
  - apps/web/messages/zh-CN/hotspotThemes.json
---
# 後台主題管理畫面：taxonomy 表格與逐景點指派

## Why

`2026-09-06-hotspot-themes-admin-api` 已經把五個端點做好了，但後台還沒有畫面，所以實務上還是只能改種子檔。管理員需要能改掉某個語系寫壞的主題名稱、新增一個季節、以及對單一景點做判斷（「這其實不算賞櫻名所」「札幌的櫻花是五月」）。

種子資料一定會有錯——第一版就已經修過釜山的櫻花月份、小樽的賞雪、東急歌舞伎町 TOWER 的店型。這些都應該在後台做完，不必等下一次部署。

## Definition of done

- [ ] 「主題分類」分頁：列出主題（類型、五語名稱、月份、排序、景點數、狀態），可新增與編輯。
- [ ] 景點列每一列可以開一個小編輯器指派主題；季節可勾「使用預設月份」或自訂；店型在非 `shopping` 分類的景點上不可選。
- [ ] 被管理員移除過的種子指派（墓碑）要看得出來，不要讓人以為可以直接再加回去。
- [ ] 五語文案齊全，`npm run check:i18n` 過。

## Steps

- [ ] `apps/web/messages/*/hotspotThemes.json`（新 namespace），**同時登記在 `apps/web/i18n/request.ts` 的 `namespaces` 與 `apps/web/vitest.setup.tsx` 的 `catalogs`**，漏一個 `t()` 會回傳原始 key。
- [ ] `admin-hotspot-themes-panel.tsx`：照 `admin-food-taxonomy-panel.tsx` 的表格＋對話框，重用它 export 的 `LocalizedNameFields`／`blankNames`／`completeNames`；月份用 12 顆 `aria-pressed` 按鈕。
- [ ] `admin-hotspot-theme-editor.tsx`：自帶觸發鈕與對話框，`admin-hotspots-panel.tsx` 只加三處（`Candidate.themes?`、import、分類欄一行 JSX）。
- [ ] `admin-hotspots-workspace.tsx`：加 `themes` 分頁，面板 lazy mount（`active === "themes" && ...`，因為 `AdminTabPanel` 不會卸載隱藏的子元件）。
- [ ] 測試：兩個面板各一個 test 檔，`admin-hotspots-workspace.test.tsx` mock 掉既有面板。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
git add -A && CI=1 node tools/check-i18n.mjs
```

`/admin/hotspots#themes`：改一個主題的日文名、新增一個主題、對淺草寺指派「賞櫻」並自訂月份；接著跑一次 `python -m app.hotspots.themes`，確認後台的指派與墓碑都還在（這是後端墓碑規則的真正驗收）。

## Notes

- API 已經備好畫面需要的東西：主題列表有 `hotspot_count`；`GET /admin/hotspots/{id}/themes` 會回 `months_overridden`、`source`、`is_active`（含墓碑）；`GET /admin/hotspots/candidates` 每一列直接帶 `themes`。
- `PUT /admin/hotspots/{id}/themes` 是**取代**語意，所以編輯器一定要先讀到目前的指派再送出，否則會把沒列出來的主題全部清掉。候選清單已經帶 `themes`，拿不到就別讓使用者存。
- 月份格式化直接用 `apps/web/lib/hotspot-themes.ts` 的 `monthRangeLabel`／`monthRuns`（公開頁那個 PR 已經進 main），不要再寫一份。
- 主題名稱本身不進語言檔（伺服器依語系回傳）；這個 namespace 只放框架文案。
- 檔案衝突：開工前確認 `2026-09-06-admin-review-density` 已經合併——它佔著 `admin-hotspots-panel.tsx` 與 `admin-hotspots-workspace.tsx`，這也是當初後端先做、畫面後做的原因。
