---
id: 2026-10-27-xiuxian-e001-colab-pilot-to-cut
title: 修仙獎勵 第 1 集：Colab 小樣、配音、剪接
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-27T23:38:58Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/xiuxian-jiangli-e001
  - docs/videos/series-plans/xiuxian-jiangli/production
---

# 修仙獎勵 第 1 集：Colab 小樣、配音、剪接

## Why

第 1 集的分鏡、鎖定包、鎖定檔與 Colab 路線都在 PR #1893（`docs/videos/series-plans/xiuxian-jiangli/production/`）。站主 2026-10-27 定：3D 國漫、Colab 直接打 MiniMax API（image-01 首格、H3 v2 片段）、約 92 秒、聲音照建議、先做小樣 s33–s35。花錢的部分要站主在 Colab 跑，之後的配音與剪接在本機。

## Definition of done

- [ ] Colab 權杖配對一次並存成 `COLAB_CLI_TOKEN_JSON`；站上產線出 `look` 與 `keyframes`（站主過關卡）；用 `h3/manifest-pilot.json` 跑小樣三支，`progress.json` 與 `colab usage` 前後餘額留下；代理看過：臉同定妝照、動作做完、s34 嘴有動、兩人鏡的第二張臉能不能用
- [ ] 小樣不過就改設計、重產 `e001-jobs.json`、`plan_lock.mjs --write --force` 重鎖；過了才 `frames` → `clips`
- [ ] 四個聲音試聽（`voice-audition.md`），定了寫回 `production/cast.json` 與 `video.json`
- [ ] 本機 `tts` → `check-audio`，用 `timeline.json` 重跑 `shot_plan.mjs --timeline` 確認買的秒數沒變
- [ ] 寫 `edit-e001.json`（片名卡、名牌、分場調色、配樂 cue），仙錄面板樣式從淡藍改成藍金色書頁；用《種田》的 `assemble-v4.mjs` 剪出第一版，開聲音看一遍
- [ ] 收據的 `prompt_sha256` 全部等於 `e001-plan-lock.json`；實際 take 數與美元回填 `e001-lock-package.md` 第 9 節

## How to verify

`node tools/video/cli.mjs lint --slug xiuxian-jiangli-e001` 0 錯誤；`drama_craft_check.mjs`、`shot_reading.mjs --route hailuo`、`shot_plan.mjs --strict` 照 `e001-lock-package.md` 第 2 節重跑；剪出的 mp4 開聲音看，說話的人嘴要動、面板字要對 `overlays.json`。

## Notes for the next person

main 在 2026-10-28 合進 PR #1894 的 skill `minimax-h3-colab`（Colab GPU 跑開源 H3，雲端 session 用權杖配對驅動）。`production/colab/README.md` 現在列兩條路：A 用那個 skill 跑片段（`h3/manifest-pilot.json`，要先配對 `COLAB_CLI_TOKEN_JSON`、首格另外畫），B 筆記本打付費 API。站主 2026-10-28 定走 A，B 已刪；首格用產線 `keyframes`。

做法與坑在 `production/colab/README.md`。image-01 的 `subject_reference` 一次只收一張人像，兩人鏡的第二張臉是這條路線最大的風險；不行改 H3 參考生影片（不帶首格）手放。H3 有首格時不能帶參考圖（官方）。1026／1027 是內容被拒，先回報不換字繞。
