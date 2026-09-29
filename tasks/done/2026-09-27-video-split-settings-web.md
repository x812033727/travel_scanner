---
id: 2026-09-27-video-split-settings-web
title: Video split settings web: the settings tab splits into tutorial, drama and shared, each saved on its own
status: done
priority: P1
area: web
owner: codex-p1-audit
claimed_at: 2026-09-29T02:12:04Z
created_at: 2026-09-27T06:16:00Z
completed_at: 2026-09-29T02:12:06Z
branch: codex/p1-task-audit
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

- [x] `?tab=settings&section=tutorial|drama|shared`（預設 `tutorial`，用 `useAdminQueryState`），三個子分頁各一顆儲存鈕，各自只送自己的欄位（`saveBody` 拆成三個；靠 API 票的「省略＝不改」）。
- [x] 教學子分頁：排程與題材、常設指示、頻道聲音、長度、語言預設（`caption_locales`，標為「語言面板預先勾選」）、輪數、預算與本月草稿、關卡（旁白、Jev 挑大綱、成片）、目前的提示詞（教學的）。
- [x] 漫劇子分頁：開關、題材、常設指示（`drama_stage_instructions`）、旁白聲音（勾「跟教學一樣」＝ `null`）與角色聲音池、語言預設（`drama_caption_locales`）、輪數（`drama_max_*` 與每鏡重做、每支片段數）、關卡（旁白、成片、設定圖自動選、分鏡自動核准、「劇本先給我看」＝ `series_script_gate`）、媒體模型、片段規格、風格預設、預算與本月媒體用量、作品的數字、目前的提示詞（漫劇的，含 variant）。
- [x] 共用子分頁：頻道立場、要避開的題材（`topic_avoid`）、每月 token 上限與用量、訂閱說明、AI 設定頁連結。
- [x] AI 設定頁 `admin-video-model-settings.tsx` 多「漫劇各階段」：「跟教學一樣」勾選（存 `null`）與六個階段選單，`PUT /settings/models` 一起送。
- [x] `admin-video-series.tsx` 與 `admin.json` 的「設定分頁要先開啟『AI 漫劇』」改成「漫劇設定要先開啟」並連到 `?tab=settings&section=drama`。
- [x] 五個語系的 `admin.json`；vitest：三個子分頁各自只送自己的欄位、舊站沒有新欄位時頁面照常。

## Steps

- [x] 殼與三個子分頁元件（`admin-video-settings.tsx` 留殼與共用，教學與漫劇各一檔）。
- [x] AI 設定頁的漫劇模型。
- [x] 字串與測試。

## How to verify

```bash
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-settings admin-video-model-settings
```

## Notes

- 加鍵與 namespace 的規矩看 skill `web-i18n-e2e`；同一頁不用改 e2e 的導覽清單。
- 「語言面板預先勾選」的意思在 `docs/videos/LANGUAGES.md`：只影響面板打開時勾了什麼。
- 2026-09-27（claude-fable-5-1-video-split）做完，在分支 `claude/video-review-manga-workflow-fp1rpz`（接在 API 票的 commit 之後）：
  - `admin-video-settings.tsx` 留殼（載入、`?section=` 子分頁、共用區）與兩個子分頁都用的東西（型別、`settingsBody`／`tutorialBody`／`sharedBody`／`dramaBody`、`useSettingsSave`、`VoiceFields`、`InstructionFields`、`LocaleDefaults`、`StageModelList`、`PromptsList`）；教學在 `admin-video-settings-tutorial.tsx`，漫劇在 `admin-video-settings-drama.tsx`。三個各自 PUT 只含自己的欄位；`saveBody` 拿掉了。
  - 漫劇子分頁多了作品的六個數字（`series_*`，之前只在物件裡來回、沒有介面）、「劇本先給我看」（`series_script_gate`）、旁白「跟教學一樣」開關（`drama_voice` 為 null）、自己的常設指示、語言預設、輪數與兩個自動核准開關。「目前的提示詞」依格式分到兩邊，並顯示 variant。
  - AI 設定頁多「漫劇各階段」：勾「跟教學一樣」送 `drama_stage_models: null`，取消勾選時六個階段從教學的複製起。`PUT /settings/models` 現在固定送兩個鍵。
  - 字串：`videoSettings.usage` 拆成 `usageDrafts`（教學）與 `usageTokens`（共用）——**改了鍵名，站上若有對 `videoSettings.usage` 的文案覆寫會變孤兒**；`fields.caption_locales` 改標「語言面板預先勾選」；`instructionsHelp`、`voicePoolHelp` 改寫；新增 sections、saveTutorial／saveDrama／saveShared、drama*、series 的 fields 等。`videoReviews.newDramaHelp`、`videoSeries.newSeriesHelp` 最後一句改成「漫劇設定要先開啟」，後面接 `openDramaSettings` 連到 `?tab=settings&section=drama`。
  - 2026-09-28 併 main（claude-opus-5-5）：main 的 #844 已把漫劇設定搬到漫劇分頁。站主選漫劇分頁，所以設定分頁只剩「教學影片」「共用」兩個子分頁，並放一顆按鈕連到漫劇分頁；`admin-video-settings-drama.tsx` 的欄位由 `admin-video-drama-settings.tsx`（#844 的外框：可收合、漫劇沒開時展開、唯讀時的角色說明）包著，缺金鑰警告也搬進來。存檔照這張的做法只送 `drama` 物件，不再用 #844 的「先重讀再整份送」。
  - 沒做：漫劇子分頁的「本月媒體用量」——後台的 `SettingsView` 沒有媒體用量（只在工人端的 `/video/media/status`），要另開 API 票才有；先只顯示預算。
  - 驗證：`check:i18n`（含 staged 的漢字檢查）、`lint:web`、`typecheck:web` 綠；`test:web` 315 檔 3396 案例全過；`admin-video-settings.test.tsx` 改成 7 個案例（三個部分各自儲存、深連結、舊站沒有新欄位、AI 設定頁的漫劇模型、唯讀）。
  - 接下來：`2026-09-27-video-split-settings-worker`。


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：claude-fable-5-1-video-split；原分支：claude/video-review-manga-workflow-fp1rpz。

- PR #870 merged; all required checks SUCCESS; all task checks complete.
- Task Notes record owner-approved change: drama settings live on drama tab after #844, rather than third settings subtab.
- apps/web/components/admin-video-settings.tsx:27 defines tutorial/shared; :199/:204/:208 separate save bodies; :439 points to drama tab; admin-video-drama-settings.tsx wraps full drama settings.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Close stale review task; retain note explaining why the final location differs from original three-subtab DoD.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
