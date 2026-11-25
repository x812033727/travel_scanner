# Mokaair Google Flow 本機 MCP v2（解說長片 ＋ AI 劇 ＋ 直式短劇 · 訂閱帳號版）

專為 Mokaair 全系列打造的本機 Google Flow MCP Server 與 CLI：
- **解說雙系列**：《原來如此事務所》（`sothatswhy`）、《奇聞檔案局》（`curio`）
- **AI 劇（橫式／直式）**：《種田娶妻打天下》橫／真人版、《恁祖媽今年18》、橫式漫劇（`drama-16x9`）與直式短劇／漫劇（`drama-9x16`）
- **零台詞 Shorts 短劇**：9:16 動物／喜劇短劇（`shorts`）

直接吃你的 **Google AI Plus / Pro / Ultra 訂閱帳號點數**（支援多帳號 Profile 切換），0 GitHub Commit（Route B 全部產物鎖定在 `.gitignore` 的 `work/video-episodes/<slug>/`）。

---

## 一、Windows 本機首次安裝（只要做一次）

> **注意**：請將 `travel_scanner` 放在 **非 OneDrive 同步** 的本機資料夾（例如 `C:\dev\travel_scanner`）。

### 一鍵安裝（推薦）

在 `travel_scanner` 根目錄開啟 Windows PowerShell：

```powershell
powershell -ExecutionPolicy Bypass -File tools\video\flow-mcp\install-windows.ps1 -WriteSetup
```

接著開啟獨立 Chrome 視窗手動登入 Google Flow（絕不碰日常 Chrome 與密碼）：

```powershell
npm run flow -- login
npm run flow -- status
```

多帳號切換（例如第二個 Google AI 訂閱帳號）：

```powershell
npm run flow -- login --profile pro-2
npm run flow -- profiles
```

---

## 二、18 個 MCP 工具與支援能力

| 階段 | 工具 | 費用 | 說明 |
| :--- | :--- | :---: | :--- |
| **環境與帳號** | `flow_status` / `flow_profiles` | 0 點 | 檢查登入態、`gflow-cli` 版本、多帳號剩餘點數與各 profile 互斥鎖 |
| **開集與角色** | `flow_init_episode` | 0 點 | 綁定 `character` 與 `scenery` 隔離雙專案，記錄劇名與集數，**並自動繼承同劇 `work/video-episodes/_series/<劇名>/cast.json` 固定角色表** |
| **AI 劇 Cast** | `flow_register_character` | 0 點 | 登記多角色 `cast.json`、多套服裝 `looks`、`noAccessories` 防串角註記、`saveToSeries: true` 寫入跨集共用表、可選建立 Flow `@Name` Character |
| **漫劇轉檔** | `flow_import_video_json` | 0 點 | 直接讀 `video.json` 轉成 `flow-shot-list.json` ＋ `cast.json`（清 `<Picture N>`、保留 `data.source` 0 點切鏡與無台詞防護句） |
| **前置把關** | `flow_preflight_shotlist` | 0 點 | 安全詞掃描（解說嚴格／AI 劇武打分級警告）、雙專案隔離、`edit_from` / `continue_from` / `cut` 驗證、多角防串角警告、3 鏡 Pilot 與彈性秒數／模型點數試算 |
| **0 點數生圖與放大** | `flow_generate_stills` / `flow_upscale_still` | 0 Veo 點 | `Nano Banana 2.1` 生首尾格（`edit_from` 圖編鏈、3 鏡 Pilot、16:9／9:16 像素驗收與互動式 `qa-gallery.html`）；`flow_upscale_still` 支援 2K／Ultra 4K 靜圖放大 |
| **靜圖簽核** | `flow_approve_stills` | 0 點 | 貼上網頁複製的 JSON 簽核通過／退回，解鎖付費生片 |
| **預算帳單** | `flow_plan_clips` / `flow_plan_extend` | 0 點 | 查先圖後片、查 `MAX_CLIP_TAKES=2` 上限、支援 `pilot` 與 `resumeMissingOnly`、餘額不足時自動推薦其他有餘額的訂閱帳號 profile、核發單次 `confirm_token` |
| **付費生片與延長** | `flow_generate_clips` / `flow_extend_clip` | **扣點** | 必帶 `confirm_token`；支援 `i2v`／`r2v`／`continue_from`（尾幀接龍）／`extend`（片段延長）、彈性 3–15s 與單鏡切 Veo 3.1；歷史 Take 全留於 `flow-clips/takes/`；免費 720p 下載 → 本機 FFmpeg `1080p30 / bt709 / tv / -an` ＋ AI 劇另存 `raw-audio/*.wav` ＋ **第 0 格 PSNR ≥ 22 與中途硬切 QC** ＋ `import-bridge.json` |
| **挑片與對帳** | `flow_select_take` / `flow_reconcile` | 0 點 | 切換正式 Take（廢片全留供雲端備份）；`flow_reconcile` 撈回 `charged: maybe` 已扣點未下載影片避免重複燒點數 |
| **排程與收工** | `flow_wait` / `flow_cancel` / `flow_episode_ledger` | 0 點 | 防 60 秒超時輪詢、安全中止、輸出最終帳本；搭配終端機 `npm run flow -- import-all --slug <slug>` 一鍵批次匯入產線與 `npm run flow -- push --slug <slug> --path "<雲端路徑>"` 驗收後直傳 Google Drive |

---

## 三、AI 劇分鏡範例（`drama-16x9` / `drama-9x16`）

```json
{
  "series": "drama-16x9",
  "shots": [
    {
      "id": "s01",
      "chapter": "act1",
      "track": "character",
      "mode": "clip",
      "characters": ["protagonist", "rival"],
      "character_looks": { "protagonist": "winter_cloak" },
      "clip_duration_sec": 6,
      "model": "omni-1.2-flash",
      "still_prompt": "Medium two-shot in lantern-lit courtyard; protagonist in blue winter cloak (no glasses) faces rival holding folded fan",
      "video_prompt": "Slow push-in as protagonist raises hand firmly while snow drifts past warm lanterns"
    },
    {
      "id": "s02",
      "chapter": "act1",
      "track": "character",
      "mode": "clip",
      "edit_from": "s01",
      "characters": ["protagonist", "rival"],
      "clip_duration_sec": 4,
      "still_prompt": "Same courtyard camera angle, rival steps back surprised dropping the folded fan",
      "video_prompt": "Quick reaction cut as rival flinches backward in the snow"
    },
    {
      "id": "s03",
      "chapter": "act1",
      "track": "character",
      "mode": "clip",
      "continue_from": "s02",
      "clip_duration_sec": 4,
      "video_prompt": "Continuous follow-through as the folded fan hits the stone tiles and slides"
    },
    {
      "id": "s04",
      "chapter": "act1",
      "track": "character",
      "mode": "cut",
      "source": "s01"
    }
  ]
}
```

### AI 劇建議標準流程

1. **三鏡 Pilot 小樣**：`flow_init_episode` → `flow_register_character`（或 `flow_import_video_json`）→ `flow_preflight_shotlist({ pilot: true })` → `flow_generate_stills({ pilot: true })` → 雙擊 `stills/qa-gallery.html` 點選並複製 JSON → `flow_approve_stills` → `flow_plan_clips({ pilot: true })` → 站主確認 → `flow_generate_clips`。
2. **全集放量與斷點續跑**：Pilot 過關後直接跑 `flow_plan_clips({ resumeMissingOnly: true })` 補齊剩餘鏡頭；若發生斷線或 `maybe`，跑 `flow_reconcile` 撈片對帳不重複扣點。
3. **挑片與回接產線**：查看 `flow-clips/qa-gallery.html`（含 PSNR、中途硬切建議剪點與原聲試聽），用 `flow_select_take` 選定最佳 Take，從 `flow-clips/import-bridge.json` 接回 `tools/video/cli.mjs clips import` 或剪接腳本，最後跑 `flow_episode_ledger` 提供的 `npm run vdrive -- push-episode` 整包備份上雲端硬碟。
