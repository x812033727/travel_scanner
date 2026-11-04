---
id: 2026-11-03-zhong-tian-e050-route-a-clips
title: Zhong-tian e050: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-03T10:27:11Z
created_at: 2026-11-03T10:27:10Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e050
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e050
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e050.json
---

# Zhong-tian e050: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 50 集（52 鏡）照第 43–49 集的做法走 RunPod 路線 A（`tasks/done/2026-11-01-zhong-tian-e043-route-a-clips.md`），一台長開的 pod 接力（`_scripts/chain.sh`）。

## Definition of done

- [ ] 52 鏡 1080p 片段，紀錄在 `colab/runs/e050/`
- [ ] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [x] 錄台詞、剪接表
- [x] 第一段（chain；掌櫃 `zhanggui` 用第 42 集的 `innkeeper-portrait-t1`、衙役 `yayi`，都由 `extras.json` 接；s23 掌櫃腋下的「酒罈」照站主 10-31 的提醒改成陶甕、不畫酒瓶）、審、重抽
- [x] 第二、三段、剪接（125.4 秒、無凍格）、匯入（2026-11-04）

## How to verify

`/admin/videos` 上第 50 集核准。

## Notes

- 酒瓶：提示詞把酒杯、酒罈全改成陶器（`extras.json` 的 `_replace`），但 `set-zhou-kezhan-t1` 場景圖帶著酒瓶，s22、s23、s26 右緣還是有一支顯眼的棕色長頸玻璃瓶，剪接時裁掉；s21、s43、s52 背景的小瓶子不是焦點，照站主的標準留著。
