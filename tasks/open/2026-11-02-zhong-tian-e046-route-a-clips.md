---
id: 2026-11-02-zhong-tian-e046-route-a-clips
title: Zhong-tian e046: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-02T07:49:03Z
created_at: 2026-11-02T07:49:02Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e046
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e046
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e046.json
---

# Zhong-tian e046: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 46 集（40 鏡）照第 43–45 集的做法走 RunPod 路線 A（票 `2026-11-01-zhong-tian-e043-route-a-clips`）。

## Definition of done

- [ ] 40 鏡 1080p 片段，紀錄在 `colab/runs/e046/`
- [ ] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [x] 錄台詞（49 句）、剪接表
- [ ] 第一段（`_scripts/st1-ep.sh 46`；衙役 `yayi` 由 `extras.json` 接定妝照）、審、重抽
- [ ] 第二、三段、剪接、匯入

## How to verify

`/admin/videos` 上第 46 集核准。

## Notes

- 2026-11-02 站主把後台 `runpod_max_pod_hours` 改成 24、`runpod_idle_stop_minutes` 改成 60。從第 46 集重抽起改成**一台 pod 長開接力**：每一步都 `KEEP=1`（`retake-run.sh`、`route_a_st23.sh`、`st1-ep.sh`、`st23-retry.sh`、`st1-retry.sh` 都認），一集的第二、三段跑完接著跑下一集第一段；審草稿時 GPU 跑上一集的後段或下一集的前段。只有慢機（`speed-guard.sh`，它會自己 `h3r.sh stop`）或整條線做完才停。
- 第 46 集重抽第一次開到的又是慢機（每支 1226–1264 秒），看門狗換掉了；但 `retake-run.sh` 當時只要開到過 pod 就當成做完（8 支只做 2 支），已改成做齊才算完。
