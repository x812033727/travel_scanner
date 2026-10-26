# 第三片製作與交付快照

截至2026-10-26T01:05:03.510145Z，繁中主體候選的完整1080p與已核驗英文M4A均已送達[後臺影片頁](https://mokaair.com/zh-TW/admin/videos?video=claude-formal-verification-255)。英文音檢及下載交付為1／8，日文正在初次ASR、尚未通過；其餘六語未完成。主體核心QA歷史11／11與final pending不變，正式頻道片頭尾仍缺，整體製作未完成。

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

本producer沒有已安裝正式品牌bookend package／default；正式頻道片頭尾動畫及branding.json仍缺。靜態outro及QA對null branding的容許不能當成品牌完成。待合法官方素材、驗證及guard後另行處理，追蹤[品牌缺件任務](../../../tasks/open/2026-10-25-local-first-build-without-branding.md)。若換版改時間軸或bytes，所有受影響CC／M4A／package／交付讀回都要重新綁定；此快照沒有改媒體或核准。

## 英文增量交付（2026-10-26T01:05:03.510145Z快照）

2026-10-26T00:27:20.776Z，英文原生音檢真正105／105、0 flags／unchecked；嚴格當前音訊核驗於00:41完成，80 exact、21 native Jev、4實際第二轉寫exact。cgit是Jev .89採認，不能改稱exact。101個實測視窗皆fit、最大tempo 1.15，沒有skipped或kept take。見[當前EN嚴格proof](localization/en-audio-audit.rich-stage-pass.json)。

英文M4A SHA94d4bfc1721615fe1c1e77cfc369dca17be15e6b569c68e032660db9ad006699，14552825 bytes，AAC 48kHz stereo，560.505秒，−14 LUFS／TP −2.0 dBTP。PCM為26900800 samples／48000＝560.433333秒；AAC尾端0.071667秒另列，不稱影片變長。

00:47:37.352Z，正常4段server assembly驗SHA／大小，再authenticated讀回dub_en與evidence_en_m4a。原files／payload欄位與歷史主片QA保留，新增英文補充下載；standard dubs payload、站主選擇、approval及final pending不改，未送正式語言批次。這不是遠端binary GET或下載後重算雜湊。見[公開白名單摘要](localization/en-delivery-verification.json)與[安全的完整helper交付收據](localization/en-backend-delivery-receipt.json)。

英文經歷初檢6旗、原句retake1剩2旗、retake2剩1旗、一次listener修詞後零旗；原始付費階段／失敗／capture未刪。最初嚴格auditor對stage字串的假設不符合實際rich object，因此第一次REVISE照存；修正的是checker的metadata契約，不是改stage／cache／轉寫迎合checker。見[原REVISE](localization/en-audio-audit.first-pass-revise.json)、[階段快照](localization/en-production-history-snapshot.json)與[八語交付狀態](languages-result.md)。

這次只交英文音訊，不宣稱八語或字幕整包完成。CC仍為narration時間軸草稿，必須按actual dub timings重產／核對；官方品牌片頭尾與整體DOD仍未完成。

## 八語與待辦

en、ja、ko、es、pt、id、vi、th各105句、7章、metadata及縮圖三欄已準備，三輪自審、獨立審稿及原生修正收據見[localization-review.md](localization-review.md)與[收據索引](public-receipt-index.json)。所有歷史review的待修／預算未解原文保留，以後續application說明已採用內容，不把文字審稿當音檢。

- 已通過嚴格音檢並送達後臺的外語為1／8（en）。JA有未驗收M4A候選、初次ASR進行中；其餘六語待完成。產生檔案與完成交付分列，全八語整包ready仍為false。
- 九語CC目前都使用繁中narration時間軸。ES四項、PT兩項、ID兩項，共8個閱讀速度advisories照實保留；完成各語實際配音fit／音檢後，須按各語真實時間軸重產與審查。
- 八張本地化縮圖由root於23:06實際查看contact；各語overlay及數字可讀、無裁切。原創guard內嵌圖仍含「容量8byte／接受」等繁中文字；正常native只翻tag／headline／sub，不能說所有像素內文字均已翻譯。
- 本輪唯讀native lint為0 errors／7 warnings：短冷開、255／256必要重現，加ES／PT／VI／TH手機標題寬度advisories；沒有為消警告改i18n。

待完成正式品牌片頭尾、八語實際合成／fit／音檢／獨審及逐語下載交付，再完成實際dub時間軸CC、metadata／package及正式語言批次。`overall_production_completed=false`，沒有YouTube公開、合併或部署。機器可讀結果見[production-progress.json](production-progress.json)。
