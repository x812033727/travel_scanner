---
id: 2026-11-01-so-thats-why-expand-the-reviewed
title: So Thats Why: expand the reviewed 1000-question pool to 10000 then validate 100000 scale
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-01T06:27:44Z
completed_at:
branch:
depends_on:
  - 2026-11-01-sothatswhy-candidate-pool
scope:
  - tools/video/so-thats-why/pool
  - docs/videos/so-thats-why/pool
---

# So Thats Why: expand the reviewed 1000-question pool to 10000 then validate 100000 scale

## Why

站主要求先完成 1,000 筆，再擴到十萬筆以上。首批在 `docs/videos/so-thats-why/pool/README.md`：1,000 個選入核心、32 個合併別名、226 個本輪來源與 12 組影片候選。本票承接後續擴庫，不表示擴庫正在背景執行。

## Definition of done

- [ ] 先以分批方式累積到 10,000 個不同核心候選，保留現有 ID、退題、來源與修訂關係，不以換物件／同義標題灌水。
- [ ] 保存來源更新到候選與影片的影響關係；補語意近似檢索的誤合、漏合抽查與調整紀錄。
- [ ] 每批報來源缺口、前提錯誤、候選轉 treatment 的實際數量與成本，未逐主張查核不升格。
- [ ] 在 10,000 實測基礎上再驗證 100,000 以上資料的索引、記憶體、去重與搜尋時間；不能把合成壓測列數算成可用素材。
- [ ] 用編輯採用與試讀結果回寫素材的保留／合併／退題，不把每題自動套成 13 分鐘影片。

## Steps

- [ ] 重新讀首批 README、VALIDATION、集中去重與獨立審閱，檢查碰撞再 claim。
- [ ] 先抽檢跨新舊題的漏合；修規則後才增加下批。
- [ ] 依真正新機制／條件補來源與題目，少量 treatment 優先證明故事價值。
- [ ] 若要大量付費模型、外站寫入或製作媒體，依當期授權與具體報價處理；本票不是花費授權。

## How to verify

首批基線：`node tools/video/so-thats-why/pool/cli.mjs check`；`node --test tools/video/so-thats-why/pool/pool.test.mjs tools/video/so-thats-why/catalog.test.mjs`。擴庫時另保存實際規模、來源抽查與效能結果；現有測試固定 1,000 的基線要以版本方式保留，不只是改數字讓測試過。

## Notes

- 100,000 規模效能與語意召回率目前未量測。當期去重會建立候選對，不能假設十萬筆同樣成本。
- 首批 121 筆歷史入選題只保留查核入口，需重新讀外站；新題生活例證有機制推導標記，進稿需補直接資料。
- 首批 46 筆合格候補、L151 暫緩與 57 個未另收錄提案均可查回，不應另發 ID 算新增。
