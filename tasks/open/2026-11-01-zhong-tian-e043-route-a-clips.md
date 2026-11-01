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
- [x] 配對影片工具權杖（login --runpod，2026-11-01 站主允許）
- [x] 補兩張配角定妝照：巡考（s27）、魏家家僕（s21，第 47 集還會出現）；書吏 s15、s17 手動接上 `registrar-portrait-t1.png`
- [x] 估價給站主（約 US$18–20，上限 US$22，2026-11-01 同意）、跑第一段（37 支，US$5.0）、審草稿
- [ ] 重抽 15 鏡 × 2 seed（`colab/runs/e043/retake1/`）
- [ ] 第二、三段
- [ ] 剪接、匯入、八語、上架包

## How to verify

`/admin/videos` 上第 43 集的成片、語言批次與上架包都是核准；`AI/備份/drama/zhong-tian-qu-qi-e043/clips/` 有 37 段。

## Notes

- `ref2manifest.mjs` 沒有把書吏（video.json 的 speaker `shuli`）對到 `registrar-portrait-t1.png`：gen-dh 的 `DH` 沒有 `shuli`，
  所以 ff-dh 的 refs 只有場景圖。第 42 集是手動接上的（沒有留下腳本）。這集在 `colab/runs/e043/` 的補丁腳本裡接上；不改 gen-dh，免得第 42 集的雜湊跟著變。
- `assets/refs-dh` 的範圍在票 `2026-10-31-zhong-tian-paint-e042-e060-refs`（另一個 session）手上；`production/README.md` 在 `2026-10-31-zhong-tian-clip-backup` 手上（stale）。
  新定妝照與表格更新會在 PR 裡說明。
- 定妝照（2026-11-01，RunPod 一台 pod US$0.64，含開機與三輪 10 張）：用書吏定妝照當 image 1，巡考、家僕都抄了書吏的臉；
  改用場景圖 `set-haoshe-t1.png` 當 image 1 才各自不同。巡考第一次畫成立領盤扣，改寫圓領袍。manifest 在 `colab/runs/e043/refs/`。
- 從雲端 session 走 RunPod：配對、開 pod、上傳、下載、stop 都通了（第一次開機約 3 分鐘才 ready，之前一直回 404，這是正常的）。
- 第一段用 `colab/runs/e043/st1.sh`（ref2manifest → `patch_st1.py` → check → batch 兩輪 → stop）。
- 第一段：兩台 pod 都比 route-a.md 的暖機數字慢 1.4–1.6 倍（2 張參照圖 175 秒、8 張 258 秒；第 40 集本機是 124／160 秒）。
  換了一台還是一樣，比較像是雲端 session 經代理上傳下載的時間（`done in` 含上傳下載），不是 GPU 慢，所以沒有再換。37 支 US$5.0（估 US$3.4）。
- 換機時用 `pgrep -f "runs/e043/st1.sh"` 找 pid，比對到自己那條 shell，把自己殺了（exit 144，lessons §7）；外層腳本的 trap 有停機。以後先 `echo $! > x.pid` 再 kill 那個 pid。
- 重抽開機時 EU-RO-1 那張卡沒貨（HTTP 409），用每 3 分鐘重試的迴圈等。
- 草稿的通病：場景圖裡有字的紙（書齋書案上那張）、考卷、摺紙都被畫成一大片亂碼字；開頭空景（只給場景圖的插鏡）；唐小棠有台詞就笑。
- 站主 2026-11-01：「如果有問題用你推薦的決定就好，除非真的要我決定再停下來；43 集做完就一直往下做到這季結束（第 60 集）。」
  每集仍照估價做（第 43 集實付約 US$18），但不再每段停下來等點頭；RunPod 月額度（2026-11 剩約 US$172）不夠全部時才停下來問。
  成片、語言批次、上架包這三個核准還是站主的，等核准的時候就先做下一集。
