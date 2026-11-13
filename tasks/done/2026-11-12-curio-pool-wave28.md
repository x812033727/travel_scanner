---
id: 2026-11-12-curio-pool-wave28
title: 奇聞檔案局素材池第二十八批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round8
claimed_at: 2026-11-12T01:35:00Z
created_at: 2026-11-12T01:34:58Z
completed_at: 2026-11-12T02:25:35Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第二十八批

## Why

站主 2026-11-12：「繼續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave28-20261112.json 與 reviews/wave28-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（Q1–Q4：U 被讀成 UFO 的古文獻、G 歐陸與俄國鬧鬼案、H 發現故事、L 被發明的失落之地）先去重再實讀來源。
- [x] 四位非作者覆核（R281–R284）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題（T122、T123、T124）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 914→937；退回 N2988（單一系譜）；暫緩 N2964、N3026（只撐得起一章，等站主決定）；待查 N2965。N3022 Lemuria 的最後一段旁白稿上稿前要請站主看過。池中 N2443 的「1879 年」與 Sclater 1864 年原文不合，另開票 2026-11-12-curio-n2443-lemuria-year。覆核代理在背景跑的素材池搜尋會掛住沒回，整批完成後要 pkill 清掉。
