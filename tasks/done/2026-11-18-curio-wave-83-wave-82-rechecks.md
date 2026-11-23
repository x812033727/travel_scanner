---
id: 2026-11-18-curio-wave-83-wave-82-rechecks
title: Curio wave 83, wave 82 rechecks, so-that's-why G734-G740 and G727/G731 reinforcement
status: done
priority: P2
area: docs
owner: claude-heimao-topics
claimed_at: 2026-11-18T13:29:19Z
created_at: 2026-11-18T13:29:02Z
completed_at: 2026-11-18T13:29:20Z
branch:
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools/data
  - apps/api/app/video_backup/target.py
---

# Curio wave 83, wave 82 rechecks, so-that's-why G734-G740 and G727/G731 reinforcement

## Why

站主 2026-11-18 合併 PR #2163 後選：再擴一批奇聞、補查第八十二批待查、補強 G727 與 G731、原來如此再擴充。

## Definition of done

- [x] 第八十二批待查：N7745、N7754、N7762、N7771 升可收（一章、暫緩），N7781 可單獨成集並評分入選，N7756、N7759 暫不收，N7749 仍待查。
- [x] 奇聞第八十三批：40 個方向研究覆核，23 收、11 待查、6 不收；6 題單集題加 N7781 入選（7 題全過 6.5），17 題一章暫緩。
- [x] 原來如此 G727（11.5→12.5）、G731（12.25→16.0）補強。
- [x] 原來如此 G734–G740 七組 ready、定稿觀眾分 6.94–8.15，登記進備份分類表；G733 只評題目未過 6.5。

## How to verify

```bash
node tools/video/curio/pool/cli.mjs check
node tools/video/so-thats-why/pool/cli.mjs check
node --test tools/video/so-thats-why/pool/pool.test.mjs
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py tests/test_video_backup.py
```

## Notes

- 奇聞被退回最多的原因變成「流傳樣本自己已講了翻轉」：寫卡與研究時要先確認樣本真的講錯。
- 原來如此第三輪七組裡五組第一輪不到門檻，原因多是同一政府體系或合著的網被併算；補研究時直接指定「不同國家、不同體系」的來源比較快。
- 單集題待評分時，可以先放進 held（註明待評分）讓建置通過，評完再移到 ids。
