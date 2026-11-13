---
id: 2026-11-11-stw-pool-e7006-source-ref
title: 原來如此素材池：E7006 合併帶進錯掛的來源，素材池沒有移除單一來源引用的機制
status: done
priority: P2
area: tools
owner: antigravity
claimed_at: 2026-11-13T03:43:00Z
created_at: 2026-11-11T16:36:25Z
completed_at: 2026-11-13T03:53:11Z
branch: claude/pool-expansion-20261113
depends_on: []
scope:
  - tools/video/so-thats-why/pool
  - docs/videos/so-thats-why/pool
---

# 原來如此素材池：E7006 合併帶進錯掛的來源，素材池沒有移除單一來源引用的機制

## Why

第五輪覆核發現 SRC-f2de49ac9ccccc6e（NPS 冰楔與熱融湖頁）掛在 E7006 上，跟它的答案無關。來源不在 E7006 自己的批次，而是 2026-11-01 dedup-decisions 把 E11012 併進 E7006 時帶進來的（合併的核心保留所有成員的來源）。素材池目前沒有移除單一舊來源引用的機制：source_merges 只能把新讀到的內容掛到既有來源，raw_changes 只記批次凍結前的修正。細節見 docs/videos/so-thats-why/pool/reviews/material-20261111-round5.json 的 open_data_issues 與 S55-NA005。E7006 只在短題 G76、G120，不在任何可成題長題或企劃的 POOL_SUPPORT。

## Definition of done

- [x] E7006 的 source_refs 不再含 SRC-f2de49ac9ccccc6e（或 E11012 的合併改成 distinct），`cli.mjs check` 與 pool.test.mjs 仍全過。

## Steps

- [x] 判斷 E11012 併進 E7006 是否正確；不正確就改 dedup-decisions。
- [x] 若合併正確，在 tools/video/so-thats-why/pool 加一個有理由、有測試的「排除單一來源引用」決定（同步補上 `excluded_source_refs` 機制與單元測試，供日後合併核心仍需排除單筆錯掛來源時使用）。

## How to verify

```bash
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs show E7006
node tools/video/so-thats-why/pool/cli.mjs show E11012
node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs
```

## Notes

- **機制判定（`E11012` vs `E7006` 應為 `distinct`）**：
  - `E7006`（`wave7-earth.json`，用於 `G76` 第三章）回答「冰河早已離開，平原為什麼後來還會凹出一個池塘？」，核心機制是冰水沉積平原包埋脫離冰河的死冰塊、延遲融去後留下鍋穴（`SRC-2bc7ad5b83b3068d`，Grand Teton Potholes Turnout）。
  - `E11012`（`wave11-landforms.json`，用於 `G120` 第二章）回答「冰楔融掉以後，多邊形中央為什麼反而看起來變高？」，核心機制是永凍土多邊形邊界下方的冰楔退化導致邊緣下陷、中央相對變高的地形反轉（`SRC-f2de49ac9ccccc6e`，NPS Alaska Park Science 冰楔與熱融湖頁）。`E11012` 自己的原始 `notes` 已寫明「與E7006埋冰鍋穴不同」。
  - 2026-11-01 將 `E11012` 併入 `E7006` 後，不但讓 `E7006` 錯掛北極冰楔來源，也讓 `G120`（「凍土中央變高，是地面真的往上頂嗎？」）借用 `E7006` 時帶進無關的大提頓鍋穴來源。因此在 `dedup-decisions.json` 改判 `distinct`，`selection.json` 選入 `E11012`（4,860 → 4,861），`themes.json` 的 `G120` 直接引用 `E11012`。凍結快照 `checkpoint-2837.json`（`pool.test.mjs` 驗證第 11 版別名紀錄）不受影響；`validateCheckpoints` 亦通過（`E7006` 仍在入選集合中）。
- **單一來源引用排除機制（`excluded_source_refs`）**：
  - 票題同時指出素材池原本缺少移除單一來源引用的稽核機制。已在 `tools/video/so-thats-why/pool/core.mjs` 與 `render.mjs` 支援於 `dedup-decisions.json` 宣告 `excluded_source_refs`（欄位：`candidate_id`、`source_id`、必填 `reason`，以及選填 `origin`、`locator`），在 `DEDUP.md` 渲染公開稽核列，並在 `pool.test.mjs` 測試：成功排除並保留稽核紀錄、拒絕非 canonical `candidate_id`、拒絕未命中的懸空規則、拒絕把合格核心的最後一筆來源排空。
