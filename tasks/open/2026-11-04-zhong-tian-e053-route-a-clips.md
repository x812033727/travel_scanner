---
id: 2026-11-04-zhong-tian-e053-route-a-clips
title: Zhong-tian e053: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-04T08:11:56Z
created_at: 2026-11-04T08:11:55Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e053
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e053
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e053.json
---

# Zhong-tian e053: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 53 集（44 鏡）照第 43–52 集的做法走 RunPod 路線 A（`tasks/done/2026-11-01-zhong-tian-e043-route-a-clips.md`），一台長開的 pod 接力（`_scripts/chain.sh st23:52 st1:53`）。

## Definition of done

- [ ] 44 鏡 1080p 片段，紀錄在 `colab/runs/e053/`
- [ ] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [x] 錄台詞、剪接表
- [x] 第一段（chain）、審、重抽
- [x] 第二、三段、剪接（105.33 秒、無凍格）、匯入（2026-11-04）

## How to verify

`/admin/videos` 上第 53 集核准。

## Notes

- 2026-11-04 15:36 the long-running pod `yaxz30ls5h3rop` (started 11-03 15:37, eps 49 stage 3 to 53 stage 3) hit the 24 h `runpod_max_pod_hours` cap and the site stopped it, after 9 of 44 stage-3 clips. EU-CZ-1 then had no stock for 90 min (28 tries of `st23-retry.sh`); a new pod `9uvu3v19ipu0vu` started at 17:06 and stage 3 continues from s10. Nothing lost; the retry loop handled it unattended.

2026-11-05 收尾交接：成片、八語語言批次已核准；上架包（44 段片段＋剪接紀錄、配樂、剪接表，PR #2021 的新匯入）已送，等站主在 /admin/videos 核准。核准後：`npm run tasks -- done` 這張票、README §4 這一列改成「都已核准」。
工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e053-dh/` 還在，沒有備份到 git；審片 session 要求的整包／精簡版備份等站主決定（清單見對話：final/、clips/、st1/、st2/、retake*/、audio*、music/、cut 的紀錄與配音軌）。在站主說審片確認之前不要刪這一集的任何檔。
