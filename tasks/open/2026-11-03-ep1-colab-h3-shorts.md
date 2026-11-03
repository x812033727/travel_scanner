---
id: 2026-11-03-ep1-colab-h3-shorts
title: 汪汪社畜 EP1 分鏡：Colab H3 小樣、Shorts 與八語上架
status: in-progress
priority: P2
area: docs
owner: claude-opus-5-5-wangwang
claimed_at: 2026-11-03T10:23:40Z
created_at: 2026-11-03T10:23:19Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/wangwang-office-e01
---

# 汪汪社畜 EP1 分鏡：Colab H3 小樣、Shorts 與八語上架

## Why

站主要做一個寵物職場喜劇的直式短劇系列《汪汪社畜》（柴犬麻糬把家當公司），指定片段用 Google Colab 的 MiniMax H3 生成、成品是 Shorts、上架要八種語言。第 1 集的分鏡已寫好，接下來要走劇本關卡、小樣與製作。

## Definition of done

- [x] `docs/videos/wangwang-office-e01/video.json` lint 零錯誤、`shot_plan --strict` 通過；`storyboard.md` 給站主讀。
- [ ] 站主核准劇本關卡。
- [ ] 三鏡小樣（s07-dash、s08-suck、s09-kpi）在 Colab H3 生成、匯入，站主看過。
- [ ] 整集合成、成片核准，`shorts from-drama` 出 9:16，八語標題、說明與 CC 上架。

## Steps

- [x] 分鏡、brief、storyboard。
- [x] `script` → `review-push --gate script`（2026-11-03 送出，等站主在 /admin/videos 核准，之後 `review-pull`）。
- [ ] `look`、`tts`、`keyframes`，用實際 timeline 重跑 `shot_plan`，`plan_lock --write`。
- [ ] Colab：`bootstrap.sh` → `h3.sh usage` → 小樣 → 其餘批次（`h3_detached.py`）→ `clips import`。
- [ ] `assemble` → 成片核准 → `shorts from-drama` → qa、package、push；語言面板勾 en、ja、ko、es、pt、id、vi、th。

## How to verify

```bash
node tools/video/cli.mjs lint --file docs/videos/wangwang-office-e01/video.json
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs docs/videos/wangwang-office-e01/video.json --route hailuo --hailuo-model h3 --strict
```

## Notes

- `drama_craft_check` 只剩 `lines.narrator`（內心話 89%）沒過，是這個系列的設計，刻意保留。
- 原本台詞用「KPI」，改成「績效」，因為 `docs/videos/lexicon.json` 正被別的任務改著；之後要用 KPI，先把它加進字典。
- 角色對話漫劇目前不能做配音（422 `video_locales_dub_not_for_drama`），八語是標題、說明與 CC。
- 原生 9:16 漫劇還沒有工具（票 `2026-09-28-video-shorts-worker-drama`），所以走 16:9 再 `from-drama` 裁切；H3 直式 736×1312 沒驗過。
