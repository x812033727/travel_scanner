---
id: 2026-11-12-curio-pool-wave27
title: 奇聞檔案局素材池第二十七批
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round7
claimed_at: 2026-11-12T00:34:45Z
created_at: 2026-11-12T00:34:43Z
completed_at: 2026-11-12T01:24:13Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
---

# 奇聞檔案局素材池第二十七批

## Why

站主 2026-11-12：「繼續擴充」。奇聞檔案局再補一批新題，去重、整理來源，太薄或無聊的合併或淘汰，不為片長硬湊。

## Definition of done

- [x] batches/wave27-20261112.json 與 reviews/wave27-review-20261112.json 入庫，`cli.mjs check` PASS，pool.test.mjs 全過。

## Steps

- [x] 四個研究代理（M1–M4：U 解密檔案、P 預言版本史、L 寶藏與傳說地點、M 傳說動物）先去重再實讀來源。
- [x] 四位非作者覆核（R271–R274）逐題重開關鍵來源，改動寫成完整欄位。
- [x] 組批、更新 selection 與 README，跑語意近鄰。

## How to verify

`node tools/video/curio/pool/cli.mjs check`（PASS）與 `node --test tools/video/curio/pool/pool.test.mjs`（23 過）。

## Notes

入選 894→914；退回 N2921 Parime 湖（委內瑞拉與蓋亞那的爭議領土）；暫緩 N2885（納粹飛碟傳說，等站主決定）；待查 N2943（gorilla 的名字，要站主先決定走法）、N2946、N2927。素材池搜尋每個關鍵字要 30 秒到 2 分鐘而且會漏，研究代理實際上都靠 grep pool.json 與批次檔去重。下一批可專人補：王懿榮與甲骨文、Project Magnet、Mu 大陸。
