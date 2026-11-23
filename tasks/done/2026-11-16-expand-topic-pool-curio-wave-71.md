---
id: 2026-11-16-expand-topic-pool-curio-wave-71
title: Expand topic pool: Curio Wave 71 & So-That's-Why Wave 102
status: done
priority: P2
area: docs
owner: antigravity
claimed_at: 2026-11-16T16:00:06Z
created_at: 2026-11-16T16:00:01Z
completed_at: 2026-11-16T16:48:54Z
branch: topic-pool-wave71-wave102
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_backup/target.py
  - apps/api/app/video_pools/data/pools.json
---

# Expand topic pool: Curio Wave 71 & So-That's-Why Wave 102

## Why

持續擴充奇聞檔案局（Curio）與原來如此事務所（So-That's-Why）題庫素材池：
1. 奇聞檔案局 Wave 71：入選達 1,839 題，新增 17 題採納（S 軸古典與近代物理化學重大發現公案 N7061–N7080），3 題暫緩（N7065、N7070、N7075）。
2. 原來如此事務所 Wave 102（第五十二輪）：凍結 6,149 題基準點（checkpoint-6149.json），新增 56 題候選（K102-001–K102-056），入選達 6,205 題；新增 3 輯長題組 G707、G708、G709，雙輪受眾覆核達標（>= 8.05 分）。
3. 雲端備份目標 target.py 登記 G707、G708、G709，並完成 pools.json 重新打包。

## Definition of done

- [x] 奇聞檔案局 Wave 71 批次與覆核入池，入選達 1,839 題，`cli.mjs check` 通過，27 項單元測試全數通過。
- [x] 原來如此事務所 Wave 102 批次、覆核、長題組 G707–G709 入池，入選達 6,205 題，`cli.mjs check` 通過，38 項單元測試全數通過。
- [x] `apps/api/app/video_backup/target.py` 正確登記 G707、G708、G709，pytest 測試通過。
- [x] `pools.json` 通過 bundle.test.mjs。
- [x] `npm run check:tasks` 通過。

## Steps

- [x] 原來如此 6,149 題 baseline 凍結（baselines/2026-11-16-6149.json.gz）與 checkpoint-6149.json 建立。
- [x] 奇聞 Wave 71 批次撰寫、覆核與 build。
- [x] 原來如此 Wave 102 批次（4 批共 56 題）、長題組 G707–G709、雙輪審稿覆核與 build。
- [x] 雲端備份目標 target.py 與 pools.json 登記。
- [x] 全套驗證測試（Curio, STW, video_backup, video_pools, check:tasks）。

## How to verify

- `node tools/video/curio/pool/cli.mjs check`
- `node --test tools/video/curio/pool/pool.test.mjs`
- `node tools/video/so-thats-why/pool/cli.mjs check`
- `node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`
- `node --test tools/video/pool-admin/bundle.test.mjs`
- `cd apps/api && uv run pytest tests/test_video_backup.py tests/test_video_pools.py`
- `npm run check:tasks`

## Notes

- 嚴格遵守各系列去重機制與規範：Curio 避免同案題目與 STW 題目交叉重疊；STW 來源保持完整 publisher/version/rights 標註。
- 長題組三組（G707–G709）依兩輪評審規則評分改進達標（門檻 6.5）。
