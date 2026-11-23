---
id: 2026-11-12-stw-pool-round11
title: 原來如此素材池第十一輪：補讀後備組題與只讀到摘要的核心
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round11
claimed_at: 2026-11-12T05:01:25Z
created_at: 2026-11-12T05:01:23Z
completed_at: 2026-11-12T05:38:13Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第十一輪：補讀後備組題與只讀到摘要的核心

## Why

站主 2026-11-12：「繼續擴充」。只補讀新來源；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave61 批次、checkpoint-3907、reviews/material-20261111-round11.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F17 補 C5-02、C6-02；作者 F18 重讀 C7-01 觸覺、C7-02 動物視覺。
- [x] 兩位非作者覆核（V20、V21）重抓來源、重算片長。
- [x] 組進素材池：新增 G621，其餘留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,907→3,921，可成題長題 79→80。後備的補法：C6-02 差 0.5 條（一份 10–30 µm 小滴碰撞效率的實驗全文，或非 Rosenfeld 研究群的暖雨起始研究）；C7-01 差約 2.4 條（Gori 2021 全文已快取但只讀摘要、Röder 2004、Azañón 2018）；C7-02 差約 2–2.5 條（重讀 Z7010、B2315，加一份開放的行為實驗）。CLI 一次連跑多個 `show` 即使各加 timeout 也會超過前景 120 秒：之後一律直接讀 pool.json。
