---
id: 2026-11-19-extend-curio-wave-88-and-so
title: Extend Curio wave 88 and So Thats Why wave 117 on PR 2177
status: done
priority: P2
area: docs
owner: codex-pools
claimed_at: 2026-11-19T06:04:18Z
created_at: 2026-11-19T06:04:13Z
completed_at: 2026-11-19T06:33:33Z
branch: codex/curio86-why115
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Extend Curio wave 88 and So Thats Why wave 117 on PR 2177

## Why

在同一個 PR #2177 接續奇聞第 87 批與原來如此第 116 批，補上實際查得到來源的新題。

## Definition of done

- [x] 兩池皆新增可追溯來源、獨立覆核與去重紀錄。
- [x] 可獨立成集的奇聞與原來如此長題皆有觀眾評分，原有入選資料可查。

## Steps

- [x] 核對原分支與兩池基準，同步主分支的新製作檔以重建最新索引。
- [x] 統整新題卡、候補與評審紀錄。
- [x] 重建兩池搜尋頁及後台，驗證新題、來源、選題與片單。

## Result

奇聞第 88 批入選五題，另保留一個章節，入選總數達 1,805。金栗四三與楊傳廣兩題改寫的校正分提升達到 0.50，採用新版。原來如此第 117 批收錄 35 張素材，入選總數達 7,182。G760 原研究稿併分 8.13，新增一組可成題長片，可成題數達 105。

桌面與手機尺寸已驗證可搜尋本批 6 張奇聞、35 張原來如此題卡及篩選 G760。既有入選 ID 與順序完整保留，舊題案內容僅隨全池重排名次與母數。後台資料包與兩池數字一致。

兩池建置檢查及 67 項 Node、4 項語意索引、92 項 API 測試通過。

## How to verify

```sh
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node tools/video/pool-admin/bundle.mjs check
node --test tools/video/{curio,so-thats-why}/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```
