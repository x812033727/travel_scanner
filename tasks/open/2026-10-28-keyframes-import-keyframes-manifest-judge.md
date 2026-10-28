---
id: 2026-10-28-keyframes-import-keyframes-manifest-judge
title: keyframes import：外部畫的首格進 keyframes manifest（站上 judge 可選）
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-28T07:30:10Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
  - tools/video/media/keyframes.test.mjs
  - tools/video/cli.mjs
  - docs/videos/DRAMA.md
---

# keyframes import：外部畫的首格進 keyframes manifest（站上 judge 可選）

## Why

站主 2026-10-28：《修仙獎勵》第 1 集的首格要在 Colab 的 GPU 畫（開源模型拿定妝照當參照），再用 Colab 的 H3 做片段（「在 Colab 先畫首格再 FL2VA」）。
現在只有 `clips import` 能把外面做的東西帶進產線；關鍵影格沒有對應的入口：`clips import` 要那一鏡在 `keyframes/manifest.json`
有通過 judge 的關鍵影格（第 0 格 PSNR 比對用），storyboard 關卡與 lookHash／visualHash 也綁 manifest。沒有 `keyframes import`，
Colab 畫的首格就只能繞過產線（像《種田》的海螺手工路線），沒有 judge、沒有帳本、`assemble` 不認。

## Definition of done

- [ ] `node tools/video/cli.mjs keyframes import --slug S --shot ID --file PNG --provider external [--judge] [--credits N --usd N --note "…"]`
      把一張外部圖放進 `keyframes/<shot>-import-<n>.jpg`、寫進 `keyframes/manifest.json`（綁現在的 look_hash／visual_hash，同 `clips import`），
      `--judge` 時用站上 judge 跑跟 `keyframes` 一樣的 rubric（識別題對定妝照）並照 passed 決定 needs_review；沒有 `--judge` 時
      是站主的選擇，needs_review false、記 `imported`；費用與 note 進帳本。
- [ ] 一張同樣的圖再匯入一次不重複（同 bytes 同檔名）；尺寸低於 1280×720 拒絕；lint 錯誤先擋。
- [ ] 之後 `clips import` 對這一鏡能過（第 0 格 PSNR 用這張）；storyboard 關卡的核准在匯入後變 stale（manifest 改了）。
- [ ] `docs/videos/DRAMA.md` 寫這條入口；`keyframes.test.mjs` 釘檔名、manifest 欄位、judge 有無兩種、拒絕的情況。

## Steps

- [ ] 照 `tools/video/media/clips.mjs` 的 `importClip` 寫 `importKeyframe`，judge 的呼叫抽成 `keyframes.mjs` 畫圖與匯入共用的 helper。
- [ ] `cli.mjs` 的 `keyframes` 多一個子命令 `import`（同 `clips import` 的接法）。
- [ ] 測試與文件。

## How to verify

```bash
node --test tools/video/media/keyframes.test.mjs
node tools/video/cli.mjs keyframes import --slug xiuxian-jiangli-e001 --shot s36 --file <png> --provider external --judge
node tools/video/cli.mjs clips import --slug xiuxian-jiangli-e001 --shot s36 --file <mp4> --provider external
```

## Notes

- 先做這張，再做 `2026-10-28-1-colab-qwen-image-edit-2509`（Colab 畫首格）；沒有入口，Colab 的圖進不了產線。
- 2026-10-28：站主 Colab Pro+、A100；Gemini 畫 45 鏡約 US$6–9，Colab 估 8–25 CU（約 US$1–2.5），差額不大，站主仍選 Colab。
