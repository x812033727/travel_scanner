---
id: 2026-11-19-curio-wave85-rechecks-and-stw-g746
title: Curio wave85 rechecks and STW G746 redo
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-19T02:12:26Z
created_at: 2026-11-19T02:12:10Z
completed_at: 2026-11-19T02:12:27Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave85 rechecks and STW G746 redo

## Why

站主 2026-11-19 在 PR #2174 之後選了兩件事：「補查第八十五批待查」「重做 G746 研究」。

## Definition of done

- [x] 第八十五批的 11 題待查都已補查並經非作者覆核：7 題收（N7885 入選，6 題暫緩），1 題仍待查，3 題不收並寫重開條件。
- [x] G746 重做研究，覆核判 ready，新片名定稿觀眾分 7.33，已入選並登記進備份分類表。

## Steps

- [x] 補查 ZV0–ZV2，覆核 R8510–R8512。
- [x] N7885 單集題另評一次分（六題錨點加 8 題對照題）。
- [x] 補研究 SY6D、覆核 SVY6D、最終評分與需求四問。
- [x] 寫進批次檔、更新 selection 與 README，刪掉 #2174 誤帶的 1 位元組空檔。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
```

## Notes

- N7885 總分 5.77，照 N7668 前例保留入選。
- N7887 奴才：下一輪讀 archive.org 清稗類鈔 jp2 逐頁影像的〈稱謂類〉。
- G746 前兩輪 5.87、5.62 都卡在來源太像規格書；改用消費者機構的實測個案後過線。
