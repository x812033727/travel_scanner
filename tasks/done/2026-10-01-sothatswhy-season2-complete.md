---
id: 2026-10-01-sothatswhy-season2-complete
title: 原來如此第二季：完成剩餘64題處置與全部採用企劃後開總PR
status: done
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-01T12:14:37Z
created_at: 2026-10-01T12:14:35Z
completed_at: 2026-10-01T15:01:38Z
branch: codex/sothatswhy-season2-complete
depends_on: []
scope:
  - docs/videos/so-thats-why/season2/B28.md
  - docs/videos/so-thats-why/season2/B29.md
  - docs/videos/so-thats-why/season2/B30.md
  - docs/videos/so-thats-why/season2/B31.md
  - docs/videos/so-thats-why/season2/B32.md
  - docs/videos/so-thats-why/season2/B33.md
  - docs/videos/so-thats-why/season2/B34.md
  - docs/videos/so-thats-why/season2/B35.md
  - docs/videos/so-thats-why/season2/B36.md
  - docs/videos/so-thats-why/season2/B38.md
  - docs/videos/so-thats-why/season2/B39.md
  - docs/videos/so-thats-why/season2/B40.md
  - docs/videos/so-thats-why/season2/B41.md
  - docs/videos/so-thats-why/season2/B43.md
  - docs/videos/so-thats-why/season2/B45.md
  - docs/videos/so-thats-why/season2/B49.md
  - docs/videos/so-thats-why/season2/S28.md
  - docs/videos/so-thats-why/season2/S29.md
  - docs/videos/so-thats-why/season2/S30.md
  - docs/videos/so-thats-why/season2/S33.md
  - docs/videos/so-thats-why/season2/S34.md
  - docs/videos/so-thats-why/season2/S37.md
  - docs/videos/so-thats-why/season2/S38.md
  - docs/videos/so-thats-why/season2/S39.md
  - docs/videos/so-thats-why/season2/S40.md
  - docs/videos/so-thats-why/season2/S41.md
  - docs/videos/so-thats-why/season2/S42.md
  - docs/videos/so-thats-why/season2/S45.md
  - docs/videos/so-thats-why/season2/S46.md
  - docs/videos/so-thats-why/season2/S47.md
  - docs/videos/so-thats-why/season2/S49.md
  - docs/videos/so-thats-why/season2/S50.md
  - docs/videos/so-thats-why/season2/T27.md
  - docs/videos/so-thats-why/season2/T30.md
  - docs/videos/so-thats-why/season2/T31.md
  - docs/videos/so-thats-why/season2/T32.md
  - docs/videos/so-thats-why/season2/T34.md
  - docs/videos/so-thats-why/season2/T36.md
  - docs/videos/so-thats-why/season2/T37.md
  - docs/videos/so-thats-why/season2/T38.md
  - docs/videos/so-thats-why/season2/T39.md
  - docs/videos/so-thats-why/season2/T40.md
  - docs/videos/so-thats-why/season2/T42.md
  - docs/videos/so-thats-why/season2/T44.md
  - docs/videos/so-thats-why/season2/T46.md
  - docs/videos/so-thats-why/season2/T47.md
  - docs/videos/so-thats-why/season2/T49.md
  - docs/videos/so-thats-why/season2/T50.md
  - docs/videos/so-thats-why/season2/A26.md
  - docs/videos/so-thats-why/season2/A27.md
  - docs/videos/so-thats-why/season2/A28.md
  - docs/videos/so-thats-why/season2/A29.md
  - docs/videos/so-thats-why/season2/A30.md
  - docs/videos/so-thats-why/season2/A32.md
  - docs/videos/so-thats-why/season2/A34.md
  - docs/videos/so-thats-why/season2/A35.md
  - docs/videos/so-thats-why/season2/A38.md
  - docs/videos/so-thats-why/season2/A42.md
  - docs/videos/so-thats-why/season2/A43.md
  - docs/videos/so-thats-why/season2/A45.md
  - docs/videos/so-thats-why/season2/A47.md
  - docs/videos/so-thats-why/season2/A48.md
  - docs/videos/so-thats-why/season2/A49.md
  - docs/videos/so-thats-why/season2/A50.md
  - docs/videos/so-thats-why/season2/reviews/completion
  - docs/videos/so-thats-why/season2/completion-packaging.json
  - docs/videos/so-thats-why/season2/dispositions.json
  - docs/videos/so-thats-why/season2/validate.mjs
---

# 原來如此第二季：完成剩餘64題處置與全部採用企劃後開總PR

## Why

前九批完成36份第二季文字企劃，仍有64個原候選沒有製作層處置。站主要求全部處理完才開總PR，因此本票一次完成剩餘題目的去重、來源重讀、完整文字包與獨立審稿，再結清100題母票。

## Definition of done

- [x] 原100個ID與原始題目查核保留；每題有採用／換角度／同核心不採用的理由與證據，沒有待決或籠統延期。
- [x] 全部新增採用題有6章480秒長片大綱、18項無字prompt、2支180–220口語單位Shorts、後台前提／備註及長片與2Shorts的五語標題／說明。
- [x] 每份新增包由非作者獨立審稿；修正後重讀全文，報告及收據綁定最終SHA256。
- [x] 完成100題處置表、README索引、題庫製作指標與completion包；前九批117份既有產物逐位元保留。
- [x] 全批驗證、漂移拒絕、連結、欄位、語速及看板檢查通過；母票與本票結案後才開總PR。

## Steps

- [x] 查main、分支、worktree及開著PR的scope碰撞，認領母票與本票並建立完整批分支。
- [x] 分四類補完剩餘64題，逐題對照第一季、第三季、品牌故事與AI詞條／既有完整包。
- [x] 交叉審稿、修正文案與來源邊界，綁定收據及總處置審查。
- [x] 更新索引與驗證器、執行完整驗證並結案，作為建立總PR的前置交付。

## How to verify

`node docs/videos/so-thats-why/season2/validate.mjs --batch=completion`；同一路徑batch01至batch09逐批驗證；隔離副本測試包／報告／bundle雜湊漂移及未完成處置會被拒絕；`npm run check:tasks`；對照aa203808的前九批117份檔案SHA256；確認100題全有決定及新增包沒有媒體／匯入／發布完成宣稱。

## Notes

- 2026-10-01 全季交付：100原ID／題名／check／verdict及其餘原欄位保留；92採用文字包、8同核心不採用、0延期／未決。新增56包及全部採用包的非作者獨審完成，184支Shorts與長短片各五語共1,380組標題／說明。B45提前貨款、S50蘋果切面經完整舊稿覆核採窄角度；8重複題有完整既有稿與條目／來源hash。100題處置、入口、順序提案、收據與completion bundle已落地。前九批117份產物逐byte保留；十批驗證、22隔離漂移／錯誤拒絕與本地連結／JSON／原資料核對全PASS，詳docs/videos/so-thats-why/season2/reviews/completion/validation.md。A38範圍修正與A45去重ID修正皆重讀閉合；沒有未解決FACT。先結案兩票再開單一總草稿PR。#1073前六批已於13:37:59Z合併main；下列舊批次PR狀態是歷史快照，開總PR前再查現況。完整長片稿、音訊／圖像／成片、媒體與站主驗收、匯入、核准、排程及發布均不在本票完成範圍。

2026-10-01：分工root旅遊與商業審稿、write_b26商業與旅遊審稿、write_a31科普與科技審稿、write_t26科技與科普審稿。先完成全部文字再建總PR；既有PR狀態不代表本票已完成，未授權合併、部署、付費生成、正式匯入或上架。來源受阻需記錄實際取得結果，不把HTML殼、搜尋摘要或200狀態當全文證據。
