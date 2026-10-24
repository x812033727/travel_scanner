# C08 short-v8 本機試片與後台交接狀態

日期：2026-10-24（Asia/Taipei）。本檔把已完成的前製、條件式報價和仍缺的實測分開；請依每集真實檔案與正式站讀回更新，不能拿這張表代替驗收。

| 關卡 | 目前證據 | 狀態 |
| --- | --- | --- |
| 企劃、36 句劇本、36 鏡方向 | 站主精確核准 v8；來源及配鏡各 36／36，雙盲讀無共同否決 | 通過前製 |
| 可執行機器稿 | 頂層 `story-everyday-kikkoman-c08-short-v8`、30 `shot`／6 `stats`、凍結來源及 pronunciation snapshot | 本機完成 |
| 程式與時長審核 | lint 0 errors／7 warnings；QA 7199／7200 body 與 9000／9001 final frame 邊界通過；獨立 DURATION_ONLY 收據 SHA `926ee0480dc3a8ef51898fa2cf067af1000a75ebbc31fe0218287dbc2e451dc3` | 僅測試通過 |
| 繁中語音、念法、實長 | `MoMA` 的文字念法有獨立審核；沒有實際 TTS、人工聽音或本集正文至少 240 秒的實測證據 | HOLD |
| C08 整支費用 | [`production-quote.md`](production-quote.md) 提議 30 圖各最多 3 次、36 句各最多 1 次有據重錄、一首配樂、整支 US$25 | 待站主核准 |
| 專屬預算路由 | 目前帳戶清單不含 C08；供應商、價格、歷史費用及請求保留未讀回 | HOLD |
| 圖像及成片 | `v7e03` 圖解、真圖評審、按秒插圖占比、繁中 CC、final.mp4、播放器驗收都未完成 | HOLD |
| 後台同一集匯入 | 本機 SQLite 模擬證明舊 slug → short-v8 只更新 planned C08 row；正式站 dry-run／apply 和 row ID 讀回未做 | HOLD |
| 上傳／發布 | 尚無成片、上傳包、Studio 驗收或發布決定 | HOLD |

下個安全動作是獨立審查報價與單集預算設計；任何首筆付費都要同時滿足站主核准、可歸因帳本、實際供應商價格及停線測試。若正式站連線未解鎖，先保留本機前製與 PR，不把本機 SQLite 模擬寫成正式站匯入。
