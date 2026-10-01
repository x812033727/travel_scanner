---
id: 2026-09-28-video-shorts-dropped-metrics
title: 撤掉的已公開 Shorts 在成效表一直顯示等待讀取
status: done
priority: P3
area: api
owner: claude-opus-5-5-shorts-metrics
claimed_at: 2026-10-01T03:39:06Z
created_at: 2026-09-28T16:52:01Z
completed_at: 2026-10-01T03:53:20Z
branch: claude/shorts-dropped-metrics
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_shorts/overview.py
  - apps/api/app/video_shorts/schemas.py
  - apps/web/components/admin-video-shorts-data.ts
  - apps/web/components/admin-video-shorts-metrics.tsx
  - apps/web/components/admin-video-shorts-metrics.test.tsx
  - apps/web/messages
  - apps/api/tests/test_video_shorts.py
---

# 撤掉的已公開 Shorts 在成效表一直顯示等待讀取

## Why

#935（`717e16280`）修掉了「YouTube 上已刪除的 Short 在成效表顯示『還沒到時間』」的誤導文字，但「撤掉」（dropped）的 Short 還有同樣的問題，這個問題在 #935 之前就存在。

- `stats.read_due`（`apps/api/app/video_shorts/stats.py:113-121`）跳過 `dropped_at` 不為空的影片，所以撤掉的 Short 不會再被讀成效。
- `overview.metrics_view`（`overview.py:253-262`）卻不過濾 `dropped_at`，成效表照樣列出它。
- `ShortMetrics`（API 端 `schemas.py:414-422`、web 端 `admin-video-shorts-data.ts:69-72`）沒有 `dropped_at`，頁面的 `blankReason`（:129）無從分辨，結果「現在」那一格永遠寫「等下一次讀取」。

要走到這個狀態並不容易：影片有 `youtube_video_id` 後，介面就不顯示撤掉鈕（`admin-video-reviews.tsx:336`），其他路徑也各自排除了撤掉的影片。但 `drop_project`（`apps/api/app/video_reviews/admin_service.py:811-826`）不會拒絕已上傳的影片，所以直接 `POST /admin/videos/{slug}/drop`，或詳情頁開著最多 60 秒、同時在另一個分頁認領上傳，就會走到。

2026-09-28 部署 `717e1628` 後的稽核找到的（兩個代理獨立確認）。

## Definition of done

擇一，並寫下理由：
- [ ] `drop_project` 拒絕已有 `youtube_video_id` 的影片（409 並說明要改用撤回），或
- [x] 成效表不列撤掉的 Short，或列出時寫「已撤掉，不再讀取」。

## Steps

- [x] 決定做法（前者最小，不必動 web）。
- [x] 補對應的 API 測試（與 web 測試，如果改了頁面）。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_shorts.py -q
cd apps/web && npx vitest run components/admin-video-shorts-metrics.test.tsx
```

## Notes

2026-10-01 claude-opus-5-5-shorts-metrics：選第二條路——成效表照樣列出撤掉的 Short，
但寫明「已放棄，不再讀取」。理由：

- 拒絕 `drop_project` 只能擋住以後的路徑，已經走到這個狀態的影片（若正式站有）還是會一直寫
  「等下一次讀取」；而且 `drop_project` 對所有格式共用，對已上傳的教學影片或漫劇加 409 會改到
  Shorts 以外的行為，還要一個五語的新錯誤碼。
- 已公開的 Short 被放棄時，在 YouTube 上它還是公開的，它在第 1 天讀到的數字仍然有用，
  所以列出來比藏起來好；跟 #935 處理「YouTube 上已刪除」的做法一致。

做法：API 的 `ShortMetrics` 多 `dropped_at`（`overview.metrics_view` 帶出
`VideoProject.dropped_at`）；web 的 `blankReason` 把「下架」與「放棄」都當成停止讀取的時刻，
取較早的那一個當理由：停止讀取前已關的時間窗仍是「沒有在時間窗內讀到」，之後的與「最新」寫
「已放棄，不再讀取」；列標題多一個「已於 {time} 放棄」的標籤。五個語系各加
`metrics.blank.dropped` 與 `metrics.dropped`（用詞沿用既有的 `dropped`／`droppedAt`：
放棄／放弃／中止／중단）。scope 加了 metrics 元件、它的測試、`apps/web/messages` 與 API 測試檔，
因為新字串與畫面要在那裡；`admin_service.py` 沒有改。

驗證：新 API 測試 `test_a_dropped_public_short_is_listed_with_when_it_was_dropped` 與欄位集合；
web 新增兩個測試（`blankReason` 的放棄與「下架、放棄取較早」、整列的畫面），把
`admin-video-shorts-data.ts` 還原時這兩個會紅。只在部署後生效。
