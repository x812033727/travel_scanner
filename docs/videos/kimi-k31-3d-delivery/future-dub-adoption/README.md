# Kimi 外語文字正式採用與參考字幕更新

紀錄：2026-10-28T05:28:14.212676+00:00。前一輪[18句未採用候選](../future-dub-text/README.md)中的17句，已依當前114句繁中稿重新獨審，經正常 captions-only sheet／merge 正式採用；西文gzek保留原句。六語為en／ja／es／pt／id／vi，全八語其餘895句（其中六語未改667句）與全部標題說明、章節、縮圖、source_hash保持。當前18句對照見[採用紀錄](edits.json)。

本輪選定18句總字元1222→1094，估算超窗18→14；**全八語912句另行完整計算為565→561處超出原max_chars估算**。前一輪的18處只指選定子集，不能當作全片總量。估算沒有調高，這些數字也不是實際語音fit失敗或通過。

正常工具只跑sheet1、merge1、captions1，真退出0；32份修改前檔案保留獨立bytecopy。九語仍1363段、當前字幕速度／版面問題0；1026個原句時窗端點保留，1009個未改群組完全相同。日文boyv原生換行將「検査」分成兩行，作非阻擋注意保留，沒有手動改門檻或強制斷行。[原生核對](native-verification.json)、[獨立實檔審查](post-native-peer.json)、[六語SRT／VTT](../captions/voice-text-adopted/README.md)。

同一筆待審成片`b1893aaf-a60c-4d4f-a7fd-ef39a1de112e`的六個current參考SRT已更新，附件42→48；六個舊SRT以`evidence_prev_cc_narration_LOCALE_voice_r1`保留。原42個binary內容仍有引用，其他36個完整FileRef欄位與順序、完整payload、QAfalse、九語metadata、站主選擇及審核歷史完全保留。六個新SRT全部HTTP200完整下載，大小／SHA／MIME／UTF8與當前檔案一致。[實際後台核對](backend-verification.json)、[獨立完整收據審查](backend-peer.json)。

本輪Mokaair為基線GET1，加交付階段GET4／PUT6／POST1／新檔完整GET6，共18個HTTP、auth讀取2、付費請求0、project PUT0。工具真退出0、project lease正常釋放；API沒有原子CAS，僅主張觀察到的送出前後一致。沒有重下舊42個binary、重hash或decode舊整片及114WAV；這些既有媒體僅核對stat身份與既有收據，不能當新fullmedia驗證。

**仍未完成：114句繁中master聽校，以及八語合格M4A與配音對時CC（均0/8）、source／final核准、核准版上架包和語言批次。** 這批CC仍是`timing:narration`；source／正文影音、原QA10/11 overallfalse、R4false、所有unknown journal／失敗／retake與rewrite上限／四份hold保持。六語未來intended配音fingerprint因正常改文而變，沒有已有外語音檔被宣稱合格。舊PREP和所有先前審核完整留存；no-auto-merge，不合併、部署或上傳YouTube。
