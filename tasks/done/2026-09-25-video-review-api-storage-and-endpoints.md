---
id: 2026-09-25-video-review-api-storage-and-endpoints
title: 影片審核：API、預覽檔儲存與端點
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T05:12:56Z
created_at: 2026-09-25T05:12:45Z
completed_at: 2026-09-25T05:20:30Z
branch: claude/video-review-api
depends_on: []
scope:
  - apps/api/app/video_reviews
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/config.py
  - apps/api/migrations/versions/0089_video_reviews.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/api/Dockerfile
  - docker-compose.prod.yml
  - .env.example
---

# 影片審核：API、預覽檔儲存與端點

## Why

站主 2026-09-25 問「沒有其他相關設定嗎？像是列出來的草稿跟成品給我審核跟確認是否要上架」，選了完整版：網站後台要有「影片審核」頁，列出每支影片在哪一步、企劃與大綱選擇、旁白、成片預覽，並能核准／退回、確認可以上架。目前這些全在本機工作區與對話裡，站主看不到。

## Definition of done

- [x] `video_projects`、`video_reviews`（migration 0089）：一支影片的狀態，與一個待決定的東西（outline／audio／final／publish），綁定所審內容的 SHA-256。
- [x] 預覽檔存在主機的 named volume `video_reviews`（掛在 API 容器 `/var/lib/mokaair/video-reviews`），以 SHA-256 命名；分段上傳（每段 ≤ 4 MiB，因為 nginx 6 MiB、API 5 MiB 上限），最後一段組合後核對雜湊。
- [x] 工具端點（影片工具權杖）：`PUT /video/reviews/{slug}` 回報狀態、`PUT /video/reviews/{slug}/files/{sha256}?part&parts&size` 上傳、`POST /video/reviews/{slug}/reviews` 送審、`GET /video/reviews/{slug}` 讀回決定。
- [x] 後台端點（`content.read`／`content.manage`）：`GET /admin/videos`、`GET /admin/videos/{slug}`、`POST /admin/videos/{slug}/reviews/{id}/decision`（寫稽核紀錄）、`GET /admin/videos/{slug}/files/{sha256}`（Range、不快取）。
- [x] 規則：同一關送不同內容 → 取代待審的舊版；送相同內容 → 回傳既有那一筆（退回過的不會變回待審）；退回一定要寫原因；大綱核准一定要選 A／B／C；沒有任何有效審核指到的檔案刪掉；影片已上 YouTube（回報了 video_id）就刪掉全部預覽。

## Steps

- [x] models、migration、config（`VIDEO_REVIEW_DIR`、單檔 400 MB、總量 20 GB）、Dockerfile 建目錄、docker-compose.prod.yml 掛 volume、.env.example。
- [x] `app/video_reviews/`：storage、schemas、admin_service、admin_api；main.py 掛上兩個 router。
- [x] 測試：`test_video_reviews.py`（檔案庫、規則、權限、上傳、Range）與 `test_video_reviews_integration.py`（CI 的 PostgreSQL 上跑完整流程）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_reviews.py
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_video_reviews_integration.py   # 需要 PostgreSQL
```

部署後：`docker volume ls | grep video_reviews`；API 容器裡 `/var/lib/mokaair/video-reviews` 屬於 app 使用者（uid 10001）。

## Notes

- 為什麼不用物件儲存：正式站沒設定 S3（新聞圖片存資料庫、上限 5 MiB），而 10 分鐘 720p 預覽約 100 MB。
- 錯誤碼都在路徑含 `admin` 的檔案裡丟（`admin_api.py`、`admin_service.py`），屬於 `test_error_localization` 的操作端豁免；`storage.py` 丟自己的 `StorageRefused`。
- 網頁與工具分別是 `2026-09-25-video-review-admin-page` 與 `2026-09-25-video-tool-pushes-reviews-and-pulls`。
