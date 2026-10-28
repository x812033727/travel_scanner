---
id: 2026-10-28-1-colab-qwen-image-edit-2509
title: 修仙獎勵 第 1 集：Colab 先畫首格（Qwen-Image-Edit-2509）再 H3 片段
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-28T07:30:10Z
completed_at:
branch:
depends_on:
  - 2026-10-28-keyframes-import-keyframes-manifest-judge
scope:
  - docs/videos/series-plans/xiuxian-jiangli/production/colab
  - docs/videos/series-plans/xiuxian-jiangli/production/e001-lock-package.md
---

# 修仙獎勵 第 1 集：Colab 先畫首格（Qwen-Image-Edit-2509）再 H3 片段

## Why

站主 2026-10-28：「在 Colab 先畫首格再 FL2VA」。第 1 集小樣三鏡的首格用站上的 Gemini 3 Pro（每張 US$0.134），其餘 42 鏡站主要改在
Colab 的 GPU 畫：開源模型拿定妝照當參照，點數便宜（估 8–25 CU），再用同一個 Colab session 跑 H3 片段。模型先選
Qwen-Image-Edit-2509（Apache-2.0，多張參照圖、`QwenImageEditPlusPipeline`，bf16 在 A100 40 GB 要 CPU offload；Lightning 8 步 LoRA
有就掛，沒有就 40 步）；對不對要三張小樣跟 Gemini 比過才知道。

## Definition of done

- [ ] `production/colab/first-frames/`：notebook（diffusers 跑 Qwen-Image-Edit-2509，輸入 manifest：每鏡 prompt、參照圖＝該鏡角色的定妝照
      ＋同一場的場景參照、1312×736、seed）、runner（同上游 H3 runner 的 Colab CLI 用法：new／upload／exec／download／stop，進度 json、
      前後 `usage`）、`gen-first-frames-manifest.mjs`（從 video.json 用 `shotPrompt` 組 prompt）。
- [ ] 小樣三鏡（另選一場）：Colab 畫的首格 `keyframes import --judge` 進產線，跟 Gemini 的同鏡對照交站主看；站主點頭才畫整集。
- [ ] 整集：42 鏡首格進 manifest、storyboard 關卡核准、`gen-h3-manifest.mjs` 的 first-frames 用它們、H3 片段 39 支、`clips import`。
- [ ] 收據：每批 CU 前後差、每張秒數、模型與步數、seed；寫進鎖定包（變更單 3）與 `colab/README.md`。

## Steps

- [ ] 等 `keyframes import` 落地（depends_on）。
- [ ] notebook 與 runner；先一張，量 A100 上的秒數與記憶體（offload 或 fp8）。
- [ ] 小樣三張 → 站主看 → 整集。

## How to verify

```bash
python3 -I .agents/skills/minimax-h3-colab/scripts/check_manifest.py docs/videos/series-plans/xiuxian-jiangli/production/colab/h3/manifest.json   # first-frames 都在
node tools/video/cli.mjs status --slug xiuxian-jiangli-e001
```

## Notes

- 這集已經花的：設定圖 US$5.06（Gemini）、關鍵影格 3 張 US$2.02、H3 小樣兩版 1.82 CU。
- Hugging Face 從 session 的代理抓是 401，Colab 裡抓沒問題；LoRA 檔名以 Colab 裡 `huggingface_hub.list_repo_files` 為準。
