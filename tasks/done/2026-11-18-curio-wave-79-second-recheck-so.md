---
id: 2026-11-18-curio-wave-79-second-recheck-so
title: Curio wave 79, second recheck, so-that's-why expansion G710–G716
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-18T04:34:12Z
created_at: 2026-11-18T04:34:06Z
completed_at: 2026-11-18T04:34:24Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave 79, second recheck, so-that's-why expansion G710–G716

## Why

站主 2026-11-18 選「再擴一批奇聞」「補待查」「原來如此擴充」，OpenStax 只處理可成題用到的。

## Definition of done

- [x] 第七十六～七十八批待查二次補查寫進各批 `recheck` 欄位與收據（9/14 補到，N7536、N7514 不收）。
- [x] 原來如此 G710–G716 七組新長題案，112 張實讀新卡，觀眾分全部過 6.5，可成題 56 → 63。
- [x] 可成題 OpenStax 清查：只有 G26 受影響，拿掉後仍 13.0 條。
- [x] 奇聞第七十九批：40 個方向研究覆核，32 收、4 待查、4 不收；17 入選、14 題過 6.5。
- [x] 新題登記進備份分類表（`apps/api/app/video_backup/target.py`）。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node --test tools/video/so-thats-why/pool/pool.test.mjs
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```

## Notes

- N7574 昆池岩：只剩「全國性日報轉述政府帳冊」一條路，等站主決定這類來源可不可用。
- 仍待查：N7560、N7574、N7543（第七十六～七十八批），N7626、N7653、N7655、N7658（第七十九批）。
- G714 只比素材門檻多 0.1 條，開拍前補 QR 破損實測的獨立來源；G711 不可把單一城市做法講成全國規定。
- 新增原來如此長題案時，要同時登記進 `apps/api/app/video_backup/target.py` 的 `SOTHATSWHY_CODES_BY_CATEGORY`，否則 `tests/test_video_backup.py` 會紅。
