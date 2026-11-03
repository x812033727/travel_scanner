# 繁中加八語字幕文字檔

這18份SRT／VTT由正常字幕工具產生，跟隨實際繁中旁白與正式片頭片尾的成片時間。全部 `timing:narration`，不是外語配音時間；八語經當前音檔聽校的M4A仍為0/8。

正常字幕階段於台北2026-10-27 00:43:01完成；ROOT於00:44:04記錄逐語SRT單調時間窗與正文／片頭尾界線核對。該本地字幕階段不構成全片聽校或伺服器核准；後續實際後台交付另記於下方。

| 語言 | SRT | WebVTT | Cue數 | 閱讀速度注意 |
| --- | --- | --- | ---: | ---: |
| zh-TW | [下載SRT](zh-TW.srt) | [下載VTT](zh-TW.vtt) | 119 | 0 |
| en | [下載SRT](en.srt) | [下載VTT](en.vtt) | 134 | 2 |
| ja | [下載SRT](ja.srt) | [下載VTT](ja.vtt) | 185 | 3 |
| ko | [下載SRT](ko.srt) | [下載VTT](ko.vtt) | 182 | 0 |
| es | [下載SRT](es.srt) | [下載VTT](es.vtt) | 165 | 15 |
| pt | [下載SRT](pt.srt) | [下載VTT](pt.vtt) | 158 | 10 |
| id | [下載SRT](id.srt) | [下載VTT](id.vtt) | 164 | 13 |
| vi | [下載SRT](vi.srt) | [下載VTT](vi.vtt) | 141 | 3 |
| th | [下載SRT](th.srt) | [下載VTT](th.vtt) | 116 | 1 |

共1,364個cue、0語言被略過；47項閱讀速度注意事項完整保留在[原生manifest](manifest.json)。正常門檻保持繁中9、日文8、韓文12、英文20、西文／葡文／印尼文／越南文17、泰文15字／秒，沒有調低門檻或清除問題。

字幕存在不代表字幕品管已通過。未來若改譯文、配音或實際時間窗，須按正常流程更新該語字幕與相關查核。

[正常字幕收據](../../receipts/production/normal-caption9.json) · [ROOT實際字幕與縮圖核對](../../receipts/production/root-actual-CC9-inspection.json)

後續正常整片QA的captions項為true，仍完整附帶47項速度注意事項；整片總結果為10/11、overallfalse，旁白未核准。後續九語SRT已真正加入同一筆待審成片，正常review-files於台北2026-10-27 01:34下載全部13個附件，ROOT於01:37逐檔完成內容大小與SHA-256核對；請讀[後台字幕交付收據](../../receipts/production/backend-CC9-complete.json)與[完整下載核對](../../receipts/production/root-final13-binary-readback.json)。後台text/plain下載副檔名為 `.txt`，內容與此處 `.srt` 完全相同；沒有外語音檔、dub對時或核准推論。
