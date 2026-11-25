---
id: 2026-11-03-zhong-tian-e049-route-a-clips
title: Zhong-tian e049: route A clips on RunPod, cut, import, dubs and publish package
status: done
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-03T04:14:13Z
created_at: 2026-11-03T04:14:11Z
completed_at: 2026-11-04T13:58:02Z
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

- [x] 46 鏡 1080p 片段，紀錄在 `colab/runs/e049/`
- [x] 剪接、匯入、站主核准；八語、上架包核准

## Steps

- [x] 錄台詞、剪接表
- [x] 第一段（chain；報榜人 `baobang` 由 `extras.json` 接定妝照）、審、重抽
- [x] 第二、三段、剪接（131.8 秒、無凍格）、匯入（2026-11-03）

## How to verify

`/admin/videos` 上第 49 集核准。

## Notes

- 2026-11-03 第三段：長開了 21.5 小時的 pod（e046 第二段起到 e049，US$52.43）GPU 掛了：12:29 s01 的 SeedVR2 等了 3600 秒沒結果，之後每支都立刻 `OSError [Errno 6] No such device or address`。速度看門狗只看「done in」的秒數，抓不到失敗，白等了約 75 分鐘。已改成連續三支失敗就判定 pod 死了、停掉換一台。13:50 停 pod，重開時 EU-RO-1 沒貨，迴圈重試。第二段 46 支都在，不用重做。
- 14:32 換的新 pod 也一樣：第三段每支 SeedVR2 都 `[Errno 6] No such device or address`。看門狗連三支失敗後停機。15:00 在另一台新 pod 上跑第 50 集第一段（只用 H3 的模型）正常（s01–s03 每支約 170 秒），所以壞的是 network volume 上的 SeedVR2 7B 檔（或 SeedVR2 寫在 volume 上的東西），不是 GPU。`fetch_models.py` 開機時只要 `.verified/<sha>` 標記在、大小對就不重驗內容，所以每台新 pod 都會讀到同一個壞檔。從這邊刪不了 volume 上的檔：要站主在後台刪 volume（站台再開一個新的、重下約 112 GiB）。在那之前第一、二段照做，第三段先累積。
- 站主 2026-11-03 在後台刪了舊 volume（EU-RO-1）。重開時全區沒貨，15:37 在 EU-CZ-1 開到一台，站台自動在那裡開了新 volume、重下模型；16:15 第一支第三段正常（s41 233.8 秒，含載入）。原因確定是舊 volume 上的 SeedVR2 檔。
- 2026-11-04 站主核准上架包（含 46 段片段）；結案。
