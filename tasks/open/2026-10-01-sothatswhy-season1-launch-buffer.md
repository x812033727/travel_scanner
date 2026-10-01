---
id: 2026-10-01-sothatswhy-season1-launch-buffer
title: 原來如此第一季：試片後建立首批庫存與開播交接
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-01T04:54:15Z
completed_at:
branch:
depends_on:
  - 2026-09-28-sothatswhy-pilot-3
scope:
  - docs/videos/so-thats-why/launch/
  - docs/videos/so-thats-why/schedule.csv
  - docs/videos/so-thats-why/operations.md
---

# 原來如此第一季：試片後建立首批庫存與開播交接

## Why

「原來如此事務所」第一季 100 集的查核與貼用企劃包已保存，但現有試片票只涵蓋 B08、S01、T01 三集。`docs/videos/so-thats-why/operations.md` 要求開播前有 14 集庫存，且庫存低於 7 集時降為隔日更；三集試片之後建立庫存、綁定長片／Shorts、確認 D1 與交接持續製作，沒有獨立票承接。

舊企劃總入口：`docs/videos/KNOWLEDGE-STORIES.md`。本票從試片實測接續，不重做 100 集題庫或另建一套產線。

## Definition of done

- [ ] `docs/videos/so-thats-why/launch/README.md` 列出三集試片結果、站主選定節奏、語言、費用上限、首批順序、生成與發布前需補的具體授權；待定欄位寫明，不能預填通過。
- [ ] 首批 14 集有逐集庫存表：source id、影片 slug、兩支 Shorts slug、素材／QA／上架包雜湊與保存位置、語言、站主觀看結果及剩餘關卡。試片三集計入 14 集，不重複開工；未完成的列仍標未完成。
- [ ] 在有具體生成授權後，14 集長片與每集兩支 Shorts 都完成必要媒體／語言檢查及站主驗收；媒體存 repo 外。若尚無授權，保留可審閱的提案與阻擋原因，本票不結案。
- [ ] 更新 `schedule.csv` 與 `operations.md`：以核准節奏整理 proposed 日期、長短片關聯、庫存 <7 的降頻規則，以及每 20 集數據檢討責任。實際 Studio video id／公開時間只在平台重讀確認後填；沒有授權發布時維持 `PROPOSED_NOT_SCHEDULED`。
- [ ] 寫出開播交接：是庫存完成／提案待批准／已排程／已公開哪個狀態，下一批誰接、資源與站主審片容量是否足夠；剩餘未解缺陷另開窄 scope 票。

## Steps

- [ ] 重新查本地、遠端及 PR，確認三集試片與畫風／Shorts 的真實驗收已完成，讀 youtube-video 技能及試片收據。
- [ ] 按 `episodes.json.release_order` 起草前 14 集清單：B08、S01、T01、A08、B06、S09、T05、S02、T02、A01、B01、S03、T03、A02；更動有理由與站主選定紀錄。
- [ ] 用試片實測估首批生成成本、圖片／旁白／訂閱額度、磁碟與站主時間；做具體提案，再按當次授權生成剩餘庫存。
- [ ] 逐集重查來源、產出及驗收，保存可續跑收據；不因一集失敗而盲目重試付費請求。
- [ ] 整理 proposed 排程與持續交接，只有獲得對應發布授權才執行 Studio 操作並記實際結果。

## How to verify

`npm run check:tasks`；檢查庫存表有 14 個不重複 source id、每個 id 都在 `episodes.json`，每集兩個 Short，文件連結與素材雜湊有效。對實際成片跑 `status`／`qa` 及 ffprobe 核對原規格；重新讀後台／Studio 記錄與站主觀看結果。只有文件或 HTTP 200 不算庫存／排程驗收。

## Notes

- 2026-10-01 補票；僅恢復舊企劃已要求的首批庫存與開播工作。本次未生成、部署、修改正式設定、排程或發布。
- 原試片票維持其 owner／依賴；沒有另開競爭的試片票。
- D1 2026-11-02 是舊提案，所有 100 集日期原為 `PROPOSED_NOT_SCHEDULED`。確認新節奏前不可沿用成已排程狀態。
- 本票不修改逐集腳本；若庫存製作需要在 repo 新增／改 `docs/videos/sothatswhy-<id>/`，先為當次批次開票列明精確 scope，再 claim，不擴張本票到所有影片。
