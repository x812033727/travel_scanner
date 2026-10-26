# 第三片語言交付快照

截至2026-10-26T02:57:52.837112+00:00。EN音訊、actual-dub字幕、native標題說明與已看縮圖均已交後臺，音訊驗收1／8；JA R1尚有14旗，其餘六語未完成。official bookends已在隔離base取得但未套用本片c8f，final pending，all_eight_ready=false、overall=false，未送正式language batch。

| 語言 | 真實當前音訊 | 後臺交付 | CC／metadata／縮圖 |
|---|---|---|---|
| en | 105／105，0 flags／0 unchecked；80 exact／21 Jev／4 second exact | M4A雙role保留；六個CC／說明／縮圖roles已追加讀回 | actual dub 108 cues／105 IDs，title-description與viewed thumb已交；正式batch未送 |
| ja | 原句R1 exit1；105 checked／91 accepted／14 flags／0 unchecked | 未交付 | native dub-timed CC仍為本地草稿；R2未啟動 |
| ko／es／pt／id／vi／th | 尚未完成實際配音音檢 | 未交付 | 文字／overlay已準備；CC仍草稿 |

## 英文實際檔案與讀回

M4A `94d4bfc1721615fe1c1e77cfc369dca17be15e6b569c68e032660db9ad006699`、14552825 bytes、AAC48kHz stereo560.505秒，−14LUFS／TP−2.0；PCM560.433333秒與AAC tail0.071667秒分列。101實測windows全fit、max1.15、零skipped／kept。cgit實為native Jev .89，非exact。[音訊獨審](localization/en-audio-audit.rich-stage-pass.json)與[00:47音訊交付](localization/en-delivery-verification.json)保留。

02:27:03.829Z，四份資產經正常server組裝SHA／大小驗證，authenticated角色metadata讀回六roles：

| 檔案 | SHA-256 | roles |
|---|---|---|
| SRT，10224 bytes | c9511097d17f1600ef8ab366cf084ad4316080271b958de349f1e0bb3288f688 | captions_en、evidence_en_cc_srt |
| VTT，9908 bytes | 60d2960b3072d0e8db60b096c99fa5aea50114ae39703081e34773050e5693ec | evidence_en_cc_vtt |
| title＋native說明，2921 bytes | bb976ea9cb3e968da45ed74f5dd402ea7fb6b1b1a584608b5505652ed40e87ef | description_en、evidence_en_metadata_txt |
| 已實際觀看縮圖，94361 bytes | 23ceca2fe0562b0ae9422cb583608ceea15d99c460f748ac584d1955540dad12 | thumbnail_en |

原M4A／main角色、payload欄位、歷史QA11與choices完整保留，final仍pending、approval未變。這是上傳server hash validation＋authenticated metadata readback，沒有remote binary GET，也不是語言批次或伺服器核准。見[安全摘要](localization/en-caption-assets-delivery-verification.json)、[完整helper收據](localization/en-caption-assets-backend-receipt.json)、[native資產新鮮度proof](localization/en-cc-assets-current-proof.json)、[root圖像觀看](localization/en-thumbnail-root-view.json)。

## 所有重錄與失敗歷史

| 原生階段 | 接受／105 | 旗標 | 實際exit |
|---|---:|---:|---:|
| initial | 99 | 6 | 1 |
| retake1 | 103 | 2 | 1 |
| retake2 | 104 | 1 | 1 |
| reword1 | 105 | 0 | 0 |

初次6旗包含2筆leaked；兩輪原句retake分別只合成6句／2句，一次listener修詞只合成1句（52 billable chars）。每輪capture、原生stage及合成／fit／meter結果照原bytes保存；request數不是唯一HTTP計費次數，不推估新費用、不重設歷史。見[EN階段快照](localization/en-production-history-snapshot.json)。

第一次嚴格auditor已接受105個當前clip，但誤把rich stage物件當字串而REVISE；[原REVISE](localization/en-audio-audit.first-pass-revise.json)不覆寫。修正checker的schema契約後，root實際重跑取得a80eed…763d PASS。沒有改producer event／capture／state／cache或清旗迎合檢查器。

## 日文R1真實結果與hold

初檢exit4：104checked／83accepted／21flags／1unchecked；u2xw是明確OTHER、無轉寫，不是unknown POST。原句R1只21新WAV、84原檔不變（含u2xw），589 billable chars，101fit0over、max1.15、freshmeter−14／TP−2.9。一次授權check含u2xw未改WAV的ASR重試後，於01:56:54.695Z真exit1：105checked／91accepted／14flags／0unchecked。u2xw現在有雙轉寫但仍真旗，沒有手動採認。

當前JA M4A `eee485c9c022e43d3c32d293b1cbea498ffd56b56301145370367ea6fb7c2c69`、15549897 bytes；尚未通過或交付。見[初檢capture](localization/ja-initial-check.capture.json)、[R1合成／fit／meter](localization/ja-retake1-synth-fit-meter.result.json)、[R1真exit capture](localization/ja-retake1-check.capture.json)。目前全域新TTS及ASR hold，R2未開始；不重設原句重錄次數。

## 未完成範圍

官方素材已取得不代表本片已採用；目前c8f依然BODY CANDIDATE。七個外語仍待真音檢及交付；JA與其他本地CC不冒稱已檢，ES／PT／ID共8速度advisories保留。EN本次字幕資產交付不改歷史主體QA11適用範圍，也不使全八語／正式batch／overall DOD成立。敘事9／13、false及原NO／教學取捨不變。

[製作結果](production-result.md)、[機讀進度](production-progress.json)、[公開收據索引](public-receipt-index.json)。
