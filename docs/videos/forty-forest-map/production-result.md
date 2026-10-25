# ForTy 製作結果快照

截至 2026-10-25T22:35:44Z，繁中主體版及VI、EN、JA已直接送達[後臺影片頁](https://mokaair.com/zh-TW/admin/videos?video=forty-forest-map)。外語已驗並交付音訊為3／8，三語各92／92句通過；KO第二輪重錄及fit／量測完成，等待共享ASR槽重檢，ES／PT／ID／TH待製作。正式品牌bookend、八語CC／package及整體交付仍未完成，overall及all_eight_ready均為false。

## 凍結主片與歷史核心QA

| 項目 | 實際結果 |
| --- | --- |
| 凍結主片 | source `450bd6ad82146cfa1110abfe133cf9124980095a22402e72bfe0c693a743394a`；speech `c6d70ecaef91a15d`；final SHA-256 `b293282ddfefdf7fb6d20e88bfef46b281c1ecac31807ac0ecc13ee4eb193d18`。 |
| 中文旁白 | 目前92／92句PASS、0 flags；初始15→8→7後採7句等義改詞，數字、聲音及style未變。 |
| 長度／檔案 | 512.7667秒，outro前正文501.0333秒；1920×1080、41255462 bytes。 |
| 原生合成 | 15383 frames，−14 LUFS、TP −2.8 dBTP；264抽樣畫格匹配slide；89 states，最長11.7秒。 |
| 歷史主片核心QA | 真實11／11；stance 0.81、demo 0.94、advice 0.01、sponsor 0.04。包含八語縮圖檢查，字幕速度advisory保留。 |
| 敘事 | 真實9／13、`passed:false`；no_toc、chapters_link、no_recap、no_detour四NO及採納教學取捨保留，沒有宣稱全過或重新盲讀。 |
| 外語文字 | 八語各92句、metadata、獨立翻譯／縮圖審稿及預算提案完成，必要修正已正常native merge。 |

最初QA唯一失敗為doi.org的403。六筆資產改用官方固定v1 API GET200，保留plain DOI及六筆CC BY 4.0署名；92句、voice、資產bytes及成片bytes未變。[source-link-fix.json](source-link-fix.json)的pending欄是歷史狀態，以[主片11／11 QA收據](qa-after-verified-vi.json)為準；它是當時主片與字幕版本的歷史紀錄，不等於新增EN或其餘音軌的CC／package已核對完成。

## 品牌bookend未完成

本producer沒有正式品牌bookend package／default，ForTy在repo及media workdir都沒有branding.json。已交付的b293…d18是主體版；歷史QA11／11及靜態outro不能當作正式品牌bookend或全部新規則已完成。待合法官方素材齊備後依guard另處理，不改既有source／media／approval。追蹤ID為`2026-10-25-local-first-build-without-branding`，記在第三片分支；此分支不建立不存在的相對連結。

## 已交付的範圍

正常final review POST已完成；主片經10部分上傳、server assembly驗SHA／大小，並以已驗證身分讀回 `evidence_zh_tw_1080p_mp4` 的SHA／大小。已通過音檢的VI同時保留原角色，另有 `evidence_vi_m4a` 下載別名。主片及VI的角色metadata與本機雜湊一致，詳見 [main-delivery-verification.json](main-delivery-verification.json)。EN於20:52:20以正常單語增量流程追加同blob的 `dub_en`、`evidence_en_m4a`；四部分上傳完成server SHA／大小驗證，authenticated GET讀回兩角色的SHA／大小。原1080p、VI及全部舊files／payload／QA保留，該次EN交付未夾帶當時尚未檢完的JA。JA其後於21:54:49正常增量交付：四部分上傳經server組裝SHA／大小驗證，只追加同blob的 `dub_ja`、`evidence_ja_m4a`，authenticated role metadata讀回兩角色的SHA／大小。原1080p、EN、VI、舊files／payload／歷史QA、遠端pending及語言選擇均保留，未重推native final或提交正式language batch。

這次驗證是server上傳組裝及authenticated role metadata讀回；未進行遠端二進位串流下載或重新計算遠端下載bytes的SHA。遠端final仍為 `pending`；19:26:40.105Z的final採用是持續委派下的本機正常決策，未改寫遠端核准狀態。未提交八語language batch，未上傳或發布YouTube。

## 外語進度與待項

- VI經兩輪原文重錄及一輪四句等義改詞，最後4句新合成／88句重用，當前take原生音檢92／92、0 flags、0 unchecked。M4A SHA-256 `1f50cdfe5b5e6ff31ea562286d77ffd9c2df7dc00f75fea6e3f2b2036ce782f8`，512.805秒、12076524 bytes、AAC 48kHz stereo、−14 LUFS／TP −2.9 dBTP；89窗全fit、tempo最高1.10。其CC已按目前dub時間軸重產，速度advisory保留。
- EN於20:30:29真實原生音檢exit0、92／92通過；獨立current WAV／完整intended／spoken form／原生裁決核對後，20:52:20已直接送後臺。M4A SHA-256 `6ca5213241ac1f107141ebd4d2e410d4f6474efe39bb1374f2fd35abc0192c63`，512.805秒、13547232 bytes、AAC 48kHz stereo、−14 LUFS／TP −2.8 dBTP；89窗全fit、tempo最高1.21，0 skipped／kept。這只證明已驗音軌與下載，未宣稱完整英語CC／metadata／配音整包ready。
- JA經兩輪原文retake、兩輪保義縮句及兩輪等義改詞後，21:50:50原生音檢exit0，92／92 PASS、0 flags／unchecked；獨立核對62 exact、20 Jev、7 second exact、3 second Jev，0 skipped／kept。M4A SHA-256 `a4af09e0a4e5be06f1469c66caa43fb7b7380296103d7159e0b73acb2a53972e`，14775477 bytes、512.805秒、AAC 48kHz stereo、−14 LUFS／TP −2.9 dBTP；89窗全fit、tempo最高1.19。21:54:49已交付兩個JA下載角色，只證明已驗音軌，未宣稱JA CC／metadata／完整package ready。
- KO上一輪原生check於22:29:17完成，exit1、92 checked／82 accepted／10 flags／0 unchecked。第二輪原文重錄及fit／量測已完成，但新take尚未音檢；producer於22:34:59為 `ko_waiting_shared_asr_slot_after_retake2`，等待root釋放共享Whisper槽。ES／PT／ID／TH仍pending。已驗並交付為VI、EN、JA共3／8，`all_eight_ready=false`，八語DOD未勾。
- 每語音檢真PASS並獨立核對後可增量交付M4A；八語音軌完成後須依實際時間軸重產／整批核對CC，保留閱讀速度advisory，再完成metadata／package與正式語言批次。

逐語結果見 [localization-review.md](localization-review.md)，機器可讀快照見 [production-progress.json](production-progress.json)。八語預設與推薦決策已有持續授權。

## 收據

- [主片交付與驗證範圍](main-delivery-verification.json)、[VI目前音檢與媒體驗證](vi-audio-verification.json)、[最新核心QA](qa-after-verified-vi.json)。
- [敘事審查](narrative-review.md)及[七句改詞後原生結果](narrative-after-audio-reword1-result.json)；舊raw／native收據保留。
- 原始交付收據：`/workspace/work/ai-tech-next/attach-forty-main-download.result.json`、`forty-main-and-vi-downloads.json`；producer快照 `2026-10-25T22:34:59.053831Z`，SHA `9912fcd3030f4453c8e3c4b9f2683ae961014af44714f5795358396d927b3819`。
- [EN獨立稽核](en-audio-verification.json)（SHA `c02f9097a75b672f6965fd94a046fa649cfb523b85e81bef83cbeb0ff0552e10`）；[實際20:52交付收據](en-backend-delivery.json)（SHA `3211bb800cb6f2d7eddc434d938c23f4c1ead55c2fd209f1e98723d1fa2127cc`）。
- JA獨立稽核 [JA獨立核驗](ja-audio-verification.json)（SHA `1de81cac0e64939a322b0963a9a651093d8c5c88eb29dbe3fbaf5794576fd8e8`）；實際增量交付 [JA後臺交付收據](ja-backend-delivery.json)（SHA `ba21ef011b4dab323777485bb85d265e31ca96a1129e62e80f7cd1e78d70ff04`）。驗證不包含遠端二進位下載。
