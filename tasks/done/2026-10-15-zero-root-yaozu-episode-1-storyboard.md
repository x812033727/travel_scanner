---
id: 2026-10-15-zero-root-yaozu-episode-1-storyboard
title: Zero-root Yaozu episode 1 storyboard: video.json, brief and a readable shot list
status: done
priority: P2
area: docs
owner: claude-opus-5-5-yaozu-e001
claimed_at: 2026-10-15T07:04:18Z
created_at: 2026-10-15T07:04:15Z
completed_at: 2026-10-15T07:04:23Z
branch:
depends_on: []
scope:
  - docs/videos/zero-root-yaozu-e001
---

# Zero-root Yaozu episode 1 storyboard: video.json, brief and a readable shot list

## Why

站主 2026-10-15「繼續，寫第 1 集分鏡劇本」。參考圖已做完，下一步是第 1 集的分鏡，付任何首格或影片點數之前要先定。

## Definition of done

- [x] `docs/videos/zero-root-yaozu-e001/video.json`：34 鏡、lint 0 錯誤、drama_craft_check 30 項全過、shot_reading 0 陷阱。
- [x] `brief.md`、`script.md`（工具產生）與給人讀的 `storyboard.md`。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/zero-root-yaozu-e001/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zero-root-yaozu-e001/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zero-root-yaozu-e001/video.json --route hailuo
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/zero-root-yaozu-e001/video.json --route hailuo --resolution 2k
```

## Notes

- 估計 79 秒（lint 估法），細綱寫 95 秒；真人語速通常再長一成。
- shot_plan（Hailuo H3 2K）：片段一次 1,656 點、期望 2,321、上限 3,312；首格 34 張約 700 點。
- shot_reading 曾把「Yan Shaoyuan off screen right」錯接到雲知意（s21），改寫 prompt 避開，不是真的畫外。
- 本 worktree 沒有 node_modules：用 junction 指向另一個 worktree 的 node_modules 才跑得了 lint（pinyin-pro）。
- 下一步：開拍鎖定（animation-preproduction 的 shot_plan／plan_lock）、首格、海螺影片、配音。
