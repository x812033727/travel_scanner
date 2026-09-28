---
id: 2026-09-28-video-shorts-admin-automation
title: Video shorts W2: the topic library, the asset box, the weekly report and the automation settings on the Shorts tab
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-28T04:00:00Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-automation-api
  - 2026-09-28-video-shorts-admin-tab
scope:
  - apps/web/components/admin-video-shorts.tsx
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/components/admin-video-shorts-topics.tsx
  - apps/web/components/admin-video-shorts-topics.test.tsx
  - apps/web/components/admin-video-shorts-report.tsx
  - apps/web/components/admin-video-shorts-report.test.tsx
  - apps/web/components/admin-video-shorts-settings.tsx
  - apps/web/components/admin-video-shorts-settings.test.tsx
  - apps/web/components/admin-video-model-settings.tsx
  - apps/web/app/api/admin-video-shorts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video shorts W2: the topic library, the asset box, the weekly report and the automation settings on the Shorts tab

## Why

第二期工人開始自己做 Shorts 之後，站主要在後台看得到三件事：接下來會做哪些題目、哪些題目在等他的素材、上週做得怎麼樣與下週的安排。第一期的 Shorts 分頁（W1）只有月曆、片庫、成效、花費與基本設定。

設計全文在 `docs/videos/SHORTS.md`（§Shorts 分頁、§三條內容線、§排片與時段、§成效與每週報告）。

## Definition of done

- [ ] `?tab=shorts&view=topics`：依內容線分組的題目清單，每題顯示狀態、系列、鉤子、來源（企劃、企劃模型、站主、自動）；點開看完整規格（測試規格、真值核對、完成條件）。可以放棄一題、把一題排到最前面。
- [ ] 「新增想法」：一格文字加內容線；存成 `idea`，企劃模型下一輪把它補成完整的規格。
- [ ] 「匯入 15 題企劃」按鈕：把 `campaign.json` 的內容送到 `topics/import`；已經匯入過時顯示匯入了幾題、略過幾題。
- [ ] 素材箱：缺素材的題目列出需要什麼；上傳照片（分段上傳，照片先在瀏覽器縮到長邊 2,048 px 並拿掉 EXIF），必填拍攝者、拍攝日期、授權說明；上傳完題目變成可以做。
- [ ] `?tab=shorts&view=report`：每週一份，最新的在上面；內文是企劃模型寫的，底下附它引用的原值表（來源與讀取時間）與下週的排片。頁面不自己算任何數字。
- [ ] Shorts 設定多三組：各內容線的每週配額、庫存天數與鎖定時間、受測模型（兩組，各選供應商與模型；選單沿用 AI 設定頁的選項）。各階段模型的「跟教學一樣」勾選放在 AI 設定頁（`admin-video-model-settings.tsx`）多一塊「Shorts 各階段」。
- [ ] 改了會讓自動上架授權失效的設定（內容線、每天上限、時段）時，存檔前先說清楚「存了之後要重新授權」。
- [ ] 五個語系的字串；`npm run check:i18n` 過。
- [ ] vitest：題目的分組與操作、想法的送出、匯入的結果、素材的必填欄位、報告的顯示、設定存檔時送出的 body、授權失效的提醒。

## Steps

- [ ] 確認 W1 已合併；這張票的元件掛在 W1 的分頁殼上。
- [ ] 題庫與想法 → 素材箱與上傳路由 → 每週報告 → 設定。
- [ ] 測試與五語字串。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-shorts
```

## Notes

- 通用代理的請求上限約 5 MiB、nginx 單一請求約 6 MB：素材上傳要專用的路由，4 MiB 一段轉給 API。
- 元件檔不能有中文字面值（`check:i18n` 的規則 7，在 CI 或暫存之後才會跑）；顯示用的字都放 `admin.json`。
- 每週報告的內文是模型寫的文字：照純文字顯示，不要當 HTML 插入。
