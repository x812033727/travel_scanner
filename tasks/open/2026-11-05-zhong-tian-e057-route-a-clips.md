---
id: 2026-11-05-zhong-tian-e057-route-a-clips
title: Zhong-tian e057: route A clips on RunPod, cut, import, dubs and publish package
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-05T09:38:36Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e057.json
---

# Zhong-tian e057: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 57 集（45 鏡）照第 43–56 集的做法走 RunPod 路線 A（`tasks/done/2026-11-01-zhong-tian-e043-route-a-clips.md`），一台長開的 pod 接力（`_scripts/chain.sh st23:56 st1:57`）。

## Definition of done

- [ ] 45 鏡 1080p 片段，紀錄在 `colab/runs/e057/`
- [ ] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [ ] 錄台詞、剪接表
- [ ] 第一段（chain）、審、重抽
- [ ] 第二、三段、剪接、匯入

## How to verify

`/admin/videos` 上第 57 集核准。

## Notes
2026-11-05 收尾交接（還沒開拍）：台詞 55 句已錄、剪接表 `hailuo/edit-dh-e057.json` 已寫；`colab/runs/e057/extras.json` 已先改掉四句短喊（s13、s19、s21、s30，避免畫成字幕）並寫明少年、騎兵、刺客穿宋式衣著。DRY 檢查 0 錯。接手時：`KEEP=1 bash colab/runs/_scripts/chain.sh st1:57`（或接在別集 st23 後面），審片、重抽、照第 55、56 集的流程做下去。
