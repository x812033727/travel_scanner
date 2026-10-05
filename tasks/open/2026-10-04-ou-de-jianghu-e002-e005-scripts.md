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

- [ ] 1. 企劃包殘留舊名：`setting.json` 竹虛外觀的「red maple iron」、派系 id `youdu-qisha`；重建並驗證企劃包。
- [ ] 2. 全系列角色表（新角色、`shot_looks`、暫定聲音），第 1 集同步（姬無霜基本外觀拿掉手背印記）。
- [ ] 3. 四集分場表：撰寫、連戲審與戲劇審、修訂、跨集審。
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
