---
id: 2026-10-15-zero-root-yaozu-episode-2-storyboard
title: Zero-root Yaozu episode 2 storyboard
status: done
priority: P2
area: docs
owner: claude-opus-yaozu-e002
claimed_at: 2026-10-15T11:39:29Z
created_at: 2026-10-15T11:39:20Z
completed_at: 2026-10-15T11:39:58Z
branch:
depends_on: []
scope:
  - docs/videos/zero-root-yaozu-e002
---

# Zero-root Yaozu episode 2 storyboard

## Why

第 1 集分鏡寫完之後，接著寫第 2 集〈山魈倒掛〉的分鏡劇本：付任何首格或影片點數之前要先定。開頭要接住第 1 集最後一格（霧路上倒掛的猴臉）。

## Definition of done

- [x] `docs/videos/zero-root-yaozu-e002/video.json`：36 鏡、約 84 秒（lint 估法）、lint 0 錯誤、drama_craft_check 30 項全過、shot_reading 0 陷阱、shot_plan --strict 沒有問題。
- [x] `brief.md`、`script.md`（工具產生）與給人讀的 `storyboard.md`（含每鏡的參考圖）。

## Steps

- [x] 照 season-01.json 第 2 集的 hook、mid_hook、turn、satisfaction、cliffhanger、spectacle、glamour_shot 排四段。
- [x] 角色沿用第 1 集的 lushi、shanxiao，新增 azheng（setting.json 的外觀，聲音 gemini:Alnilam）。
- [x] 跑五個檢查並改到全過。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/zero-root-yaozu-e002/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zero-root-yaozu-e002/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zero-root-yaozu-e002/video.json --route hailuo
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/zero-root-yaozu-e002/video.json --route hailuo --resolution 2k --strict
node tools/video/cli.mjs script --slug zero-root-yaozu-e002
```

## Notes

- 估計 83.8 秒（lint 估法），細綱寫 80 秒；真人語速通常再長一成。台詞 id 是 e2a01–e2a26（LINE_ID 是 `^[a-z0-9]{4,8}$`，跟第 1 集的 e1aNN 不撞）。
- shot_plan（Hailuo H3 2K）：片段一次 1,740 點、期望 2,304、上限 3,480；風險 A 21、B 15、C 0；只有 s29（阿猙出場的顏值鏡，4 s 動作）買 5 s，其餘 4 s。
- 扁擔是細綱的道具、第 1 集沒有交代：s02 用插鏡讓陸拾從裂罈的繩套裡抽出一根短竹扁擔。
- 細綱的 state.time 寫「回程第三夜」，但本集照指示從第 1 集最後一格直接接下去（同一個黃昏轉夜）；細綱這一格與「十里坡就在村外」的地理之後要不要改，留給站主。
- 提示詞裡阿猙寫成 Azheng：shot_reading 的 `nameOf` 讀不出「A-Zheng」（連字號、只有一個大寫字母），畫外的子句會被誤接到說話的人；寫成 Azheng 就對上角色 id。
- craft 的 `isInsert` 把「Close-up of Lu Shi on screen right」讀成插鏡（OBJECT 有 screen、NOT_A_MODIFIER 沒有 on）；臉的近景在 prompt 寫「Lu Shi's face」就讀對。第 1 集的近景剛好都有 face 字。
- 「The three monkey faces …」被 isLookOnly 的 faces（面向）那組字讀成只是站著：改寫成 monkey heads。
- 下一步：開拍鎖定（shot_plan／plan_lock）、首格（s01 用第 1 集 s32 的採用首格當構圖參考）、海螺影片、配音。
