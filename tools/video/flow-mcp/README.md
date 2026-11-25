# Mokaair Google Flow 本機 MCP（訂閱帳號版 · 路線 A）

專為《原來如此事務所》（`sothatswhy`）、《奇聞檔案局》（`curio`）與零台詞 Shorts 打造的本機 Google Flow MCP Server 與 CLI。

- **直接吃 Google AI Plus / Pro / Ultra 訂閱帳號的 Flow 點數**（免另付按次計費 API Key）。
- **路線 A 雙層解耦**：上層由本目錄純 Node.js 22 ESM 把關 6 道 Mokaair 製作防雷關卡，底層透過 `FlowDriver` 介面委派給高頻維護的 [`gflow-cli`](https://github.com/ffroliva/gflow-cli)，免自行追 Google Flow 網頁改版。
- **Route B 嚴格零外洩**：所有靜圖、片段、QA 表與帳本一律只寫入 `.gitignore` 的 `work/video-episodes/<slug>/`，**0 GitHub Commit**，完片後直接 `npm run vdrive -- push-episode` 上傳雲端硬碟。

---

## 一、Windows 本機首次安裝（只要做一次）

> **注意**：請將 `travel_scanner` 放在 **非 OneDrive 同步** 的本機資料夾（例如 `C:\dev\travel_scanner`），避免 OneDrive 雲端佔位檔或權限鎖定影響 Chrome Profile 與 MCP 啟動。

### 快速一鍵安裝（推薦）

在 `travel_scanner` 根目錄開啟 Windows PowerShell，直接跑內建腳本即可自動檢查／安裝 `uv` + `gflow-cli`、拉取雲端角色設定圖，並寫入各客戶端 MCP 設定（覆寫前自動備份 `.bak`）：

```powershell
powershell -ExecutionPolicy Bypass -File tools\video\flow-mcp\install-windows.ps1 -WriteSetup
```

若想手動逐步安裝，請照下方步驟操作：

### 1. 確認必備工具（Node.js 22+、Chrome、FFmpeg、uv、gflow-cli）

在 Windows PowerShell 依序執行：

```powershell
# 1) 安裝 uv（Python 工具管理器，若尚未安裝）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2) 安裝 gflow-cli（底層 Google Flow 驅動）
uv tool install gflow-cli

# 3) 安裝 FFmpeg（供本機 720p -> 1080p30 bt709 升頻與 4 格 QA 表使用，若尚未安裝）
winget install Gyan.FFmpeg

# 4) 拉取雲端最新規則與鎖定角色設定圖（ada-canon-v2.png / chief & kid canon）
npm run vdrive -- pull-rules explainer

# 5) 檢查本機環境是否全綠
npm run flow -- doctor
```

### 2. 手動登入 Google Flow（獨立 Chrome Profile，絕不碰日常 Chrome 與密碼）

```powershell
npm run flow -- login
```

這會開啟一個獨立的 Chrome 視窗，請**親自手動登入你的 Google AI 訂閱帳號**並進入 `flow.google.com`。完成後驗證狀態與點數餘額（0 點數）：

```powershell
npm run flow -- status
```

### 3. 一鍵寫入 MCP 設定（Claude Desktop / Codex / Antigravity / Claude Code）

先預覽將產生的設定檔與路徑：

```powershell
npm run flow -- setup
```

確認路徑正確後，直接加上 `--write` 自動合併寫入（覆寫前會自動備份 `.bak`）：

```powershell
npm run flow -- setup --write
```

- **Antigravity**：自動寫入 `%USERPROFILE%\.gemini\antigravity\mcp_config.json`
- **Codex**：自動寫入 `%USERPROFILE%\.codex\config.toml`
- **Claude Desktop**：自動寫入 `%APPDATA%\Claude\claude_desktop_config.json`
- **Claude Code**：複製 `setup` 輸出的 `claude mcp add --scope user mokaair-flow ...` 指令貼到終端機執行即可。

重啟對應客戶端後，直接對 Agent 說：「**幫我檢查 Flow 狀態與剩餘點數**」，Agent 會呼叫 `flow_status` 回報方案與餘額。

---

## 二、內建 6 道 Mokaair 防雷硬關卡

1. **雙專案嚴格隔離**：`flow_init_episode` 綁定兩個獨立 Flow Project（`characterProjectId` 只放鎖定角色設定圖；`sceneryProjectId` 零角色參考圖）。若 `scenery` 鏡頭夾帶角色參考圖，程式直接擋下。
2. **全軸安全詞前置深掃**：`flow_preflight_shotlist` 在開 Chrome 前就攔截未成年詞（`child / girl / boy / 8-year-old / schoolgirl ...`）、血腥暴力詞、版權 IP 與 Flow 過濾詞，並給出中性改寫建議。
3. **16:9 靜默重置自動抓漏**：`Nano Banana 2.1` 下載後立刻以二進位檔頭驗像素；若 Flow 靜默重設回 `1:1`，自動隔離到 `stills/_rejected/` 並報 `aspect_drift_1_1`，絕不混進正片。
4. **0 點數先圖後片閘門**：每張靜圖／首尾格皆輸出互動網頁 `stills/qa-gallery.html`（Windows 檔案總管直接雙擊即可逐張看圖）；必須透過 `flow_approve_stills` 簽核通過，才能解鎖付費生片。
5. **單集點數硬上限 ＋ 一次性 `confirm_token`**：`sothatswhy` 硬上限 **500 點**、`curio` 軟上限 **550 點／硬上限 600 點**。呼叫付費 `flow_generate_clips` 前，必先跑 0 點數 `flow_plan_clips` 產生綁定鏡頭與金額的單次 `confirm_token`，經站主確認後才放行。
6. **免費 720p 原檔下載 → 本機自動升頻 `1080p30`**：鎖死下載 0 額外點數的 720p，再用本機 FFmpeg Lanczos 升 `1920×1080 @ 30fps`、`bt709`、`video_full_range_flag=0`（防後期壓浮水印色域重建消失）、`-an` 抽離模型原聲，自動產出 4 格 QA 表 `flow-clips/qa4/*-qa4.jpg`、`flow-clips/qa-gallery.html` 與含 SHA-256 的 `flow-clips/manifest.json`。

---

## 三、單集標準作業流程（搭配 10 個 MCP 工具）

在 `work/video-episodes/<slug>/flow-shot-list.json` 放好分鏡表，範例格式：

```json
{
  "series": "curio",
  "shots": [
    {
      "id": "s01",
      "chapter": "hook",
      "track": "character",
      "mode": "clip",
      "still_prompt": "3.5-head-ratio Ada holding an old brass compass in a dimly lit archive, theatrical gouache",
      "video_prompt": "Slow push-in as Ada tilts the brass compass toward warm desk lamplight, subtle dust motes"
    },
    {
      "id": "s02",
      "chapter": "hook",
      "track": "scenery",
      "mode": "still",
      "duration_sec": 6,
      "still_prompt": "18th-century nautical parchment map spread across dark oak table, candlelight, no text, theatrical gouache"
    }
  ]
}
```

接著由 Agent（或終端機）依序執行：

1. `flow_status` — 確認登入態、剩餘點數、無其他客戶端佔用 Chrome 鎖。
2. `flow_init_episode` — 初始化並綁定本集 `character` 與 `scenery` 雙專案。
3. `flow_preflight_shotlist` — 0 點數跑完安全詞、雙專案、留存紅線與點數預估。
4. `flow_generate_stills` → `flow_wait` — 0 點數用 `Nano Banana 2.1` 生完所有 `1376×768` 首尾格與靜圖。
5. 雙擊開啟 `work/video-episodes/<slug>/stills/qa-gallery.html` 肉眼檢查 → 呼叫 `flow_approve_stills` 核准通過鏡頭（退回的改稿後重跑）。
6. `flow_plan_clips` — 0 點數試算本批扣點（12 點/支）與單集累積總點數，取得 `confirm_token`。
7. 站主確認帳單後呼叫 `flow_generate_clips(confirm_token)` → `flow_wait` — 逐鏡生成、免費下載 720p、本機升 `1080p30` 並產出 4 格 QA 表與 `manifest.json`。
8. `flow_episode_ledger` — 檢視最終點數帳本與缺檔清單，確認後執行：
   ```powershell
   npm run vdrive -- push-episode --series curio --path "<分類>/<代碼>/製作檔/<slug>" --from "work/video-episodes/<slug>"
   ```

---

## 四、維護與升級

- Google Flow 若改版 UI，只需在 Windows 終端機執行：
  ```powershell
  uv tool upgrade gflow-cli
  ```
- 若同時開了 Claude Code、Codex、Antigravity，系統會透過 `%LOCALAPPDATA%\mokaair-flow\runtime.lock` 強制單一序列執行，避免搶 Chrome Profile 造成鎖檔或風控。
- 遇到 403／帳號驗證／selector 漂移時系統採 **Fail-Fast 絕不自動重試**，保護訂閱帳號安全。
