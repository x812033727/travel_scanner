# 完整成片繁中音訊試聽（未完成聽校）

本次已在[該片後台](https://mokaair.com/zh-TW/admin/videos?video=kimi-k31-3d-delivery)交付可下載的完整成片繁中AAC M4A及114句索引TXT，同一待審紀錄現有28個附件，正常完整下載及Root逐檔實體SHA核對均完成。M4A為22,272,505bytes／SHA`74df3b198eda4da18228d8a75629a8ace0a4e4a15af8456bf8aa819b7d11223a`，後台角色`evidence_audio_audition_zh_tw`；索引TXT角色`evidence_audio_audition_index_zh_tw`。[音檔規格與來源](program-audition-artifact.json)、[114句索引TXT](program.zh-TW.pending.index.txt)、[完整索引JSON](program.zh-TW.pending.index.json)可查；音訊本體保留在影片後台與repo外工作區，沒有放入Git。

音訊直接複製目前12分36.733秒候選成片的AAC音軌，含第一章後5秒正式片頭及21秒片尾。真正比對全部35,473個AAC payload、完整解碼PCM及實際ebur128量測；這些證明內容與當前成片一致，沒有正規化、合成、修句、調速或新ASR。[原生技術證據](native-program-technical-proof.json)、[Root獨立媒體複核](root-independent-media-review.json)、[packet摘要](AAC-packet-identity-summary.json)、[PCM同一性](decoded-PCM-identity.json)與[響度比較](meter-comparison.json)分開保存。原始4MB packet逐列紀錄、PCM/WAV/M4A/影片、profile/release及privateproject均未複製進Git。

這是「未完成聽校」的繁中試聽候選，全部114句均待實際聆聽。既有主轉寫105/114：74句快取比對吻合、31句差異未判定、9句未完，第二轉寫未完成。它沒有完成旁白核准，也沒有新增八種外語配音；當前經音檔聽校的外語M4A仍為0/8。原QA仍10/11整體false，47項字幕速度與3項歷史縮圖提醒、R4兩項false、DFA sent journal及兩globalholds全部保留。

最初V3在admission的檔案集合過濾條件出錯，尚未執行任何媒體工具即失敗；[原失敗投影](producer-v3-admission-failure.json)保留原始private收據SHA，完整原錯誤留在scratch。修正一個否定條件後，先真跑[普通與outputs-aware兩項預檢](media-v4-both-preflights.json)，再完成[獨立V4實際流程](producer-v4-lifecycle.json)。原失敗未改成成功，也沒有清除原journal或flags。

此次後台僅附加兩個source audition附件，原26個FileRef與完整payload／metadata9／QAfalse／手動旗標／選擇及歷史均原樣。[後台更新摘要](actual-backend-audition-delivery.json)、[正常完整28附件清單](normal-final28-review-files.json)、[Root完整28實體驗核](root-final28-binary-readback.json)記錄實際結果。[更新前進度](before-audio-audition-progress.json)與[本次里程碑](actual-audio-audition-milestone.json)保留前後狀態。主片與本體、source a8及八語文字未改；既有字幕仍依繁中旁白時間，未稱外語dub時間。父票仍blocked，source/final核准、上架包及語言批次仍未完成。
