---
id: 2026-10-05-ou-de-jianghu-e006-script
title: 《偶的江湖》第 6 集劇本：紗女（22 分鐘長篇動畫）
status: in-progress
priority: P2
area: docs
owner: claude-fable-local
claimed_at: 2026-10-05T12:29:12Z
created_at: 2026-10-05T12:29:05Z
completed_at:
branch: claude/ou-de-jianghu-e006
depends_on: []
scope:
  - docs/videos/ou-de-jianghu-e006
  - docs/videos/series-plans/ou-de-jianghu/production
---

# 《偶的江湖》第 6 集劇本：紗女（22 分鐘長篇動畫）

## Why

站主 2026-10-05 要在第 2–5 集（PR #1276）之後接著寫後面的集數。第 6 集〈紗女〉照企劃包 `season-01.json` 第 6 集：沈歸鶴倒在書齋、分魂成紗女與無名劍客；扶瀾使者洛青衍抵盟、姬無霜在盟堂看見他頸後的胎記；懸念是她對柳不活說「他是我的兒子。」。本集起兩個新角色（紗女 `sha-nu`、無名劍客 `wuming-jianke`）第一次出場，洛青衍第一次有戲。做法照 `docs/videos/series-plans/ou-de-jianghu/production/README.md`「寫下一集」。

## Definition of done

- [ ] `production/cast.json` 加了 `sha-nu`、`wuming-jianke`（與本集需要的 `shot_looks`），`cast-notes.md` 有第 6 集段落，`ep6/meta.json`、`ep6/header.json`、`ep6/check-act.mjs` 齊；第 1–6 集同一角色的物件逐字相同。
- [ ] `production/ep6/beats.md` 照第 5 集的十一節寫成，經連戲審、戲劇審、修訂與對抗驗收。
- [ ] `docs/videos/ou-de-jianghu-e006/` 五檔齊；lint 0 錯誤、`drama_craft_check.mjs` 全達標、`shot_reading.mjs` 0 陷阱；估算正文 1,390–1,418 秒。
- [ ] 懸念類型 reveal、兩段高張力在對的半場（書齋分魂在前半、盟堂國書與茶盞在後半）；跨集連戲（對第 1–5 集）經獨立審稿；原作名稱掃描 0 筆。

## Steps

- [x] 1. 角色表：新角色、looks、聲音（紗女的聲音「是沈歸鶴的聲音」）、cast-notes 第 6 集段、meta、表頭。
- [x] 2. 分場表：撰寫 → 連戲審與戲劇審 → 修訂 → 對抗驗收。
- [ ] 3. 五幕分鏡：每幕自我檢查，整集審、修、驗收。
- [ ] 4. 合併、`script.md`、跨集審（第 1–6 集）、`brief.md` 與 `review.md`、名字掃描。

## How to verify

```bash
s=ou-de-jianghu-e006
node tools/video/cli.mjs lint --slug $s
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/$s/video.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/$s/video.json
D=docs/videos/series-plans/ou-de-jianghu
node $D/build.mjs --check && node $D/validate.mjs && node --test $D/validate.test.mjs
npm run check:tasks
```

## Notes

- 2026-10-05 角色表與分場表完成（PR #1276 合併後分支已接到主線 50b418b00）：紗女與無名劍客都用沈歸鶴的 Iapetus（lint 不擋同聲；將來走製作設計書流程要換）；沈歸鶴加 `shen-bedridden`；分場表 1,182 行、25 場、經連戲審（2 major 10 minor）、戲劇審（2 major 10 minor）與三輪修訂驗收。主編定案：冷開場給一眼分魂後的紗女（時間只往前走的例外）、藥瓶由包三錢撿到、沈歸鶴吞最後一粒、瓶空交給第 7 集；洛青衍本集給詩號；三宗知道沈先生病倒；殷無聲每日端湯藥為第 7 集懸念鋪路；本集不用 `wushuang-armed`。縮圖鏡：a01 場 6 分魂全景，寫完後填。

- 分支從 #1276 的 head 開出；#1276 squash 進 main 後要 `git rebase --onto origin/main <#1276 head>` 再開 PR（內容相同，應該乾淨）。
- 承接狀態見 `production/ep5/beats.md` 第十一節「本集結束時交給第 6 集」；分魂規則在 `setting.json` rules `soul-split`。
