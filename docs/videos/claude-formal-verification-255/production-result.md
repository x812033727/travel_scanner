# 第三片製作與交付快照

截至2026-10-25T23:07:06Z，繁中主體候選的完整1080p已送達[後臺影片頁](https://mokaair.com/zh-TW/admin/videos?video=claude-formal-verification-255)，核心QA真實11／11，遠端final仍pending。正式頻道片頭尾尚缺，已完成外語音訊為0／8，整體製作未完成。

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

## 八語與待辦

en、ja、ko、es、pt、id、vi、th各105句、7章、metadata及縮圖三欄已準備，三輪自審、獨立審稿及原生修正收據見[localization-review.md](localization-review.md)與[收據索引](public-receipt-index.json)。所有歷史review的待修／預算未解原文保留，以後續application說明已採用內容，不把文字審稿當音檢。

- 實際外語M4A、音檢PASS與交付均0／8；全八語整包ready為false。
- 九語CC目前都使用繁中narration時間軸。ES四項、PT兩項、ID兩項，共8個閱讀速度advisories照實保留；完成各語實際配音fit／音檢後，須按各語真實時間軸重產與審查。
- 八張本地化縮圖由root於23:06實際查看contact；各語overlay及數字可讀、無裁切。原創guard內嵌圖仍含「容量8byte／接受」等繁中文字；正常native只翻tag／headline／sub，不能說所有像素內文字均已翻譯。
- 本輪唯讀native lint為0 errors／7 warnings：短冷開、255／256必要重現，加ES／PT／VI／TH手機標題寬度advisories；沒有為消警告改i18n。

待完成正式品牌片頭尾、八語實際合成／fit／音檢／獨審及逐語下載交付，再完成實際dub時間軸CC、metadata／package及正式語言批次。`overall_production_completed=false`，沒有YouTube公開、合併或部署。機器可讀結果見[production-progress.json](production-progress.json)。
