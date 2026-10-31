# S52 R17｜兩次定點重配後的單句口語修訂

2026-10-20 UTC。R16 已通過獨立史料／書面畫面及雙人正式敘事 13／13；只合成新版 18 句，沿用其餘 101 句。R16 第一輪正式 `check-audio` 119／119，僅 `s52127` 旗標（Jev 0.12）。同文定點重配兩次後仍各為唯一旗標：第一次 Jev 0.05、第二次 0.11。三次機器轉寫都未穩定識別「那句『成功』」；沒有可用實際聽音輸入可證實口播錯字，因此不冒稱聽音結果。R16 最後一版私有 `check.json` SHA-256 `7914c36a218623b4cdfaecb186205bc4e99fe788a8735b8de51f8ca1ecf99d87`、該句 WAV `9a08b59e0ea157cb093785a6a8feaf886ef49abb6328bede60219be8805e5f10`；前兩版亦保存在 `/workspace/.video-work/curio-s52/review/r16-before-retake/` 與 `r16-after-retake1/`。已達同文重配兩輪上限。

R17 **只改** `s52127`：

> R16：六月四日那句「成功」，能補齊三個地點每人記下的接觸時刻嗎？
> R17：六月四日的日誌和後來的觀測報告，能補齊三個地點每人記下的接觸時刻嗎？

同一文字只替換於 `video.json` 的一處 `lines[].text` 與 `claims.md` 的對應口播欄；`script.md` 由工具重生。沒有改 `s52127` 的畫面提示詞、史料連結、周圍問答、章名或 21 個伏筆。兩份文本的特定範圍由 [Cook 6 月 4 日日誌 L5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982) 和 [1771 原報轉錄 L140–163](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L140-L163) 界定；下一句仍只說這兩份文本沒有外派兩隊逐人四接觸時刻表，沒有推斷所有史料不存在。這是作者判讀，須另一人核對。

| R17 內容檔 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `0f93f8c414ffe00419b9251800293238713298f018adf845deb8d9b12b2affce` |
| `video.json` | `ba6896e5a95caf1dee4e653702b036c0bc14340857dcb93ad08e97510b7e757c` |
| `script.md` | `767a4b363233dff90f5e933404fa12d885b7ffb92fd950953f2ba1282b55aab6` |

`lint --slug curio-s52 --json`：0 errors／0 warnings、119 句。R17 是**作者候選**；R16 兩位讀者和來源 PASS 綁舊稿，不能搬來。須另一人做單句來源／書面畫面差分，兩名新隔離讀者盲讀 R17，之後才對新句 TTS 與完整 `check-audio`。R16 既有 `narration.wav` 與 `timeline.json` 均為舊稿，R17 未合成音訊或圖。
