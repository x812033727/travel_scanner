---
id: 2026-11-17-fold-a-demand-dimension-into-the
title: Fold a demand dimension into the pool audience score
status: review
priority: P2
area: tools
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T01:16:15Z
created_at: 2026-11-17T01:16:15Z
completed_at:
branch: claude/wizardly-albattani-is0lls
depends_on: []
scope:
  - tools/video/curio/pool
  - tools/video/so-thats-why/pool
  - tools/video/pool-admin
  - docs/videos/history-curiosity/pool
  - docs/videos/so-thats-why/pool
  - apps/api/app/video_pools
  - apps/api/tests/test_video_pools.py
  - apps/web/components/admin-video-pools.tsx
  - apps/web/components/admin-video-pools.test.tsx
  - apps/web/lib/video-pools-messages
  - apps/web/lib/video-pools-copy.ts
---

# Fold a demand dimension into the pool audience score

## Why

站主 2026-11-17：擴充池本來就有獨立觀眾評分，照參考頻道觀看數歸納的選題四問要整合進去，不另立一套。站主定了三件事：併成一個總分、
先只評可成題的題案、門檻維持 6.5 看總分；並要求把這個機制寫進擴充池的流程。量測與四問的出處在 `docs/videos/channel-review-20261116/README.md`。

## Definition of done

- [x] 兩個池的題案 `audience` 多一項 `demand`（四個是非題換算 1–10），`score =（五項平均 × 5 + demand）÷ 6`，五項平均留在 `base`。
- [x] `build`／`check` 擋：可成題沒有需求分、需求分與答案不符、總分不符公式、可成題總分低於 6.5。
- [x] 奇聞 77 組、原來如此 154 組可成題由獨立評審答完四問，紀錄在各池 `reviews/demand-20261117.json`；總分低於 6.5 的改成後備。
- [x] 後台資料包、API 欄位、後台頁面與五個語系帶出需求分。
- [x] 兩個池 README 的〈獨立觀眾評分〉寫進第六項與「擴充時的順序」。
- [ ] PR 合併。

## Steps

- [x] 兩份 `render.mjs`：`DEMAND_QUESTIONS`、`demandScore`、`blendedScore`、`validateDemand` 與兩條關卡。
- [x] 六位獨立評審分批答四問；每批三組重複題，24 個答案全部一致。
- [x] 寫回 `themes.json`、重排名次、重建兩池與 `pools.json`。
- [x] 測試與文件。

## How to verify

```bash
node --test tools/video/curio/pool/pool.test.mjs tools/video/so-thats-why/pool/pool.test.mjs tools/video/pool-admin/bundle.test.mjs
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py
cd apps/web && npx vitest run components/admin-video-pools.test.tsx
```

## Notes

- 結果：奇聞可成題 77 → 23（54 組改後備），原來如此 154 → 84（70 組改後備）。改後備的題案 `material.was` 是 `ready`、`missing` 寫總分；
  要還原就把 `verdict` 改回 `ready` 並調門檻或換算，`base` 都留著。
- 需求分布偏低：奇聞 0 題 25、1 題 40、2 題 9、3 題 3；原來如此 0 題 89、1 題 62、2 題 3。原來如此池的可成題幾乎都是通用科學現象，
  「規格或誰收錢」只有 4 組、「大公司或日本品牌」0 組。下一批擴充先照四問挑方向。
- 基準初評 `reviews/audience-20261114.json` 的題案原本不受 6.5 關卡限制；併分後 API 測試（可成題都要過門檻）會紅，
  所以有需求分的題案一律看總分，基準只豁免「要有 rounds」。這多改了奇聞 14 組、原來如此 3 組。
- 沒動：奇聞池單題層的 156 筆觀眾分數仍是五項；品牌故事沒有池子；`producer` skill 的評分表（scope 在票 `2026-11-03-skill-ai`）。
- 四問來自三個頻道最新 200 支的標題分組，是相關不是因果；分數是代理的判斷。
