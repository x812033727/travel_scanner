---
id: 2026-11-19-extend-curio-wave-89-and-so
title: Extend Curio wave 89 and So Thats Why wave 118 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T07:01:01Z
created_at: 2026-11-19T07:01:00Z
completed_at: 2026-11-19T07:29:05Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 89 and So Thats Why wave 118 on PR 2177

## Why

延續 PR #2177 的兩個系列，以新的來源與題材繼續擴池。

## Definition of done

- [x] 新題卡有可核對的來源及非作者覆核，入選前查兩池和既有退案。
- [x] 長題及奇聞單集經觀眾評估與複評。舊入選順序保留。

## Steps

- [x] 確認 PR 分支及既有入選基準。
- [x] 擴充奇聞第 89 批與原來如此第 118 批。
- [x] 重建、驗證搜尋及片單，推回原 PR。

## Result

奇聞新增 5 個單集，入選達 1,810 題。紙上錄音等 4 個重複提案保留舊 ID。原來如此新增 12 張日常、6 張出版編目與 18 張捷運素材，入選達 7,218 張。新長題 G761 同站進出以高捷公布的動線修正後複評，觀眾併分 6.83，成為第 106 組可成題長片。

桌面與手機尺寸均可搜尋本批全部 41 張題卡，並用 G761 篩出 18 張捷運素材。已核對原有入選 ID 與順序、既有題案內容與後台各項數字。

兩池檢查、67 項 Node 題庫／後台測試、4 項語意索引、92 項 API 與 261 項影片文件測試通過。

## How to verify


```sh
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
node --test tools/video/{curio,so-thats-why}/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```
