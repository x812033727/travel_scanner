# 三段式 H3：960×544 定動作 → 1312×736 補細節 → SeedVR2 到 1920×1080

站主 2026-10-30 要的流程：先用小畫布把構圖與動作定下來、過關的才放大補細節、再過關的才交給 SeedVR2 放到 1080p。同一天在 Colab G4（RTX PRO 6000 Blackwell 96 GB）跑通《種田》e030 三鏡，這份是做法、數字與坑。單段的寫法（正文、秒數、畫布）仍以 `motion-quality.md` 為準。

## 一、流程

| 步驟 | 做什麼 | 指令 | 關卡 |
| --- | --- | --- | --- |
| 0 | 鎖定包定稿正文；首格裁兩份：960×544（第一段）、1312×736（第二段 keyframe） | `fit_first_frame.sh`（或 ffmpeg cover-crop）、`h3.sh check` | 格式錯誤在本機擋掉 |
| 1 | H3 生成 960×544，`hero`（20 步、不掛 LoRA、CFG 1）、seed 固定 | `H3_PROFILE=hero bootstrap.sh patch`；`COLAB_GPU=G4 h3.sh batch --manifest st1.json …` | **關卡 1**：構圖、動作、嘴；不過換 seed 只重做這一段 |
| 2 | 拉伸到 1312×736，從 σ0.5 重算 10 步，首格當 frame 0 keyframe | `h3.sh refine --manifest st2.json --output-dir refined/` | **關卡 2**：臉與第一段同一張、第 0 格 PSNR ≥ 22 |
| 3 | SeedVR2 3B 到短邊 1080，剪掉 prepend 的格，置中裁成 1920×1080 | `h3.sh upscale --input-dir refined/ --output-dir final/` | 幀數＝輸入；皮膚是否補得太寫實 |
| 4 | 進產線 | `clips import`（凍格、切鏡、第 0 格 PSNR）→ `music` → `assemble` | 既有規則 |

**按階段整批跑**：整集先跑完第一段 → 停 session、審 → 再開 session 跑第二段 → 審 → 第三段。審片時沒有 GPU 開著；每段各付一次冷啟動（2–3 分鐘）。

第二段 manifest（`jobs[]`）：`id`、`input_video`（第一段的 MP4）、`first_frame`（1312×736 那張）、`prompt_file`（與第一段同一份正文）、`output_name`；可選 `width`／`height`（預設 1312×736）、`sigma_start`（預設 0.5）、`steps`（預設 10）、`seed`（用第一段的 seed）。`refine.py --manifest … --check` 免費先擋錯。

## 二、第二段為什麼從 σ 開始，不是「20 步的後 10 步」

H3 的 video flow shift 是 12（ComfyUI `supported_models`：shift 12.0、audio_shift 3.0）。20 步 `simple` 排程的第 10 步，σ = 12·0.5/(1+11·0.5) ≈ **0.92**：從那裡重算幾乎等於重新生成，第一段定好的動作會被改掉。`h3_refine.ipynb` 改成在 base grid 上從 `sigma_start` 等距排 `steps` 步、再套 shift，十步全落在細節區：

- σ0.7：0.700, 0.673, 0.642, 0.607, 0.565, 0.515, 0.455, 0.381, 0.288, 0.166, 0
- σ0.5：0.500, 0.472, 0.440, 0.406, 0.367, 0.324, 0.276, 0.221, 0.158, 0.085, 0

圖（核心節點，接法照 Henge `alisson-anjos/Henge` MIT 的 `full_refiner_graph`）：`VHS_LoadVideoPath` → `ImageScale`（lanczos、拉伸，960×544 與 1312×736 比例差約 1%）→ `VAEEncodeTiled` → 與空的音訊 latent `LTXVConcatAVLatent` → `MiniMaxH3ImageToVideo`（只取 conditioning：正文＋首格 keyframe）→ `ManualSigmas` → `SamplerCustomAdvanced`（`res_multistep`）→ `VAEDecodeTiled`。音訊不保留。像素空間放大再編碼，不直接放大 latent（直接放大要另外的 latent upscaler 模型，見第五節）。

## 三、實測（2026-10-30，Colab Pro+ 帳號 A，G4，e030 s21／s34／s42，5–6 秒）

| 段 | 每支（暖機後） | 這批 | CU | 品質 |
| --- | --- | --- | --- | --- |
| 1：960×544、20 步 | 5 秒 1:24、6 秒 1:57（第一支含冷啟動 4:55） | 3 支、8.4 分 | 1.07 | 三鏡構圖動作照正文；第 0 格 PSNR 33.8／30.2／30.9 |
| 2：σ0.5、10 步 | 算圖 105（5 秒）／145 秒（6 秒），連上傳下載約 2:45 | 6 支（σ0.7、σ0.5 各 3）、18.3 分 | 2.51 | 鬍鬚、髮絲、柵欄、石頭明顯補出；σ0.7 細節多但臉型與眼型會變，σ0.5 最貼第一段；第 0 格 PSNR σ0.7 36.0／32.2／33.2、σ0.5 31.1／28.1／28.6 |
| 3：SeedVR2 3B fp16 | 117（5 秒）／142 秒（6 秒），第一支含下載與載入 309 秒 | 3 支、10.6 分 | 1.48 | 皮膚、裂縫、草、髮梢最銳；皮膚紋理偏寫實（毛孔、額頭），國漫要盯 |

三段合計 5.06 CU；暖機後一支 6 秒走完三段約 7 分、約 0.9 CU。G4 扣點約 7.6–8.4 CU／小時（session 停後讀餘額差；Colab 入帳可能延遲，下批再對一次）。

## 四、坑

| 症狀 | 原因 | 怎麼辦 |
| --- | --- | --- |
| `colab new` 回「Backend rejected accelerator 'G4'」 | 帶了 `--high-mem` | `h3.sh`、`images.py`、`refine.py`、`upscale.py` 在 G4／L4 都不再要 high-RAM |
| 「從第 10 步接著算」把動作改掉 | shift 12，第 10 步 σ≈0.92 | 用 `sigma_start`（第二節） |
| SeedVR2 輸出多 4 格（158 → 162） | `--prepend_frames 4` 的倒放格 CLI 沒移除 | `seedvr2_upscale.ipynb` 剪掉並核對幀數，不符就停 |
| SeedVR2 短邊 1080 時寬是 1925 | 1312×736 不是精確 16:9 | 置中裁 1920×1080 |
| `colab upload … /content/dir/x.mp4` 回 500 | upload 不會建資料夾 | 傳到 `/content/s3in__x.mp4`，notebook 再搬 |
| notebook 載的不是 BF16 | 上游選 `fl2va_pruned_int8_convrot`（CUDA 13）與 `qwen3vl_32b … nvfp4_awq` | 數字都以這組量化權重為準；BF16 沒量過 |

## 五、變體試做（2026-10-30，同三鏡同 seed）

第二段（manifest 的 `guide`、`sigmas`、`sampler`），9 支 52 分鐘、8.62 CU。逐格變化是 s34（鎖定鏡）同一塊背景的相鄰格平均差，越低越穩；只量一鏡一塊，只當方向。

| 做法 | 6 秒／5 秒算圖 | 第 0 格 PSNR（s21／s34／s42） | 逐格變化 | 看到的 |
| --- | --- | --- | --- | --- |
| **σ0.5、無引導（預設）** | 145／105 秒 | 31.1／28.1／28.6 | **0.259** | 細節最銳 |
| σ0.5＋整支草稿引導 | 435／290 秒 | 29.4／26.6／27.0 | 0.328 | 皮膚較平滑 |
| σ0.7＋整支草稿引導 | 435／290 秒 | 30.6／27.6／27.4 | 0.457 | 臉比無引導的 σ0.7 穩，閃爍最多 |
| Henge 3 步 sigmas＋`er_sde`＋引導 | 160／110 秒 | 32.0／29.3／29.1 | 0.426 | 細節接近預設，閃爍較多 |

結論：預設不變。整支引導（`MiniMaxH3AddGuide`）多一份畫面要算，慢 3 倍，換到的身份穩定不大。所有版本的運鏡都與草稿差不到 0.5%（`tools/video/media/camera-motion.mjs`），第二段不改鏡頭。

第三段：同樣三支 σ0.5 跑 7B fp16（`h3.sh upscale --model 7b`）：130–152 秒一支（第一支含下載 316 秒），3 支 1.30 CU，時間只比 3B 多 5–10%。皮膚的毛孔與顆粒明顯比 3B 少、柵欄與石頭細節相當，對國漫比較合適；預設仍是 3B，等站主看過再改。

## 六、還沒試的

- LBH-123-AI 的 latent upscaler（`MiniMaxH3LatentUpscaleWithModel`，程式註解寫 MIT，授權待確認）＋1 步 denoise 0.15，比十步便宜。
- Ref2VA 的加速 LoRA（Kijai DMAD 4 步、Pika 6 步）對照 `smooth` 8 步；只適用 Ref2VA，授權待查。
- 用 RunPod 跑同一套：notebook 的圖可直接搬到自己的 ComfyUI 映像（票 `2026-10-30-runpod-h3-image-and-runner`）。以 Colab 約 US$0.10／CU 換算，G4 約 US$0.8／小時，RunPod 上同一張卡站主看到的報價是 US$2.59／小時（換算是假設，未查方案帳單）。
