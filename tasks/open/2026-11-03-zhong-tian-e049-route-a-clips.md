---
id: 2026-11-03-zhong-tian-e049-route-a-clips
title: Zhong-tian e049: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-03T04:14:13Z
created_at: 2026-11-03T04:14:11Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e049
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e049
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e049.json
---

# Zhong-tian e049: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 49 集（46 鏡）照第 43–48 集的做法走 RunPod 路線 A（`tasks/done/2026-11-01-zhong-tian-e043-route-a-clips.md`），一台長開的 pod 接力（`_scripts/chain.sh`）。

## Definition of done

- [ ] 46 鏡 1080p 片段，紀錄在 `colab/runs/e049/`
- [ ] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [ ] 錄台詞、剪接表
- [ ] 第一段（chain；報榜人 `baobang` 由 `extras.json` 接定妝照）、審、重抽
- [ ] 第二、三段、剪接、匯入

## How to verify

`/admin/videos` 上第 49 集核准。

## Notes

- 2026-11-03 第三段：長開了 21.5 小時的 pod（e046 第二段起到 e049，US$52.43）GPU 掛了：12:29 s01 的 SeedVR2 等了 3600 秒沒結果，之後每支都立刻 `OSError [Errno 6] No such device or address`。速度看門狗只看「done in」的秒數，抓不到失敗，白等了約 75 分鐘。已改成連續三支失敗就判定 pod 死了、停掉換一台。13:50 停 pod，重開時 EU-RO-1 沒貨，迴圈重試。第二段 46 支都在，不用重做。
