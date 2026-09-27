---
id: 2026-09-26-video-drama-admin-settings-and-gates
title: Video drama: admin settings section and look/storyboard review cards
status: done
priority: P2
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T07:17:16Z
created_at: 2026-09-26T01:53:26Z
completed_at: 2026-09-26T07:25:09Z
branch:
depends_on:
  - 2026-09-26-video-drama-settings-and-look-gates
  - 2026-09-25-run-the-site-s-claude-features
scope:
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video drama: admin settings section and look/storyboard review cards

## Why

站主要在 `/admin/videos` 的「設定」分頁看到並改漫劇的媒體設定，並在審核頁決定 `look`（每個角色選一張設定圖）與 `storyboard`（看分鏡聯絡表）。文案在五語 `admin.json`，這些檔案與 `admin-settings-panel.tsx` 正被 `2026-09-25-run-the-site-s-claude-features` 鎖住，所以這張票排在它之後（或它過期 24 小時後接手）。

## Definition of done

- [x] 設定分頁多一個 `video-settings-drama` 區：啟用、三種媒體的供應商／模型（沒金鑰的標「(沒有金鑰)」；模型選項帶單價與預覽版標記）、解析度與秒數依片段模型縮選（換廠商或模型時自動改成該模型有的值）、畫面比例、風格預設、上限與 judge 門檻、音樂／燒錄字幕／原生音訊／分鏡自動核准、角色聲音池（Gemini 聲音勾選）、每月預算與單支上限、漫劇題材；存檔送 `drama` 物件（`saveBody` 把題材文字框轉成陣列）。
- [x] 審核頁 `LookBody` 以 radio 卡片顯示候選圖（`candidate_<key>` 檔案）、judge 分數與評語、「judge 建議」標記，選了才能核准（「用這張」）；`StoryboardBody` 顯示每鏡關鍵影格、章節、秒數、提示詞、judge、待修標記、相鄰太像的警告、聯絡表；卡片標題帶角色名。列表對漫劇多「AI 漫劇」標籤與媒體花費（`format`／`media_usd`／`clip_seconds`，#797 之後才有值）。
- [x] 五語文案齊全（`videoSettings.drama*`、`stylePresets`、`videoReviews.gates.look|storyboard`、`chooseLook`、`candidate`、`suggested`、`approveLook`、`approveStoryboard`、`judgeScore`、`voice`、`lookAlike`、`seconds`、`shotNeedsReview`、`drama`、`spend`）；`check:i18n`、lint、typecheck、vitest 綠。

## Steps

- [x] `admin-video-settings.tsx`：型別加 `drama`、`media_options`、`style_presets`；`SETTINGS_KEYS` 加 `drama`；新區塊、`dramaNumberFields`、`mediaChoice()`。`usage.media` 沒做：伺服器的 `UsageView` 還沒有 media 欄位（`/video/media/status` 才有預算），留給 owner-controls-ui 票視需要加。
- [x] `admin-video-reviews.tsx`：`Gate` 加 look／storyboard；`LookBody`、`StoryboardBody`、`JudgeLine`；`needsChoice` 涵蓋 look；approve 標籤表。
- [x] 五語 `admin.json`（scratchpad 的 `add-drama-messages.mjs` 一次加進五個檔，保持兩空格 JSON）。
- [x] 兩個元件的 vitest（漫劇區存檔、模型縮選、聲音池；look 卡片選圖後才能核准、storyboard 卡片、列表標籤）。

## How to verify

```bash
cd apps/web && npm run lint && npm run typecheck && npm run test:web -- admin-video && git add -A && CI=1 npm run check:i18n
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 先確認 `2026-09-25-run-the-site-s-claude-features` 的 PR 已合併或認領已過期，再 claim。
