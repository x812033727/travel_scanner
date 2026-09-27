# 本機看 /hotspots，以及區域（area）的規則

## 不開 Postgres 也能看公開景點頁

本機沒有 Docker 時 Postgres 整合測試只在 CI 跑，但要用眼睛確認 `/hotspots` 的篩選與卡片，可以用假 API：

1. 從 `HOTSPOT_SEEDS`（`apps/api/app/hotspots/catalog.py`）與 `apps/api/app/hotspots/areas.py` 產一份 fixture（rankings 的 `items` 與 facets 的國家、目的地、分類、區域計數）。
2. 複製 `tools/e2e-runtime-api.mjs` 到暫存目錄，加上 `GET /api/v1/hotspots/facets` 與 `GET /api/v1/hotspots/rankings` 回 fixture，並讓 `/api/v1/auth/me` 與 `/api/v1/saved-items` 回 401（原檔的 `auth/me` 會回一個登入使用者）。它聽 `127.0.0.1:${E2E_API_PORT:-8000}`，web 端以 `API_INTERNAL_URL`（預設 `http://localhost:8000`）找它。
3. `npm run dev --workspace @travel-scanner/web -- --port 3100`，打開 `http://127.0.0.1:3100/zh-TW/hotspots`。

fixture 與改過的 mock 放暫存目錄，不進 repo。

## 區域的規則

- 區域是 `apps/api/app/hotspots/areas.py` 裡每個城市的圓（中心＋半徑）。`travel_hotspots.area_code` 是**衍生值**：`sync_hotspot_areas` 在每次 collect 重算，review 端點改座標或目的地時也當場用 `resolve_area_code` 重算。
- 取 `距離／半徑` 最小的圓；落在所有圓外就沒有區域。**不要加「最近的區域」fallback**，否則三十公里外的一日遊會顯示成新宿。
- 分錯區域要移中心或改半徑，不要手改列、不要加種子覆寫。
- 種子座標與名稱對不上的列列在 `apps/api/tests/test_hotspot_areas.py` 的 `AREA_UNASSIGNED_SEEDS`；修它們會動到各城市的深度旅遊數量契約，是另一件資料變更。
- 熱門新興街區放在區域裡而不是景點裡，因為區域沒有永久座標閘門。錨定時韓國的洞名在維基多半是消歧義頁（要用「성수동 (서울)」這類標題），日文裸地名可能命中別縣同名市，一律用城市的圓框住命中結果。
- Wikidata 座標可能指向舊址或河口；種子產生器（`tools/generate_kanto_expansion.py` 的 `PREFER_OVERRIDE`）用審過的座標覆蓋這類例外。
