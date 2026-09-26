---
id: 2026-09-26-video-hands-off-web
title: 影片交給 AI 決定：審核頁顯示 Jev 的理由與品管項目，加上「可以上架」清單
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-web
claimed_at: 2026-09-26T23:07:34Z
created_at: 2026-09-26T16:18:44Z
completed_at: 2026-09-26T23:47:02Z
branch: claude/video-hands-off-web
depends_on:
  - 2026-09-26-video-hands-off-judge
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_reviews_youtube.py
  - apps/api/tests/test_video_reviews.py
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 影片交給 AI 決定：審核頁顯示 Jev 的理由與品管項目，加上「可以上架」清單

## Why

站主不再逐關審核之後，`/admin/videos` 的用途變成三件事：看 AI 為什麼這樣決定、處理沒過的項目、拿到可以上架的影片（`docs/videos/HANDS-OFF.md` §上傳包與「可以上架」）。

## Definition of done

- [x] 大綱審核卡片：Jev 自動選的，顯示「Jev 挑選」標記與理由表，列出每個選項的 pick 機率、符合立場、有示範，以及 advice。
- [x] 成片審核卡片：列出品管項目，沒過的排在最上面並附細節；自動核准的顯示備註。
- [x] `/admin/videos` 的排序：
  - 最上面是「需要你」：等站主的審核與卡住的影片；
  - 其次是「可以上架」：「確認上架」已核准、還沒有 `youtube_video_id` 的影片。每支列出標題、長度、章節數、下載連結（mp4、縮圖、字幕、說明欄）、中文標題與說明欄與標籤的複製鈕，以及揭露要怎麼勾。
- [x] 「已上傳」表單：
  - 貼上 YouTube 網址，接受 youtu.be、`watch?v=` 與 Studio 的網址，解析出 11 字元的 id；上架時間選填；
  - 送到 `POST /admin/videos/{slug}/youtube`（ContentManager），存下 `youtube_video_id` 與 `youtube_publish_at`，寫稽核紀錄；
  - ProjectSummary、ProjectOut 與工具的 GET 都帶出這兩個欄位。
- [x] 標成已上架滿 7 天後，審核檔案區刪掉這支影片的 mp4。
- [x] 文案五種語言；加上 vitest 與 API 測試。

## Steps

- [x] API：schemas、端點、服務、檔案保留規則，加上測試。
- [x] 審核卡片：pick 表、品管清單。
- [x] 清單排序與「可以上架」卡片。
- [x] 表單與網址解析。

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_reviews.py tests/test_video_reviews_youtube.py -q
cd apps/web && npx vitest run components/admin-video && npm run lint && npm run typecheck && cd ../.. && npm run check:i18n
```

## Notes

- 下載用既有的 `apps/web/app/api/admin-video-files/[slug]/[sha256]/route.ts`。
- T8（`2026-09-24-video-youtube-sync`）完成後，同一張卡片的上架時間會改成由網站用 API 排程。

### scope 的增減（2026-09-27）

- `apps/web/components/admin-video-review-card.tsx`：開票後 #818 把審核卡片與各關卡的內容搬到這個檔案，pick 表、品管清單、上傳包與「已上傳」表單都寫在這裡；`admin-video-reviews.tsx` 只剩清單、影片頁與分頁。
- `apps/api/tests/test_video_reviews.py`：清單路由現在會先開審核檔案區（做保留規則），既有的 `test_admin_routes_need_content_capabilities` 用 AsyncMock session 讀不到設定，補上和同檔其他測試一樣的 `load_runtime_settings` stub（只改這一個測試的三行）。
- claim 時 judge 票還在分支上（PR #832 即將合併），用 `--force` 認領；伺服器端的規則（`payload.pick`、`payload.qa`、自動核准、同雜湊重判）都由那張票實作，這裡沒有重做，也沒有動 `submit_review`。

### 工人要送的 payload（給 `2026-09-26-video-hands-off-worker`）

大綱（`gate: outline`）與成片（`gate: final`）照 judge 票的合約：`payload.pick = { choice, probabilities: { key: p }, options: { key: { stance, demo } }, advice }`、`payload.qa = { ok, final_sha256, items: [{ id, ok, detail, warnings? }] }`，11 個 id 是 `assemble, render, narration, pace, captions, metadata, facts, links, thumbnail, policy, disclosure`。卡片把沒過的排最前面、`detail` 跟在後面、`warnings` 列在該項目底下；項目名稱用 `admin.videoReviews.qaItems.<id>` 翻譯，沒有翻譯的 id 直接顯示。

「確認上架」（`gate: publish`）的審核，卡片讀這些欄位（每一個都可以缺，缺了就不畫）：

| 欄位 | 內容 |
| --- | --- |
| `payload.package` | `{ ok, final_sha256, items: [{ id, ok, detail, warnings? }] }`，id 是 `files, descriptions, captions, disclosure` |
| `payload.minutes` | 數字，影片長度（分鐘） |
| `payload.chapters` | 數字，章節數 |
| `payload.locales` | 字串陣列，有字幕與說明欄的語系，例如 `["zh-TW", "zh-CN", "en", "ja", "ko"]` |
| `payload.zh` | `{ title, description, tags: string[] }`，站主要貼進 Studio 的 zh-TW 標題、說明欄、標籤（標籤用逗號接起來給複製鈕） |
| `payload.disclosure` | `{ synthetic: boolean, reason: string }`，Studio「變造或合成內容」要不要勾與原因 |
| `files[]` | `{ role, sha256, size, content_type }`，角色：`final`（final.mp4，`video/mp4`）、`thumbnail`（thumbnail.jpg，`image/jpeg`）、`captions_<locale>`（captions/<locale>.srt，`text/plain`；也收 `application/x-subrip` 與 `text/vtt`）、`description_<locale>`（description.<locale>.txt，`text/plain`）、`metadata`（metadata.json，`application/json`） |

`<locale>` 在 role 裡照語系原樣寫（`captions_zh-TW`，工人票 PR #836 就是這樣送）；為此 `ReviewFile.role` 的樣式從 `^[a-z][a-z0-9_]{0,39}$` 放寬成 `^[a-z][A-Za-z0-9_-]{0,39}$`，`ReviewFile.content_type` 多收 `text/plain`、`application/json`（以及 `application/x-subrip`、`text/vtt`）。卡片把 role 的字尾對回 `payload.locales` 裡的語系（大小寫與 `-`／`_` 都當同一個）當下載檔名，對不到就照字尾。工人現在送的 `payload.checklist` 一律是 `[]`，卡片沒有它也不畫那一段。同一份合約寫在 `admin-video-review-card.tsx` 的 `UploadPackage` 註解上。

### 伺服器端

- `POST /admin/videos/{slug}/youtube`：body `{ url, publish_at }`；`admin_service.youtube_video_id` 解析 `youtu.be/<id>`、`youtube.com/watch?v=<id>`（其他參數可有）、`youtube.com/shorts/<id>`、`studio.youtube.com/video/<id>/edit`、`embed/<id>` 與裸 id，其他網域一律 422 `video_youtube_url_invalid`。`publish_at` 是 pydantic `AwareDatetime`，沒帶時區在驗證就被擋；服務內再擋一次（`video_youtube_publish_at_naive`）。寫 `AdminAuditLog(action="video_youtube_linked", target="video_project:<slug>")`。再貼一次會覆蓋（改錯連結用）。放棄的影片 409。
- `ProjectSummary`／`ProjectOut` 多了 `youtube_publish_at` 與 `publish_approved_at`（「確認上架」最近一次核准的時間，清單用子查詢、影片頁從 reviews 算）。清單頁只有 summary，沒有它就分不出「可以上架」；這是票上沒寫、自己加的欄位。工具的 `GET /video/reviews/{slug}` 與 `GET /video/automation/videos` 共用這兩個 schema，所以一起帶出。
- `upsert_project`：工人的 `PUT` 沒帶 `youtube_video_id`（或帶 null）時，保留站主貼的那個——`tools/video/review/sync.mjs` 現在送 `youtube.video_id || null`，`automation/flow.mjs` 的 report 根本沒送，不改的話站主一貼、工人下一輪就清掉。原本「有 `youtube_video_id` 就整個檔案區清空」也拿掉，改成下面的保留規則。
- 保留規則 `prune_published_previews(session, store, now)`：有 `youtube_video_id`、「確認上架」核准（`decided_at`）滿 7 天、且有設 `youtube_publish_at` 時上架時間也滿 7 天的影片，刪掉 `content_type` 是 `video/mp4` 或 role 是 `final` 的檔案（成片與 720p 預覽都算），縮圖、字幕、說明欄留著。`GET /admin/videos` 每次先跑它（便宜、可重跑；沒有 mp4 可刪的影片只花幾個 stat）。沒有核准過「確認上架」的影片不會被清（站主可以放棄它，放棄照舊清空）。
- 「需要你」的定義：`pending > 0`，或工人回報卡住——`stage === "blocked"` 或 checklist 第一列 `key === "blocked"`（`tools/video/automation/flow.mjs` 的 report 就是這樣寫的）；沒有在伺服器加新旗標。
- 影片頁與清單用同一條規則判斷 mp4 是否已被清掉（`mp4Retired`），清掉後不再畫 mp4 的下載連結與 720p 預覽，改顯示說明。

### 前端

- 清單分五組依序排：需要你、可以上架、進行中、已上架、已放棄；每組內維持伺服器的順序（最後同步時間新的在前）。「可以上架」的卡片自己再抓 `GET /admin/videos/{slug}` 取最近一筆核准的「確認上架」，畫上傳包、複製鈕、揭露與「已上傳」表單；同一張影片同時有待決定的審核時排在「需要你」。
- 複製鈕用 Clipboard API，失敗時（非安全來源或被拒）把該欄位的文字選取起來並提示按 Ctrl+C。
- 「已上傳」表單前端先用同一套規則解析 id（`youtubeVideoId`），看不出 id 就不能送；`datetime-local` 轉成 ISO（帶 Z）再送。影片頁在「確認上架」已核准、還沒有 id 時也顯示這張表單，深連結 `?video=` 直接可用。
- `previewsGone` 的文案改成「mp4 滿 7 天後刪除，其餘留著」；新增的 52 個鍵五語都在 `admin.videoReviews.*`。
