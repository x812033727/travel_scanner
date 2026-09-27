---
id: 2026-09-27-video-drama-room-web
title: Video drama room web: the discussion thread on documents and screenplays, the one-off episode's page
status: review
priority: P1
area: web
owner: claude-fable-5-1-video-languages
claimed_at: 2026-09-27T11:36:45Z
created_at: 2026-09-27T06:16:02Z
completed_at:
branch:
depends_on:
  - 2026-09-27-video-drama-room-messages-api
scope:
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-thread.tsx
  - apps/web/components/admin-video-thread.test.tsx
  - apps/web/messages
---

# Video drama room web: the discussion thread on documents and screenplays, the one-off episode's page

## Why

站主要能在後台跟模型討論設定集、細綱與劇本（`docs/videos/DRAMA-FLOW.md` §三），單集也要有跟作品一樣的頁面（§二）。伺服器端在 `2026-09-27-video-drama-room-messages-api`。

## Definition of done

- [x] `DocPanel`（`admin-video-series.tsx`）多一節「討論」：訊息列（站主／模型、對哪一版說的、時間）、輸入框、「送出」（`POST …/messages`）；有未回覆的訊息顯示「等模型回覆」；文件核准後唯讀。原本的核准、退回、自己改不動。
- [x] 劇本關卡卡片（`admin-video-review-card.tsx` 的 `ScriptBody`）同樣一節，subject `script:<集數>`；影片頁對帶 `series_slug` 的漫劇載入。
- [x] 單集的影片頁最上面顯示 one-off 作品的 `bible` `DocPanel`（含討論），下面才是關卡；「單集漫劇」清單改列 `kind = one-off` 的作品；「新的漫劇」表單送出後開那部作品。
- [x] 作品列表卡顯示等模型回覆與等你核准的則數。
- [x] 五語 `admin.json`；vitest：發言、等回覆、新版本出現後串留著、核准後唯讀。

## Steps

- [x] 討論串元件（共用給文件與劇本）。
- [x] 單集頁與清單。
- [x] 字串與測試。

## How to verify

```bash
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-series admin-video-reviews
```

## Notes

- 2026-09-27 做完（claude-fable-5-1-video-languages）。
  - 討論串是新檔 `admin-video-thread.tsx` 的 `DiscussionThread`（`docSubject`、`scriptSubject`、`threadPath`），只從 `admin-video-review-card.tsx` 拿 `useRefresh`／`useWhen`／`control`，那邊不反過來引用。`GET …/messages?subject=` 每 `REFRESH_MS` 讀一次；送出後重讀，重讀失敗就先把伺服器回的那一則接上去。每則：站主／企劃／撰稿、對第 n 版（`refers_to` 是 `v3` 這種）或對劇本雜湊、時間；站主那則 `answered_at` 為空就掛「等模型回覆」。`readOnly` 時沒有輸入框，寫「已核准：這條討論串只留紀錄」；沒有任何一則的唯讀串不畫。409／404 的 `detail` 顯示在「沒有送出：…」。
  - `DocPanel`：「看全文」之後多「討論」，subject 由 `doc.kind`／`chapter_number` 推，文件 `approved` 就唯讀，`unanswered > 0` 在 summary 掛「等模型回覆」；`onPosted` → 重讀作品（模型出的新版本會換掉 panel，串以 subject 為 key 留著）。核准、退回、自己改都沒動。`docKinds.bible`＝故事聖經；單集在 `setting` 狀態的 pill 顯示「故事聖經」（`statuses.bible`）。
  - `ReviewCard` 多一個可選的 `discussion` 節點，渲染在關卡 body 之後；影片頁對有 `series_slug` 與 `episode_number` 的影片，在 `script` 卡片放 `DiscussionThread`（subject `script:<集數>`）：pending 的卡收訊息，歷史裡 approved 的卡唯讀留紀錄，rejected／superseded 的不畫（同一個 subject 會重複）。
  - 單集影片頁：只要影片有 `series_slug` 就讀 `GET /admin/video-automation/series/{slug}`，有 `bible` 文件就在最上面畫 `DocPanel`（含討論）；`kind = one-off` 但還沒有聖經就寫「工人下一輪會寫故事聖經」；長篇作品的集沒有 bible 就什麼都不畫。**不用 slug 前綴判斷**（伺服器以 `kind` 定義單集）。
  - 「漫劇」分頁：作品清單讀 `?kind=series`，「單集漫劇」清單讀 `?kind=one-off`（卡片：單集、狀態、等你核准／等模型回覆、花費、風格、分鐘、前提；點開作品頁），不再讀 `/admin/videos?format=drama`；請求佇列只留沒有 `series_slug` 的舊請求。「新的漫劇」送出後用回應的 `series_slug` 直接開那部作品的頁面。作品頁對單集：pill「單集」、沒有「x/y 集」與「先規劃下一篇」。
  - 五語 `admin.json`：`videoSeries.docKinds.bible`、`statuses.bible`、`messagesPending`、`bibleEmpty`、`oneOff`、`thread.*`（title、empty、authors.*、aboutVersion、aboutScript、waiting、closed、input、placeholder、send、sending、sendError、loadError）；`videoReviews.newDramaHelp` 改文字。
  - 測試：`admin-video-thread.test.tsx` 4 個、`admin-video-series.test.tsx` 6 個（討論後新版本出現串留著、核准後唯讀、單集清單與表單開作品）、`admin-video-reviews.test.tsx` 21 個（劇本卡的討論、單集頁的故事聖經含核准後重讀、歷史裡 approved 劇本唯讀而 rejected 不畫、以作品 `kind` 認單集）。
  - 審查發現、另開票：單集在故事聖經核准前沒有地方撤回（`2026-09-27-video-drama-room-withdraw-a-one`）。
- 卡片與關卡 body 都在 `admin-video-review-card.tsx`（#818 抽出）；頁面在 `admin-video-reviews.tsx`；作品頁在 `admin-video-series.tsx`。
