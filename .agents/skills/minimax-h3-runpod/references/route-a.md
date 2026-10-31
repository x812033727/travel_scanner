# 路線 A 在 RunPod 上（2026-10-31 實測）

站主的標準：**除了 GPU 伺服器，品質和流程都要和 Colab 一樣；一樣就繼續，不一樣就找原因。** 寫法、審片與重抽的規則不在這裡重寫，照 `.agents/skills/minimax-h3-colab/references/lessons.md` 第 2、6 節與 `.agents/skills/minimax-h3-colab/references/three-stage.md`。

## 一、和 Colab 的對照

《種田》e033 s08、s21，同 seed 330000、同參考圖，第一段與第二段正文的 SHA-256 都與 Colab 當時送出的相同，Colab 原始檔在分支 `transfer/zt-e033-parity`。

| 階段 | 構圖、動作、臉 | SSIM（s08／s21） |
| --- | --- | --- |
| 第一段 960×544 hero | 一致 | 0.835／0.910 |
| 第二段 1312×736 | 一致 | 0.830／0.903 |
| 第三段 1920×1080 | 一致 | 0.802／0.880 |

位元不會相同：Colab 是 Server 版 G4、PyTorch 2.11（第三段記錄）、當時最新的 ComfyUI、SeedVR2 命令列；這裡是 WK、PyTorch 2.9.1、釘住的 ComfyUI、SeedVR2 節點。背景細節與表情有些微差異，判斷只看過兩鏡的抽格。

## 二、實測時間與費用（WK，US$2.59／小時）

| 項目 | 時間 |
| --- | --- |
| 第一次下載全部模型（112.4 GiB） | 約 19 分鐘（FP8 那組）；之後開機不重下 |
| 開機到可送工作 | 約 1–5 分鐘 |
| 第一段，第一支（含載入） | 238–284 秒 |
| 第一段，暖機 | e040 前 14 支平均 124 秒；7 張參考圖 160 秒 |
| 第二段（含載入／之後） | 223–255 秒／s21 192 秒 |
| 第三段 7B（含載入／之後） | 198–225 秒；暖機未單獨量 |

三段一支約 US$0.3–0.4（估算）。兩鏡三段一個 Pod 實付 US$0.99。同一張卡 Colab 約 US$0.8／小時（換算，未查帳單），RunPod 約貴 3 倍；好處是模型留在 volume、站台代開代停。

## 三、踩過的坑

| 症狀 | 原因 | 怎麼辦 |
| --- | --- | --- |
| 每步 31.65 秒、一支 11 分鐘、GPU 滿載 | 映像用 CUDA 12.8＋FP8；Colab 是 CUDA 13＋INT8 | 已改成相同的組合，**不要自行換權重**；要換先和 Colab 對照 |
| Pod 回報就緒，下一個上傳卻 404 且無內容 | 新 Pod 的 RunPod 代理還不穩（由症狀推斷） | runner 已要求連續三次就緒並重試 |
| 覺得風格和舊集不同 | 拿第一次抽的原始片段比調色、挑片後的成片；那鏡又是清晨群戲 | **同鏡同 seed 比原始檔**再下結論；原始片段未經 `assemble-v4.mjs` 的調色與暗角 |
| 人物赤腳 | 定妝照看不到腳，或別人的定妝照是赤腳 | 第一段重抽，後兩段救不回來 |
| Windows 上 `ref2manifest.mjs` 沒有輸出 | 它的 main 判斷只在 Linux 成立 | 從 Linux 跑 |
| 同時開第二個 Pod 被拒 | 站台一次只准一個 | 等前一批結束 |
| Pod 終止後讀不到記錄 | 記錄隨 Pod 消失 | 每步秒數要趁跑的時候從 RunPod 主控台看 |

## 四、整集做法

```bash
bash .agents/skills/minimax-h3-runpod/scripts/route_a_st1.sh 40 400000   # 草稿；先給站主估價
# 審草稿、重抽有問題的鏡；不做的鏡寫進 st2/skip.txt
bash .agents/skills/minimax-h3-runpod/scripts/route_a_st23.sh 40 400000 s08:400001   # 第二、三段，重抽過的鏡寫它的 seed
```

輸出在 `VIDEO_WORKDIR` 底下的 `zhong-tian-qu-qi-eNNN-dh/runpod/a/`；第三段的檔名是 `<id>_1080.mp4`。這兩支都會花錢，先請站主點頭。

**雲端 session 從這條路跑還沒驗過**：要有 `MOKAAIR_VIDEO_TOKEN`，環境要連得到 `mokaair.com` 與 `*.proxy.runpod.net`，整集要用 `setsid nohup` 脫離（背景指令上限 2 小時，`lessons.md` 第 4 節）。兩支腳本也還沒照原樣跑完過整集，本機是用相同步驟的工作目錄腳本跑的。片段匯入產線是票 `2026-10-30-runpod-canvas-and-import`。
