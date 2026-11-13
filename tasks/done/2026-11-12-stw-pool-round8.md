---
id: 2026-11-12-stw-pool-round8
title: 原來如此素材池第八輪：補後備缺口與新組長題
status: done
priority: P2
area: docs
owner: claude-cloud-pool-round8
claimed_at: 2026-11-12T01:35:01Z
created_at: 2026-11-12T01:34:59Z
completed_at: 2026-11-12T02:18:00Z
branch: claude/sleepy-rubin-3jpyl9
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第八輪：補後備缺口與新組長題

## Why

站主 2026-11-12：「繼續擴充」。後備長題都補過一輪了，這一輪只補點名缺的那一塊，並從池中既有核心新組長題；夠成一集的才成題，不為片長硬湊。

## Definition of done

- [x] wave58 批次、checkpoint-3838、reviews/material-20261111-round8.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 作者 F11 補 G01、G42、G38、G35 點名缺的來源；作者 F12 新組 8 組長題提案。
- [x] 兩位非作者覆核（V14、V15）重抓來源、重算片長。
- [x] 組進素材池：G01、G42、G38 升為可成題，新增 G610–G612，其餘留後備。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,838→3,859，可成題長題 65→71。新組長題作者自判 6 組、覆核只收 3 組：離題章節刪掉後多半只剩 7.3–7.8 分。等站主決定：行人人群（C4-02）用不用 2006 年朝覲事故的分析、G35 是否做長片、G42 是否改題。留後備的組題與各自的翻案條件在 reviews/material-20261111-round8.json 的 reserve_records（太陽風暴補兩份技術來源、咖啡補 Cameron 2020 全文與一份感官研究就可再評）。
