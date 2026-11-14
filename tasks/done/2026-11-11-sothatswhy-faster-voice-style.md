---
id: 2026-11-11-sothatswhy-faster-voice-style
title: 原來如此事務所：配音 style 改成站主選的偏快版本，語速門檻 4.3
status: done
priority: P2
area: docs
owner: claude-opus-5.5-p06-p18-handoff
claimed_at: 2026-11-11T03:33:56Z
created_at: 2026-11-11T03:33:46Z
completed_at: 2026-11-11T03:34:47Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/dialogue-pilot-20261103
  - tools/video/core/pace.mjs
  - tools/video/core/pace.test.mjs
  - .agents/skills/producer/references/pace-targets.md
  - docs/videos/lessons/sothatswhy.md
---

# 原來如此事務所：配音 style 改成站主選的偏快版本，語速門檻 4.3

## Why

站主 2026-11-11「之後都調快」，聽過 P06 三種 style 的試聽（3.74／4.39／4.95 字／秒）後選了 4.39 那種（試聽檔 2）。要把那句 style 寫進原來如此的範本，並讓 `tts` 的語速警告以這個為準，不要每集都對站主選的速度發警告。

## Definition of done

- [x] 新一集照 dialogue-pilot README §4 寫兩個角色的 style。
- [x] `pace.mjs` 分系列門檻：原來如此 4.3、奇聞 4.5（奇聞的聲音沒測過，不動）。
- [x] `pace-targets.md` 的語速列、教訓檔更新。

## Steps

- [x] 改 pace.mjs 與測試（5/5）。
- [x] 改 README §4、pace-targets.md、lessons/sothatswhy.md；刪掉試聽用的 zz-rate-test-b／c。

## How to verify

`node --test tools/video/core/pace.test.mjs`；下一集 `tts` 結尾的語速 ≥ 4.3 時不印 `pace:`。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
- 2026-11-11：style 要寫得比目標快：寫「一秒五個字以上」實際只到 4.39，寫「一秒六個字」才到 4.95。認領時 `--force`：dialogue-pilot 資料夾在 P02 那張沒結案的舊票範圍裡。
