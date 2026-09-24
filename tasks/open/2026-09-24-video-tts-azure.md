---
id: 2026-09-24-video-tts-azure
title: 影片產線 T2：台灣口音 TTS 用戶端（經伺服器合成）與選聲
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T02:42:18Z
created_at: 2026-09-24T00:41:02Z
completed_at:
branch: claude/video-tts
depends_on:
  - 2026-09-24-video-tooling-core
scope:
  - tools/video/tts
  - tools/video/core/paths.mjs
  - tools/video/core/state.test.mjs
  - tools/video/cli.mjs
---

# 影片產線 T2：台灣口音 TTS 用戶端（經伺服器合成）與選聲

## Why

影片旁白用 Azure AI Speech 的台灣口音語音：`zh-TW-HsiaoChenNeural`、`zh-TW-YunJheNeural`、`zh-TW-HsiaoYuNeural`，或用多語語音講 zh-TW。設計在 `docs/videos/DESIGN.md`。

2026-09-24 站主改了做法：金鑰存在正式站後台，由伺服器代為合成（票 `2026-09-24-video-speech-server`，PR #709）。所以這張票不直接呼叫 Azure：

- 本機工具帶著後台建立的「影片工具權杖」，呼叫 `POST {site}/api/video/speech`。
- 送出的內容是 `{voice, rate, segments:[{parts:[{text, alias?}], break_after_ms}]}`，拿回 48 kHz 16-bit mono WAV。
- 用 `GET {site}/api/video/speech/status` 查允許的聲音、每月上限與本月用量。

即時合成沒有時間點，所以時間軸這樣來：每個場景送一次請求、句間固定停頓，然後在 Node 裡找靜音切段。逐句分開合成的話，每句語調都會重新起頭。

## Definition of done

- [x] `node tools/video/cli.mjs login` 把權杖存到使用者目錄（不在 repo、不在環境變數），並用 status 驗證可用。
- [x] `audition --text-file <f> [--voices a,b]` 為每個聲音產生試聽 WAV，另附一頁可以並排播放的 HTML。
- [x] `tts --slug <slug>` 產生每句的 WAV、`narration.wav`、`timeline.json`（帶 `speech_hash`）。
  - 改一句只重送那一句所在的請求（內容雜湊快取）。
  - 靜音切段對不上時，該段自動退回逐句合成，並說明是哪一段。
- [x] `tts --dry-run` 印出估計的計費字元，以及伺服器回報的本月用量與上限，不送合成請求。
- [x] `tts --redo flags.json` 只重做被標記的句子。
- [x] 遇到 429 依 `Retry-After` 退避。
  - 權杖無效或伺服器沒設定：結束碼 3（需要站主）。
  - 預算用完或服務錯誤：結束碼 4。
- [x] 工作區預設為 `~/mokaair-work/videos`，不必設 `VIDEO_WORKDIR`。

## Steps

- [x] `tools/video/tts/wav.mjs`：WAV 讀寫、格式檢查、靜音、串接。
- [x] `tools/video/tts/split.mjs`：靜音偵測與切段、修掉頭尾靜音、和字數比例對照。
- [x] `tools/video/tts/requests.mjs`：場景→請求（依發音字典組 parts、每次最多 1,500 字、句間停頓）、快取鍵。
- [x] `tools/video/tts/client.mjs`：呼叫伺服器、重試、錯誤分類。
- [x] `tools/video/tts/credentials.mjs`：權杖的存放與讀取。
- [x] `tools/video/tts/cli.mjs`：`login`、`audition`、`tts`。
- [x] `tools/video/core/paths.mjs`：預設工作區。
- [ ] 站主在正式站後台填好金鑰、建立權杖、跑 `login`，用試作影片實際合成一次（要等 #709 部署）。

## How to verify

```bash
node --test "tools/video/**/*.test.mjs"
node tools/video/cli.mjs login
node tools/video/cli.mjs tts --slug <slug> --dry-run
```

## Notes

- **沒勾的實際合成**：要等 PR #709 部署、站主在後台建立權杖並跑 `login`。這一步是試作影片（`2026-09-24-video-pilot-ai-model-choice`）的第一步，在那張票裡做；這張票的程式與測試都已完成。
- **切段**：每次請求句間固定 800 ms 停頓。取最長的 N−1 段靜音（至少 450 ms，RMS < 120）的中點切開，修掉頭尾靜音（留 40 ms），再用「每段長度占比對照字數占比，差距在 0.45–2.2 倍內」判斷切得對不對；不對就整批改成逐句合成。
- **快取**：`audio/cache.json` 記每句屬於哪個請求的內容雜湊；請求的句子、聲音、語速、發音字典任一改變，那一批就重合成。`--redo flags.json` 接審聽頁匯出的 `{flags:[句子 id]}`。
- **權杖**：存在 `~/.mokaair/video-tool.json`（`login` 用隱藏輸入讀，先向伺服器驗證再存）。`MOKAAIR_VIDEO_TOKEN`、`MOKAAIR_SITE` 可以覆寫，給 CI 或本機測試用。
- **預設工作區**：`~/mokaair-work/videos`（`resolveWorkBase`），`--workdir`／`VIDEO_WORKDIR` 仍可覆寫。

- 需要站主先在後台開 Azure 語音（F0）並建立權杖；代理不經手金鑰。
- zh-TW 的 `<phoneme>` 音標集沒有官方文件，不用；發音修正一律用 `alias`（伺服器轉成 `<sub alias>`）。
