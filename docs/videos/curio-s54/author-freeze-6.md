# S54｜作者第六版凍結：三處窄幅修正

2026-10-20 UTC。依 [第五版獨立逐句史料與畫面覆核](review/r5-source-independent.md) 的 HOLD 表格，僅修正 `s54071`、`s54118`、`s54120`；`brief.md` 同步更新兩個漢字造成的書面時長估計。`research.md` 未變。此作者紀錄不宣告新版史料、盲讀、政策或媒體 PASS，請獨立覆核者按下列精確雜湊作差異重查。

| 凍結輸入 | SHA-256 |
| --- | --- |
| `research.md` | `57f24b58a1d407825f71fcd389576ae0ae77e6a547d87b5e1ca8be17863557fa` |
| `brief.md` | `9ee29f8d25d0c3044c2b42e6d3b8982c3f9426b81cef06998d1a4ad25432c4fe` |
| `claims.md` | `a10df345472a8a8f94f9f0ca1dba709211b2a364a70c9ac879b4e6eaff2399dd` |
| `video.json` | `b29d73b97759d575d58c6934c06b2bf8c673c0c60a58330e330518f2b4e5e332` |
| `script.md` | `33ae45c7addd0088918128a5711969c128bbe4b692743b71cc5703f16deb73ef` |

精確修正：

1. `s54071` 把希爾轉錄的主管回報改成「每二十封信，**最多**只有一封得上秤」，保留原文 *not more than one in twenty* 的上限。
2. `s54118` 的主張列除 P09 的售票敘述外，補 [P10／H L13354–13359](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13354-L13359) 的收件所分發直接引證；畫面改為規劃人員移動無字封包和分發板，不預告配發結果。
3. `s54120` 改畫職員查看**闔上的無字庫存簿**，在提問時不揭露短缺。`s54121` 才保留空供應架作答案畫面。`s54118` 和 `s54120` 的旁白文字均未改。

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s54` 已重產逐句稿；`lint --slug curio-s54 --json` 回傳 **0 errors、0 warnings**。第六版仍為 7 章、148 正文場（141 插圖、7 張工具字卡）、22 組 `loops`，另有三句片尾旁白。前八場約 44 秒；排除開頭與片尾的正文為 2,658 個漢字，以每分鐘 325 字估算 **8.18 分鐘**；工具全段書面估計 14.02 分鐘，實際片長仍待 TTS。148 列主張與正文場景 ID、文字逐列相符。

沒有合成語音、繪製付費插圖或送出影片。
