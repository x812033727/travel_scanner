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

## 2026-10-16 鉤子＋3D 國漫改版

站主 10-16：「一集應該要兩三個鉤子以上」，並從第 1 集起改拍成 3D 國漫（CG 動畫，不是真人）。點數不再那麼緊，可以往細綱的 95 秒長。

- 32 鏡 → 38 鏡、約 76 → 89 秒（lint；shot_plan 89.0 秒），細綱 95 秒 ±10 內。台詞 e7a01–e7a27（重新編號）。
- `look` 換成 3D 國漫（同第 6 集），motion 跟第 4、5 集同一句。角色的 id、外觀與聲音都沒動。
- 鉤子（storyboard.md 與 brief.md 都標了）：開場 s01「搜！」（0:00）；鉤子1 s04–s05 靴子踩上藏假靈石的地磚、陸拾屏氣（0:04）；鉤子2 s10–s13 全村一步護燈（0:19，刻意留到第 9／44 集）；鉤子3 s14–s15「執事，沒有。長老那邊……」「多嘴。」（0:28，第 10 集「嚴」令牌收，s01-t09）；鉤子4 s16–s18「我的人，看得清清楚楚。」（0:38）；鉤子5 s19–s21 信（0:44，第 8 集收）；鉤子6 s23 奶奶盯著信（0:53，第 8 集收）；轉折 s24–s27（0:55）；鉤子7 s32「這村的燈……記下來。」（1:13，第 8 集結尾燒燈收）；結尾 s38 手伸向地磚（1:26）。最長空檔 18 秒。
- 新增 6 鏡：s04 地磚、s05 陸拾屏氣、s14 弟子回報、s15「多嘴。」、s23 奶奶盯信、s32 記下燈；s20「是你從她房裡偷的。」改成錢通舉著信在畫面上說（原本是信的插入鏡配畫外音，信的插入鏡拿掉）。
- 新增的台詞：「執事，沒有。長老那邊……」（褐袍弟子）、「多嘴。」「這村的燈……記下來。」（錢通）。其餘台詞照舊。
- 檢查：lint 0 錯誤（只剩沒有 sources 的警告）、drama_craft 30 項全過、shot_reading --strict 0 陷阱（第一版 s15「toward the disciple off screen left」被讀成 cast.offscreen，改成 prompt 寫「a disciple off screen left」、motion 寫「glares toward screen left」後過）、shot_plan --strict 沒有問題；script.md 重新產生。
- shot_plan（Hailuo H3 2K）：38 支都買 4 s；片段一次 1,824 點、期望 2,477、上限 3,648；首格 38 張約 874 點；一次合計約 2,698 點。風險 A 18、B 20、C 0；小樣建議 s09–s11（抬腳踢燈、全村一步、三嬸）。
- 細綱第 7 集（10-16 版）的五個 hooks（20／40／50／66／78 s）本片都有；第五個細綱寫「抬不動米缸、單手提到一邊」，本片照原樣用院子的大石水缸一推就倒（米缸在 s06 已經被推倒；水缸是站主還沒定的事），寫在 brief.md 等站主決定。
- validate.mjs 這時候紅（960 個問題），全部是同時在改的細綱檔，沒有一筆是第 7 集。
