---
id: 2026-10-28-31-60-colab-qwen-image-edit
title: 種田娶妻 第 31–60 集：首格與片段都在 Colab 做（Qwen-Image-Edit 首格、H3 FL2VA 片段）
status: done
priority: P1
area: tools
owner: claude-fable-5.1-zt-colab
claimed_at: 2026-10-28T07:24:42Z
created_at: 2026-10-28T07:20:55Z
completed_at: 2026-10-28T09:01:21Z
branch: claude/compassionate-fermat-4jl79a
depends_on:
  - 2026-10-27-minimax-h3-on-colab-from-a
scope:
  - .agents/skills/minimax-h3-colab
  - .claude/skills/minimax-h3-colab
  - tools/minimax-h3-colab.test.mjs
  - docs/videos/series-plans/zhong-tian-qu-qi/production/colab
---

# 種田娶妻 第 31–60 集：首格與片段都在 Colab 做（Qwen-Image-Edit 首格、H3 FL2VA 片段）

## Why

站主 2026-10-28 定：《種田娶妻打天下》第 31–60 集（第一季剩下的 30 集）不再用海螺，
首格與片段都在 Colab 的 GPU 上做（路線 B）。片段走 skill `minimax-h3-colab` 的 `first_frame`
模式已經有工具；首格沒有：上游筆記本只跑 H3 影片，海螺時期的首格是圖片頁用定妝照、三視圖與
場景圖當參照畫出來的（`production/hailuo/gen-dh.mjs` 的 ff 清單、`fetch-dh.sh`），所以要在同一個
Colab session 裡加一個吃多張參照的圖像模型，再把首格接進 FL2VA。

模型選 **Qwen-Image-Edit-2509**（Apache 2.0，可商用；ComfyUI 原生支援；多張輸入圖，正好對應
角色定妝照＋場景圖；有 8 步 Lightning LoRA）。FLUX.1 Kontext dev 是非商用授權，頻道有營利，不用。

預估（2026-10-28，未實測；每集 100 秒約 38 鏡，第 25–30 集實測 0.34 鏡/秒；第 31–60 集規劃
總長 3,425 秒 ≈ 1,160 鏡）：

| 項目 | 每集 | 30 集 |
| --- | --- | --- |
| 首格：Qwen-Image-Edit 8 步、1312×736，A100 一張約 15–25 秒，重畫係數 1.3 | 約 4 CU | 約 120 CU |
| 片段：H3 `smooth` 一支 5–6 秒約 1 CU，重拍係數 1.25 | 約 48 CU | 約 1,450 CU |
| 冷啟動（ComfyUI、H3 約 40 GiB、Qwen-Image-Edit 約 40 GiB）每集一個 session | 約 6 CU | 約 180 CU |
| 顏值鏡 `hero` | 約 2 CU | 約 60 CU |
| **合計** | **約 60 CU（45–90）** | **約 1,800 CU（1,200–2,700）** |

Pro+ 每月配額（500 CU，未確認，以後台卡片的 `colab usage` 為準）約做 8 集；一個月做完要加購
約 1,300 CU（100 CU = US$9.99）。海螺不再花點。磁碟：A100 高 RAM runtime 要放得下兩組模型
（H3 筆記本說至少 60 GiB，Ref2VA 備援 80 GiB，加 Qwen 約 40 GiB），第一次跑先看 `df`。

## Definition of done

- [x] `h3.sh images --manifest <ff.json>`（`scripts/images.py` 加 `assets/qwen_image_edit.ipynb`）在同一個 Colab session 用
      Qwen-Image-Edit 從參照圖與提示詞產出 1312×736 的首格 PNG，命名 `sNN-tK.png`（工作區既有的命名，`assemble-v4.mjs` 讀得到），下載到
      `<VIDEO_WORKDIR>/zhong-tian-qu-qi-eNNN-dh/first-frames/`；送出前 `h3.sh images-check`（參照檔存在、
      1–3 張、尺寸、`image N` 對得上、重複輸出），有 `progress.json`（含 seed），逾時原則與 H3 相同（`--only` 只重跑沒完成的）。
- [x] 轉檔工具：`production/colab/ff2manifest.mjs`（ff 清單 → 首格 manifest，每 40 張一份）、`clips2manifest.mjs`（`clips-dh-eNNN.json` → H3 manifest，每 20 支一份，
      `first_frame`、1312×736、秒數照 gen-dh、`prompts/clip-sNN.txt` 原封不動、全文 `prompt_sha256`）。
      片段輸出 `sNN-tK.mp4` 放進 `clips/`，`assemble-v4.mjs` 不用改。
- [ ] 首格審查留在產線：PNG 下載後由代理照第 1–24 集掃描的規則看（女角不露、不血腥、畫面無字、
      唐小棠高領），退的重畫 t2；通過的才進片段 manifest。
- [ ] e031 小樣：三鏡（含一個雙人鏡、一個顏值鏡）首格→審查→片段，跟 e030 的 3D 國漫定妝照比畫風與臉；
      記冷啟動分鐘、一張圖與一支片各扣幾 CU、`colab usage` 前後餘額，寫進
      `.agents/skills/minimax-h3-colab/references/cloud-pairing.md` §4 與本票。
- [ ] 小樣過關後 e031 整集做完、剪出來給站主看；站主點頭才排 e032 起，每集一個 session、兩個 manifest。
- [x] skill 文件（SKILL.md 流程、pipeline-handoff.md §5）寫上首格這一段；`.claude/skills` 副本 byte-identical；
      `tools/minimax-h3-colab.test.mjs` 用假 `colab` 蓋到筆記本、檢查器、`images.py` 與 wrapper；轉檔器的測試在 `production/colab/manifests.test.mjs`。

## Steps

- [x] 筆記本：`.agents/skills/minimax-h3-colab/assets/qwen_image_edit.ipynb`（本 repo 自己的），
      ComfyUI 原生 Qwen-Image-Edit-2509 節點（官方 2509 範本的接法：`TextEncodeQwenImageEditPlus`、`ModelSamplingAuraFlow` shift 3、`CFGNorm`）與 8 步 Lightning LoRA，
      `QIE_*` 環境變數帶參照圖、提示詞檔、尺寸、seed、latent 來源、輸出路徑；跟 H3 共用 `/content/ComfyUI` 與 `--session NAME`。
- [x] `scripts/images.py` 與 `h3.sh images`／`images-check`：上傳參照圖與提示詞、`colab exec`、下載 PNG（驗 IHDR 尺寸）、寫 `progress.json`。
- [x] `scripts/check_images_manifest.py`：參照檔、1–3 張、16 的倍數與面積、`image N` 對得上張數、seed、latent、重複輸出、提示詞非空；`<Picture N>` 與沒點名圖片只警告。
- [x] `production/colab/ff2manifest.mjs`、`clips2manifest.mjs`，用法在 `production/colab/README.md`。
- [ ] 參照圖：沿用 `_series/zhong-tian-qu-qi/refs-dh/` 的定妝照（唐小棠用 t2 立領版）與 `dh-set-*` 場景圖，
      提示詞沿用 gen-dh 的首格提示詞；Qwen-Image-Edit 對「哪張參照是誰」的讀法要在小樣驗。
- [ ] e031 的 brief／script／storyboard／video.json 照既有流程先寫好（不在本票 scope；走 docs 的集票）。

## How to verify

```bash
node --test tools/minimax-h3-colab.test.mjs tools/skills.test.mjs
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh            # 要配對過（exit 4 表示沒配對）
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage             # 前
bash .agents/skills/minimax-h3-colab/scripts/h3.sh images --manifest docs/videos/series-plans/zhong-tian-qu-qi/production/colab/ff-e031-pilot.json --session zt31
bash .agents/skills/minimax-h3-colab/scripts/h3.sh batch  --manifest docs/videos/series-plans/zhong-tian-qu-qi/production/colab/clips-e031-pilot.json --session zt31 --stop-on-complete
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage             # 後，差額寫進票
```

三支片段：第 0 格對首格 PSNR ≥ 22、臉同定妝照、說話鏡嘴有動、沒有切鏡；`assemble-v4.mjs` 能吃 1312×736 的片放大到 1080p。

## Notes

- 2026-10-28 工具做完（本票的分支）：筆記本、`images.py`、檢查器、`h3.sh images`、兩支轉檔、文件、測試；離線測試全綠
  （`tools/minimax-h3-colab.test.mjs` 15 個、`production/colab/manifests.test.mjs` 3 個）。沒碰真的 Colab：
  站主配對後照 `production/colab/README.md` 的「第一批要量的」做 e031 小樣。
- 做的時候才知道的：gen-dh 的首格清單一鏡最多 4 張參照（3 張定妝照＋場景），Qwen-Image-Edit 只收 3 張，所以轉檔
  固定留場景圖＋前兩張定妝照、被擠掉的印出來（e030 有 7 鏡）；e030 有 44 鏡，超過一批 40 張，轉檔自動分 part；
  上游 H3 runner 一批最多 20 支，片段也分 part。`images.py` 的 output_name 原本會把 `.png` 的點換成 `-`，已修。
- 沒做、留給小樣決定：Qwen-Image-Edit 用空白 latent（`QIE_LATENT=empty`）從參照圖畫新構圖，官方範本是編碼第一張圖再改
  （`image1`），哪個對《種田》的首格比較好要實拍；三人同框第三人只剩文字描述，臉不像就拆鏡或用 `image1` 重畫。

- 2026-10-28 規劃時的替代案：路線 A「Ref2VA 不畫首格」每集約 70 CU、重拍係數 1.5，
  失去首格階段的內容審查，站主不選；首格繼續用海螺每集約 1,000 點。本票是路線 B。
- 輸出只有 1312×736，`assemble-v4.mjs` 放大到 1080p 的畫質沒驗，小樣一併看。
- Colab 的 Turbo LoRA 版 H3 不是海螺的 H3，臉的一致性在 e031 小樣才知道；A100 配不到或餘額不足時
  先問站主再換 GPU 或 `--no-high-mem`。
- `exec` 逾時後遠端可能還在跑，重跑會重扣；只重跑 `progress.json` 沒完成的鏡。
