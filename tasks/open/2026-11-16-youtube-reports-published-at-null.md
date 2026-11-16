---
id: 2026-11-16-youtube-reports-published-at-null
title: 頻道報表：overview 的 published_at 全是 null，videos／traffic 的公開後 N 天彙總用不了
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-11-16T02:00:51Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_youtube/reports.py
  - apps/api/tests
---

# 頻道報表：overview 的 published_at 全是 null，videos／traffic 的公開後 N 天彙總用不了

## Why

2026-11-16 每週頻道檢討時，`node tools/video/youtube-reports/cli.mjs overview` 回傳的 86 支影片 `published_at` 全是 null，所以 `videos --window 7` 回「no published video matches」，每週檢討只能自己用 channel_basic 第一天有觀看的日期當公開日。原因：`apps/api/app/video_youtube/reports.py` 第 527 行用的是 `project.youtube_publish_at`，那是排程公開時間，直接公開的影片沒有這個值。

## Definition of done

- [ ] `overview` 的 `published_at` 對已公開影片有值（實際公開時間；排程的取排程時間），`videos --window 7` 能列出上週的新片。

## Steps

- [ ] 找出站台存實際公開時間的欄位（上傳完成、改公開的時間，或 YouTube videos.list 的 snippet.publishedAt），沒有就補存。
- [ ] reports.py 改用它，`youtube_publish_at` 只當排程時的值；加 API 測試。

## How to verify

部署後跑 `node tools/video/youtube-reports/cli.mjs overview --json` 看 published_at，再跑 `videos --window 7`。

## Notes

暫代做法：每週檢討用 channel_basic 每支影片第一個 views>0 的太平洋日當公開日（2026-11-16 製片單就是這樣算）。
