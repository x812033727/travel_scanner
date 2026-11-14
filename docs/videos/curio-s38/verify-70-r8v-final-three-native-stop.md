# S38 R8v｜PF015 最終退件；PF016／017 原圖保留

2026-10-22 UTC。[最後候選獨立書審](verify-69-r8v-final-three-prompt-independent.md)按固定 R8v `video.json` SHA-256 `fd506ba278ffbcbb2b17908b957eb9a2163a2d26cd3b2b78556bab365212b7f4` 分別放行 `pf015 → pf016 → pf017`，每景在 EXIT 恢復私有 `STOP` 的單 ID 指令中只生成**第三張、也是最後一張** MiniMax `image-01` 原圖。每張直接查看 1280×720 原生 JPEG 及選圖，再決定下景是否可畫。結果：**PF015 最終 REJECT；PF016、PF017 原圖 KEEP。PF019 未購圖**，沒有第四張或下一章。

| 景 | 原圖／選圖 SHA-256 前 12 碼 | 機器與直接原圖判定 |
| --- | --- | --- |
| `pf015` | `c72e3f9bc4a7`／`6fcd90db587e` | **9.71/10 FAIL；人工 REJECT_FINAL。** 塔上開放平台、低屋頂、煙、成年人物與 2D 風格比前兩輪準確，但石欄後在人物背旁多出**第三隻手**；原圖和裁圖皆清楚可見。不能把解剖錯圖放進成片；**此景不再有第四次生成**。 |
| `pf016` | `576dcbabf390`／`4c81c46f16a8` | **10/10 PASS；人工 KEEP。** 灰鬚成年說話者在石室開口、空手比劃；無地圖、偽字、文件、電燈或制服徽章。深色服飾是卡通簡化，沒有足以把它誤讀為近代軍服的標記；符合口頭轉述的畫面用途。 |
| `pf017` | `ece37bffa96b`／`728004748d86` | **10/10 PASS；人工 KEEP。** 單一人物用空手靠耳傾聽，沒有第三方書面報告、書本或紙張；暗色石室仍能看清動作與表情。人物採系列誇張大頭比例，沒有明確的現代或童裝物件；不把聽聞畫成目擊起火。 |

[完整來源檔、評審、原圖、選圖、日誌及帳本 SHA](verify-70-r8v-final-three-native-inventory.json)已保存。PF016／017 的 CLI exit `1` 是既有 PF015 `needs_review` 使整張圖單未通過；兩景實際都已生成、各有一次評審，且上表原圖已直接檢查。PF015 的 `needs_review: true` 仍在 manifest；不可因其他兩景 KEEP 就送全片 storyboard。

批前私有備份 `/workspace/.video-work/curio-s38/review/r8v-final-pf015-017-pre/` 包含 ledger、manifest、三張 R8u 舊原圖／裁圖，以及九張此前 KEEP 的圖單項目和選圖檔 SHA。批後重算九張 KEEP **全部未變**；新原圖及裁圖在 `keyframes/`，每景 CLI 日誌在 `review/r8v-pf015/016/017-final-native.*`。`STOP` 已恢復，PF009／013／014 的舊退件圖仍不在 manifest。

帳本 **US$0.6640／44 image／43 judge／1 music** → **US$0.7045／47 image／46 judge／1 music**，恰三圖三評審增加 US$0.0405，舊 US$0.0035 預約不動，低於整集 **US$4.58** 上限。ledger SHA-256 `427e1fcb…` → `a4087375…`；manifest `f7a59d91…` → `2517afd9…`。`script.md`／`claims.md` 及旁白都未變。

**後續邊界：**PF015 只能由作者提出**同一章已過圖的來源相容重用**，或用帶 1666-09-02 Pepys 日記出處的引句卡；不可再購圖。PF013／014 已是兩張連續引句卡，如果 PF015 也改卡，會達三張連卡上限，PF016／017 須維持插圖，任何額外卡要重新算上限。PF016／017 的 KEEP 在後續改動 `video.json` 後仍須按新 `pictures_hash` 確認 request key、評審 stamp 和所選檔案 SHA 不變。PF019 書面 PASS 但尚無原圖；PF018／020–022 同樣尚未生成。此回條不放行第一章／全片分鏡、成片或上架。
