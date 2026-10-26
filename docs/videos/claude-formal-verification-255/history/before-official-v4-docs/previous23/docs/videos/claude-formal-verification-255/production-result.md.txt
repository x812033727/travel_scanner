# 第三片製作與交付快照

截至2026-10-26T02:57:52.837112+00:00，繁中主體候選與EN實測M4A已交後臺；EN的actual-dub字幕、標題說明及已實際觀看縮圖亦於02:27:03.829Z完成六角色附件讀回。已通過音檢及交付為1／8。JA原句R1已真結束：105 checked／91 accepted／14 flags／0 unchecked，尚未ready，其餘六語未完成。final仍pending、八語批次未提交、overall=false。官方5/21 v4_416c素材已正常取得於隔離base，第三c8f主體候選尚未套用正式片頭尾。

## 凍結版本與實測

| 項目 | 實際結果 |
|---|---|
| 當前來源 | video `e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f`；claims `527048b6061d21f70e00475cc4790a46b0de6e536a37e8966402194a043fa9c6`；speech `8028c7320d9cab29`。 |
| 主體候選 | SHA `c8f4bf86b1bfcc66aa8dccfdf2c047469da56bad2461a0ef130e72988dd63ed5`，48226281 bytes，H264 1920×1080／30fps，AAC 48kHz stereo。 |
| 畫面與聲音時間 | 16813 frames／30＝560.4333秒影片；AAC及容器560.505秒，聲音尾端較影片晚0.071667秒。不能把容器時間誤稱影片時長。 |
| 正文 | outro前548.1333秒；扣除24.4秒冷開及outro後523.7333秒，實測均超過8分鐘。 |
| 旁白 | 105／105當前WAV／完整原文／spoken form／有效原生裁決雜湊綁定，0 flags／unchecked；64 exact、19同音／語助、13 Jev及9筆實際第二轉寫。 |
| 合成機械檢查 | −14 LUFS、TP −2.9 dBTP，93片段、101 states、279抽樣畫格與圖卡匹配；最長state 12.3秒。 |
| 核心QA | 11／11；stance .84、demo .92、advice .01、sponsor .04。這是當前主體與當時文字／縮圖／narration-timed CC的QA。 |
| 敘事 | 初版4／13、5／13；R1兩位新讀者均9／13、passed=false；八句修詞後是知情差異核對，仍9／13、false，非新盲讀。三項必要NO及章名advisory保留。 |

[當前旁白核驗](narration-current-layout-verification.json)、[表格版面差異獨審](table-layout-independent-review.json)、[主體候選檢查](main-body-candidate-verification.json)與[實際核心QA](qa-main-body-initial.json)各有自己的範圍。主體檢查檔的`qa_status:not_yet_run…`是21:34寫入時狀態，未覆寫歷史；22:38完成的QA收據及22:48交付pin才是後續結果。樣格觀看不冒稱全片逐秒播放。

## 真正已交付的範圍

2026-10-25T22:48:50.599Z，正常附件流程完成12段完整1080p上傳，server assembly驗證SHA／大小，再authenticated讀回 `evidence_zh_tw_1080p_mp4` 的SHA／大小。既有files／payload／11項QA皆保留，final review `00f2b388-712e-4886-9849-64e12e0f6bec` 仍pending；沒有改approval、語言選擇、YouTube狀態或提交language batch。

驗證是伺服器上傳組裝及有身分的role metadata讀回，**不是遠端二進位下載後重算SHA**。見[公開交付摘要](main-delivery-verification.json)。原始收據完整SHA `fed7607d0871f0f5e7db6c267f756c79b7dad3ea42a0befd2a2a0dae81043430`保留；公開版本是白名單摘要，不複製原始server／project回覆。

第三片當時合成因未安裝正式品牌package而先產主體候選。官方素材現在已由正常途徑取得於隔離base；第三c8f仍未套用，靜態outro及QA對null branding的容許不能當成品牌完成。須另行驗證／採用及重新綁定，追蹤[品牌缺件任務](../../../tasks/open/2026-10-25-local-first-build-without-branding.md)。若換版改時間軸或bytes，所有受影響CC／M4A／package／交付讀回都要重新綁定；此快照沒有改媒體或核准。

## 歷史英文音訊增量交付（2026-10-26T01:05:03.510145Z快照）

2026-10-26T00:27:20.776Z，英文原生音檢真正105／105、0 flags／unchecked；嚴格當前音訊核驗於00:41完成，80 exact、21 native Jev、4實際第二轉寫exact。cgit是Jev .89採認，不能改稱exact。101個實測視窗皆fit、最大tempo 1.15，沒有skipped或kept take。見[當前EN嚴格proof](localization/en-audio-audit.rich-stage-pass.json)。

英文M4A SHA94d4bfc1721615fe1c1e77cfc369dca17be15e6b569c68e032660db9ad006699，14552825 bytes，AAC 48kHz stereo，560.505秒，−14 LUFS／TP −2.0 dBTP。PCM為26900800 samples／48000＝560.433333秒；AAC尾端0.071667秒另列，不稱影片變長。

00:47:37.352Z，正常4段server assembly驗SHA／大小，再authenticated讀回dub_en與evidence_en_m4a。原files／payload欄位與歷史主片QA保留，新增英文補充下載；standard dubs payload、站主選擇、approval及final pending不改，未送正式語言批次。這不是遠端binary GET或下載後重算雜湊。見[公開白名單摘要](localization/en-delivery-verification.json)與[安全的完整helper交付收據](localization/en-backend-delivery-receipt.json)。

英文經歷初檢6旗、原句retake1剩2旗、retake2剩1旗、一次listener修詞後零旗；原始付費階段／失敗／capture未刪。最初嚴格auditor對stage字串的假設不符合實際rich object，因此第一次REVISE照存；修正的是checker的metadata契約，不是改stage／cache／轉寫迎合checker。見[原REVISE](localization/en-audio-audit.first-pass-revise.json)、[階段快照](localization/en-production-history-snapshot.json)與[八語交付狀態](languages-result.md)。

這次只交英文音訊，不宣稱八語或字幕整包完成。CC仍為narration時間軸草稿，必須按actual dub timings重產／核對；官方品牌片頭尾與整體DOD仍未完成。

## EN字幕／說明／縮圖已交付

02:27:03.829Z，正常checked-assets流程上傳四份資產，server assembly核SHA／大小，再authenticated讀回六角色：`captions_en`、`evidence_en_cc_srt`、`evidence_en_cc_vtt`、`description_en`、`evidence_en_metadata_txt`、`thumbnail_en`。原M4A雙角色仍94d4、105／105音檢不變；主體c8f、所有舊files／payload／QA與choices保留，final仍pending。這不是遠端binary GET、server approval或正式language batch。見[交付摘要](localization/en-caption-assets-delivery-verification.json)及[完整安全收據](localization/en-caption-assets-backend-receipt.json)。

EN原生字幕為actual dub timing，108 cues覆蓋105個source ID；SRT `c9511097d17f1600ef8ab366cf084ad4316080271b958de349f1e0bb3288f688`，VTT `60d2960b3072d0e8db60b096c99fa5aea50114ae39703081e34773050e5693ec`，零cue問題。Title及native composed description檔SHA `bb976ea9cb3e968da45ed74f5dd402ea7fb6b1b1a584608b5505652ed40e87ef`；實際觀看EN縮圖SHA `23ceca2fe0562b0ae9422cb583608ceea15d99c460f748ac584d1955540dad12`。八張native redraw與root contact view有據；原創圖內「容量8byte／接受」仍是繁中，沒有宣稱全部像素都翻譯。見[當前native資產proof](localization/en-cc-assets-current-proof.json)與[root視覺收據](localization/en-thumbnail-root-view.json)。

早先以檔名搜尋漏判縮圖不存在的[原收據](localization/en-cc-assets-earlier-missing-thumbnail-note.json)不覆寫；825820…9496的superseding proof實查八圖、native hash與完整bytes。當時native final沒有送CC；本次六角色才是實際附件交付，不把歷史本地準備倒稱已送。

## 八語與待辦

- EN已交音訊及字幕／標題說明／縮圖；仍未提交正式語言批次，整包不冒稱獲准。
- [JA R1真實capture](localization/ja-retake1-check.capture.json)為exit1、105／91／14／0；21句新WAV、84句原檔不變。u2xw先前OTHER後的一次合法ASR重試仍旗，沒有新增其TTS或手清旗。R2尚未啟動，TTS／ASR均hold。
- 其餘六語未完成音訊；JA dub-timed CC與其他本地草稿仍未驗收／交付。ES四、PT二、ID二共8項閱讀速度advisories保留；八語文字審查與早期39項靜態超額是歷史準備資料，不等同實際fit。
- 主體歷史QA11／11、敘事9／13 false及必要NO均保留；官方bookends待套用、全八語與overall DOD仍未完成。沒有YouTube公開、合併或部署。

見[languages-result.md](languages-result.md)、[localization-review.md](localization-review.md)、[production-progress.json](production-progress.json)與[收據索引](public-receipt-index.json)。
