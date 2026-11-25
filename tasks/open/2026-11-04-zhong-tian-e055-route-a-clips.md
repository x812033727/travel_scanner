---
id: 2026-11-04-zhong-tian-e055-route-a-clips
title: Zhong-tian e055: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-04T20:46:59Z
created_at: 2026-11-04T20:46:51Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e055.json
---

# Zhong-tian e055: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 55 集（43 鏡）照第 43–54 集的做法走 RunPod 路線 A（`tasks/done/2026-11-01-zhong-tian-e043-route-a-clips.md`），一台長開的 pod 接力（`_scripts/chain.sh st23:54 st1:55`）。

## Definition of done

- [ ] 43 鏡 1080p 片段，紀錄在 `colab/runs/e055/`
- [ ] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [x] 錄台詞、剪接表
- [x] 第一段（chain）、審、重抽
- [x] 第二、三段、剪接（102.1 秒、無凍格）、匯入（2026-11-05）

## How to verify

`/admin/videos` 上第 55 集核准。

## Notes

2026-11-05 收尾交接：43 鏡 1080p、剪接（102.1 秒）、已匯入，等站主審成片。
剪接時的處理：`s30@1.2 s35@2.0`；s40 從 0.6 秒起 `crop=1200:675:200:300`、s43 `crop=1400:788:520:0`（裁掉信上的假字），未裁的原片在 `clips-uncropped/`；重跑 stage-clips.sh 會蓋掉裁切，要再裁一次（指令見 `colab/runs/e055/stage-clips-args.txt`）。
成片核准後：八語（照第 53、54 集，一集一個代理、各自的 scratchpad 資料夾）→ `import --languages` → 核准 → `import --publish --clips <workdir>/clips --edit hailuo/edit-dh-e055.json`（輸出不能有 build data not found）。
工作資料夾沒有備份到 git，不要刪。
