---
id: 2026-09-28-video-shorts-tab-browser-spec
title: Video shorts: a browser spec for the Shorts tab against the fixture API
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-28T14:18:23Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-shorts-tab-browser-fixes
scope:
  - apps/web/e2e/admin-video-shorts.spec.ts
  - tools/e2e-runtime-api.mjs
  - .github/workflows/ci.yml
---

# Video shorts: a browser spec for the Shorts tab against the fixture API

## Why

Shorts 分頁（`/admin/videos?tab=shorts`）現在只有元件測試。元件測試的環境不做版面計算，回應是每個測試自己手寫的，所以分頁合併之後第一次在瀏覽器裡打開就找到六件事（`2026-09-28-video-shorts-tab-browser-fixes`）：頁面說錯狀態、金額寫成 0、表格欄位被擠扁。這些都要有一支真的在瀏覽器裡跑的測試才擋得住。

CI 的瀏覽器測試（`apps/web/e2e`）沒有任何一支打開這個分頁；`tools/e2e-runtime-api.mjs` 也沒有 Shorts 的端點，現在對著它打開分頁只會看到「讀取失敗」。

## Definition of done

- [ ] `tools/e2e-runtime-api.mjs` 回答 Shorts 分頁會問的端點，形狀照 `apps/api/app/video_shorts/schemas.py`：`/admin/video-shorts/overview`、`/uploads`、`/slots`（照 `from`、`to` 篩）、`/metrics`、`/costs`、`/settings`，以及 `/admin/videos?shorts=only` 與單支的 `/admin/videos/<slug>`。資料涵蓋八個狀態各至少一支、一格不發、一格空格、一支已下架、一筆不到 1 元的帳、一筆不知道金額的帳。
- [ ] `apps/web/e2e/admin-video-shorts.spec.ts` 在桌機與手機兩個 project 都過：五個子畫面各打開一次、資料真的畫出來（不是只等到沒有錯誤）、頁面不比視窗寬、沒有第一方的 404 與 console error。
- [ ] 片庫的封面載入（`naturalWidth` 大於 0）而且畫成 9:16；單支頁面的播放器是 9:16、高度不超過視窗。
- [ ] 反向驗證：拿掉一筆資料或把一項修正改回去，測試紅在預期的斷言上。
- [ ] 這支 spec 加進 `.github/workflows/ci.yml` 隔離測試的清單。

## Steps

- [ ] 讀 skill `web-i18n-e2e`（兩層假資料、登入與後台角色、flake 的教訓）；拿 `apps/web/e2e/admin-video-manual-upload.spec.ts` 當範本。
- [ ] 先補假 API，再寫 spec；本機用 `--repeat-each` 壓過再接進 CI。

## How to verify

```bash
cd apps/web && npx playwright test e2e/admin-video-shorts.spec.ts --repeat-each=5
```

## Notes

- 等待的條件（`2026-09-28-video-shorts-tab-browser-fixes` 截圖時踩到的）：伺服器先畫出來的是預設分頁，而且是空的；頁面讀到網址之後才換到 Shorts。要等「Shorts 分頁被選上」與「那個子畫面的資料出現」，不要等固定的時間。
- 片庫的卡片各自再讀一次那支影片（封面、長度、品管結果在審核裡），封面是延遲載入的：要先捲到卡片才會載入。
- 檔案走 `/api/admin-video-files/<slug>/<sha256>`，是另一支路由，假 API 要回真的圖片位元組與 `Range`。
- 成效區不能出現任何本站自己算的數字（合計、平均、比率、排名），spec 可以順便擋這一條。
