---
id: 2026-10-15-zero-root-yaozu-episode-4-storyboard
title: Zero-root Yaozu episode 4 storyboard
status: done
priority: P2
area: docs
owner: claude-opus-yaozu-e004
claimed_at: 2026-10-15T17:34:40Z
created_at: 2026-10-15T17:34:27Z
completed_at: 2026-10-15T17:51:15Z
branch:
depends_on: []
scope:
  - docs/videos/zero-root-yaozu-e004
---

# Zero-root Yaozu episode 4 storyboard

## Why

第 3 集分鏡寫完之後，接著寫第 4 集〈盆裡兩顆〉的分鏡劇本：付任何首格或影片點數之前要先定。開頭要接住第 3 集最後一格（胡家飯桌、油燈火苗舔上奶奶手上字條的紙角）。

## Definition of done

- [x] `docs/videos/zero-root-yaozu-e004/video.json`：37 鏡、約 86 秒（lint 估法）、lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題、validate.mjs ok。
- [x] `brief.md`、`script.md`（工具產生）與給人讀的 `storyboard.md`（含每鏡的參考圖）。

## Steps

- [x] 照 season-01.json 第 4 集的 hook、mid_hook、turn、satisfaction、cliffhanger、spectacle、glamour_shot 排六段（雞飼料的帳／盆裡兩顆／連裂紋都一樣／守夜／不能說／刀）。
- [x] 角色只有 lushi、grandma，外觀與聲音整段照抄第 3 集（細綱的 characters 也只有這兩人）。
- [x] 跑六個檢查並改到全過。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/zero-root-yaozu-e004/video.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zero-root-yaozu-e004/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zero-root-yaozu-e004/video.json --route hailuo --strict
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/zero-root-yaozu-e004/video.json --route hailuo --resolution 2k --strict
node tools/video/cli.mjs script --slug zero-root-yaozu-e004
node docs/videos/series-plans/zero-root-yaozu/validate.mjs
```

## Notes

- 估計 86 秒（lint 估法），細綱 85 秒。台詞 id 是 e4a01–e4a24。
- shot_plan（Hailuo H3 2K）：37 支都買 4 s；片段一次 1,776 點、期望 2,405、上限 3,552；風險 A 18、B 19、C 0（B 幾乎都是 speech.visible-mouth，另有 physics.fluid：s21、s23 的金色水紋、s35 刀尖碰盆沿）；小樣建議 s21–s23（水紋、驚醒、兩顆分成四顆）。
- 為了不買 5 s，每句台詞估計 ≤ 3.4 s（最多 10 個字）。
- 第一版 33 鏡只有 74 秒、三項沒過：pace.spread 1.7（補兩個 1 s 的動作鏡、把幾句台詞拉到 9–10 個字）、size.face 39%（補 s13、s16、s29、s30 四個臉）、size.reestablish 10 鏡（s33 改成全景）；章節「連裂紋都一樣」不到 10 秒，s14 改成 3 s 動作。
- 陷阱：「Close-up of Lushi on screen left … holding two stones」被 craft 讀成插鏡（拍東西的特寫），寫成「Close-up of Lushi's face」才讀成臉；「toward the house off screen right」「toward the kitchen off screen right」讀不出畫外是誰，改成「toward Grandma Hu off screen right」。
- 「對著太陽比」寫成 bright midday sky：提示詞不出現 sun 這個英文字（孫二的 id 是 sun）。
- 細綱寫「連放兩夜，兩顆變四顆」：第一夜 1→2（s06→s08），第二夜 2→4、銅錢成對（s18–s23）。
- 下一步：開拍鎖定（shot_plan／plan_lock）、首格（s01 用第 3 集 s44 的採用首格當構圖參考）、海螺影片、配音。
