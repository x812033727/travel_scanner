# Colab 路線：第 1 集的片段在 Google Colab 的 GPU 上跑開源 MiniMax H3

站主 2026-10-28 定：這部跟《修仙獎勵》同一條——**只用 Colab 的 GPU 跑開源 H3**（skill `minimax-h3-colab`），不走海螺網頁、不走站上伺服器的片段模型、也不在 Colab 打 MiniMax 付費 API。首格與設定圖用產線自己的 `look` 與 `keyframes`（站上的 Gemini 圖，有 judge），因為 `clips import` 要用通過 judge 的關鍵影格當首格才過第 0 格 PSNR。做法、配對、風險全照 `docs/videos/series-plans/xiuxian-jiangli/production/colab/README.md`，這裡只寫本集的路徑與數字。

## 分工

| 階段 | 在哪裡做 | 花什麼 |
| --- | --- | --- |
| 設定圖 `look`（7 角色 × 2 候選，含三十二歲的 zhouye32） | 站上產線 | 約 US$1.1（上限 2.1） |
| 關鍵影格 `keyframes`（42 張，含 judge） | 站上產線 | 約 US$5.6（上限 16.9） |
| 片段 39 支 | **Colab GPU，開源 H3 Turbo LoRA 版** | compute units（推算 15–20 CU；一支 12 秒約 1 CU 是 kocpc 的說法，本 repo 沒量過） |
| 配音、音樂、剪接 | 站上產線 `tts` → `music` → `assemble` | 配音額度、音樂 US$0.08 |

## 檔

- `h3/manifest-pilot.json`：小樣三支 s29、s30、s31。
- `h3/manifest.json`：整集 39 支（靜圖 s12、s18、s25 不買）。
- `h3/prompts/<id>.txt`：鎖定檔（`../e001-plan-lock.json`）的 H3 定稿正文原封不動；每個 job 的 `prompt_sha256` 等於鎖定檔。
- `reference_images` 指 `first-frames/<id>.png`（相對於 manifest 所在目錄，不進 git）：跑之前把通過 judge 的關鍵影格複製成這個名字。
- 1344×768、24 fps；4 秒會變 4.46 秒、5 秒變 5.17 秒（s15 買 5 秒）；`assemble` 重編碼進 1080p，畫質沒驗。

## 流程

```bash
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh                       # 每個新 session
node tools/video/cli.mjs look --slug ershou-chongsheng-e001 --dry-run && node tools/video/cli.mjs look --slug ershou-chongsheng-e001
node tools/video/cli.mjs keyframes --slug ershou-chongsheng-e001 --dry-run && node tools/video/cli.mjs keyframes --slug ershou-chongsheng-e001
# 小樣：把 s29–s31 通過 judge 的關鍵影格放到 h3/first-frames/sNN.png，抄餘額，跑
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage
bash .agents/skills/minimax-h3-colab/scripts/h3.sh batch \
  --manifest docs/videos/series-plans/ershou-chongsheng/production/colab/h3/manifest-pilot.json \
  --output-dir <VIDEO_WORKDIR>/ershou-chongsheng-e001/colab-out --progress <VIDEO_WORKDIR>/ershou-chongsheng-e001/colab-out/progress.json --timeout 10800
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage
# 站主看過小樣 → 其餘 36 支用 h3/manifest.json 同樣跑（一批共用一個 Colab session）
node tools/video/cli.mjs clips import --slug ershou-chongsheng-e001 --shot s29 --file <…>/s29-t1.mp4 \
  --provider external --credits <CU> --usd <美元> --note "route=colab-h3 mode=first_frame session=<name> seed=<n> req_s=4 cu=<n>"
```

## 小樣看什麼（s29 車底滑出、s30 滑走合約夾「這合約，我留著」、s31 抬眼一邊嘴角先笑）

身份跟設定圖同一張臉（林晚秋、老柯、王經理）；三個動作各做完；s30 嘴有動、夾子只有一本；s29 → s30 她站的位置連得上；第 0 格對關鍵影格的 PSNR；一支實際扣幾 CU、冷啟動幾分鐘。失敗條件：兩個 take 都壞在手與道具、嘴不動、三人全景裡任何一張臉走樣。

## 這條路線自己的風險

跟《修仙》第 1 集一樣四條：開源 Turbo LoRA 版的畫質與一致性沒實測；雲端容器經代理走 Colab 的 WebSocket 沒試過；輸出 1344×768 不是 1080p；配對帳號要是沒有 GCP 專案與帳單的帳號。兩部若同時開拍，Colab 的 compute units 是同一個池，先做哪一部的小樣要站主排。
