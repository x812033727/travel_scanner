---
id: 2026-09-06-hotspot-themes-admin-api
title: 後台可以維護景點主題並逐景點指派
status: in-progress
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T17:03:53Z
created_at: 2026-09-06T17:03:42Z
completed_at:
branch: claude/hotspot-themes-admin-api
depends_on: []
scope:
  - apps/api/app/hotspots/admin_router.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_hotspot_admin_themes.py
---
# 後台可以維護景點主題並逐景點指派

## Why

`2026-09-06-hotspot-themes-api` 把季節與店型主題做進資料庫與公開 API，但主題只能改 `theme_bootstrap.json` 再等下一次 collect run。管理員沒辦法新增一個主題、改掉某個語系的名稱、或是對「這個景點其實不算賞櫻名所」做出判斷——而這正是種子資料一定會需要人工修正的地方。

## Definition of done

- [x] 後台可以列出、新增、修改主題（五語名稱、月份、排序、啟用）。
- [x] 可以逐景點指派主題，並為單一景點覆寫月份。
- [x] **管理員移除一個種子指派後，下一次 collect run 不會把它加回來。**
- [x] 每個寫入動作都留下 `AdminAuditLog`。
- [x] 候選清單（`GET /admin/hotspots/candidates`）帶出每個景點目前的主題。

## Steps

- [x] `admin_router.py`：payload（`ThemeWritePayload`／`ThemeUpdatePayload`／`HotspotThemeAssignment`／`HotspotThemesPutPayload`）與五個端點。
- [x] 候選清單加 `themes`（用 `load_hotspot_themes` 一次批次查，不要在既有的 per-row 迴圈裡再加一次查詢）。
- [x] `i18n.py`：三個新錯誤碼 ×5 語系。
- [x] `tests/test_hotspot_admin_themes.py`：15 個案例。
- [ ] 後台畫面（`admin-hotspot-themes-panel.tsx`、逐景點編輯器、workspace 分頁）——**另開任務**，見 Notes。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
```

```
GET    /admin/hotspots/themes?kind=season&status=active
POST   /admin/hotspots/themes            {slug, kind, names(五語), months, display_order, is_active}
PATCH  /admin/hotspots/themes/{id}       {names?, months?, display_order?, is_active?}
GET    /admin/hotspots/{hotspot_id}/themes     # 含墓碑，讓編輯器看得到「被移除過」
PUT    /admin/hotspots/{hotspot_id}/themes     {themes:[{slug, months?, note?}], reason?}
```

## Notes

- **墓碑是這張任務的重點**：`PUT` 是取代語意。請求裡沒有的 link，若 `source="seed"` 就留下來但 `is_active=false, source="admin"`；`admin`／`ai` 的直接刪掉。因為 `sync_hotspot_themes` 只管 `source="seed"` 的 link，改成 admin 之後它就不會再被種子檔復活。測試 `test_assigning_replaces_seed_links_with_tombstones_and_deletes_the_rest` 與 `test_clearing_every_theme_keeps_the_seed_tombstone` 就是守這條。
- `slug` 與 `kind` 建立後不可改：種子檔與使用者存下來的 `?theme=` 連結都以 slug 為準。
- 季節一定要有月份、店型一定不能有月份，兩邊都在 payload 驗證，也在 `PATCH` 針對既有 `kind` 再驗一次。
- 後台畫面沒有一起做：`apps/web/components/admin-hotspots-panel.tsx` 與 `admin-hotspots-workspace.tsx` 當時被 `2026-09-06-admin-review-density` 佔著（in review），硬排會撞。畫面需要的東西這裡都備好了——列表有 `hotspot_count`，逐景點 GET 會回 `months_overridden` 與 `source`，候選清單直接帶 `themes`。
- 測試用的 FakeSession 會在 `flush()` 補上 `created_at`／`updated_at`：真的資料庫是在 INSERT 時蓋這兩個欄位，而 `SessionFactory` 是 `expire_on_commit=False`，端點 commit 之後仍讀得到。fake 不補就會測到一個現實中不存在的狀態。
