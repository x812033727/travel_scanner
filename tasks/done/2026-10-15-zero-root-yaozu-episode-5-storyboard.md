---
id: 2026-10-15-zero-root-yaozu-episode-5-storyboard
title: Zero-root Yaozu episode 5 storyboard
status: done
priority: P2
area: docs
owner: claude-opus-yaozu-e005
claimed_at: 2026-10-15T17:34:45Z
created_at: 2026-10-15T17:34:30Z
completed_at: 2026-10-15T17:51:18Z
branch:
depends_on: []
scope:
  - docs/videos/zero-root-yaozu-e005
---

# Zero-root Yaozu episode 5 storyboard

## Why

第 4 集分鏡寫完之後，接著寫第 5 集〈越疊越多〉的分鏡劇本：付任何首格或影片點數之前要先定。開頭要接住第 4 集最後一格（傍晚雞舍前，陸拾捧著奶奶的豆腐刀、刀尖碰到盆沿，奶奶在背後問「拾兒，你在幹嘛？」）。

## Definition of done

- [x] `docs/videos/zero-root-yaozu-e005/video.json`：39 鏡、約 89–90 秒（lint 估法）、lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題、validate.mjs ok。
- [x] `brief.md`、`script.md`（工具產生）與給人讀的 `storyboard.md`（含每鏡的參考圖）。

## Steps

- [x] 照 season-01.json 第 5 集的 hook、mid_hook、turn、satisfaction、cliffhanger、spectacle、glamour_shot 排七段（刀不准碰／越疊越多／錢莊／書攤／孝敬／吸不進去／三十二）。
- [x] 角色沿用 lushi、grandma、tuantuan（外觀與聲音照抄第 3 集）；新增 clerk（錢莊夥計，gemini:Sadaltager）與 watcher（窗外的人，只露一隻眼睛，gemini:Charon），兩個聲音都是代理暫定、沒有試聽。
- [x] 跑六個檢查並改到全過。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/zero-root-yaozu-e005/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zero-root-yaozu-e005/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zero-root-yaozu-e005/video.json --route hailuo --strict
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/zero-root-yaozu-e005/video.json --route hailuo --resolution 2k --strict
node tools/video/cli.mjs script --slug zero-root-yaozu-e005
node docs/videos/series-plans/zero-root-yaozu/validate.mjs
```

## Notes

- 估計 89 秒（drama_craft_check）／90.3 秒（shot_plan），細綱 90 秒。台詞 id 是 e5a01–e5a28。
- shot_plan（Hailuo H3 2K）：39 支都買 4 s；片段一次 1,872 點、期望 2,534、上限 3,744；風險 A 19、B 20、C 0（B 多半是 speech.visible-mouth，另有 s05 physics.fluid、s18 hands.weapon）；小樣建議 s11–s13（夥計瞧不起、靈石一拍、夥計坐直）。
- 第一版有兩個 C 風險：s22 團團從陸拾手上接過糖葫蘆（contact.two-person）、s23 團團邊吃邊說（eat-drink）；改成糖葫蘆一開始就在她懷裡、用糖葫蘆指人之後是 0 個 C。
- s03「Lushi slumps down」被讀成只有看或呼吸的全景（motion.look），改成「sits down hard」。
- 細綱寫「八、十六、三十二」：s07 只喊「滿……滿盆了！」，「三十二」留給結尾第一次說出口；否則換錢花一顆、吸碎一顆之後床底還是三十二，算術對不上。
- 錢莊夥計沒有參考圖，s11、s13、s14、s17 都是他的臉：開拍前先畫一張定妝照。青石鎮的街、錢莊、書攤、陸拾的臥房都沒有場景圖，提示詞寫全了。
- 窗外的人身分細綱沒寫：本集 `characters` 列 watcher 只為了讓說話的人對得上角色；第 6 集決定是誰之後再換外觀與聲音。
- 標題第一版 44 個全形字寬（手機上限 36），改成「雞盆變出三十二顆靈石，窗外卻有雙眼睛跟著他數｜長燈村 第5集」；縮圖字原本「三十二顆」跟標題重複，改成「窗外有眼」。
- 下一步：夥計定妝照、開拍鎖定（shot_plan／plan_lock）、首格（s01 用第 4 集 s37 的採用首格當構圖參考）、海螺影片、配音。

## 2026-10-16 鉤子＋3D 國漫改版

站主 10-16：「一集應該要兩三個鉤子以上」，整部從第 1 集起改拍 3D 國漫（CG 動畫，不是真人）。

- `look` 換成 3D 國漫 CG（同第 4 集）；負面詞排除照片與真人感。角色 id、外觀、聲音不動（clerk、watcher 仍是代理暫定聲音）。
- 39 鏡、約 90 秒（shot_plan 89.8 s），細綱 90 秒；台詞 28 → 27 句，e5a01–e5a27。
- 鉤子：開場 s01（老手從盆沿抄走豆腐刀）＋中段六個（s03／s05 奶奶看盆、「她……看見了吧？」0:03–0:08、s08 滿盆 0:14、s09–s10 屋頂瓦片一響「誰在上面？」0:16–0:18、s17–s18「玄穹宗的印？」0:33–0:35、s26 團團「會出事喔」0:54、s34–s35 靈石碎成灰 1:13–1:16）＋結尾 s38–s39；最長空檔約 19 秒。細綱 `hooks` 的四個（18／42／62／78 s）都在片裡。
- 鏡頭與台詞改動：開頭雙人鏡「奶奶從他手上奪刀」（兩人接觸）改成 s01 插鏡：刀已掉在盆沿、只有奶奶的手抄走，「刀不准碰。」移到 s02 奶奶自己說，新增 s03 奶奶看盆的特寫；「八顆。」（畫外）＋「十六……」併成 s07「八顆……十六……」；新增 s09「……誰在上面？」與 s10 屋瓦插鏡（接第 6 集開頭屋頂上的灰影）；「奶奶的新刀、團團的糖……」→「貓吧……新刀、糖葫蘆……」；「就這本！」（畫外）刪掉，s23 書本插鏡改成無台詞；老手推回紅紙包的插鏡併進 s29 奶奶「舊的順手。」；刪掉天亮垮坐與拖木盒兩鏡；「三十、三十一……」（畫外插鏡）→ s36 陸拾在畫面裡數「二十九、三十、三十一……」。縮圖鏡 s07 → s08（滿盆那一鏡）。
- 章節：第一版改完「刀不准碰」「書攤」「三十二」三段不到 10 秒，加 s03、s23 改 2 s、s38 改 3 s、s36 台詞拉長之後過；pace.spread 一度 1.8，s10 改 1 s 之後過。
- 檢查：lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題（A 17、B 22、C 0；B 是 speech.visible-mouth、s06 physics.fluid、s21 hands.weapon）、script 重產。validate.mjs 目前紅（細綱第 41 集以後 mid_hook → hooks，另一條線在改）。
- 估價：片段一次 1,872 點、期望 2,563、上限 3,744；首格 39 張約 897 點；一次合計約 2,769 點；夥計定妝照另約 23 點。
- 等站主：參考圖要不要重做成 3D 國漫版（同第 4 集）；夥計定妝照；clerk／watcher 的聲音試聽。
