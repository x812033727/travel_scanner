# A01 第 12 輪來源完整性複核與候選修正 — HOLD

日期：2026-10-16。對象是 [A01 round12 隔離候選](A01-round12-candidate/README.md)，不是正式主機上的 A01。候選 `manifest.json` 的 SHA-256 為 `8c5dfadca9d26806afb510cf8bd85852dedd90ae280aaca971c8004e6c5b2725`。本表記錄原始資料與繼承裁決之間的衝突；它不是工人 verifier、listener 或劇情 panel 的審查收據。

## 五筆繼承的 `NOT FOUND`

第 11 輪的原檔與原裁決保持原樣；第 12 輪 [source-map.json](A01-round12-candidate/source-map.json) 的 `inherited_claim_reconciliation` 逐筆保留原 claim、verdict、note 和新候選狀態。以下只修正「來源不存在」這個事實判斷，不把舊場景自動恢復，也不把任何項目判成 `CONFIRMED`。

| 舊 claim | 原始資料中的定位與被推翻的理由 | 第 12 輪狀態 |
| --- | --- | --- |
| `o7` | [Kelly US2392926A](https://patents.google.com/patent/US2392926A/en) 說明書前段確有鐵路站搬運工稀缺、男女旅客搬重箱受苦的發明人陳述。原註記稱 source 9 沒有這段，與原件衝突。 | `origin-09` 不在候選 scenes；舊 verdict 留作歷史，不恢復旁白。 |
| `e11` | [Sadow US3653474A](https://patents.google.com/patent/US3653474A/en) 的 BACKGROUND 明列航空、鐵路與巴士航站旅客自行搬運。原註記稱 source 0 沒有鐵路、巴士，與原件衝突。 | `engine-04` 已退休；新 `r12e01` 以歸屬申請書的措辭重講航站問題，仍為 `PENDING`。 |
| `e3` | 同一 [Sadow 原始專利](https://patents.google.com/patent/US3653474A/en) 的 BACKGROUND 把行李搬運形容為航空旅客可能遇到的最大單一難題。原註記稱找不到這個說法，與原件衝突。 | `engine-05` 已退休；第 12 輪沒有恢復這個最高級說法。 |
| `n13` | [ABC News 2010 年原始訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469) 後段直接訪問空服員 Heather Poole，談到乘客把有輪行李裝太滿、離開輪子後難以搬動。原註記稱 source 6 沒有空服員或過量裝箱，與報導衝突。 | `now-05` 已退休；引語與空服員歸屬仍不進口播。 |
| `n14` | 同一 [ABC 原始訪談](https://abcnews.com/Travel/suitcase-wheels-turns-40-radical-idea-now-travel/story?id=11779469) 確有空服員歸屬；原註記稱「任何段落都查不到」，與報導衝突。 | 歸屬已從稿中刪除，但 `now-06/tszs` 的一般句「輪子能幫忙移動，卻不會減掉重量。」仍在場景中。候選把 `n14` 重新綁定到這句並改為 `PENDING`，待獨立查核。 |

Kelly 專利的直接頁面擷取於 2026-10-16 回 HTTP 200，原件 DESCRIPTION 的前段含上述搬運工敘述。Sadow 的 BACKGROUND 與 ABC 訪談亦在原始頁面逐段核對。這些都是原件含有相關文字的證據，不能直接證明每句舊口播的歸屬、強度或畫面已合格。尤其專利陳述是申請人的說法，不能轉成獨立市場統計；ABC 的受訪者觀察也不能寫成所有旅客的普遍情形。

## 本輪候選稿修正

- `origin-03/csdd` 畫面移除來源未指定的螺絲起子與固定手法，只畫館方敘述的輪子箱、木把手和匿名家人。
- `engine-r12-04/r12e04` 口播與畫面都明示這是 Sadow 專利的示例，避免把紙面輪組構造當成已核實的上市箱實物。依據是專利 SPECIFIC EXAMPLE 的輪組 23–26 與蓋／身底段 111／121。
- `turn-r12-01/r12t01` 的來源 map 同時具備 `source_index=12` 的 [Plath 1989 申請書](https://patents.google.com/patent/US4995487A/en) 和 `secondary_source_index=5` 的 [ABC／USA TODAY 2012 原始採訪報導](https://abcnews.com/Travel/rollaboard-luggage-celebrates-wheelie-big-birthday/story?id=17024603)，後者以 2012 年往前 25 年指向 1987 年車庫原型；兩份資料不能互代。
- `turn-r12-08/r12t08` 插圖提示詞增列偏心導件、套筒、上襯套之間的摩擦接觸，依據 Plath 專利 DETAILED DESCRIPTION 與 FIG. 4；不虛構按鈕或卡榫。
- `turn-12/6jx3` 畫面改成 1990 年代初期的匿名構圖，呼應 [Travelpro 自家年表](https://travelpro.com/blogs/the-travelpro-blog/the-history-of-rolling-luggage) 的 1991 年離職經營說法；不把當事人或實際轉職場景畫成紀實重建。`t13` 只綁 `6jx3` 這一句，原本獨立的 `3tsp` 仍由歷史 `t12/source 2` 支持，兩句不再混在同一 claim。

鏡頭提示詞只說主體、動作、構圖與光線；整部影片的可愛畫風由系列 `look.preset=cute-mystery` 設定，沒有在上述四筆 prompt 另指定風格。

## 驗證與未過的關卡

`build.mjs --write` 以第 11 輪六章的已綁定雜湊為輸入重建本候選，回報 79 scenes、108 lines、16 新鏡、22 條新增／改寫來源 map、`lintVideo` 0 error／38 warnings、`cuteStoryVisualProblems` 0 error。這只是本機機械檢查。以 300 units／分鐘的文字估時為 553.3 秒；320 units／分鐘估時 525.8 秒，低於 540 秒正文下限，實際 TTS 尚未量測。真實 worker verifier、逐章 listener、整片 narrative panel、真圖與成片品檢均**未跑**；第 9 輪正式 narrative panel 的 `chapters_link`、`payoffs`、`one_thread` 仍是 FAIL。本候選維持 **HOLD**，不得用本表代替審稿收據或啟動付費／匯入／上傳。
