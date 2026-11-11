---
id: 2026-11-11-warn-when-narration-is-slower-than-4-5
title: 影片工具：旁白語速低於 4.5 字／秒時警告（奇聞、原來如此）
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-11T01:41:35Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/pace.mjs
  - tools/video/core/pace.test.mjs
  - tools/video/core/lint.mjs
---

# 影片工具：旁白語速低於 4.5 字／秒時警告（奇聞、原來如此）

## Why

`pace-targets.md` 與原來如此 SCORECARD 的規則：奇聞檔案局、原來如此事務所旁白語速 ≥ 4.5 字／秒（2026-10-25 量黑貓研究院 5.06）。
目前沒有任何工具檢查語速，PR #2069 也只改停頓。

P06（2026-11-11 量 `timeline.json`）：只算說話的時間 3.74 字／秒，整支 3.16 字／秒。配音提示詞寫「一秒四到五個字」，但 Gemini 實際講不到。
原來如此的 `build_scenes.py` 估片長還在用 3.2 字／秒，跟規則矛盾，所以稿子寫得剛好、片長也剛好，但語速一直偏慢。

## Definition of done

- [ ] `tts` 之後（或 `lint` 讀得到 `timeline.json` 時），curio-／sothatswhy- 的影片算出每秒字數（只算說話的取樣，不含停頓），低於 4.5 就警告，寫出實際數字。
- [ ] 中文字數的算法與 `build_scenes.py` 的估算一致（只數漢字），並在說明裡寫清楚。
- [ ] 警告文字說明兩條路：調配音的語速設定，或請站主調整目標；不自動改已核准的旁白。

## Steps

- [ ] 寫 `tools/video/core/pace.mjs`：從 timeline（`lines[].audio_samples`、`sample_rate`）和 video.json 的台詞算字數／秒。
- [ ] 接到 lint 的警告（或 `tts` 結尾印出），加測試（快、慢、非這兩個系列不警告）。
- [ ] 查 Gemini 配音有沒有可調的語速參數（`voice.style` 之外），結果寫在 Notes。

## How to verify

`node --test tools/video/core/pace.test.mjs`；對 P06 跑 `node tools/video/cli.mjs lint --slug sothatswhy-p06-bubble-film` 應出現「語速 3.7 字／秒，低於 4.5」的警告。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 接在 PR #2069（票 `2026-11-11-series-default-tight-pauses-and-beat`，在那個 PR 的分支上）之後做。
- 2026-11-11：從 PR #2069 的檢查拆出來。要調快到 4.5 還是接受較低的目標，是站主的決定；這張票只負責量出來、提醒。
