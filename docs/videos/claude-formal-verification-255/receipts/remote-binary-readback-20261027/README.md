# Formal：當前23附件完整遠端讀回

核對時間：2026-10-27T06:35:17.186Z。這次補完既有成品的正常完整binary下載驗證；沒有新增或重新上傳音訊／影片。正常工具取得待審紀錄 `e66d6661-c991-42fc-abde-30e942c9fe5b` 全23個附件，逐檔核對完整內容、SHA-256、大小、MIME及角色順序，`not_fetched:[]`。前後兩次完整project GET逐位元組相同，所有payload、審核歷史、站主選擇與核准狀態保持。

當前正式片頭尾版1080p為54,578,838 bytes，SHA `b635269e24134b2c2c0e300a77d03f51ce4c15f2a9bc31cd6e61c0ec87c1162a`；英文M4A為15,391,038 bytes，SHA `af7c3d50693e7231513bdb57e4f404b9491d449dddcad9c12d7c5e931c3a799a`，兩個音軌角色完整下載內容都與當前合格音檔相同。使用 `_formal-bookend-candidate` 官方5秒片頭／21秒片尾版，原canonical舊BODY與舊英文音軌保持，沒有混作新版本。

ROOT重新綁定當前105句英文的完整intended、WAV全hash、synthesis keys、ASR／Jev／第二轉寫證據；80 exact、21 Jev、4 second exact，共105 accepted，0flags／unchecked／skipped／kept。101時間窗fit0over、tempo上限1.15與既有全軌響度−14.1 LUFS／truepeak−2.1 dBFS量測仍綁同一音檔；沒有新執行ASR、TTS、QA、fit或meter。這不是新一輪聽校，也不稱整軌人工逐秒聆聽。繁中106cue、英文108cue皆完整覆蓋105ID；實際字幕、標題說明全文與native current intended一致，九語metadata物件也相同。

舊BODY待審紀錄仍superseded且12refs及其餘欄位保持，七個歷史physical blobs在目前引用下的下載內容與本地原件相等。日本語14flags與stale保持；英文仍是八語中目前完成的1語，其餘七語與正式語言批次未完成。原整片QAfalse10/11、caption未過與8項CPS提醒、敘事未過項與所有重錄／改寫歷史保留，沒有server核准、merge、部署或YouTube上傳。

- [ROOT完整23檔與105句驗核](root-full23-binary-proof.json)
- [正常下載清單](normal-review-files.json)、[實際CLI結果](normal-process-result.json)、[實際退出觀測](normal-observed-exit.json)
- [前GET收據](project-before-GET.json)、[後GET收據](project-after-GET.json)、[原進度快照](before-progress.json)
- [原合格英文proof](../../branding-v4/EN-current-independent-proof.json)、[原QAfalse](../../branding-v4/native-current-QA-false10.json)
- [驗核程式](verifier.mjs.txt)、[獨立靜審](verifier-static-review.md)、[最終增補](verifier-static-final-addendum.md)

Raw project snapshots、權杖、媒體與音檔不進Git；這裡只有文字證據與來源描述。
