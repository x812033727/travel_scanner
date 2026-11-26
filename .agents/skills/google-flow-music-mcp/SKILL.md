---
name: google-flow-music-mcp
description: 用本機 Google Flow Music MCP（mokaair-flow-music，直連 www.flowmusic.app / Lyria 3.5，零外部依賴 Chrome CDP）製作與管理 Mokaair 全系列底樂（bed）、短音樂（cue）與音效（sfx）：多帳號隔離登入、底樂禁人聲／禁爆點與版權前置把關、同源批次下載防覆蓋（-takeN）、FFmpeg EBU R128 響度與靜音切段、互動式 qa-gallery.html 試聽簽核、匯出通過 sfxSetProblems 的第 2 版 _sfx/<set>/manifest.json、部署 _music/ 與 SHA-256 0 差異同步 Google 雲端硬碟。要用 Flow Music 生音樂、拉曲目、試聽既有配樂庫（如 flow-music-20261117）、剪短音樂或音效組時，先讀這個 skill。Produce, audition, slice, and sync Mokaair background beds, cues, and SFX with the local Google Flow Music MCP server (mokaair-flow-music).
---
# Google Flow Music 本機 MCP（`google-flow-music-mcp`）

本 skill 規範 Claude Code、Codex 與 Antigravity 呼叫本機 `mokaair-flow-music` MCP Server（[`tools/video/flow-music-mcp/server.mjs`](tools/video/flow-music-mcp/server.mjs)）操作 `https://www.flowmusic.app`（Lyria 3.5）製作與整理配樂庫的標準流程。所有產物一律鎖在 `.gitignore` 的 `work/music-library/`（Route B，0 GitHub Commit）。

## 一、開工前確認

1. 本機體檢與登入（絕不碰日常 Chrome 或密碼）：
   - 體檢：`npm run flow-music -- doctor`
   - 登入：`npm run flow-music -- login`（多帳號加 `--profile <name>`）
   - 寫入各客戶端設定：`npm run flow-music -- setup --write`
2. 呼叫 `music_status`（或 `music_profiles`）確認 `www.flowmusic.app` session 有效且無併發鎖。

## 二、標準作業順序

1. **建庫或匯入既有曲庫**：呼叫 `music_init_collection`（要整理既有雲端曲庫如 `flow-music-20261117` 時，傳入 `importFromDir` 直接帶入現有 `manifest.json` 與音檔）。
2. **提示詞前置把關（生新曲時）**：必跑 `music_preflight_plan`：
   - `bed`（底樂）必須純音樂、無人聲、無大爆點、速度穩定、結尾乾淨（墊在旁白下 `gain_db -20`、`duck_db -10`，混音後 ≤ `-24 LUFS`）。
   - `cue`（短音樂）與 `sfx`（音效）因 Lyria 3.5 一律生成約 1 分鐘，下載後必經切段步驟。
3. **生曲或批次下載**：
   - 生新曲：`music_generate` → `music_wait`（自動下載並防同標題覆蓋為 `-take1/-take2/-take3`）。
   - 拉雲端既有曲目：`music_list_remote` → `music_download` → `music_wait`。
4. **本機 FFmpeg 量測與切段**：
   - `music_measure`：產出完整解碼秒數、`lufs_i`、`lufs_m`、`peak_dbtp`、`silences` 與 `sha256`，自動標記近靜音（`< -38 LUFS`）與削波（`> 0 dBTP`）。
   - `music_detect_slices` + `music_cut`：用 `silencedetect` 找出短音樂與多段音效切點，裁切為 `*-cut.m4a` 或單一音效並寫入 `manifest.json`。
5. **試聽簽核**：
   - 呼叫 `music_qa_gallery` 產出 `qa-gallery.html`；由站主開啟網頁試聽，標記可用／不用與理由（有人聲、有爆點、搶旁白等），複製 JSON 貼回執行 `music_approve`。
6. **接回產線與雲端備份**：
   - **底樂／短音樂**：呼叫 `music_stage_for_episode` 複製已通過曲目至 `<workBase>/_music/` 並取得 `video.json` 的 `music` 片段與 SHA-256。
   - **第 2 版音效組**：呼叫 `music_export_sfx_set`（含必填 `stamp`、`whoosh`、`pop`）產出通過 `sfxSetProblems` 的 `_sfx/<set>/manifest.json`，並可選擇直接執行 `assemble sfx-measure`。
   - **雲端硬碟備份**：呼叫 `music_push_drive` 做 SHA-256 0 差異同步回 `AI/備份/AI劇/`。

## 三、AI 揭露與帳號安全鐵則

- 所有 Flow Music 曲目皆為 AI 生成（Lyria 3.5），`manifest.json` 固定標記 `ai_generated: true`；影片上架前須依 YouTube「經過修改或合成的內容」規則確認揭露設定。
- 遇授權失效（`auth_expired`）、限流 403/429（`rate_limited`）或頁面 DOM 改版（`selector_drift`）時，佇列會立即 **Fail-Fast 中止**；嚴禁寫迴圈硬重試。
