---
id: 2026-09-28-video-shorts-admin-tab
title: Video shorts W1: the Shorts tab on /admin/videos with the calendar, the library, the 9:16 preview and the numbers
status: in-progress
priority: P1
area: web
owner: claude-fable-5-1-shorts
claimed_at: 2026-09-28T10:21:21Z
created_at: 2026-09-28T03:25:00Z
completed_at:
branch: claude/video-shorts-admin-tab
depends_on:
  - 2026-09-28-video-shorts-api
scope:
  - apps/web/components/admin-video-shorts.tsx
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/components/admin-video-shorts-calendar.tsx
  - apps/web/components/admin-video-shorts-calendar.test.tsx
  - apps/web/components/admin-video-shorts-data.ts
  - apps/web/components/admin-video-shorts-costs.tsx
  - apps/web/components/admin-video-shorts-costs.test.tsx
  - apps/web/components/admin-video-shorts-player.tsx
  - apps/web/components/admin-video-shorts-metrics.tsx
  - apps/web/components/admin-video-shorts-metrics.test.tsx
  - apps/web/components/admin-video-shorts-settings.tsx
  - apps/web/components/admin-video-shorts-settings.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-youtube.test.tsx
  - docs/videos/SHORTS.md
  - apps/web/app/api/admin-video-shorts
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video shorts W1: the Shorts tab on /admin/videos with the calendar, the library, the 9:16 preview and the numbers

## Why

站主 2026-09-28 的決定：「Shorts 區」是後台 `/admin/videos` 的一個分頁，而且全自動。現在的頁面只有「影片｜漫劇｜設定」三個分頁，播放器與圖片都假設 16:9（`aspect-video`），直式影片會被縮成中間一小條；沒有月曆、沒有成效、沒有花費。Shorts 一旦以新的格式出現在清單裡，還會混進「影片」分頁，因為那裡只濾掉 `drama`。

設計全文在 `docs/videos/SHORTS.md`（§Shorts 分頁、§一支 Shorts 的一生、§上架）。

## Definition of done

- [x] 分頁順序「影片｜漫劇｜Shorts｜設定」，`?tab=shorts`；子畫面 `?view=calendar|library|metrics|costs|settings`（題庫與每週報告在 W2 加）；`?video=<slug>` 照舊優先開單支影片。切換一律走 `adminNavigate`。
- [x] 「影片」分頁的清單帶 `shorts=exclude`，漫劇分頁的清單也帶；Shorts 不會出現在那兩處。`ProjectSummary.format` 的型別加 `shorts`，並多 `shorts_line`、`shorts_series`、`source_slug`、`shorts_state`、`slot_at`。
- [x] 頂列：自動上架的狀態（開、暫停、沒有授權、授權快到期）、今天與明天的時段、片庫夠幾天、本期花費與上限、頻道連結、工人上次回報、需要你的數量、90 天目標旁的 YouTube 觀看數。
- [x] 「需要你」：每一項一句話說要做什麼，按鈕直接做那件事。
- [x] 「等你上傳」（頻道還沒勾「稽核已通過」時才出現）：接下來幾天要上的清單、「下載這一批」（zip，走新的串流路由 `apps/web/app/api/admin-video-shorts/batch`）、三行步驟、「我上傳好了」與認領結果。
- [x] 月曆：一天一列、每個時段一格，顯示題目、內容線、狀態；可以換時段、指定影片、抽掉、標成不發。手機上是直向的清單。
- [x] 片庫與製作中：卡片有封面、長度、內容線、品管結果、排在哪一格。
- [x] 成效：每支已公開的 Shorts 一列，第 1、3、7 天與最新的數字；每個數字旁有來源與讀取時間；沒讀到的格子留白並寫「沒有在時間窗內讀到」。**不顯示任何自己算的分數、排名或百分比。**
- [x] 花費：帳目清單、補一筆的表單、三個 30 天區間各自的合計與狀態。
- [x] Shorts 設定與自動上架授權卡：沒有 `settings.manage` 時欄位唯讀，並照漫劇設定的寫法說明需要哪個角色。授權卡列出 `SHORTS.md` §自動上架授權 的每一項，按下去才送出。
- [x] 單支 Shorts 的頁面：9:16 播放器（高度不超過視窗的 80%、不裁切）、安全區遮擋的開關、兩個標題備案、說明、標籤、揭露、實測線的證據清單（檔名、SHA-256、下載）、品管 12 項、審核紀錄、`YoutubeSyncPanel`、放棄。`FinalBody` 的播放器與 `look`、`storyboard` 的圖片在 Shorts 上不再強制 16:9。
- [x] 五個語系的字串都在 `admin.videoShorts.*`（`admin.json` 裡新的一個物件）與 `admin.videoReviews.tabShorts`；`qaItems` 補上 Shorts 的新項目（`profile`、`loudness`、`layout`、`evidence`、`variety`）。`npm run check:i18n` 過。
- [x] vitest：分頁切換與網址、清單的篩選參數、狀態分組、月曆的操作送出的 body、沒有權限時的唯讀、成效的留白、直式播放器的尺寸類別。

## Steps

- [x] **先確認 PR #870 的狀態**：它大改 `admin-video-reviews.tsx`、設定元件與 `admin.json`。已合併就從 main 開工；還沒合併就等它，或疊在它的分支上（跟那條線說一聲）。
- [x] 讀 skill `web-i18n-e2e`（加鍵的規則、元件檔不能有中文字面值）。
- [x] 型別與篩選 → 分頁殼與頂列 → 月曆 → 片庫 → 單支頁與播放器 → 成效與花費 → 設定與授權 → 批次下載的路由。
- [x] 測試與五語字串。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-shorts components/admin-video-reviews components/admin-video-youtube app/api/admin-video-shorts
```

沒有本機 API 時預覽後台頁的做法：用一支假 API 回影片端點、其餘轉給 `tools/e2e-runtime-api.mjs`，再用 `npm --prefix apps/web run dev` 開頁面；側窗隱藏時改用讀文字的方式驗證，不要靠截圖。

## Notes

做完之後（2026-09-28）：

- 認領時用了 `--force`：工具說這張票跟四張 `review` 的票重疊（`2026-09-27-video-drama-room-web`、`…-drama-room-withdraw-a-one`、`…-languages-web`、`…-split-settings-web`）。那四張的工作都在 PR #870 裡合併了（2026-09-28），它們的分支在那之後沒有新的 commit，也沒有任何開著的 PR 在動這些檔案；票只是還沒被 `done`。那四張票我沒有動。
- 多了一個子畫面 `costs`：花費要有自己的地方放帳目與表單，塞進「成效」會讓「這裡的數字都是 YouTube 的原值」這句話不成立（花費是本站自己的帳）。
- 多了三個檔：`admin-video-shorts-data.ts`（型別與幾個純函式，沒有畫面，所以分頁與每個子畫面都能匯入它而不互相匯入）、`admin-video-shorts-costs.tsx` 與它的測試。
- 清單的網址變了（`/admin/videos?shorts=exclude`），所以 `admin-video-reviews.test.tsx` 與 `admin-video-youtube.test.tsx` 裡假的清單回應也跟著改。e2e 的假回應比的是路徑、不含查詢字串，不用改。
- 時段的時間是「月曆時區的幾點幾分」，不是瀏覽器時區的：換時段的輸入框用 `zonedInstant` 照月曆的時區讀（`admin-video-shorts-data.ts`），站主人在國外也不會排錯。測試涵蓋了加州換日光節約時間的那兩天。
- 片庫的卡片各自讀一次那支影片（封面、長度、品管結果都在審核裡，清單沒有），所以每一組先顯示 12 支，按了才多讀。
- 「90 天目標旁的 YouTube 觀看數」第一期沒有數字可以放：Data API 的頻道觀看數不分 Shorts 與長片，自己把每支加起來又是政策不准的衍生指標。頂列現在寫的是目標本身，加一句「要接上 Analytics 才讀得到」；數字等 `2026-09-28-video-shorts-analytics`。
- 單支 Shorts 的頁面不顯示「這支影片的語言」：Shorts 的語言是 Shorts 設定決定的，不是逐支勾。
- 標題、說明、標籤、揭露在這一版只能看與複製，不能在頁面上改；要改標題或說明，用既有的「送到 YouTube」表單（它本來就讓站主改這兩欄）。設計文件寫的「都可以改」留給之後的票。
- 授權卡只顯示伺服器給的條文（`consent.offer.text`），同意時送的是那段條文的雜湊；頁面不自己組條文。設定改了還沒儲存時不能同意也不能開跑，因為伺服器的條文是照已儲存的設定產生的。
- 沒有在真的瀏覽器裡對著真的 API 看過：本機沒有 PostgreSQL。元件測試之外，部署之後要實際打開 `/admin/videos?tab=shorts` 看一次（`2026-09-28-video-shorts-pilot-launch`）。

- 通用代理 `/api/travel` 把回應當文字讀、上限 10 MiB，請求上限 5 MiB：zip 下載一定要專用的串流路由（照 `apps/web/app/api/admin-video-files` 的寫法，傳 `Range`、`content-disposition`）。
- 影片預覽的檔案照舊走 `/api/admin-video-files/<slug>/<sha256>`。Shorts 的 `final` 審核裡 `preview` 就是成片本身（幾 MB），沒有另外的 720p。
- 加分頁不需要動導覽登記、側欄圖示、`navigation.*`、`pageHeaders.*`。側欄的數字只算待審的審核；「需要你」裡不是審核的項目（授權到期、等你上傳）要不要算進去，由 A1 決定，這張票照 `overview` 回的數字顯示。
- 手機上分頁是下拉選單，多一個分頁不會擠。
