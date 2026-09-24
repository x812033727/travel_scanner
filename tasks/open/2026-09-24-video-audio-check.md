---
id: 2026-09-24-video-audio-check
title: 旁白自動檢查：Gemini 轉寫每句、Jev 判斷有沒有唸錯
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-24T10:43:09Z
created_at: 2026-09-24T10:43:08Z
completed_at:
branch: claude/video-audio-check
depends_on: []
scope:
  - apps/api/app/video_speech
  - apps/api/tests/test_video_speech_check.py
  - apps/web/app/api/video/speech
  - tools/video/tts
  - tools/video/cli.mjs
---

# 旁白自動檢查：Gemini 轉寫每句、Jev 判斷有沒有唸錯

## Why

試作片〈AI 模型怎麼挑〉的旁白用 Gemini 的 Sulafat 合成好了，共 157 句、10 分 1 秒。原本的流程是站主在審聽頁逐句聽，再標出唸錯的句子。

2026-09-24 站主改成「正確與否給 Jev 判斷」。Jev（TypeSafe System One）只讀文字、聽不到聲音，所以要先把每句的音檔轉成文字，再讓 Jev 判斷。

## Definition of done

- [x] 伺服器 `POST /video/speech/transcribe`：用網站的 Gemini 金鑰和文字模型，把一句的 WAV 轉寫成繁體中文。
- [x] 伺服器 `POST /video/speech/judge`：一次最多 40 句，每句問 Jev「轉寫說的是不是稿子上的字」，回傳機率。每個請求只花一次 Jev 的每日額度。
- [x] 本機 `check-audio --slug S`：
  - 每句的音檔降到 16 kHz 送去轉寫，結果依音檔雜湊快取，重跑不會重送；
  - 忽略標點、空白與大小寫後逐字相同的句子，直接通過；
  - 其餘句子每個場景問 Jev 一次，低於門檻（預設 0.5）的寫進 `review/check-flags.json`，可以直接交給 `tts --redo`。
- [ ] 部署後，對試作片實際跑一次，把結果交給站主。

## Steps

- [x] API：`app/video_speech/checking.py`，以及 `admin_api.py` 的兩個端點與 schema。
- [x] Web：`/api/video/speech/transcribe`（本文上限放寬到 3 MB）、`/api/video/speech/judge`。
- [x] 本機：`tools/video/tts/check.mjs`、`wav.mjs` 的 `downsample`、`client.mjs` 的 `transcribeClip`／`judgeLines`、CLI 的 `check-audio`。
- [x] 測試：API 4 項、Web 路由 1 項、本機 3 項（含一次完整流程）。
- [ ] 合併、部署、對試作片跑一次。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_speech_check.py
node --test tools/video/tts/check.test.mjs
node tools/video/cli.mjs check-audio --slug ai-model-choice
```

## Notes

- Jev 官方說它英文最準，其他語言沒有公布數字；repo 的 `jev_cjk_autopilot_enabled` 預設關著，就是為了這一點。所以這裡：
  - 問題用英文寫，中文放在 state 裡；
  - 工具只回報 Jev 的機率，不會自己改稿；
  - 旁白的核准仍然由站主做。
- 轉寫本身也會出錯，例如同音字、英文字母有沒有空格、數字寫法。這些差異交給 Jev 判斷算不算唸錯；真正的漏字、多字、換字才會被標出來。
- 每日 Jev 額度（`JEV_DAILY_CALL_BUDGET`，預設 200）和新聞自動化共用。一支片大約需要場景數以內的呼叫次數。
