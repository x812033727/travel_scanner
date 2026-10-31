# S52 R15｜刪除重複場景的獨立史料與書面畫面覆核：PASS

2026-10-20 UTC。此結論只適用以下精確五檔；敘事、政策、實際配音和畫面均須另驗。前一版的 [獨立逐句與書面畫面查核](r14-source-independent.md)為 PASS，本版按新內容重新檢查刪除的場景、保留的回收句及所有 ID／文字對齊。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `aed770f9ac194db89305ff8aa4ac3fdf87e800c356a32280c189a2690b0fd977` |
| `video.json` | `9ab5b5cc77ef6f0ea0fed5ce056a90e390964b6f63f44042657bd58c0f655068` |
| `script.md` | `1764cc03aa5bb5ea402e89b7e21e163d676045c6e42611dfaa54fdc69fa62131` |

R14 被雙讀者共同否決的 `s52315` 同時從 `video.json`、`script.md` 和 `claims.md` 消失；它與前一句 `s52122` 重述同一件事，刪除沒有遺失獨立史料資訊。開場 `s52007`「後出那張四格表之外，還有誰的接觸記錄？」的 loop 回收點現為仍在稿中的 `s52122`：「皇家學會的刊物把格林、庫克與索蘭德的觀測分別列出」。重新核 [1771 年 Green／Cook 皇家學會原報轉錄 L140–163](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L140-L163) 確有三人分列，沒有拿機讀 OCR 的殘缺數字算三人的秒差。`s52122` 畫面只把三張空白概念記錄條分開放在後來的閱讀桌，沒有偽裝成原件。固定原文位元組 SHA-256 為 `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`，與研究表一致。

本版 `video.json` 的 117 景含 114 插圖、2 工具卡、1 片尾；119 句仍各有相同 ID／文字的主張列，21 條 loop 端點均存在。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s52 --json` 回報 0 errors、0 warnings。刪去一個來源已查的重述句不新增歷史主張；保留的書面畫面沿用 R14 查核，故 **史料 PASS、書面畫面 PASS**。真實正文八分鐘仍須 TTS 實測；作者的最快語速估算約 8:12。
