---
id: 2026-10-28-zhong-tian-e031-colab-pilot
title: 種田娶妻 e031 Colab 小樣：首格與片段實拍、CU 與分鐘數回填
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-28T09:00:55Z
completed_at:
branch:
depends_on:
  - 2026-10-27-minimax-h3-on-colab-from-a
scope:
  - docs/videos/zhong-tian-qu-qi-e031
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab
  - .agents/skills/minimax-h3-colab/references/cloud-pairing.md
---

# 種田娶妻 e031 Colab 小樣：首格與片段實拍、CU 與分鐘數回填

## Why

PR #1909（票 `2026-10-28-31-60-colab-qwen-image-edit`，已結）把路線 B 的工具做完：Qwen-Image-Edit-2509
首格筆記本、`h3.sh images`、兩支轉檔。全部只用假 colab 離線測過，沒碰真的 Colab。站主配對 Colab 之後，
第一批真跑要在 e031 上量數字、驗畫質，才知道規劃時每集約 60 CU、30 集約 1,800 CU 的預估對不對，
以及三個沒驗的設計決定站不站得住。做法與指令在
`docs/videos/series-plans/zhong-tian-qu-qi/production/colab/README.md`。

## Definition of done

- [ ] e031 的 brief／script／storyboard／video.json 照既有流程寫好（集票另開或併在這張），
      `gen-dh.mjs` 出 `ff-dh-e031.json` 與 `clips-dh-e031.json`。
- [ ] 小樣三鏡（含一個雙人鏡、一個顏值鏡）：`ff2manifest.mjs --only` → `h3.sh images` → 代理審首格
      （女角不露、不血腥、畫面無字、唐小棠高領；臉像不像定妝照）→ `clips2manifest.mjs --only` → `h3.sh batch`，
      同一個 `--session`。
- [ ] 回填數字：冷啟動分鐘、磁碟（兩組模型放不放得下）、一張首格與一支片各幾秒幾 CU、`colab usage`
      前後餘額差，寫進 `.agents/skills/minimax-h3-colab/references/cloud-pairing.md` §4 與本票。
- [ ] 三個設計決定的結論寫進 `production/colab/README.md`：空白 latent（`QIE_LATENT=empty`）的構圖對不對提示詞、
      還是要改 `image1`；三人同框第三人只剩文字描述時臉像不像，要不要拆鏡；1312×736 放大到 1080p 的畫質。
- [ ] 小樣過了做完 e031 整集、剪出來給站主看；不過就改設計再跑一輪小樣。

## Steps

- [ ] 站主：配對 Colab（後台 /admin/ai-accounts「Google Colab」區，或 secret `COLAB_CLI_TOKEN_JSON`）。
- [ ] `bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh && h3.sh usage`，餘額抄下來。
- [ ] 照 `production/colab/README.md`「一集的流程」步驟 1–4，先只跑 `--only` 的三鏡。
- [ ] 看片：照 motion-quality.md 第六節；首格的第 0 格 PSNR 對的是 Qwen 畫的那張。
- [ ] 回填、寫結論、決定要不要全集。

## How to verify

`*.progress.json` 每鏡 `completed`、有 seed；`first-frames/sNN-t1.png` 是 1312×736；`clips/sNN-t1.mp4` 開聲音實速看，
說話的人嘴有動、沒有切鏡；`cloud-pairing.md` §4 的「沒試」格子都填了數字。

## Notes

- 規劃時的預估（未實測）：每集約 60 CU（首格 4、片段 48、冷啟動 6、hero 2），30 集約 1,800 CU；Pro+ 月配額若是
  500 CU 約做 8 集。
- 已知限制：首格一批最多 40 張、片段最多 20 支（轉檔自動分 part）；Qwen-Image-Edit 只收三張參照；
  `exec` 逾時後遠端可能還在跑，用 `--only` 只重跑沒完成的。
