---
id: 2026-10-27-xiuxian-e002-e012-storyboards
title: 修仙獎勵 第 2–12 集分鏡 video.json
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-27T23:39:00Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/xiuxian-jiangli-e002
  - docs/videos/xiuxian-jiangli-e003
  - docs/videos/xiuxian-jiangli-e004
  - docs/videos/xiuxian-jiangli-e005
  - docs/videos/xiuxian-jiangli-e006
  - docs/videos/xiuxian-jiangli-e007
  - docs/videos/xiuxian-jiangli-e008
  - docs/videos/xiuxian-jiangli-e009
  - docs/videos/xiuxian-jiangli-e010
  - docs/videos/xiuxian-jiangli-e011
  - docs/videos/xiuxian-jiangli-e012
---

# 修仙獎勵 第 2–12 集分鏡 video.json

## Why

第一篇十二集的細綱在 `docs/videos/series-plans/xiuxian-jiangli/chapter-01.md`，第 1 集已寫成 `docs/videos/xiuxian-jiangli-e001/`（45 鏡、四個離線檢查全過）。第 2 到 12 集照同一套寫，等第 1 集小樣看過再開始，免得畫風或路線改了要重寫。

## Definition of done

- [ ] 每集：brief.md、video.json、overlays.json、storyboard.md；`node tools/video/cli.mjs script --slug` 產 script.md
- [ ] 每集的 hook 接上一集的 cliffhanger（同一個畫面接下去）；結尾照細綱的類型收在最高點
- [ ] 每集 lint 0 錯誤、`drama_craft_check.mjs` 30 列全過、`shot_reading.mjs --route hailuo` 0 陷阱、`shot_plan.mjs --strict` 沒有「會白花」；說話鏡頭動嘴、靜圖 ≤ 10%
- [ ] 角色外觀從 `production/cast.json` 逐字照抄；新角色（何大勇、小石頭、陸昭、白鷺、宋綰綰、阿璃）先補進 cast.json 再用
- [ ] 每集產 `e00N-jobs.json` 與鎖定檔，照第 1 集的 `colab/README.md`

## How to verify

四個離線檢查的指令在 `production/e001-lock-package.md` 第 2 節；第 1 集的 `video.json` 是格式範本（位置前綴、說話子句、插鏡不列角色、避開 `shot of X on screen` 這種會被讀成插鏡的寫法）。

## Notes for the next person

第 1 集的 `video.json` 是用一支生成腳本寫的（prompt 前綴、說話子句、鉤子表、中文分鏡表都從同一份資料出），寫下一集時照同樣做法省得手改 45 鏡。注意 craft 的 `OF_OBJECT` 把 `shot of <三字內> screen` 讀成插鏡；`hands.small-prop` 看 motion 裡「拿小東西的動詞＋小道具」同一子句；吃喝、兩人接觸、微小反應都是 C／B 級，寫法在 `shot-risk.md`。
