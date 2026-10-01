---
id: 2026-10-01-sothatswhy-season2-production-packages
title: 原來如此第二季：把已查核候選題整理成製作包
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-01T04:54:16Z
completed_at:
branch:
depends_on:
  - 2026-09-29-so-that-s-why-vet-the
scope:
  - docs/videos/so-thats-why/season2/
  - docs/videos/so-thats-why/season2-topics.json
---

# 原來如此第二季：把已查核候選題整理成製作包

## Why

`docs/videos/so-thats-why/season2-topics.json` 保存 B/S/T/A 26–50 共 100 個第二季候選題。題目查核票已完成，每列都有 `status: checked` 與 `check` 報告；完成票明確留下「排進製作時才補完整包」的工作。目前沒有票承接第一季 week1–week15 格式的完整大綱、Shorts 稿、後台貼用包與包裝。

本票只接續這份已查核題庫。第一季已完成查核；品牌故事與 AI 名詞系列另有製作票，選題時須避免照搬相同問題／例子。

## Definition of done

- [ ] `season2/README.md` 列 100 題處置：選入製作包／延後／換角度／不採用，附理由、原 id、查核報告與對應包；分批處理，每批記交接。延後不假裝已寫完。
- [ ] 選入的每題都有 `season2/<id>.md`，沿用第一季完整包格式：逐條來源與查核日期、修正／限制、7–9 分鐘章節大綱、圖像注意事項、兩支 35–55 秒 Shorts 稿、長片與短片標題／說明、後台「故事前提／備註」貼用文字。
- [ ] 五語標題／說明包裝與 proposed 順序在 `season2/` 單獨保存；題號維持 26–50，不改第一季 `episodes.json`、`titles.json` 或 `schedule.csv`。
- [ ] 每個採用包有獨立查核／聽眾審稿交接；回寫候選題時保留 `check` 與來源，重大新事實重新查核，無法確認的刪除或標清限制。
- [ ] `season2-topics.json` 的包入口與處置可追溯；所有 100 題都有明確處置，沒有遺留未決項才可結案。完整包、候選題、已生成與已公開狀態分開。

## Steps

- [ ] claim 前查 worktree、遠端分支、PR；讀 youtube-video 技能與 `week1/B08.md`、`week15/A25.md` 的完整包格式。
- [ ] 讀 100 列的 `check`，對第一季、第三季、品牌故事與 AI 名詞題庫去重。先列處置與批次再逐批寫作，選題變更留理由。
- [ ] 處理跨季重疊：S50/S55、A29/A30/A70、A38/A58 的切入點先決定，記在本季交接，不能把同一解釋拆成新題目。
- [ ] 從既有查核報告寫大綱、兩支 Shorts、圖像／縮圖與包裝；新增事實與會變動的數字用製作當天的一手來源確認。
- [ ] 由不同代理審稿與查核，逐批落地；需新增／更正原 `topic-checks` 報告時另開精確 scope 票，不越出本票範圍。
- [ ] 檢查完整性、貼用欄位長度、順序及重複；回寫包入口與本季 README，不建立正式工作或發布排程。

## How to verify

`npm run check:tasks`；JSON 能解析、100 個 id 不變且處置完整，所有包與查核連結存在。核對 `DramaRequestIn` 當前欄位限制（舊包為前提 ≤4,000 字元、備註 ≤2,000），兩支 Shorts 稿符合原長度規格；審稿收據綁當次內容雜湊。沒有真實媒體就不填 QA、費用或播放結果。

## Notes

- 2026-10-01 補票，來源是已完成的 `2026-09-29-so-that-s-why-vet-the`；本次未重查 100 題外部事實。
- 候選題已查核不等於已有完整稿或發布許可；本票交付文字包，不付費生成、匯入正式站或上架。
- 100 題依選題結果逐批處理，不要求把不採用或延後題硬寫成完整包。要開始下一批先在 README 留精確 id 與目前進度。
