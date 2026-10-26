# 第三片語言交付快照

截至2026-10-26T01:05:03.510145Z。英文已驗音訊與後臺交付1／8；JA初次ASR進行中、尚未通過，其餘六語未完成。CC／metadata／package與正式品牌片頭尾仍未完成，all_eight_ready=false、overall=false。此快照不隨後續JA活動倒改。

| 語言 | 實際音訊狀態 | 後臺交付 | CC／整包 |
|---|---|---|---|
| en | 105／105嚴格核驗，0旗；80 exact／21 Jev／4 second exact | dub_en及evidence_en_m4a已讀回 | narration草稿，待actual dub timing重產 |
| ja | 已有候選，初次ASR進行中；無完成或PASS聲明 | 未交付 | 待完成 |
| ko／es／pt／id／vi／th | 未完成實際音檢 | 未交付 | 待完成 |

## 英文檔案與交付

英文M4A SHA 94d4bfc1721615fe1c1e77cfc369dca17be15e6b569c68e032660db9ad006699，14552825 bytes，AAC 48kHz stereo，560.505秒；PCM560.433333秒與AAC tail0.071667秒分列。−14 LUFS、TP−2.0，101實際windows皆fit、tempo最大1.15，沒有skipped／kept。cgit以native Jev .89通過，不是exact。

00:47:37.352Z正常4段上傳完成server SHA／大小組裝，再authenticated角色metadata讀回。不是遠端binary GET或下載後重算SHA；原主體／原角色與payload欄位、歷史QA11、approval與語言選擇保留，final仍pending。standard dubs payload不改，未送正式language batch。

[當前嚴格proof](localization/en-audio-audit.rich-stage-pass.json)、[公開交付摘要](localization/en-delivery-verification.json)、[安全完整helper收據](localization/en-backend-delivery-receipt.json)。

## 所有重錄與失敗歷史

| 原生階段 | 接受／105 | 旗標 | 實際exit |
|---|---:|---:|---:|
| initial | 99 | 6 | 1 |
| retake1 | 103 | 2 | 1 |
| retake2 | 104 | 1 | 1 |
| reword1 | 105 | 0 | 0 |

初次6旗包含2筆leaked；兩輪原句retake分別只合成6句／2句，一次listener修詞只合成1句（52 billable chars）。每輪capture、原生stage及合成／fit／meter結果照原bytes保存；request數不是唯一HTTP計費次數，不推估新費用、不重設歷史。見[EN階段快照](localization/en-production-history-snapshot.json)。

第一次嚴格auditor已接受105個當前clip，但誤把rich stage物件當字串而REVISE；[原REVISE](localization/en-audio-audit.first-pass-revise.json)不覆寫。修正checker的schema契約後，root實際重跑取得a80eed…763d PASS。沒有改producer event／capture／state／cache或清旗迎合檢查器。

## 仍未完成

主體c8f4仍只是缺正式頻道片頭尾的候選，歷史核心QA11不代表八語或新配音CC／package驗收；敘事9／13、passed=false與原NO／教學取捨保留。八語文字及overlay已準備，內嵌原創圖仍有繁中演示字。既有CC仍是narration草稿，EN／JA後續修詞後也未在本輪重新認定其文字新鮮度；必須依actual dub timings重產核對。全八語與overall DOD不勾。

[製作結果](production-result.md)、[機讀進度](production-progress.json)、[公開收據索引](public-receipt-index.json)。
