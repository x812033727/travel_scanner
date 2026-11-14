---
id: 2026-11-14-video-unlink-youtube
title: 影片後台：已連結未記錄公開時間的影片可以解除 YouTube 連結，讓重推的新版重新上傳
status: done
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-11-14T13:44:16Z
completed_at: 2026-11-14T13:58:40Z
branch:
depends_on: []
scope:
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_youtube/vps.py
  - apps/api/tests/test_video_reviews_unlink_youtube.py
  - apps/api/tests/test_video_reviews_youtube.py
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-unlink-youtube.tsx
  - apps/web/components/admin-video-unlink-youtube.test.tsx
  - apps/web/messages
---

# 影片後台：已連結未記錄公開時間的影片可以解除 YouTube 連結，讓重推的新版重新上傳

## Why

站主（2026-11-14）：「有重推的如果狀態是已連結，未記錄公開時間 要解除狀態 讓我可以重新上傳」。
重做的一集重推之後，/admin/videos 上那支影片還記著舊版的 YouTube id（`youtube_video_id` 有值、
`youtube_publish_at` 空，卡片顯示「已連結，未記錄公開時間」），可以上架、送 YouTube、換版都把它當成
已經上傳，新版傳不上去。

## Definition of done

- [x] ContentManager 可以在「已連結，未記錄公開時間」的影片按「解除連結」，影片回到可以上架的狀態。
- [x] 已記錄公開時間（排程或已公開）、YouTube 同步進行中、已放棄的影片拒絕解除（409）。
- [x] 解除後，worker 或手動 review-push 從 video.json 再報同一個舊 id 不會把連結填回去。
- [x] 每次解除寫一筆稽核紀錄。

## Steps

- [x] `DELETE /admin/videos/{slug}/youtube` 與 `admin_service.unlink_youtube`。
- [x] `upsert_project` 不收站主解除過的 id；VPS `start` 不拿舊工作的同一個 id 當已知影片。
- [x] 後台「解除連結」按鈕（確認後呼叫 API、重新讀取）。
- [x] 五個語系的文案。
- [x] pytest 與 vitest。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_reviews_unlink_youtube.py tests/test_video_reviews_youtube.py
npm run test:web -- admin-video-unlink-youtube
```

## Notes

- Unlink clears `youtube_video_id`, `youtube_upload_session`, `youtube_sync` and
  `youtube_removed_at` (`youtube_publish_at` is already empty by precondition): the same five
  fields `_renewable_final` and the uploaders read as "already uploaded".
- The worker (`tools/video/automation/flow.mjs` `recorded()`/`report()`) and a hand review-push
  (`tools/video/review/sync.mjs`) send `youtube.video_id` from video.json on every report, and
  `recordVideoId` never overwrites an id video.json already has. Rather than teach both tools,
  the site remembers each unlinked id in its `video_youtube_unlinked` audit row and
  `upsert_project` ignores a reported id the owner unlinked from that slug (another id is still
  taken). The worker's video.json keeps the stale id; harmless for the site, but its own
  `auto.json` stays `done`. Not changed here (outside scope).
- The VPS uploader's last finished job also names the old id: `vps.start` no longer treats it as
  the known video, and `assert_idle(upload=True)` no longer refuses an API upload because of it.
- A new publish review for a linked-without-publish-time video does not auto-unlink: unlinking
  stays an explicit owner action.
- The API's twin check (`_same_title_on_channel`) still refuses to upload a second video with the
  same title while the old one is on the channel; the owner deletes it in Studio or uses the
  Studio route.
- Done by claude-opus on branch claude/video-unlink-youtube. Never claimed: `claim --force` (needed
  because older video tickets list the same admin files) was refused by the session permission
  check, so owner and branch above are empty.
