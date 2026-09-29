---
id: 2026-09-28-video-story-admin
title: 後台的故事清單、匯入表單、每日支數與上架時段
status: done
priority: P2
area: web
owner: claude-opus-5-5-video-story-admin
claimed_at: 2026-09-28T14:27:24Z
created_at: 2026-09-28T03:31:15Z
completed_at: 2026-09-28T16:30:12Z
branch: claude/video-story-admin
depends_on:
  - 2026-09-28-video-story-api-series-kind
scope:
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/app/api/admin
  - apps/web/messages
---

# 後台的故事清單、匯入表單、每日支數與上架時段

## Why

站主的原則是一切在後台做、不碰命令列。品牌故事第一期用主機指令匯入清單（票 `2026-09-28-video-story-api-series-kind`），用既有的作品頁暫停與略過集數；這樣能上線，但站主看不到清單全貌，也改不了每天幾支。

## Definition of done

- [x] `/admin/videos` 的漫劇分頁裡，故事作品有自己的清單：每一列是一個故事（代號、標題、分類、排程日與時段、狀態、影片連結），可以篩選分類與狀態。
- [x] 清單上方顯示今天已開始幾支、每日上限、同時進行幾支、「可以上架」緩衝幾支，以及現在不開新故事的原因（如果有）。
- [x] 有 `settings.manage` 的帳號可以改每日支數、暫停作品、略過或恢復一個還沒開始的故事；沒有權限時看得到但不能改，並說明需要什麼角色。（API 的作品端點要的是 `content.manage`，頁面照 API；見 Notes。）
- [x] 匯入表單：貼上或上傳 `stories.json`，先顯示試跑結果（新增、更新、略過的列數與問題），確認後才寫入。
- [x] 「可以上架」卡片對故事預填下一個空的上架時段（12:00 或 20:00，台北時間）。
- [x] 五個語系的文字都有；`npm run check:i18n` 通過。

## Steps

- [x] 伺服器端如果缺端點（清單、改每日支數、匯入），在這張票的 web 轉送路由加；API 本身缺的另開票。（都不缺：清單與改每日支數在 main，匯入與恢復在 PR #936；既有的轉送路由夠用，量過，見 Notes。）
- [x] 元件與測試。
- [x] 五語文字。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

本機沒有 API 時預覽後台頁的方法見記憶「YouTube channel link」與 skill `web-i18n-e2e`。

## Notes

- PR #870 大改了 `admin-video-series.tsx` 與設定元件，Shorts 那條線也要在 `/admin/videos` 加分頁（`docs/videos/SHORTS.md`）；開工前先查誰在動同一批檔案。
- 新的後台頁或分頁要做的登記見 skill `backend-conventions`。
- 分鏡審核卡片的分頁聯絡表不用這張票做：PR #895 合併時已經一起做了（`admin-video-review-card.tsx` 的 `StoryboardBody`，測試在 `admin-video-storyboard-pages.test.tsx`）。
- 匯入指令多了 `--limit` 與 `--episodes-per-day`，作品多了 `look` 欄位（票 `api-series-kind`）；匯入表單要能選只匯入前幾個。
- 2026-09-28 認領（claude-opus-5-5-video-story-admin），用了 `--force`：`claim` 先因為相依的票 `2026-09-28-video-story-api-series-kind` 還在 `in-progress` 而拒絕。它的 PR #910 已在 2026-09-28T11:49Z 合併進 main（`3156370b8`），只剩結案的 PR #923 還開著。`--force` 同時蓋過了 scope 的重疊：四張 `review` 狀態的 PR #870 票（`video-drama-room-web`、`video-drama-room-withdraw-a-one`、`video-languages-web`、`video-split-settings-web`；#870 在 06:38Z 合併，遠端分支已刪，只是沒人跑 `done`），以及兩張 9 月過期的票（`ask-origin-airport-at-trip-creation`、`display-card-promises-language`，只持有 `newTrip.json` 與 `community.json`，這張票不碰）。那些票都沒有動。分支 `claude/video-story-admin` 從 PR #936 的分支 `claude/video-story-admin-import-api`（草稿，匯入與恢復的端點）開，再併 main；#936 合併之前，這張票的 PR 會帶著它的 commit。
- **做了什麼、在哪裡**：新元件 `apps/web/components/admin-video-stories.tsx`（測試 `admin-video-stories.test.tsx`）。漫劇分頁的作品清單下多一段「品牌故事」（`AdminVideoStorySeries`）：讀 `GET /admin/video-automation/series?kind=story`，每部故事作品一張卡（今天開始幾支／每日上限、同時進行、可以上架未上傳／緩衝、待做，以及不開新故事的原因），下面是匯入表單。打開故事作品時，`SeriesPage` 讀到 `kind: "story"` 就改畫 `StorySeriesPage`：沒有文件、篇章、「現在開始下一集」與免關卡開關（那些端點對故事作品本來就回 409）。`admin-video-series.tsx` 只動五處：import、`SeriesKind` 加 `story`、清單插入故事一段、`SeriesPage` 的切換，以及故事作品在第一次讀到之後不再讀合集清單（`/admin/videos?series=`；故事沒有合集，100 支影片時每分鐘白讀一次）。不是新的後台頁或分頁，所以不用 skill `backend-conventions` 的四處登記。
- **權限**：API 的作品端點（`PATCH /series/{slug}`、`/skip`、`/restore`、匯入的 `apply`）要的是 `content.manage`（「內容」與「Owner」角色），不是這張票寫的 `settings.manage`；頁面照 API，用 `useAdminActionGuard("content.manage")`。沒有權限時全部看得到、控制項不出現，頁面說明要 `content.manage`、哪兩個角色有、你現在的角色（角色名稱照成員頁的 `lib/admin-users-copy.ts`）。匯入的試跑只要 `content.read`，所以唯讀帳號也能試跑，只是沒有「確認寫入」。這些端點都不要 step-up（`STEP_UP_SCOPE_CAPABILITY` 只有帳號與資料庫維護）。
- **狀態**：清單的狀態從集數與影片推出來（`storyState`）：待做（`planned`、`ready`、`queued`）、製作中（`started`，或 `done` 但影片還不能上架）、可以上架、已排程、已上架（影片的 `publishState`）、完成（`done` 而沒有影片資料）、已略過、影片已放棄（影片有 `dropped_at`、集數還沒被標成略過；票 `api-policy-languages` 之後會標成略過）。分類、狀態的篩選與打開的故事都在網址（`story_category`、`story_state`、`story`），回作品列表時一起清掉。100 列都來自同一次作品讀取，沒有逐列的請求；逐支讀的只有「可以上架」的卡片（最多緩衝的幾支）。
- **「今天」與原因**：日期用伺服器的 `quota.day`（台北日期，只換成各語系的月／日寫法，不在瀏覽器算）。原因依 `hold` 代碼用五語的句子（數字取自 `quota`），不認得的代碼才顯示伺服器的 `hold_detail`（只有中文）。
- **匯入怎麼送（大小與逾時）**：頁面讀檔（或貼上）後在瀏覽器 `JSON.parse`，用檔案的 `series.slug` 決定路徑（在作品頁上就是那部作品；檔案寫的不同會先提醒，試跑也會拒絕），把 `{"file": <解析後的 JSON>, "apply", "limit", "episodes_per_day"}` 送到既有的轉送 `/api/travel/admin/video-automation/series/{slug}/stories/import`。送出前先量請求大小，超過 API 的 `STORY_IMPORT_MAX_BYTES`（4 MiB）就不送，並說出大小。真實的 `docs/videos/story-plans/brand-stories-100/stories.json`：磁碟上 1,414,653 位元組，頁面送出的請求 1,185,612 位元組；一路上的上限是轉送 5 MiB 與 15 秒、API middleware 5 MiB、nginx `6m`。2026-09-28 用 API 自己的測試工具（`tests/test_video_story.py` 的記憶體 SQLite、`tests/test_video_story_admin.py` 的 `_client`）把真實檔案走過端點：新作品試跑 0.62 秒（含暖機）、`limit 2` 加每天 1 支寫入 0.08 秒、其餘 98 個試跑 0.10 秒、寫入 0.13 秒、再試跑 0.10 秒（`leave_alone 100`）。離 15 秒很遠，所以**沒有加轉送路由**，`apps/web/app/api/admin` 沒動。正式站是 PostgreSQL，多幾次往返，量級不變。
- **422 自己讀**：網站的 `api()` 遇到非 2xx 只留一句話；匯入改用自己的 `fetch`（同樣的 `/api/travel` 前綴與 `X-Travel-Locale`），200 與 `video_story_import_refused` 的 422 都當報告讀，列出每一個問題；其他錯誤照 `apiProblemMessage` 變成一句話。問題與附註是 `stories.py` 的英文句子，原樣列出。
- **先試跑、確認才寫**：送出鍵永遠是試跑。報告記著它回答的是哪一份檔案（檔案每換一次就換版本）、哪部作品、`limit` 與每日支數；只有同一組、沒有問題、而且有東西要寫（新增、更新或建立作品）時才出現「確認寫入（新增 N、更新 M）」。之後改了任何一項，報告標成過期、按鈕消失。建立作品時的每日支數只在清單那一段的表單出現；作品頁的表單不送它（API 對已有的作品只會回一句附註）。
- **上架時段**：故事作品頁有自己的「可以上架」一段（教學清單的「可以上架」會濾掉漫劇格式，故事影片本來沒有這種卡片）。每個可以上架的故事一張卡：上傳包、送 YouTube 的進度，以及紀錄上傳的表單（沒連結頻道是 `UploadedForm`，連結了是 `YoutubePublishForm`），時間欄預填這個故事的下一個空時段。規則（`planSlots`、`nextFreeSlot`）：照企劃的時段（`beats.publish.slot`，12:00 或 20:00 台北時間；沒寫就兩個都行），至少比現在晚一小時；這部作品的影片已經排定的時間（`youtube_publish_at`，或正在送 YouTube 的排程時間）前後一小時內的時段算已占用；多張卡依企劃的日子與時段排序分配，彼此不重複。只看這部作品自己的排程，教學影片與 Shorts 不算。台灣全年 UTC+8，時段用固定位移算。
- **scope 加了兩個檔**：`admin-video-review-card.tsx` 的 `UploadedForm` 與 `admin-video-youtube.tsx` 的 `YoutubePublishForm` 各多一個可選的 `publishAt`（時間欄的初始值），其他不變。要預填，只能讓表單收初始值。兩個檔當時沒有活的持有者（只有已合併的 #870 留下的 review 票）；開著的 PR 只有 #935 動到 `admin-video-review-card.tsx`，改的是 `publishState`，不同段落。影片頁自己的「送到 YouTube」（`admin-video-reviews.tsx` 的 `SendToYoutube`）沒有預填，那個檔不在 scope。
- **沒做、另開的票**：故事作品頁每分鐘重讀整部作品，100 個故事時一次 1,197,209 位元組（每集帶企劃全文）→ 票 `2026-09-28-video-story-light-series-read`（API 的輕量讀法）；影片頁的 `OneOffBible` 為了找單集漫劇的故事聖經，對每一支漫劇與故事影片都每分鐘讀整部作品 → 票 `2026-09-28-video-page-reads-whole-series-for`。圖片模型與畫風（`image_model`、`look`）API 可以改，這張票只顯示圖片模型、不做表單（票沒有要求）。
- **反向驗證**：把試跑改成一律寫入、卡片的表單不預填時段、分配時段後不占用，三種改法讓預期的測試變紅（試跑的 3 個、分配的 2 個；預填的 1 個另外單獨改一次，紅在時間欄的值），還原後全綠。
- **併 main**：開 PR 前併了兩次 main。第二次（`57eb97b9b`）帶進 #904（`flat-explainer` 畫風，改了 `admin-video-series.tsx` 的常數與單集表單、五個 `admin.json` 的 `presets`）與 #939（`STORY.md` 的站主步驟與新票），git 自動合併、沒有衝突：兩邊的文字與控制項都在（`REQUEST_PRESETS` 與故事的切換並存，五語都有 `flat-explainer` 與 `videoStories`）。#939 的 `STORY.md` 第 6 步也寫明這些操作要 `content.manage`，與頁面一致。
- **整個 repo 的 typecheck 抓到的**：第一次 typecheck 在寫測試檔之前跑，所以沒看到新測試檔的兩個型別錯誤（fixture 的 `video` 與 `started_at` 被推成 `null`，展開與轉型編不過）；第二輪全套檢查的 typecheck exit 2 才抓到，改成明確的型別後 exit 0，測試內容沒變。
- **重做按鈕**：#939 的票 `2026-09-28-video-story-redo-dropped`（API：放棄的故事可以重做一次）說後台按鈕另開票；開了 `2026-09-28-video-story-admin-redo-button`，依賴它。在那之前，開始過、影片已放棄的故事在清單上只說「不能恢復」。
- **檢查（2026-09-29，這台 Windows，記憶體只剩約 0.5–1 GB）**：併 main（`57eb97b9b`）之後：`npm run lint:web` exit 0；`npm run check:i18n` exit 0（`Validated 5 locales across 25 namespaces.`；寫中文的檢查在 commit 前 `git add` 後也跑過，exit 0）；`npm run typecheck:web` exit 0；`node tools/tasks.mjs check` exit 0。`npm run test:web`（整套 334 個測試檔，一次一個 worker）**在這台沒有跑完**：兩次都跑了十幾分鐘還在跑，照這台的速度要好幾個小時，所以停掉，改跑動到的測試檔與依賴那兩個共用元件的：`npx vitest run components/admin-video-stories.test.tsx components/admin-video-series.test.tsx components/admin-video-youtube.test.tsx components/admin-video-reviews.test.tsx components/admin-video-storyboard-pages.test.tsx` exit 0（5 個檔、67 個測試）。整套交給 CI 的 `web` job。
- **沒有看到頁面畫出來**：記憶體不夠同時開 `next dev` 與測試，只有元件測試（jsdom）驗過，沒有用替身 API 在瀏覽器裡看過桌機與手機版面。下一個接手的人可以照記憶「YouTube channel link」的做法：替身 API 用真實的 `stories.json` 回 `series?kind=story`、`series/brand-stories`、`/admin/videos/story-*`，其餘轉給 `tools/e2e-runtime-api.mjs`。
