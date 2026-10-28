# Colab 做出來的 H3 片段怎麼進產線

唯一的匯入程序在 `.agents/skills/animation-production/references/stage-preconditions.md` 最後一節（`clips import`）；這份只寫 Colab 這條路跟它對接的地方。

## 1. 先確認目的地收得進去

- `series.production.profile` 存在的作品，`clips import` 一律以 3 拒絕（`tools/video/media/clips.mjs` 的 `importClip`），而且 Colab 輸出最大 1344×768，本來就過不了 profile 的原生 1920×1080 要求。這條路**只給沒有 profile 的 pilot 與作品**；正片要用得等 `2026-10-04-profile-works-external-clip-route` 那張票。
- storyboard 要核准、這一鏡的關鍵影格要通過 judge；**首格就用那張關鍵影格**（`first_frame` 模式），不然匯入時第 0 格 PSNR 過不了、`needs_review`。
- 開拍鎖定包（`.agents/skills/animation-preproduction/SKILL.md`）要先有：每鏡秒數、定稿正文與 SHA-256；Colab 不是另一個可以不鎖就試的地方。

## 2. 每鏡的輸入

| 欄位 | 怎麼填 |
| --- | --- |
| `inference_mode` | 關鍵影格當首格 → `first_frame`（恰好一張圖，FL2VA；先用 `scripts/fit_first_frame.sh` 裁到畫布比例）；只有設定圖、沒有首格 → `reference`（1–9 張，Ref2VA，`<Picture N>` 照順序） |
| `prompt_file` | 鎖定包的定稿正文原封不動寫進 UTF-8 檔；runner 不改寫。H3 的首格正文照官方 I2VA 結構（`shot_plan.mjs --route hailuo --hailuo-model h3`；正文結構的差異在 `.agents/skills/animation-camera/references/model-misreads.md` 第六節與票 `2026-10-05-shot-plan-h3-body-official-i2va`），`[Shot 1]` 裡的寫法（風格詞、`<Picture 1>` 錨句、動作軌跡、一個運鏡、`holds a static shot`）照 `.agents/skills/minimax-h3-colab/references/motion-quality.md` 第二節；只寫 `[Shot 1]`，`[Shot 2]` 會切鏡 |
| `duration_seconds` | 鎖定包的 buy 秒數，**5–15**：4 秒＝107 幀低於 H3 訓練範圍 124–362 幀，`check_manifest.py` 會警告；H3 以 24 fps、幀數對齊 `17k+5`，所以 5 → 5.17 秒、6 → 6.58、8 → 8.00、12 → 12.25。畫面上有人說話或動作兩拍買 6，多的在剪接切 |
| `width`／`height` | 32 的倍數、面積不超過 1344×768。**首格鏡用 1312×736**（離 16:9 不到 0.005；1344×768 是 7:4，節點會把 16:9 的首格拉伸；1280×720 不是 32 的倍數）；只有設定圖的 reference 模式用 1344×768。不是 1080p，`assemble` 會重編碼進 30 fps 1080p 的時間軸，放大畫質沒驗 |
| `seed` | 省略時 runner 隨機；重做同一鏡要比較時固定它，寫進 `clips import --note` |
| `prompt_sha256` | 可選；鎖定檔的正文雜湊，`check_manifest.py` 對 prompt 檔算一次，不符就不上傳 |

音訊：H3 會生成同步音軌（AAC），產線丟棄；正文的 `overall_soundscape` 寫 `N/A`，跟 Hailuo 網頁路線一樣。

## 3. 收據與匯入

每支下載回來後，`progress.json` 有 session、seed、秒數與 bytes；再抄 `colab usage` 前後的 `Current balance` 差額當這一批的 CU。匯入：

```bash
node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <mp4> \
  --provider external --credits <CU 差額> --usd <CU 換算的美元> \
  --note "route=colab-h3 mode=first_frame profile=smooth session=<name> seed=<n> req_s=<n> cu=<n>" [--judge]
```

- provider 用 `external`（enum 沒有 colab；不偽標成 `hailuo-web`）。`--usd` 工具不代換：CU 換美元照站主那個方案的月費除以每月 CU 自己算，算法寫進 `--note`。
- `--judge` 才會問 judge（US$0.01 一次）並要站上的權杖；沒帶就完全不碰網站。
- 沒過（exit 1）就重做一支或 `--force`；點數已經花了，失敗的也照記。

## 4. 之後

照常 `music`、`assemble`；`status` 會列「imported: external N」，`run_report.mjs` 把匯入的跟買的分開。`clips --force` 會把匯入的那鏡重買，要重做別的鏡用 `--shot`。
