---
id: 2026-09-27-video-languages-web
title: Video languages web: the language panel after the final cut, the languages card, the publish card's five states
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-27T06:16:03Z
completed_at:
branch:
depends_on:
  - 2026-09-27-video-languages-api
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
---

# Video languages web: the language panel after the final cut, the languages card, the publish card's five states

## Why

站主要在成片核准後、上架前決定每支影片加哪些語言、每種加什麼（標題與說明、CC、配音），決定並做好才排上架（`docs/videos/LANGUAGES.md`）。現在影片頁只有配音的四個勾選（`DubLanguages`）與 `dubs` 卡片。伺服器端在 `2026-09-27-video-languages-api`。

## Definition of done

- [ ] 語言面板取代 `DubLanguages`：成片核准後出現（之前一行「成片核准後可以選語言」）；四語 × 三部件的勾選；「照預設勾選」（設定的 `caption_locales`／`drama_caption_locales`）、「只出繁體中文」、「儲存」（`PUT …/languages`）；勾配音自動勾 CC；漫劇的配音灰掉；每格旁邊顯示 製作中／已完成／跳過（原因）／已上傳；上架後面板仍可多勾，取消只對還沒送上 YouTube 的部件有效並這樣寫。
- [ ] `languages` 卡片取代 `DubsBody`：每語三部件狀態、下載連結（說明欄、字幕、音軌）、Studio「語言」頁步驤（`DUBS.md` §站主要做的事）、有配音時「已在 Studio 上傳」結案。
- [ ] 上架卡五個狀態（等你決定語言／語言製作中／可以上架／已排定／已上架，LANGUAGES.md §上架流程）；`readyToUpload` 改讀伺服器的 `ready_to_upload`；「需要你」含等語言決定的影片；語言還在做時寫「排程會在語言做好後送出」。
- [ ] 五語 `admin.json`；vitest：面板規則、卡片、五個狀態。

## Steps

- [ ] 面板與卡片。
- [ ] 上架卡狀態與清單分組。
- [ ] 字串與測試。

## How to verify

```bash
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-reviews
```

## Notes

- `DUB_LOCALES` 與 `dubsTitle`、`dubStatuses.*`、`downloadTrack` 等字串可以沿用或改名，五個語系一起改。
