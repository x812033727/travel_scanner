---
id: 2026-09-27-video-drama-room-web
title: Video drama room web: the discussion thread on documents and screenplays, the one-off episode's page
status: in-progress
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
  - apps/web/messages
---

# Video drama room web: the discussion thread on documents and screenplays, the one-off episode's page

## Why

站主要能在後台跟模型討論設定集、細綱與劇本（`docs/videos/DRAMA-FLOW.md` §三），單集也要有跟作品一樣的頁面（§二）。伺服器端在 `2026-09-27-video-drama-room-messages-api`。

## Definition of done

- [ ] `DocPanel`（`admin-video-series.tsx`）多一節「討論」：訊息列（站主／模型、對哪一版說的、時間）、輸入框、「送出」（`POST …/messages`）；有未回覆的訊息顯示「等模型回覆」；文件核准後唯讀。原本的核准、退回、自己改不動。
- [ ] 劇本關卡卡片（`admin-video-review-card.tsx` 的 `ScriptBody`）同樣一節，subject `script:<集數>`；影片頁對帶 `series_slug` 的漫劇載入。
- [ ] 單集的影片頁最上面顯示 one-off 作品的 `bible` `DocPanel`（含討論），下面才是關卡；「單集漫劇」清單改列 `kind = one-off` 的作品；「新的漫劇」表單送出後開那部作品。
- [ ] 作品列表卡顯示等模型回覆與等你核准的則數。
- [ ] 五語 `admin.json`；vitest：發言、等回覆、新版本出現後串留著、核准後唯讀。

## Steps

- [ ] 討論串元件（共用給文件與劇本）。
- [ ] 單集頁與清單。
- [ ] 字串與測試。

## How to verify

```bash
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-series admin-video-reviews
```

## Notes

- 卡片與關卡 body 都在 `admin-video-review-card.tsx`（#818 抽出）；頁面在 `admin-video-reviews.tsx`；作品頁在 `admin-video-series.tsx`。
