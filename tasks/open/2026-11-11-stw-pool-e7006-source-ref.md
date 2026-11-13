---
id: 2026-11-11-stw-pool-e7006-source-ref
title: 原來如此素材池：E7006 合併帶進錯掛的來源，素材池沒有移除單一來源引用的機制
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-11T16:36:25Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/so-thats-why/pool
  - docs/videos/so-thats-why/pool/dedup-decisions.json
---

# 原來如此素材池：E7006 合併帶進錯掛的來源，素材池沒有移除單一來源引用的機制

## Why

第五輪覆核發現 SRC-f2de49ac9ccccc6e（NPS 冰楔與熱融湖頁）掛在 E7006 上，跟它的答案無關。來源不在 E7006 自己的批次，而是 2026-11-01 dedup-decisions 把 E11012 併進 E7006 時帶進來的（合併的核心保留所有成員的來源）。素材池目前沒有移除單一舊來源引用的機制：source_merges 只能把新讀到的內容掛到既有來源，raw_changes 只記批次凍結前的修正。細節見 docs/videos/so-thats-why/pool/reviews/material-20261111-round5.json 的 open_data_issues 與 S55-NA005。E7006 只在短題 G76、G120，不在任何可成題長題或企劃的 POOL_SUPPORT。

## Definition of done

- [ ] E7006 的 source_refs 不再含 SRC-f2de49ac9ccccc6e（或 E11012 的合併改成 distinct），`cli.mjs check` 與 pool.test.mjs 仍全過。

## Steps

- [ ] 判斷 E11012 併進 E7006 是否正確；不正確就改 dedup-decisions。
- [ ] 若合併正確，在 tools/video/so-thats-why/pool 加一個有理由、有測試的「排除單一來源引用」決定。

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
