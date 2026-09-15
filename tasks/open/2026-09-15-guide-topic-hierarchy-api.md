---
id: 2026-09-15-guide-topic-hierarchy-api
title: Two-level article topics and a country filter on the public guides API
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-15T13:58:23Z
created_at: 2026-09-15T13:53:24Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on: []
scope:
  - apps/api/app/guides/models.py
  - apps/api/app/guides/taxonomy.py
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/service.py
  - apps/api/app/guides/router.py
  - apps/api/app/guides/admin_service.py
  - apps/api/migrations/versions/0076_guide_topic_hierarchy.py
  - apps/api/tests/test_guides.py
  - apps/api/tests/test_guides_migration.py
  - docs/travel-guides.md
---

# Two-level article topics and a country filter on the public guides API

## Why

生活分享的主題是扁平的八個 slug：`tutorial` 掛在 659／818 篇、`ai` 529 篇、403 篇同時是兩者，主題 chip 對讀者已經沒有導覽意義。
旅遊文章的第二軸是目的地，但 33 個目的地沒有「國家」這一層可以分組。站主 2026-09-15 核准的架構（`docs/article-architecture.md`）
第一步就是讓主題有父子兩層、讓旅遊列表能依國家篩，其餘階段（搜尋、互連、SEO）都建立在這上面。

## Definition of done

- [x] `guide_topics` 有 `parent_id`（自我參照、可空）與 `descriptions_json`；migration `0076_guide_topic_hierarchy` 只新增欄位與種子，既有資料不動，可回滾。
- [x] `GET /guides/topics?locale&section` 每列多 `parent`、`description`、`count`（該語系已發布篇數）、`counts`（各語系）；父主題的數字是自身∪子主題的 distinct 篇數。
- [x] `GET /guides?topic=<父主題>` 含子主題的文章；`GET /guides?country=japan` 只回日本目的地的文章，未知國家回空。
- [x] `GET /guides/destinations?locale&section` 回每個有已發布文章的目的地與國家、篇數。
- [x] 文章 slug 不能是 `topics`、`series`、`search`（主題 hub 與搜尋頁的路徑段）。
- [x] `tests/test_guides_migration.py` 的種子對照涵蓋 0076；子主題 slug 不與旅遊／discovery 詞彙相撞。

## Steps

- [x] models.py／taxonomy.py（`LIFE_SEED_SUBTOPICS`、`LIFE_TOPIC_DESCRIPTIONS`、`topic_ids_including_children`、count 聚合）。
- [x] 0076 migration：欄位用 `batch_alter_table` + inspector 守衛；種子沿用 0072 契約；downgrade 只刪本 revision 的 slug。
- [x] schemas／service／router：`TopicOption` 擴充、`country` 篩選、`destination_facets`、`/guides/destinations`。
- [x] admin_service：父子並存、保留 slug。
- [x] 測試與 `docs/travel-guides.md` Classification 段。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app
cd apps/api && uv run pytest tests/test_guides.py tests/test_guides_migration.py -q
```
啟動 API 後：`GET /api/v1/guides/topics?locale=zh-TW&section=life`、`GET /api/v1/guides?locale=zh-TW&kind=howto&country=japan`、`GET /api/v1/guides/destinations?locale=zh-TW`。

## Notes

- 2026-09-15 落地。`descriptions_json` 用 `JSON(none_as_null=True)`：SQLAlchemy 會把 Python None 存成 JSON 文字 `null`，`IS NULL` 比不到，0076 的種子 UPDATE 兩種都接受。
- `tutorial` 降為橫向標籤（不再是導覽用的父主題）；新父主題 `website`、`marketing`；子主題表在 `docs/article-architecture.md`，標籤可在合併前改種子。
- `2026-09-12-guide-topic-admin-crud` 之後要讓 `TopicCreate/TopicUpdate` 帶 `parent_slug` 與 `descriptions_json`。
- `service.py`／`router.py` 也被 `2026-09-14-guide-listing-curated-order` 與 sitemap-split 兩張 open 任務列在 scope，後合併者 rebase。
