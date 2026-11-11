---
id: 2026-11-11-sothatswhy-line-pauses-via-pauses-line-ms
title: 原來如此事務所：句間停頓交給 pauses.line_ms，只在答案前留一拍
status: done
priority: P2
area: docs
owner: claude-opus-5.5-p06-p18-handoff
claimed_at: 2026-11-11T01:49:18Z
created_at: 2026-11-11T01:41:34Z
completed_at: 2026-11-11T01:50:35Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/dialogue-pilot-20261103
---

# 原來如此事務所：句間停頓交給 pauses.line_ms，只在答案前留一拍

## Why

`.agents/skills/producer/references/pace-targets.md` 的規則：兩個系列靜音 ≤ 3%，「拿掉句子之間的固定停頓，只在答案揭曉前留一拍」。
PR #2069 讓新集預設 `pauses: { line_ms: 0, scene_ms: 150 }`，但 `timeline.mjs` 是「每句自己的 `pause_after_ms` 優先」，
而原來如此事務所每一集的 `build_scenes.py`（P02、P05、P06、P07、P08、P14、P18，都從同一份範本複製）在每一句都寫 `pause_after_ms: 100`，
所以 `line_ms: 0` 對這個系列不會生效，每句仍停 0.1 秒；答案前也沒有比較長的一拍。

P06 成片實測（2026-11-11，`reference_analysis.mjs` 0–180、300–480 秒）：`silent_share` 7.1%／4.9%，最長空檔 0.83 秒。
照 #2069 的換景 150 毫秒估算會降到約 2.8%／1.9%（只靠換景，句間 0.1 秒還在）。

## Definition of done

- [x] 新一集原來如此的 `build_scenes.py` 不再每句寫 `pause_after_ms`；句間由 `video.json` 的 `pauses.line_ms` 決定。
- [x] 答案揭曉前那一句（小問說出答案前、所長揭曉前）留一拍：只在那幾句寫 `pause_after_ms`（建議 400–600 毫秒，先試）。
- [x] `dialogue-pilot-20261103/README.md` 的範本說明寫進這兩條，並註明已核准的舊集不重做。
- [x] 量測移到下一集的票：照 §10.6 做的第一集，成片量 `silent_share` ≤ 3%、沒有 1.5 秒以上的空檔，`BEAT_MS` 依結果調（§9「停頓」那列已寫成關卡）。

## Steps

- [x] 找出範本裡寫 `pause_after_ms=100` 的地方（`k()`／`c()` 或 `_shot`），改成預設不寫，加一個標記答案前一拍的寫法（例如 `tag="beat"`）。
- [x] 改 README 的〈怎麼做一集〉與已知的坑。
- [x] 下一集照做後量測（寫進 §9 的關卡，由那一集的票負責）。

## How to verify

```bash
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file ~/mokaair-work/videos/<slug>/final.mp4 --range 0-180 --range 300-480 --out /tmp/pace.json
```
看兩段的 `sound.silent_share` ≤ 0.03；`timeline.json` 相鄰兩句之間沒有 ≥ 1.5 秒的空檔。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 接在 PR #2069（票 `2026-11-11-series-default-tight-pauses-and-beat`，在那個 PR 的分支上）之後做。
- 2026-11-11：從 PR #2069 的檢查拆出來（站主要求開票）。範本在各集的 `build_scenes.py`，這張票只改範本說明；實際改的是下一集自己的 builder（那一集的票 scope）。
- 2026-11-11（claude-opus-5.5-p06-p18-handoff）：README §9 加「停頓」一列、新增 §10.6，附新一集 builder 的寫法：
  `video.json` 寫 `pauses: {line_ms: 0, scene_ms: 150}`、`still_motion: "beat"`；台詞不寫 `pause_after_ms`，只在 `P:` 那一句的前一句（同一景）寫 `BEAT_MS = 500`。
  拿 P06 的 builder 在暫存目錄試跑：一集 12 處留拍；句間＋換景停頓約 99 秒 → 約 23 秒，依 P06 量測比例估靜音約 7.1% → 約 2%（估算，未剪片）。
  main 的 `core/timeline.mjs` 已支援 `pauses`（`pausesOf`），不必等 PR #2069。已核准的 P02–P18 不重做。
  認領時用了 `--force`：`2026-11-03-sothatswhy-dialogue-pilot-p02`（P02 早已完成，票停在 review）與 `2026-11-10-drive-ai-drama-layout`（已以 #2057 合併）是沒結案的舊認領。
