---
id: 2026-09-28-video-shorts-admin-automation
title: Video shorts W2: the topic library, the asset box, the weekly report and the automation settings on the Shorts tab
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5-shorts-w2
claimed_at: 2026-10-02T06:11:51Z
created_at: 2026-09-28T04:00:00Z
completed_at:
branch: claude/video-shorts-admin-automation
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
  - apps/web/components/admin-video-shorts-data.ts
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

- [x] `?tab=shorts&view=topics`：依內容線分組的題目清單，每題顯示狀態、系列、鉤子、來源（企劃、企劃模型、站主、自動）；點開看完整規格（測試規格、真值核對、完成條件）。可以放棄一題、把一題排到最前面。
- [x] 「新增想法」：一格文字加內容線；存成 `idea`，企劃模型下一輪把它補成完整的規格。
- [x] 「匯入 15 題企劃」按鈕：把 `campaign.json` 的內容送到 `topics/import`；已經匯入過時顯示匯入了幾題、略過幾題。
- [x] 素材箱：缺素材的題目列出需要什麼；上傳照片（分段上傳，照片先在瀏覽器縮到長邊 2,048 px 並拿掉 EXIF），必填拍攝者、拍攝日期、授權說明；上傳完題目變成可以做。
- [x] `?tab=shorts&view=report`：每週一份，最新的在上面；內文是企劃模型寫的，底下附它引用的原值表（來源與讀取時間）與下週的排片。頁面不自己算任何數字。
- [x] Shorts 設定多三組：各內容線的每週配額、庫存天數與鎖定時間、受測模型（兩組，各選供應商與模型；選單沿用 AI 設定頁的選項）。各階段模型的「跟教學一樣」勾選放在 AI 設定頁（`admin-video-model-settings.tsx`）多一塊「Shorts 各階段」。（「Shorts 各階段」那一塊沒做：API 沒有欄位可以存，見 Notes 與 `2026-10-02-shorts-stage-models-the-api-saves`）
- [x] 改了會讓自動上架授權失效的設定（內容線、每天上限、時段）時，存檔前先說清楚「存了之後要重新授權」。
- [x] 五個語系的字串；`npm run check:i18n` 過。
- [x] vitest：題目的分組與操作、想法的送出、匯入的結果、素材的必填欄位、報告的顯示、設定存檔時送出的 body、授權失效的提醒。

## Steps

- [x] 確認 W1 已合併；這張票的元件掛在 W1 的分頁殼上。
- [x] 題庫與想法 → 素材箱與上傳路由 → 每週報告 → 設定。
- [x] 測試與五語字串。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-shorts
```

## Notes

- 通用代理的請求上限約 5 MiB、nginx 單一請求約 6 MB：素材上傳要專用的路由，4 MiB 一段轉給 API。
- 元件檔不能有中文字面值（`check:i18n` 的規則 7，在 CI 或暫存之後才會跑）；顯示用的字都放 `admin.json`。
- 每週報告的內文是模型寫的文字：照純文字顯示，不要當 HTML 插入。

### 2026-10-02 claude-opus-5-5-shorts-w2

- 認領時被兩張舊票擋住：`2026-09-27-video-drama-room-withdraw-a-one`（PR #870 已合併）與 `2026-09-28-drama-preloaded-document-approval-order`（codex-ten-drama，PR #978 已合併），兩張都是過期的認領，用 `--force` 認領。
- 加進 scope：`apps/web/components/admin-video-shorts-data.ts`（分頁的型別與 `VIEWS` 都在這裡，題庫、報告、受測模型的型別與上傳用的 `shrinkImage`、`sha256Hex` 也放這裡，測試才能換掉 jsdom 沒有的 canvas）。另外開了接續票 `2026-10-02-shorts-stage-models-the-api-saves`。
- **素材上傳沒有另開路由**，走既有的 `/api/travel` 通用代理：每段 4 MiB（4,194,304 位元組）在代理的 5 MiB 上限（`API_PROXY_MAX_BODY_BYTES`）與 nginx 的 6 MB 之內，照片又先在瀏覽器縮到長邊 2,048 px，通常一段就完。另開路由反而要重寫跨站檢查（`isAllowedMutationOrigin`）、session 續期，而且瀏覽器不會把 `admin_step_up` cookie（path `/api/travel/admin`）送到別的路徑。所以 `apps/web/app/api/admin-video-shorts` 沒有改。
- 縮圖：`createImageBitmap(file, { imageOrientation: "from-image" })` 畫到 canvas 再 `toBlob`，canvas 只帶像素，EXIF 自然不見；PNG 維持 PNG（手繪線稿），其他轉 JPEG 0.9。拍攝日期在 API 是選填，照票的要求在網頁設成必填。
- 「排到最前面」：同一條內容線、還能改的題目裡，有順序的最小值減一；已經在最前面就不動；最小值已經是 0 時，先把那幾題各往後挪一（PATCH `release_order + 1`）再把這題設 0。順序是全池共用的（`topics.order_key`），但排片是依內容線取題，所以只比同一條線。
- 每週報告：內文用 React 文字節點加 `whitespace-pre-wrap` 顯示，不轉 Markdown、不插 HTML。原值表只列「至少有一列有值」的欄位（判斷有沒有值，不是計算）；整數加千分位，小數照原值寫出，不四捨五入。來源與讀取時間沿用成效區的 `metrics.readAt`。
- Shorts 設定：每週配額、庫存天數、鎖定時間 W1 已經有了（內容線、節奏與時段兩塊），這次加「受測模型」一塊（A、B 兩組，選單是 AI 設定頁的 `model_options`，沒有金鑰的供應商標「還不能用」；B 不選就是跟 A 一樣，送出時不帶 `b`）與「一個月最多開始做幾支」（`max_per_month`）。存檔的 body 多了 `subject_models`、`max_per_month`。
- 授權失效的提醒：W1 已經在表單上方寫了提醒；這次在按儲存時再用 `window.confirm` 問一次（只在授權有效、而且改到內容線、每天上限、時段或時區時），取消就不送。
- **沒做「Shorts 各階段」**：`video_shorts_settings.stage_models` 欄位存在、`ai.stage_choice` 也會讀，但 `SettingsWrite`／`SettingsSave`／`SettingsView` 都沒有它，`SettingsSave` 是 `extra="forbid"`，網頁送了只會 422。要先改 API，開了 `2026-10-02-shorts-stage-models-the-api-saves`，`admin-video-model-settings.tsx` 這次沒動。
- 順帶發現（沒改，API 的契約）：素材上傳把拍攝者與授權說明放在查詢字串（`author`、`rights_note`），nginx 的 access log 會記下來。若在意，之後可以改成放在 header 或第一段的 JSON。
- 驗證：`cd apps/web && npx vitest run components/admin-video-shorts`（7 個檔、68 個測試全過）、`npm run typecheck:web`、`npm run lint:web`、`npm run check:i18n`（暫存後跑）全過。沒有在瀏覽器實際操作上傳（jsdom 沒有 canvas），縮圖那一步要部署後在後台試一張。
