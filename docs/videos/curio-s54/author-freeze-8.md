# S54｜作者第八版凍結：兩句敘事修正

2026-10-20 UTC。第七版 [獨立史料與畫面覆核](review/r7-source-independent.md) 已 PASS；[兩位隔離盲讀正式合併](review/r7-isolated-merge.md) 的官方 OR 判定為 **12/13 Yes，僅 `no_recap` FAIL**。讀者 B 另指出三總局售票的問題問「誰反對」，答案只說「部門」；讀者 A 判 `payoffs` Yes，因此官方 OR 在該項 PASS。第八版仍一併修窄這個問答，待新版獨立重查。本作者紀錄不宣告第八版史料、盲讀、政策或媒體 PASS。

| 凍結輸入 | SHA-256 |
| --- | --- |
| `research.md` | `47642150198fa8dcc9a9991a5be9497dfd1f0db4a3085ff3f7d74f7f53126336` |
| `brief.md` | `b10fa670558f3a0e6fb7296c77ee3979e7faf2d5f9ee22ac3b9172c5ba5b236d` |
| `claims.md` | `0b7d0c2817f57be52f2b05a16771a8984cdf308942f0114cffc8d2cce237eadd` |
| `video.json` | `100128600cbd4027bd2855fb904336fb12655bf203cd370c1a60d0bbcb508726` |
| `script.md` | `b9981a1b503504e48b452b2a37ddc42731ee7a4bcc6096dd6d7f79ec9d25438c` |

精確修訂：`s54104` 原本又說「可貼的郵票尚在印製」，與 `s54075` 重複；現以「**還記得希爾備用的那片附膠紙嗎？現在窗口等的正是它。**」回呼早前希爾的方案並直接回答 `s54103`。主張列另補 [P07／H L13138–13145](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13138-L13145) 的採用與待備妥原文；畫面是政府規劃處的無字紙片樣本，沒有畫一月寄件人已拿到郵票。`s54110` 改問「**三個總局售票的提議，部門一開始怎麼看？**」，緊接 `s54111` 直接回答該部門起初反對；不追問來源未具名的官員或哪一個部門。`research.md` 未變；`brief.md` 僅同步書面字數與估計時長。其餘第七版敘事、史料界線與相鄰畫面不動。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s54` 已重產逐句稿；`lint --slug curio-s54 --json` 回傳 **0 errors、0 warnings**。第八版為 7 章、147 正文場（140 插圖、7 張工具字卡）、23 組 `loops`，另有三句片尾旁白。前八場約 44 秒；排除開頭及片尾，正文 2,630 個漢字，以每分鐘 325 字估算 **8.09 分鐘**。工具全段書面估計 13.89 分鐘，實際片長仍待 TTS。147 列主張與正文場景 ID、文字逐列相符。

沒有合成語音、繪製付費插圖或送出影片。
