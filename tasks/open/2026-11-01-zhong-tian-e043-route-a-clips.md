---
id: 2026-11-01-zhong-tian-e043-route-a-clips
title: Zhong-tian e043: route A clips on RunPod, cut, import, dubs and publish package
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-01T13:40:01Z
created_at: 2026-11-01T13:39:58Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e043
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e043
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e043.json
---

# Zhong-tian e043: route A clips on RunPod, cut, import, dubs and publish package

## Why

第 43 集〈貢院〉的稿與分鏡已寫好（37 鏡），六張新參照圖已在 main。第 42 集以前由別的 session 做，第 43 集起由這張票接：
路線 A（Ref2VA 960×544 hero → refine σ0.5 1312×736 → SeedVR2 1920×1080）在 RunPod 上做片段，剪接、匯入、八語、上架包。
這也是第一次從雲端 session 走 RunPod 路線。

## Definition of done

- [ ] 37 鏡的 1080p 片段，審過、紀錄在 `colab/runs/e043/`（manifest、提示詞、takes.tsv）
- [ ] `hailuo/edit-dh-e043.json` 提交；成片匯入、站主核准
- [ ] 八語配音與說明、語言批次核准、上架包（含片段）核准
- [ ] `production/README.md` 第 4 節的表更新

## Steps

- [x] gen-dh 重跑（輸出與 repo 相同）、ref2manifest 37 鏡沒有缺圖
- [x] 雲端 session 連得到 mokaair.com 與 *.proxy.runpod.net（2026-11-01）
- [ ] 配對影片工具權杖（login --runpod）
- [ ] 補兩張配角定妝照：巡考（s27）、魏家家僕（s21，第 47 集還會出現）；書吏 s15、s17 手動接上 `registrar-portrait-t1.png`
- [ ] 估價給站主、點頭後跑第一段，審草稿、重抽（每鏡兩個 seed）
- [ ] 第二、三段
- [ ] 剪接、匯入、八語、上架包

## How to verify

`/admin/videos` 上第 43 集的成片、語言批次與上架包都是核准；`AI/備份/drama/zhong-tian-qu-qi-e043/clips/` 有 37 段。

## Notes

- `ref2manifest.mjs` 沒有把書吏（video.json 的 speaker `shuli`）對到 `registrar-portrait-t1.png`：gen-dh 的 `DH` 沒有 `shuli`，
  所以 ff-dh 的 refs 只有場景圖。第 42 集是手動接上的（沒有留下腳本）。這集在 `colab/runs/e043/` 的補丁腳本裡接上；不改 gen-dh，免得第 42 集的雜湊跟著變。
- `assets/refs-dh` 的範圍在票 `2026-10-31-zhong-tian-paint-e042-e060-refs`（另一個 session）手上；`production/README.md` 在 `2026-10-31-zhong-tian-clip-backup` 手上（stale）。
  新定妝照與表格更新會在 PR 裡說明。
