---
id: 2026-11-01-zhong-tian-e044-route-a-clips
title: Zhong-tian e044: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-01T21:06:29Z
created_at: 2026-11-01T21:06:28Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e044
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e044
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e044.json
---

# Zhong-tian e044: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 44 集（43 鏡）照第 43 集的做法（票 `2026-11-01-zhong-tian-e043-route-a-clips`）走 RunPod 路線 A。站主 2026-11-01：照推薦的決定做，一路做到第 60 集。

## Definition of done

- [ ] 43 鏡的 1080p 片段，紀錄在 `colab/runs/e044/`
- [ ] 剪接、匯入成片、站主核准；八語、上架包核准

## Steps

- [x] 第 44–60 集的 10 個配角定妝照（同一台 pod，`_series/.../refs-paint-e044/round1.json`），挑好進 `assets/refs-dh/`
- [x] 第一段（`colab/runs/_scripts/st1-ep.sh 44`，巡兵 s09 用 `extras.json` 接定妝照）、審、重抽
- [x] 第二、三段、剪接（106.2 秒、無凍格）、匯入（2026-11-02）

## How to verify

`/admin/videos` 上第 44 集核准。

## Notes

- 第二段第一台 pod 中途 `Connection reset by peer`，s11–s20、s40 沒做；`route_a_st23.sh` 重跑一次（跳過已有的）補齊，那台 US$2.92。
- 只給場景圖的插鏡，s31、s36 的空景長達 4.0／2.5 秒（不是開頭一閃），`headtrim.sh` 只看前 1.5 秒抓不到；整支跑 scene 偵測找切點再 `sNN@秒`。
- s43 兩個 seed 都在左邊前景放了一個人（越肩鏡）；不再抽，`crop=1280:720:640:40` 再放大。
- 成片 2026-11-02 核准。八語：一個代理依序做完 8 語（約 29 分鐘），s20「她爹，」只有 0.63 秒，ja、es、id 縮到一個詞、情緒改「極短促」才放得進。8 語通過，`import --languages` 已送。
- 翻譯代理發現中文說明「吹熄燭火」與分鏡 s02「捏熄」不符：以分鏡為準，改 `video.json` 的 `youtube.description`（八語本來就寫捏熄）。
