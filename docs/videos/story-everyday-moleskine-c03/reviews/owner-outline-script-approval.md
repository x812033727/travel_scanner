# C03 Moleskine｜站主核准企劃與劇本

2026-10-22（臺北）。站主在本次對話看到「C03 已依奇聞檔案局規則更新；草稿 PR #1652 含企劃、94 句劇本與重剪收據」及核准範圍後，明確選擇「**核准目前企劃與劇本**」。這是目前稿件兩關的核准；不含音訊、分鏡、完整試片、上傳或發布。

| 關卡 | 本機核准紀錄時間（UTC） | 目前檔案 SHA-256 | 讀回 |
| --- | --- | --- | --- |
| outline／`brief.md` | `2026-10-22T02:13:08.908Z` | `6e2666b5ce66bfe098b31ff0426496127258adae0185b4e1458f88bde0229671` | `status` 顯示已核准，與檔案雜湊吻合 |
| script／`script.md` | `2026-10-22T02:13:10.298Z` | `5f148061a2fa4bb89a42b1d91adfa67a6bad4796ee5a44b82f1eea473722cb46` | `status` 顯示已核准，與檔案雜湊吻合 |

以 `node tools/video/cli.mjs approve --slug story-everyday-moleskine-c03 --gate outline|script --note ...` 把上述明確站主回覆寫入工作區 `approvals.json`；隨後重算兩個檔案 SHA-256 並讀回 `status`，兩關皆為 `[x]`。沒有改動這兩份被核准檔案。

後台先前由 `review-push` 建立的兩筆送審，`review-pull --gate outline` 與 `--gate script` 目前仍回報 `waiting for the owner`；本機核准不等於後台紀錄已同步。嘗試開啟後台瀏覽器頁時，瀏覽器 webview 連接逾時，未在後台按核准。後續如要讓後台也顯示同一決定，須核對它收到的檔案雜湊與本收據相同，再依站主這次核准同步；不得把後台的待審狀態寫成已核准。

目前 `timeline.json` 仍對應「七十八家」的舊句；`c031202` 更正為「七十九家」後，Gemini TTS 三次受控執行均遇 HTTP 429。音訊關卡仍未核准，舊 02–20 段 481.25 秒讀值不能證明更正版符合至少 480 秒正文規格。
