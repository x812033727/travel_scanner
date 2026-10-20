# S52 R17｜單句獨立史料與書面畫面差分

2026-10-20 UTC。**史料 PASS；主張對齊 PASS；書面畫面 PASS。** 本裁決只適用下列五檔的 R17 文字版。兩位新讀者的敘事盲評、新句 TTS／全篇音訊、站台卡片、插圖和成片仍須各自驗收；R16 的音訊及簽核不移作 R17 結果。

| R17 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `0f93f8c414ffe00419b9251800293238713298f018adf845deb8d9b12b2affce` |
| `video.json` | `ba6896e5a95caf1dee4e653702b036c0bc14340857dcb93ad08e97510b7e757c` |
| `script.md` | `767a4b363233dff90f5e933404fa12d885b7ffb92fd950953f2ba1282b55aab6` |

## 重新核對固定原文

- 重新核完整本地 [Cook／Wharton 1893 日誌轉錄](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)，SHA-256 `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`。6 月 4 日條說派去觀測的人當晚 `return'd with success`，沒有逐人接觸時刻。這是經 1893 編輯轉錄的庫克視角，不能把「成功」擴充成逐筆數據均準確。
- 重新核完整本地 [1771 年皇家學會原報的 OCR 轉錄](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L140-L163)，SHA-256 `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`。L3 標明 1771-11-21 宣讀；L140、146、162 分列本站 Green、Cook、Solander，L160 只概述異地觀測者也見到類似現象。全文 342 行未出現 Hicks、Gore、Monkhouse 或 Sporing 的逐人四接觸表。OCR 數字拼接，這裡只核表的存在與文字敘述，不取秒數。
- R17 `s52127` 問「六月四日的日誌和後來的觀測報告，能補齊三個地點每人記下的接觸時刻嗎？」；緊接 `s52128` 答這兩份文字不能補齊外派兩隊的逐人四接觸表。日期、後刊來源層級和問答界限均符合固定文本。這不主張所有其他史料都沒有外派記錄。

## 精確差分與對齊

R16 `s52127` 是「六月四日那句『成功』，能補齊三個地點每人記下的接觸時刻嗎？」；R17 只把該句改成上述明指兩份文獻的問句。在 `claims.md` 和 `video.json` 各將新版句子逆換一次，所得 SHA-256 分別是 R16 已核版的 `dfff33996d540d8c5d083190510bf5a9564a2283f6b6e63c83eece22cd6431f8` 和 `24ff83fc63a92a6b36875d0ed0bca163906b96fdeb1fc961fa2158ac56692079`。所以兩檔除此句外完全相同，`s52127` 的 blank-chart 概念提示詞、運鏡、史料連結、其餘 118 句、章名、伏筆和片尾欄位未動。

現版 `script.md` 與 `screenplay(video.json)` **逐位元相同**。把 `video.json` 的該句逆換，再由同一工具重生劇本，所得 SHA-256 `a5e75f568c542b6918b393c3485f2a1a18eb23c3b53dabbddf5f50f9d7c3747a`，正是 R16 劇本；末尾 `narrative`／`speech` 雜湊依改句更新，無額外敘事變動。119 句 ID 唯一，與 `claims.md` 的 119 列 ID／逐字旁白全部對齊；`lint --slug curio-s52 --json` 回傳 0 errors、0 warnings、119 lines。
