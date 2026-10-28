# Colab 路線：第 1 集的片段在 Google Colab 的 GPU 上跑開源 MiniMax H3

站主 2026-10-28 定：**只用 Colab 的 GPU 跑開源 H3**（PR #1894 的 skill `minimax-h3-colab`），不走海螺網頁、不走站上伺服器的片段模型、也不在 Colab 打 MiniMax 付費 API。首格與設定圖用產線自己的 `look` 與 `keyframes`（站上的 Gemini 圖，有 judge），因為 `clips import` 要用通過 judge 的關鍵影格當首格才過第 0 格 PSNR。

## 分工

| 階段 | 在哪裡做 | 花什麼 |
| --- | --- | --- |
| 設定圖 `look`（4 角色 × 2 候選） | 站上產線 | 約 US$1.07（上限 2.14） |
| 關鍵影格 `keyframes`（45 張，含 judge） | 站上產線 | 約 US$6.03（上限 18.09） |
| 片段 42 支 | **Colab GPU，開源 H3 Turbo LoRA 版** | compute units（Google AI Pro 每月 200 CU；一支 12 秒約 1 CU，kocpc 的說法，本 repo 沒量過） |
| 配音、音樂、剪接 | 站上產線 `tts` → `music` → `assemble` | 配音額度、音樂 US$0.08 |

## 檔

- `h3/manifest-pilot.json`：小樣三支 s33、s34、s35。
- `h3/manifest.json`：整集 42 支（靜圖 s10、s19、s31 不買）。
- `h3/prompts/<id>.txt`：鎖定檔（`../e001-plan-lock.json`）的 H3 定稿正文原封不動；每個 job 的 `prompt_sha256` 等於鎖定檔。
- `reference_images` 指 `first-frames/<id>.png`（相對於 manifest 所在目錄，不進 git）：跑之前把通過 judge 的關鍵影格複製成這個名字。
- 1312×736、24 fps、每支至少 5 秒（＝124 幀＝5.17 秒；s06 本來就是 5 秒）。2026-10-28 從 4 秒、1344×768 改過來：4 秒只有 107 幀，低於 H3 訓練範圍 124–362 幀；1344×768 是 7:4，節點會把 16:9 的首格拉伸，1312×736 離 16:9 不到 0.005（`.agents/skills/minimax-h3-colab/references/motion-quality.md` 第三節）。`assemble` 重編碼進 1080p，畫質沒驗。

## 流程（照 `.agents/skills/minimax-h3-colab/SKILL.md`，只在這裡寫本集的路徑）

```bash
# 0. 每個新 session：裝 CLI、抓上游、向站台拿 Colab 憑證（MOKAAIR_VIDEO_TOKEN）、驗一次
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh

# 1. 配對走 PR #1896 的「跟後台配對」（站主 2026-10-28 定），不用 pair.py 的 OAuth：
#    主機部署 #1896 後，站主在 /admin/ai-accounts 的「Google Colab」區登入 Google 帳號（用沒有 GCP 專案與帳單的帳號）
node tools/video/cli.mjs login --colab --name "Claude 雲端 session"   # 印驗證碼與後台連結，站主在卡上允許
#    工具把 mkv_ 權杖存進 ~/.mokaair/video-tool.json；站主存成環境 secret MOKAAIR_VIDEO_TOKEN 才留得住；COLAB_ACCOUNT_SLOT 選帳號 a–e

# 2. 站上產線先出設定圖與關鍵影格（要站主過 look 與 storyboard 關卡）
node tools/video/cli.mjs look --slug xiuxian-jiangli-e001 --dry-run && node tools/video/cli.mjs look --slug xiuxian-jiangli-e001
node tools/video/cli.mjs keyframes --slug xiuxian-jiangli-e001 --dry-run && node tools/video/cli.mjs keyframes --slug xiuxian-jiangli-e001

# 3. 小樣：把 s33–s35 通過 judge 的關鍵影格裁成畫布比例放到 h3/first-frames/sNN.png，檢查 manifest，抄餘額，跑
bash .agents/skills/minimax-h3-colab/scripts/fit_first_frame.sh <關鍵影格.png> docs/videos/series-plans/xiuxian-jiangli/production/colab/h3/first-frames/s33.png   # 每鏡一次，預設 1312×736
bash .agents/skills/minimax-h3-colab/scripts/h3.sh check --manifest docs/videos/series-plans/xiuxian-jiangli/production/colab/h3/manifest-pilot.json
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage
bash .agents/skills/minimax-h3-colab/scripts/h3.sh batch \
  --manifest docs/videos/series-plans/xiuxian-jiangli/production/colab/h3/manifest-pilot.json \
  --output-dir <VIDEO_WORKDIR>/xiuxian-jiangli-e001/colab-out --progress <VIDEO_WORKDIR>/xiuxian-jiangli-e001/colab-out/progress.json --timeout 10800
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage

# 4. 站主看過小樣 → 其餘 39 支用 h3/manifest.json 同樣跑（一批共用一個 Colab session，不要一鏡開一次）

# 5. 進產線（每支一筆；CU 換美元的算法寫進 --note）
node tools/video/cli.mjs clips import --slug xiuxian-jiangli-e001 --shot s33 --file <…>/s33-t1.mp4 \
  --provider external --credits <CU> --usd <美元> --note "route=colab-h3 mode=first_frame profile=smooth session=<name> seed=<n> req_s=5 cu=<n>"
```

## 小樣看什麼（三鏡 s33 銅閥噴氣、s34 掀鍋蓋說「好了？」、s35 木勺舀飯金色光點）

身份跟設定圖同一張臉；三個動作各做完；s34 嘴有動；s33 → s34 蒸汽量連得上；第 0 格對關鍵影格的 PSNR；一支實際扣幾 CU、冷啟動幾分鐘。Colab 的 Turbo LoRA 版 H3 不是海螺的 H3，一致性要自己驗。失敗條件：兩個 take 都壞在手與道具、蒸汽畫成火、金色光點畫成文字、嘴不動。

## 這條路線自己的風險

1. 開源 Turbo LoRA 版的畫質與一致性沒有本 repo 的實測；小樣就是在量這件事。
2. `colab new`／`exec` 在這個雲端容器經代理走 WebSocket 還沒試過（cloud-pairing.md §4）；卡住先看 `~/.config/colab-cli/colab.log`。
3. 輸出 1312×736，不是 1080p；放大畫質沒驗。
4. Google 帳號的 token 帶 `cloud-platform` scope，而且會交給配對的雲端 session：後台登入的帳號要是沒有 GCP 專案與帳單、只有 Google AI Pro／Ultra 的帳號。
5. 配對前主機要先部署 #1896（migration 0142、`colab-credentials` 端點、`login --colab`）；沒部署就 `login --colab` 拿不到帶 Colab 旗標的權杖，`bootstrap.sh` 向站台要憑證會 403。
