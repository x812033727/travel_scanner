# C14 CamelBak｜作者 v5 修稿收據（待獨立覆核）

- 日期：2026-10-23（台北時間）；作者：`codex-c14-script`；去向：[draft PR #1695](https://github.com/x812033727/travel_scanner/pull/1695)。
- 站主已採用 [Treatment](../treatment.md) SHA-256 `078DC1D77C46EB49BB6F27F60535F22775781E5963783BDA7C1F7625B1A8700E`、[來源矩陣](../source-matrix.md) SHA-256 `F8CF68AA36264DF18CDBE6ECD698D4AF1F22E405DEAADA8ED275B7685050587E`；本輪重驗且未改其位元組。
- 本收據只是作者交件。v4 [獨立逐句與逐鏡 HOLD](independent-v4-source-visual-review.md) 綁前版 SHA；v5 不繼承任何來源、畫面或純旁白 PASS。

## v5 作者檔案 SHA-256

| 作者檔案 | SHA-256 |
| --- | --- |
| [`script.md`](../script.md) | `B323E2775C2FCBFBDDB536F9E1A9884290430686A73ABBF765F4A3D8C20A31DB` |
| [`script-source-notes.md`](../script-source-notes.md) | `2958D6585119061C81994A839B61D156C7F5B2DDC26BD325952DEEED5E0C6823` |
| [`visual-plan.md`](../visual-plan.md) | `FFC378004F85A582133DB2FA00323C98A59437F6E7C011E308504817283DFC62` |
| [`visual-plan.json`](../visual-plan.json) | `3667BEBC13059A505114B0350159EDBA8CD8D96415CE7EC867CDDBD924440301` |

## 對 v4 HOLD 的作者修正

- **I10** 依 [CamelBak 地區品牌回顧](https://camelbak.co.nz/pages/about-us)說 Wemmer 將沿途訂單一筆筆傳真回工廠；不臆測單車店數、實際訂單數或當日成交細節。I03／I04 收窄為首款商品名稱與九〇年代初的**早期**山地車追隨者；I11／I12 只引出較晚口器文件的設計問題。
- **T05** 依 [US6070767A](https://patents.google.com/patent/US6070767A/en)區分 1998 年申請、2000 年授權；口播與字卡均稱「2000 年授權的口器專利」。[水瓶申請](https://patents.google.com/patent/US20060226110A1/en)引用前件，只證兩份設計文件的關聯；2006 年二月 [GearJunkie 展會報導](https://gearjunkie.com/uncategorized/outdoor-retailer-trade-show-winter-market-2006-gear-highlights)另證當時所見實物，五月販售仍只是預告，不把可選專利部件視為量產瓶零件表。
- O08、E06、E10、T04、T10、N08、N12、N14 移開審稿口吻，改由動作、具體設問與揭露承接。2003 寄送只作背水用途擴展，不當首次軍用或水瓶動機；N11 明示假設情境；2012／2014 百分比仍只指 CamelBak 當年**毛銷售額商品占比**。
- I03 圖不畫未證首款外觀；I10 用空白紙與泛用傳真機；N07 不把銷售占比畫成實體貨架；T18／N12 並列泛用使用情境而不畫逐店搬遷。全部插圖仍只是無標誌、無可讀字、無專利附圖、無真人重建的概念提示詞；後製卡片另放有來源的字。

## 機械核對與尚待關卡

- 74 個唯一口播 ID 對 74 個同序 JSON 鏡頭；每行有存在於註解的 S 來源；逐句依每分鐘 250 個口播字元重算鏡頭秒數。正文 **2,342 字元／1,917 漢字、紙上 562.3 秒**；加濃縮開場後 5 秒片頭與 21 秒 v4 片尾，總估 **588.3 秒（約 9:48）**。**沒有 TTS；正文實際是否 ≥480 秒未驗。**
- 58 幅概念插圖／16 張後製字卡；規劃插圖 **428.2／562.3 秒＝76.15%**，最長連卡 2；最長單鏡 **T16 11.3 秒**。只將新的「鉤」計入，排除「回收鉤」，按鏡頭終點及 H05 後的 5 秒片頭重算，最大空檔 **H05→O05 42.3 秒**；最後一鉤至正文結束 32.0 秒。這些都不是獨立敘事或成片畫面 PASS。
- `git diff --check` exit 0；結構、來源代號、畫風欄位、圖像禁項、圖時比例、連卡、片頭片尾和節拍的作者機械檢查 exit 0。`npm run check:tasks` exit 1，唯一錯誤是兩份既存未追蹤的 v4 獨立覆核 task 同 ID（`tasks/done/...` 與 `tasks/open/...`）；本作者未編輯、暫存或刪除它們。其餘是原有長期認領／範圍警告。

請另一位代理按以上**四個 v5 SHA**重開原件逐句及逐鏡覆核，再交兩位未讀本版的讀者純旁白盲讀。其後仍須自然語速 TTS、生成圖片逐張驗收、站主採用稿與分鏡、付費前整集報價。此輪沒有付費、匯入、上傳、合併、發布或部署。