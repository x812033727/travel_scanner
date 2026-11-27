---
name: google-flow-mcp
description: 用本機 Google Flow MCP（mokaair-flow，訂閱帳號點數，路線 A 封裝 gflow-cli）製作原來如此事務所、奇聞檔案局、AI 劇（橫式 16:9 與直式 9:16 漫劇／真人劇）與零台詞 Shorts 短劇：雙專案隔離、多角色 Cast 與防串角、同機位 edit_from 圖編鏈、尾幀接龍 continue_from、0 點數靜圖與 16:9／9:16 驗收、三鏡 Pilot、多 Take 保留與 MAX_CLIP_TAKES 上限、單次 confirm_token 預算守門、video.json 匯入橋接、斷點續跑與失聯撈片對帳，以及本機 FFmpeg 1080p30 bt709 升頻與 PSNR／硬切 QC。要用 Google Flow MCP 生圖、生片、延長片段、查點數、換訂閱帳號、匯入 video.json 或做 AI 劇與解說片拍攝時，先讀這個 skill。Produce Mokaair explainers, AI dramas (16:9/9:16), and vertical Shorts with the local subscription-backed Google Flow MCP server (mokaair-flow).
---
# Google Flow 本機 MCP（`google-flow-mcp`）

本 skill 規範 Claude Code、Codex 與 Antigravity 呼叫本機 `mokaair-flow` MCP Server（[`tools/video/flow-mcp/server.mjs`](tools/video/flow-mcp/server.mjs)）製作解說長片、AI 劇與零台詞 Shorts 的標準關卡。所有單集產物一律鎖在 `.gitignore` 的 `work/video-episodes/`（Route B，0 GitHub Commit）。

## 一、開工前確認

1. 本機環境檢查與登入（在有畫面的 Windows / macOS 本機執行，絕不碰日常 Chrome 或密碼）：
   - 環境體檢：`npm run flow -- doctor`
   - 手動登入：`npm run flow -- login`（多帳號加 `--profile NAME`）
   - 寫入各客戶端設定：`npm run flow -- setup --write`（Windows 可直接跑 `tools/video/flow-mcp/install-windows.ps1`）
2. 開工前必先拉取雲端最新正本規則與角色設定圖：
   - 解說系列：`npm run vdrive -- pull-rules explainer`
   - AI 劇／全系列：`npm run vdrive -- pull-rules all`
3. 確認可用訂閱帳號與點數（0 點數）：呼叫 `flow_status` 或 `flow_profiles`。若電腦將進入休眠或 Chrome 視窗最小化，先提醒站主保持視窗可見。

## 二、系列預設與防雷紅線

| `series` 值 | 適用節目 | 畫幅／靜圖尺寸 | 預算軟／硬上限 | 音訊與 QC 策略 |
| :--- | :--- | :---: | :---: | :--- |
| `sothatswhy` | 原來如此事務所 | `16:9` / `1376x768` | 500 / 500 點 | `-an` 靜音升 `1080p30 bt709 tv` |
| `curio` | 奇聞檔案局 | `16:9` / `1376x768` | 550 / 600 點 | `-an` 靜音升 `1080p30 bt709 tv` |
| `drama-16x9` | 橫式 AI 劇（種田、祖媽、漫劇） | `16:9` / `1376x768` | 800 / 1200 點 | `-an` 成片 ＋ 另存 `raw-audio/*.wav` ＋ PSNR／硬切 QC |
| `drama-9x16` | 直式 AI 短劇／真人短劇 | `9:16` / `768x1376` | 300 / 500 點 | 同上 ＋ 9:16 安全區紅框 QA |
| `shorts` | 零台詞 Shorts 短劇 | `9:16` / `768x1376` | 120 / 240 點 | 自動加無台詞防護句 ＋ `-an` ＋ 9:16 安全區紅框 QA |

## 三、標準作業順序（不可跳關）

1. **建集與雙專案隔離（0 點數）**：呼叫 `flow_init_episode` 綁定獨立 `characterProjectId` 與 `sceneryProjectId`。無人空景鏡絕不放入角色參考圖。
2. **備齊 Cast 與分鏡表（0 點數）**：
   - AI 劇多角色先用 `flow_register_character` 寫入 `cast.json`（含多套 `looks` 與 `noAccessories` 防串角註記；加 `saveToSeries: true` 存進跨集共用表，後續集數 `flow_init_episode` 自動繼承；需要 `@Name` 時設 `createFlowEntity: true`）。
   - 若已有漫劇 `video.json`，直接呼叫 `flow_import_video_json` 自動轉出 `flow-shot-list.json` 與 `cast.json`（保留 `data.source` 0 點數 `cut` 鏡並清除 H3 標籤）。
3. **前置檢查（0 點數）**：必跑 `flow_preflight_shotlist`（AI 劇首輪建議加 `pilot: true`），將所有 `blocker`（未成年詞、極端血腥、版權 IP、雙專案外洩、無效 `edit_from`／`continue_from`／`cut`、超預算）清到 0 才准開 Chrome。
4. **先圖後片（0 點數）**：
   - 呼叫 `flow_generate_stills`（AI 劇首輪先跑 `pilot: true` 三鏡小樣；高解析封面／靜圖可用 `flow_upscale_still` 拉 2K 或 Ultra 4K），用 `flow_wait` 輪詢至完成。
   - 系統會自動以二進位檔頭驗尺寸，抓到 Flow 靜默重置回 `1:1` 會隔離到 `stills/_rejected/`。
   - 請站主雙擊開啟 `stills/qa-gallery.html` 肉眼檢查（直式劇開 9:16 安全區紅框），點「複製 flow_approve_stills JSON」貼回執行 `flow_approve_stills`。
5. **試算點數與人工簽核（0 點數 → 扣點）**：
   - 呼叫 `flow_plan_clips`（斷點續跑加 `resumeMissingOnly: true`；Pilot 加 `pilot: true`）或 `flow_plan_extend`（延長既有片段）；若目前帳號點數不足，依回傳的 `suggestedProfiles` 改換餘額足夠的訂閱帳號 `profile`。
   - **未經站主同意，禁止自行呼叫 `flow_generate_clips` 或 `flow_extend_clip`。** 取得同意後才帶入該次一次性 `confirm_token` 送出，並以 `flow_wait` 分段等待避免 60 秒超時。
6. **挑片、對帳、批次匯入與交付雲端（0 點數）**：
   - 每個鏡頭最多自動保留到 `MAX_CLIP_TAKES = 2`（存於 `flow-clips/takes/`，廢片全留不刪）；達上限時必先改 prompt 重設計，勿盲目重抽。
   - 用 `flow_select_take` 選定最佳 Take 並更新 `flow-clips/import-bridge.json`；可用 `npm run flow -- import-all --slug <slug>` 一鍵批次匯進產線。
   - 若出現斷線或 `charged: "maybe"`，**先跑 `flow_reconcile` 從 Flow 撈回已扣點影片**，再以 `flow_plan_clips({ resumeMissingOnly: true })` 補跑缺鏡，嚴禁重複扣點。
   - 收工呼叫 `flow_episode_ledger` 或直接跑 `npm run flow -- push --slug <slug> --path "<雲端路徑>"` 通過防呆檢查後備份至 Google 雲端硬碟。
7. **純雲端環境透過遠端閘道（`POST /api/video/mcp/flow`）跨機同步（0 點數）**：
   - 先用 `node tools/video/cli.mjs login --flow` 配對影片工具權杖。
   - 把本機分鏡表與已審首幀增量推上主機閘道：`npm run flow -- remote-push --slug <slug> --from work/video-episodes/<slug>`（底層呼叫 `flow_list_files` ＋ 512 KiB 分塊 `flow_write_file` 與 SHA-256 0 差異驗證）；遠端生片前呼叫 `flow_approve_stills` 會自動辨識已上傳的 16:9／9:16 首幀。
   - 生片完成後用 `npm run flow -- remote-pull --slug <slug> --to work/video-episodes/<slug>` 拉回成片（底層走 `flow_read_file` 分塊校驗），或於主機有設定 `vdrive` 時直接呼叫 `flow_push_drive` 備份至 Google 雲端硬碟。

## 四、帳號安全鐵則

- 遇 403／帳號風控（exit 22）、selector 漂移（exit 23／28）或授權失效（exit 3）時，MCP 會立刻 **Fail-Fast 中止批次**；**絕不可手動寫迴圈反覆重試**，改用 `uv tool upgrade gflow-cli` 或 `npm run flow -- login` 排除原因。
- 詳見 [`tools/video/flow-mcp/README.md`](tools/video/flow-mcp/README.md) 與 `tools/video/flow-mcp/config.mjs`。
