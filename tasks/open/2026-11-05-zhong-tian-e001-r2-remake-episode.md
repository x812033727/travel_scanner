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
- 2026-11-05 站主（經審片轉達）：所有集會合成一支長片，r2 各集**不放片名卡、不寫集數、不回顧上一集**，每集第一鏡接上一集最後一鏡；`edit-dh-e901.json` 已拿掉 `title`。系統要換新聲音（還沒定）：系統台詞 `zq901a04`、`a08`、`a35`、`a36` 各自是一支獨立的錄音，換聲音時只重錄這四支、重跑 `asm.sh`，不必重剪。
- 第 2–10 集的 r2 稿子審片正在寫（`docs/videos/zhong-tian-qu-qi-e0NN-r2/script.md`、`production/r2-bible-e001-e010.md`），送過來之前不要開始。
- 2026-11-05 走一遍收尾流程時補的洞：
  - `stage-clips.sh` 的工作資料夾寫成 `e0$N`（901 會變 e0901），改成三位數；`SRC=refined` 改拿第二段 1312×736 的片（r2 不升 1080p）：`SRC=refined bash colab/route-a/stage-clips.sh 901`。
  - `prep-import.mjs`：`video.json` 的 slug 跟編號不同時用它的 slug（901 → `zhong-tian-qu-qi-e001-r2`）；`meta.json` 的 note 要改成「第 1 集重製版 r2，對照原版第 1 集」。
  - `gen-dh.mjs`：內心獨白（emotion 有「嘴閉著」「內心獨白」）與 `data.nospeak` 的人不再加「嘴在動」那句（s08、s38 原本會對嘴）；`build-r2.py` 把 `nospeak` 與 `BUY`（長鏡秒數）帶進 `video.json`。
  - 用已經抽好的草稿在暫存資料夾試剪一次：45 句、面板、配樂、音效、`punch: false`、新的閃避都跑得過（196.7 秒、exit 0）；照新的秒數只有 s35 還會不夠長，改買 12 秒。
- 第二批草稿 v2（31 鏡 × 2）：EU-CZ-1 從 16:01 起沒貨，`scratchpad/r2v2loop.sh` 每次放棄就重開，最多 4 小時。
- 2026-11-05 22:50 站主把 r2 上限從 US$25 提高到 US$28（容器 20:15 重啟，pod 閒置到 21:15 才被站台停掉，多花約 US$2.6）。
