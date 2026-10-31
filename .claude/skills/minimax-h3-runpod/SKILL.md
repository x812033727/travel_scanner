---
name: minimax-h3-runpod
description: 用 RunPod 的 GPU pod 跑 MiniMax H3（ComfyUI，≤1920×1088，加 Qwen 首格、σ refine、SeedVR2 放大），從 Claude Code 雲端 session、Codex 或任何 shell 驅動：配對影片工具權杖一次（login --runpod），金鑰留在站台，由站台代開代停 pod，模型在 network volume，用完自動停。要在 RunPod 上生 H3 片段、畫首格、放大到 1080p、配對 RunPod 權限、查本月花費或處理 pod 開不起來時，先讀這個 skill。Drive MiniMax H3 on a RunPod pod through the site's broker from a browserless session, with a paired video tool token.
metadata:
  short-description: RunPod 上的 MiniMax H3：權杖配對、站台代開 pod、批次、放大
---

# MiniMax H3 on RunPod（minimax-h3-runpod）

路線與 `minimax-h3-colab` 同一套：manifest、檢查器、取樣 profile、三段式和寫法都共用，差別是 GPU 由站台代開。RunPod 金鑰只在站台；工具只拿得到影片工具權杖和一次性的 gate 權杖。

| 要做什麼 | 讀哪裡 |
| --- | --- |
| 映像、閘道、模型鎖定檔、站主第一次要設定什麼 | `ops/runpod/README.md` |
| 正文寫法、秒數、畫布、片段僵硬怎麼辦 | `.agents/skills/minimax-h3-colab/references/motion-quality.md` |
| 三段式的 σ、實測與坑 | `.agents/skills/minimax-h3-colab/references/three-stage.md` |
| 片段進產線 | `.agents/skills/minimax-h3-colab/references/pipeline-handoff.md` |

## 不變的規矩

1. **先配對。** 新的雲端 session 要有 `MOKAAIR_VIDEO_TOKEN`（環境 secret），或跑一次 `node tools/video/cli.mjs login --runpod --name "Claude 雲端 session"`，站主在後台按允許。權杖不進 chat、repo、log。
2. **花錢前站主要點頭。** 每批先 `h3r.sh usage`。第一個 pod 要下載約 110 GiB 模型，比平常多等 15–30 分鐘（估計，未實測）。
3. **一次一個 pod、一批共用一個。** 站台擋第二個；同一批放同一個 manifest，不要一鏡開一次。
4. **空間由站台管。** 帳號裡有 ≥120 GB 的 volume 就用它，沒有才在有貨的資料中心開 150 GB（每月約 US$10.5）。pod 只開得在 volume 那一區；那區沒貨就回報 `runpod_no_stock`，換區要站主在後台刪舊的（新區要重下模型）。
5. **預設會停。** 跑完 runner 會終止 pod；`--keep` 才留著，留著就要記得 `stop`。回收器也會停閒置、超時或超過月上限的 pod。
6. **逾時不要盲目重試。** 已有輸出檔的 job 會跳過，重跑只付剩下的；失敗原因看 `--progress` 的檔案。
7. **不要開 Sage Attention**（INT8 瑕疵，motion-quality.md 第五節）。
8. **權重是 INT8 ConvRot、PyTorch CUDA 13**，與 Colab 筆記本的選擇相同。FP8＋CUDA 12.8 在同一張卡每步 31.7 秒（10-31 實測），這組的速度要看測速結果。

## 流程

```bash
node tools/video/cli.mjs login --runpod --name "Claude 雲端 session"   # 第一次
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh usage              # 路線、本月額度、跑著的 pod
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh check --manifest jobs.json   # 免費
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh batch --manifest jobs.json --output-dir out/ --progress out/progress.json --label e033 --slug zhong-tian-qu-qi

# 一支
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh single --mode first_frame --image f.png --prompt p.txt --output o.mp4 --seconds 6

# 首格、補細節、放大（manifest 與 Colab 路線相同）
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh images --manifest ff.json --output-dir first-frames/
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh refine --manifest st2.json --output-dir refined/
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh upscale --input-dir refined/ --output-dir final/

# 手動開停；一批之間想留著就加 --keep
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh start --label pilot
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh stop
```

`--profile smooth|hero|draft`（或 `H3_PROFILE`）與 Colab 同義；沒指定就用後台 RunPod 卡的預設 profile，三段式第一段草稿是 `hero`（20 步、CFG 1、不掛加速 LoRA）；首格用 `.agents/skills/minimax-h3-colab/scripts/fit_first_frame.sh` 裁。`latent=image1`（Qwen）和 `guide=draft`（refine）這條路線還沒做，會直接報錯。

## 還沒實測

映像只在 CI 的 CPU 上驗過節點；真 GPU 的冷啟動、每支秒數、VRAM 與每支美元要等 pilot（票 `2026-10-30-runpod-h3-image-and-runner`），量到再寫進這裡。片段匯入與 1088p 畫布的產線檢查是另一張票 `2026-10-30-runpod-canvas-and-import`。

## 離線驗證

```bash
node --test tools/minimax-h3-runpod.test.mjs
```
