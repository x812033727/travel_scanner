# S52 R12｜固定來源與書面畫面獨立差分覆核：PASS

2026-10-20 UTC。**史料 PASS、書面畫面 PASS**，只適用於下列精確五檔；敘事雙盲、政策、真實語音與成片仍須另驗。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `8b5ece5ba66ecd672f6d8b89dd8191f087734f1d7277abce1fedca32b663f699` |
| `video.json` | `a23d2d57147f327e2f0c61283395e71ee5ede03374ef95e7468d815ffd14ceed` |
| `script.md` | `b9bae5c830d5e1260c4a034318f8bcede8a9824affa482b24d50a0e4a032be99` |

重新核對 R11 [獨立查核](r11-source-independent.md)所用 Cook 日誌固定原文 [C 5950–5961](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5950-L5961)：Gore 一支去 Eimeo，Hicks 另一支去大溪地東面。R12 `s52128` 書面提示詞現為 `two unfilled off-site timing columns`，與兩支外派隊相符，畫面是研究桌上的無字概念圖，不裝成保存下來的真實逐人秒數表。主站是第三處觀測點，**不是**第三個外派地點。

位元組差分：將本版 `video.json` 中唯一一次 `two unfilled off-site timing columns` 反向替回 `three unfilled off-site timing columns`，算得舊 R11 SHA-256 `3b4ae5f3dfda56df5b7d5a18fa397e62ced2e0936bec2350bae03cdc613721c9`，與 R11 作者凍結完全相同；故除這一個英文數量詞外，分鏡、旁白、來源、片尾及其餘提示詞均未改。其餘四檔 SHA 也與 R11 獨立查核對象逐一相同，原有史料 PASS 適用。`video.json` 仍有 118 景、120 句對齊主張表、115 張插圖／2 卡／1 片尾；`lint --slug curio-s52 --json` 為 0 errors／0 warnings。`git diff --check` 通過。
