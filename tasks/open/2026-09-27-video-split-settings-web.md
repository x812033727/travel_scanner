---
id: 2026-09-27-video-split-settings-web
title: Video split settings web: the settings tab splits into tutorial, drama and shared, each saved on its own
status: open
priority: P1
area: web
owner:
claimed_at:
created_at: 2026-09-27T06:16:00Z
completed_at:
branch:
depends_on:
  - 2026-09-27-video-split-settings-api
scope:
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings-tutorial.tsx
  - apps/web/components/admin-video-settings-drama.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/components/admin-video-model-settings.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/messages
---

# Video split settings web: the settings tab splits into tutorial, drama and shared, each saved on its own

## Why

`/admin/videos?tab=settings` 是一張表單：教學的排程在最上面、漫劇在最下面、中間的常設指示寫「投影片與漫劇每一支都適用」，一顆儲存鈕整張送。站主 2026-09-27 要漫劇與教學的設定分開。設計與欄位歸屬表在 `docs/videos/DRAMA-FLOW.md` §一。

## Definition of done

- [ ] `?tab=settings&section=tutorial|drama|shared`（預設 `tutorial`，用 `useAdminQueryState`），三個子分頁各一顆儲存鈕，各自只送自己的欄位（`saveBody` 拆成三個；靠 API 票的「省略＝不改」）。
- [ ] 教學子分頁：排程與題材、常設指示、頻道聲音、長度、語言預設（`caption_locales`，標為「語言面板預先勾選」）、輪數、預算與本月草稿、關卡（旁白、Jev 挑大綱、成片）、目前的提示詞（教學的）。
- [ ] 漫劇子分頁：開關、題材、常設指示（`drama_stage_instructions`）、旁白聲音（勾「跟教學一樣」＝ `null`）與角色聲音池、語言預設（`drama_caption_locales`）、輪數（`drama_max_*` 與每鏡重做、每支片段數）、關卡（旁白、成片、設定圖自動選、分鏡自動核准、「劇本先給我看」＝ `series_script_gate`）、媒體模型、片段規格、風格預設、預算與本月媒體用量、作品的數字、目前的提示詞（漫劇的，含 variant）。
- [ ] 共用子分頁：頻道立場、要避開的題材（`topic_avoid`）、每月 token 上限與用量、訂閱說明、AI 設定頁連結。
- [ ] AI 設定頁 `admin-video-model-settings.tsx` 多「漫劇各階段」：「跟教學一樣」勾選（存 `null`）與六個階段選單，`PUT /settings/models` 一起送。
- [ ] `admin-video-series.tsx` 與 `admin.json` 的「設定分頁要先開啟『AI 漫劇』」改成「漫劇設定要先開啟」並連到 `?tab=settings&section=drama`。
- [ ] 五個語系的 `admin.json`；vitest：三個子分頁各自只送自己的欄位、舊站沒有新欄位時頁面照常。

## Steps

- [ ] 殼與三個子分頁元件（`admin-video-settings.tsx` 留殼與共用，教學與漫劇各一檔）。
- [ ] AI 設定頁的漫劇模型。
- [ ] 字串與測試。

## How to verify

```bash
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-settings admin-video-model-settings
```

## Notes

- 加鍵與 namespace 的規矩看 skill `web-i18n-e2e`；同一頁不用改 e2e 的導覽清單。
- 「語言面板預先勾選」的意思在 `docs/videos/LANGUAGES.md`：只影響面板打開時勾了什麼。
