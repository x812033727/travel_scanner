# S52 R14｜史料與書面畫面獨立差分覆核：PASS

2026-10-20 UTC。此結論只適用下列精確內容檔；敘事雙盲、政策、實際語音及媒體仍待另驗。R12 曾對其餘逐句主張與書面畫面做 [獨立覆核](r12-source-independent.md)；本次重新核對 R13 的三句改稿和 R14 的一景時間提示詞，不把作者凍結紀錄當成史料。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `f133ff0dbed147fb7c06130db9a2f39a1202c6d73ca4e3d67c1f5aa6f2dde53d` |
| `video.json` | `e04880a6bec0b9cdcb517e0215de9060bb65844021d2f05e20a8234251a8a445` |
| `script.md` | `e1d04c2bd2e126baf5f777f8237cc1e4c075fdfc465ef6a183ec861fd212ae9c` |

我從固定提交網址重新下載 [R：Green／Cook 1771 原報 OCR](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt)，位元組 SHA `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`，以及 [K：Kippis 後出傳記](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt)，SHA `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`；兩者均與研究表記錄相符。

| 改動 | 獨立核對 |
| --- | --- |
| `s52053`「到了五月，儀器何時才安置好？」 | R 第 5 行明說儀器到 **5 月 10 日**才安置妥當；這是下一句的答案。刪去重複的四月雲況沒有造成因果暗示。書面鏡頭已由 `late May 1769` 改為 `early May 1769`，是五月十日前後的概念場景，不冒稱實物影像。 |
| `s52116`「還記得基皮斯那張表嗎？只靠它，真能算出三人相差幾秒嗎？」 | K 第 1165–1178 行只列 **Green 一人**的四格接觸時刻；R 第 140–163 行才另列 Cook、Solander 與接觸辨認。問題對來源層級及無法僅靠 K 算三人秒差的限制正確，畫面是後來閱讀桌、無字書和三張空白記錄條，沒有杜撰原件。 |
| `s52316`「原報中的『碰到』，究竟指哪一道邊？」 | R 第 150–163 行明辨暗影、金星本體邊與微弱亮線，設問確實通向後段答句。畫面為檔案室無字太陽／圓點示意，不宣稱取得原刊圖版。 |

R14 `video.json` 只有一處 `early May 1769`；逆向替換回 `late May 1769` 算得 R13 凍結 SHA `46ccd8047247b5a7ed143de1da813814c74e9371995745103ea764188c1ca328`，其他四檔 SHA 與 R13 相同。作者 R13 的三句改動及其主張列已逐一查過；R12 其餘句子／提示詞的獨立結論適用。`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s52 --json` 為 0 errors、0 warnings，120 句。**史料 PASS、書面畫面 PASS；並非敘事、語音或成片放行。**
