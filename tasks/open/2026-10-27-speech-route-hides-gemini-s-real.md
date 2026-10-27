---
id: 2026-10-27-speech-route-hides-gemini-s-real
title: Speech route hides Gemini's real error for whole-film budget films
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-27T00:28:26Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_speech/admin_api.py
---

# Speech route hides Gemini's real error for whole-film budget films

## Why

`_synthesize_with_gemini`（`apps/api/app/video_speech/admin_api.py`）對有整片預算帳戶的片（`reserve_pilot_call` 回 pilot），Gemini 回任何 401／403 以外的錯誤（429 每日上限、400 沒有音訊、500）都一律改成 504 `video_speech_upstream_lost`「可能已處理，請勿自動重送」，而且不記 log。保守地把它算成可能已計費沒錯，但真正的狀態碼從此看不到：站方、站主與工具都分不出是額度用完、內容被拒還是服務故障。

2026-10-27 00:00 UTC 前後，C14 remake（`story-everyday-camelbak-c14-remake-20261025`）第一句旁白連四次 504（含換一句不同的短句），每次在帳上留一筆 uncertain（上限 US$0.152）。推測是前一天 C11 約 102 次合成用完了 `gemini-3.8-flash-tts` 的每日請求數，但沒辦法確認。

## Definition of done

- [ ] 這條路徑把 Gemini 的狀態碼與錯誤摘要寫進 log（不含金鑰與內文），主機上 `docker compose logs api` 查得到。
- [ ] 能確定沒有計費的情況（例如 429 配額拒絕、400 沒有音訊且 usage 為零）照非 pilot 路徑回明確的代碼，並放掉預留；真的不確定的才回 `video_speech_upstream_lost`。
- [ ] 測試涵蓋 429、400（無音訊）與 500 三種。

## How to verify

`cd apps/api && uv run pytest tests -k speech`；在測試裡讓假的 Gemini 回 429，看回應代碼與帳上那筆的狀態。
