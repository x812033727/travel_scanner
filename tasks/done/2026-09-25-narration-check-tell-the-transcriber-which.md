---
id: 2026-09-25-narration-check-tell-the-transcriber-which
title: Narration check: tell the transcriber which English words a line says, and let sentence-final particles pass
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-25T07:09:15Z
created_at: 2026-09-25T07:09:07Z
completed_at: 2026-09-25T07:15:45Z
branch: claude/video-check-hints
depends_on: []
scope:
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_speech_check.py
  - tools/video/tts/check.mjs
  - tools/video/tts/client.mjs
  - tools/video/tts/check.test.mjs
---

# Narration check: tell the transcriber which English words a line says, and let sentence-final particles pass

## Why

`check-audio` 用 Gemini 把每句旁白轉成文字，再跟腳本比對。2026-09-25 第二批的前兩支出了兩類誤判：

- **英文單字被聽成中文字**：ChatGPT 那支 22 句被標，其中 11 句是單獨的「Go」被轉寫成狗、各、購、夠。轉寫器只拿到音檔，不知道這句有英文字，Jev 看到「付錢的狗」自然判不對。語音辨識服務都收「詞彙提示」，就是為了這種情況。
- **台灣口語的句尾詞**：Google 學生方案那支有 3 句只差一個「齁」「耶」「餒」。站主 2026-09-25 已經決定語氣詞保留，但工具的語氣詞清單沒有這三個字。

## Definition of done

- [x] 轉寫請求帶上這句的英文字，轉寫器照腳本拼法寫。
- [x] 句中的「齁」、句尾多出來的「耶」「餒」算語氣詞；腳本本身以「氣餒」結尾時，少了「餒」仍然會被標。

## Steps

- [x] API：`TranscribeIn.terms`，最多 20 個。每個詞只能是拉丁字母、數字和 `.+#'_-`，不能有空格，所以提示組不出句子。`checking.transcribe` 在指示後面附上提示清單。
- [x] 工具：`hintTerms(line)` 從唸出來的文字取英文字；只有這句有英文字時才送 `terms`，所以舊伺服器照常可用。快取記下用了哪些提示，提示不同就重新轉寫：舊快取裡有英文字的句子會重做一次。
- [x] 語氣詞：`齁` 加進清單；`耶`、`餒` 只從聽到的文字句尾拿掉。

## How to verify

- `cd apps/api && uv run pytest tests/test_video_speech_check.py`：5 個測試通過，包含提示進了指示、端點轉交提示、6 種不合格的提示回 422。
- `node --test tools/video/tts/check.test.mjs`：9 個測試通過，包含提示清單、語氣詞，以及舊快取裡有英文字的句子會重新轉寫。
- 部署後，對 ChatGPT 那支重跑 `check-audio`：原本被標的 Go 句子應該轉寫成 Go。

## Notes

- API 要先部署，工具才會送 `terms`（`TranscribeIn` 是 `extra="forbid"`）。沒有英文字的句子不送這個欄位，所以工具先更新也不會壞。
- 提示只影響英文字怎麼拼。如果聲音真的漏唸某個字，轉寫出來還是會少那個字，照樣會被標。
