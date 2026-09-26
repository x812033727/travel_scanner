---
id: 2026-09-26-video-drama-admin-settings-and-gates
title: Video drama: admin settings section and look/storyboard review cards
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-26T01:53:26Z
completed_at:
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

- [ ] 設定分頁多一個 `video-settings-drama` 區：啟用、供應商／模型（沒金鑰的以現有 `noKey` 樣式停用）、解析度與秒數依模型縮選、預算與單支上限、風格預設、音樂／燒錄字幕／原生音訊／分鏡自動核准、聲音池；存檔送 `drama` 物件。
- [ ] 審核頁 `LookBody` 以 radio 卡片顯示候選圖，選了才能核准；`StoryboardBody` 顯示聯絡表、關鍵影格與 judge 摘要。
- [ ] 五語文案齊全；`git add -A && CI=1 npm run check:i18n`、lint、typecheck、vitest 綠。

## Steps

- [ ] `admin-video-settings.tsx`：型別加 `drama`、`media_options`、`style_presets`、`usage.media`；`SETTINGS_KEYS` 加 `drama`；新區塊與 `numberFields.drama`。
- [ ] `admin-video-reviews.tsx`：`Gate` 加 look／storyboard；`LookBody`（沿用 `OutlineBody` 與聯絡表 `img` 的寫法）、`StoryboardBody`；`needsChoice` 涵蓋 look。
- [ ] 五語 `admin.json`：`videoSettings.drama*`、`videoReviews.gates.look`／`storyboard`、`chooseLook`、`approveStoryboard` 等。
- [ ] 兩個元件的 vitest。

## How to verify

```bash
cd apps/web && npm run lint && npm run typecheck && npm run test:web -- admin-video && git add -A && CI=1 npm run check:i18n
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。 先確認 `2026-09-25-run-the-site-s-claude-features` 的 PR 已合併或認領已過期，再 claim。
