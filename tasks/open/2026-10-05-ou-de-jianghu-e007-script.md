---
id: 2026-10-05-ou-de-jianghu-e007-script
title: 《偶的江湖》第 7 集劇本：西嶺來客（22 分鐘長篇動畫）
status: in-progress
priority: P2
area: docs
owner: claude-fable-local
claimed_at: 2026-10-05T14:34:07Z
created_at: 2026-10-05T14:33:09Z
completed_at:
branch: claude/ou-de-jianghu-e007
depends_on: []
scope:
  - docs/videos/ou-de-jianghu-e007
  - docs/videos/series-plans/ou-de-jianghu/production
---

# 《偶的江湖》第 7 集劇本：西嶺來客（22 分鐘長篇動畫）

## Why

站主 2026-10-05 要在第 2–5 集之後接著寫後面的集數；第 6 集〈紗女〉在票 `2026-10-05-ou-de-jianghu-e006-script`。第 7 集〈西嶺來客〉照企劃包 `season-01.json` 第 7 集：西嶺兩位隱士同日下山，滄瀾客為救寂聞來盟（寒潭引血、折壽），岳嵐客化名赤羽帶「能救沈歸鶴」的毒丹而來；無名劍客截下毒丹、追到外港劃開紅衣露出赤淵宮雙淵紋、廢其左臂，卻被燕迴當成襲擊貴客攔下；懸念（danger）是殷無聲端起寂聞的湯藥、藥面浮著一層不該有的紅。新角色：滄瀾客 `canglan-ke`、岳嵐客（赤羽）`yuelan-ke`。做法照 `production/README.md`「寫下一集」。

## Definition of done

- [ ] `production/cast.json` 加了 `canglan-ke`、`yuelan-ke` 與本集需要的 `shot_looks`，`cast-notes.md` 有第 7 集段落，`ep7/meta.json`、`ep7/header.json`、`ep7/check-act.mjs` 齊；第 1–7 集同一角色的物件逐字相同。
- [ ] `production/ep7/beats.md` 照第 5、6 集的十一節寫成，經連戲審、戲劇審、修訂與對抗驗收。
- [ ] `docs/videos/ou-de-jianghu-e007/` 五檔齊；lint 0 錯誤、`drama_craft_check.mjs` 全達標、`shot_reading.mjs` 0 陷阱；估算正文 1,390–1,418 秒。
- [ ] 懸念類型 danger、兩段高張力在對的半場（禪房引血之辯在前半、外港紅衣與雙淵紋在後半）；跨集連戲（對第 1–6 集）經獨立審稿；原作名稱掃描 0 筆。

## Steps

- [x] 1. 角色表：新角色、looks（岳嵐客的紅衣與衣內雙淵紋、廢臂；滄瀾客的毛皮斗篷與引血刀）、聲音、cast-notes 第 7 集段、meta、表頭。
- [x] 2. 分場表：撰寫 → 連戲審與戲劇審 → 修訂 → 對抗驗收。
- [ ] 3. 五幕分鏡：每幕自我檢查，整集審、修、驗收。
- [ ] 4. 合併、`script.md`、跨集審（第 1–7 集）、`brief.md` 與 `review.md`、名字掃描。

## How to verify

```bash
s=ou-de-jianghu-e007
node tools/video/cli.mjs lint --slug $s
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/$s/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/$s/video.json
D=docs/videos/series-plans/ou-de-jianghu
node $D/build.mjs --check && node $D/validate.mjs && node --test $D/validate.test.mjs
npm run check:tasks
```

## Notes

- 第 6 集在 PR #1327（分支 `claude/ou-de-jianghu-e006`），本集從它的 head 開出 `claude/ou-de-jianghu-e007`；#1327 合併後要把本分支接到主線上（同 #1276 → 第 6 集的做法）。分場表與角色表在第 6 集五幕還在寫時就先做（照第 2–5 集「分場表先於分鏡」的做法），第 6 集定稿後跨集審再對一次。
- 承接狀態見 `production/ep6/beats.md` 第十一節「本集結束時交給第 7 集」：藥瓶已空（第 6 集主編定案沈歸鶴吞下最後一粒，包三錢知道有過藥、不知來歷）、殷無聲每日端湯藥（黑陶碗，第 6 集 a04 場 3 已立）、三宗知道沈先生病倒、紗女與無名劍客是「代行」。
- 2026-10-06 角色表與分場表完成：滄瀾客 Zubenelgenubi、岳嵐客「赤羽」Algieba（男聲已全部用完）；岳嵐客三個 look（yuelan-crest 露紋、yuelan-crippled 廢臂、yuelan-covered 右手攏住衣襟蓋紋，第三個是分場表戲劇審後加的）。分場表 1,177 行、25 場，連戲審 2 major 18 minor、戲劇審 2 major 23 minor，三輪修訂；最後兩條由主控裁定（meta.json 改字；「赤羽」暫留，見下）。
- 主編定案：姬無霜本集不入鏡（已從 meta 的 cast 拿掉）；一集兩首詩號（滄瀾客、岳嵐客，依 narrative_constraints 都是主要角色）；真身由劍客認出雙淵紋、赤羽自報名、紗女推出「管藥的是大宮主」；第一劍切斷藥箱背帶、藥箱落海（接上沒有藥箱的 look）；執事上梵林被殷無聲擋在門外、聽見寒潭與折壽回報；最後一句台詞寂聞「無聲。」「……藥。」、尾鏡浮紅的湯藥無台詞；火脊丹是一顆（不是一瓶）。
- 超出細綱、要第 8–11 集接住的知情狀態：赤淵宮知道沈歸鶴分魂了（赤羽看過化身的影子、說了「先生也知道了」）；滄瀾客與赤羽在嶺口打過招呼、認得彼此，但滄瀾客本集不知道赤羽就是岳嵐客；洛青衍給了藥童一枚白貝錢，藥童帶進梵林，本集沒人撿到。
- 等站主裁定：化名「赤羽」與另一部作品角色全名的前兩字相同（不像「斷浪」是全名相同），暫留；要改時同步 setting.json、season-01.json、cast.json、cast-notes.md、ep7/beats.md、meta.json，再重產表頭並重合併。
