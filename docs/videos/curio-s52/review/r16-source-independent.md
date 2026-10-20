# S52 R16｜18 句口語改寫的獨立史料與書面畫面差分

2026-10-20 UTC。**旁白史料 PASS；主張對齊 PASS；書面畫面 PASS。** 此裁決只適用下表五檔。敘事雙盲、R16 實際 TTS／聽音、站台卡片、插圖及成片仍各有自己的關卡。

| 檔案 | SHA-256 |
| --- | --- |
| `brief.md` | `3463fced92403975e91bb624216370f9e56ac603348336c037929f4084efc5df` |
| `research.md` | `644adc7e538ca85fe1e1b6e274293b7cc39c54c8bd94b0e8decb5466072b038a` |
| `claims.md` | `dfff33996d540d8c5d083190510bf5a9564a2283f6b6e63c83eece22cd6431f8` |
| `video.json` | `24ff83fc63a92a6b36875d0ed0bca163906b96fdeb1fc961fa2158ac56692079` |
| `script.md` | `a5e75f568c542b6918b393c3485f2a1a18eb23c3b53dabbddf5f50f9d7c3747a` |

## 獨立重開與精確差分

重新核本地固定原文全檔 SHA：Cook／Wharton 1893 轉錄 `c00d08c12188eaf17d8f631e22e5b36882af8f5f6ee0bfe469e8601d9b8cf536`，Kippis 後出傳記 `c723fd1d180efb3c55e783fc156018741cb9bc7b1402c3a490f50a65b31f9956`，1771 年皇家學會原報 OCR 轉錄 `d7b32ca98aadd3a652748091eabc1c1ff329ed5e6df51498fbb5d20ff6b21a74`。來源固定 URL 與可說範圍見 `research.md`。OCR 表格仍不適合逐格計算秒差。

獨立以 18 列舊口播逆向還原現版 `video.json` 與 `claims.md`，得到前版已獨立通過的 SHA `9ab5b5cc77ef6f0ea0fed5ce056a90e390964b6f63f44042657bd58c0f655068`、`aed770f9ac194db89305ff8aa4ac3fdf87e800c356a32280c189a2690b0fd977`。因此本版分鏡、畫面提示詞、章名、伏筆、卡片及其餘 101 句確實未改；18 列主張文字均與 18 句新版口播相同。全稿 119／119 有對應主張列。

| 改句 ID | 重開原文後的判斷 |
| --- | --- |
| `s52004`, `s52078`, `s52116`, `s52118` | [Cook 日誌 5963–5971](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5963-L5971)確稱三人接觸讀時差距出乎意料；[Kippis 1165–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1165-L1178)只印格林一組四時刻。新版問句把「三處逐人」和「三人」分開，沒有聲稱可從後出表計算差值。 |
| `s52301`, `s52303`, `s52094`, `s52117`, `s52306` | [Kippis 598–617](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L598-L617)列馬克薩斯與友誼群島候選；[1151–1178](https://github.com/GITenberg/Narrative-of-the-Voyages-Round-the-World-Performed-by-Captain-James-Cook--13-With-an-Account-o__7777/blob/4e42d95f91cc87a616b030b0f1e2e58776332fd1/7777.txt#L1151-L1178)記前夜擔心天氣、表前 `According to Mr. Green`。新版以「後來出版的傳記」準確交代後出層級，四格表仍只屬單一觀測者。 |
| `s52314`, `s52054` | [原報 5–15、53–55](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L5-L15)載等高度觀日校鐘及六月三日欄、儀器五月十日安妥；[Cook 5941–5944](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5941-L5944)另記五月三十日仍忙觀測準備和教人。新稿未把兩個層次混成器材尚未就位。 |
| `s52070` | [Cook 5950–5955](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5950-L5955)明寫格林替 Gore 外派隊備儀器；[1771 原報開頭](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L1-L3)列他曾任格林威治皇家天文台助理。「觀測處的天文學家」是可接受的口語指稱。 |
| `s52122`, `s52316`, `s52321`, `s52324` | [原報 140–163](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L140-L163)分列 Green、Cook、Solander，並描述離開時亮線逐漸中斷、暗影和實體邊緣難辨。新版不填 OCR 損壞的數字，也不歸因於某單一現代光學效應。 |
| `s52127`, `s52128` | [Cook 5977–5982](https://github.com/GITenberg/Captain-Cook-s-Journal-During-His-First-Voyage-Round-the-World--13-Made-in-H.-M.-Bark--Endeavo__8106/blob/2db69c74a62f35649149b141a437a05fc0f9fdab/8106.txt#L5977-L5982)只稱外派隊成功返回；本集使用的[原報 140–163](https://github.com/markjhill/2025-helsinki_cascade/blob/2ac861600a431e8cb2e2eae3b1cdcd33b7350207/data/rsc/Royal_Society_Corpus_open_v6.0_texts_txt/Royal_Society_Corpus_open_v6.0_text_106113.txt#L140-L163)沒有外派兩隊逐人四接觸表。新版把否定限制在這幾份固定文本，沒有斷言其他史料不存在。 |

`lint --slug curio-s52 --json` 回傳 0 errors／0 warnings、119 句。最快 325 CPM 正文估時 8:25.43 仍是文字推算；R15 WAV 綁舊稿且有 18 個未經實聽清除的旗標，本報告不將其轉成 R16 音訊 PASS。兩位全新隔離讀者對本版劇本的 13 題盲評仍待合併。
