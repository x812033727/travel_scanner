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

## 2026-10-16 鉤子＋3D 國漫改版

站主 2026-10-16：「一集應該要兩三個鉤子以上」，而且從第 1 集起改拍 3D 國漫（國漫 CG）。

- `look` 換成 3D 國漫（UE5 電影感渲染、半寫實 CG 角色、冷灰藍底色配暖色燈火、體積光與霧；negative 擋 photograph／live action／real person／photorealistic skin／text／subtitles／watermark／UI）；`motion` 拿掉 realistic。角色 id、外觀與聲音不動。
- 34 鏡改成 38 鏡、約 92 秒（shot_plan；lint 91 秒；細綱 95 秒），鏡號與台詞 id 從頭重編（s01–s38、e1a01–e1a32），縮圖改指 s13（金紅光柱）。全部買 4 s（台詞估計都 ≤ 3.4 s）：片段一次 1,824 點、期望 2,534、上限 3,648；首格 38 張約 874 點；一次約 2,698 點。風險 A 14、B 24、C 0。
- 鉤子（storyboard.md 鏡頭列標【開場鉤子】【鉤子1–7】【結尾懸念】，brief.md 有表）：0:00 手拍黑石「零——。」／0:17 只有雲知意不笑（新增 s08）／0:31「什麼味道？」／0:45 嚴崇「零靈根……哪來這把力氣？」／0:55–0:57 握拳＋嚴少淵把劍頂出一指「零靈根想動手？」（新增 s24）／1:00 雲知意擋下／1:20「回家再打開。別讓人看見。」／1:26 沒風的樹枝自己晃／1:30「嘻。」。最長空檔約 17 秒。
- 新增鏡：s07 陸拾額頭抵著黑石「說好要寄錢回家的……」、s08 雲知意不笑、s24 嚴少淵頂劍、s30 雲知意「下山吧。」獨立成鏡。
- 改的台詞：「問天石不說謊。」→「問天石，從不說謊。」；「少淵，讓他看看什麼叫天才。」→「少淵，讓他開開眼。」；「我奶奶醃的菜。」→「我奶奶醃的菜，拜師禮。」；「嗯？」→「零靈根……哪來這把力氣？」；「我自己會走。」→「挑了十年水。我自己會走。」；「那是我奶奶醃了三個月的……」→「奶奶醃了三個月的……」；「知意，妳替他說話？」→「知意，妳替零靈根說話？」；「妳……為什麼？」→「妳……為什麼幫我？」；「回家再看。」→「回家再打開。別讓人看見。」（跟第 8 集字條「藏好，有人跟著你」接得上）；「誰？」→「沒風啊……誰？」。
- 不接觸：嚴少淵不再用肩膀撞人（直直走過去，陸拾自己退開）；兩個執事改成拽罈子的繩耳；罈子是放到他腳前、饅頭是伸長手臂遞出。s16 的 hugs 被 shot_plan 讀成 contact.two-person（C），改寫成 clutches。
- 霧路的鏡頭寫進「罈子繩套裡插著短竹扁擔」，第 2 集 s02 從繩套抽扁擔才接得上。
- 檢查：lint 0 錯誤、drama_craft_check 30 項全過、shot_reading --strict 0 陷阱、shot_plan --strict 沒有問題、script 重產；validate.mjs ok（10 季 600 集）。
- 過程：pace.spread 一度 1.9、size.reestablish 一度 14 鏡沒有全景（s19 執事、s25 雲知意擋人改成全景後過）；s30 一度 motion.look（改成她往下一階遞饅頭）。
- 等站主：refs 是真人劇照質感，3D 版要不要先重畫 3D 角色參考；新加的兩句台詞（拜師禮、寄錢回家）合不合角色。
