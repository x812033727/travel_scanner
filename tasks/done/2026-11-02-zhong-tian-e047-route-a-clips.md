---
id: 2026-11-02-zhong-tian-e047-route-a-clips
title: Zhong-tian e047: route A clips on RunPod, cut, import, dubs and publish package
status: done
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-02T17:54:58Z
created_at: 2026-11-02T17:54:57Z
completed_at: 2026-11-04T02:01:03Z
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e047
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e047
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e047.json
---

# Zhong-tian e047: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 47 集（38 鏡）照第 43–46 集的做法走 RunPod 路線 A（票 `2026-11-01-zhong-tian-e043-route-a-clips` 在 done/）。第一段由 `_scripts/chain.sh st23:46 st1:47` 接在第 46 集後面，同一台長開的 pod。

## Definition of done

- [x] 38 鏡 1080p 片段，紀錄在 `colab/runs/e047/`
- [x] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [x] 錄台詞、剪接表
- [x] 第一段（chain）、審、重抽
- [x] 第二、三段、剪接（105.1 秒、無凍格）、匯入（2026-11-03）

## How to verify

`/admin/videos` 上第 47 集核准。

## Notes

- 2026-11-03 00:39 the cloud session's container restarted: every `setsid nohup` driver died (stage 2 had 36 of 38 done), but the work folder under `~/mokaair-work` survived and the pod kept running and billing. Rerunning `chain.sh st23:47 st1:48` picked up the same pod (h3r's local state survived too) and skipped what already existed. After a restart: `h3r.sh usage` shows the pod, `ps` shows no drivers, so rerun the last chain.
- 2026-11-04 站主核准上架包（含片段）；結案。
