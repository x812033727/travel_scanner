---
id: 2026-10-26-merge-curio-f-and-g-topics
title: Merge curio F and G topics into topics.json
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-26T13:43:59Z
completed_at:
branch:
depends_on:
  - 2026-10-18-curio-s-axis-pilot-s01-red
  - 2026-10-26-curio-f-and-g-axes-fairy
scope:
  - docs/videos/history-curiosity/topics.json
  - docs/videos/history-curiosity/topics-fg.json
---

# Merge curio F and G topics into topics.json

## Why

奇聞檔案局 F、G 兩軸的 61 題 2026-10-26 先放在 `docs/videos/history-curiosity/topics-fg.json`，因為 `topics.json` 還在
`2026-10-18-curio-s-axis-pilot-s01-red` 的 scope 裡。題庫應該只有一份。

## Definition of done

- [ ] `topics.json` 的 `topics` 多了 F01–F38、G01–G23（含查核過後改的 `status` 與 `note`），`series.axes` 有 F、G，`note` 寫第四批的來歷。
- [ ] `topics-fg.json` 刪掉；`docs/videos/history-curiosity/README.md` 指向它的地方改指 `topics.json`（README 不在這張的 scope，要嘛加進 scope，要嘛另開一張小票）。

## Steps

- [ ] 等 S01 試片那張結案（或它的 scope 不再含 `topics.json`）。
- [ ] 用腳本合併，確認 id 不重複、題數 224 + 61。

## How to verify

`python3 -c "import json,collections;d=json.load(open('docs/videos/history-curiosity/topics.json'));print(collections.Counter(t['axis'] for t in d['topics']))"` 有 F 38、G 23（或查核後的數字）。

## Notes

這張票由 `2026-10-26-curio-f-and-g-axes-fairy` 拆出來。
