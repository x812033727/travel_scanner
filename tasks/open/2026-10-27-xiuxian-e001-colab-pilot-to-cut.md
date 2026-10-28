---
id: 2026-10-27-xiuxian-e001-colab-pilot-to-cut
title: 修仙獎勵 第 1 集：Colab 小樣、配音、剪接
status: in-progress
priority: P1
area: docs
owner: claude-fable-5.1
claimed_at: 2026-10-28T07:44:54Z
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

第 1 集的分鏡、鎖定包、鎖定檔與 Colab 路線都在 PR #1893（`docs/videos/series-plans/xiuxian-jiangli/production/`）。站主 2026-10-27 定：3D 國漫、約 92 秒、聲音照建議、先做小樣 s33–s35；2026-10-28 定：片段只在 Colab 的 GPU 跑開源 H3（skill `minimax-h3-colab`），設定圖與關鍵影格用產線的 look／keyframes，不打 MiniMax 付費 API。

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

做法與坑在 `production/colab/README.md` 與 `.agents/skills/minimax-h3-colab/`。開源 Turbo LoRA 版 H3 的一致性沒實測，小樣先量；`colab new`／`exec` 經代理的 WebSocket 沒試過，卡住看 `~/.config/colab-cli/colab.log`；輸出 1344×768。

### 2026-10-28 進度（claude-fable-5.1）

- 配對：走 #1896 的站上配對（slot a，1000 CU），不是 `COLAB_CLI_TOKEN_JSON`；bootstrap 向站台要憑證可用。
- `look`：image-01 三輪沒過；站主選用 Gemini（PR #1899／#1900 的 `series.json` `image_model`），三視圖那版站主說「畫風不是很好」，改成《種田》定妝照寫法（#1903），定稿 江小滿 B、沈照雪 A、宋管事 F，look 關卡 05:20Z 核准。累計 US$5.06。
- `keyframes --shot s33,s34,s35`：s33／s35 照站主選的構圖改提示詞後全過（7.08／7.0／7.0，US$2.02），storyboard 關卡核准。
- Colab H3 小樣：第一版（4 秒、1344×768）三支成，0.69 CU；main 併 #1904 後照新規矩重鎖（#1907 的 shot_plan、#1903 的變更單 2：5／6 秒、1312×736、smooth、官方順序正文），第二版三支成，1.13 CU，第 0 格 PSNR 35.3／28.2／29.5 dB。站主看過第二版。
- `tts`：Gemini 語音 01:50Z–03:37Z 一直 429，07:19Z 成功（39 句、旁白 1:59）；`check-audio` 標 13 句，多是短句辨識誤聽，要站主聽的是 s07、s23、s42、s43。`clips import` 三支小樣（第二版）已進產線，收據 0.377 CU／支。
- 站主 2026-10-28 改路線：「在 Colab 先畫首格再 FL2VA」——其餘 42 鏡的首格不用 Gemini，改 Colab 畫（票 `2026-10-28-1-colab-qwen-image-edit-2509`），入口是 `keyframes import`（#1910）。
- #1908（另一個 session，manifest 5 秒／1312×736、變更單 8a）站主關掉；它的改動都在 #1903 裡做到底了，不另外 cherry-pick。
- 沒做：聲音試聽、`edit-e001.json`、收據回填第 9 節。
