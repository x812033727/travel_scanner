---
id: 2026-09-06-tokyo-planner-duration-500
title: 東京 AI 行程一律 500：一筆種子的 20 分鐘低於 planner 下限
status: done
priority: P0
area: api
owner: claude-opus-5
claimed_at: 2026-09-06T13:45:42Z
created_at: 2026-09-06T13:45:36Z
completed_at: 2026-09-06T13:46:52Z
branch: fix/planner-candidate-duration-clamp
depends_on: []
scope:
  - apps/api/app/ai/itinerary.py
  - apps/api/app/trips/router.py
  - apps/api/tests/test_ai_itinerary.py
---

# 東京 AI 行程一律 500：一筆種子的 20 分鐘低於 planner 下限

## Why

生產環境每一次對東京行程按 AI 規劃都回 HTTP 500。首爾正常。當時線上五筆行程有四筆是東京。

鏈路每一環都已驗證：

1. `nrt-hachiko-statue`（忠犬八公像）的 `metadata_json.recommended_duration_minutes` 是 `20`。
   它 `approved`、`is_active`、`map_match_status='verified'`、有座標與 Place ID，且在
   `destination:tokyo` 排第 5 名，穩穩落在 `load_planner_hotspots(limit=40)` 的取用範圍內。
2. `apps/api/app/hotspots/service.py` 讀回時寫成 `item["recommended_duration_minutes"] or 120`，
   20 是 truthy，所以原封不動傳下去。
3. `apps/api/app/trips/router.py` 的 `_load_ai_planner_candidates` 在 list comprehension 裡建構
   `AIPlannerCandidate(...)`，過濾條件只有 `depth_kind` 與 `is_cross_city`，沒有任何一項檢查時長。
4. `apps/api/app/ai/itinerary.py` 的 `duration_minutes` 宣告 `Field(ge=30, le=480)`，於是拋出
   pydantic `ValidationError: Input should be greater than or equal to 30`（本機以真實模型重現過）。
5. 三個呼叫點都沒有 try/except，而 `apps/api/app/main.py` 只註冊了 `AppError` 與
   `RequestValidationError` 兩個處理器。pydantic 的 `ValidationError` 兩者皆非，所以逃逸成 500。

**為什麼後台顯示一切正常**：`ai_planner` 的連線測試用 `candidates=[]` 建請求，永遠走不到這段。

**為什麼測試全綠**：`apps/api/tests/test_kanto_expansion.py` 的斷言是
`row["recommended_duration_minutes"] >= 20`——下限剛好就設在這個壞值上，等於把它正當化；而
`test_hotspot_depth_catalog.py` 裡 `>= 30` 的嚴格不變量只套用在 `is_deep_travel` 的列，看不到這一筆。

**為什麼壞值進得來**：同一個 metadata key 有兩條寫入路徑，鬆緊相反。管理員改景點走
`hotspots/admin_router.py` 的 `HotspotReviewRequest`，`Field(ge=30, le=480)` 會用 422 擋下 20；
種子匯入走 `hotspots/service.py` 的 `seed_catalog`，`HotspotSeed` 是沒有驗證器的 dataclass，
值原封不動寫進 `metadata_json`，還直接設成 `approved` + `is_active`。

## Definition of done

- [x] 東京行程的 AI 規劃不再因為任何一筆種子資料而回 500。
- [x] 目錄保留真實的 20 分鐘：忠犬八公像本來就是 20 分鐘的拍照點，景點頁該照實顯示。
- [x] 未來任何一筆越界的種子值，會在測試就失敗，而不是在生產環境。

## Steps

- [x] 在 `apps/api/app/ai/itinerary.py` 把界線抽成常數（`MIN_/MAX_CANDIDATE_DURATION_MINUTES`、
      `MAX_CANDIDATE_ACCESS_MINUTES`）並讓 `Field(...)` 直接引用，避免界線與夾限日後漂移；
      加上 `clamp_candidate_duration()` 與 `clamp_candidate_access()`。
- [x] 在 `apps/api/app/trips/router.py` 的候選建構點改用這兩個夾限函式。
- [x] 在 `apps/api/tests/test_ai_itinerary.py` 加三個測試：夾限行為、忠犬八公像這個實例（並以
      `pytest.raises` 保留「未夾限就會炸」的證據）、以及走過所有真實種子檔的回歸測試。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
```

部署後在生產環境建一筆東京行程並按 AI 規劃，應該回傳草稿而不是 500；同一操作在首爾維持原樣。

## Notes

**刻意不改種子檔。** 20 分鐘是正確的資料。為了配合 planner 的排程下限去竄改目錄，等於對這個地點說謊，
而且下一個匯入還是會寫回 20。夾限放在 planner 邊界，界線常數與 `Field` 綁在一起，是唯一不會漂移的位置。

**刻意不改生產資料庫。** 夾限上線後那一列不再造成任何問題，所以不需要為了修 bug 去動線上資料。

**沒有做但已確認存在的同類問題**（另立任務）：

- `seed_catalog` 與 `HotspotReviewRequest` 對同一個 metadata key 的驗證鬆緊相反，種子路徑完全沒有界線。
- `ai_planner` 的後台連線測試送 `candidates=[]`，所以它結構上看不到這一類缺陷；改成送一筆真實候選就能擋下。
- 全庫掃過四份種子檔共 393 筆，只有這一筆越界；`access_minutes`、`name`、`category`、經緯度全部乾淨。

**本任務的測試沒有覆蓋到的**：測試直接呼叫夾限函式，所以如果有人把 `router.py` 呼叫點的夾限拿掉、
卻留著函式，測試仍會通過。要真正鎖住呼叫點需要走到 DB 層的測試，成本較高，留給後續任務。
