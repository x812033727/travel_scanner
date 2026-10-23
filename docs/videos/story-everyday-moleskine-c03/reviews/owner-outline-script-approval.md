# C03 Moleskine｜站主核准企劃與劇本

2026-10-22（臺北）。站主在本次對話看到「C03 已依奇聞檔案局規則更新；草稿 PR #1652 含企劃、94 句劇本與重剪收據」及核准範圍後，明確選擇「**核准目前企劃與劇本**」。這是目前稿件兩關的核准；不含音訊、分鏡、完整試片、上傳或發布。

| 關卡 | 本機核准紀錄時間（UTC） | 目前檔案 SHA-256 | 讀回 |
| --- | --- | --- | --- |
| outline／`brief.md` | `2026-10-22T02:13:08.908Z` | `6e2666b5ce66bfe098b31ff0426496127258adae0185b4e1458f88bde0229671` | `status` 顯示已核准，與檔案雜湊吻合 |
| script／`script.md` | `2026-10-22T02:13:10.298Z` | `5f148061a2fa4bb89a42b1d91adfa67a6bad4796ee5a44b82f1eea473722cb46` | `status` 顯示已核准，與檔案雜湊吻合 |

以 `node tools/video/cli.mjs approve --slug story-everyday-moleskine-c03 --gate outline|script --note ...` 把上述明確站主回覆寫入工作區 `approvals.json`；隨後重算兩個檔案 SHA-256 並讀回 `status`，兩關皆為 `[x]`。沒有改動這兩份被核准檔案。

2026-10-22 約 10:13（臺北）時，後台先前由 `review-push` 建立的兩筆送審，`review-pull --gate outline` 與 `--gate script` 仍回報 `waiting for the owner`；當時本機核准尚未同步到後台。第一次嘗試開啟後台瀏覽器頁時，webview 連接逾時，當時未在後台按核准。

## 後台同步讀回（2026-10-22 10:46 臺北）

之後透過已登入的 `https://mokaair.com/zh-TW/admin/videos` 找到 `story-everyday-moleskine-c03`，讀到當前劇本 **94 場、94 句**及更正的「七十九家」，大綱企劃書也載明 **73 張插畫、21 張卡片**。依站主本次明確核准，依序按「用這個大綱」與「核准劇本」。頁面「過去的決定」兩項均顯示「已核准」，決定時間皆為 **2026-10-22 上午 10:46**；目前沒有等站主決定的項目。這是瀏覽器 UI 讀回與本機核准的對照；後台沒有顯示完整檔案 SHA，不能聲稱後台直接核對了上表兩個 SHA。

| 後台畫面截圖（本機工作區 `review/`） | SHA-256 |
| --- | --- |
| `admin-outline-approved.png` | `f390ea5bc7e49bf4d88f20cff44aa53e0816d0014237efc03da4dded95dc9263` |
| `admin-script-approved.png` | `30c17b7346060bc58413bc2176c58e005f3e49d712df2b9c53f39e75d908d32e` |

再次執行本機 `review-pull --gate outline` 與 `--gate script` 均印 `already recorded`，因為本機 `approvals.json` 已有這兩筆站主決定；這兩行輸出本身**不是**後台讀回證據。後台讀回以上述頁面決定列與截圖為準。此操作沒有核准音訊、分鏡、成片、上傳或發布。

目前 `timeline.json` 仍對應「七十八家」的舊句；`c031202` 更正為「七十九家」後，Gemini TTS 三次受控執行均遇 HTTP 429。音訊關卡仍未核准，舊 02–20 段 481.25 秒讀值不能證明更正版符合至少 480 秒正文規格。
