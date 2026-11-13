---
id: 2026-11-12-curio-pool-wave29
title: 奇聞檔案局素材池第二十九批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round9
claimed_at: 2026-11-12T02:29:45Z
created_at: 2026-11-12T02:29:44Z
completed_at: 2026-11-12T03:24:26Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第二十九批

## Why

站主 2026-11-12：「繼續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave29-20261112.json 與 reviews/wave29-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（J1–J4：未完成的線索、M 天空與天氣、P 被說成預言的舊文字、F 童謠與俗語的起源說）先去重再實讀來源。
- [x] 四位非作者覆核（R291–R294）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、成題（T125、T126、T127）、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 937→960（含 N2964 移出暫緩）；暫緩 N3044、N3066；待查 N3103（年獸）、N3088。組批腳本曾把第二十七、二十八批的覆核收據寫到第二十六批的檔名上，本輪開工時已還原並補檔；之後組批要確認收據檔名跟批次一致。覆核的素材池搜尋一律前景加 timeout，不放背景。
