---
id: 2026-09-28-sothatswhy-pilot-3
title: So That's Why: pilot the first three episodes with Shorts, captions and dubs, and measure
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T06:00:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-sothatswhy-explainer-preset
  - 2026-09-28-sothatswhy-shorts-from-episode
  - 2026-09-28-sothatswhy-mascot-setting
  - 2026-09-26-video-dubs-worker
scope:
  - docs/videos/so-thats-why/README.md
  - docs/videos/so-thats-why/schedule.csv
  - docs/videos/sothatswhy-b08/
  - docs/videos/sothatswhy-s01/
  - docs/videos/sothatswhy-t01/
---

# So That's Why: pilot the first three episodes with Shorts, captions and dubs, and measure

## Why

`docs/videos/so-thats-why/README.md` 的成本、產能與「每天一集」都是估的。每天一集的瓶頸是站主審片與上傳配音；開播前要知道一集真正花多少錢、多少時間，才決定能不能日更、要先囤幾集。

## Definition of done

- [ ] B08、S01、T01 三集做完：長片、各 2 支 Shorts、五語 CC、四語配音、上架包。
- [ ] 每集記錄：插圖張數與重做次數、媒體花費、token、站主審稿與審片分鐘數、配音塞不下的句數。
- [ ] README 的成本與產能改成實測數字；確定開播日與節奏（日更或隔日更），重排 `schedule.csv`。

## Steps

- [ ] 依 `episodes.json` 那一列生成 brief，查 `facts_to_verify`。
- [ ] 走漫劇路線做完三集與 Shorts。
- [ ] 改文件。

## How to verify

`node tools/video/cli.mjs status --slug sothatswhy-b08`（其他兩集同）顯示已到上架包；README 的數字有來源。
