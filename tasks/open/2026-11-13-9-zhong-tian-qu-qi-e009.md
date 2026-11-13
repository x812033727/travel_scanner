---
id: 2026-11-13-9-zhong-tian-qu-qi-e009
title: 種田娶妻打天下 第 9 集真人版（zhong-tian-qu-qi-e009-r2）：Colab 拍攝、精修、審片、雲端備份與匯入後台
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-13T04:05:09Z
completed_at:
branch: antigravity/zt-e009-r2
depends_on: []
scope:
  - docs/videos/zhong-tian-qu-qi-e009-r2
  - docs/videos/series-plans/zhong-tian-qu-qi/production/writer-tools/e009-r2
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/ff-dh-e909.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e909.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/edit-dh-e909-live.json
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/e909-live
---

# 種田娶妻打天下 第 9 集真人版（zhong-tian-qu-qi-e009-r2）：Colab／RunPod 拍攝、精修、審片、雲端備份與匯入後台

## Why

延續真人重拍版第 1–8 集的定妝照、場景圖與製作規格，將已通過分鏡審稿的 `docs/videos/zhong-tian-qu-qi-e009-r2/script.md`（38 鏡、197.5 秒，夜戲，許家院子＋三女東屋、中屋、西屋）轉為完整拍攝規格、錄製非模型原聲台詞、拍攝 960×544 草稿與 1312×736 精修、完成獨立挑片與成片／表情審查、備份至 Google Drive 並匯入 `/admin/videos`。

## Definition of done

- [ ] 38 鏡真人版成片通過 `cut-qa.py`、`cut-jumps.py`、`audio-qa.py` 與獨立子代理成片／表情審查（嚴重與中等問題全數修畢）。
- [ ] 全部製作檔備份至 Google Drive `AI/備份/AI劇/種田娶妻打天下（真人版）/第009集/製作檔/` 並核對 0 差異。
- [ ] 成片、軟字幕（`burn_in: false`）與真人版封面透過 `node tools/video/cli.mjs import` 送進 `/admin/videos`。

## Steps

- [x] 建立 `writer-tools/e009-r2/{tl.mjs,build-r2.py,s01_19.py,s20_38.py,r2.py}`，產出 `docs/videos/zhong-tian-qu-qi-e009-r2/{video.json,overlays.json,storyboard.md}`、`hailuo/{ff,clips}-dh-e909.json` 與 `colab/runs/e909-live/spec.json`。
- [x] 產生真人版第一段草稿清單 `zhong-tian-qu-qi-e909-dh/runpod/live/d1/{retake.json,colab-jobs.json,prompts/}`（38 鏡 × 2 seeds `9091101`/`9091102` = 76 支，`960x544` `hero`），通過 `preflight-prompts.py`（0 error / 0 warning）、`check_manifest.py`（0 error / 0 warning）與 `npm run test:docs-videos`（256/256）。
- [x] 錄製全部 10 句非 `clip_voice` 台詞（`zq909a04`、`a09`、`a14`、`a17`、`a18`、`a20`、`a31`、`a32`、`a33`、`a34`，含 5 句 `xitong` 1.3× 電音後製）至 `zhong-tian-qu-qi-e909-dh/audio/`。
- [x] 將已完成的 `zhong-tian-qu-qi-e909-dh`（含 15 個 `.wav` 檔與 76 支草稿清單／提示詞）與 `docs-zhong-tian-qu-qi-e009-r2` 快照備份至 Google Drive `種田娶妻打天下（真人版）/第009集/製作檔/` 並核對 0 差異。
- [ ] 跑完第一段 76 支 `960×544` `hero` 草稿（Colab `G4` 或 RunPod），執行 `cuts.py`、獨立子代理挑片（`review-picks.tsv`）、`continuity-sheets.py` 連戲審查（含 `s01` 接第 8 集 `s40`）與必要的 `RETAKE`。
- [ ] 跑完第二段 `1312×736` σ0.5 `refine`（不做 SeedVR2），建立 `hailuo/edit-dh-e909-live.json` 並以 `assemble-v4.mjs` + `alimiter=limit=0.63` + `loudnorm2.sh` 合成 1080p 成片。
- [ ] 通過 `cut-qa.py`、`cut-jumps.py`、`audio-qa.py`、三項人工檢查與獨立子代理成片／表情審查，製作 `thumbnail.png`（1280×720），完整備份至 Google Drive 並匯入 `/admin/videos`。

## How to verify

```bash
python3 docs/videos/series-plans/zhong-tian-qu-qi/production/writer-tools/storyboard-check.py docs/videos/zhong-tian-qu-qi-e009-r2/script.md
python3 -I docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/preflight-prompts.py ~/mokaair-work/videos/zhong-tian-qu-qi-e909-dh/runpod/live/d1/retake.json
bash .agents/skills/minimax-h3-colab/scripts/h3.sh check --manifest ~/mokaair-work/videos/zhong-tian-qu-qi-e909-dh/runpod/live/d1/colab-jobs.json
npm run test:docs-videos && npm run check:tasks
```

## Notes

- **已完成的前置與備份位置（2026-11-13）**：
  - 分支 `antigravity/zt-e009-r2` 已包含第 9 集全部 repo 內規格（`video.json`、`overlays.json`、`storyboard.md`、`writer-tools/e009-r2/`、`ff-dh-e909.json`、`clips-dh-e909.json`、`colab/runs/e909-live/spec.json`）。
  - Google Drive `AI/備份/AI劇/種田娶妻打天下（真人版）/第009集`（folder ID `1Gu6ThzJIG6TRSOLmnhHWznuddnQ3N38q`）底下的 `製作檔`（`1bcSmyz2KRLfpMXp6E7rq7fkXfq0LErUO`）已備份：
    - `zhong-tian-qu-qi-e909-dh`（`1ZibEXd9ZXd0FWFlawUQhuJPZqnUlA1b_`，178 個檔案、0 差異）：含 `audio/` 全部 10 句錄音與 5 個 `.raw-tts.wav`（不需重錄）、`runpod/a/st1/`、`runpod/live/st1/`、`runpod/live/d1/{retake.json,colab-jobs.json,prompts/}`。
    - `docs-zhong-tian-qu-qi-e009-r2`（`1M3PyuZsOwOmmBgiDM0TLy0YXaKb3Cj6T`，4 個檔案、0 差異）。
- **寫規格踩到並已修掉的點**：
  - `LOC["tang"]`/`LOC["qin"]`/`LOC["aling"]` 不寫角色英文名，避免 `gen-dh.mjs` 在單人鏡誤掛屋主定妝照；`s04`、`s16`、`s25` 畫外視線加上 `off screen left/right`；`s21` 暗景插鏡放 `xuyan` 袖口特寫錨定（38 鏡全數 1 對 1 對應角色定妝照，`sets` 只有 `s01` 掛 `dh-set-xujia-yuan-t1`）。
  - 被褥顏色寫 `dark ash-grey`、棉被寫 `dark-indigo`，避開 `reddened eyes` 後面出現 `blue` 觸發 `preflight-prompts.py` 的 `eye-glow` 誤報。
- **Antigravity 容器跑 Colab 的限制與暫停原因**：
  - Antigravity VM 的沙盒代理 `agy-plugin-proxy` 放行純 HTTPS（`colab usage`/`start`/`upload`/`stop` 皆 200/204），但對所有 WebSocket 升級（`colab exec`/`run`/`ssh` 連線至 `wss://*.prod.r.colab.dev/api/kernels/.../channels`）回傳 `403 Forbidden: WebSocket upgrades are not allowed`；當時開的 `zt-e909`（`G4`）已立即停機，0 支草稿生成。
  - 下一個接手的 session：若在支援 WebSocket 的環境（Claude Code 雲端 session 或本機 WSL）可直接用 `d1/colab-jobs.json` 跑 Colab `G4`；若在 Antigravity 環境則配對 `login --runpod` 改走純 HTTPS 的 `h3r.sh`（直接吃 `d1/retake.json` 與 `refine-prep.py`）。站主指示先暫停，已釋出票供後續接手。
