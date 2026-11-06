---
id: 2026-10-28-ershou-chongsheng-season-one-plan-e001
title: 新漫劇《我的重生系統是二手的》第一季 72 集企劃包與第 1 集製作檔
status: review
priority: P2
area: docs
owner: claude-fable
claimed_at: 2026-10-28T04:21:23Z
created_at: 2026-10-28T04:21:21Z
completed_at:
branch: claude/pensive-bell-o7fimo
depends_on: []
scope:
  - docs/videos/series-plans/ershou-chongsheng
  - docs/videos/ershou-chongsheng-e001
---

# 新漫劇《我的重生系統是二手的》第一季 72 集企劃包與第 1 集製作檔

## Why

站主 2026-10-28 要開第三部漫劇，定了：都市重生系統（避開古裝修仙）、3D 國漫 CG 加 Colab 開源 H3（跟《修仙獎勵》同一條）、第一季 6 篇 × 12 集的企劃包加第 1 集製作檔、故事核心「二手重生系統」。這張票是把企劃包與第 1 集寫到「站主看一次鎖定包就能開拍」的狀態；不花錢、不建站上作品、不生成媒體。

## Definition of done

- [x] `docs/videos/series-plans/ershou-chongsheng/`：README、setting、chapter-01…06、spine-13-72、production/cast.json
- [x] 每集三個不同的鉤子、兩個以上爽點、結尾類型相鄰不重複、主角不連輸、連續四集至少收一條線、謎團照表揭一次（人工逐集對過；跨篇一致性由另一個分身對過一輪）
- [x] 第 1 集：brief.md、video.json（42 鏡）、overlays.json、storyboard.md、script.md；lint 0 錯誤、`drama_craft_check` 30 列全過、`shot_reading --route hailuo --strict` 0 陷阱、`shot_plan --strict` 沒有「會白花」（C 級 0）
- [x] 開拍鎖定包 `production/e001-lock-package.md`、鎖定檔 `e001-plan-lock.json`（`plan_lock --write --assist off`）、H3 與伺服器兩份分鏡表、Colab 的 manifest 與正文（SHA-256 等於鎖定檔）
- [x] 站主看過鎖定包第 0 節的五件事（片名、集長、聲音、小樣、zhouye32）：2026-10-28「五件事都照建議」，鎖定檔已帶原話重寫

## Steps

- [x] 讀 animation-preproduction、youtube-video、《修仙》與《種田》的企劃包，問站主題材、畫風、規模、故事核心
- [x] cast.json、setting.md、chapter-01.md、spine-13-72.md
- [x] chapter-02…06 由五個平行分身照 spine 寫，再由一個分身對跨篇一致性
- [x] 第 1 集用一支一次性生成腳本（scratchpad，不進 repo）從同一份資料出 video.json、storyboard.md、overlays.json
- [x] 四個離線檢查、shot_plan、plan_lock、colab manifest
- [x] 站主確認鎖定包 → 票 `2026-10-28-ershou-e001-colab-pilot-to-cut`

## How to verify

```bash
node tools/video/cli.mjs lint --slug ershou-chongsheng-e001
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/ershou-chongsheng-e001/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/ershou-chongsheng-e001/video.json --route hailuo --strict
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/ershou-chongsheng-e001/video.json --route hailuo --plan hailuo:pro --hailuo-model h3 --resolution 2k --pilot s29,s30,s31 --strict
node .agents/skills/animation-preproduction/scripts/plan_lock.mjs --file docs/videos/ershou-chongsheng-e001/video.json --workdir <有 plan/lock.json 的目錄> --route hailuo --plan hailuo:pro --hailuo-model h3 --resolution 2k --pilot s29,s30,s31 --check
```

## Notes

- 三十二歲的周野另開角色 id `zhouye32`（同一張臉老十年、雨衣安全帽），只在第 1 集前 6 鏡；兩個 id 都在 cast.json。
- `look.style` 上限 600 字：沿用《修仙》原句，現代都市的場景字寫在每鏡 prompt，不塞進 style。
- craft 把 `close-up of <人> … hand/pen/folder` 讀成插鏡（size.agree）：臉的特寫把道具放到分號後的子句；`swallow`、`handwriting`、`lifts … page` 會被讀成 eat-drink、text.readable、hands.small-prop。
- 畫外說話者一律寫「<Name> speaks off screen」或「toward <Name> off screen right」，寫「his brother」「the door off screen」會被 shot_reading 報 cast.offscreen。
- 鎖定檔的 `--note` 是代理寫的，站主點頭後若要留站主原話就 `--write --force --note`。
