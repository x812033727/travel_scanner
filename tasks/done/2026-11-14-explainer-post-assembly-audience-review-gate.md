---
id: 2026-11-14-explainer-post-assembly-audience-review-gate
title: explainer post-assembly audience review gate and P12 lessons — 把成片獨立觀眾評分與修完再推後台備份加入流程，並補入縮圖裁切、色溫對比、無字圖解與八語配音教訓
status: done
priority: P2
area: docs
owner: antigravity-audience-review-gate
claimed_at: 2026-11-14T13:43:42Z
created_at: 2026-11-14T13:43:29Z
completed_at: 2026-11-14T14:08:15Z
branch: claude/video-audience-review-gate
depends_on: []
scope:
  - AGENTS.md
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - docs/videos/explainer-series/README.md
  - docs/videos/so-thats-why/CURRENT.md
  - docs/videos/so-thats-why/look.md
  - docs/videos/so-thats-why/thumbnails.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/HANDOFF.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/SCORECARD.md
  - docs/videos/lessons/sothatswhy.md
  - docs/videos/lessons/explainer.md
---

# explainer post-assembly audience review gate and P12 lessons — 把成片獨立觀眾評分與修完再推後台備份加入流程，並補入縮圖裁切、色溫對比、無字圖解與八語配音教訓

## Why

站主在檢視 `sothatswhy-p12-qr-code` 時明確指示：「找一個觀眾評分一下內容跟影片看起來的感覺，如果有需要改善的改善，如果有需要加入規則或教訓的就加入」以及「那就是把觀眾評分加入流程，修完後才推後台跟備份」。既有流程在 `assemble`＋`qa`（11/11）後就直接備份到 Google Drive 並 `review-push --gate final`，但機械品管抓不到縮圖 `subject: "right"` 搭配 `on the right third` 造成的右緣斷頭裁切、連續 35 張暖黃木桌造成的色溫疲勞與低對比、無字示意圖跨鏡幾何漂移，以及八語 MiniMax 配音的符號誤讀（如印尼文 `&` 唸成 `"FT"`、越南文千分位 `.` 唸成小數）。需將「成片獨立觀眾視角體驗評分 → 全數修完並重過 `qa` → 才執行雲端備份與後台送審」定為硬性關卡，並把本輪實測抓到的畫面、縮圖與多語配音規則寫入系列文件與共用教訓。

## Definition of done

- [x] `AGENTS.md`、`.agents/skills/curio-episode/SKILL.md`（與位元組一致的 `.claude/skills/curio-episode/SKILL.md`）、`docs/videos/explainer-series/README.md`、`docs/videos/so-thats-why/CURRENT.md`、`dialogue-pilot-20261103/{README,HANDOFF,SCORECARD}.md` 皆納入「成片獨立觀眾視角評分（`review/audience-review.md`）→ 問題全數修完並重過 `qa` 11/11 → 最後才執行 Google Drive 備份與 `review-push --gate final`」的強制順序。
- [x] `docs/videos/so-thats-why/{thumbnails,look}.md`、`dialogue-pilot-20261103/README.md` 與 `docs/videos/lessons/{sothatswhy,explainer}.md` 完整收錄縮圖 `subject: "right"` 中央構圖規則、厚塗水粉冷暖色溫呼吸與淺冷底圖解高對比、無字圖解跨鏡幾何鎖定、所長耳後鉛筆手勢高度限制、口語「剛剛／剛才」上限，以及八語 MiniMax 配音防呆。
- [x] `npm run test:tools`、`npm run test:docs-videos`、`npm run check:tasks` 與 `node docs/videos/rules-sync/sync.mjs --dry-run` 全數通過，且不動到 `docs/videos/long-form/review.json` 綁定雜湊的檔案。

## Steps

- [x] 更新 `docs/videos/lessons/sothatswhy.md` 與 `docs/videos/lessons/explainer.md` 記錄 2026-11-14 P12 觀眾視角審片與八語配音實戰教訓。
- [x] 更新 `docs/videos/so-thats-why/{CURRENT,look,thumbnails}.md` 與 `dialogue-pilot-20261103/{README,HANDOFF,SCORECARD}.md`。
- [x] 更新 `docs/videos/explainer-series/README.md`、`AGENTS.md` 與 `.agents/skills/curio-episode/SKILL.md`（同步複製至 `.claude/skills/curio-episode/SKILL.md`）。
- [x] 跑過 `npm run test:tools && npm run test:docs-videos && npm run check:tasks` 與 `rules-sync --dry-run`，結案並發 PR 合併。

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
node docs/videos/rules-sync/sync.mjs --dry-run
```

## Notes

- Claimed with `--force` because legacy stale tickets (`2026-10-10-sothatswhy-minimax-images`, `2026-10-14-curio-episodes-keep-the-series-look`, `2026-11-03-sothatswhy-dialogue-pilot-p02`, all >240h stale with no active worktree or competing PR) still list `look.md`, `dialogue-pilot-20261103`, and `curio-episode/SKILL.md` in their scopes. Verified via `who-is-on-it.mjs` and `gh pr list` that zero active sessions or open PRs touch any of the 12 scoped files.
