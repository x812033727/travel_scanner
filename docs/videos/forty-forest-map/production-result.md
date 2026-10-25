# ForTy 製作結果快照

截至 2026-10-25T18:42:32Z，中文主片已在本機完成並通過核心QA；八語音軌及後臺交付仍在進行，交付DOD尚未完成。

## 已完成

| 項目 | 實際結果 |
| --- | --- |
| 中文旁白 | 目前92／92句音檢PASS、0 flags；初始15→8→7後採7句等義改詞，沒有改數字、聲音或style。speech `c6d70ecaef91a15d`。 |
| 長度 | 實測512.7667秒，outro前正文501.0333秒。 |
| 原生合成 | 15383 frames，−14 LUFS、TP −2.8 dBTP；264個抽樣畫格與slide匹配；89 states，最長11.7秒，checks全部通過。 |
| 核心QA | 修來源URL後真實11／11；demo 0.94、stance 0.79、advice 0.01、sponsor 0.04。 |
| 敘事 | 真實9／13、`passed:false`；no_toc、chapters_link、no_recap、no_detour四NO及採納教學取捨保留，沒有改成全過或新盲讀。 |
| 外語文字 | en／ja／ko／es／pt／id／vi／th各92句與metadata、獨立審稿及預算提案已完成，必要修正已正常native merge。 |

目前 `video.json` SHA-256：`450bd6ad82146cfa1110abfe133cf9124980095a22402e72bfe0c693a743394a`。本機 `final.mp4` SHA-256：`b293282ddfefdf7fb6d20e88bfef46b281c1ecac31807ac0ecc13ee4eb193d18`。

最初10／11 QA僅因doi.org回403。六筆資產來源改用固定官方v1 API的GET200，保留plain DOI及六筆CC BY 4.0署名；92句、voice、資產bytes與成片bytes不變。沒有宣稱DOI／HTML頁現在可開。[source-link-fix.json](source-link-fix.json)的pending欄是修URL當時快照，後續原生QA才是目前11／11結果。

## 尚未交付

- VI已生成M4A且89窗全部fit；初次音檢session37621已完成，exit1、92 checked／10 flags，均有二轉寫。待正常bounded retake1及重檢，尚未通過。其餘七語M4A未製作，外語ready為0。
- 核心QA當時含zh-TW＋八語共九份CC初稿，不等於八語配音已ready。每語須依自己的實際M4A重對時；既有字幕速度advisory保留。
- 主片audio已送後臺、狀態pending；主片final尚未送，避免自動附帶尚未音檢通過的VI。後臺成片、八語下載／交付及讀回驗證均未完成。未上傳或發布YouTube。

VI媒體實測、初檢flags及逐語狀態見 [localization-review.md](localization-review.md)。下一步是VI bounded retake／音檢、其餘七語生成與音檢、逐語CC對時，以及真正的原生後臺送審／交付讀回。八語預設與推薦決策已有持續授權，不再詢問相同偏好。

## 收據

- `/workspace/work/videos/forty-forest-map/checks.json`、`review/check-flags.json`、`review/qa.json`；來源修復後QA log：`/workspace/work/ai-tech-next/forty-qa-source-link-fixed.log`。
- [敘事審查](narrative-review.md)及 [七句改詞後原生結果](narrative-after-audio-reword1-result.json)；舊raw／native收據未覆寫。
- [production-progress.json](production-progress.json)保存當前雜湊、量測與待項。此快照不聲稱後臺final或八語已交付。
