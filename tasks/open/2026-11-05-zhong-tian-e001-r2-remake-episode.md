---
id: 2026-11-05-zhong-tian-e001-r2-remake-episode
title: Zhong-tian e001 r2: remake episode 1 (new script, camera-feel rules), stage 2 only, zh cut for the owner
status: in-progress
priority: P2
area: docs
owner: claude-opus-5.5-zt-e043
claimed_at: 2026-11-05T11:10:59Z
created_at: 2026-11-05T11:10:58Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/minimax-h3-runpod/scripts/route_a_st23.sh
---
# Zhong-tian e001 r2: remake episode 1, stage 2 only, zh cut for the owner

## Why

站主 2026-11-05：原版第 1 集打 40 分、參考的《孟婆今天也不想上班》80 分，要比 80 好。稿子與交辦在 `docs/videos/zhong-tian-qu-qi-e001-r2/`（`script.md`、`brief.md`），量法在 `origin/claude/zhong-tian-camera-feel` 的 `camera-feel-study-20261105.md`。預算：站主同意以 RunPod 美元計，估 US$16，**超過 US$25 先停下來回報**。

## Definition of done

- [ ] 三鏡試拍（s05、s13、s22）鏡內動量 ≥ 7、靜止幀 ≤ 15%，給站主看數字
- [ ] 其餘 35 鏡（每鏡兩個種子），只做到第二段 1312×736
- [ ] 中文整句配音、剪接（punch false、slow_max 1.1、interpolate false、duck 3.5／900 ms）、量成片寫進 brief.md 最後一節
- [ ] `import --from`（備註「第 1 集重製版 r2」），只送成片

## Notes

- 內部工作編號 901：工作資料夾 `~/mokaair-work/videos/zhong-tian-qu-qi-e901-dh/`、`hailuo/*-dh-e901.json`、`colab/runs/e901/`；
  `docs/videos/zhong-tian-qu-qi-e901` 是本機指向 `zhong-tian-qu-qi-e001-r2` 的連結（`.git/info/exclude`，不進 git），發布 slug 是 `zhong-tian-qu-qi-e001-r2`。
- 製作檔由 `writer-tools/e001-r2/build-r2.py r2` 產生（`r2.py` 是 38 鏡的規格）。
- `route_a_st23.sh` 加了 `NO_UPSCALE=1`；`assemble-v4.mjs` 加了 `punch: false` 與 `duck_ratio`／`duck_release_ms`（預設不變）。
- `colab/runs/_scripts/camera-feel.py` 照研究的量法量片段或成片（第 55 集成片：動量 3.9、靜止 34%）。
- 新配樂：`cue-river`、`cue-warm`（Lyria，各約 US$0.08）。
- 工作資料夾每天推一次到 `transfer/zt-e001-r2-work`（站主同意）。
