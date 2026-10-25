# ForTy 製作結果快照

截至 2026-10-25T21:02:27Z，繁中主片及VI、EN已直接送達[後臺影片頁](https://mokaair.com/zh-TW/admin/videos?video=forty-forest-map)。主片交付DOD完成；外語已驗音訊為2／8，VI、EN各92／92句通過並附下載角色。JA正在重錄／音檢流程，其餘五語待製作；八語CC／package及整體交付仍未完成。

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

## 已交付的範圍

正常final review POST已完成；主片經10部分上傳、server assembly驗SHA／大小，並以已驗證身分讀回 `evidence_zh_tw_1080p_mp4` 的SHA／大小。已通過音檢的VI同時保留原角色，另有 `evidence_vi_m4a` 下載別名。主片及VI的角色metadata與本機雜湊一致，詳見 [main-delivery-verification.json](main-delivery-verification.json)。EN於20:52:20以正常單語增量流程追加同blob的 `dub_en`、`evidence_en_m4a`；四部分上傳完成server SHA／大小驗證，authenticated GET讀回兩角色的SHA／大小。原1080p、VI及全部舊files／payload／QA保留，沒有native final重推或夾帶JA。

這次驗證是server上傳組裝及authenticated role metadata讀回；未進行遠端二進位串流下載或重新計算遠端下載bytes的SHA。遠端final仍為 `pending`；19:26:40.105Z的final採用是持續委派下的本機正常決策，未改寫遠端核准狀態。未提交八語language batch，未上傳或發布YouTube。

## 外語進度與待項

- VI經兩輪原文重錄及一輪四句等義改詞，最後4句新合成／88句重用，當前take原生音檢92／92、0 flags、0 unchecked。M4A SHA-256 `1f50cdfe5b5e6ff31ea562286d77ffd9c2df7dc00f75fea6e3f2b2036ce782f8`，512.805秒、12076524 bytes、AAC 48kHz stereo、−14 LUFS／TP −2.9 dBTP；89窗全fit、tempo最高1.10。其CC已按目前dub時間軸重產，速度advisory保留。
- EN於20:30:29真實原生音檢exit0、92／92通過；獨立current WAV／完整intended／spoken form／原生裁決核對後，20:52:20已直接送後臺。M4A SHA-256 `6ca5213241ac1f107141ebd4d2e410d4f6474efe39bb1374f2fd35abc0192c63`，512.805秒、13547232 bytes、AAC 48kHz stereo、−14 LUFS／TP −2.8 dBTP；89窗全fit、tempo最高1.21，0 skipped／kept。這只證明已驗音軌與下載，未宣稱完整英語CC／metadata／配音整包ready。
- JA初次音檢已真實完成92 checked／9 flags（21:00:08、exit1），正進行bounded retake1流程，尚未ready；producer `ja_dub_running`（狀態 `2026-10-25T21:02:20.158Z`）。 KO／ES／PT／ID／TH待製作。已驗音訊為VI、EN共2／8，`all_eight_ready=false`，八語DOD未勾。
- 每語音檢真PASS並獨立核對後可增量交付M4A；八語音軌完成後須依實際時間軸重產／整批核對CC，保留閱讀速度advisory，再完成metadata／package與正式語言批次。

逐語結果見 [localization-review.md](localization-review.md)，機器可讀快照見 [production-progress.json](production-progress.json)。八語預設與推薦決策已有持續授權。

## 收據

- [主片交付與驗證範圍](main-delivery-verification.json)、[VI目前音檢與媒體驗證](vi-audio-verification.json)、[最新核心QA](qa-after-verified-vi.json)。
- [敘事審查](narrative-review.md)及[七句改詞後原生結果](narrative-after-audio-reword1-result.json)；舊raw／native收據保留。
- 原始交付收據：`/workspace/work/ai-tech-next/attach-forty-main-download.result.json`、`forty-main-and-vi-downloads.json`；製作狀態：`/workspace/work/ai-tech-next/forty-language-production.json`（本快照讀到 `2026-10-25T21:02:20.158Z`、`ja_dub_running`）。
- [EN獨立稽核](en-audio-verification.json)（SHA `c02f9097a75b672f6965fd94a046fa649cfb523b85e81bef83cbeb0ff0552e10`）；[實際20:52交付收據](en-backend-delivery.json)（SHA `3211bb800cb6f2d7eddc434d938c23f4c1ead55c2fd209f1e98723d1fa2127cc`）。
