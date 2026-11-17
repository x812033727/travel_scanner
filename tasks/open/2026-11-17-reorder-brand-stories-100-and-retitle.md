---
id: 2026-11-17-reorder-brand-stories-100-and-retitle
title: Reorder brand-stories-100 and retitle by reference-channel topic data
status: review
priority: P2
area: docs
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T00:04:50Z
created_at: 2026-11-17T00:04:19Z
completed_at:
branch: claude/wizardly-albattani-is0lls
depends_on: []
scope:
  - docs/videos/channel-review-20261116
---

# Reorder brand-stories-100 and retitle by reference-channel topic data

## Why

2026-11-16 站主要分析參考頻道黑猫研究院並照它的選題篩法排我們的品牌故事。量測結果是它起飛靠選題（觀眾自己用過的東西、規格與標準、日本品牌），不是做法；
我們 100 題的順序與標題還沒照這個排。報告與提案在 `docs/videos/channel-review-20261116/`。

## Definition of done

- [x] 頻道量測、篩法、100 題的分數、提案排程與標題提案寫在 `docs/videos/channel-review-20261116/`。
- [ ] 站主決定四個撞題（K01、A27、B05、B06）與要不要套用。
- [ ] 提案套用到 `docs/videos/story-plans/brand-stories-100/`（另開票或擴大這張票的 scope，見 Notes）。

## Steps

- [x] 用 yt-dlp 讀頻道 361 支的公開數字，和 10-31 快照比。
- [x] 起飛前後 18 支比對。
- [x] 替 100 題打四項分數，產生 `proposed-schedule.json`。
- [x] 寫 17 個標題提案。
- [ ] 套用（被擋，見 Notes）。

## How to verify

`python3 -c "import json;d=json.load(open('docs/videos/channel-review-20261116/proposed-schedule.json'));print(len(d['days']),len(d['scores']))"` 印出 `50 100`；
`npm run check:tasks` 通過。

## Notes

- 2026-11-17：`brand-stories-100` 的 `stories.json` 與 `SCHEDULE.md` 在票 `2026-10-14-correct-a21-pringles-patent-fact-and`（codex-8a78-a21，10-14 認領，
  工作已完成、卡在看板搬移）的 scope 裡。`claim` 拒絕重疊，`--force` 被自動模式擋下，所以這張票的 scope 縮成只有報告資料夾，沒有動題庫。
- 套用時要連動：各題 `reviews/<代號>.json` 要另一個人重讀重綁；`docs/videos/long-form/plans.json` 與 `apps/api/app/video_plans/data/catalog.json` 讀 `stories.json`，要重建。
- 分數是一個代理的判斷，不是量測；套用前站主可以直接改 `proposed-schedule.json` 的順序。
- 字幕只用來量結構，沒有存進 repo。
