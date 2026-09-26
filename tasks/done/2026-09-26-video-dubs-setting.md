---
id: 2026-09-26-video-dubs-setting
title: Video dubs: the owner picks each video's dub languages on /admin/videos
status: done
priority: P2
area: api
owner: claude-fable-5-1-video-dubs-setting
claimed_at: 2026-09-26T18:32:25Z
created_at: 2026-09-26T17:59:10Z
completed_at: 2026-09-26T20:08:15Z
branch: claude/video-dubs-setting
depends_on: []
scope:
  - apps/api/app/models.py
  - apps/api/migrations
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/tests/test_video_reviews.py
  - apps/api/tests/test_video_reviews_integration.py
  - apps/api/tests/test_migration_0100_video_dub_locales.py
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages
---

# Video dubs: the owner picks each video's dub languages on /admin/videos

## Why

多語言音軌沒有 API：每條配音都要站主在 YouTube Studio 手動上傳（`docs/videos/DUBS.md`）。站主 2026-09-27 決定**不要**全站的 `dub_locales` 設定：每支影片都只做繁體中文；成片之後，站主在 `/admin/videos` 為那支影片勾選要配音的語言，工人只在那時做那幾條音軌，做完當一批送審（`dubs` 關卡），站主上傳到 Studio 後核准。這張票取代原本「設定分頁加 `dub_locales`、預設關」的設計。

## Definition of done

- [x] `video_projects` 多一欄 `dub_locales`（JSON 陣列，預設空；json 不是 jsonb），遷移接在 main 最新的 head 之後（實作時是 `0098`，這張是 `0100_video_dub_locales`；`2026-09-26-video-hands-off-settings` 也要用 `0099`，後落地的改號）。同一支遷移把 `ck_video_review_gate` 放寬到含 `dubs`。
- [x] `PUT /admin/videos/{slug}/dubs`（content.manage，body `{"locales": [...]}`，只能是 en、ja、ko、zh-CN、不重複），寫 `AdminAuditLog`（`video_dub_locales_set`），已放棄的影片拒絕（同 `drop`），回 `ProjectOut`。`ProjectSummary` 與 `ProjectOut` 都帶 `dub_locales`，工人現有的 `GET /video/automation/videos` 與 `GET /video/reviews/{slug}` 就看得到，不加新端點。
- [x] 審核：`Gate` 多 `dubs`（一批做好的音軌，附音檔，payload 形如 `{"locales": {"en": {"file": "en.m4a", "file_role": "dub_en", "status": "ready"}, "ja": {"status": "skipped", "reason": "..."}}}`）；`ContentType` 多 `audio/mpeg`、`audio/wav`。`dubs` 只有核准（表示「已在 Studio 上傳」）與附原因退回，沒有選項。
- [x] `/admin/videos` 的影片頁：清單下方、審核卡片上方多一節「配音語言」（`DubLanguages`：四個勾選、儲存鈕、一行提示；沒放棄的投影片影片才顯示，只有 `content.manage` 能改，以已存的語系當 key 讓別人的儲存會刷新、自己改到一半不會被每分鐘的重讀蓋掉）；`dubs` 審核卡片列出每個語系的狀態、跳過的原因與下載連結（`DubsBody`，用 payload 的 `file_role` 找檔）。五個語系的 `admin.json` 都有字串，`npm run check:i18n` 過。（協調 session 2026-09-27 補上這兩段，vitest 11 個案例全過、lint 與 typecheck 過。）
- [ ] 測試：欄位預設空、PUT 來回與驗證、已放棄拒絕、audit 列、`dubs` 送審與核准；遷移的整合測試（改了 CHECK，照 skill 要第三層）；元件的勾選、儲存、卡片。（API 與遷移的都有；元件只有 `dubs` 卡片核准的測試，勾選與音軌清單的測試跟著上一項。）

## Steps

- [x] 遷移、model、schema、service、admin API。
- [x] 元件、訊息檔。
- [ ] 測試與檢查。（API 側全綠；web 側見 Notes。）

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && PYTHONUTF8=1 uv run pytest tests/test_video_reviews.py tests/test_schema.py tests/test_migration_sql_dialect.py -q
# 只在 CI 跑（要 PostgreSQL）：tests/test_video_reviews_integration.py、tests/test_migration_0100_video_dub_locales.py
npm run check:i18n && npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-reviews
```

## Notes

- **2026-09-27 改號**：#822（漫劇系列）先落地並用掉 0099，這張的遷移改成 `0100_video_dub_locales`，`down_revision = 0099_video_drama_series`；gate 的 OLD／NEW 都保留 `script`，NEW 再加 `dubs`；models.py 與 schemas.py 的 gate 清單是兩邊的聯集。

- **web 部分的兩段最後由協調 session 補上（2026-09-27，同一條分支）**：`DubLanguages` 在 `admin-video-reviews.tsx`、`DubsBody` 與 `DUB_LOCALES` 在 `admin-video-review-card.tsx`，測試在 `admin-video-reviews.test.tsx`。下面是代理當時留下的紀錄：Claude Code 的 auto 模式分類器以「Modify Shared Resources」拒絕了兩個編輯（當時 `ReviewCard` 還在 `admin-video-reviews.tsx`；#818 之後型別與卡片都在 `admin-video-review-card.tsx`），其他編輯都過了：(1) `ProjectSummary` 型別加 `dub_locales?: string[]`，加 `DUB_LOCALES = ["en", "ja", "ko", "zh-CN"] as const` 與 `DubLocale` 型別（現在在 `admin-video-review-card.tsx`，要 export 給頁面用）；(2) `ReviewCard` 裡 `review.gate === "dubs"` 時渲染 `<DubsBody slug={slug} review={review} />`（同檔，放在 `PublishBody` 那行下面）。少了 (1) 勾選區 `DubLanguages`（四個 checkbox、儲存鈕 PUT `/admin/videos/<slug>/dubs`、提示 `dubsHelp`，放在 `admin-video-reviews.tsx` 的 `ProjectDetail`：過去的決定下方、`DropVideo` 上方，`!dropped` 才顯示）沒法編譯，少了 (2) 音軌清單 `DubsBody`（每個語系：`locales.<l>` 標籤、`dubStatuses.<status>`、`reason`、用 payload 的 `file_role` 或 `dub_<locale>` 慣例找檔給 `downloadTrack` 下載連結）不會顯示，所以這兩個函式先從分支拿掉，留下 `dubs` 卡片的標題、`approveDubs` 鈕與五語字串（`dubsTitle`、`dubsHelp`、`dubsSave`、`dubsSaved`、`dubsError`、`downloadTrack`、`dubStatuses.*`、`locales.*` 都已在五個 `admin.json` 裡）。要補上時由站主允許那兩個編輯（或把 session 切成 Manual 權限模式）再做，並加勾選與音軌清單的 vitest。
- 認領時 `claim` 因為 `2026-09-06-ask-origin-airport-at-trip-creation` 與 `2026-09-13-display-card-promises-language`（都是 9 月 19 日的認領、同一條已棄置的 PR #552 分支）鎖住 `apps/web/messages` 而拒絕；兩張都超過 24 小時沒動，所以用 `--force` 接手。
- 沒有專用的 BFF route：`drop` 也是走 `apps/web/app/api/travel/[...path]` 的通用代理（`api()` 送 `/api/travel/admin/videos/<slug>/...`，PUT 也在它的 export 裡），所以 PUT `/dubs` 同樣走它，不另開檔案。
- `dubs` 審核的檔案角色慣例：每條音軌的 `role` 是 `dub_<locale>`，語系小寫、連字號改底線（`dub_en`、`dub_zh_cn`）——`ReviewFile.role` 的樣式是 `^[a-z][a-z0-9_]{0,39}$`，`dub_zh-CN` 會被 422；payload 每個語系可帶 `file_role` 指名，頁面沒有 `file_role` 時照這個慣例找。工人票（`video-dubs-worker`）照這個送。
- `dub_locales` 存的順序固定是 en、ja、ko、zh-CN（schema 排序），不管站主勾的順序；同樣的選擇再存一次不會多一筆 audit。
- `docs/videos/DUBS.md` 在 #819 合併時已改成每支影片的選擇（「每支影片的選擇（不是設定）」一節），和這裡做的一致；它的票表寫 scope 含 `apps/web/app/api/admin/videos/[slug]/dubs`，但實際不需要（見上一條 BFF 的說明）。
- 遷移照 skill `backend-conventions`：revision id 不一定等於檔名、json 不是 jsonb、平行 session 會撞號。
- 配音一支約多 20,600 個 Gemini 字元；站主開始勾配音時，同時在後台把 `video_speech_gemini_monthly_character_limit`（預設 300,000）調到 600,000 以上。
