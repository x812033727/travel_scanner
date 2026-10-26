# 九語說明更新稿（初次交付時尚未採用的歷史稿）

這批稿件替繁中加en、ja、ko、es、pt、id、vi、th的完整影片說明，各增加一段[原創教具公開下載連結](../resources.md)。原有標題、完整本文、數字、否定、章節時間與來源均保留；新增段落使用各語言文字，說明教材為自行製作的CC0教具，並非Kimi模型輸出。

- [完整九語標題與說明JSON](metadata9-draft.json)
- [完整九語標題與說明TXT](resource-metadata9-draft.txt)
- [各語言新增的連結段落](localized-resource-blocks.json)

**這些保存初次交付時的DRAFT／REFERENCE ONLY狀態。** 初次交付時Canonical `video.json`、`i18n`及目前後台 `payload.metadata` 都維持原值；不能把附件或本地更新稿當作metadata已正式替換。當時正常採用與重審尚未完成。

九語草稿均以現行原生組成函式及正式片頭尾的實際時間軸檢查，完整說明皆低於5,000 UTF-8 bytes。每語只新增該連結段落；移除新增段落後，組成值與先前已讀回的完整九語metadata逐字相同。見[純函式組成驗證](../receipts/production/resource-supplement/pure-composition-verification.json)、[逐語新增差異](../receipts/production/resource-supplement/description-append-diff.json)及[ROOT獨立審閱](../receipts/production/resource-supplement/ROOT-resource-drafts-review.json)。

經當前音檔完整聽校的八語M4A仍為0/8。現有九語字幕對齊繁中旁白；正常QA仍為10/11、整體false，47項字幕速度與3項外語縮圖注意事項保留。這批說明稿不代表旁白、成片、語言批次或上架包已核准，也不改變既有音檢未知請求的處理規則。

原創ZIP由固定commit網址完整下載，並核對全部位元組、CRC與內容雜湊；官方模型、實際匯出及列印均未親測，教材的毫米、最小淨空與有限檢查限制見[教具說明](../resources.md)。後台新附件是否完成送達，須以該階段實際寫回的完整binary收據為準，本文件不預告尚未執行的交付成功。

台北2026-10-27 05:24，經獨立重審後，上述九語新增文字已透過正常metadata-only sheet/merge正式採用，並送回同筆後台待審後讀回核對。這裡的JSON/TXT與後台舊參考附件保持原始bytes及not_adopted歷史旗標；[最新實際採用與完整九語值](../receipts/production/metadata-adoption/README.md)另行保存，不能用本歷史稿的旗標推論目前未採用。八語M4A與核准依賴仍未完成。
