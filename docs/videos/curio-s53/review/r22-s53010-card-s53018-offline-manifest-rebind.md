# S53 R22｜地震日來源卡與南公園窄景私人圖單離線重綁

2026-10-22 UTC。**離線重綁 PASS：14 張既收圖完整保留；`s53018` 僅書面 PASS，原生圖仍待。**依 [R22 獨立紙審](r22-s53010-card-s53018-prompt-independent-paper.md)，只在私人工作區更新 keyframes manifest；沒有執行 image、judge、音樂或其他付費呼叫。

## 凍結依據與原子操作

目前 `video.json` SHA-256 `49bdd04e5ebb88ff98cd207c6da0545faf1d1721834a0dc099d514a2daf9fa99`、`claims.md` SHA `34f765eee27fb0ff083413e3e209b42d5dd09b5a2a7a89f16d14556ce1cac44b`。以 [R22 可逆差分](r22-two-scene-structured-diff.json)還原 R21 場景，工具 `visualHash` 得舊值 `2a9d1106e7fc4f3f`，恰等於舊 manifest；R22 新值是 **`133eba68d1a96469`**，`look_hash=98a370ae40badbaf` 未變。R21 manifest 原 SHA `72399b433a156ee5064f35ee2da318f2495afea8a0eacd9c7ad8b891d7df5164`，ledger 原 SHA `786794fa452fc6049b428726516d86d4e1e7a84aca90fa772658fe26e3081499`；操作前 `STOP` 在位、jobs 空。

舊 manifest 已獨占備份至 `/workspace/.video-work/curio-s53/rebind-backups/r21-manifest-before-r22-card-and-prompt.json`，備份 SHA 仍是 `72399b433a156ee5064f35ee2da318f2495afea8a0eacd9c7ad8b891d7df5164`。在備份及 14 張選圖實際 SHA 驗證後，以 mode `600` 暫存檔原子取代 manifest：只更新 `visual_hash`，刪除 R21 人工未收且機器 FAIL 的 `shots.s53010`、`shots.s53018`，將含這兩張舊圖的 `contact_sheet` 清為 `null`、`contact_sheets` 清為 `[]`。舊 contact sheet 和原 JPEG 留私人區作歷史證據，**新 manifest 無退件景 ID、選圖路徑、request key 或過期 contact sheet 引用**。`thumbnail_source=keyframes/s53005-1.jpg`、`duplicates=[]`、其他頂層欄位及以下 14 筆完整 shot 條目逐項不變；manifest 權限仍 `600`。新 manifest SHA-256 **`96ef6a6d67c03fd37f86963f819f5bdbafce8c72fbb9f04d0bb983b371a04ef5`**。

## 既收選圖實際檔案雜湊

下表逐檔重算 SHA-256，均與備份及新 manifest 的 `sha256` 相符；`s53007` 合規重用 `s53003` 同一張圖。

| 景 | 私有相對路徑 | 實際 SHA-256 |
| --- | --- | --- |
| `s53002` | `keyframes/s53002-1.jpg` | `e17678ab3fd82acd649e9f691f44530e1afdf2a3bc49a2492d753ec2df905690` |
| `s53003` | `keyframes/s53003-1-trim.jpg` | `73823edb92173cf2df2be0f4988f6a25fd3c1044d9387041602c2e171a3f2f2b` |
| `s53004` | `keyframes/s53004-1.jpg` | `17c28641f67e3452e7a08a6255e502dc551da79982dd94d037eadd0adf7cfaa6` |
| `s53005` | `keyframes/s53005-1.jpg` | `55acdbb1a0db155710d578e9e36ec881c09317c6900ee27b86612331fa3b44b0` |
| `s53006` | `keyframes/s53006-1-trim.jpg` | `5b73da5203ed2ac04c8f87d49053ef2af92f6e73313999d7a2a15c3d4180fb9c` |
| `s53007` | `keyframes/s53003-1-trim.jpg` | `73823edb92173cf2df2be0f4988f6a25fd3c1044d9387041602c2e171a3f2f2b` |
| `s53008` | `keyframes/s53008-1-trim.jpg` | `e1dfd630cf38cfc007eb110e3956c5b82a6af9280a37a72b18ba9b68b3a5f6` |
| `s53009` | `keyframes/s53009-1-trim.jpg` | `b957cf0aeee02ea366e48a64c973ca4d38bf41c676e249f0610be841bf641799` |
| `s53011` | `keyframes/s53011-1.jpg` | `812d2941450d2a57d5c11c928b5d4514859723fa491efc779a26aac11207b406` |
| `s53014` | `keyframes/s53014-1.jpg` | `290c0b20d56f3acd3168e1c749bb243580504613c5062c48abba11cf43199b4d` |
| `s53015` | `keyframes/s53015-1-trim.jpg` | `2e63e543f40b7dc000fd1a00dfd42c25f0cac7d53fd6dc58818436a589e728a9` |
| `s53017` | `keyframes/s53017-1-trim.jpg` | `40170d8eb8c2b63517c8a455257a58ec377a03d24d592e1409807e7dc548f278` |
| `s53020` | `keyframes/s53020-1-trim.jpg` | `1954d9dd33a86bfd87b6b6deda88580e0fd568b1dfd26eadc7f24c8212aa626e` |
| `s53021` | `keyframes/s53021-1.jpg` | `2dde34b31fe93a2b676df73dc25fa8304d13413e56aa8560824f2c9cff438bc1` |

## 讀回與下一關

只對這 14 張 KEEP 執行工具 `keyframeProblems` 得 **0 問題**。完整 R22 有 114 個 `shot`，尚有 **100 景缺合格圖**；完整檢查恰列 100 個缺圖，沒有退件／毀損圖錯誤。`s53010` 不再是 `shot`，沒有缺圖或圖單條目；工具 `renderPlan` 將它輸出為 `big`／`stills` 卡，文字含「1906 年 4 月 18 日｜舊金山／地震之後，又起大火／1913 年《舊金山救濟調查》回顧」，HTML 不引用退件圖。`s53018` 現為缺圖而非錯誤沿用 R21 圖。

操作後 ledger SHA 仍 `786794fa452fc6049b428726516d86d4e1e7a84aca90fa772658fe26e3081499`，即 **US$0.4590／35 image／34 judge／0 預約**，低於整集 US$4.78；jobs SHA `a9d2c69ab3cb5704417b4f0968a7d8d0dae6eb0e35d37e053463220b30d55ca3`、jobs 空、`STOP` 在位。下一步只能在 R22 精確雜湊及即時額度再次核對後，對 `s53018` 做一張第三／最後原生圖和 judge，原圖／裁圖逐張看；**不得買第四張 `s53010`**。本回未核准完整第二章、網站卡、人耳、音樂或成片。
