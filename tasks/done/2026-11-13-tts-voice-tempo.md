---
id: 2026-11-13-tts-voice-tempo
title: TTS 支援 voice.tempo 等高微加速與語速輸出
status: done
priority: P2
area: tools
owner: antigravity-gemini
claimed_at: 2026-11-13T18:43:32Z
created_at: 2026-11-13T18:43:15Z
completed_at: 2026-11-13T19:11:47Z
branch: feat/video-tts-voice-tempo
depends_on: []
scope:
  - tools/video/core/schema.mjs
  - tools/video/core/schema.test.mjs
  - tools/video/tts/requests.mjs
  - tools/video/tts/tempo.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/tts.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# TTS 支援 voice.tempo 等高微加速與語速輸出

## Why

站主在 Claude 對話配對影音權杖做片時，Gemini TTS（如 `Sulafat`、`Leda`）即使在 `voice.style` 寫明「一秒五個字以上，句與句緊接、不拖長尾音」，有時實測仍落在 4.1–4.3 字／秒，低於站主 2026-11-13 定下的 **≥ 4.4 字／秒**門檻，過去只能反覆花點數重抽整集 TTS。

需要在 `voice`（`doc.voice`、`doc.characters[].voice`、`doc.cohost.voice`）提供選填的 `tempo`（`1 <= tempo <= 1.5`，只許等高加速縮短音訊、嚴禁 `< 1` 灌水墊長片長），在 `tts` 合成單句音檔後、`buildTimeline` 量測 `samplesById` 前，以 `ffmpeg -af atempo=<tempo>` 做不變調微加速並同步縮放字元時間軸，同時保存 1x 原始音檔讓後續微調 `tempo` 免重複付費，並在 `tts` 結尾直接印出實測語速（`chars/s`，不含標點字數 ÷ 單句音檔秒數總和）以及支援 `audition --tempo`。

## Definition of done

- [x] `validateVoice` 接受 `voice.tempo` 為 `1` 到 `1.5` 的有限數值（涵蓋 `voice`、`characters[].voice`、`cohost.voice`），拒絕 `< 1`、`> 1.5`、字串、布林與無限值；未填或 `1` 時快取鍵與既有影片 100% 一致。
- [x] `planRequests` 在 `tempo > 1` 時切分不同 `tempo` 的請求並納入 `line.key`／`request.key` 與 `audio_ref` 一致性檢查，但不把 `tempo` 放進送往 `/api/video/speech` 的 HTTP body。
- [x] `tts` 在 `tempo > 1` 時以 `ffmpeg -af atempo=<tempo>` 等高加速 48 kHz 16-bit mono WAV、等比縮放 `timing.chars`，並保留 `<id>.raw.wav` 支援本機免付費重調 `tempo`；缺少 `ffmpeg` 時在發送任何付費請求前以 `EXIT.missing` 結束。
- [x] `audition` 支援 `--tempo <1..1.5>`；`tts` 結尾印出實測語速 `(X.XX chars/s)`。
- [x] 由獨立審查代理完成 `docs/videos/long-form/review.md` 與 `review.json` 的 `DURATION_ONLY` 綁定，`node tools/video/long-form/cli.mjs check` 與測試通過。

## Steps

- [x] 新增 `tools/video/tts/tempo.mjs` 並更新 `schema.mjs`、`requests.mjs`、`tts/cli.mjs`。
- [x] 補齊 `schema.test.mjs` 與 `tts.test.mjs` 單元與真實 `ffmpeg` 整合測試。
- [x] 先提交程式碼變更（`0fb563fb`），再由獨立審查代理（`antigravity-review-tts-voice-tempo-20261113`）執行 `DURATION_ONLY` 審查並更新 `docs/videos/long-form/review.{md,json}`。

## How to verify

```bash
node tools/video/long-form/cli.mjs check
node --test --test-concurrency=4 tools/video/core/*.test.mjs tools/video/tts/*.test.mjs tools/video/long-form/*.test.mjs tools/video/qa/*.test.mjs
npm run test:docs-videos && npm run check:tasks
```

## Notes

- `VOICE_TEMPO_MIN = 1` 確保 `tempo` 只能縮短語音時長，絕不可能把不足 8 分鐘的短稿灌水拉長通過 `MIN_EPISODE_MINUTES` 或 14,400 影格 QA 門檻。
- 實測語速計算公式對齊 `.agents/skills/curio-episode/SKILL.md` §系列定案〈語速與停頓〉：字數不含空白與標點符號，除以每句錄音長度加總（不含句間停頓）。
