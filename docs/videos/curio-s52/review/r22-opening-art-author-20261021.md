# S52 R22｜第二格成年觀測者最後一次書面修正

2026-10-21 UTC。R21 的第一格 `s52001` 原生圖可用；第二格 `s52002` 雖獲 9.71 總分，九題 `subject=0`，原生圖實為持望遠鏡的男孩與奇異擬人器材，已人工退圖，見 [指名試畫回條](r21-opening-native-stop-20261021.md)。私有 `STOP` 保持存在，這輪沒有買圖。

我只改 `s52002.data.prompt` 一葉，把單一動作、短髮且成熟臉孔的 **三十多歲英國成年男子**、1760 年代馬甲和及膝短褲、木架上的普通短望遠鏡及抬起摺疊亞麻布寫清楚；仍在大溪地遮棚下，棚外晴朗。明確去掉多個背景器材，避免產生擬人道具或讓主體混淆。這是概念插畫，不把人物宣稱為格林或索蘭德的真實肖像、器材的確切材質與形制、或文獻逐字記載的揭布動作。Cook 1769 年 6 月 3 日[日誌 L5963–5975](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5975)明載格林、索蘭德和本人觀測、格林與庫克各有 telescope，並記整日無雲；提示詞一人畫面不排除另外兩人在場。

[結構化差分](r22-opening-art-structured-diff.json)驗證現檔 `video.json` SHA-256 **`3e380aa29543a868dd643f588834e188d48c481da4c36e0a738a17968af9ad41`**，只把該新字串換回舊值便逐位元恢復 R21 SHA-256 **`6d2714aa8c5fa3fd30aec85654693085afac4485efca30f69909a28d196ced36`**。遞迴 JSON 唯一差異是 `scenes[1].data.prompt`；brief、research、claims、script 與全部旁白、節奏、其餘 112 景未改。`visualHash=dc38ae420f09bee7`，`speechHash=2af0a08f6e592b5d`；lint 0 errors／0 warnings。

這是 `s52002` 在 R19、R21 兩張人工退件後的最後一次候選試畫：請**非作者先做紙上史實及差分獨立覆核**，PASS 才暫解 `STOP`，只跑 `--shot s52002 --takes 1` 並逐張看原生 JPEG。US$4.46 整集上限不變；目前帳本 **US$0.0540**（4 image、4 judge）。若仍畫錯，停止該景新圖，改用同章合格圖或有意義的資訊卡，另作獨立覆核。站主音訊／分鏡、品牌動畫與成片仍待完成。
