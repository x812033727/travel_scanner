# 製作採用

2026-10-25。站主持續委派「預設八語都要做」「如果要決定事情用你推薦的就好 不用問我」，並要求完成後繼續下一支。協調者採用與Jev一致的A：先讓255暴露邊界，再把契約修完整。

- 正式企劃SHA-256：dc3577cf783cba29c09cd77bf990a30e3988afb62555e12b5e32d4b48f85f4c3。
- 原生Jev真實結果：A 0.99、立場0.89、示範0.96、建議0.01，通過；2026-10-25T18:59:13.326Z。其餘B/C原始評分保留於outline-judgment.json。
- 正常後臺登記及outline提交已完成；提交後實際審核狀態pending，Jev回覆的『依設定自動核准』文字不能當伺服器已核准證據。
- 18:59:41.621Z依站主委派，用原生approve記錄本機採用當前brief雜湊；不是冒稱站主在介面點選，不造auto.json、不改站主開關或伺服器審核狀態。

本片主題：Claude形式驗證研究，用兩個本片自寫的C程式與255邊界，完成接受／拒絕／返回條件的可重跑紀錄。官方239/123、public release60/25與本地各256輸入分列；不聲稱重現Rocq或vendor checker。

正式交付為繁中主片加en、ja、ko、es、pt、id、vi、th各自標題說明、CC和真正檢查完成的可下載M4A，直接送本片後臺後讀回伺服器驗SHA的角色／大小。以下時間段保存各階段原實況；最新快照為繁中主體候選及EN音訊／actual-dub字幕／native標題說明／已看縮圖已交，音訊驗收1／8；JA R1真105／91／14／0，仍未通過。主體歷史QA11／11不改；官方素材已在隔離base取得，但第三尚未套用，七語仍未完成，詳[production-result.md](production-result.md)與[languages-result.md](languages-result.md)。沒有執行YouTube上傳／公開、合併或部署。

後臺：https://mokaair.com/zh-TW/admin/videos?video=claude-formal-verification-255


## 正式稿前的事實釐清（2026-10-25 19:09 UTC）

依新查到的官方checking.md，Rocq核心是在編譯proof term時檢查；wrapper再核固定型別並列假設，最後稽核允許清單。兩份本地修法也明示同時移除運算式中的舊uint8_t窄化，不能只改宣告。企劃更新SHA為f67e8bb712a105ba63ea30a141ed58b667e3634bd1756e56b7c2f770329807d7，A故事線與成果不變。

初次Jev的A0.99／示範0.96只適用舊dc3577雜湊，原始收據完整保留；本次不重標分數，以協調者依站主持續委派推薦A，再用原生approve綁新版brief於19:09:25.373Z。後臺另送實際新版企劃，仍不冒稱伺服器已核准。


## 繁中製作採用（R1，2026-10-25）

正式video SHA a77c48e48131a2a17196cbddf2bf192f33c02c9d5defc3953a543155e441514d；claims SHA134e8e888f6aba07ed4da185b8d97f26e0ef65877c542684fe0433ed08e1b1d8。93場景／105句／101狀態／7章，原生lint零錯誤、三警告（短冷開及必要運算數字重現）照實保留。正文估565.7秒、全片估602.4秒，尚不是實際音長。

verify-2實際PASS，0待修、0未找到；逐句對齊、完整C與SAT查詢歸屬、官方固定命題／模型／kernel及允許假設稽核、數量層級皆已核對。初版verify-1的REVISE完整保留。說明組合實得2552 bytes、10 credits，符合上限。

兩個新盲讀各9/13，passed=false與三個必要NO及一項advisory不改寫；採用同一份驗收紀錄、完整運算及短片尾的教學取捨，詳narrative-review.md。14張原生樣卡已實際檢視，零layout／glyph問題；專用縮圖已實際看過，替換初版裁切不佳的圖，未變更任何資料值或旁白聲音。

協調者依站主持續委派採用此R1進行正常繁中TTS。聲音與風格和ForTy相同；四個原文術語的實際發音仍以最新WAV音檢驗證，不因字典null預先稱已聽過。正文及成片都需實測至少八分鐘，不靠片頭片尾、靜音、慢播補時。音檢有旗只重錄／保義改寫被標take，留存所有原始收據，不能清旗或改轉寫偽造通過。

繁中完成後預設八外語逐語完成CC、metadata與實際音檢M4A，再直接交後臺與讀回驗證；尚未完成的媒體不因這項採用而稱完成，不執行YouTube公開、合併或部署。


## 八句音檢修詞後的實測進度

目前source232b4495b433041007c039630ec517b7e0b4948c3cd7a5a47da6ecd88cae8a15、claims527048b6061d21f70e00475cc4790a46b0de6e536a37e8966402194a043fa9c6、speech8028c7320d9cab29。僅八句保義改詞，其他97句及所有畫面資料不變；verify-3真正PASS、原有敘事NO保留。只合成八個新WAV、92個request重用，逐WAV對帳確認只有八句SHA變動，97句原檔不變。

目前實際105／105句音檢通過：64 exact、19同音／語助、13 Jev、9實際第二轉寫，0 flags、0 unchecked。獨立唯讀[旁白核驗](narration-reword1-verification.json)以完整原文、spoken form、原生key／裁決及最新WAV的完整SHA綁定105句，沒有清旗或覆寫ASR。全旁白560.4333秒、outro前548.1333秒、扣冷開與outro的正文523.7333秒，均為實測；音檢通過不是成片或八語完成聲明。

正常audio review提交後伺服器仍pending；21:01:22.994Z原生approve依既有委派記錄本機timeline採用，不冒稱遠端核准。正式render首次因未設定既有Playwright路徑在啟動瀏覽器前exit5，指定既有/workspace/work/playwright後重跑，不重合成旁白、不安裝或更換素材。成片與QA尚在製作，八語譯稿同步進行、未交付外語媒體。


## 主體候選成片與正式動畫待補

目前版面修正後source e6e87e77f069a574d6e1d7f47bf2e5be031eb8566bb2edb71defa24ae4c2b99f。five-small-examples僅把0、1、2、3、4五個相同結果整併成顯式單列表格，沒有減少輸入／輸出，所有105句與聲音／metadata不變。原生render 1個狀態重畫、100重用、零layout問題，修後表格與完整聯絡表已實際檢視；[獨立資料差異與最新旁白核驗](table-layout-independent-review.json)通過。

正式片頭片尾套用在編碼前因本producer沒有已安裝素材而拒絕，沒有因此重合成旁白。後續正常assemble取得的是主體候選，並非完整正式定版：[實際候選驗證](main-body-candidate-verification.json)，SHA c8f4bf86b1bfcc66aa8dccfdf2c047469da56bad2461a0ef130e72988dd63ed5，48226281 bytes，16813 frames，容器560.505秒；H264 1920×1080／30fps、AAC 48kHz stereo，−14 LUFS／TP −2.9，93片段及101狀態的原生機械檢查通過。實際編碼5秒、220秒、555秒樣格已打開核對，並未宣稱逐秒播放。

正式頻道片頭片尾素材與綁定尚待補，不能把本片的靜態outro卡或QA對null branding的容許當作已完成動畫。新任務2026-10-25-local-first-build-without-branding保留重現及三支片需核對項；已詢問一次既有素材路徑／下載連結，其他製作照常進行。此段21:37記錄的「尚待文字／CC／縮圖／核心QA」已由下列新收據接續，原候選驗證檔的寫入時狀態不覆寫。

## 主體候選已交與八語文字準備（23:07快照）

22:38原生核心QA完成11／11，stance .84、demo .92、advice .01、sponsor .04；八語各105句／7章、metadata、獨立文字審查及本地化overlay／CC已準備。字幕目前都依繁中narration時間軸，ES／PT／ID共8項速度advisories保留；實際外語M4A、音檢及交付0／8，各語音軌完成後仍須以actual dub timings重產CC。四個手機標題寬度advisories保留，最新native lint為0 errors／7 warnings；沒有為消警告修改i18n。

22:48:50.599Z，正常12段完整1080p上傳完成server assembly SHA／大小驗證，authenticated role metadata讀回`evidence_zh_tw_1080p_mp4`，SHA仍c8f4bf86b1bfcc66aa8dccfdf2c047469da56bad2461a0ef130e72988dd63ed5、48226281 bytes。final仍pending，原files／payload／QA及語言選擇完整保留；沒有遠端二進位下載、approval改動或正式language batch。詳[公開交付摘要](main-delivery-verification.json)。

本體已交不等於正式品牌定版或八語完成。官方片頭尾仍missing，靜態outro不替代動畫；敘事9／13、passed=false及教學採用理由保持原記錄，不改NO或捏造新盲讀。root23:06實際看過八語縮圖overlay可讀／無裁切，內嵌guard演示圖仍含繁中文字，不聲稱所有像素均翻譯。最新可機讀狀態見[production-progress.json](production-progress.json)，歷史自審／獨審與原生套用檔已在[收據索引](public-receipt-index.json)保留完整SHA。


## 英文已驗音訊增量交付（2026-10-26T01:05:03.510145Z）

站主既有八語授權下，EN正常合成／fit／量測、原生音檢及嚴格當前WAV核驗均完成。初次音檢6旗，兩輪原句retake後為2／1旗，僅剩cgit進入一次保義listener修詞；最後105／105、80 exact／21 Jev／4 second exact，cgit為Jev .89而非exact。原付費歷史、轉寫、兩輪重錄與第一次rich-stage錯誤REVISE均完整保留，不清旗或改舊收據。

00:47:37正常4段上傳英文M4A完成server SHA／大小組裝驗證與authenticated角色metadata讀回，dub_en／evidence_en_m4a均94d4bfc1721615fe1c1e77cfc369dca17be15e6b569c68e032660db9ad006699／14552825 bytes。final仍pending，原主體QA／payload欄位、approval／語言選擇保留；無remote binary GET、無language batch。這是1／8音訊交付，不是八語metadata／CC／package或官方片頭尾完成。JA在本快照仍為initial ASR進行中，不預寫PASS。見[languages-result](languages-result.md)。


## EN字幕資產實際交付與JA R1（2026-10-26T02:57:52.837112+00:00）

Root既有委派下，依當前105句EN音訊獨審、native actual-dub108cue／105ID字幕、完整metadata重建及真root圖像觀看pin，正常checked-assets工具於02:27:03.829Z真完成四檔／六roles附件；同pending final的所有舊files／payload／QA／choices保留。原M4A雙role仍94d4、sourcee6／speech8028／mainc8f固定。見[交付摘要](localization/en-caption-assets-delivery-verification.json)與[安全完整收據](localization/en-caption-assets-backend-receipt.json)。不nativefinal重送、不送正式languagebatch、不變serverapproval，沒有遠端binary下載核驗。

原missing-thumbnail誤判及guard peer REVISE不覆寫；superseding825820 proof實核八個native圖，root實際view收據b9380c綁EN23ce與contact5a051。ENoverlay可讀／無裁切，內嵌原創圖繁中文字照實保留。JA原句R1真exit1、105checked／91accepted／14flags／0unchecked；R2及所有新TTS／ASR均hold，沒有為音檢改frozen繁中或清旗。

官方5/21 v4_416c素材已正常取得於隔離base，這是新進度，不能再說全局無bytes；但第三c8f仍未套用正式頻道片頭尾，早期missing-package失敗仍是當時真實歷史。品牌換版須獨立採用與重新綁定，八語／wholepackage／overall仍false。
