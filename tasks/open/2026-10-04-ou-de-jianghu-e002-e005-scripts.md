---
id: 2026-10-04-ou-de-jianghu-e002-e005-scripts
title: 《偶的江湖》第 2–5 集劇本：鯨背嶼、三十六魂、裂山秘錄、封功（22 分鐘長篇動畫）
status: in-progress
priority: P2
area: docs
owner: claude
claimed_at: 2026-10-04T23:34:11Z
created_at: 2026-10-04T23:34:07Z
completed_at:
branch: claude/vibrant-cray-mdpjzx
depends_on: []
scope:
  - docs/videos/ou-de-jianghu-e002
  - docs/videos/ou-de-jianghu-e003
  - docs/videos/ou-de-jianghu-e004
  - docs/videos/ou-de-jianghu-e005
  - docs/videos/series-plans/ou-de-jianghu
---

# 《偶的江湖》第 2–5 集劇本：鯨背嶼、三十六魂、裂山秘錄、封功（22 分鐘長篇動畫）

## Why

站主要接著第 1 集〈幽皇之女〉（`docs/videos/ou-de-jianghu-e001/`），把第一季第 2–5 集的 22 分鐘劇本寫出來，照企劃包 `docs/videos/series-plans/ou-de-jianghu/season-01.json` 的細綱。四集要和第 1 集已寫出的台詞、道具、角色外觀連得上，同一角色在每一集的角色檔逐字相同（設定圖共用）。

## Definition of done

- [ ] `docs/videos/ou-de-jianghu-e00{2,3,4,5}/` 各有 `video.json`、`series.json`、`script.md`、`brief.md`、`review.md`；long-anime-v1，正文估算約 1,404 秒。
- [ ] 每集 lint 0 錯誤、`drama_craft_check.mjs` 全達標、`shot_reading.mjs` 0 陷阱；`script.md` 與 `video.json` 一致。
- [ ] 四集的懸念類型照細綱（reveal、choice、reversal、emotion），兩段高張力在對的半場；跨集連戲（時間線、人物位置、物證流向、誰知道什麼）經獨立審稿。
- [ ] 同一角色在第 1–5 集的角色物件逐字相同；新角色與詩號列在各集 `brief.md` 等站主核定；原作名稱掃描 0 筆。

## Steps

- [x] 1. 企劃包殘留舊名：`setting.json` 竹虛外觀的「red maple iron」、派系 id `youdu-qisha`；重建並驗證企劃包。
- [x] 2. 全系列角色表（新角色、`shot_looks`、暫定聲音），第 1 集同步（姬無霜基本外觀拿掉手背印記）。
- [x] 3. 四集分場表：撰寫、連戲審與戲劇審、修訂、跨集審。
- [ ] 4. 二十幕分鏡：每幕自我檢查，每集整集審與修。
- [ ] 5. 合併、`script.md`、最後對抗審稿、`brief.md` 與 `review.md`。

## How to verify

```bash
for n in 2 3 4 5; do
  s=ou-de-jianghu-e00$n
  node tools/video/cli.mjs lint --slug $s
  node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/$s/video.json
  node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/$s/video.json
done
D=docs/videos/series-plans/ou-de-jianghu
node $D/build.mjs --check && node $D/validate.mjs && node --test $D/validate.test.mjs
npm run check:tasks
```

## Notes

- 做法沿用第 1 集：分場表 → 每集五幕各一個代理 → 合併檢查 → 讀全集台詞修連戲。第 1 集的檢查腳本與分場表在 session scratchpad，不進 repo。
- 第 1 集的角色檔變動（姬無霜基本外觀、`shot_looks`）屬試播票 `2026-10-04-clip-route-pilot-comparison` 的 scope，記在那張票。
- 2026-10-05 角色表：14 人（第 1 集九人，加竹虛 zhuxu、柳不活 liu-buhuo、書院長老 shuyuan-elder、玄門執事長老 xuanmen-steward、客院盟兵 alliance-guard），新角色聲音暫定 Umbriel、Enceladus、Orus、Charon、Sadachbia；`shot_looks` 管狀態變化（寂聞中箭／封功、姬無霜背弓、柳不活受傷／投敵、竹虛回程、包三錢落海、殷無聲斷髮、聶孤鐵釘傷）。姬無霜基本外觀拿掉手背印記，第 2 集起兩道印只寫在插鏡 prompt。
- 2026-10-05 分場表四份各經連戲審、戲劇審、修訂與跨集審。主編定案：旁白一律用相對時間，不報「第幾日」；第 1 集名句（「你知道的，我都要知道」「瞞得過一天，是一天」「幽都殺人，用不著走門」）不在後面的集數逐字重用，前者只留給第 5 集寂聞「你做到了嗎？」；島底陣上的符一律說「盟符」，不說「三宗的符」（避免跟她手背的三宗印混淆）；物證（斷弦、鐵釘、拓片、備用封條）收在沈歸鶴書齋案的抽屜；押差官改押解官、萬教通緝改九洲通緝（企劃包已同步）。
- 2026-10-05 站主決定：燕迴的外號由「斷浪」改成「赤纓」（取自他刀上的紅刀穗；「斷浪」與漫畫《風雲》的主要角色同名）。企劃包、路線圖人名表（含後面時代的招式「斷浪八式」→「赤纓八式」）、全系列角色表與第 1 集都已改。
- 2026-10-05 額度將盡，先備份：第 2、3 集五幕都寫完、各幕過檢查，合併成草稿 `video.json`、`series.json`、`script.md` 與最短的 `brief.md`（lint 0 錯誤）；還沒做整集修、最後審稿與 `review.md`。第 4 集只寫了 a01–a03，第 5 集還沒開寫。工作檔（角色表、分場表、各幕、檢查與合併腳本、第 2 集的整集審意見）在 `docs/videos/series-plans/ou-de-jianghu/production/`，README 寫了怎麼接著做。

