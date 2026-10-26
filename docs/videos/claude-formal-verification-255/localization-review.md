# 第三片當前本地化驗收範圍

截至本輪新版實交：EN1/8的M4A、actual-dub108cue／105ID CC及標題說明已在官方片頭尾版b635後台完成；繁中106cue／105ID CC及說明也完成。23roles的[當前證據](branding-v4/delivery-summary.json)與[QAfalse10](branding-v4/native-current-QA-false10.json)須共同閱讀，不能沿用舊BODY QA11作新版全片通過。

JA仍原句R1的91accepted／14flags，新manifest因branding不符跟narration並保留harderror；其餘六語音訊未完成。8CPS保留，沒有skip／keep-fitted、調門檻、手清旗或假server approval。來源e6e／speech8028、原MASTER19ae、EN完整accepted targets／raw／cache／ASR沒有為本次包裝而改寫。只重用當前已驗的EN，不把未驗JA fitted dub自動附帶送出。

以下舊文字／BODY／縮圖與失敗歷史完整保留；當前新片型交付只以上述23roles、current hash與[production-progress](production-progress.json)的明示scope為準。

## 原文保留：02:57以前本地化快照

# 第三片八語文字與媒體快照

截至2026-10-26T02:57:52.837112+00:00，EN105／105音訊已驗收交付，actual-dub108cue／105ID字幕、native標題說明與實際觀看縮圖亦真送後臺並讀回六角色。JA原句R1已105 checked／91 accepted／14 flags／0 unchecked，未ready；其餘六語未完成，all_eight_ready與overall仍false，正式language batch未提交。見[languages-result.md](languages-result.md)。

[EN音訊proof](localization/en-audio-audit.rich-stage-pass.json)、[當前CC／metadata／八圖native proof](localization/en-cc-assets-current-proof.json)、[root實際視覺收據](localization/en-thumbnail-root-view.json)及[六角色交付摘要](localization/en-caption-assets-delivery-verification.json)範圍分列。原M4A雙role不變；server SHA組裝及authenticated metadata讀回不等於遠端binary下載或核准。字幕六角色附件是新增實際交付，不把早期native final或本地CC倒稱已送。

[早先漏判縮圖的原記錄](localization/en-cc-assets-earlier-missing-thumbnail-note.json)與[helper早期REVISE](localization/en-caption-assets-helper-earlier-revise.json)照存；後續superseding proof及[137項peer guard驗證](localization/en-caption-assets-helper-peer-review.json)分別修正證據，未改舊收據、當前字幕／縮圖或媒體。

只有EN CC已對真配音核驗並交付；JA雖原生使用dub timing仍是未驗收草稿，其餘CC草稿及ES／PT／ID共8速度advisories保留。八張overlay可讀，原創圖內繁中「容量8byte／接受」未全像素翻譯。官方5/21 v4_416c素材已在隔離base正常取得，但第三c8f未套用，不能宣稱正式品牌成片完成。

以下23:07文字準備、靜態39項預算超額、narration-timed草稿及當時0／8是原歷史快照；不倒改為現時成功。當前JA證據另見[R1 capture](localization/ja-retake1-check.capture.json)，TTS／ASR hold、不啟動R2。

## 2026-10-25T23:07:06Z 文字準備歷史快照

截至2026-10-25T23:07:06Z，八語文字、7章、title／description／tags／縮圖三欄已原生merge，翻譯自審與獨立審稿收據已封存；外語完整M4A、音檢與後臺交付均為0／8。這份記錄不宣稱配音fit或八語整包完成。

| 語言 | 當前句數／章 | 自審／獨審與必要文字修正 | 當前暫定字數超額 | 當前CC | 實際M4A／音檢／交付 |
|---|---|---|---:|---|---|
| en | 105／7 | 完成；fzz5改為8bytes內預留1byte | 0 | narration timing，108 cues | 0／未完成 |
| ja | 105／7 | 完成；AI寫證明、+1步驟及formal術語已修 | 1 | narration timing，122 cues | 0／未完成 |
| ko | 105／7 | 完成；AI作者、寬型別、+1及條件範圍已修 | 4 | narration timing，119 cues | 0／未完成 |
| es | 105／7 | 完成；輸入／建置／容量及release範圍已修 | 12 | narration timing，110 cues，4 speed advisories | 0／未完成 |
| pt | 105／7 | 完成；必要語義與容量／release範圍已修 | 16 | narration timing，109 cues，2 speed advisories | 0／未完成 |
| id | 105／7 | 完成；必要語義與容量／release範圍已修 | 3 | narration timing，109 cues，2 speed advisories | 0／未完成 |
| vi | 105／7 | 完成；必要語義修正已採用 | 0 | narration timing，112 cues | 0／未完成 |
| th | 105／7 | 完成；4nfp公開版／研究整體否定範圍已修 | 3 | narration timing，105 cues | 0／未完成 |

字數是以目前repo譯文對當前worksheet的原max_chars計數，超額合計39句；不是音訊量測，未改預算或為硬塞刪前提。JA／KO原獨審的未解及其他語原review均保持歷史判定，後續application另記已採用改法。沒有把全句保義等同單句靜態fit，也沒有以靜態fit等同實際音檢。

## 可追溯的審稿與套用

[localization/](localization/)封存16份原始bytes一致的資料，完整SHA／來源在[public-receipt-index.json](public-receipt-index.json)：

- 三組翻譯者三輪自審：EN／JA／KO、ES／PT／ID、VI／TH，各Markdown及JSON。
- 三組由非該語翻譯者執行的獨審，各Markdown及JSON；EN另有root獨審。
- JA／KO與其餘五語的原生application紀錄，以及TH 4nfp後續範圍修法。

這些檔案照原bytes複製，未把原來的「獨審待做」「未merge」「預算未解」倒改成成功。當前merged譯文105句／7章的SHA、字幕／縮圖SHA及未解字數列表另見[localization-preparation-snapshot.json](localization-preparation-snapshot.json)。沒有改video、claims、i18n、聲音或原始收據。

保留的關鍵範圍包括官方239入口／123庫、公開版60／25及兩個本地各256輸入的分列；no halts proof只限定該公開release；guard不寫buffer，loop是獨立程式；完整加寬RHS與存放轉型、兩項SAT查詢只屬加寬guard；0.25秒等待觀察不等於有限圖的循環推理。文字審稿不能證明外語已正確唸出這些條件。

## 圖與字幕已準備的真正範圍

當前核心QA11／11檢查了八語title／description上限、7章、九語字幕及八張本地化縮圖。root於23:06實際打開contact，確認各語overlay／數字可讀且無裁切；內嵌原創guard仍是同一張繁中演示圖，包含「容量8byte／接受」。native可本地化tag／headline／sub，未翻譯全部內嵌像素。白名單摘要見[localized-thumbnail-review.json](localized-thumbnail-review.json)。

九語字幕manifest的timing均為narration，並非各語配音。ES／PT／ID的8項速度advisories保留；八語實際合成、fit與音檢完成後，每語都要以其實際dub時間軸重產／核對CC，保留仍存在的速度警告。核心QA不能當成後續外語音訊、字幕及package ready證據。

本輪native lint的ES／PT／VI／TH手機標題寬度advisories保留；YouTube硬上限仍通過。全八語audio／package DOD未勾，all_eight_ready=false。官方品牌片頭尾亦未完成，整體交付false。
