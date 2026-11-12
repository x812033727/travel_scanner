---
id: 2026-11-12-curio-pool-wave40
title: 奇聞檔案局素材池第四十批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round20
claimed_at: 2026-11-12T11:30:37Z
created_at: 2026-11-12T11:30:37Z
completed_at: 2026-11-12T13:01:25Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第四十批

## Why

站主 2026-11-12：「持續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave40-20261112.json 與 reviews/wave40-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 十個研究代理（U1–U10）先去重再實讀來源。
- [x] 十位非作者覆核（R401–R410）逐題重開關鍵來源，並逐筆讀工具紀錄。
- [x] 組批、更新 selection、README 與 dedup-decisions（9 組字面近鄰判不同），跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 1156→1191；暫緩 N4264、N4283；待查 6 題。三位研究代理違反網址規則（U7 自打維基文庫書名頁、U3 自打 Gutenberg 搜尋頁、U2 兩次讀書名頁），U7 的五筆來源移除、由覆核重取取代；另刪 U9 的第三方全文轉貼。N4204 Aurora 的主權疑慮留給站主決定。wave41 O4 的 N4385 是 N4265 的重複，新讀的 1930 年來源記在 R414 的 merge_notes，整合 wave41 時併進 N4265。
