# B18 企劃審稿收據：800 字元相容繼任版

2026-10-17，`/root/b18_name_delta_review`。**狀態：隔離版資料列審稿收據可通過雙集編譯；正式匯入、逐章查核、付費製作與成片仍 HOLD。**

原 [B18 名稱移除候選](../B18-worker-input-name-trim-candidate-20261017/README.md) 的 `B18.json`、六章、逐景主張與[獨立差異審查](../B18-worker-input-name-trim-candidate-20261017/independent-review-20261017.md)均未改。原 `reviews/B18.json`（SHA-256 `538d6614c00a102fa0a04fb0fa4e3f3ba11719dede4d8353636c37b2f46c2752`）保留。此 [繼任收據](reviews/B18.json) SHA-256 `124b4bea3e08a14e5402370c678b8d53d7f61c6180db5e80c6d4aeff52278114`，與原收據的 JSON 物件**僅 `notes` 欄位不同**：移除已完整列在 row `caveats` 的重複年份、價格、給茶與機械遺產提醒，保留本人核讀法院 PDF 的頁行、worker 不能擷取該 PDF、`reviewer_only=[]` 的原因，以及不指名未證實的啤酒公司。

新版 canonical story SHA-256 仍是 `3c43dc0c0eccdb063cc1e62d756c48ce2a476c5bfe1a70b74799c8f3cfc475f1`。直接使用 `plan.mjs` 得 `reviewProblems=[]`；row `caveats` 394 字元、繼任 `notes` 220 字元，依雙集編譯器加兩個換行後是 **616／800**。六來源讀取狀態與[原驗證紀錄](../B18-worker-input-name-trim-candidate-20261017/review-receipt-validation-20261017.md)相同；本次未更改任何來源或故事主張。

為避免動到另一個代理的產物，我把其 [A01／B18 雙集編譯沙盒](../B18-import-build-20261017/sandbox/)逐檔複製到本目錄 `validation-sandbox/`。`series.json`、`build.mjs`、A01／B18 row 與 A01 review 都與來源沙盒逐位元組相同；僅把複本中的 B18 review 換成上述繼任收據。複本執行 `build.mjs --write` **兩次退出 0，輸出雜湊兩次相同**：`validation-sandbox/docs/videos/brand-stories-pilot-v2-20261015/stories.json` SHA-256 `07a71fc18c3aa12d426dcc1c9ecd30e59c150079a1e83d868b7024c09670c999`，恰有 A01／B18 兩列、序位 1／2，B18 合併 caveats 616 字元。這只是本機可重現的編譯證據，沒有替換原沙盒或正式企劃檔，也沒有主機、媒體或付費呼叫。

65 筆 B18 逐景主張仍為 `UNCHECKED`；此收據只核准新版企劃資料列，不等於正式 worker 查核、聽眾審稿、十三題敘事、TTS 片長、圖片、CC、成片或站主觀看。
