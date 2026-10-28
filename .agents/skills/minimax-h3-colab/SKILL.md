---
name: minimax-h3-colab
description: 用 Google Colab 的 GPU 跑 MiniMax H3（ComfyUI Turbo LoRA 版）做首格或多參照圖的短片段，從 Claude Code 雲端 session、Codex 或任何沒有瀏覽器的 shell 驅動：Colab CLI 的 OAuth2 權杖配對一次、存成環境 secret COLAB_CLI_TOKEN_JSON，每個新 session 用 bootstrap 還原；上游 killkli/minimax-h3-colab-skill 釘 commit 取用、不複製，取樣設定由 patch 套成 8 步 LoRA 的 smooth／hero／draft 三種 profile；送出前 check 擋掉會花錢的錯；片段用 clips import 進產線。另有 H3 動作流暢度手冊（貼圖感的來源、正文的軌跡寫法、≥5 秒、1312×736 畫布、錯誤目錄），Hailuo 網頁與 API 的 H3 也照它寫。要在 Colab 上生 H3 片段、配對或換 Colab 帳號、查 compute units、寫 manifest 批次跑、把 Colab 片段匯進某一集、或 H3 片段僵硬像貼圖要改寫法時，先讀這個 skill。Drive MiniMax H3 video generation on Google Colab from a browserless Claude Code cloud session with a paired, secret-stored Colab CLI token, 8-step sampling profiles and a motion-quality manual.
metadata:
  short-description: Colab 上的 MiniMax H3：權杖配對、bootstrap、取樣 profile、批次、匯入、流暢度
---

# MiniMax H3 on Colab（minimax-h3-colab）

kocpc 2026-10 介紹的做法是 Codex 裝 `killkli/minimax-h3-colab-skill`，在本機用 Colab CLI 把圖片與 prompt 丟上 Colab 的 GPU 跑 H3，再把 MP4 抓回來。這個 skill 把同一條路搬到**沒有瀏覽器、每次都是乾淨容器**的 Claude Code 雲端 session：runner 與 notebook 還是上游那份（釘 commit），差別在權杖怎麼進來、每個 session 怎麼開機、取樣設定怎麼套、送出前怎麼檔錯，以及片段怎麼進本 repo 的產線。Codex 用同一份：上游的 `install.sh` 只是把檔案複製到 `~/.codex/skills`，可以照跑。

| 要做什麼 | 讀哪裡 |
| --- | --- |
| 三條配對路線（跟後台配對、session 自己配、自己電腦配）、權杖在哪、這個容器查過什麼、配額與價格的來源、上游怎麼釘 | `.agents/skills/minimax-h3-colab/references/cloud-pairing.md` |
| **片段僵硬、像貼圖、不流暢**：原因、正文的軌跡寫法、秒數與畫布、三個取樣 profile、錯誤目錄、收工看什麼 | `.agents/skills/minimax-h3-colab/references/motion-quality.md` |
| 後台「Google Colab」區與主機 agent 的安裝、信任邊界 | `ops/ai-accounts/README.md` |
| 片段進產線：哪些作品收得進、每鏡的 manifest 欄位、收據與 `clips import` 的寫法 | `.agents/skills/minimax-h3-colab/references/pipeline-handoff.md` |
| 匯入程序本身（唯一的一份） | `.agents/skills/animation-production/references/stage-preconditions.md` 最後一節 |
| 開拍前的鎖定包、每鏡秒數與定稿正文 | `.agents/skills/animation-preproduction/SKILL.md` |
| H3 正文的官方外框、模型會誤讀什麼 | `.agents/skills/animation-camera/references/model-misreads.md` 第六節 |

## 不變的規矩

1. **先配對，再談生成。** `bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh` 是每個新 session 的第一步：裝 CLI（0.7.5）、抓上游（釘 commit）、套取樣 profile、拿到 `~/.config/colab-cli/token.json`、`colab usage` 驗一次。token 的來源照順序：secret `COLAB_CLI_TOKEN_JSON`，不然就**向站台要**（建議：站主在 `/admin/ai-accounts` 的「Google Colab」區登入帳號，session 用 `node tools/video/cli.mjs login --colab` 配對過的影片工具權杖取預設帳號的憑證；cloud-pairing.md §2）。以 4 結束就是沒配對或網路不通，不要自己想辦法繞。
2. **權杖不進 chat、repo、manifest、log。** 只有站主要存 secret 時才跑 `pair.py export`，印出來那一行是 Google refresh token，當密碼看。那個權杖帶 `cloud-platform` scope：**用沒有 GCP 專案與帳單的 Google 帳號配對**（cloud-pairing.md §1）。
3. **花 compute units 之前站主要點頭。** 每一批先 `h3.sh usage` 抄餘額，批完再抄一次；冷啟動要裝 ComfyUI 與抓模型，所以一批放同一個 manifest 共用 session，不要一鏡開一次。GPU 配不到（方案、餘額、A100 沒貨）就如實回報，試 `--no-high-mem` 或換 GPU 前先問。
4. **目的地先查**：有 `series.production.profile` 的作品 `clips import` 以 3 拒絕，Colab 輸出最大 1344×768 也過不了原生 1080p 的檢查。這條路給沒有 profile 的 pilot 與作品（pipeline-handoff.md §1）。
5. **首格用通過 judge 的關鍵影格**（`first_frame` 模式），16:9 的首格用 **1312×736** 畫布（1344×768 會拉伸；`fit_first_frame.sh` 裁比例）；**買 ≥5 秒**（4 秒＝107 幀低於訓練下限，說話鏡 6 秒）；正文用鎖定包的定稿、原封不動放進 prompt 檔，寫法照 motion-quality.md 第二節（風格詞＋`<Picture 1>` 錨句、動作軌跡、一個運鏡、`holds a static shot`）；runner 與 notebook 不改寫 prompt。
6. **送出前 `h3.sh check --manifest`**（`batch` 會自己先跑）：32 的倍數、`<Picture N>`、首格比例、秒數、`prompt_sha256` 對鎖定檔；有錯就不上傳。
7. **取樣 profile 預設 `smooth`**（Ref2VA 換 8 步 LoRA）；顏值與身份鏡用 `H3_PROFILE=hero`（20 步、不掛 LoRA）另開一批；只看構圖才 `draft`。profile、seed、秒數寫進收據。
8. **逾時不要盲目重試**：`colab exec` 逾時時遠端 kernel 可能還在跑，runner 會停掉自己開的 session 並把做完的記進 `progress.json`；重跑會重扣。

## 一次完整的流程

```bash
# 0. 開機（每個新 session）；沒 secret 時會說要先配對；H3_PROFILE=hero 換 profile（預設 smooth）
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh

# 1. 第一次配對。建議走後台（帳號由站主在 /admin/ai-accounts 管）：
node tools/video/cli.mjs login --colab --name "Claude 雲端 session"  # 印驗證碼，站主在後台按允許
#    之後每個 session 要有 MOKAAIR_VIDEO_TOKEN（環境 secret），bootstrap 的 token 步驟就會向站台拿
#    另一條：session 自己配對再存成 COLAB_CLI_TOKEN_JSON（cloud-pairing.md §3）
python3 .agents/skills/minimax-h3-colab/scripts/pair.py start      # 印網址，背景等驗證碼
python3 .agents/skills/minimax-h3-colab/scripts/pair.py code '4/…'  # 站主貼回來的驗證碼
python3 .agents/skills/minimax-h3-colab/scripts/pair.py export      # 站主存成環境 secret

# 2. 餘額（免費，也證明配對有效）
bash .agents/skills/minimax-h3-colab/scripts/h3.sh usage

# 3. 首格裁到畫布比例（16:9 關鍵影格 → 1312×736），再檢查 manifest（免費）
bash .agents/skills/minimax-h3-colab/scripts/fit_first_frame.sh <關鍵影格.png> <first-frames/s01.png>
bash .agents/skills/minimax-h3-colab/scripts/h3.sh check --manifest <jobs.json>

# 4. 一支（首格 = 關鍵影格；first_frame 沒給尺寸就是 1312×736）
H3_DURATION_SECONDS=5 bash .agents/skills/minimax-h3-colab/scripts/h3.sh single \
  --mode first_frame --image <first-frames/s01.png> --prompt <正文.txt> --output <out.mp4>

# 5. 一批（共用一個 Colab session；先跑 check，有錯就停）
bash .agents/skills/minimax-h3-colab/scripts/h3.sh batch --manifest <jobs.json> \
  --output-dir <outputs/> --progress <outputs/progress.json> --timeout 10800

# 6. 進產線
node tools/video/cli.mjs clips import --slug <SLUG> --shot <id> --file <out.mp4> \
  --provider external --credits <CU> --usd <美元> --note "route=colab-h3 profile=smooth seed=<n> …"
```

manifest 的形狀（`jobs[]`：`id`、`title`、`inference_mode`、`reference_images`、`prompt_file` 或 `prompt`、`duration_seconds` 5–15（4 會警告）、`width`／`height` 32 的倍數且面積 ≤ 1344×768（首格鏡 1312×736）、`seed`、`output_name`、可選 `prompt_sha256`）照上游 `README.zh-TW.md`，欄位對產線的意義在 pipeline-handoff.md §2。`h3.sh` 的其他參數原樣交給上游的 `runner.py`：`--gpu`（預設 A100）、`--no-high-mem`、`--session NAME --stop-on-complete`、`start`／`stop`、`batch --no-check`。

## 收工要留下的

- 這一批的 `progress.json`（session、每鏡 seed、秒數、bytes、失敗原因）、套的 profile、`colab usage` 前後的餘額差；CU 換美元的算法寫進 `clips import --note`。
- 第一次真跑要把 `cloud-pairing.md` §4「沒試」的格子改成結果：`colab new` 經代理成不成、A100 的 `Usage rate`、冷啟動幾分鐘、一支 5 秒實際扣幾 CU、`smooth` 與 `hero` 各多久。
- 看片照 motion-quality.md 第六節與 `.agents/skills/animation-production/references/browser-production.md` §3 的三鏡 pilot 標準：Colab 的 Turbo LoRA 版 H3 不是 Hailuo 網頁的 H3，一致性要自己驗。

## 離線驗證（不花錢、不碰權杖）

```bash
node --test tools/minimax-h3-colab.test.mjs        # pair.py、bootstrap.sh token/verify、h3.sh、patch_notebook.py、check_manifest.py，用假的 colab
bash .agents/skills/minimax-h3-colab/scripts/h3.sh test   # 上游 runner 的 unittest（要先 bootstrap.sh install）
python3 -I .agents/skills/minimax-h3-colab/scripts/patch_notebook.py --dry-run   # 對抓下來的上游 notebook 印 profile 的 diff
```
