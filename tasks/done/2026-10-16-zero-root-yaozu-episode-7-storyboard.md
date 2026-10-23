---
id: 2026-10-16-zero-root-yaozu-episode-7-storyboard
title: Zero-root Yaozu episode 7 storyboard
status: done
priority: P2
area: docs
owner: claude-opus-yaozu-e007
claimed_at: 2026-10-16T03:20:18Z
created_at: 2026-10-16T03:18:41Z
completed_at: 2026-10-16T03:37:08Z
branch:
depends_on: []
scope:
  - docs/videos/zero-root-yaozu-e007
---

# Zero-root Yaozu episode 7 storyboard

## Why

第 6 集分鏡寫完之後，接著寫第 7 集〈她說你偷的〉的分鏡劇本：付任何首格或影片點數之前要先定。開頭要接住第 6 集最後一格（村口，錢通的令牌直直指著陸拾「就是他。」）。這次海螺帳號只剩約 1,816 點，鏡數要壓緊。

## Definition of done

- [x] `docs/videos/zero-root-yaozu-e007/video.json`：32 鏡、約 76 秒（lint 估法）、lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題、validate.mjs ok。
- [x] `brief.md`、`script.md`（工具產生）與給人讀的 `storyboard.md`（含每鏡的參考圖）。

## Steps

- [x] 照 season-01.json 第 7 集的 hook、mid_hook、turn、satisfaction、cliffhanger、spectacle、glamour_shot 排五段（搜／燈籠／信／撿的／縛仙索）。
- [x] 角色沿用 lushi、grandma、tuantuan、aunt（外觀與聲音照抄第 3、5 集）與第 6 集新增的 qian、disciple（照抄第 6 集）。
- [x] 跑六個檢查並改到全過。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/zero-root-yaozu-e007/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zero-root-yaozu-e007/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zero-root-yaozu-e007/video.json --route hailuo --strict
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/zero-root-yaozu-e007/video.json --route hailuo --resolution 2k --strict
node tools/video/cli.mjs script --slug zero-root-yaozu-e007
node docs/videos/series-plans/zero-root-yaozu/validate.mjs
```

## Notes

- 估計 76 秒（drama_craft_check）／75.8 秒（shot_plan），細綱 95 秒：為了點數刻意壓在 32 鏡。台詞 id 是 e7a01–e7a24。
- shot_plan（Hailuo H3 2K）：32 支都買 4 s；片段一次 1,536 點、期望 2,102、上限 3,072；首格 32 張約 736 點；一次合計約 2,272 點。風險 A 14、B 18、C 0；小樣建議 s07–s09（抬腳踢燈、全村一步、三嬸）。
- 第一版兩個 C 風險都是 hands.small-prop（令牌小動作）：s11「令牌敲下巴」改成往後退一步、s23「把令牌拋起來接住」改成倚門抱胸（細綱的「甩令牌」改由袍子下擺甩開表現）。
- drama_craft 第一版兩項沒過：longest run without a wide 11 鏡（s18 改成雙人鏡）；silent shots 9%（拿掉 s21 眼睛特寫、s21 奶奶加一聲「拾兒。」、s31 加錢通畫外「想好了嗎？」）。章節「水缸」不到 10 秒，併進「撿的」。
- 細綱的 face_slap（後半）沒寫是什麼：本集寫成兩個弟子抬不動的大石水缸，陸拾一個人推倒（他挑水砍柴的力氣，第 2 集扁擔掃斷樹枝同一套），錢通「零靈根……力氣倒不小。」；站主可以換。
- 錢通「三十二顆，交出來。」「我的人，看得清清楚楚。」把第 5 集窗外那隻眼睛定成錢通的人；要保留懸念可以把後一句改成「有人，看得清清楚楚。」。
- 床在 s03 被掀起來，假靈石袋藏在床底的地磚下（第 6 集 s25），所以沒被搜到；結尾陸拾的手伸向那塊地磚，接第 8 集開頭拖出一袋發光的「靈石」。
- 下一步：開拍鎖定（shot_plan／plan_lock）、首格（s01 用第 6 集 s32 的採用首格當構圖參考）、海螺影片、配音。
