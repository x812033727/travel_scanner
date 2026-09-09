# 飯店審核續批（2026-09-09）

本批使用內建瀏覽器逐項核對，已由正常管理服務核准 **1 間飯店與 18 個訂房選項**，
正式資料已生效。沒有使用 Gemini、提高額度、部署或調整應用程式。

| 項目 | 本批核准 | 前台結果 |
| --- | ---: | --- |
| 京都威斯汀都酒店 | 飯店本體 1 | 新增公開飯店，原已核准 5 個選項同時可見 |
| 京都 Expedia | 9 個選項 | 威斯汀 1 個可見；其餘 8 個仍受待審父飯店限制 |
| 大阪 Rakuten Travel | 7 個選項 | 全部可見 |
| 東京 Agoda | 2 個選項 | 全部可見 |

## 目前狀態

| 類型 | 已核准 | 待審 |
| --- | ---: | ---: |
| 飯店本體 | 41 | 19 |
| 訂房選項 | 318 | 42 |

公開目錄為 **41 間飯店／227 個訂房選項**（本批前 40／212）。
京都 9 間、釜山 10 間飯店仍待審；42 個待審選項中，32 個尚缺已存的精確平台網址，
10 個已有網址但有未解條件。逐項理由與原始查核時間見 [remaining-items.json](remaining-items.json)。
不將先前「未找到」解讀為平台未販售，也不宣稱本批重新查核了所有保留項目。

## 證據與正常規則

- [iab-observations.json](iab-observations.json) 保存實際頁面名稱、完整地址、原始／落地網址
  與時間。來源研究檔只提供線索，不代替 IAB 證據；官方既有紀錄保留原查核日期。
- 大阪先查到的 7 個樂天日本站頁面確實有同館身分，但 `.co.jp` 不符合正常品牌規則。
  未放寬網域；另從實際搜尋結果找到 `.com` 全球站頁面，再逐一用 IAB 核對門牌。
  日本站觀察保留為排除證據，不進入審核修改。
- 東京 Gracery 保留實際 `/zh-tw/` 落地 URL；Tawaramachi 與 Asakusabashi 分館沒有混用。
  Expedia 以頁面實際 Location 地址核對；等待完成載入後重新檢查，沒有保存誤開相簿的 URL。
- 京都威斯汀的字面 Place ID URL 實際在 IAB 解析至相同飯店、完整地址及 Marriott 官網。
  沒有轉換 CID、猜測 ID 或擷取 Google 座標。
- 獨立座標重新讀取 Wikidata current 與固定 revision 2434981201 JSON，選取
  Q11288502 的 Japanese Wikipedia P143 座標陳述；兩份資料一致，其他 Skyscanner 陳述排除。
  保留京都市原始名稱／地址授權，再加入 CC0 座標來源。這是代表性飯店位置，
  不是測量過的入口，也不保證測量精度。見 [座標證據](westin-coordinate-evidence.json)。
- 正常區域、地圖、來源、DNS、重導向、URL、版本與授權規則全部保留。
  平台連線檢查為 Agoda 2 筆 healthy、Expedia 9 筆 unconfirmed、Rakuten 7 筆 ReadTimeout。
  後兩者憑實際 IAB 身分證據走既有人工核對流程，不宣稱連線健康；無 unsafe/unavailable 覆寫。
- 每筆正常 edit／review 版本 1 → 3；19 筆核准、0 筆 guard hold。
  沒有 property ID、有效房價、日期／房型選擇、訂房或分潤點擊。
  平台身分核准不等於報價 API 能力或分潤使用權。

## 驗證結果與明確保留

飯店資料驗證符合預期，但**嚴格的「所有供應商設定完全不變」驗證未通過**。
保留原始失敗 [strict-verification-failure.json](strict-verification-failure.json)，
沒有修改驗證器或重寫快照來製造全部通過。

實際原因是本批正常飯店修改開始前，同一管理帳號另有一筆版面設定更新：
`layout.alerts_enabled` 於 00:59:41 UTC 改變，並有 `layout_settings_updated` 稽核。
最早飯店正常修改在 01:00:29 UTC。備份與目前資料逐列唯讀比對確認，
15 組供應商設定中只有 layout 的 config／updated_at 不同，其他 14 列完整相同。
同一 actor 不能用來推論是另一個人；本報告只陳述不同的管理操作與時間。
未還原或覆寫該版面設定，也未輸出金鑰等設定值。

因此本批驗證結論是 **qualified：飯店變更已驗證，整體全不變驗收仍失敗**。
詳見 [concurrent-change-assessment.json](concurrent-change-assessment.json)、
[provider-config-concurrency.json](provider-config-concurrency.json) 與
[hotel-public-verification.json](hotel-public-verification.json)。

已獨立確認：

- 原 340 筆已核准、範圍外 401 筆完整飯店／選項列不變；保留 408 筆舊審核收據。
- 新增正常 edit 19 筆、review 19 筆與收據 19 筆，全部對應有效原管理請求。
- SQL 三相使用 REPEATABLE READ／READ ONLY，ROLLBACK 成功後才輸出；
  除兩組供應商設定集合指紋外，其餘 11 組相同，包括 9,929 筆歷史稽核、品牌、報價與點擊。
- 重播沿用相同 19 筆收據，全部 420 列不變；沒有新正常稽核或收據。
  after 與 after-replay 的全 13 組指紋相同。
- 三相各 6 城市 × 5 語系，共 90 次匿名公開 GET 均為 200／no-store。
  原 40 間飯店／212 個選項的公開欄位保留；公開新增符合本批核准及父飯店條件。
- 229 個離線測試通過（既有核心 92、操作器防護 60、獨立驗證器 77）。
  Scoped Ruff 與任務板檢查通過；本批不是應用程式變更，未跑部署或完整 CI。
- 新建 13,644,025 bytes 的 PostgreSQL 備份，還原索引可讀；目錄 700／檔案 600。
  未做完整還原演練，舊備份保留。服務健康，schema 0064；見 [preflight.json](preflight.json)。

基準時間 2026-09-09 00:32:08.141514 UTC；重播後快照 01:03:59.826605 UTC。
manifest 檔案 SHA256：`2a0b4c880d948c237822aba74194138d963977296f9fdd9abc0b1f41e1794d9e`。
證據僅提交本機功能分支；沒有推送、PR、合併或部署。

## 重驗

操作器使用部署 f752ce43 的應用程式檔案雜湊；舊工作樹的應用程式不能代替目前版本。
本機 PYTHONPATH 指向相同現行版本 `mokaair-planner-premium/apps/api`。

```powershell
python -B -m pytest --import-mode=importlib -q docs/hotel-review-remaining-20260909/test_operator_guards.py docs/hotel-review-evidence-20260909/test_operator_guards.py docs/hotel-review-evidence-20260909/test_verify_results.py
python -B docs/hotel-review-evidence-20260909/verify_results.py --manifest-sha256 2a0b4c880d948c237822aba74194138d963977296f9fdd9abc0b1f41e1794d9e
ruff check --config apps/api/pyproject.toml ops/hotel_review_evidence_20260909.py docs/hotel-review-evidence-20260909
node tools/tasks.mjs check
```

上方完整 verifier 應忠實重現 provider config 差異失敗；飯店／公開／重播的分項驗證
詳列在兩份 qualified 報告，不把它當成無條件通過。
