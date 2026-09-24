---
id: 2026-09-24-video-tts-azure
title: 影片產線 T2：Azure 台灣口音 TTS 與選聲
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-24T00:41:02Z
completed_at:
branch:
depends_on:
  - 2026-09-24-video-tooling-core
scope:
  - tools/video/tts
---

# 影片產線 T2：Azure 台灣口音 TTS 與選聲

## Why

影片旁白用 Azure AI Speech 的台灣口音語音（`zh-TW-HsiaoChenNeural`、`zh-TW-YunJheNeural`、`zh-TW-HsiaoYuNeural`，或多語語音 Ava／Andrew 講 zh-TW）。免費層每月 50 萬計費字元；每個中文字算 2 個、SSML 標記也計費，一支 10 分鐘約 8,000–9,000 計費字元（2026-09-24 查 Microsoft Learn〈Text to speech overview〉§Billable characters）。即時 REST 只回音檔、沒有時間點，所以時間軸靠「每場景一次合成、句間固定停頓、在 Node 裡找靜音切段」。設計全文在 `docs/videos/DESIGN.md`（T1 一起合併）；skill 是 `.agents/skills/youtube-video/`。

## Definition of done

- [ ] `node tools/video/cli.mjs audition --text-file <f> --voices <a,b,c> --workdir <dir>` 產生各聲音的試聽檔與一頁比較用的 HTML。
- [ ] `tts --slug <slug> --workdir <dir>` 產生每句的 48 kHz 16-bit mono WAV、`narration.wav`、`timeline.json`；改一句只重做那一句所在的場景（內容雜湊快取）。
- [ ] `tts --dry-run` 依實際送出的 SSML 算計費字元（中文字 ×2、標記計入）與相對免費額度的用量，不打 API。
- [ ] `tts --redo flags.json` 只重做被標記的句子。
- [ ] 靜音切段對不上時自動退回逐句合成，並在輸出中說明哪個場景退回。
- [ ] 429 依 `Retry-After` 退避；金鑰只從 `AZURE_SPEECH_KEY`、`AZURE_SPEECH_REGION` 讀，不寫進任何檔案或日誌。

## Steps

- [ ] `tools/video/tts/ssml.mjs`：組 SSML（`<sub alias>` 套用 `docs/videos/lexicon.json`、句間 `<break>`、`rate`），純函式＋測試。
- [ ] `tools/video/tts/split.mjs`：PCM 靜音偵測與切段，純函式＋合成訊號的測試。
- [ ] `tools/video/tts/azure.mjs`：REST 呼叫、`riff-48khz-16bit-mono-pcm`、重試。
- [ ] `tools/video/tts/index.mjs`：供應商介面、快取、`audition`、`tts` 子指令。
- [ ] 站主試聽後把選定的聲音寫進 `docs/videos/DESIGN.md` 的頻道規格（或 T5 的 README）。

## How to verify

```bash
node --test tools/video/tts/*.test.mjs
node tools/video/cli.mjs tts --slug <slug> --workdir <VIDEO_WORKDIR> --dry-run
```

## Notes

- 需要站主先開 Azure Speech 資源（F0）並自己設定環境變數；代理不經手金鑰。
- zh-TW 的 `<phoneme>` 音標集沒有官方文件，不用；發音修正一律 `<sub alias>`。
- 靜音切段不穩時的備案：Azure 批次合成 API 的 `sentenceBoundaryEnabled`（部分區域不收免費層）。
