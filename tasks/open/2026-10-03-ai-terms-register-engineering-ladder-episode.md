---
id: 2026-10-03-ai-terms-register-engineering-ladder-episode
title: AI 名詞庫登記五層樓總覽集（terms.json 與系列 README）
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-03T23:45:46Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ai-terms
---

# AI 名詞庫登記五層樓總覽集（terms.json 與系列 README）

## Why

`docs/videos/ai-terms-prompt-to-graph-engineering/` 是「AI 名詞十分鐘」第一集五個名詞一起講的總覽集（提示詞、上下文、駕馭、迴圈、圖形工程），由票 `2026-10-03-ai-terms-engineering-ladder-video` 寫好並查核兩輪。系列的名詞庫 `docs/videos/ai-terms/terms.json` 與 README 還不知道它：名詞庫一列一個名詞，沒有「總覽集」這種列；README 的 §一個名詞怎麼變成一集 也只寫單一名詞。那個資料夾當時在票 `2026-09-29-ai-terms-video-pilot` 的 scope 裡，所以撰稿票沒碰。

## Definition of done

- [ ] `terms.json` 能表達這一集：加一個 `overviews`（或同義）區塊，列 `video_slug`、涵蓋的名詞 id（prompt-engineering、context-engineering、harness-engineering、loop-engineering，graph-engineering 沒有文章）、`status`、`video_id`；或在五個名詞的列加 `overview_video`。schema 的改法寫在 README。
- [ ] README 的播放清單表把它放進 `engineering`，§跟其他系列與既有影片的分工 說明總覽集與單名詞集怎麼分工（總覽講地圖與診斷，單名詞集深講機制）。
- [ ] `npm run check:tasks` 與既有讀 `terms.json` 的測試（若有）通過。

## Steps

- [ ] 等 `2026-09-29-ai-terms-video-pilot` 結案釋出 scope，或與持有者協調。
- [ ] 決定 schema（overviews 區塊 vs 每列加欄位），改 `terms.json` 與 README。
- [ ] 上架後補 `video_id`、`published_at`。

## How to verify

```bash
node -e "JSON.parse(require('fs').readFileSync('docs/videos/ai-terms/terms.json','utf8'))"
npm run check:tasks
```

## Notes

- 2026-10-03：Graph Engineering 站上還沒有文章（名詞庫也沒有這一列）；總覽集的說明欄連總索引與另外三篇文章。若之後要替它開單名詞集，先走 content-pipeline 寫文章。
