---
id: 2026-11-11-sothatswhy-line-pauses-via-pauses-line-ms
title: 原來如此事務所：句間停頓交給 pauses.line_ms，只在答案前留一拍
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-11-11T01:41:34Z
completed_at:
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

- [ ] 新一集原來如此的 `build_scenes.py` 不再每句寫 `pause_after_ms`；句間由 `video.json` 的 `pauses.line_ms` 決定。
- [ ] 答案揭曉前那一句（小問說出答案前、所長揭曉前）留一拍：只在那幾句寫 `pause_after_ms`（建議 400–600 毫秒，先試）。
- [ ] `dialogue-pilot-20261103/README.md` 的範本說明寫進這兩條，並註明已核准的舊集不重做。
- [ ] 下一集成片量 `silent_share` ≤ 3%、沒有 1.5 秒以上的空檔。

## Steps

- [ ] 找出範本裡寫 `pause_after_ms=100` 的地方（`k()`／`c()` 或 `_shot`），改成預設不寫，加一個標記答案前一拍的寫法（例如 `tag="beat"`）。
- [ ] 改 README 的〈怎麼做一集〉與已知的坑。
- [ ] 下一集照做後量測，結果寫回這張票。

## How to verify

```bash
node .agents/skills/youtube-video/scripts/reference_analysis.mjs --file ~/mokaair-work/videos/<slug>/final.mp4 --range 0-180 --range 300-480 --out /tmp/pace.json
```
看兩段的 `sound.silent_share` ≤ 0.03；`timeline.json` 相鄰兩句之間沒有 ≥ 1.5 秒的空檔。

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.

- 接在 PR #2069（票 `2026-11-11-series-default-tight-pauses-and-beat`，在那個 PR 的分支上）之後做。
- 2026-11-11：從 PR #2069 的檢查拆出來（站主要求開票）。範本在各集的 `build_scenes.py`，這張票只改範本說明；實際改的是下一集自己的 builder（那一集的票 scope）。
