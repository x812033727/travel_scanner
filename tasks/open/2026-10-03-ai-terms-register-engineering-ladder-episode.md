---
id: 2026-10-03-ai-terms-register-engineering-ladder-episode
title: AI 名詞庫登記五層樓總覽集（terms.json 與系列 README）
status: in-progress
priority: P3
area: docs
owner: claude-opus-5-5-ai-terms-ladder-register
claimed_at: 2026-10-05T07:06:34Z
created_at: 2026-10-03T23:45:46Z
completed_at:
branch: claude/ai-terms-ladder-register
depends_on: []
scope:
  - docs/videos/ai-terms
---

# AI 名詞庫登記五層樓總覽集（terms.json 與系列 README）

## Why

`docs/videos/ai-terms-prompt-to-graph-engineering/` 是「AI 名詞十分鐘」第一集五個名詞一起講的總覽集（提示詞、上下文、駕馭、迴圈、圖形工程），由票 `2026-10-03-ai-terms-engineering-ladder-video` 寫好並查核兩輪。系列的名詞庫 `docs/videos/ai-terms/terms.json` 與 README 還不知道它：名詞庫一列一個名詞，沒有「總覽集」這種列；README 的 §一個名詞怎麼變成一集 也只寫單一名詞。那個資料夾當時在票 `2026-09-29-ai-terms-video-pilot` 的 scope 裡，所以撰稿票沒碰。

## Definition of done

- [x] `terms.json` 能表達這一集：加一個 `overviews`（或同義）區塊，列 `video_slug`、涵蓋的名詞 id（prompt-engineering、context-engineering、harness-engineering、loop-engineering，graph-engineering 沒有文章）、`status`、`video_id`；或在五個名詞的列加 `overview_video`。schema 的改法寫在 README。——改放在 `terms.json` 旁邊的 `docs/videos/ai-terms/overviews.json`（`overviews` 區塊，欄位如上再加 `source_guide`、`playlist`、`covers_without_term`、`published_at`、`notes`），`terms.json` 一個位元組都沒動，理由見 Notes；schema 寫在 README §總覽集。
- [x] README 的播放清單表把它放進 `engineering`，§跟其他系列與既有影片的分工 說明總覽集與單名詞集怎麼分工（總覽講地圖與診斷，單名詞集深講機制）。
- [x] `npm run check:tasks` 與既有讀 `terms.json` 的測試（若有）通過。

## Steps

- [x] 等 `2026-09-29-ai-terms-video-pilot` 結案釋出 scope，或與持有者協調。——那張票 2026-10-04 被看板總整理釋出（owner 空），沒有進行中的票持有 `docs/videos/ai-terms`，claim 沒被拒，不需要 `--force`。
- [x] 決定 schema（overviews 區塊 vs 每列加欄位），改 `terms.json` 與 README。——選 overviews 區塊，放在新檔 `overviews.json`；README 改了，`terms.json` 不改。
- [ ] 上架後補 `video_id`、`published_at`。——要等站主挑大綱與上傳，拆到票 `2026-10-05-ai-terms-overview-episode-after-upload`。

## How to verify

```bash
node -e "JSON.parse(require('fs').readFileSync('docs/videos/ai-terms/terms.json','utf8'))"
node -e "JSON.parse(require('fs').readFileSync('docs/videos/ai-terms/overviews.json','utf8'))"
git diff --exit-code origin/main -- docs/videos/ai-terms/terms.json docs/videos/long-form apps/api/app/video_plans
node tools/video/long-form/cli.mjs check
node --test tools/video/long-form/admin-catalog.test.mjs tools/video/long-form/plans.test.mjs tools/video/long-form/review.test.mjs
npm run check:tasks
```

## Notes

- 2026-10-03：Graph Engineering 站上還沒有文章（名詞庫也沒有這一列）；總覽集的說明欄連總索引與另外三篇文章。若之後要替它開單名詞集，先走 content-pipeline 寫文章。
- 2026-10-05（claude-opus-5-5-ai-terms-ladder-register）：為什麼不寫進 `terms.json`。`docs/videos/long-form/plans.json` 的 `source_hashes` 綁著 `terms.json` 整份的 SHA-256，每一列也有 `source_record_sha256`；`plans.json` 又在長度收據 `docs/videos/long-form/review.json` 的 108 個受審檔案裡。用 `buildAdminCatalog` 注入一份只把 prompt-engineering 的 `status` 改成 `planned` 的 `terms.json`，結果是 `source hash drift: docs/videos/ai-terms/terms.json`（`npm run test:tools` 的 `admin-catalog.test.mjs` 會紅）。所以在 `terms.json` 加區塊或欄位都要重建 `plans.json` 與 `apps/api/app/video_plans/data/catalog.json`，再請獨立代理補收據增量，scope 也要擴到長片目錄。旁邊另放 `overviews.json` 不在任何雜湊裡，長片目錄與收據都不用動；README §名詞庫與出片順序 的最後一段把這條連鎖寫下來，因為發起一集（`status` 改 `planned`）與上架（填 `video_id`）本來就要改 `terms.json`，之後每一集都會碰到。
- `overviews.json` 那一筆的 `status` 是 `planned`，跟試片三集同樣狀態（brief、稿子、查核做完，等站主挑大綱；README 第 3 步才改 `in-production`）。`covers` 四個 id 都在 `terms.json`；`covers_without_term` 記圖形工程；`notes` 記旁白用「駕馭工程」、文章卡與片尾說站上譯名「代理執行環境工程」，給之後的 harness-engineering 單名詞集沿用。
- 長片目錄（`plans.json`、後台 `/admin` 的長片企劃）不列總覽集；總覽集在 `/admin/videos` 出現靠 `review-push`，跟其他全自動影片一樣，所以沒有另開票。
- 留下的：上架後補 `video_id`、`published_at` 與 `status`，拆到 `2026-10-05-ai-terms-overview-episode-after-upload`（只改 `overviews.json`）。
