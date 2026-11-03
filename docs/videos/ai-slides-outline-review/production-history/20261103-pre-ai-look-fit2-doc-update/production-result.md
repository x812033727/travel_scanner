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

# 第四片製作進度快照

截至 2026-10-26T04:12:21.363Z，含**官方5秒片頭與21秒片尾的完整1080p新版，以及按當前影片對時的繁中CC／標題說明下載檔，均已交後台並讀回核對**。片頭接在首章濃縮段後，新成片既有fresh QA11/11不變。final仍是manual-review pending；已交付1/9個字幕語言（繁中），八外語已驗配音仍0/8，overall_complete=false。

| 項目 | 當前實際狀態與證據 |
|---|---|
| 凍結來源／音訊 | source `296fa0c93be25c7074ec50259db650f5663aca2324a5e0a16da2118406757c2f`、claims `2c56550a6ffde77c8ee781f909554a8c94c9f7d787f877fc34b4c385160778f7`、speech `a8055d3edb90bcda`未改。沿用完整相同118個已驗當前WAV／full intended／ASR收據，118 accepted、0 flags／unchecked；這次不宣稱新TTS或ASR。 |
| 官方片頭尾 | 真實official v4 package `416c8768d4d29f2e746a0c019d2d598ec367cbb66b0ff996841c523651a63e88`；placed pin `39d34ab0d563aff4143d88518e178fe57e769747772084c7e9b05f42f6aeda64`。body frame757插入150frames，907格回正文；18256格開始630frames片尾。詳[官方來源摘要](branding-v4/official-package-source-summary.json)。 |
| 新版1080p | SHA `c387af9dcd36a5f351ac6d347808e8d47b58bdd740b6db4814f30a019f111d1c`，58,584,900 bytes，1920×1080／30fps／18,886frames。視訊629.533333秒，48kHz雙聲道AAC／容器629.610秒，額外AAC尾端0.076667秒分開記，不稱視訊長度。-14.1 LUFS／true peak -2.8。詳[當前媒體證據](branding-v4/current-media-verification.json)。 |
| 原主體保護 | 新版`build/body.mp4`完整SHA精確等於舊3cdb，52,296,204 bytes；encoded video stream也相同。原canonical2096檔全部SHA不變、2070 protected copied檔無shared inode。原603.533333秒主體扣冷開與原outro仍566.133333秒，不用官方片頭尾補正文八分鐘。 |
| 當前QA | [新媒體原始QA](branding-v4/native-final-qa.json)11/11，綁c387新SHA。Jev立場.83／示範.76／建議.02／業配.08；27筆CC閱讀速度提醒原樣保留。沒有把此QA當八語配音或fresh narrative PASS。 |
| 後台實際下載 | [正常附件收據](branding-v4/main-download-attachment.json)：新主片14parts、舊主體13parts、舊preview4parts，各正常store complete；登入角色metadata回讀同SHA／大小。新current review `a0e0a6bc-aca6-4182-adf1-00fa8176937e`仍pending；沒有遠端binary重取驗hash。 |
| 舊版審核與實體 | 舊BODY review `532d5837-0036-4695-9535-97d0c6a6044b`為superseded，原files／QA／payload等metadata全保留。兩個原獨有blob以current live `evidence_history_body_1080p_mp4`及`evidence_history_body_preview_mp4`保留；沒有寫reserved renewal欄位、伺服器核准或設定。 |
| Helper真實歷史 | 舊ee1候選因真native GC會清逾1小時superseded-undecided舊blob而[REVISE](branding-v4/main-helper-earlier-revise.json)。新retained-body helper保留94純guards，獨審20額外負例及真native GC正反例通過；[獨審](branding-v4/main-helper-retained-peer-review.json)只作code/pure門檻，實際交付另由root收據證明。 |
| 繁中CC／說明真實交付 | [正常CC附件收據](branding-v4/zh-tw/backend-delivery-receipt.json)於04:12:21.363Z完成3個text/plain blob PUT及一次same-a0e append POST，5個下載roles已登入讀回。SRT `b1375188f1cafbdb776bb000f1fdf4268e9653df6ab4e879f3e1242989d88969`／11,607 bytes；VTT `07a2a11a857975277340e715e22ab6b39db3be366197d2bd3c8f088cce96761b`／11,251 bytes；標題空行說明TXT `410f0c49ae7ef5ebf79702555f10ac7ddbe8bcdaa5cf126217c4fc432f027e62`／3,203 bytes。118 cues、0閱讀速度提醒，chapter2=00:30；native帶CC標記標題及說明精確等於existing payload zh-TW。 |
| CC與metadata界線 | current final共11roles，原6refs／payload／manualQA11／舊review／history／八語選擇全未改。**字幕語言已交1/9（繁中）；外語CC0/8、外語縮圖0/8、外語配音0/8**。其餘8套local字幕仍為主旁白timing草稿，須依各語實際接受音軌重排；normal final payload9語文字不代表外語下載檔已交付。 |
| 八語音訊 | EN initial只有93/118 raw WAV，兩次native process已知settled429，第二次0新WAV；沒有M4A／fit／meter／當前音檢PASS。其餘七語亦未完成。保存逐句快取、原失敗、重錄上限與未知計費限制，不換provider／聲音／全局設定。詳[真實held收據](branding-v4/en-initial-synthesis-held.json)。 |
| 敘事與來源 | R2兩個12/13、passed=false、no_recap原樣保存；完整提示與必要算義的教學取捨未改。官方事實／原創示範／未親測限制仍見[verify5](verify-5.md)與[製作採用](production-decision.md)。 |

ZH helper210純guards（73+66+28+17+26）、獨立14額外負例與18個readonly子審負例通過；[精確count收據](branding-v4/zh-tw/helper-author-exact-counts.json)只更正原aggregate summary，原錯誤summary及完整tests均保留。實際交付另由root收據證明，不以peer代替runtime。

root已實看9格真實splice contact；本文件作者只核對其實際hash及root報告，沒有另稱全片人耳聽校。三個短review音檔已留在工作區，不把「已準備片段」說成完整人工觀看。

## 仍待完成

- 完成八外語當前M4A／fit／meter／完整目標音檢、依接受配音重排CC及逐語metadata／縮圖下載附件，再正常讀回驗證。
- 正常final核准與language batch仍待完成；不宣稱八語ready或全部新規則完成。沒有YouTube公開、合併或部署。

本次追加前的main-only29檔freeze與文件已[逐bytes封存](production-history/20261026-pre-zh-cc-doc-update/archive-manifest.json)，原freeze90bf保留；更早BODY當前文件亦[完整保留](production-history/20261026-pre-official-v4-main-doc-update/archive-manifest.json)。原[本體QA](body-core-qa.json)、[本體附件收據](main-download-attachment.json)及所有verify／失敗歷史仍保留。詳[機器進度](production-progress.json)、[後台附件摘要](branding-v4/current-backend-attachment-summary.json)與[收據索引](production-receipt-index.json)。
