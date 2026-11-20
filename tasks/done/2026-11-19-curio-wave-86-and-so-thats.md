---
id: 2026-11-19-curio-wave-86-and-so-thats
title: Curio wave 86 and So Thats Why wave 115 reviewed topic expansion
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T04:33:52Z
created_at: 2026-11-19T04:33:48Z
completed_at: 2026-11-19T05:04:37Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave 86 and So Thats Why wave 115 reviewed topic expansion

## Why

接續奇聞第 85 批與原來如此第 114 批，補入可回溯到館藏、同期紀錄、實驗或技術規格的新題；用兩池既有核心比對，保留退回理由。

## Definition of done

- [x] 兩池都有新增、經非作者查過來源的題卡，並在搜尋頁與後台顯示。
- [x] 單集題及新長片題案附獨立觀眾評分，章節素材明列用途。

## Steps

- [x] 核對主線批次、跨池同案和來源定位。
- [x] 將通過覆核的題卡、評分和片案寫入正式資料並重建索引。
- [x] 驗證資料包、搜尋與相關測試。

## How to verify

```sh
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
node --test tools/video/{curio,so-thats-why}/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```

## Notes

- 奇聞入選 1,793 → 1,796，另收兩題章節。三個單集的併分為 7.02、7.39、6.51。
- 原來如此入選 7,078 → 7,102。六張日常段落與十八張照片卡各有可定位來源。G757 定稿併分 6.43，維持後備。LINE 測試只涵蓋當時的聊天室照片路徑，未測現版文件模式。
- 兩池與後台資料檢查通過，67 項 Node 測試、4 項 Python 語意索引測試及 92 項後台與備份測試通過。桌機及手機視窗皆能查出新卡並篩出 G757 的 18 張素材。
