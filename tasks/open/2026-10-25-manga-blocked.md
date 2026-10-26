---
id: 2026-10-25-manga-blocked
title: 免關卡的漫劇（manga 等級）關鍵影格改完兩輪提示詞仍沒過時，保留最佳張往下做，不再 blocked
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5-manga-accept-best
claimed_at: 2026-10-26T15:54:01Z
created_at: 2026-10-25T22:59:31Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - docs/videos/BINGE.md
  - docs/videos/HANDS-OFF.md
---

# 免關卡的漫劇關鍵影格：改完兩輪提示詞仍沒過就保留最佳張往下做

## Why

2026-10-25 《系統說我是 BUG》第 1 集重做與第 5 集同時 `blocked: keyframes still fails after 2 prompt fixes`：50 鏡裡 6 鏡、55 鏡裡 4 鏡的最後一張還被 judge 列問題（例：極遠景畫成中景、唐測沒有髮髻、小鐵畫成 3D、隱身的「熱氣漣漪」畫成實體人），分數多在 8.4–9.6。免關卡作品（`hands_off`、`drama_auto_approve_final` 開著）在這裡就停，等人改提示詞或接受；50 集每集 10% 的鏡頭會這樣，等於每集都要人。

`flow.mjs acceptBestPictures` 已有這條路（站主 2026-10-06 的決定：影片不再因圖片卡住，保留 judge 最佳張、備註帶到成片審核），但只對插圖投影片（`illustrated(video)`）開；`media/keyframes.mjs --accept-best` 對漫劇直接 UsageError。manga 等級的漫劇（BINGE.md §畫面等級）也是靜圖，成片的觀感一樣由成片關卡把關，沒有理由不走同一條。

當天的解法是手改主機：在容器裡照 `acceptBest` 的做法把 10 鏡標成 `accepted_with_problems`、auto.json 加 `accepted_pictures`、刪 `prompt_fixes.keyframes`，後台按重試。

## Definition of done

- [ ] manga 等級的漫劇（單集與作品的集；`visual_tier === "manga"`）在 `prompt_fixes.keyframes` 用完後走 `acceptBestPictures`：保留每個還沒過的鏡的最佳張、備註進 `accepted_pictures`，分鏡審核照 #1821 的 details 規則自動核准，成片審核的 payload 列出保留的鏡與 judge 的話。
- [ ] `keyframes --accept-best` 接受 manga 漫劇；動畫漫劇（有 clip 的）與長篇動畫行為不變，仍 blocked。
- [ ] 不是免關卡的 manga 漫劇也走這條（站主 10-06 的決定是「影片不再因圖片卡住」，成片關卡會看到備註）。
- [ ] BINGE.md §畫面等級、HANDS-OFF.md 的表寫明。

## Steps

- [ ] `keyframes.mjs acceptBest`：`illustrated(doc) || mangaTier(doc, project)`；`flow.mjs acceptBestPictures` 同一條件（看 `doc.series?.visual_tier ?? project.series?.visual_tier`，和 keyframes.mjs 的 `manga` 判法一致）。
- [ ] `sync.mjs`：final 審核的 `accepted_pictures` 對 drama 也送（確認 `acceptedPicturesOf` 沒被 format 擋）。
- [ ] 測試：manga 漫劇兩輪後保留並進分鏡；動畫漫劇仍 blocked。
- [ ] `npm run test:tools`；`flow.mjs`、`keyframes.mjs`、`sync.mjs` 在 REVIEW_FILES，收據由獨立審查代理做 DURATION_ONLY 增量。

## How to verify

第 2 集重做起若有鏡頭兩輪沒過，auto.json 出現 `accepted_pictures`、notes「pictures kept with the judge's remarks」，作品不再 blocked；成片審核 payload 列出那些鏡。

## Notes

- 10-25 手改用的腳本在 scratchpad `host_keep_pictures.js`（`docker exec -i travel_scanner-video-worker-1 node -`）。
- 相關票：`2026-10-25-fixprompts-look-blocked-sheet-prompt`（退件設定圖沒重畫）、`2026-10-24-storyboard-check-passed-problems-manga-details`（分鏡 details 自動核准，#1821）。
