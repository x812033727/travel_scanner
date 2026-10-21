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
branch: codex/brand-stories-20261020
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
- [ ] 正式工人部署新系列配樂／插圖關卡；具 `content.manage` 的後台帳號先限額 1 試跑與匯入 B10，首支成片驗收後再匯入餘下四集。
- [ ] 正式工人完成劇本、媒體、視聽 QA、成片與上傳包。
- [ ] 首批完成後重查新題，接續匯入下一批；逐批延續而不重製。

## Completed work

- 首批 B10 無印良品、A30 IKEA、C15 Garmin、B11 UNIQLO、T04 捷安特已寫六章企劃、Treatment、來源研究與獨立查核。兩名代理重讀合計 48 個列入來源；`build.mjs` 由收據編譯出 `stories.json`。
- 本機開發資料庫的唯讀匯入乾跑通過：`accepted=true`、`written=false`、`create=5`、`refuse=0`。收據在 `research/local-import-dry-run.json`；這不代表正式站已匯入。
- 第二輪原生裝置配對回報 `allowed`、`saved`，語音狀態也通過。權杖保存在 `/workspace/.local/video-client/.mokaair/video-tool.json`，私人目錄0700、檔案0600，不曾在記錄中列印內容。
- 正式站上次成功唯讀取得完整 54 支漫劇影片清單，未見五集的新影片 slug；`brand-stories-new-20261020` 的 series context 回 404。正式站 automation enabled、drama.music_enabled。影片工具無權檢視所有未開工的跨系列企劃。後續雲端代理對 `mokaair.com` 回 CONNECT 403，不能再查詢；環境網路草稿已保存並待站主發布。
- 系統 `/usr/bin/chromium` 已通過 Playwright 官方 `executablePath` 的頁面與截圖 smoke；固定版瀏覽器下載遭 `cdn.playwright.dev` 403，原生 renderer 尚未整合測試。
- 程式修正與首批企劃已提交到 `codex/brand-stories-20261020`，原生 Git 推送成功；尚未建立 PR、合併或部署。分支與更新後的 `origin/main` 重整無衝突。重整後故事測試 33/33、影片文件測試 236/236、`npm run check:tasks` 通過；本機匯入乾跑再次新增5／拒絕0，未寫入。
- 首批系列已改預留總數 100 集，只為有來源的五題建立匯入列；工人做完現有列後安全等待新批次，不會自己編題。本機完整檔案試跑新增5／拒絕0，限額1的首支試跑新增1／拒絕0，均未寫入。五集旁白編輯參考稿與逐段主張索引在 `editorial/`；只供人工交接，不是工人正式稿或逐句查核通過。下一批五題重開來源均受雲端代理 CONNECT 403 阻擋，紀錄在 `research/next/`。
- 2026-10-21 再查，本地分支有 2 個未合併提交，GitHub 尚無 PR；附著執行環境仍是零自訂網域，`mokaair.com` 與已配對工具的唯讀設定查詢都無法連線。已將下一批五題舊來源缺少的網域及 `api.github.com` 加入雲端環境草稿，合計 50 個自訂網域；草稿已保存但仍需檢視、儲存並發布及新環境驗證。
- 下一批 A28 Levi’s、B13 養樂多、B19 寶礦力水得、K03 賓格瑞香蕉牛奶、A23 是拉差辣椒醬各完成一份新六章研究 Treatment，並由另一代理檢查敘事與來源語氣。草稿在 `next-drafts/`，全部明示未重查、不可匯入。首批五集的本地成本預查在 `research/budget-preflight-20261021.md`：10 分鐘撰稿目標每集 80 鏡，五集 400 鏡；沒有真實分鏡、文字／語音及重試完整報價。

## Current block and next action

影片工具權杖只涵蓋影片工具路由，不能對後台故事匯入 API 進行寫入。`/admin/video-automation/series/{slug}/stories/import` 的 `apply` 明確要求 `content.manage`，而管理員頁支援上傳或貼上編譯好的檔案、先試跑後確認。先部署本工作區 `tools/video/automation/story.mjs` 的新系列配樂／插圖關卡；否則正式工人可能按舊程式付費製作。部署後，具此權限的登入帳號依 `docs/videos/brand-stories-new-20261020/IMPORT.md` 對 `stories.json` 限額 1 執行正式站試跑；確認新增一、拒絕零，再人工比對跨系列題材與核對正式站成本護欄，沒有衝突才寫入 B10。匯入器只檢查 slug 衝突，不會判斷語意同題；首支成片驗收通過後再放行餘下四支。若衝突，換題並重新查核。不可把已配對工具權杖當成管理員憑證，也不可假造 worker `auto.json` 跳過審核。

2026-10-21 預算再查發現新五集 slug 尚未納入系統的全片 US$25 持久計費帳戶；通用媒體預設上限為 US$200，且不涵蓋文字與語音。此缺口須與上述配樂／插圖關卡一起修正、測試並部署，再確認正式帳戶與供應商價格；只修改後台通用媒體上限不足以守住全片 US$25。此護欄已在分支實作並另立工作票 `2026-10-21-guard-october-brand-story-batch-with`，仍待合併、部署及正式站帳戶核對；在此之前不得正式匯入 `hands_off: true` 的新系列。

匯入後用影片工具唯讀確認系列與首集狀態，讓正式工人逐集製作。新企劃的查核不等於逐字稿與成片 QA。新系列的工人專用關卡會在付費畫圖前檢查 70% 以上插圖與連續卡片最多三張；成片仍需再核對真實畫面與配樂。付費生成前仍須依品牌故事技能提供整批張數與總額，守每片 US$25 上限；上架由站主執行。

## How to verify

執行 `node docs/videos/brand-stories-new-20261020/build.mjs` 及 `npm run check:tasks`。正式站是否真的完成，只以後台匯入回報、系列工作狀態和成片 QA 收據為準；本機乾跑及影片清單不能替代。
