---
id: 2026-09-28-video-planner-counts-the-ai-shorts-folder
title: The video planner counts docs/videos/ai-shorts as a video it already made
status: done
priority: P3
area: tools
owner: claude-fable-5-1-planner
claimed_at: 2026-09-30T03:40:19Z
created_at: 2026-09-28T04:25:00Z
completed_at: 2026-09-30T03:50:16Z
branch: claude/video-planner-earlier-videos
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# The video planner counts docs/videos/ai-shorts as a video it already made

## Why

`tools/video/automation/flow.mjs` 的 `earlierVideos()` 把 `docs/videos` 底下**每一個資料夾**都當成一支做過的影片，不管裡面有沒有 `video.json` 或 `brief.md`。PR #871 加了 `docs/videos/ai-shorts/`（企劃、試片腳本、實驗紀錄），它不是一支影片，卻會以「代號 `ai-shorts`、標題空白、沒有來源文章」的樣子進到企劃模型看的「已經做過的影片」清單，代號也被當成已經用掉。

2026-09-28 規劃 Shorts 區時讀程式發現的，還沒有在正式站造成看得到的問題：主機工人的 `docs/videos` 是舊的 volume，裡面還沒有這個資料夾。volume 一更新（票 `2026-09-25-the-video-worker-s-docs-volume`）就會出現。

## Definition of done

- [x] `earlierVideos()` 只收有 `video.json` 或 `brief.md` 的資料夾。
- [x] 測試：`docs/videos` 底下放一個只有說明文件的資料夾，清單裡沒有它；有 `brief.md` 沒有 `video.json` 的草稿仍然在清單裡。

## Steps

- [x] 改 `earlierVideos()` 的篩選。
- [x] 加測試。

## How to verify

```bash
node --test tools/video/automation/automation.test.mjs
```

## Notes

- `2026-09-28-video-shorts-worker-lab` 也會改 `flow.mjs`；兩張票不要同時做，誰先拿到誰順手做掉這一項並在另一張票留一句。
- 2026-09-30 claude-fable-5-1-planner 用 `--force` 認領：scope 被 `2026-09-28-sothatswhy-shorts-from-episode`（claude-opus）的認領鎖住，那個認領超過 24 小時，本機、遠端都沒有它的分支，也沒有開著的 PR，照規則算過期。`2026-09-28-drama-listener-stale-check` 也在 scope 裡列了 `flow.mjs`，這裡只動 `earlierVideos()` 一個函式，合併時若撞到只會是文字相鄰。
- 做了什麼：`earlierVideos()` 讀 `docs/videos` 時，資料夾裡沒有 `video.json` 也沒有 `brief.md` 就跳過；有其中一個就照舊收進清單（只有 `brief.md` 的草稿用 brief 的第一個標題當標題）。工人自己的草稿與 /admin/videos 上的影片兩個來源沒有變。
- 測試：`automation.test.mjs` 加一條，在 sandbox 的 `docs/videos` 放一個只有說明文件的 `ai-shorts`、一個空資料夾、一個只有 `brief.md` 的草稿，清單只剩草稿與 fixture。拿掉篩選那一行時這條測試會紅，放回去就綠。
- 學到的：以 2026-09-30 的 main 來看，被排除的資料夾有 `ai-shorts`、`ai-terms`、`image-trust-opening-v2`、`imported-long-languages`、`series-plans`、`so-thats-why`、`story-plans`、`validation`。`image-trust-opening-v2` 是第一支長片（`01-image-trust`）的開場改版包，只有 `long-video.json`，不是一支新影片，排除它是對的；那支影片本身在 /admin/videos 上，企劃模型仍然看得到。
- 上面提到的 `2026-09-28-video-shorts-worker-lab` 已經在 `tasks/done/`，它沒有改 `earlierVideos()` 的篩選，所以這一項留到這張票做。
