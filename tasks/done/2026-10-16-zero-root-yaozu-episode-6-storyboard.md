---
id: 2026-10-16-zero-root-yaozu-episode-6-storyboard
title: Zero-root Yaozu episode 6 storyboard
status: done
priority: P2
area: docs
owner: claude-opus-yaozu-e006
claimed_at: 2026-10-16T03:18:57Z
created_at: 2026-10-16T03:18:37Z
completed_at: 2026-10-16T03:37:01Z
branch:
depends_on: []
scope:
  - docs/videos/zero-root-yaozu-e006
---

# Zero-root Yaozu episode 6 storyboard

## Why

第 5 集分鏡寫完之後，接著寫第 6 集〈盆的規矩〉的分鏡劇本：付任何首格或影片點數之前要先定。開頭要接住第 5 集最後一格（第九天深夜的小臥房，窗紙破洞後那隻眼睛跟著陸拾數「三十二。」）。這次海螺帳號只剩約 1,816 點，鏡數要壓緊。

## Definition of done

- [x] `docs/videos/zero-root-yaozu-e006/video.json`：32 鏡、約 70 秒（lint 估法）、lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題、validate.mjs ok。
- [x] `brief.md`、`script.md`（工具產生）與給人讀的 `storyboard.md`（含每鏡的參考圖）。

## Steps

- [x] 照 season-01.json 第 6 集的 hook、mid_hook、turn、satisfaction、cliffhanger、spectacle、glamour_shot 排四段（推窗／盆的規矩／假靈石／銅鑼）。
- [x] 角色沿用 lushi、azheng、gui（外觀與聲音照抄第 3 集）與 watcher（照抄第 5 集，另加 `shot_looks` 的 `night-runner` 夜行衣造型）；新增 qian（錢通，gemini:Achird）與 disciple（褐袍弟子，gemini:Orus），兩個聲音都是代理暫定、沒有試聽。
- [x] 跑六個檢查並改到全過。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/zero-root-yaozu-e006/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zero-root-yaozu-e006/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zero-root-yaozu-e006/video.json --route hailuo --strict
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/zero-root-yaozu-e006/video.json --route hailuo --resolution 2k --strict
node tools/video/cli.mjs script --slug zero-root-yaozu-e006
node docs/videos/series-plans/zero-root-yaozu/validate.mjs
```

## Notes

- 估計 70 秒（drama_craft_check）／71.3 秒（shot_plan），細綱 85 秒：為了點數刻意壓在 32 鏡。台詞 id 是 e6a01–e6a19。
- shot_plan（Hailuo H3 2K）：32 支都買 4 s；片段一次 1,536 點、期望 2,117、上限 3,072；首格 32 張約 736 點；一次合計約 2,272 點，已經超過帳號剩下的約 1,816 點（第 6、7 兩集合計約 4,544 點）。風險 A 13、B 19、C 0（B 多半是 speech.visible-mouth，另有 s02／s03 action.fast、s04／s12／s15 physics.fluid、s29／s31 crowd）；小樣建議 s01–s03（推窗、屋頂、巷口）。
- 錢通的 id 取 `qian`、提示詞寫 Qian Tong：`nameOf` 拿「Qian Tong」比對時，`qian` 這個標籤讀得到（跟 Grandma Hu → grandma 同一套）。
- 窗外的人細綱沒寫身分：本集讓他在池塘掉了一條繡著玄穹宗雲紋的褐布（細綱 knowledge「有宗門的人在盯他」），第 7 集錢通再說「我的人，看得清清楚楚。」；全身鏡用 watcher 的 `shot_looks`（night-runner），基本外觀與聲音不動。
- 細綱寫「一天放兩次只有第一次有用」：第 4、5 集都是夜裡變的，本集台詞寫「一晚上……只認一次？」。
- 灰影撞上阿猙那一下不拍（兩人接觸是 C 風險），s03 衝向他、s04 已經在水裡。
- pace.spread 一度 2.0（< 2）：把四句台詞拉長（s10、s16、s22、s24）、s09／s27 改 1 s、s23 改 3 s 之後過。shot_reading 一度兩個 cast.offscreen（s05「splashing off screen left」、s20「the hissing kitten off screen right」），改寫成不說 off screen 之後 0 陷阱。
- 章節第一版有三段不到 10 秒（小貓、假靈石、魚簍），併成四段。
- 下一步：站主確認 qian／disciple 的聲音、決定點數要先花在哪幾鏡；開拍鎖定（shot_plan／plan_lock）、首格（s01 用第 5 集 s35／s37 的採用首格當構圖參考）、海螺影片、配音。

## 2026-10-16 鉤子＋3D 國漫改版

站主 10-16：「一集應該要兩三個鉤子以上」，並從第 1 集起改拍成 3D 國漫（CG 動畫，不是真人）。點數不再那麼緊，可以往細綱的 85 秒長。

- 32 鏡 → 36 鏡、約 70 → 80 秒（lint；shot_plan 81.0 秒），細綱 85 秒 ±10 內。台詞 e6a01–e6a21（重新編號）。
- `look` 換成 3D 國漫（UE5 算圖、半寫實美型臉、冷調灰藍加燈籠暖光、體積光與輪廓光；負面詞排除 photograph／live action／real person／photorealistic skin／UI），motion 跟第 4、5 集同一句。角色的 id、外觀與聲音都沒動。
- 鉤子（storyboard.md 的鏡頭列與 brief.md 的「鉤子」表都標了）：開場 s01 推窗「誰！」（0:00）；鉤子1 s09–s10 褐布雲紋跟靈石的印對上「同一個印……衝著靈石來的。」（0:15）；鉤子2 s14 第二顆不變（0:27）；鉤子3 s21 盆底金光眨眼（0:43，刻意留到第 18／19／35 集）；鉤子4 s26–s27 一滴水沖掉假靈石的光「沾水就掉……只要別下雨。」（0:56，第 8 集雨夜收）；鉤子5 s32 銅鑼進村（1:09）；鉤子6 s35「失竊……？」（1:17，第 7、8 集的信收）；結尾 s36「就是他。」（1:19）。最長空檔 16 秒。
- 新增 4 鏡：s09（靈石與褐布對雲紋，取代原本只拍褐布的插入鏡）、s22（「活的……它不收。」改成陸拾在畫面上說，原本是畫外音蓋在盆的插入鏡上）、s26／s27（水滴與「沾水就掉……只要別下雨。」）、s35（「失竊……？」）。
- 改的台詞：「玄穹宗的人……一直在盯我。」→「同一個印……衝著靈石來的。」；新增「沾水就掉……只要別下雨。」「失竊……？」。
- 檢查：lint 0 錯誤（只剩沒有 sources 的警告）、drama_craft 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題；script.md 重新產生。第一版 37 鏡時插入鏡 27%（> 25%），把只拍褐布的 s09 併進對雲紋的那一鏡；兩句台詞估計超過 3.5 s 要買 5 s，縮短。
- shot_plan（Hailuo H3 2K）：36 支都買 4 s；片段一次 1,728 點、期望 2,405、上限 3,456；首格 36 張約 828 點；一次合計約 2,556 點。風險 A 13、B 23、C 0；小樣建議 s01–s03。
- validate.mjs 這時候紅（960 個問題），全部是同時在改的細綱檔（S01 第 21 集以後與第 2–10 季的 `mid_hook is replaced by hooks`／`needs at least 3 hooks`），沒有一筆是第 6 集。
- 細綱第 6 集（10-16 版）的四個 hooks（18／36／50／66 s）本片都有，落在 0:15／0:27／0:39–0:47／0:50–1:08。
