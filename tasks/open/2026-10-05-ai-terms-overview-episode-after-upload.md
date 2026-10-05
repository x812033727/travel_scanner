---
id: 2026-10-05-ai-terms-overview-episode-after-upload
title: AI 名詞五層樓總覽集：大綱關卡與上架後更新 overviews.json
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T07:25:04Z
completed_at:
branch:
depends_on:
  - 2026-10-03-ai-terms-register-engineering-ladder-episode
scope:
  - docs/videos/ai-terms/overviews.json
---

# AI 名詞五層樓總覽集：大綱關卡與上架後更新 overviews.json

## Why

「AI 名詞十分鐘」的五層樓總覽集 `ai-terms-prompt-to-graph-engineering`（提示詞、上下文、駕馭、迴圈、圖形工程一集講完）已經寫好稿子、查核兩輪（PR #1188），並由票 `2026-10-03-ai-terms-register-engineering-ladder-episode` 登記在 `docs/videos/ai-terms/overviews.json`，`status: "planned"`、`video_id` 與 `published_at` 是 `null`。剩下的都要等站主：在 `/admin/videos` 挑大綱（頻道立場仍空白時 Jev 不會自動挑），之後產線做完、站主在 YouTube Studio 上傳。這張票把那兩個時間點的登記接下來，免得名詞庫的狀態跟影片脫節。

## Definition of done

- [ ] 大綱關卡過了以後，`overviews.json` 那一筆 `status` 是 `in-production`。
- [ ] 上架以後，那一筆有 `video_id`（YouTube 影片 ID）、`published_at`（ISO 8601），`status` 是 `published`；`notes` 寫上架日期與卡過的關。
- [ ] 影片在 `all` 與 `engineering` 兩份播放清單裡（站主在 Studio 做；這張票只記錄做了沒有）。

## Steps

- [ ] 確認站主挑過大綱（`/admin/videos` 或 `node tools/video/cli.mjs status --slug ai-terms-prompt-to-graph-engineering`），改 `status`。
- [ ] 上架後從站主或後台拿到 `video_id` 與上架時間，填進 `overviews.json`。
- [ ] 提示詞工程、上下文工程、Harness Engineering、Loop Engineering 四集之後做時，說明欄連這支總覽集（`docs/videos/ai-terms/README.md` §跟其他系列與既有影片的分工）；這張票不改那四集。

## How to verify

```bash
node -e "const o=JSON.parse(require('fs').readFileSync('docs/videos/ai-terms/overviews.json','utf8')).overviews.find(v=>v.video_slug==='ai-terms-prompt-to-graph-engineering'); console.log(o.status, o.video_id, o.published_at)"
git diff --exit-code origin/main -- docs/videos/ai-terms/terms.json docs/videos/long-form
npm run check:tasks
```

## Notes

- 2026-10-05：split from `2026-10-03-ai-terms-register-engineering-ladder-episode`（那張票的「上架後補 `video_id`、`published_at`」一步）。
- 只改 `overviews.json`，不要改 `terms.json`：`terms.json` 整份綁在 `docs/videos/long-form/plans.json` 的 `source_hashes`，改一個位元組就要重建長片目錄並請獨立代理補長度收據（`docs/videos/ai-terms/README.md` §名詞庫與出片順序 最後一段）。
- 需要站主：挑大綱、Studio 上傳與播放清單都是站主的步驟；代理只做登記。
