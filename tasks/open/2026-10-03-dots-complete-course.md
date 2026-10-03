---
id: 2026-10-03-dots-complete-course
title: Implement OpenAI dots complete course
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-03T15:14:09Z
completed_at:
branch: codex/dots-complete-course
depends_on: []
scope:
  - docs/dots-series
  - tools/dots-series
  - tools/dots-series.test.mjs
  - apps/api/app/guides/series_data/dots.json
  - apps/api/app/guides/series_registry.json
  - apps/api/app/guides/publish_holds.json
  - apps/web/public/guides/dots-guide
  - apps/web/public/guides/dots-lesson-01
  - apps/web/public/guides/dots-lesson-02
  - apps/web/public/guides/dots-lesson-03
  - apps/web/public/guides/dots-lesson-04
  - apps/web/public/guides/dots-lesson-05
  - apps/web/public/guides/dots-lesson-06
  - apps/web/public/guides/dots-lesson-07
  - apps/web/public/guides/dots-lesson-08
  - apps/web/public/guides/dots-lesson-09
  - apps/web/public/guides/dots-lesson-10
  - apps/web/public/guides/dots-lesson-11
  - apps/web/public/guides/dots-lesson-12
  - apps/web/public/guides/dots-lesson-13
  - apps/web/public/guides/dots-lesson-14
  - apps/web/public/guides/dots-lesson-15
  - apps/web/public/guides/dots-lesson-16
  - apps/web/public/dots-course
  - apps/web/e2e/dots-series.spec.ts
  - apps/api/app/guides/content/dots-guide.json
  - apps/api/app/guides/content/dots-lesson-01.json
  - apps/api/app/guides/content/dots-lesson-02.json
  - apps/api/app/guides/content/dots-lesson-03.json
  - apps/api/app/guides/content/dots-lesson-04.json
  - apps/api/app/guides/content/dots-lesson-05.json
  - apps/api/app/guides/content/dots-lesson-06.json
  - apps/api/app/guides/content/dots-lesson-07.json
  - apps/api/app/guides/content/dots-lesson-08.json
  - apps/api/app/guides/content/dots-lesson-09.json
  - apps/api/app/guides/content/dots-lesson-10.json
  - apps/api/app/guides/content/dots-lesson-11.json
  - apps/api/app/guides/content/dots-lesson-12.json
  - apps/api/app/guides/content/dots-lesson-13.json
  - apps/api/app/guides/content/dots-lesson-14.json
  - apps/api/app/guides/content/dots-lesson-15.json
  - apps/api/app/guides/content/dots-lesson-16.json
  - docs/videos/dots-lesson-01
  - docs/videos/dots-lesson-02
  - docs/videos/dots-lesson-03
  - docs/videos/dots-lesson-04
  - docs/videos/dots-lesson-05
  - docs/videos/dots-lesson-06
  - docs/videos/dots-lesson-07
  - docs/videos/dots-lesson-08
  - docs/videos/dots-lesson-09
  - docs/videos/dots-lesson-10
  - docs/videos/dots-lesson-11
  - docs/videos/dots-lesson-12
  - docs/videos/dots-lesson-13
  - docs/videos/dots-lesson-14
  - docs/videos/dots-lesson-15
  - docs/videos/dots-lesson-16
---

# Implement OpenAI dots complete course

## Why

站主已核定 OpenAI dots 繁中完整課程：總目錄加 16 課、16 支 8–15 分鐘逐步畫面教學，以及六組可下載應用資料。現有網站尚無 dots 系列，需要沿用 ArticlePack 與系列 API，並把真實操作、資料變更、成片及公開結果分別驗收後一次推出。

## Definition of done

- [x] 17 篇文章通過既有內容包檢查、來源查核與獨立審稿。
- [ ] 02／03 樣本先通過畫面與旁白節奏驗收。
- [ ] 六個案例有真實 dots before／after、可開啟成果及核對紀錄；報表獨立計算。
- [ ] 排程真正執行；主工作、委派任務與排程各完成停止／取消驗證。
- [ ] 16 支成片正文各至少 480 秒，繁中 CC、實際章節、縮圖與遮罩檢查通過。
- [x] 既有系列 API 提供 dots，桌面／手機閱讀、提示詞複製及下載素材通過。
- [ ] 部署／發布與站主 Studio 上架後核對 17 個文章網址、16 個影片網址及播放清單。

## Steps

- [x] 查重、開票與認領，採窄路徑避免活躍 scope。
- [x] 當日官方文件查核，建立 16 課大綱與驗收規格。
- [x] 準備六組合成素材與第二版變更輸入。
- [x] 原創封面／概念圖解 17 組完成渲染與版面檢查。
- [x] 完成 17 篇作者原稿、16 份旁白及既有內容包整合。
- [ ] 真實帳號操作、媒體製作與全套驗收。
- [ ] 協調 apps/api/tests/test_guide_series.py 的窄 scope，更新 registry 既有固定預期。
- [ ] 相關 CI、發布及最終網址驗證。

## How to verify

離線內容與門檻測試：`node --test tools/dots-series.test.mjs`。

先在 PowerShell 設定 `$dotsWorkspace = Join-Path ([Environment]::GetFolderPath('UserProfile')) 'mokaair-work/dots-series'`，或指定其他 repo 外的製作目錄。

素材包：`apps/api/.venv/Scripts/python.exe tools/dots-series/package.py --workspace $dotsWorkspace`。

ArticlePack：`apps/api/.venv/Scripts/python.exe tools/dots-series/build.py --workspace $dotsWorkspace`，全部通過才可 `--install` 草稿；再執行 API 的 `python -m app.guides.pack_cli lint` 完整檢查。

真實證據與媒體門檻：`apps/api/.venv/Scripts/python.exe tools/dots-series/readiness.py --workspace $dotsWorkspace`。欠缺證據必須失敗，不代表工具故障。

Web：`npm run typecheck:web` 與 `apps/web/e2e/dots-series.spec.ts`；共用檢查 `npm run test:tools`、`npm run check:tasks`。完整驗收細節見 `docs/dots-series/ACCEPTANCE.md`。

## Notes

分支 `codex/dots-complete-course` 由當日 origin/main 建立。原有 `.codex/environments/` 不屬本票。

原始 screenshot、音訊、影片、實測紀錄保存在 repo 外 `<home>/mokaair-work/dots-series/`（`<home>` 為執行者家目錄）。17 個 slug 已設 publish hold；全套未驗收前不可解除。

另一張活躍票 `2026-10-03-illustrated-slides-round-2-a-family` 宣告整個 `apps/api/tests`。本票沒有越界修改；既有 registry exact-set 測試需更新 dots 預期，待窄 scope 協調。

2026-10-03：現有 dot 帳號已登入，可做合成資料實測。D03 獨立閱讀分享會的初版及期限／時間更新均正確，保存真實畫面與文字；資料不同於作者的讀書會示範，不能當作 canonical03 的完整驗收。既有 dot 原工作及帳號權限不做停止或授權測試。

第 13 課合成資料由 Python 作者計算及根代理 PowerShell 分別重算，第一版淨額 3140、第二版 5540，分類合計一致。dots 真實上傳第一批後，HTML 已開啟並下載到外部 evidence/13/report-v1.html，獨立核對 52 項數值／SVG 全通過，根代理檢視本機渲染文字與圖表清晰。實際計算 CSV 下載與第二版同任務更新仍待核對。

2026-10-04：17 份網站原稿、16 份旁白稿、16 份文字製作包及六套素材已完成交叉覆核與雜湊綁定；候選 ArticlePack 已安裝，發布 hold 保留。lint:web、typecheck:web、check:i18n、build:web 和桌面／手機六項 dots fixture 檢查已通過。完整 test:tools 在 Node24.19 有1467通過／5失敗／3略過；Hook失敗單獨重跑通過，其餘POSIX假工具與symlink權限問題其後查新main已有assemble portable／anime junction修正，本票未保留重複待辦，不宣告全CI綠燈。原始 Chrome 連線中斷後依站主要求改用內建瀏覽器，02建立、名稱讀回與兩版偏好回述已實測；canonical03還未成功送出，兩支樣本媒體仍待驗。

最終 P2 路徑修正通過：Node 3/3；Python 34 案例中32通過、兩個檔案symlink權限案例略過，directory junction 回歸有實際執行；獨立七次junction越界探測外部讀寫／安裝皆0。Ruff及17包重編譯通過，33個凍結來源未變。真實02操作、截圖覆核和來源SHA另存 reviews/lesson02-capture-log.json；readiness 仍應未就緒。IAB已保留示範分頁與復原viewport，DOM操作再次中斷；後續原始實測、02／03樣本、全套媒體與最後發布皆未完成，不能結案。

提交前修正 Windows 生成文字的換行／雜湊：所有生成文字為LF，原始來源與輸出副本SHA分開；33份凍結來源未改，142個製作輸出及56個compiler staging／install檔核對，四個Git index blob實際bytes驗證通過。相關Node3/3與Python34案例重新通過（32pass、2個檔案symlink權限skip）。

CI修正階段：目前不修改既有.github/workflows/ci.yml兩行，從本階段scope移除該檔以避開community-foundation活躍票。修正SVG無障礙、公開文件路徑與產生器，重跑真實pack_cli lint及repo hygiene。API registry一行仍待站主精確範圍例外。

CI run 37142483680 的三個根因已逐項確認：SVG 缺少標題／描述、公開文件硬編碼使用者路徑，以及 registry 固定預期未加入 dots。前兩項已修正；34 SVG production checker 零錯誤，編譯器補用既有 checker 及先失敗再修正的 regression。完整 1,170 包 lint、失敗過的生活包 pytest、dots／repo hygiene Node 6/6、Ruff、tasks check 均通過；Python 35 案例33pass／2個檔案 symlink 權限 skip。17 篇草稿與16份 brief 已重建，影片／公開狀態不變。registry 仍待精確範圍例外，不能宣告全CI綠燈。

registry 提案在記憶體中執行既有 test function：原版失敗，僅新增 dots 的版本通過全部 hub／vocabulary／catalogue 檢查，原測試 bytes 與 SHA 未變；`git apply --check` 通過。不是已套用或 CI 通過的證據。待辦保留 open，修正完成後交回占用範圍協調及尚未完成的課程實測／媒體製作。
