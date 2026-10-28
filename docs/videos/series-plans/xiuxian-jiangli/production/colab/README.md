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
- 1344×768、24 fps；4 秒會變 4.46 秒、5 秒變 5.17 秒；`assemble` 重編碼進 1080p，畫質沒驗。

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

# 3. 小樣：把 s33–s35 通過 judge 的關鍵影格放到 h3/first-frames/sNN.png，抄餘額，跑
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage
cd docs/videos/series-plans/xiuxian-jiangli/production/colab/h3 && bash ../../../../../../../.agents/skills/minimax-h3-colab/scripts/h3.sh batch \
  --manifest manifest-pilot.json \
  --output-dir <VIDEO_WORKDIR>/xiuxian-jiangli-e001/colab-out --progress <VIDEO_WORKDIR>/xiuxian-jiangli-e001/colab-out/progress.json --timeout 10800
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage

# 4. 站主看過小樣 → 其餘 39 支用 h3/manifest.json 同樣跑（一批共用一個 Colab session，不要一鏡開一次）

# 5. 進產線（每支一筆；CU 換美元的算法寫進 --note）
node tools/video/cli.mjs clips import --slug xiuxian-jiangli-e001 --shot s33 --file <…>/s33-t1.mp4 \
  --provider external --credits <CU> --usd <美元> --note "route=colab-h3 mode=first_frame session=<name> seed=<n> req_s=4 cu=<n>"
```

## 小樣看什麼（三鏡 s33 銅閥噴氣、s34 掀鍋蓋說「好了？」、s35 木勺舀飯金色光點）

身份跟設定圖同一張臉；三個動作各做完；s34 嘴有動；s33 → s34 蒸汽量連得上；第 0 格對關鍵影格的 PSNR；一支實際扣幾 CU、冷啟動幾分鐘。Colab 的 Turbo LoRA 版 H3 不是海螺的 H3，一致性要自己驗。失敗條件：兩個 take 都壞在手與道具、蒸汽畫成火、金色光點畫成文字、嘴不動。

## 這條路線自己的風險

1. 開源 Turbo LoRA 版的畫質與一致性沒有本 repo 的實測；小樣就是在量這件事。
2. `colab new`／`exec` 在這個雲端容器經代理走 WebSocket 還沒試過（cloud-pairing.md §4）；卡住先看 `~/.config/colab-cli/colab.log`。
3. 輸出 1344×768，不是 1080p；放大畫質沒驗。
4. Google 帳號的 token 帶 `cloud-platform` scope，而且會交給配對的雲端 session：後台登入的帳號要是沒有 GCP 專案與帳單、只有 Google AI Pro／Ultra 的帳號。
5. 配對前主機要先部署 #1896（migration 0142、`colab-credentials` 端點、`login --colab`）；沒部署就 `login --colab` 拿不到帶 Colab 旗標的權杖，`bootstrap.sh` 向站台要憑證會 403。

## 小樣結果（2026-10-28，第一次真跑）

| 項 | 實測 |
| --- | --- |
| session | `h3-20261028-060722-acfdb4`，A100 高 RAM，`colab new` 經代理成功 |
| 冷啟動 | 06:07 起、06:09 開始第一鏡：裝 ComfyUI 與抓模型（qwen3vl 14.6 GiB、H3 16 GiB 級、VAE、Turbo LoRA）約 2 分鐘（模型已在快取；第一次抓會更久） |
| 每支 4 秒（排程 107 幀＝4.46 秒） | s33 5 分 19 秒（含首鏡暖機）、s34 2 分 20 秒、s35 2 分 18 秒 |
| compute units | `h3.sh usage` 前 1000.00、後 999.31（**0.69 CU，3 支，session 停止後 1 分鐘讀的；Colab 的用量常延遲入帳，下一批前再抄一次**） |
| 第 0 格對關鍵影格 PSNR | s33 35.4 dB、s34 31.9 dB、s35 32.2 dB（首格 1376×768 被拉到 1344×768，runner 有提醒） |
| 畫面 | 三支動作都做完：閥門噴氣直上、掀蓋蒸氣撲出而兩人臉同設定圖、勺子把飯倒回鍋；蒸汽沒畫成火、金色光點沒變文字 |
| 沒驗 | s34 嘴型（要站主聽原音看）；`clips import` 還進不了：`timeline.json` 要 `tts` 先成功，Gemini 語音 01:50Z 起一直 429 |

輸出在 `<VIDEO_WORKDIR>/xiuxian-jiangli-e001/colab-out/`（`s33-t1_mp4_s33.mp4` 等三支，`progress.json` 有 seed）。上游 runner 把 `reference_images` 當成相對於**目前目錄**而不是 manifest，所以 `h3.sh batch` 要在 `h3/` 目錄裡跑（第一次在 repo 根目錄起跑就是這樣失敗的，沒花到點數）。
