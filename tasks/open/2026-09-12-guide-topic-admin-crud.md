---
id: 2026-09-12-guide-topic-admin-crud
title: 後台新增／編輯文章主題標籤
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-12T14:18:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/router.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/schemas.py
  - apps/api/tests/test_guides.py
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 後台新增／編輯文章主題標籤

## Why

`docs/travel-guides.md` 與 `GuideTopic` 的 docstring 都說「編輯可以不用部署就新增主題」，但 API 只有
`GET /guides/topics` 與 `GET /admin/guides/topics`（`apps/api/app/guides/router.py`），沒有任何寫入端點，
後台面板（`apps/web/components/admin-guides-panel.tsx`）也只把既有主題畫成勾選框。主題目前只能靠
migration 種子（0072 旅遊、0074 生活）或直接改資料庫。生活分享專區的定位是「AI、教學、其他的東西」，
編輯遲早會需要新主題。

## Definition of done

- [ ] `POST /admin/guides/topics`（slug、section、五語系 `names_json`、display_order）與
      `PUT /admin/guides/topics/{slug}`（改名、停用），`content.manage` 才能寫，寫入留 `AdminAuditLog`。
- [ ] `source='admin'` 的主題不會被 migration 種子覆蓋（0072／0073 已保證）；slug 用與文章相同的小寫規則。
- [ ] 後台面板多一個小表單可新增主題並立即出現在對應專區的勾選框。
- [ ] 錯誤碼從 `admin_service.py` 拋出（路徑含 admin，免翻譯）；測試涵蓋重複 slug、缺語系標籤、跨專區。

## Steps

- [ ] schemas：`TopicCreate`／`TopicUpdate`；admin_service：寫入與審計；router：兩個端點。
- [ ] 面板：表單＋重新載入主題；測試。
- [ ] 文案：`messages/*/admin.json` `guides.*` 新 key（五語系同步）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides.py -q
cd apps/web && npx vitest run components/admin-guides-panel.test.tsx
```

## Notes

- 這張票的 scope 完全落在 `2026-09-12-lifestyle-section-and-guides-relabel` 之內，那張 `done` 之前 claim 會被拒絕；這是刻意的。
- 主題 slug 全域唯一（`uq_guide_topic_slug`），旅遊與生活不能各有一個 `ai`。
