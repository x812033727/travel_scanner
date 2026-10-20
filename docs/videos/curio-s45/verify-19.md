# S45 R9｜政策判讀與精確劇本交接

2026-10-20。R9 `script.md` SHA-256 `cd51d875c9ccee9b6d99caf4da66a06d0b8f8ac22f2160a8de0d8ad33905e2c8`、`video.json` `f0a29e1116363409392af7dca68c32e6d7ec6f9a08fe937aaadb42e36cddecec`、`brief.md` `965d4f46b1b90cad9d52882ca5187003c42ca9a897debc874fbc0937d5a40909` 對應[獨立史料／書面畫面 PASS](review/r9-source-independent.md)及[兩名隔離讀者合併敘事 PASS](review/r9-official-panel.md)。以下只記這些精確版本後續關卡，不轉用 R8 的劇本或音訊結果。

一次完整 `policyRequest({ doc, brief })` 於 15:38:04 UTC 回覆 HTTP 成功，請求 SHA-256 `97c380fadb91f65473c53e87ea4e93c4f2977ed050cecc5cb22a32c00bad8a1d`、回條 SHA-256 `35f2af0c25f6d2ce0741fd16519816c952ccd6549fc676cb37967c86344fa694`，私有檔 `/workspace/.video-work/curio-s45/review/policy-pre-tts-r9.json`。Jev `explainer` **PASS**：「符合立場 0.77、有示範不適用、建議 0.02、業配 0.02，通過」。此次不截短劇本、不重送相同請求。政策 PASS 不等於史料、聲音或網站核准。

`review-pull` 讀到網站大綱／舊劇本核准都屬過期版本，精確大綱仍 `waiting for the owner`。`review-push --gate script` 把 R9 劇本送站台，回覆 `hand_pushed`／**pending**，需站主於 `/admin/videos` 決定；不標為網站核准。使用者持續授權「採推薦、不要例行詢問、做完後繼續」，本地 `approvals.json` 在 15:38:51 UTC 針對上方精確 R9 劇本記一筆**明示為本地委派編輯決定**的 script approval；註記同樣說明站台仍 pending。大綱內容 SHA 與 R8 本地核准相同，工具狀態仍顯示 `outline approved`。

以當前工具及既有語音快取作 `tts --dry-run`：102 個旁白請求中 **23 句需新合成**，約 667 計費字元；Gemini Sulafat 就緒、當月尚餘 8603829 字元。這是合成前估價，**不是**音訊檢查或實際使用量。R8 的 23 個官方音檢旗標仍是舊音訊 HOLD；R9 必須新合成並全片重驗，零旗標且有可查聽審前不進插圖或組片。
