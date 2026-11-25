---
id: 2026-11-02-zhong-tian-e045-route-a-clips
title: Zhong-tian e045: route A clips on RunPod, cut, import, dubs and publish package
status: done
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-02T03:51:30Z
created_at: 2026-11-02T03:51:29Z
completed_at: 2026-11-04T02:00:56Z
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e045
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e045
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e045.json
---

# Zhong-tian e045: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 45 集（37 鏡）照第 43、44 集的做法走 RunPod 路線 A（票 `2026-11-01-zhong-tian-e043-route-a-clips`）。站主 2026-11-01／02：照推薦的決定做、做到第 60 集；額度已調高。

## Definition of done

- [x] 37 鏡 1080p 片段，紀錄在 `colab/runs/e045/`
- [x] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [x] 第一段（`_scripts/st1-ep.sh 45`；書吏妻 `shuliqi` 由 `extras.json` 接定妝照）、審、重抽
- [x] 第二、三段、剪接（89.0 秒、無凍格）、匯入（2026-11-02）

## How to verify

`/admin/videos` 上第 45 集核准。

## Notes

- 第一段 US$3.42；重抽兩輪＋第二段在同一台（09:17 被 4 小時上限回收，第三段只做 4 支）。
- 09:18 起 EU-RO-1 沒貨（409），`_scripts/st23-retry.sh` 每 3 分鐘重試，09:32 開到一台，但第三段每支 830–900 秒（正常約 200 秒），慢 4 倍；做了 7 支後 11:20 換機。之後 EU-RO-1 又沒貨，迴圈繼續等。
- s33、s36（唐小棠在客房）高領下露抹胸，四個 seed 都壓不住，剪接時只取上半部再放大。
- 剪接時的修正見 `colab/runs/e045/review-st1.md` 最後一節（s08 漏看了背景的全身分身，裁切救回）。匯入回報 120 fps：是成片的 r_frame_rate，平均 23.96 fps，與前兩集相同。
- 2026-11-04 站主核准上架包（含片段）；結案。
