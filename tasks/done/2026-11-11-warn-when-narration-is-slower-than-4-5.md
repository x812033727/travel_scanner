---
id: 2026-11-11-warn-when-narration-is-slower-than-4-5
title: 影片工具：旁白語速低於 4.5 字／秒時警告（奇聞、原來如此）
status: done
priority: P2
area: tools
owner: claude-opus-5.5-p06-p18-handoff
claimed_at: 2026-11-11T02:34:33Z
created_at: 2026-11-11T01:41:35Z
completed_at: 2026-11-11T03:10:26Z
branch:
depends_on: []
scope:
  - tools/video/core/pace.mjs
  - tools/video/core/pace.test.mjs
  - tools/video/tts/cli.mjs
---

# 影片工具：旁白語速低於 4.5 字／秒時警告（奇聞、原來如此）

## Why

`pace-targets.md` 與原來如此 SCORECARD 的規則：奇聞檔案局、原來如此事務所旁白語速 ≥ 4.5 字／秒（2026-10-25 量黑貓研究院 5.06）。
目前沒有任何工具檢查語速，PR #2069 也只改停頓。

P06（2026-11-11 量 `timeline.json`）：只算說話的時間 3.74 字／秒，整支 3.16 字／秒。配音提示詞寫「一秒四到五個字」，但 Gemini 實際講不到。
原來如此的 `build_scenes.py` 估片長還在用 3.2 字／秒，跟規則矛盾，所以稿子寫得剛好、片長也剛好，但語速一直偏慢。

## Definition of done

- [x] `tts` 之後（或 `lint` 讀得到 `timeline.json` 時），curio-／sothatswhy- 的影片算出每秒字數（只算說話的取樣，不含停頓），低於 4.5 就警告，寫出實際數字。
- [x] 中文字數的算法與 `build_scenes.py` 的估算一致（只數漢字），並在說明裡寫清楚。
- [x] 警告文字說明兩條路：調配音的語速設定，或請站主調整目標；不自動改已核准的旁白。

## Steps

- [x] 寫 `tools/video/core/pace.mjs`：從 timeline（`lines[].audio_samples`、`sample_rate`）和 video.json 的台詞算字數／秒。
- [x] 接到 lint 的警告（或 `tts` 結尾印出），加測試（快、慢、非這兩個系列不警告）。
- [x] 查 Gemini 配音有沒有可調的語速參數（`voice.style` 之外），結果寫在 Notes。

## How to verify

`node --test tools/video/core/pace.test.mjs`；對 P06 的 timeline 算 `paceWarning` 應出現「語速 3.7 字／秒，低於 4.5」的警告。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 接在 PR #2069（票 `2026-11-11-series-default-tight-pauses-and-beat`，在那個 PR 的分支上）之後做。
- 2026-11-11：從 PR #2069 的檢查拆出來。要調快到 4.5 還是接受較低的目標，是站主的決定；這張票只負責量出來、提醒。
- 2026-11-11（claude-opus-5.5-p06-p18-handoff）：站主決定「之後都調快」（目標 4.5）。`tools/video/core/pace.mjs`（只數漢字，跟 build_scenes 一致；
  秒數只算錄音 `audio_samples`，不含停頓），`tts` 結尾對 curio-／sothatswhy- 低於 4.5 時印 `pace:` 警告、不讓指令失敗。放在 tts 而不是 lint：lint 時還沒有錄音，
  而且 `core/lint.mjs` 在一張舊票（2026-10-24-manga-sticker-drama-pace-visible-camera，review）的範圍裡。認領時 `--force`：tts/cli.mjs 也在兩張十月的舊認領範圍裡。
- **Gemini 沒有語速參數**（`requests.mjs` `voiceFields`：只送 voice、style、model），速度只能寫在 style。用 P06 全稿、只換 style 實測（Sulafat 所長＋Leda 小問）：
  - 原本「語速像平常聊天，一秒四到五個字，句與句之間不拖。」→ 3.74 字／秒，check-audio 第一輪 28 句
  - b「語速偏快、輕快，像節目主持人，一秒五個字以上，句與句緊接、不拖長尾音。」（小問加「，一秒五個字以上，不拖尾音」）→ 4.39，24 句
  - c「說得很快很輕快，像趕著把話說完的 YouTuber，一秒六個字，句子之間完全不停、尾音不拖。」（小問加「，說得很快，一秒六個字，不拖尾音」）→ 4.95，32 句
  三段開頭 45 秒已交站主試聽；站主選定後把那句寫進系列範本（原來如此 README §4、奇聞的 voice 設定）。
