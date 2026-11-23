---
id: 2026-11-11-stw-pool-round5
title: 原來如此素材池第五輪：補後備長題缺的來源
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T15:32:52Z
created_at: 2026-11-11T15:32:45Z
completed_at: 2026-11-11T16:36:36Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池第五輪：補後備長題缺的來源

## Why

站主 2026-11-11 再次說「繼續擴充池」：原來如此事務所補後備長題缺的來源，夠成一集的才升為可成題，不為片長硬湊。

## Definition of done

- [x] 新批次、檢查點與 reviews/material-20261111-round5.{json,md} 入庫，`cli.mjs check` PASS，pool.test.mjs 與 catalog.test.mjs 全過。

## Steps

- [x] 兩個研究代理（F5：G18、G34、G25、G03；F6：G02、G10、G23、G07）照各題 missing 補讀來源。
- [x] 兩位非作者覆核（V8、V9）重開來源、重算片長。
- [x] 組進素材池，夠 8.5 分鐘的升為可成題，其餘留後備並寫明缺什麼。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`、`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（32 過）。

## Notes

入選 3,661→3,733，可成題長題 46→54（G18、G34、G25、G03、G02 改名、G07、G10、G23）。覆核抓到研究者自己算錯的倍數（F5-001）、從料號自行解讀的規格（F5-008）、把兩段 EPA 原文寫成一條追蹤到底的迴圈（F6-042）、仍用到 G48 的例子（G02）。E7006 錯掛來源另開票 2026-11-11-stw-pool-e7006-source-ref。
