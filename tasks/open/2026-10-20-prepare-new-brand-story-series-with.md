---
id: 2026-10-20-prepare-new-brand-story-series-with
title: Prepare new brand story series with curio rules
status: blocked
priority: P1
area: docs
owner: codex
claimed_at: 2026-10-20T09:17:40Z
created_at: 2026-10-20T09:17:30Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/brand-stories-new-20261020
---

# Prepare new brand story series with curio rules

## Why

站主要求製作新的品牌故事影片，沿用奇聞檔案局規則，標題以 ` | 品牌故事` 結尾。首批先挑五題，完成後繼續做新題；製作選項採建議值，不再詢問偏好。

## Definition of done

- [x] 系列規格與首批五集企劃建立，標題後綴一致。
- [x] 五集來源重查、獨立 hash-bound 查核與可匯入檔完成。
- [x] 影片工具權杖配對並安全儲存，正式站現有影片及新系列唯讀預查。
- [ ] 正式工人部署新系列配樂／插圖關卡；具 `content.manage` 的後台帳號再執行匯入試跑、核對其他待做題目後寫入五集。
- [ ] 正式工人完成劇本、媒體、視聽 QA、成片與上傳包。
- [ ] 首批完成後重查新題，接續匯入下一批；逐批延續而不重製。

## Completed work

- 首批 B10 無印良品、A30 IKEA、C15 Garmin、B11 UNIQLO、T04 捷安特已寫六章企劃、Treatment、來源研究與獨立查核。兩名代理重讀合計 48 個列入來源；`build.mjs` 由收據編譯出 `stories.json`。
- 本機開發資料庫的唯讀匯入乾跑通過：`accepted=true`、`written=false`、`create=5`、`refuse=0`。收據在 `research/local-import-dry-run.json`；這不代表正式站已匯入。
- 第二輪原生裝置配對回報 `allowed`、`saved`，語音狀態也通過。權杖保存在 `/workspace/.local/video-client/.mokaair/video-tool.json`，私人目錄0700、檔案0600，不曾在記錄中列印內容。
- 正式站上次成功唯讀取得完整 54 支漫劇影片清單，未見五集的新影片 slug；`brand-stories-new-20261020` 的 series context 回 404。正式站 automation enabled、drama.music_enabled。影片工具無權檢視所有未開工的跨系列企劃。後續雲端代理對 `mokaair.com` 回 CONNECT 403，不能再查詢；環境網路草稿已保存並待站主發布。
- 系統 `/usr/bin/chromium` 已通過 Playwright 官方 `executablePath` 的頁面與截圖 smoke；固定版瀏覽器下載遭 `cdn.playwright.dev` 403，原生 renderer 尚未整合測試。

## Current block and next action

影片工具權杖只涵蓋影片工具路由，不能對後台故事匯入 API 進行寫入。`/admin/video-automation/series/{slug}/stories/import` 的 `apply` 明確要求 `content.manage`，而管理員頁支援上傳或貼上編譯好的檔案、先試跑後確認。先部署本工作區 `tools/video/automation/story.mjs` 的新系列配樂／插圖關卡；否則正式工人可能按舊程式付費製作。部署後，具此權限的登入帳號依 `docs/videos/brand-stories-new-20261020/IMPORT.md` 對 `stories.json` 執行正式站試跑；確認新增五、拒絕零且無跨系列同題，再寫入。若衝突，換題並重新查核。不可把已配對工具權杖當成管理員憑證，也不可假造 worker `auto.json` 跳過審核。

匯入後用影片工具唯讀確認系列與首集狀態，讓正式工人逐集製作。新企劃的查核不等於逐字稿與成片 QA。新系列的工人專用關卡會在付費畫圖前檢查 70% 以上插圖與連續卡片最多三張；成片仍需再核對真實畫面與配樂。付費生成前仍須依品牌故事技能提供整批張數與總額，守每片 US$25 上限；上架由站主執行。

## How to verify

執行 `node docs/videos/brand-stories-new-20261020/build.mjs` 及 `npm run check:tasks`。正式站是否真的完成，只以後台匯入回報、系列工作狀態和成片 QA 收據為準；本機乾跑及影片清單不能替代。
