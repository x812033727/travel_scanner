---
id: 2026-09-11-discovery-saved-count-ranking
title: 探索卡顯示累積蒐藏數與蒐藏數排行分頁
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T08:19:59Z
created_at: 2026-09-11T08:19:56Z
completed_at: 2026-09-11T10:24:13Z
branch: claude/planning-card-collection-count-pdbiwg
depends_on: []
scope:
  - apps/web/components/discovery/card.tsx
  - apps/web/components/discovery/explorer.tsx
  - apps/web/components/discovery/discovery.module.css
  - apps/web/components/discovery/discovery.test.tsx
  - apps/web/lib/discovery.ts
  - apps/web/messages/en/community.json
  - apps/web/messages/ja/community.json
  - apps/web/messages/ko/community.json
  - apps/web/messages/zh-CN/community.json
  - apps/web/messages/zh-TW/community.json
  - apps/api/app/discovery/router.py
  - apps/api/app/discovery/schemas.py
  - apps/api/app/discovery/service.py
  - apps/api/app/saved/service.py
  - apps/api/app/community/models.py
  - apps/api/migrations/versions/0071_collection_item_lookup.py
  - apps/api/tests/test_travel_discovery.py
  - apps/api/tests/test_collection_item_lookup_migration.py
---

# 探索卡顯示累積蒐藏數與蒐藏數排行分頁

## Why

`/explore` 的規劃小卡（`DiscoveryCard`）只有「收藏」按鈕，讀者看不出一個景點／美食／飯店／攻略被多少人收藏過，沒有任何熱門度訊號。分頁列也只有「為你推薦 / 最新 / 追蹤中」，全是時間或個人化排序，沒有一個照大家的收藏量排。

## Definition of done

- [x] 探索卡與詳情抽屜顯示這一項被多少人收藏（0 時不顯示），未登入者也看得到。
- [x] 「最新」與「追蹤中」中間出現「蒐藏數」分頁，照累積收藏數由高到低排，不需登入。
- [x] 同一個使用者用多種管道收藏同一項只算一次；攻略、貼文與五種 typed favorite 都算得到。
- [x] 五語系皆有分頁標籤，且沒有新的中文寫進 `apps/web/lib`（`check:i18n` 的漢字守衛）。

## Steps

- [x] `saved_counts()`：跨 typed favorite／`Reaction`／收藏清單的 `COUNT(DISTINCT user_id)`。
- [x] `community_collection_items (kind, target)` 索引 + migration 0071。
- [x] `most_saved` mode 進 `/discovery/feed` 與 `/discovery/search`，並填 `saved_count`。
- [x] 前端型別、分頁、卡片數字、五語系字串。
- [x] API 與 web 測試。

## How to verify

```sh
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
```

`check:i18n` 的漢字守衛只在 CI 或有 staged 檔案時才跑，所以 `git add` 之後要再跑一次才真的驗到。

手動：`/zh-TW/explore` 應有四個分頁；收藏一張卡後重新整理會出現「1 次收藏」；切到「蒐藏數」該卡排前面；帶 `?q=` 搜尋時切分頁不應 422。

## Notes

- **scope 重疊，使用 `--force` 認領。** 要動的檔案幾乎全被三個 2026-09-09 認領、已逾 24 小時的 stale claim 押住：
  `2026-09-09-discovery-card-details`（`apps/api/app/discovery` 整個目錄、`card.tsx`、`discovery.module.css`、`lib/discovery.ts`）、
  `2026-09-09-frontend-flow-discovery-web`（`explorer.tsx`、`discovery.test.tsx`）、
  `2026-09-09-frontend-flow-saved-api`（`apps/api/app/saved`、`apps/api/app/community/models.py`）。
  三者的 Notes 都記載 PR #374 已合併（`a899437a`）且原作者已停止動工；`tools/tasks.mjs` 的重疊檢查不看 claim 是否過期，所以必然拒絕。`npm run check:tasks` 本來就列出十幾組 active 重疊且只是 warning。
- `ensure_base()` 依類型**只寫一處**：景點／美食／店家／飯店寫 typed favorite 表，貼文／行程寫 `Reaction(save)`，攻略（article/video→guide）沒有 typed 表、只落在 `community_collection_items`。三個來源少查一個就會有整個類型歸零。
- 加進具名清單時 `collect_reference()` 會先建 base，同一使用者於是同時有 typed favorite 列與 `CollectionItem` 列，所以必須 `COUNT(DISTINCT user_id)` 而不是 `COUNT(*)`。
- `collection_columns()` 用 `lower(replace(cast(target as text),'-',''))` 正規化，普通 btree 索引吃不到；計數改成把別名 kind 與 UUID 的各種寫法展開後過濾**原始欄位**，再於 Python 端用 `canonical()` 折算，語意等價且吃得到新索引。
- 新分頁的 `recommendation_reason` 設 `None`，避免在 `lib/discovery-copy.ts` 的 `getRecommendationReason` 新增中文而踩到 `check:i18n`。
- 排行榜候選受 `catalog_items` 每個來源 `SOURCE_LIMIT=100` 的既有上限，是「近期內容中的收藏排名」而非全庫排名。
- 收藏庫頁走 `/saved-items/all`，這次不填 `saved_count`。
- `check-i18n` 的漢字守衛連**程式註解**也算，第一次把「次收藏」寫進 `card.tsx` 的註解就被擋下；註解也要避開中文。
- 已驗：`lint:web`、`check:i18n`（含 staged 後的漢字守衛）、`typecheck:web`、`test:web`（216 檔 1996 測試）、`test:tools`、`check:tasks`、`ruff check .`、`mypy app`（303 檔）、`pytest`（3036 passed / 161 skipped）、`alembic heads` = `0071_collection_item_lookup`。
- `alembic upgrade head` 無法在 SQLite 跑完整條鏈（舊的 `usage_ledger ALTER COLUMN ... SET NOT NULL` 是 PostgreSQL 專用），與本次修改無關；0071 由 `tests/test_collection_item_lookup_migration.py` 以新舊兩種起始狀態驗證。
- PR: https://github.com/x812033727/travel_scanner/pull/393 （in review，尚未合併或部署）。
- 開 PR 前先併入 `main`（#392 訂位平台），`tasks/BOARD.md` 衝突照 `AGENTS.md` 規則 2 用 `npm run tasks:board` 重新產生。合併後重跑全部檢查：web 218 檔 2134 測試、API 3133 passed / 165 skipped，其餘全過。
- 本機跑 `CI=1 npm run check:i18n` 會誤報 `reservation-platforms.ts` 的「一休」：本機 merge commit 的 `HEAD^` 是本功能 commit，而 CI 在 PR merge ref 上的 `HEAD^` 是 base，兩者父節點順序相反。以 `origin/main...HEAD` 重跑同一套守衛邏輯為 PASS。
