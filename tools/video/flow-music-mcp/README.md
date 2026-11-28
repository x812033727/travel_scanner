# Mokaair Google Flow Music 本機 MCP（`mokaair-flow-music` · Lyria 3.5）

專為 Mokaair 解說雙系列（`curio` / `sothatswhy`）、AI 劇（`drama-16x9` / `drama-9x16`）與零台詞 Shorts（`shorts`）打造的零外部依賴本機 Google Flow Music（`https://www.flowmusic.app` / Lyria 3.5）MCP Server 與 CLI。

- **零外部二進位依賴**：純 Node.js >= 22 ESM + 原生 WebSocket Chrome DevTools Protocol（CDP）＋本機 FFmpeg。
- **憑證不離開 Chrome**：每個帳號隔離在獨立的 `%LOCALAPPDATA%\mokaair-flow-music\chrome-profiles\profile_<name>`，透過頁面內同源 `fetch()` 呼叫 `/__api/clips/user/<id>?public_only=false` 與 `/__api/download/audio/<id>?format=m4a|mp3|wav`，繞過瀏覽器多次下載封鎖與背景分頁凍結。
- **Route B（0 GitHub Commit）**：所有暫存、下載、剪輯與簽核檔全部鎖在 `.gitignore` 的 `work/music-library/<collection>/`，完成後經 SHA-256 0 差異驗證同步至 Google 雲端硬碟。

---

## 一、Windows 本機首次安裝

```powershell
powershell -ExecutionPolicy Bypass -File tools\video\flow-music-mcp\install-windows.ps1 -WriteSetup
```

手動開啟隔離 Chrome 視窗登入 Flow Music（不碰日常 Chrome 與密碼），登入後關閉該視窗即可：

```powershell
npm run flow-music -- login
npm run flow-music -- status
```

多帳號隔離登入：

```powershell
npm run flow-music -- login --profile member-2
npm run flow-music -- profiles
```

---

## 二、17 個 MCP 工具

| 階段 | 工具 | 說明 |
| :--- | :--- | :--- |
| **環境與帳號** | `music_status` / `music_profiles` | 檢查 Chrome/FFmpeg、`www.flowmusic.app` 登入態、帳號 handle 與 profile 鎖檔 |
| **建庫／匯入** | `music_init_collection` | 建立 `work/music-library/<collection>/` 或直接匯入既有雲端資料夾（如 `flow-music-20261117`） |
| **提示詞把關** | `music_preflight_plan` | 檢查底樂禁人聲／禁大爆點混音規範、版權藝人詞、重複檔名與 Lyria 3.5 短音樂／音效切段提醒 |
| **生曲與拉取** | `music_generate` / `music_list_remote` / `music_download` | 透過 Chrome CDP 送 Lyria 3.5 提示詞、列雲端曲目、批次下載（自動 `-take1/-take2/-take3` 防覆蓋） |
| **音訊量測與切段** | `music_measure` / `music_detect_slices` / `music_cut` | FFmpeg 完整解碼長度、EBU R128（`lufs_i`、`lufs_m`、`peak_dbtp`）、近靜音／削波警訊、`silencedetect` 找切點與淡入淡出裁切 |
| **試聽與簽核** | `music_qa_gallery` / `music_approve` | 產出內含 `<audio>` 播放器與響度標章的 `qa-gallery.html`，一鍵複製 JSON 簽核可用／不用與理由 |
| **接產線與備份** | `music_export_sfx_set` / `music_stage_for_episode` / `music_push_drive` | 匯出通過 `sfxSetProblems` 驗證的第 2 版 `_sfx/<set>/manifest.json`（可自動跑 `assemble sfx-measure`）、部署 `_music/`＋`video.json` 片段、SHA-256 0 差異回傳雲端硬碟 |
| **非同步排程** | `music_wait` / `music_cancel` | 分段等待批次生曲／下載任務或中途安全取消 |
