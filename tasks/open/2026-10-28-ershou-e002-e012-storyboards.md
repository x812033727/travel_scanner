---
id: 2026-10-28-ershou-e002-e012-storyboards
title: 重生系統 第 2–12 集分鏡 video.json
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-28T04:50:29Z
completed_at:
branch:
depends_on:
  - 2026-10-28-ershou-e001-colab-pilot-to-cut
scope:
  - docs/videos/ershou-chongsheng-e002
  - docs/videos/ershou-chongsheng-e003
  - docs/videos/ershou-chongsheng-e004
  - docs/videos/ershou-chongsheng-e005
  - docs/videos/ershou-chongsheng-e006
  - docs/videos/ershou-chongsheng-e007
  - docs/videos/ershou-chongsheng-e008
  - docs/videos/ershou-chongsheng-e009
  - docs/videos/ershou-chongsheng-e010
  - docs/videos/ershou-chongsheng-e011
  - docs/videos/ershou-chongsheng-e012
---

# 重生系統 第 2–12 集分鏡 video.json

## Why

第一篇十二集的細綱在 `docs/videos/series-plans/ershou-chongsheng/chapter-01.md`，第 1 集已寫成 `docs/videos/ershou-chongsheng-e001/`（42 鏡、四個離線檢查全過）。第 2 到 12 集照同一套寫，等第 1 集小樣看過再開始，免得畫風或路線改了要重寫。

## Definition of done

- [ ] 每集：brief.md、video.json、overlays.json、storyboard.md；`node tools/video/cli.mjs script --slug` 產 script.md
- [ ] 每集的 hook 接上一集的 cliffhanger（同一個畫面接下去）；結尾照細綱的類型收在最高點
- [ ] 每集 lint 0 錯誤、`drama_craft_check.mjs` 30 列全過、`shot_reading.mjs --route hailuo` 0 陷阱、`shot_plan.mjs --strict` 沒有「會白花」；說話鏡頭動嘴、靜圖 ≤ 10%
- [ ] 角色外觀從 `production/cast.json` 逐字照抄；新角色（小米第 3 集、蘇寧第 6 集、梁啟第 7 集、錢經理、阿輝、大強第 7–8 集、周父周母第 10 集）都已在 cast.json；再有新的先補進去再用
- [ ] 每集產鎖定檔與 colab manifest，照第 1 集的 `production/colab/README.md`

## How to verify

四個離線檢查的指令在 `production/e001-lock-package.md` 第 2 節；第 1 集的 `video.json` 是格式範本。

## Notes

第 1 集的 `video.json` 是用一支生成腳本寫的（場景前綴、說話子句、鉤子表、中文分鏡表都從同一份資料出）；寫下一集照同樣做法。craft 與 shot_reading 的坑寫在票 `2026-10-28-ershou-chongsheng-season-one-plan-e001` 的 Notes。面板文字（備忘、校驗失敗、黑屏、筆記）全在 overlays.json，prompt 裡只寫臉上的青綠色光。
