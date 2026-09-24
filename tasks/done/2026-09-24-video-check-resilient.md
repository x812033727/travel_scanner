---
id: 2026-09-24-video-check-resilient
title: 旁白檢查遇到 Gemini 轉寫失敗時繼續跑、並記下上游狀態
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T15:27:25Z
created_at: 2026-09-24T15:27:17Z
completed_at: 2026-09-24T15:33:03Z
branch: claude/video-check-resilient
depends_on: []
scope:
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_speech_check.py
  - tools/video/tts/check.mjs
  - tools/video/tts/check.test.mjs
---

# 旁白檢查遇到 Gemini 轉寫失敗時繼續跑、並記下上游狀態

## Why

試作片〈AI 模型怎麼挑〉第一次跑 `check-audio`（#732 上線後），157 句跑到第 40 句、第二次跑到第 83 句，
就被一句「Gemini 暫時無法轉寫」整個停掉：客戶端每句已重試 5 次，還是失敗。主機 log 只看得到
`/api/v1/video/speech/transcribe` 的 200 與 502 交錯，看不出 Gemini 回了什麼，因為
`checking.transcribe` 把上游狀態丟掉了；Gemini 回 200 但被擋或截斷時，`gemini_output_text` 的
`ValueError` 還會變成 500。

## Definition of done

- [x] 一句轉寫不了，其他句照跑；結束時列出沒檢查到的句子與原因，exit 4，重跑只補那幾句。
- [x] 連續 3 句失敗就停（Gemini 整個掛了），不在剩下每一句上各耗掉一輪重試。
- [x] 主機 log 與錯誤訊息都帶 Gemini 的 HTTP 狀態與錯誤狀態字（例如 `HTTP 503 UNAVAILABLE`），不帶金鑰或請求內容。
- [x] Gemini 的 500／503／504 回 503＋`Retry-After: 20`，讓工具真的等一下再試；被擋或空白的回應是 502，不是 500。

## Steps

- [x] `checking.transcribe`：記 log、訊息帶狀態、`ValueError` 轉成 `SpeechUpstreamError`。
- [x] `/speech/transcribe`：5xx 對應 `video_speech_upstream_busy`＋Retry-After，其他上游錯誤的 detail 帶原因。
- [x] `check.mjs`：服務端錯誤跳過該句、`GIVE_UP_AFTER = 3`、摘要寫「N of M lines checked」、stage 紀錄 `unchecked`。
- [x] 測試：`test_video_speech_check.py` 兩項、`check.test.mjs` 兩項。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_check.py tests/test_error_localization.py
npm run test:tools
```

部署後：`check-audio` 再遇到轉寫失敗時，摘要會列出句子 id 與「Gemini answered HTTP …」；主機上
`docker compose -f docker-compose.prod.yml logs api | grep "Gemini transcription"` 看得到同樣的狀態。

## Notes

- 工具端的跳過不用等部署：現行伺服器回的 502 `video_speech_upstream_failed` 在客戶端已經是可重試的服務端錯誤，
  新版 `check.mjs` 重試 5 次後就跳過。部署後才多了狀態碼與較長的等待。
- 錯誤狀態字只收全大寫、40 字以內（Google 的 `status` 欄位），`message` 不收，免得哪天它回顯請求內容。
- 例外仍在 `admin_api.py` 轉成 `AppError`：`checking.py` 不在 admin 路徑下，丟 `AppError` 會被
  `test_error_localization` 要求五語系翻譯（#732 踩過）。
