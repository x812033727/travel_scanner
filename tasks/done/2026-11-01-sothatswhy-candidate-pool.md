---
id: 2026-11-01-sothatswhy-candidate-pool
title: So Thats Why: deliver the first 1000 sourced candidate questions and film themes
status: done
priority: P2
area: tools
owner: codex-gpt6-7ba3
claimed_at: 2026-11-01T06:05:38Z
created_at: 2026-11-01T05:56:09Z
completed_at: 2026-11-01T06:30:57Z
branch: codex/sothatswhy-refresh-20261101
depends_on:
  - 2026-11-01-sothatswhy-episode-depth
scope:
  - tools/video/so-thats-why/pool
  - docs/videos/so-thats-why/pool
---

# So Thats Why: deliver the first 1000 sourced candidate questions and film themes

## Why

站主要素材池可累積十萬筆以上，再依內容厚度組成影片。規劃已在 `docs/videos/so-thats-why/refresh-20261101/POOL-STRATEGY.md`；目前只有 313 筆來源紀錄，沒有大型索引或批次擴庫。不得用同義標題或無來源答案灌成十萬列，也不能讓候選資料繞過逐集企劃和查核。

## Definition of done

- [x] 以現有 313 筆與原 ID／查核／退題理由建立可續跑的本機索引，不修改歷史包或正式資料庫。
- [x] 原始、核心、可選、入選、歷史／新研究來源、影片候選與已審劇本分開計數；未授予逐主張研究素材狀態。
- [x] 每個研究目標連到精確來源、小節、條件、查閱日期與前提狀態；完整答案仍待逐主張查核，未讀歷史連結不能升格為本輪閱讀。
- [x] 去重保留原 ID／提問變體／來源與修訂；歷史剔除、轉線、暫緩題不靠新標題復活。
- [x] 完成第一批 1,000 個選入核心；32 別名合併、1 新題暫緩、46 合格候補。10,000／100,000 的擴量和效能由後續票承接。
- [x] 12 組影片候選有共同追問、相接理由、章節預算、無聊與刪除條件；僅輸出 treatment 研究包，不呼叫製作 API。

## Steps

- [x] 開始前重新查工作樹、同 scope 任務與 PR；閱讀 CURRENT、POOL-STRATEGY、SPEC 及本機 selector。
- [x] 本機候選／來源／原始題／關係／修訂索引、preview、交易匯入及重複快照零寫入已驗證。
- [x] 作者之外逐題編輯審閱 911 個新候選；39 個批次來源頁獨立抽查，修正 5 題範圍措辭並保留提醒與抽查限制。
- [x] 交付可搜尋頁、完整資料、來源與去重帳、12 組候選；本輪沒有付費媒體／正式資料寫入，未量測十萬規模。

## How to verify

`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`（12 項）；既有 selector 與 long-form 473 筆檢查。瀏覽器查詢、別名、來源展開、分頁、主題篩選及手機版驗證詳 `docs/videos/so-thats-why/pool/VALIDATION.md`。抽查報告不宣稱整批事實全對。

## Notes

- 2026-11-01 已依使用者指示執行第一批；舊「僅記錄待做」描述已由本次實際結果取代。
- 《十萬個為什麼》是提問方向，沒有指定版本，也不授權複製整本問答。
- 先本機小批驗證，按使用需求再決定是否服務化；不要先開正式 DB migration。
- 已完成的 30 支候選只是編輯規劃，不是 30 支完成腳本或核准影片。
- 2026-11-01 站主明確要求開始做到 1,000 筆，去重、整理來源並挑可組片主題，再擴十萬以上。沿用同一 PR 分支；前置企劃已在 bdc10b47e 提交且獨立審閱完成，但票因搬移拒絕保留 review。claim --force 僅允許此已完成規劃相依，未覆蓋其他持有者或重疊 scope；無需先合併／部署。
- 後續擴量票：2026-11-01-so-thats-why-expand-the-reviewed。交付與修正證據在 pool/reviews；G01 主線統一、G10/G12 刪背景縮成 8–9 分鐘，未以補字維持片長。
