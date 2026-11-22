---
id: 2026-11-22-shorts-flow-3series-lessons
title: 零台詞 Shorts 三系列 Flow 重製：教訓與規則更新
status: done
priority: P2
area: docs
owner: claude-opus-5-5-shorts-flow
claimed_at: 2026-11-21T19:01:08Z
created_at: 2026-11-21T19:00:55Z
completed_at: 2026-11-21T19:13:47Z
branch: claude/shorts-flow-3series-20261122
depends_on: []
scope:
  - docs/videos/lessons/shorts.md
  - docs/videos/shorts-drama
---

# 零台詞 Shorts 三系列 Flow 重製：教訓與規則更新

## Why

站主 2026-11-22 要把《汪家夫妻》《闖禍小浣熊》《網美小豬》各五集照社畜地獄的新規則用 Google Flow
重製。這次做的過程裡學到的事（盲評回歸、配件外漏、Flow 用舊版圖、剪接推鏡的錯、響度量法差異、
零台詞片的政策檢查）只記在對話裡就會丟，下一個做 Shorts 的代理會再踩一次。

## Definition of done

- [x] `docs/videos/lessons/shorts.md` 有 2026-11-22 三系列的教訓。
- [x] `WRITING.md`、`REVIEW.md`、`PRODUCTION-ROUTES.md` 補上會影響下一集做法的規則。
- [x] 三個系列檔都有 Flow 重製版的集數表、審核結果與排程提醒。

## Steps

- [x] 寫教訓（盲評、系列骨架、配件外漏、NEWEST version、描述性檔名、推鏡錯、響度、核准、背景分頁、附圖）。
- [x] 改共用規則與三個系列檔。
- [x] 跑 `npm run check:tasks`。

## How to verify

`npm run check:tasks`；讀 `docs/videos/shorts-drama/series/*.md` 第六節。

## Notes

- 製作檔在本機 `mokaair-work/shorts-flow/<系列>/`，備份在雲端硬碟 `AI/備份/Shorts/<系列>/`。
- 零台詞片的網站政策檢查只讀標題與說明（`tools/video/shorts/qa.mjs`），「符合立場」分數會飄
  （同一份文字 0.53 → 0.47）；改寫成「零台詞小日常、輕鬆看」也沒有變好（0.44），所以交給站主判斷，
  不再重跑。頻道立場存在 `/admin/videos` 的設定裡，repo 讀不到。
