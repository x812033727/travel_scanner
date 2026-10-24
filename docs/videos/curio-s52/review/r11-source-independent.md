# S52 R11｜固定原文與書面畫面獨立覆核：史料 PASS／畫面 HOLD

2026-10-20 UTC。此判定只綁定以下五檔；不代表敘事、政策、真實配音或成片已通過。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `8b5ece5ba66ecd672f6d8b89dd8191f087734f1d7277abce1fedca32b663f699` |
| `video.json` | `3b4ae5f3dfda56df5b7d5a18fa397e62ced2e0936bec2350bae03cdc613721c9` |
| `script.md` | `b9bae5c830d5e1260c4a034318f8bcede8a9824affa482b24d50a0e4a032be99` |

另從三個固定提交的 raw URL 獨立重新下載 Cook 日誌 C、Kippis 傳記 K、1771 年 Green／Cook 皇家學會原報 OCR R；完整位元組 SHA-256 分別為 `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`、`c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`、`d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`，與研究表相同。R 是原報**機讀轉錄**；未將錯列的數字當原刊影像精確讀秒。

**史料 PASS。**重開 C 5375–5425、5439–5457、5941–5982 與 K 600–624、1133–1185，R 1–15、53–56、140–163，逐段對照現有 120 句、主張列及末段推論。R 第 5–10 行支持 5 月 10 日安置妥當的器材、木架防碰動、望遠鏡與象限儀；第 12–15、53–55 行確有太陽等高度及校鐘表，後表含 6 月 3 日條。R 第 140–163 行分列 Green、Cook、Solander；Cook 明說初見暗影、實體邊緣稍晚且他與 Green 都未記下當刻時刻，亮線漸斷與最後外接觸有幾秒難定。K 第 1165–1178 行的四格僅歸 Green。C 第 5977–5982 行只稱外派人員「帶著成功返回」，R 全文亦未列兩支外派隊各人的四接觸時刻；末句只限定**這份日誌與這份原報**，沒有說別處史料都沒有。R11 來源表與說明欄保留 4 月 15 日死者、大溪地人無獨立證詞、後出編者與 OCR 的限制。`video.json` 118 景、120 句 ID 唯一，與 `claims.md` 的 120 列同序同字；115 張 `shot` 提示詞均非空，2 張資料卡、1 張片尾；lint 0 錯誤／0 警告。

**書面畫面 HOLD，一處必修。**`s52128` 的提示詞寫 `three unfilled off-site timing columns`（**三**欄「外派地點」）；但 C [5950–5961](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5950-L5961)只記兩支外派隊：Gore 去 Eimeo，Hicks 去大溪地東面；第三處是**主觀測站**，不是第三支外派隊。請將此提示詞窄改為 `two unfilled off-site timing columns`，或明確把第三欄標為主站且仍保持無字概念示意；前者較簡單。旁白 `s52128` 和主張列毋須改。改動 `video.json` 後須重算精確雜湊、重跑 lint，並由另一人對變更的書面畫面做差分覆核；舊畫面判定不能套到新位元組。除此之外，新加入的 R11 提示詞都是無字概念畫面，沒有把 OCR 表格畫成可信讀秒原件或令人裸眼直視太陽。
