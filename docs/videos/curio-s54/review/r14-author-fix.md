# S54 R14｜封套備貨者主語定點修正

2026-10-20 UTC。[R13 獨立史料／書面畫面覆核](r13-source-independent.md)只對 `s54135` 的「希爾先前備下的大批封套」提出來源 **HOLD**：[Hill H 13390–13399](https://github.com/GITenberg/The-Life-of-Sir-Rowland-Hill-and-the-History-of-Penny-Postage-Vol-I-of-2_59390/blob/b508867f1e1390093789dd72b1d84bcd6bbdaa58/59390-0.txt#L13390-L13399)只寫 *the great stock of covers which had been prepared*，未指出是希爾本人備貨。本紀錄只凍結作者定點修稿，不冒稱獨立來源或敘事 PASS。

| 凍結檔 | SHA-256 |
| --- | --- |
| `brief.md` | `bedc89ef669f9b64868ff3ccea85adb13ee07d75a1ab2120ab6193079f4623f9` |
| `research.md` | `8bd0b5be9efe77b440b3677ba60b26fa97e9b6de47e8fcfc7b3f6284796eb6ae` |
| `claims.md` | `46d2e01f36e1f79263bcf2be686729a48e4dae3e7e628c492bddef3257b133f3` |
| `video.json` | `ab07d7166dc1141a822747dfd43d46675fa9f5c97ce3cff528875df48764a83b` |
| `script.md` | `483558f1617939d109c453ec35f09840ed3de9bcbf0455aa1598433f9b74448f` |

`s54135` 只刪「希爾」兩字，現為：「另一頭的印刷廠也被需求逼緊：先前備下的大批封套，居然派不上多少用場。」`video.json`、`claims.md` 與重產的 `script.md` 三處同步。原本的印量／附膠郵票需求意義及書面畫面保持；`research.md` 的 P11 本來就沒有指明備貨者。`brief.md` 僅按兩個漢字減量把正文改成 2,643 字、工具書面估長 13.92 分鐘、最快估長 8.13 分鐘，沒有更動故事節拍。

全片 145 個敘事場的口播與主張表、劇本各 **145／145 逐字相同**，24 組 loop；開場 153 漢字，正文 2,643 漢字，按 325 字／分鐘為 **8 分 07.94 秒**。`node tools/video/cli.mjs lint --slug curio-s54 --json` 為 **0 errors／0 warnings**、7 章、148 句、工具總估 **13.9194 分鐘**；`git diff --check` 通過。這是書面估算，尚無新版 TTS 實測。

下一關由另一位工作者只核新 `s54135`、主張表與畫面是否合於固定史料；R14 的五檔雜湊也要求兩位完全無先前對話背景的讀者重做 13 題敘事。舊稿 S54 TTS 僅六句草稿快取，`/workspace/.video-work/curio-s54/STOP` 仍在，新版來源與敘事放行前不可續做媒體。
