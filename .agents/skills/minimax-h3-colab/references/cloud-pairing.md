# 雲端 session 與 Colab 的權杖配對

這份管「誰拿著 Google 的權杖、放在哪、怎麼進到一個沒有瀏覽器的 shell」。製作本身在 `.agents/skills/minimax-h3-colab/SKILL.md`，片段進產線在 `.agents/skills/minimax-h3-colab/references/pipeline-handoff.md`。

## 1. 配對的機制（2026-10-27 讀 google-colab-cli 0.7.5 的 `auth.py`）

- `colab --auth=oauth2 <任何指令>` 第一次跑會印一個 `accounts.google.com/o/oauth2/auth?...` 的網址，然後在 stdin 等一個驗證碼。流程跟 `gcloud auth application-default login` 同一套：redirect 到 Google 自己的 `sdk.cloud.google.com/applicationdefaultauthcode.html` 頁面顯示驗證碼，人複製回來貼。**不需要本機瀏覽器、不開 localhost**，所以雲端容器也走得通。
- 換到的憑證寫在 `~/.config/colab-cli/token.json`（google-auth 的 `Credentials.to_json()`：`token`、`refresh_token`、`client_id`、`client_secret`、`scopes`、`expiry`）。之後每個指令自己用 `refresh_token` 換新的 access token 並改寫同一個檔；`refresh_token` 本身不變，所以**存一次就夠**。
- 要的 scope：`openid`、`userinfo.profile`、`userinfo.email`、**`cloud-platform`**、`colaboratory`、`drive.file`。`cloud-platform` 很寬（等於那個帳號在 GCP 能做的事）。用**沒有 GCP 專案與帳單、只有 Google AI Pro／Ultra 訂閱**的 Google 帳號配對，風險才只有 Colab 的 compute units。
- 撤銷：Google 帳號的「第三方存取」頁撤掉「Google Cloud SDK」，或刪掉 `token.json` 重新配對（舊的 refresh token 留在誰手上都失效）。

## 2. 三條路線，先選哪條

| 路線 | 誰拿著 Google 的權杖 | 什麼時候用 |
| --- | --- | --- |
| **C. 跟後台配對（建議）** | 主機：站主在 `/admin/ai-accounts` 的「Google Colab」區登入最多五個帳號、看每個帳號的 compute units、選預設帳號。雲端 session 用影片工具權杖（`node tools/video/cli.mjs login --colab`，站主在後台按允許）向站台要預設帳號（或 `COLAB_ACCOUNT_SLOT=a-e`）的 token.json。換帳號、撤銷都在後台做，session 什麼都不用改 | 正式的做法；多個 Google 帳號輪著用時只有這條管得住 |
| A. 在雲端 session 配 | session 自己（`pair.py`），之後存成 secret `COLAB_CLI_TOKEN_JSON` | 後台還沒部署這版、或只有一個帳號想快速試 |
| B. 在自己電腦配 | 站主電腦，再存成 secret | 不想把驗證碼貼進對話 |

`bootstrap.sh token` 照這個順序找：`COLAB_CLI_TOKEN_JSON`（A／B）→ 站台（C：`MOKAAIR_VIDEO_TOKEN` 或 `~/.mokaair/video-tool.json`，`MOKAAIR_SITE` 預設 https://mokaair.com）→ 已經在 `~/.config/colab-cli/token.json` 的。

**C 的一次設定**：

```bash
node tools/video/cli.mjs login --colab --name "Claude 雲端 session"   # 印驗證碼與後台連結
# 站主在後台「Azure 語音（影片旁白）」卡核對驗證碼；卡上會標「這台電腦也要求 Google Colab 帳號的憑證」，按允許
# 工具把 mkv_ 權杖存進 ~/.mokaair/video-tool.json（容器被回收就沒了：存成環境 secret MOKAAIR_VIDEO_TOKEN 才留得住）
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh            # token 這一步會向站台拿 token.json 並驗 colab usage
```

後台那邊：`/admin/ai-accounts`（AI 設定 → 訂閱帳號）多了「Google Colab」區，登入走同一種貼授權碼的流程，卡片直接顯示 `colab usage` 的餘額、每小時耗用與執行中的 runtime；站台每次交出憑證都寫一筆審計（`ai_account.colab_credentials_fetched`，記權杖開頭，不記憑證）。沒有 Colab 權限的影片工具權杖拿到 403 `video_tool_token_no_colab`：重新 `login --colab`，或站主在卡上建權杖時勾「可取得 Colab 帳號憑證」。主機端的安裝與信任邊界在 `ops/ai-accounts/README.md`。

## 2a. 路線 A／B：為什麼雲端 session 要「權杖配對」而不是每次登入

Claude Code 雲端 session 的容器每次新開都是乾淨的，`~/.config` 不會留下來；環境設定裡的 **setup script 讀不到環境的 secret**，所以還原權杖這一步要在 session 裡做（`bootstrap.sh token` 讀環境變數）。做法：

1. 配對一次（§3 的 A 或 B），拿到 `token.json`。
2. `python3 .agents/skills/minimax-h3-colab/scripts/pair.py export` 印一行 base64（內容就是 token.json）。
3. 站主把那一行存成雲端環境的 secret，名稱 **`COLAB_CLI_TOKEN_JSON`**（環境設定 → Edit → Network secrets 或環境變數那一區；新開的 session 才看得到）。原始 JSON 直接存也可以，`bootstrap.sh token` 兩種都認。
4. 之後每個新 session 第一件事：`bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh`（裝 CLI、抓上游、寫 token、`colab usage` 驗一次）。驗不過會以 4 結束並說是沒配對還是網路。

權杖**不進 chat、不進 repo、不進 manifest 與 log**；`pair.py` 只有 `export` 會印它，而且是站主要才跑。要換帳號就重新配對再換 secret。

## 3. 路線 A 與 B 的配對步驟

**A. 在雲端 session 裡配（agent 跑，站主貼驗證碼）**

```bash
bash .agents/skills/minimax-h3-colab/scripts/bootstrap.sh install
python3 .agents/skills/minimax-h3-colab/scripts/pair.py start     # 印網址，背景等驗證碼（最多 30 分鐘）
# 站主開網址、登入擁有 Colab 方案的帳號、同意、複製驗證碼，回到對話貼給 agent
python3 .agents/skills/minimax-h3-colab/scripts/pair.py code '4/0A…'
python3 .agents/skills/minimax-h3-colab/scripts/pair.py export      # 站主存成 COLAB_CLI_TOKEN_JSON
```

驗證碼只有一次有效、幾分鐘內要貼；`pair.py` 把它寫進 state 目錄幾秒鐘後就刪。容器被回收時背景程序也沒了，`pair.py status` 會說 `not_paired`，重跑 `start` 就是新的一組網址。

**B. 在自己的電腦配（站主自己跑，再把 token 交給環境）**

```bash
uv tool install --python 3.12 google-colab-cli
colab --auth=oauth2 usage        # 照終端機的網址／驗證碼走完
python3 /path/to/repo/.agents/skills/minimax-h3-colab/scripts/pair.py export
```

Windows 要在 WSL 裡（CLI 只支援 Linux／macOS）。B 不經過 agent，適合不想把驗證碼貼進對話的人。

## 4. 這個容器查過的事（2026-10-27）

| 查什麼 | 結果 |
| --- | --- |
| `uv tool install google-colab-cli` 經代理裝 0.7.5 | 可以（系統 Python 3.13 直接用；低於 3.12 時 bootstrap 用 `--python 3.12`） |
| `colab --auth=oauth2 usage` 無瀏覽器 | 印出授權網址並等 stdin；stdin 關掉就印 `EOF` 警告、exit 0（所以 `bootstrap.sh verify` 看的是輸出有沒有 `Current balance`，不是 exit code） |
| 代理放不放 Google | `colab.research.google.com` 200、`accounts.google.com` 302、`oauth2.googleapis.com` 可達 |
| `colab new`／`exec`／`upload`（走 WebSocket 到 runtime） | **沒試**（要花 compute units、要先配對）。第一次真跑如果卡在 `new` 或 `exec`，先懷疑代理對 WebSocket 的處理，看 `~/.config/colab-cli/colab.log` 與 `--logtostderr` |
| 上游 runner 需要的旗標（`new --gpu/--high-mem`、`exec --env/--file/--timeout`、`upload`、`download`、`stop`） | 0.7.5 都有 |

## 5. 配額與價格：只記來源，不當實測

- **站主的方案是 Colab Pro+**（2026-10-28 站主說的），登在後台「Google Colab」槽位 A 當預設帳號。Pro+ 是 `--high-mem` 的前提（Colab CLI 註明要 Pro 或 Pro+），也有背景執行，所以 `h3.sh` 預設的 `--gpu A100 --high-mem` 照用。每月點數網路上說法不一（500 或 600），A100 每小時扣 13–15 點也不一致，GPU 配不配得到不保證：**以後台卡片的 `colab usage` 餘額為準**，第一批跑完把前後差額寫進票。

- Google AI Pro 每月含 200 compute units、Ultra 另有 Premium GPU 與背景執行；一支 12 秒約 1 CU：這是 kocpc 2026-10 文章與作者 Threads 帖的說法，**本 repo 沒量過**。A100 高 RAM 每小時扣幾 CU 以 `colab usage` 印的 `Usage rate` 為準，第一次跑時抄進收據。
- 第一次在同一個 session 要裝 ComfyUI、從 Hugging Face 抓 `Comfy-Org/MiniMax-H3` 的模型（notebook 說至少 60 GiB 磁碟，Ref2VA 的 BF16 備援 80 GiB）：冷啟動幾分鐘到更久，所以**一批放同一個 manifest 共用 session**，不要一鏡開一次。
- 它是 ComfyUI 跑的 **Turbo LoRA 版 H3**（Ref2VA 用官方 4-step LoRA；first_frame 用社群 `drbaph` 的 v4 Turbo LoRA），不是 MiniMax API 或 Hailuo 網頁的 H3：畫質與一致性要自己小樣，不沿用 `providers-and-plans.md` 的 Hailuo 實測。

## 6. 上游怎麼釘、怎麼升

上游 `killkli/minimax-h3-colab-skill` 沒有授權檔，所以不複製進 repo；`bootstrap.sh` 用 `MINIMAX_H3_UPSTREAM_COMMIT` 釘 commit clone 到 `MINIMAX_H3_COLAB_HOME`。要升版：先 `h3.sh test` 跑上游的離線測試、對照 `README.zh-TW.md` 的變更，改 `bootstrap.sh` 裡的 commit，再跑本 repo 的 `tools/minimax-h3-colab.test.mjs`。上游的 `install.sh` 只是把檔案複製到 `~/.codex/skills`；Codex 要用同一條路時照樣可以跑它，runner 與 notebook 是同一份。
