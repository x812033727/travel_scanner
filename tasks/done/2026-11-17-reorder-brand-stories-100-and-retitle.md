---
id: 2026-11-17-reorder-brand-stories-100-and-retitle
title: Reorder brand-stories-100 and retitle by reference-channel topic data
status: done
priority: P2
area: docs
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T00:04:50Z
created_at: 2026-11-17T00:04:19Z
completed_at: 2026-11-19T16:29:04Z
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
- [x] 站主決定四個撞題（K01、A27、B05、B06）與要不要套用（2026-11-19 決定退役 `brand-stories-100`，改為篩選打分後移入奇聞 W 軸）。
- [x] 後續由奇聞 W 軸遷移與擴充票接手（不再改 `brand-stories-100` 排程）。

## Steps

- [x] 用 yt-dlp 讀頻道 361 支的公開數字，和 10-31 快照比。
- [x] 起飛前後 18 支比對。
- [x] 替 100 題打四項分數，產生 `proposed-schedule.json`。
- [x] 寫 17 個標題提案。
- [x] 2026-11-19 站主拍板退役 `brand-stories-100` 並篩選移入奇聞 W 軸，本票分析與提案階段結案。

## How to verify

`python3 -c "import json;d=json.load(open('docs/videos/channel-review-20261116/proposed-schedule.json'));print(len(d['days']),len(d['scores']))"` 印出 `50 100`；
`npm run check:tasks` 通過。

## Notes

- 2026-11-17：`brand-stories-100` 的 `stories.json` 與 `SCHEDULE.md` 在票 `2026-10-14-correct-a21-pringles-patent-fact-and`（codex-8a78-a21，10-14 認領，
  工作已完成、卡在看板搬移）的 scope 裡。`claim` 拒絕重疊，`--force` 被自動模式擋下，所以這張票的 scope 縮成只有報告資料夾，沒有動題庫。
- 2026-11-19：站主決定「品牌故事 100 題不要了，都移到 W 軸（篩選跟打分數過後）」，並從後台企劃目錄移除 `brand-stories`，同意結案本票。
- 分數是一個代理的判斷，不是量測。
- 字幕只用來量結構，沒有存進 repo。
