# 四語參考字幕27處閱讀速度修訂已交後台

2026-10-28T00:59:13.242475+00:00。日／西／葡／印尼語27句保義修訂經語義獨審及正常sheet／merge／captions，原27項CPS提醒→九語manifest零問題，原JA8／ES、PT、ID17門檻。

同pending final `a0e0a6bc-aca6-4182-adf1-00fa8176937e`／成片 `c387af9dcd36a5f351ac6d347808e8d47b58bdd740b6db4814f30a019f111d1c` 保原38完整參照，新四SRT＋四VTT＋TXT共47；新九檔完整GET bytes／SHA／MIME／UTF-8驗。[Mokaair下載](https://mokaair.com/zh-TW/admin/videos?video=ai-slides-outline-review)、[manifest](receipts/caption-pacing-20261028/captions-manifest.json)、[實際收據](receipts/caption-pacing-20261028/index.json)。

只屬已驗繁中旁白及official首章後5＋片尾21時序參考。未來25句仍超字數估計，完整列新增progress；未核准最終翻譯／配音或actual fit／meter／聽校。外語M4A／actualdubCC仍各0/8，無batch／server／整片核准。

原28progress值與歷史品質結果保持。

---

以下舊日期全文保留；舊27提醒為歷史，當前以新增caption_pacing_reference_only為準。

# 繁中完整節目M4A已交後台

2026-10-27T23:35:56.818396+00:00。既有官方v4成片已另交繁中完整節目[M4A下載](https://mokaair.com/zh-TW/admin/videos?video=ai-slides-outline-review)，保留第一章後5秒片頭及21秒片尾；AAC／容器均629.610秒。輸出17283377 bytes／SHA `74a61024d1f235b225b2f4a8945571c0bca5a01c190ca8b3f114b1ef65601b6f`，來源成片 `c387af9dcd36a5f351ac6d347808e8d47b58bdd740b6db4814f30a019f111d1c` 未改。

同一pending final `a0e0a6bc-aca6-4182-adf1-00fa8176937e` 保留原36份參照、完整payload／QA／審核與語言歷史，追加M4A與使用說明TXT，共38份；新兩檔均完整下載並逐bytes／SHA／MIME核對。

單次remux後只把來源衍生的mdhd與末stts欄位精確還原原值；原始AAC payload、全部29,511個packet時序／side-data、stts／elst／stsz及完整解碼PCM均相同，沒有重編碼、變速、重採樣、剪接或放寬門檻。118句沿用已驗當前WAV／完整intended／轉寫／timeline，來源綁定另獨審；本輪沒有新TTS／ASR或完整人耳重聽。詳[實際音檔manifest](receipts/original-zh-program-m4a-20261027/program-audio-manifest.json)及[安全文字收據索引](receipts/original-zh-program-m4a-20261027/index.json)。

原QA11/11、兩份敘事12/13 false、27項外語字幕速度提醒、EN93/118 raw及全部失敗／未知／重錄上限保留。已驗外語M4A仍0/8，八語actual-dub CC／正式語言批次及遠端final核准仍待，整片未done。

---

以下完整保留舊日期紀錄。當前M4A／38附件以本段及production-progress.json新增original_ZH_program_M4A物件為準；舊progress27欄原值未改。

# 公開PDF到有來源的四頁簡報

本片以本地原創四頁簡報示範大綱審查、集中修改、可編輯交付與回查來源，沒有Notebook產品實測。

最新交付（2026-10-27）：含官方5秒片頭與21秒片尾的1080p新版、繁中CC與標題說明，以及八外語各自的字幕參考稿、縮圖和完整標題說明TXT，已送到本片後台；目前待審版本共36個附件，經正常工具完整下載並核對每檔內容、SHA-256、大小與角色。成片仍待人工核准；外語已驗M4A仍0/8，整片尚未完成。[交付與完整讀回證據](receipts/foreign-reference-assets-20261027/README.md)。

八外語SRT依當前已驗繁中旁白時間軸製作，已包含首章後的5秒片頭位移。它們是參考稿，仍須在每語配音接受後按真正音訊重排；不能當作外語配音已驗。原QA11/11與27項外語字幕閱讀速度提醒、兩份敘事12/13 false及教學取捨完整保留，沒有新執行音訊合成、聽校或QA。

| 閱讀入口 | 內容 |
|---|---|
| [本輪後台交付與完整讀回](receipts/foreign-reference-assets-20261027/README.md) | 新增8字幕參考稿、8原生縮圖、8完整標題說明TXT與說明報告；current36完整讀回 |
| [製作結果](production-result.md)／[機器進度](production-progress.json) | 既有結果與最新實際附件、未完成項 |
| [製作採用](production-decision.md) | 原始授權、PR1860委派、來源／產品實測界線 |
| [新版1080p原始附件收據](branding-v4/main-download-attachment.json)／[QA](branding-v4/native-final-qa.json) | 2026-10-26官方新版上傳與QA；原有紀錄不倒改 |
| [新版實測](branding-v4/current-media-verification.json)／[官方素材來源](branding-v4/official-package-source-summary.json) | 18886frames／629.533333秒video／629.610秒AAC，5+21秒官方動畫 |
| [繁中CC／說明原始交付](branding-v4/zh-tw/backend-delivery-receipt.json)／[繁中標題說明TXT](branding-v4/zh-tw/title-description.zh-TW.txt) | 2026-10-26當前118 cues／0提醒；chapter2=00:30 |
| [前一輪11附件摘要](branding-v4/current-backend-attachment-summary.json)／[原helper獨審](branding-v4/main-helper-retained-peer-review.json) | 當時metadata-only讀回的歷史範圍；本輪完整binary讀回另留新證據 |
| [原本體附件](main-download-attachment.json)／[原本體QA](body-core-qa.json) | 原3cdb歷史，沒有改綁新版 |
| [八語文字／九CC初始快照](localization-initial-reviewed-snapshot.json)／[EN held收據](branding-v4/en-initial-synthesis-held.json) | 初始文字／縮圖與93/118 raw、0/8配音的實際限制 |
| [來源主張](claims.md)／[當前事實核驗](verify-5.md) | 數值、單位、母體、資料年及70/79未解註記 |
| [原創教材](data/DELIVERY.md) | 四頁PDF、可編輯PPTX與引用 |
| [歷史收據索引](production-receipt-index.json) | 舊時點SHA／大小與封存紀錄不變 |

後台：https://mokaair.com/zh-TW/admin/videos?video=ai-slides-outline-review 。主片為SHA `c387af9dcd36a5f351ac6d347808e8d47b58bdd740b6db4814f30a019f111d1c`，58,584,900 bytes；舊正文3cdb與舊preview另有live history附件。新附件保留原11refs與完整payload、manualQA、審核歷史及選擇；沒有伺服器核准或語言批次。

原公開教材沿用固定版本：https://github.com/x812033727/travel_scanner/tree/c8308b78321ad3ebc23bf516d1828203d07a40a8/docs/videos/ai-slides-outline-review/data 。PR保持no-auto-merge，不部署、不合併、不上傳或公開YouTube。
