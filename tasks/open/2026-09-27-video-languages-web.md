---
id: 2026-09-27-video-languages-web
title: Video languages web: the language panel after the final cut, the languages card, the publish card's five states
status: review
priority: P1
area: web
owner: claude-fable-5-1-video-languages
claimed_at: 2026-09-27T07:39:31Z
created_at: 2026-09-27T06:16:03Z
completed_at:
branch: claude/video-review-manga-workflow-fp1rpz
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

- [x] 語言面板取代 `DubLanguages`：成片核准後出現（之前一行「成片核准後可以選語言」）；四語 × 三部件的勾選；「照預設勾選」（設定的 `caption_locales`／`drama_caption_locales`）、「只出繁體中文」、「儲存」（`PUT …/languages`）；勾配音自動勾 CC；漫劇的配音灰掉；每格旁邊顯示 製作中／已完成／跳過（原因）／已上傳；上架後面板仍可多勾，取消只對還沒送上 YouTube 的部件有效並這樣寫。
- [x] `languages` 卡片取代 `DubsBody`：每語三部件狀態、下載連結（說明欄、字幕、音軌）、Studio「語言」頁步驤（`DUBS.md` §站主要做的事）、有配音時「已在 Studio 上傳」結案。
- [x] 上架卡五個狀態（等你決定語言／語言製作中／可以上架／已排定／已上架，LANGUAGES.md §上架流程）；`readyToUpload` 改讀伺服器的 `ready_to_upload`；「需要你」含等語言決定的影片；語言還在做時寫「排程會在語言做好後送出」。
- [x] 五語 `admin.json`；vitest：面板規則、卡片、五個狀態。

## Steps

- [x] 面板與卡片。
- [x] 上架卡狀態與清單分組。
- [x] 字串與測試。

## How to verify

```bash
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-reviews
```

## Notes

- `DUB_LOCALES` 與 `dubsTitle`、`dubStatuses.*`、`downloadTrack` 等字串可以沿用或改名，五個語系一起改。
- 做法（2026-09-27）：`admin-video-review-card.tsx` 多了 `LOCALES`、`LOCALE_PARTS`、`LocaleChoice`、`LanguagePart`、`finalApproved`、`publishState`（五個狀態；舊 API 沒有 `ready_to_upload` 時只認得可以上架／已排定／已上架）、`partStateLabel`，`readyToUpload` 改讀伺服器的 `ready_to_upload`（沒有時退回舊公式），`needsOwner` 把「等你決定語言」算進去；`LanguagesBody` 取代 `DubsBody`，`languages` 與舊的 `dubs` 卡片都用它（舊 payload 的 `status`／`file_role` 當成配音那一格）。`admin-video-reviews.tsx` 的 `LanguagePanel` 取代 `DubLanguages`（教學與漫劇都顯示；漫劇的配音灰掉），`PublishPill` 用在清單、可以上架卡與影片頁標題；`UploadedForm` 改成上傳包核准就出現，語言還在做時標題下寫「排程會在語言做好後送出」。
- 「照預設勾選」讀 `GET /admin/video-automation/settings` 的 `caption_locales`（漫劇讀 `drama.drama_caption_locales`），每個預設語言勾標題說明與 CC，不勾配音。
- 成片核准的判斷（清單沒有審核列）：checklist 的 `final_video_approved` 打勾、或已有 `publish_approved_at`／`locales_decided_at`／`youtube_video_id`；影片頁再加「有核准的 `final` 審核」。
- 刪掉的字串：`videoReviews.dubsTitle`、`dubsHelp`、`dubsSave`、`dubsSaved`、`dubsError`、`dubStatuses.*`；這些 key 的後台覆寫會變孤兒（無害，覆寫頁看得到）。`gates.dubs`、`approveDubs`、`downloadTrack`、`locales.*` 留著。
- `ProjectSummary` 仍留 `dub_locales?`，等 API 拿掉 shim 時一起刪。
